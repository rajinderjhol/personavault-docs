# Clinical Decision Receipt Specification (CDR 1.0)

> The open receipt spec. Publishable when complete.

**Status:** `draft`

---

## Status

This document is a draft. It describes the shape the CDR 1.0
specification will take when the underlying schema is stable. It is
not yet a standard and should not be cited as one.

## Purpose

The CDR is the signed, portable projection of a Clinical Decision
Object. It is what leaves the system that produced it, and it is
what a stranger verifies without trusting that system.

The CDR 1.0 specification defines:

- The wire format of a receipt.
- The canonicalization rules.
- The signature algorithm.
- The verification procedure.
- The set of errors a verifier can report.

## The wire format

A receipt is a JSON document. Its top-level fields are defined in
`02-architecture/the-receipt.md`. The schema is `cdr.v1`.

The receipt is self-contained: it carries everything a verifier
needs, including the chair's public key and the payloads whose
hashes it binds.

### `knowledge_state.entries` — the evidence the decision was grounded in

Each entry names one source the decision drew on. The fields:

| Field | Values |
|---|---|
| `kind` | `case_document`, `policy`, `clinical_record`, `guideline`, `precedent`, `context`, or the spec's non-evidence kinds (`ai_output`, `ontology_entity`, `pack_knowledge`, `patient_data`, `pathology`, `imaging`, `genomic`, `literature`, `retrieved_passage`, `pattern`). |
| `source` | The document's name, as a human reads it. |
| `content_hash` | The sha256 of the entry's `metadata.content`. |
| `metadata.scope` | `case` or `environment`. |
| `metadata.authority` | `grounding`, `binding`, `advisory`, `precedent`, or `contextual`. |
| `metadata.content` | The retrieved chunk's text, up to 2000 characters. **This is what the AI was shown.** |
| `metadata.episode_id` | The `ontology_episodes` row the chunk came from. |

The `content_hash` is the sha256 of `metadata.content`. The verifier
recomputes it and compares. A one-character change to the chunk
fails verification.

The `snapshot_hash` on `knowledge_state` is the canonical hash of
the sorted `(kind, source, version, content_hash)` tuples of every
entry. A change to any entry's hash changes the snapshot; a change
to any chunk changes the entry's hash. The chain is: chunk bytes →
entry hash → snapshot → CDO hash → chair signature.

The entry commits to the **chunk** the AI read, not the whole
document. The document's own content hash is on its `source_documents`
row; a reader who wants to check the whole document unchanged checks
that row, with database access. The receipt's claim is bounded and
exact: *the AI was shown these bytes, and the chair signed the hash
of them.*

## Canonicalization

The canonicalization rules are in
`02-architecture/the-verification-protocol.md`. They are the
critical part of the standard, because two implementations that
disagree on canonicalization produce different hashes for the same
semantic content, and verification fails.

Summary:

- Sort object keys.
- Remove insignificant whitespace.
- Normalize strings to NFC.
- Normalize numbers (no trailing zeros).
- Escape exactly the required characters.
- Encode as UTF-8, no BOM.

## Signature

`Ed25519` over the raw 32 bytes of the SHA-256 canonical hash of the
signed payload. The signed payload is the CDO's payload excluding
`attestation`, `version_chain`, `actions`, `outcome`, and
`integrity`.

The public key is 32 bytes, base64-encoded. The signature is 64
bytes, base64-encoded. See
`02-architecture/the-verification-protocol.md` for the exact
verification sequence.

## Verification

The verifier walks the sequence in
`02-architecture/the-verification-protocol.md`. On success, it
prints a report and exits with status 0. On failure, it names the
specific check that failed and exits with status 1.

## Errors

The set of errors the verifier can report is part of the standard:

| Error | Meaning |
|---|---|
| `schema_version_mismatch` | The receipt does not declare `cdr.v1`. |
| `cdo_schema_version_mismatch` | The CDO does not declare `cdo.v1`. |
| `cdo_hash_mismatch` | The recomputed CDO hash does not match the receipt. |
| `signed_payload_hash_mismatch` | The recomputed signed payload hash does not match the attestation. |
| `signature_verification_failed` | The Ed25519 signature does not verify. |
| `transcript_hash_mismatch` | The recomputed transcript hash does not match. |
| `transcript_binding_mismatch` | The transcript hash does not match the CDO's deliberation binding. |
| `record_hash_mismatch` | The recomputed record hash does not match. |
| `record_binding_mismatch` | The record hash does not match the CDO's decision binding. |
| `version_chain_inconsistent` | The version chain link is missing or invalid. |
| `prior_version_missing` | A referenced prior version is not present. |
| `dqi_mismatch` | The recomputed DQI does not match the attached value. |
| `knowledge_state_entry_kind` | An entry's `kind` is not a known evidence kind. |
| `knowledge_state_entry_hash_mismatch` | An entry's `content_hash` is not the sha256 of its `metadata.content`. A tampered chunk fails here, with the source named. |

A verifier must not report an error outside this set. If it detects
a condition not covered by an error, the condition is a defect in
the receipt that the standard does not yet address, and the verifier
reports `unknown_error` with a description.

## Test vectors

The standard will include a set of test vectors:

- A canonical valid receipt.
- A receipt with one byte changed in the CDO.
- A receipt with the signature replaced by a signature over
  different bytes.
- A receipt with a valid signature but a mismatched transcript hash.
- A receipt with a broken version chain.

Two independent verifiers must agree on the outcome of every test
vector. This is the conformance test.

## What is deliberately not in the standard

- **Clinical correctness.** The standard does not evaluate the
  decision.
- **Regulatory admissibility.** The standard defines a valid
  receipt; it does not define whether a specific regulator accepts
  it.
- **Key trust.** The standard assumes the public key in the receipt
  is the correct key. Establishing that is a separate problem (key
  enrollment, revocation, trust anchors).

## The one-sentence statement

**CDR 1.0 is the specification for a self-contained, cryptographically
verifiable clinical decision receipt, implementable by anyone and
verifiable by a stranger.**
EOF