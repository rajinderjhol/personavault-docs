# Folder structure — PersonaVault documentation

This repository follows the same documentation taxonomy as `verilinkos-docs`. The taxonomy is written down here so it can be applied consistently across repositories; **only directories that contain files are created**. Directories marked *reserved* are part of the taxonomy but are deliberately absent until there is content for them.

## Full taxonomy

```
<docs-repo>/
├── README.md                     front door: status banner, index, quick links
├── STATUS.md                     what the implementation does today; wins on conflicts
├── FOLDER_STRUCTURE.md            this file
├── CITATION.cff                   citation metadata
├── LICENSE
│
├── academic/                     formal papers and theoretical foundations
│   ├── <paper-slug>/
│   │   ├── paper.md               full paper
│   │   ├── abstract.md            standalone abstract
│   │   ├── references.bib         BibTeX references
│   │   └── figures/
│   │       └── README.md          figure inventory and placeholders
│   ├── three-foundations/         (populated)
│   ├── defensible-autonomy/       (populated)
│   └── mappings-dses-des-cdo/     (populated)
│
├── whitepapers/                  deep dives on capabilities and market vision
│   ├── <topic>.md
│   └── figures/                   shared figure fragments (reserved until used)
│
├── protocols/                    technical protocol specifications
│   └── <protocol>/<version>/
│       ├── specification.md
│       ├── schemas/
│       └── security/
│
├── standards/                    specifications offered for external adoption
│   └── <standard>-<version>/
│       ├── README.md
│       └── <standard>-<version>.md
│
├── references/                   supporting research and claim-boundary documents
│   └── <topic>.md
│
├── technical/                    getting-started, API reference, integration guides
│   ├── getting-started.md         (reserved)
│   └── api-reference.md           (reserved)
│
├── enterprise/                   architecture overviews for enterprise implementers
│   └── architecture-overview.md   (reserved)
│
├── investor/                     executive summaries and strategy
│   └── executive-summary.md       (reserved)
│
├── blog-posts/                   thought leadership
│   └── YYYY-MM-DD-<slug>.md       (reserved)
│
├── benchmark/                    runnable evidence (kept at root; not a paper)
│   ├── verify_demo.sh
│   ├── verify_cdr.py
│   ├── passing.cdr.json
│   └── <case-letter>-<description>.json
│
├── challenge-kit/                frozen adversarial challenge (kept at root)
│   ├── README.md                 threat model, expected results, limits
│   ├── FINDINGS.md               confirmed findings log
│   ├── CHECKSUMS.sha256          frozen artifact hashes
│   ├── receipt-valid.json
│   ├── receipt-tampered.json
│   └── verify_cdr_standalone.html
│
├── <old-paper>.md                 redirect stub when a paper moves into academic/
│
└── .github/ISSUE_TEMPLATE/       contribution entry points
    └── challenge-finding.md
```

## What belongs where

| Directory | Content | Not content |
|---|---|---|
| `academic/` | Peer-reviewable papers. Each paper gets its own slug directory with all four artifacts. | Product briefs, status pages, runnable benchmarks. |
| `whitepapers/` | Long-form argument or capability deep dives that are not formal papers. | Specifications with a version and conformance claims. |
| `protocols/` | Versioned wire/schema specifications and their threat models. | Marketing explanations of a protocol. |
| `standards/` | Specifications intended for external adoption or conformance. | Internal design decisions. |
| `references/` | Claim matrices, boundary statements, literature notes that support the papers. | New papers. |
| `technical/`, `enterprise/`, `investor/`, `blog-posts/` | Audience-specific entry points and posts. | Anything that belongs in `academic/`. |
| Root | Status, evidence summaries, citation metadata, redirect stubs. | Papers (except stubs). |

## Naming rules

- Paper slugs are lowercase, hyphenated, and stable: `three-foundations`, `defensible-autonomy`, `mappings-dses-des-cdo`.
- A paper's full text is always `paper.md`; never name the file after the paper title inside `academic/`.
- `abstract.md` contains only the title and the abstract, so it can be linked or pasted independently.
- `references.bib` uses standard BibTeX keys (`author-year-shorttopic`). Internal specifications use `@misc` with `howpublished = {PersonaVault implementation repository}`.
- Protocol and standard directories are versioned (`cdr/v1/`, `ARAS-v1.0/`); a new version gets a new directory, not an overwritten file.
- Blog posts are dated `YYYY-MM-DD-<slug>.md`.

## Operating rules

1. **Use `git mv` when relocating a document**, so history follows the file.
2. **Leave a root redirect stub** whenever a previously published root-level document moves into `academic/`. External links and `CITATION.cff` keep working.
3. **`STATUS.md` wins on conflicts** with papers or benchmark material. Papers describe claims; status describes what is actually shipped.
4. **Do not create empty directories.** Add `technical/`, `enterprise/`, `investor/`, `blog-posts/`, `standards/` when the first real document lands. A README promising content that does not exist is worse than no directory.
5. **Keep the public/private split.** This repository holds papers, specifications, and verifiable evidence. Internal readiness assessments, file-path inventories, and unapproved product claims stay in the private implementation repository.
6. **Benchmark and verification artifacts stay at root** (`benchmark/`), because they are runnable evidence, not a paper.

## Current population (2026-11-22)

```
README.md, STATUS.md, FOLDER_STRUCTURE.md, CITATION.cff, LICENSE
three-foundations.md                         redirect stub
academic/three-foundations/                  paper.md, abstract.md, references.bib
academic/defensible-autonomy/                paper.md, abstract.md, references.bib, figures/README.md
academic/mappings-dses-des-cdo/              paper.md
whitepapers/                                 measuring-clinical-judgment.md,
                                             verifiable-decision-layer-for-clinical-ai.md
protocols/cdr/v1/                            specification.md
references/                                  claim-matrix.md, claim-boundaries.md
benchmark/                                   unchanged (10 records + verifier + demo script)
challenge-kit/                               README.md, FINDINGS.md, CHECKSUMS.sha256,
                                             valid + tampered receipts, standalone HTML verifier
.github/ISSUE_TEMPLATE/                      challenge-finding.md
```

Reserved and not created: `standards/`, `technical/`, `enterprise/`, `investor/`, `blog-posts/`, `whitepapers/figures/`, `protocols/*/schemas/`, `protocols/*/security/`.

## Source mapping from the private implementation repository

| Private path | Public path |
|---|---|
| `docs/papers/three-foundations-of-verifiable-decision-evidence.md` | `academic/three-foundations/paper.md` |
| `docs/papers/defensible-autonomy/PAPER_DRAFT.md` | `academic/defensible-autonomy/paper.md` |
| `docs/papers/mappings-dses-des-cdo.md` | `academic/mappings-dses-des-cdo/paper.md` |
| `docs/HEALTHCARE/09-whitepapers/measuring-clinical-judgment.md` | `whitepapers/measuring-clinical-judgment.md` |
| `docs/HEALTHCARE/09-whitepapers/verifiable-decision-layer-for-clinical-ai.md` | `whitepapers/verifiable-decision-layer-for-clinical-ai.md` |
| `docs/HEALTHCARE/04-standards/cdr-1.0.md` | `protocols/cdr/v1/specification.md` |
| `docs/CLAIM_MATRIX.md` | `references/claim-matrix.md` |
| `docs/HORIZONTAL_CLAIM.md` | `references/claim-boundaries.md` |
| `challenge-kit/` (implementation repo) | `challenge-kit/` (canonical public kit) |

Not published: `docs/papers/defensible-autonomy/READINESS_ASSESSMENT.md` (internal working document), ADRs, and other private engineering notes.
