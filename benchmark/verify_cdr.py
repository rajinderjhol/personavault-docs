#!/usr/bin/env python3
"""
Chapter 4.6, item 6: portable offline verifier.

Verifies a Clinical Decision Receipt (CDR v1) without importing the
PersonaVault application. Depends only on `cryptography` and `json`.

Usage:
    python verify_cdr.py receipt.json

Exit code:
    0 on success, 1 on failure.
"""
import base64
import hashlib
import json
import sys
from typing import Any

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.exceptions import InvalidSignature
except ImportError:
    print("ERROR: the 'cryptography' package is required.", file=sys.stderr)
    print("       pip install cryptography", file=sys.stderr)
    sys.exit(2)


def _canonical_default(obj: Any) -> Any:
    """
    Deterministic default serializer for non-JSON types.

    Mirrors app/services/governance/receipt_interface._canonical_default.
    The two must produce identical bytes for the same input, or the
    offline verifier will disagree with the server on any payload
    that contains a datetime, UUID, or Enum.
    """
    from datetime import datetime, timezone
    from uuid import UUID
    import enum

    if isinstance(obj, datetime):
        if obj.tzinfo is None:
            obj = obj.replace(tzinfo=timezone.utc)
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, enum.Enum):
        return obj.value
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if hasattr(obj, "dict"):
        return obj.dict()
    raise TypeError(
        f"Object of type {obj.__class__.__name__} is not JSON serializable"
    )


def canonical_json(data: Any) -> str:
    """
    Deterministic JSON serialization.

    Identical to app/services/governance/receipt_interface.canonical_json:
    sorted keys, compact separators, Unicode preserved, and a default
    handler for datetimes, UUIDs, and Enums.

    `None` values are emitted as `null`, not dropped. Dropping them
    produces a different hash than the server, which is the bug this
    implementation fixes.
    """
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=_canonical_default,
    )


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _b64(s: str) -> bytes:
    return base64.b64decode(s, validate=True)


class Failure(Exception):
    def __init__(self, check: str, reason: str):
        self.check = check
        self.reason = reason
        super().__init__(f"{check}: {reason}")


def verify(receipt: dict) -> list[str]:
    """Return a list of check names that passed. Raise Failure on first failure."""
    passed: list[str] = []

    # 1. Schema versions
    if receipt.get("schema_version") != "cdr.v1":
        raise Failure(
            "Schema version",
            f"expected 'cdr.v1', got {receipt.get('schema_version')!r}",
        )
    cdo = receipt.get("cdo_payload") or {}
    # Prefer the exact canonical bytes if the CDR includes them.
    # They are the bytes that were hashed at signing time and are
    # immune to re-serialization drift (e.g. FastAPI JSON converting
    # whole-number floats 0.0 -> 0). See BACKEND_WIRING_PLAN.md
    # Sprint 0.5.
    cdo_canonical_str = receipt.get("cdo_payload_canonical")
    if cdo.get("schema_version") != "cdo.v1":
        raise Failure(
            "CDO schema version",
            f"expected 'cdo.v1', got {cdo.get('schema_version')!r}",
        )
    passed.append("Schema version")

    # 1b. The knowledge state's snapshot — the entries' sorted
    # 2. CDO hash
    if isinstance(cdo_canonical_str, str):
        import hashlib as _hl
        cdo_hash = _hl.sha256(cdo_canonical_str.encode("utf-8")).hexdigest()
    else:
        # Fallback: old CDRs without canonical bytes. Re-canonicalize
        # the dict. This may fail verification for payloads with
        # whole-number floats — that is expected for the four legacy
        # CDRs produced before 2026-10-21.
        cdo_hash = canonical_hash(cdo)
    if cdo_hash != receipt.get("cdo_hash"):
        raise Failure(
            "CDO hash",
            f"recomputed {cdo_hash[:16]}… != claimed {str(receipt.get('cdo_hash'))[:16]}…",
        )
    passed.append("CDO hash")

    # 2b. The knowledge state's snapshot — the entries' sorted
    # (kind, source, version, content_hash) tuples. A legacy CDR
    # with no knowledge state (empty snapshot, empty entries)
    # passes — the check is the snapshot's integrity, not its
    # presence.
    ks = (cdo.get("knowledge_state") or {}) if isinstance(cdo, dict) else {}
    claimed_snapshot = ks.get("snapshot_hash") or ""
    _entries = ks.get("entries") or []
    if claimed_snapshot or _entries:
        _tuples = sorted([
            [str(e.get("kind") or ""), str(e.get("source") or ""),
             str(e.get("version") or ""), str(e.get("content_hash") or "")]
            for e in _entries if isinstance(e, dict)
        ])
        _actual = canonical_hash(_tuples)
        if _actual != claimed_snapshot:
            raise Failure(
                "knowledge_state.snapshot_hash",
                f"the entries' hash is {_actual[:16]}…; "
                f"the claimed is "
                f"{claimed_snapshot[:16] if claimed_snapshot else '(empty)'}",
            )
        passed.append("knowledge_state.snapshot_hash")

        # 2b. Provenance completeness — every entry's availability is
        # one of the five declared values, and the counts are
        # internally consistent. The universe itself is whatever the
        # CDO declares; the check is completeness against that
        # declaration, not against an external ideal.
        # The five-state availability vocabulary. Inlined rather
        # than imported so this verifier stays offline (no app import).
        # Must stay in sync with
        # app/services/governance/knowledge_state.py:AVAILABILITY_VALUES.
        _AVAIL = {
            "available",
            "referenced",
            "generated",
            "retrieved_but_excluded",
            "unavailable",
        }
        for _e in _entries:
            _a = _e.get("availability")
            if _a not in _AVAIL:
                raise Failure(
                    "Provenance completeness",
                    f"entry {str(_e.get('kind', ''))[:32]}… carries "
                    f"unknown availability {_a!r}",
                )
        _u = ks.get("declared_universe")
        if _u:
            _avail_n = int(_u.get("available_count", 0))
            _ret_n = int(_u.get("retrieved_count", 0))
            if _ret_n > _avail_n:
                raise Failure(
                    "Provenance completeness",
                    f"retrieved_count {_ret_n} > available_count {_avail_n}",
                )
        passed.append("Provenance completeness")

    # 2c. Consent reference. Inlined (the verifier is offline and
    # standalone; it cannot import from tools/). Must stay in sync
    # with tools/_verify_consent.py:check_consent.
    _consent = cdo.get("consent") or {}
    _ref_kind = _consent.get("ref_kind")
    _status = _consent.get("status_at_decision")
    if _ref_kind == "fhir_consent":
        if _status in ("inactive", "revoked", "rejected"):
            raise Failure(
                "Consent",
                f"consent status at decision was {_status!r}",
            )
        if _consent.get("ref_hash"):
            passed.append("Consent reference (unresolved)")
        else:
            passed.append("Consent reference")
    else:
        passed.append("Consent (pack basis)")

    # 3. Signed payload hash
    attestation = receipt.get("attestation") or {}
    if cdo_hash != attestation.get("signed_payload_hash"):
        raise Failure(
            "Attestation signed payload hash",
            f"CDO hash {cdo_hash[:16]}… != signed_payload_hash "
            f"{str(attestation.get('signed_payload_hash'))[:16]}…",
        )
    passed.append("Attestation signed payload hash")

    # 4. Ed25519 signature
    chair = receipt.get("chair") or {}
    pub_b64 = chair.get("public_key_b64")
    sig_b64 = attestation.get("signature_b64")
    if not pub_b64 or not sig_b64:
        raise Failure(
            "Ed25519 signature",
            "missing public_key_b64 or signature_b64",
        )
    try:
        pub = Ed25519PublicKey.from_public_bytes(_b64(pub_b64))
        pub.verify(_b64(sig_b64), bytes.fromhex(cdo_hash))
    except InvalidSignature:
        raise Failure(
            "Ed25519 signature",
            "signature does not verify against the provided public key",
        )
    except Exception as e:
        raise Failure("Ed25519 signature", str(e))
    passed.append("Ed25519 signature")

    # 5. Transcript hash
    transcript = receipt.get("transcript") or {}
    if transcript:
        t_hash = canonical_hash(transcript.get("payload") or {})
        if t_hash != transcript.get("content_hash"):
            raise Failure(
                "Transcript hash",
                "recomputed transcript hash does not match the receipt",
            )
        passed.append("Transcript hash")

        # 6. Transcript binding
        cdo_delib = cdo.get("human_deliberation") or {}
        if cdo_delib.get("transcript_hash") and cdo_delib["transcript_hash"] != t_hash:
            raise Failure(
                "Transcript binding",
                "transcript hash does not match the CDO's deliberation binding",
            )
        passed.append("Transcript binding")

    # 6b. Pre-AI commitment — Events 2 and 3. Inlined (the verifier
    # is offline and standalone). Must stay in sync with
    # tools/_verify_pre_ai.py:check_pre_ai_commitment.
    _ai_rec = cdo.get("ai_recommendation") or {}
    if bool(_ai_rec.get("policies")):
        _pac = cdo.get("pre_ai_commitment")
        _pai = cdo.get("pre_ai_assessment")
        if not _pac or not _pai:
            raise Failure(
                "Pre-AI commitment",
                "the CDO carries AI policies but no pre-AI commitment — "
                "the disclosure gate did not fire",
            )
        _canonical_plan_str = json.dumps(
            {"plan_text": _pai.get("plan_text"),
             "plan_structured": _pai.get("plan_structured") or {}},
            sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        )
        _expected_hash = hashlib.sha256(
            _canonical_plan_str.encode("utf-8")
        ).hexdigest()
        if _pac.get("plan_hash") != _expected_hash:
            raise Failure(
                "Pre-AI commitment",
                f"plan_hash {str(_pac.get('plan_hash', ''))[:16]}… != "
                f"recomputed {_expected_hash[:16]}…",
            )
        _committed = _pac.get("committed_at")
        _captured = (cdo.get("knowledge_state") or {}).get("captured_at")
        if _committed and _captured and _committed >= _captured:
            raise Failure(
                "Pre-AI commitment",
                f"committed_at {_committed} does not precede "
                f"knowledge_state.captured_at {_captured}",
            )
        passed.append("Pre-AI commitment")

    # 7. Record hash
    record = receipt.get("record") or {}
    if record:
        record_canonical_str = record.get("payload_canonical")
        if isinstance(record_canonical_str, str):
            import hashlib as _hl
            r_hash = _hl.sha256(record_canonical_str.encode("utf-8")).hexdigest()
        else:
            # Fallback for legacy CDRs produced before the
            # payload_canonical field existed. Re-canonicalization may
            # drift on whole-number floats; those CDRs fail as
            # expected and no retrofit is attempted.
            r_hash = canonical_hash(record.get("payload") or {})
        if r_hash != record.get("content_hash"):
            raise Failure(
                "Record hash",
                "recomputed record hash does not match the receipt",
            )
        # Cross-check: if payload_canonical is present, it must describe
        # the same object as payload. Otherwise a consumer reading
        # record.payload sees different bytes than the verifier hashed.
        # This closes the F3 tamper gap: mutating payload while leaving
        # payload_canonical intact was previously undetected.
        if isinstance(record_canonical_str, str):
            try:
                payload_from_canon = json.loads(record_canonical_str)
            except Exception:
                raise Failure("Record hash", "payload_canonical is not valid JSON")
            if payload_from_canon != record.get("payload"):
                raise Failure("Record hash", "record.payload does not match record.payload_canonical")
        passed.append("Record hash")

    # 8. Version chain
    vc = receipt.get("version_chain") or cdo.get("version_chain") or {}
    version = vc.get("version")
    prior = vc.get("prior_cdo_hash")
    if version == 1 and prior is not None:
        raise Failure(
            "Version chain",
            "version 1 must have prior_cdo_hash == null",
        )
    if version and version > 1 and not prior:
        raise Failure(
            "Version chain",
            f"version {version} must have a prior_cdo_hash",
        )
    passed.append("Version chain")

    # 9b. Attestation timestamp present and >= decided_at
    # Per ADR 0029: the CDR's attestation block carries the
    # authoritative signing time (the CDO's own attestation.attested_at
    # is null for cdo.v1). This check ensures the timestamp is
    # present and not before the decision was made.
    attested_at = (receipt.get("attestation") or {}).get("attested_at")
    if not attested_at:
        raise Failure(
            "Attestation timestamp",
            "attestation.attested_at is missing from the CDR",
        )
    decided_at = ((receipt.get("cdo_payload") or {})
                  .get("human_decision") or {}).get("decided_at")
    if decided_at and attested_at < decided_at:
        raise Failure(
            "Attestation timestamp",
            f"attested_at {attested_at[:19]} is before decided_at {decided_at[:19]}",
        )
    passed.append("Attestation timestamp")

    # 9. AI provenance graph (optional, present from Chapter 4.7)
    provenance = cdo.get("ai_provenance") or {}
    if provenance:
        nodes = provenance.get("nodes") or []
        # Sanity: every node has a node_id and a kind.
        for n in nodes:
            if not n.get("node_id") or not n.get("kind"):
                raise Failure(
                    "AI provenance graph",
                    f"node missing node_id or kind: {n}",
                )
        passed.append("AI provenance graph")

    return passed


def main():
    if len(sys.argv) != 2:
        print("Usage: python verify_cdr.py receipt.json", file=sys.stderr)
        sys.exit(2)

    path = sys.argv[1]
    try:
        with open(path) as f:
            receipt = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON: {e}", file=sys.stderr)
        sys.exit(2)

    cdo = receipt.get("cdo_payload") or {}
    case = receipt.get("case") or {}
    chair = receipt.get("chair") or {}

    print("CLINICAL DECISION RECEIPT")
    print(f"  case:       {case.get('case_id') or cdo.get('case_identity', {}).get('case_id') or '(unknown)'}")
    print(f"  chair:      {chair.get('actor_id') or '(unknown)'} (Ed25519)")
    print(f"  issued:     {receipt.get('issued_at') or '(unknown)'}")
    print()

    try:
        passed = verify(receipt)
    except Failure as f:
        # Print the checks that passed before the failure
        print(f"  ✗ {f.check} — {f.reason}")
        print()
        print("DECISION INTEGRITY: INVALID")
        print(f"  Failed at: {f.check}")
        print(f"  Reason: {f.reason}")
        sys.exit(1)

    for check in passed:
        print(f"  ✓ {check}")

    # Print the AI provenance node list (from Chapter 4.7).
    provenance = cdo.get("ai_provenance") or {}
    nodes = provenance.get("nodes") or []
    if nodes:
        print()
        print("AI PARTICIPANTS")
        for n in nodes:
            kind = n.get("kind", "?")
            model = n.get("model", "?")
            provider = n.get("provider", "?")
            version = n.get("model_version", "")
            model_class = n.get("model_class")
            label = f"{kind}"
            if model_class:
                label += f" ({model_class})"
            print(f"  · {label}: {model} v{version} via {provider}")

    print()
    print("DECISION INTEGRITY: VALID")
    sys.exit(0)


if __name__ == "__main__":
    main()
