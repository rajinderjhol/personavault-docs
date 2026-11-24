# Third-party audit path

> **Who this is for:** an internal audit function, a second-line reviewer, an
> external auditor, or a regulator who needs to form their own opinion about
> PersonaVault's decision evidence.
>
> **What this is not:** a certification, a SOC 2 report, or a claim that an
> independent party has already audited the implementation. PersonaVault makes
> **no T2 claim of its own**. The artifacts below let an auditor *produce* a
> T2 opinion; they do not substitute for one.

## 1. Evidence tiers, placed honestly

The GAISSF insurance evidence catalogue distinguishes primary operating
evidence (T1) from vendor white papers (T4, "insufficient alone"). Here is
where each PersonaVault artifact sits:

| Tier | Meaning | PersonaVault artifacts |
|---|---|---|
| **T1** | Primary verified operating evidence: automated logs, immutable decision trails, access records | Signed CDRs, governance event ledger, append-only disclosure views, append-only subject contestations, frozen challenge kit |
| **T2** | Independent or second-line verified evidence: model-risk validation, internal audit, privacy/legal/security review | **None supplied by PersonaVault.** This is the auditor's own work product |
| **T3** | Controlled simulation / adversarial exercise | Challenge kit's one-character tampered twin; the 10-record benchmark with its known `KIT-001` caveat |
| **T4** | Vendor benchmarks, papers, white papers | Everything in `academic/` and `whitepapers/` — useful framing, insufficient alone |

A reviewer should not cite a PersonaVault paper as T1 evidence. The receipt
and the kit are T1; the argument about them is T4.

## 2. What is independently checkable, and what is not

| Check | Artifact | Verifiable by the auditor | Requires vendor trust |
|---|---|---|---|
| A signed receipt's bytes and signature | [Challenge kit](../challenge-kit/README.md) | Yes — offline, no account, no network | No |
| A one-character content change fails verification | Tampered twin in the kit | Yes — same verifier, expected failure at `knowledge_state.entry.content_hash` | No |
| Canonicalization is deterministic across two implementations | Python tests + standalone HTML verifier | Partly — frozen artifacts only; parity is artifact-scoped | No for the kit; yes for future receipts |
| Exact bytes shown to the AI are bound to the signature | [CDR specification](../protocols/cdr/v1/specification.md) §`knowledge_state.entries` | Yes — recompute `content_hash` → `snapshot_hash` → chain | No |
| The declared evidence universe was complete | Completeness attestation in the receipt | The attestation is checkable; the declaration's completeness is not | Partly |
| The decision was clinically correct | — | **No.** DQI is documentation quality; no outcome evidence exists | — |
| The implementation matches the verifier's assumptions | Code and tests | No — implementation is in a private repository | Yes |
| The signer key belongs to the named institution | Self-published signer anchor | The binding is checkable when an anchor is supplied; its provenance is not | Yes — same installation publishes the anchor |
| A subject's challenge was recorded and not rewritten | Subject contestation chain | For a deployment with data access; method described below | Partly |

## 3. Runbook — what an auditor can run today

```sh
# A. Verify the frozen kit has not changed.
cd challenge-kit
shasum -a 256 -c CHECKSUMS.sha256

# B. Verify offline in a browser with the network disabled.
#    Open verify_cdr_standalone.html, then:
#      receipt-valid.json    -> DECISION INTEGRITY: VALID (16 pass-labels)
#      receipt-tampered.json -> fails at knowledge_state.entry.content_hash

# C. Reproduce the artifact-class benchmark.
cd ../benchmark
./verify_demo.sh
#    Read benchmark/README.md first: the bundled verifier is a frozen
#    older snapshot and KIT-001 documents its disagreement with the kit.
```

For a live deployment, additionally request from the operator:

1. A production receipt and the current implementation verifier output.
2. The signer anchor document from `/.well-known/personavault-trust-anchor.json`
   and the `Signer anchor` check result.
3. A hash-bound disclosure view for a receipt with sensitive narrative —
   confirm `source_receipt_hash`, the redaction manifest and that the original
   receipt still verifies.
4. A subject contestation chain (if the deployment uses it) — confirm each
   revision preserves `statement` and `statement_hash` and that status changes
   are appended, not edited.
5. The [conformance self-assessment](conformance.md),
   [claim matrix](../references/claim-matrix.md) and
   [mitigation register](../references/mitigation-register.md) as the vendor's
   own claims to test against, not as findings.

## 4. Scope of an audit opinion

An auditor can reasonably opine that:

- a supplied receipt is internally consistent and its signature verifies;
- a one-character change is detected;
- the verifiers agree on the frozen artifacts;
- the redacted view is the declared projection of the original;
- a contestation chain is append-only by construction.

An auditor cannot opine on this evidence alone that:

- the AI's claims were true or the evidence universe complete;
- the decision was clinically appropriate;
- the running implementation matches the verifier's assumptions;
- the signer anchor was obtained through a trusted channel;
- the deployment is sovereign in the SEAL sense (see the
  [sovereign decision evidence pack](sovereign-decision-evidence.md)).

## 5. Maturity statement

There is no third-party audit, accreditation or certification of PersonaVault
today. The private product risk register tracks this as an open item; the public
[STATUS.md](../STATUS.md) *Claim boundaries* section states it without qualifier.
When an external opinion exists, this page will name the auditor, scope and
date — and will not generalise a component-level result into a product claim.

## Related

- [Conformance self-assessment](conformance.md)
- [Sovereign decision evidence pack](sovereign-decision-evidence.md)
- [Claim boundaries](../references/claim-boundaries.md) and [claim matrix](../references/claim-matrix.md)
- [Challenge kit](../challenge-kit/README.md) and [benchmark](../benchmark/README.md)
