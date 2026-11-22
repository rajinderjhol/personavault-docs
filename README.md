# Beyond AI Audit Trails

> **Current implementation status:** [STATUS.md](STATUS.md) (2026-11-22).
> It supersedes older claims in the paper and benchmark material. PersonaVault
> is a separate system from VeriLinkOS; no interoperation is defined or claimed.

**The three foundations of verifiable decision evidence — and a benchmark that tests whether they hold.**

A signed decision record proves who signed it. It does not prove that the human formed an independent judgment before the AI spoke. It does not prove what evidence was available and skipped. It does not prove the signer had the authority to act on the specific decision the record documents.

## Papers

- [Beyond AI Audit Trails: The Three Foundations of Verifiable Decision Evidence](academic/three-foundations/paper.md) — v3.3, 2026-11-06. [Abstract](academic/three-foundations/abstract.md) · [References](academic/three-foundations/references.bib). The paper argues that **sequence**, **provenance**, and **authority** are three separate evidence claims, and offers a benchmark that tests them against a runnable verifier. The old root path is preserved as a [redirect stub](three-foundations.md).
- [Defensible Autonomy: Cryptographic Decision Receipts as an Evidentiary Bridge Between Automation Bias and Hindsight Liability](academic/defensible-autonomy/paper.md) — working draft. [Abstract](academic/defensible-autonomy/abstract.md) · [References](academic/defensible-autonomy/references.bib). A framing paper about what a signed decision record can and cannot establish when a human departs from AI advice.
- [Companion Mappings: DSES and DES onto the CDO](academic/mappings-dses-des-cdo/paper.md) — v0.2, 2026-11-05. Field-by-field mapping to the three-foundations paper.

## Whitepapers

- [A Verifiable Decision Layer for Clinical AI](whitepapers/verifiable-decision-layer-for-clinical-ai.md)
- [Measuring Clinical Judgment](whitepapers/measuring-clinical-judgment.md)

## Specification and claim boundaries

- [CDR 1.0 specification](protocols/cdr/v1/specification.md)
- [Claim matrix — what we can say, and what proves it](references/claim-matrix.md)
- [The horizontal claim — what the CDR proves and does not prove](references/claim-boundaries.md)

## Run the benchmark

```sh
cd benchmark
./verify_demo.sh
```

That runs the offline verifier against the paper's reference case. The output ends with `DECISION INTEGRITY: VALID` and lists `Pre-AI commitment` among the passed checks. The full table — ten records, ten artifact classes, seven failure modes — is in the benchmark material.

## What this repository is not

It is not a product. The framework does not claim that a conforming record documents a good decision: cryptography proves sequence integrity, not independent cognition. The offline verifier cannot check that the declared evidence universe was complete.

It is not the implementation. The Clinical Decision Object, its pipeline, and the internal engineering notes live in a separate private repository. This repo contains the parts a reader needs to evaluate the claims.

## Repository structure

See [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md) for the full taxonomy and naming rules. In short: `academic/` for papers, `whitepapers/` for long-form arguments, `protocols/` for versioned specifications, `references/` for claim-boundary documents, and `benchmark/` for runnable evidence.

## Cite

> Jhol, R. (2026). *Beyond AI Audit Trails: The Three Foundations of Verifiable Decision Evidence* (v3.3). https://github.com/rajinderjhol/personavault-docs

The benchmark's format is not yet a published specification. If you want to add a record or compare your verifier against the ten records here, open an issue.
