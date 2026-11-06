# Beyond AI Audit Trails

**The three foundations of verifiable decision evidence — and a benchmark that tests whether they hold.**

A signed decision record proves who signed it. It does not prove that the human formed an independent judgment before the AI spoke. It does not prove what evidence was available and skipped. It does not prove the signer had the authority to act on the specific decision the record documents.

This repository contains two artifacts. A paper that argues those are three separate evidence claims — **sequence**, **provenance**, and **authority** — and that no existing lineage carries all three. And a benchmark that runs an offline verifier against ten evidence records for one decision, so a reader can check the paper's claims against a runnable artifact rather than taking them on trust.

## Read the paper

[`three-foundations.md`](three-foundations.md) — v3.3, 2026-11-06.

The paper makes four claims:

1. **Sequence, provenance, and authority are orthogonal.** They answer different questions, fail in different ways, and are verified by different mechanisms. A record can answer one and fail the others.
2. **No lineage identified in the survey carries all three at the implemented-and-verified level.** The Decision-Sequence Evidence Schema is sequence-rich and authority-deferred. The Agent Passport System is authority-rich and sequence-light. The Decision Object is a component taxonomy without temporal ordering. The Receipt Layer, in the Clinical Decision Object, is the only lineage the survey identifies that architectures all three.
3. **The Clinical Decision Object implements the framework, partially.** Sequence and provenance are independently verifiable by an offline verifier. Authority is implemented for one reference (consent) and specified for five. The collective case is open.
4. **The framework invites falsification.** An existing architecture that can independently establish sequence, provenance, and authority for a consequential AI-assisted decision would defeat the comparative claim. The conditions are stated in Section 11.

## Run the benchmark
cd benchmark
./verify_demo.sh

text

That runs the offline verifier against the paper's reference case. The output ends with `DECISION INTEGRITY: VALID` and lists `Pre-AI commitment` among the passed checks.

The benchmark's full table — ten records, ten artifact classes, seven failure modes — is in [`benchmark/README.md`](benchmark/README.md). The short version:

| Record | Result | What it shows |
|---|---|---|
| A conventional audit log | not a CDR | A log is not evidence a stranger can verify. |
| A signed record with no pre-AI sequence | fails `Pre-AI commitment` | A signature does not establish that the human judged first. |
| A complete sequence with no authority | passes all 14 | The verifier checks sequence, not authority. |
| An authority record with no sequence | fails `Pre-AI commitment` | Authority without sequence cannot prove independence. |
| The reference case (pipeline-produced) | passes 13 of 14 | `Pre-AI commitment` is skipped because the pack fired no policies. See below. |
| The reference case with the commitment stripped | fails `Pre-AI commitment` | Tampering is detected. |
| A record whose payload was re-hashed to match tampering | fails `Attestation signed payload hash` | The attestation binding, not the hash, is the tamper-detector. |
| A record whose knowledge state was backdated | fails `Pre-AI commitment` (ordering branch) | The ordering check catches a timeline tamper. |
| A record whose transcript was fabricated | fails `Transcript hash` | The check catches a naive fabricator; a recomputed hash would pass (see `i-alt` in the benchmark README). |
| A `fhir_consent` record with revoked consent | fails `Consent` | The status check fires for `fhir_consent` records. |

## The finding worth knowing before reading the paper

The benchmark was built after the paper's first draft and before circulation. It found three places where the paper's claims were narrower in the code than in the prose. The paper now says what the code does, and the corrections are visible in the text:

- The verifier's `Pre-AI commitment` check is keyed on the AI recommendation's policies, not on the pre-AI commitment. A record that carries a valid commitment but no policies passes the check silently.
- The pre-AI check has two failure branches — absence and ordering — not one.
- The consent status check fires only for records whose `consent.ref_kind` is `fhir_consent`.

Each correction cites a benchmark record that demonstrates it. The paper's Section 5.3 names the provenance of the corrections.

## Repository structure
three-foundations.md the paper (v3.3)
benchmark/ the ten evidence records and the offline verifier
README.md what each record contains and what it demonstrates
verify_cdr.py the offline verifier (imports only cryptography)
passing.cdr.json the reference-case CDR
verify_demo.sh runs the verifier against passing.cdr.json

text

## What this repository is not

It is not a product. The paper's Section 1.4 is explicit about what the framework does not claim: a conforming record can document a terrible decision; cryptography proves sequence integrity, not independent cognition; the verifier is offline and cannot check that the declared evidence universe was the right one.

It is not the implementation. The Clinical Decision Object and its pipeline live in a separate private repository. This repo contains the paper and the benchmark, which are the parts a reader needs to evaluate the claims.

## Cite

> Jhol, R. (2026). *Beyond AI Audit Trails: The Three Foundations of Verifiable Decision Evidence* (v3.3). https://github.com/rajinderjhol/personavault-docs

The benchmark's format is not yet a published specification. If you want to add a record or compare your verifier against the ten records here, open an issue.
