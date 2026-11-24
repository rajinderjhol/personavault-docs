# Conformance self-assessment

**This is a vendor self-assessment, not a certification, not legal advice, and not a regulatory determination.** It maps what the implementation actually records to the obligations a regulated deployer is likely to ask about. Every row should be verified against the running system and the public verifier rather than trusted from this table. Last reviewed 2026-11-22 against implementation commit `99ad38f4`.

For an auditor's own test plan, see the [third-party audit path](third-party-audit-path.md).
For procurement reviews framed around sovereignty or hospital sourcing
requirements, see the [sovereign decision evidence pack](sovereign-decision-evidence.md).
It maps the same artifacts to the Commission's eight sovereignty objectives
and to T-CAIREM Appendix G; it makes no SEAL or certification claim.

## Classification argument (self-assessment)

For the evaluated pilot configuration, PersonaVault is assessed as:

- **Not a high-risk AI system under EU AI Act Art. 6(3)**, on three grounds: it performs a narrow procedural task (retrieval and draft generation), it improves a human activity (the tumor board or review remains the human decision), and it documents decisions made by named humans.
- **Not a medical device** under Swissmedic / EU MDR, for the same reasons: it does not provide a clinical recommendation as its output; it records the deliberation around one.

This argument is configuration-specific and context-dependent. A deployer that changes the intended purpose must redo it. It is not an approval by any authority.

## Regulatory surface

| Regime | What the implementation records | What is not covered |
|---|---|---|
| EU AI Act Art. 12 — record-keeping | Signed CDO/CDR with `knowledge_state`, transcript hash, version chain, provenance completeness, assessment | The verifier cannot check that the declared evidence universe was complete or right |
| EU AI Act Art. 13 — transparency | `ai_bom_ref`, `ai_provenance` nodes and graph hash, model attribution, `presentation_state` | No claim that the end user was informed in any particular jurisdiction |
| EU AI Act Art. 14 — human oversight | `pre_ai_commitment` ordered before AI output; `presentation_state` with derived independence class; `divergence_from_ai`, `evidence_contradiction`, `human_deliberation.dissent` | Presentation proves exposure, not that the item was read or understood; gesture interaction capture is not implemented |
| EU AI Act Art. 26 — deployer duties | Consent status at decision time, enrolled signing keys, authority mandates, audit events | No standing instruction set is delivered to each deployer |
| Swiss nDSG | `consent.subject_id`, `status_at_decision`, supersede with revision and reason; regulatory retention exception asserted for pilot decisions | Scope is recorded, not enforced at upload; no zero-knowledge consent proof; no crypto-erasure |
| FINMA Guidance 08/2024 (model governance) | AIBOM reference, model/provider attribution, per-decision receipts, frozen DQI snapshot | No model approval workflow is shipped; no aggregate model validation |
| FDA/EMA joint principles — traceability, human oversight | Hash-bound evidence entries, named chair signature, dissent, version chain | No FDA/EMA submission package; no clinical outcome validation |
| FMH/SAMW — Swiss medical AI | Deliberation transcript, provenance, consent | Bias/equity analysis is deferred; this is the most material open requirement |

The pilot attestation originally mapped PersonaVault to EU AI Act Arts. 6/12/14/17, FINMA 08/2024, nDSG, the FDA/EMA joint principles, and FMH/SAMW. The table above is the portion that can be checked from the public artifacts. Do not read the private attestation as evidence of implementation — see [Implementation status](../STATUS.md).

## Field-to-obligation map

| CDR field | Obligation it can evidence |
|---|---|
| `knowledge_state.entries` + `snapshot_hash` | Record-keeping; what evidence was referenced at decision time |
| `knowledge_state.declared_universe` + completeness attestation | Bounded claim about the evidence universe — relative to the declaration only |
| `transcript` + `transcript_hash` | Audit trail of deliberation |
| `ai_bom_ref`, `ai_provenance` | Model and provider attribution |
| `presentation_state` | AI output was rendered; derived independence class |
| `pre_ai_commitment`, `pre_ai_assessment` | Human formed a plan before AI output; sequence integrity |
| `human_decision.content.adopted_items`, `divergence_from_ai` | Disposition of each AI recommendation; field-level rationale |
| `human_deliberation.dissent`, `alternatives` | Recorded disagreement and alternatives |
| `consent` | Consent basis and status at decision time — recorded, not enforced as to scope |
| `attestation` (Ed25519, key id) | Non-repudiation of the named signer's key |
| `version_chain`, `prior_cdo_hash` | Amendment without rewriting history |

## How to verify rather than trust

1. Run the [challenge kit](../challenge-kit/README.md): the valid receipt verifies, the one-character tampered receipt fails. This checks bytes and signatures. To check the signer binding as well, pass an anchor document (`python3 tools/verify_cdr.py receipt.json --anchor anchor.json`); the kit itself is frozen and runs without one.
2. Run the [ten-record benchmark](../benchmark/README.md): it shows which artifact classes pass which checks, including the case that passes every check without an authority block.
3. Open `exhibits/exhibit-b-override.cdr.json` in the paper's appendix and verify it offline: it binds a reasoned override with sequence, provenance, and authority in one record.
4. Ask for a run of the implementation's full verifier if you need checks beyond the frozen kit.

## Boundaries

- **No external certification** is claimed. ARAS covariates, SCITT, W3C DID interoperability, and any cross-system conformance are forward-looking.
- **Disclosure views are derived, not signed independently.** An evidentiary or minimal projection omits narrative and source content and is bound to the original receipt by hashes. A receiver must verify the original and the projection; the view alone is not a new attestation.
- **No transparency log, external root of trust, or notarization** is implemented. A published `signer-anchor.v1` registry binds keys to owners and institutions, and the offline verifier can check that binding when an anchor document is supplied. The anchor is published by the same installation that signs the receipt, so a receiver must obtain it through a channel it already trusts. A signed receipt is not a timestamped public anchor.
- **Execution evidence**: the CDR proves *attested*, not *executed*. The separate execution-evidence verifier specified in ADR 0030 does not exist. The current verifier's "Execution evidence" check reads an embedded assessment inside the CDO, which is a different thing.
- **Offline verification cannot check the evidence universe**, the truth of the AI's claims, or whether the decision was clinically correct. With an anchor document it can check the asserted owner/institution binding for the signing key — but the binding is an assertion by the issuing installation, not an independently verified identity.
- **No interoperation with VeriLinkOS** is defined or claimed; the systems have separate evidence models and separate test suites.
- **Privacy**: see the implemented / specified / absent distinction in [Implementation status](../STATUS.md). Do not infer crypto-erasure or per-session pseudonymization from design documents.
