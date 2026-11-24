# PersonaVault

**A governed decision operating system for regulated organizations.**

PersonaVault lets AI assist high-stakes decisions without letting it own them. Each deliberation produces a **Cryptographic Decision Receipt (CDR)**: a signed, offline-verifiable record of what the human knew before the AI spoke, the exact advice the AI gave, the evidence available at that moment, and what the human did with that advice. Models generate intelligence; PersonaVault accumulates it. The customer's own experts are the reward signal, and the provenance-backed knowledge they create becomes more valuable the longer the system is used.

The substrate is the foundation. The product is the packs: thirteen Domain Intelligence Units that give each domain its own vocabulary, form, decision kinds, and AI action perimeter — clinical, legal, insurance, compliance, security, procurement, tax, and robotics.

This repository is the **public evidence layer** for PersonaVault: the papers, specification, benchmark, challenge kit, and evaluator guides. The implementation lives in a separate private repository.

> **Current implementation status:** [STATUS.md](STATUS.md) (2026-11-22). It supersedes older claims in the paper and benchmark material. PersonaVault is a separate system from VeriLinkOS; no interoperation is defined or claimed.

## Start here

| If you want to… | Read |
|---|---|
| Understand the product and its domains | [Packs and Domain Intelligence Units](enterprise/packs-and-dius.md) |
| Check regulatory alignment | [Conformance self-assessment](enterprise/conformance.md) |
| Answer a sovereign / hospital procurement review | [Sovereign decision evidence pack](enterprise/sovereign-decision-evidence.md) |
| Give an auditor something to test | [Third-party audit path](enterprise/third-party-audit-path.md) |
| See what a receipt proves and does not | [The horizontal claim](references/claim-boundaries.md) and [claim matrix](references/claim-matrix.md) |
| See which AI-risk mitigations we report | [Mitigation register (PRIMER)](references/mitigation-register.md) |
| Verify something yourself | [Run the benchmark](#run-the-benchmark) or [challenge the verifier](#challenge-the-verifier) |
| Read the argument | [Beyond AI Audit Trails](#papers) |

## Papers

- [Beyond AI Audit Trails: The Three Foundations of Verifiable Decision Evidence](academic/three-foundations/paper.md) — v3.3, 2026-11-06. [Abstract](academic/three-foundations/abstract.md) · [References](academic/three-foundations/references.bib). The paper argues that **sequence**, **provenance**, and **authority** are three separate evidence claims, and offers a benchmark that tests them against a runnable verifier. The old root path is preserved as a [redirect stub](three-foundations.md).
- [Defensible Autonomy: Cryptographic Decision Receipts as an Evidentiary Bridge Between Automation Bias and Hindsight Liability](academic/defensible-autonomy/paper.md) — working draft. [Abstract](academic/defensible-autonomy/abstract.md) · [References](academic/defensible-autonomy/references.bib). A framing paper about what a signed decision record can and cannot establish when a human departs from AI advice; includes [Exhibit A](academic/defensible-autonomy/exhibits/exhibit-a-kit-valid.json) and a freshly signed [override exhibit](academic/defensible-autonomy/exhibits/exhibit-b-override.cdr.json).
- [Companion Mappings: DSES and DES onto the CDO](academic/mappings-dses-des-cdo/paper.md) — v0.2, 2026-11-05. Field-by-field mapping to the three-foundations paper.

## Whitepapers

- [A Verifiable Decision Layer for Clinical AI](whitepapers/verifiable-decision-layer-for-clinical-ai.md)
- [Measuring Clinical Judgment](whitepapers/measuring-clinical-judgment.md)

## Specification and boundaries

- [CDR 1.0 specification](protocols/cdr/v1/specification.md)
- [Claim matrix — what we can say, and what proves it](references/claim-matrix.md)
- [Mitigation register — PRIMER reporting view](references/mitigation-register.md)
- [The horizontal claim — what the CDR proves and does not prove](references/claim-boundaries.md)

## Run the benchmark

```sh
cd benchmark
./verify_demo.sh
```

That runs the offline verifier against the paper's reference case. The output ends with `DECISION INTEGRITY: VALID` and lists `Pre-AI commitment` among the passed checks. The full table — ten records, ten artifact classes, and the findings behind them — is in the [benchmark README](benchmark/README.md). The bundled verifier is a frozen snapshot; read its version note before interpreting results.

## Challenge the verifier

The [`challenge-kit/`](challenge-kit/README.md) is a frozen signed receipt, its one-character tampered twin, and a standalone browser verifier with no network dependency. Try to break it and [file a finding](challenge-kit/FINDINGS.md). The expected results, the threat model, and the limits of what a valid receipt proves are stated up front in the kit's README.

## What this repository is not

It is not the product implementation. The Clinical Decision Object, its pipeline, the compiler, and the internal engineering records live in a separate private repository. This repo contains what a reader needs to evaluate the claims.

It does not claim that a conforming record documents a good decision. Cryptography proves sequence integrity, not independent cognition; the offline verifier cannot check that the declared evidence universe was complete. PersonaVault is evidence infrastructure, not a medical device, and it does not give clinical advice.

## Repository structure

See [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md) for the full taxonomy and naming rules: `academic/` for papers, `enterprise/` for evaluator and buyer guides, `whitepapers/` for long-form arguments, `protocols/` for versioned specifications, `references/` for claim-boundary documents, `benchmark/` for the ten-record suite, and `challenge-kit/` for the frozen adversarial challenge.

## Cite

> Jhol, R. (2026). *Beyond AI Audit Trails: The Three Foundations of Verifiable Decision Evidence* (v3.3). https://github.com/rajinderjhol/personavault-docs

The benchmark's format is not yet a published specification. If you want to add a record or compare your verifier against the ten records here, open an issue.
