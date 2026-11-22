# Independent Verifier Challenge Kit

A frozen CDR and its one-character tampered twin, plus a browser verifier with no network access, no account, and no platform dependency. The purpose is adversarial review: try to make the verifier accept the tampered receipt, reject the valid one, or say something it should not.

This is the canonical kit. The copies in `academic/defensible-autonomy/exhibits/` are frozen paper exhibits and are not updated when this kit changes.

## Contents

| File | Role |
|---|---|
| `receipt-valid.json` | Signed `cdr.v1` receipt, 82,634 bytes |
| `receipt-tampered.json` | Same receipt with one changed character in a source document's content hash |
| `verify_cdr_standalone.html` | Self-contained browser verifier; no external scripts, styles, fetches, or network calls |
| `CHECKSUMS.sha256` | SHA-256 of the three files above |

Verify the frozen bytes first:

```sh
cd challenge-kit
shasum -a 256 -c CHECKSUMS.sha256
```

## Try it

1. Open `verify_cdr_standalone.html` in a browser with no network connection.
2. Load `receipt-valid.json`. Expected: `DECISION INTEGRITY: VALID`, 16 passed checks.
3. Load `receipt-tampered.json`. Expected: integrity failure at `knowledge_state.entry.content_hash`.

A node-based check of the same verifier logic is what the implementation repository's `tests/test_challenge_kit.py` runs. It asserts exactly 16 passes for the valid receipt, rejection of the tampered receipt at `knowledge_state.entry.content_hash`, and that the two receipts differ by exactly one character in canonical JSON.

### A known mismatch — read before using the Python verifier

`benchmark/verify_cdr.py` is an **older, frozen snapshot** of the verifier. It predates the `knowledge_state.entry.content_hash` check and therefore reports `DECISION INTEGRITY: VALID` for `receipt-tampered.json`. Use the bundled HTML verifier — or the current verifier in the private implementation repository — when testing this kit. This mismatch is logged as `KIT-001` in `FINDINGS.md`.

## What the verifier checks

The 16 pass-labels cover: schema version, CDO hash, `knowledge_state.snapshot_hash`, knowledge-state entries, provenance completeness, consent basis, attestation payload hash, Ed25519 signature, system receipt signature, transcript hash, transcript binding, pre-AI commitment, record hash, version chain, attestation timestamp, and AI provenance graph. Canonicalization is sorted keys with compact separators; the Ed25519 signature is over the raw 32 bytes of the payload hash.

## What a valid result proves

- The signed payload's bytes have not changed relative to the signature.
- The signature validates under the public key embedded in the receipt.
- The declared evidence entries carry content hashes consistent with the snapshot hash.
- The transcript is bound to the CDO, the record hash matches its payload, the version chain is consistent, and a pre-AI commitment was recorded before the knowledge snapshot.
- The receipt names the chair, the subject, the case, and the AI participants that produced the advice.

## What a valid result does **not** prove

- **Clinical or factual truth.** A well-formed receipt can document a bad decision; the AI's claims inside it may be false.
- **Signer identity.** The key is named, not enrolled or vouched for by the verifier.
- **Execution.** That the recorded order was carried out. This receipt proves *attested*, not *executed*.
- **Completeness.** That the declared evidence universe contained everything relevant.
- **Absence of automation bias.** That the human critically evaluated the AI's advice.
- **Replay resistance or external anchoring.** There is no transparency log, no external trust anchor, and no notarization.
- **Court admissibility.** No legal conclusion follows from a verifier exit code.

## Scope limits of this particular kit

- It is **frozen**. The standalone verifier does not include checks added to the implementation after the freeze; new checks need a new kit version.
- The receipt is a **harness-generated adoption case**. The chair adopted the AI's item while ordering a different regimen; this is an internal inconsistency, not a defensible override. See Exhibit B in the paper for a signed override scenario.
- Its pre-AI `plan_text` is a harness test plan, and some AI-provenance fields are `unspecified` placeholders. These are honest fixture artifacts, not hidden defects.
- It tests **one tamper class**: a single-character change to a content hash. It is not a general robustness suite.

## Reporting a finding

Open an issue using the **Challenge finding** template. Include:

- which file and verifier you used, with its checksum or version;
- the exact command or UI steps, and the observed versus expected output;
- whether you believe the result is a **false accept**, **false reject**, **crash**, **ambiguous message**, or **documentation mismatch**;
- the minimum reproduction you can share.

Do not include private patient, client, or subject data. Confirmed findings are credited in `FINDINGS.md` unless you ask to remain anonymous.

Suggestions that are not findings (but are welcome as issues): new tamper classes, clearer wording, additional pass-labels with a rationale for why they belong in integrity rather than advisory review.

A claim that "the receipt is valid, therefore the decision was correct" is a scope misunderstanding, not a verifier bug.
