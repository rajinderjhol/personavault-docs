# Decision-evidence benchmark, v0

Ten artifacts for one synthetic decision, checked with the bundled offline verifier. The benchmark reports **which artifact class passes which checks**. It does not rank them: an artifact that fails more checks is not worse, it is a different kind of object. An audit log is not a CDR, and the CDR verifier is not the right tool for it.

This benchmark is the runnable companion to [Beyond AI Audit Trails](../academic/three-foundations/paper.md) §12.

## Run it

```sh
cd benchmark
./verify_demo.sh                      # the reference case only
```

To reproduce the full table with the bundled verifier:

```sh
cd benchmark
for f in [a-j]-*.json; do
  echo "== $f"
  python3 verify_cdr.py "$f" | grep -E 'DECISION INTEGRITY|Failed at'
done
```

`verify_cdr.py` depends only on `cryptography` and `json`. Exit code 0 means every check it knows about passed; 1 means a check failed.

### Verifier version — read this first

The bundled `verify_cdr.py` is a **frozen snapshot** with fourteen checks. It predates several checks in the current implementation, including `knowledge_state.entry.content_hash`. As a result it reports `DECISION INTEGRITY: VALID` for the tampered receipt in the [challenge kit](../challenge-kit/README.md); that mismatch is logged as `KIT-001`. The results below are what this bundled script produces and are reproducible. Do not read them as the output of the current production verifier.

## The records and observed outcomes

| Record | Artifact class | Bundled verifier result | What it demonstrates |
|---|---|---|---|
| `a-audit-log.json` | Conventional audit log | `INVALID` — fails `Schema version` | Not a CDR. The failure means "wrong artifact class", not "bad CDR". |
| `b-signed-no-sequence.json` | Signed record, no pre-AI blocks | `INVALID` — fails `Pre-AI commitment` | A valid signature does not establish that the human judged first. |
| `c-sequence-no-authority.json` | Full sequence, no authority block | **`VALID` — 14 checks** | See finding 1: sequence evidence can pass every check without authority evidence. |
| `d-authority-no-sequence.json` | Authority blocks, no pre-AI sequence | `INVALID` — fails `Pre-AI commitment` | Authority without sequence cannot prove independence. |
| `e-vdr.json` | Complete pipeline-produced CDR | `VALID` — 13 checks; `Pre-AI commitment` does not run | See finding 2: the check is keyed on AI policies, which this query did not fire. |
| `f-vdr-stripped.json` | Reference case with commitment stripped, re-signed | `INVALID` — fails `Pre-AI commitment` | The tampering-detection state: stripping the commitment is caught. |
| `g-hash-consistent-tampered.json` | Decision content changed and hashes recomputed, signature not renewed | `INVALID` — fails `Attestation signed payload hash` | The attestation binding, not the self-consistent CDO hash, is the tamper detector. |
| `h-backdated-knowledge.json` | Evidence snapshot backdated before the commitment, re-signed | `INVALID` — fails `Pre-AI commitment` (ordering branch) | The check catches a timeline tamper, not just an absent block. |
| `i-fabricated-transcript.json` | Transcript segment rewritten, hash left intact | `INVALID` — fails `Transcript hash` | The transcript is bound to the signed record. |
| `j-revoked-consent.json` | Consent marked revoked with a FHIR reference | `INVALID` — fails `Consent` | Consent status is checked when the record declares a FHIR consent reference. |

## Findings worth knowing before reading the paper

**1. Record `c` passes all fourteen checks with no authority block.** It has no `consent`, no `disclosure`, and no `trust_anchor`, yet it passes as `Consent (pack basis)`, and no check requires the other two to exist. A human using the deliberation room cannot reach this state: `seed_decision` refuses to create a draft when the session has no pre-AI commitment message. Record `c` is producible only by a direct pipeline call. The gap is between what the verifier checks and what the workflow prevents — three layers, three different mechanisms.

**2. Record `e` passes 13, not 14.** It carries a valid `pre_ai_commitment`, but `ai_recommendation.policies` is empty because the packs fired no policies for that query. The verifier only runs its pre-AI check when policies are present. The CDO carries `incomplete: pre_ai_commitment_missing`; the verifier does not read that field. A signature can therefore be valid while the sequence check never ran.

**3. The consent check has four paths, three of which pass.** A FHIR consent with status inactive, revoked, or rejected fails. A FHIR consent with a reference hash passes as `Consent reference (unresolved)`; one without a hash passes as `Consent reference`; and any record with no consent block, or another `ref_kind`, passes as `Consent (pack basis)`. The status branch fires only for `fhir_consent`.

## What the benchmark does not claim

- That any record is clinically correct, or that a passing verifier means a good decision.
- That the declared evidence universe was complete, or that the AI's claims were true.
- That the frozen verifier includes every check in the current implementation.
- That the zero-record case is achievable through the UI — the workflow gate is a separate control from the verifier.
