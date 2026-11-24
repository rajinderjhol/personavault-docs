# Mitigation register — PRIMER reporting view

> This page reports the AI-risk mitigations PersonaVault has **implemented or
> piloted**, using PRIMER (Preferred Reporting Items for Mitigations of
> Emerging Risks) from Saeri et al., *The AI Risk Mitigation Repository*
> (MIT AI Risk Initiative / MIT FutureTech, November 2026).
>
> This is a **reporting view, not a new claim**. Where it conflicts with
> [STATUS.md](../STATUS.md) or the [claim matrix](claim-matrix.md), those
> documents win. [Conformance self-assessment](../enterprise/conformance.md)
> is the evaluator-facing companion.

## How to read this register

- **Only implemented or piloted mitigations are listed.** Planned work is not
  reported here; deliberately deferred items are listed in the claim matrix's
  *Not claimed* section.
- **Role** follows PRIMER: a *core intervention* acts directly on the risk
  pathway; a *supporting technique* acts only through an intervention it
  enables; an *enabling condition* is a state, not an action. A signed receipt,
  for example, is a supporting technique — the core intervention is the human
  decision it records.
- **Risk addressed** uses the MIT AI Risk Repository risk taxonomy. **Objective**
  uses the paper's 17 mitigation domains. **Mechanism** uses its 9 instruments.
  **Actor** and **Timing** use the paper's actor and lifecycle taxonomies.
- **Coverage is not effectiveness.** The source paper explicitly does not
  establish which mitigations work, what they cost, or their unintended
  effects. Nothing here claims a clinical outcome or decision-quality benefit.
- Proofs named `(private)` live in the implementation repository and cannot be
  inspected here. Externally inspectable evidence — the challenge kit, the
  benchmark, the standalone verifier — is preferred wherever available.

## Register

| # | Mitigation | Role | Risk addressed | Objective (domain) | Mechanism (instrument) | Actor | Timing | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Chair pre-AI commitment with sign gate | Core | Overreliance & unsafe use; loss of human agency | Human Oversight & Agentic Control; Content Authenticity & Provenance | Technical Artifacts; Practices & Processes | Deployer | Operate & Monitor | Implemented |
| 2 | Per-item HITL disposition with structured reason codes | Core | Overreliance & unsafe use; governance failure | Human Oversight & Agentic Control | Technical Artifacts; Practices & Processes | Deployer | Operate & Monitor | Implemented |
| 3 | Bound chair identity on HITL approval and rejection | Core | Governance failure | Accountability & Responsibility | Technical Artifacts | Deployer | Operate & Monitor | Implemented |
| 4 | Chair-signed decision receipt (CDR) | Supporting | Governance failure | Content Authenticity & Provenance | Technical Artifacts | Deployer | Operate & Monitor | Implemented |
| 5 | Offline verifier with frozen challenge kit | Core | Governance failure (undetected alteration) | Content Authenticity & Provenance; Accountability & Responsibility | Technical Artifacts; Evaluation & Audit | Governance Actor | Operate & Monitor | Implemented |
| 6 | Fail-closed completeness attestation against a declared universe | Supporting | Governance failure | Content Authenticity & Provenance; Risk Management & Assurance | Technical Artifacts | Deployer | Operate & Monitor | Implemented |
| 7 | Consent recorded and enforced at case-scoped boundaries | Core | Compromise of privacy; governance failure | Privacy & Data Protection; End-use Governance | Technical Artifacts; Practices & Processes | Deployer | Operate & Monitor | Implemented |
| 8 | Append-only amendments with fresh chair signature | Core | Governance failure | Content Authenticity & Provenance | Technical Artifacts | Deployer | Operate & Monitor | Implemented |
| 9 | Hash-bound disclosure profiles | Core | Compromise of privacy by obtaining, leaking or inferring sensitive information | Privacy & Data Protection | Technical Artifacts | Deployer | Operate & Monitor | Implemented |
| 10 | Published signer-anchor binding | Supporting | Governance failure (key impersonation) | Content Authenticity & Provenance | Information Sharing & Disclosure | Deployer | Outside Lifecycle | Implemented |
| 11 | Tool perimeter at the HTTP boundary | Core | Malicious actors & misuse; dangerous capabilities | Operational Safety & Control; Capability Control & Containment | Technical Artifacts | Deployer | Operate & Monitor | Implemented |
| 12 | Drift findings surfaced for review without auto-invalidation | Core | AI system safety, failures & limitations | Risk Management & Assurance | Monitoring | Deployer | Operate & Monitor | Implemented |
| 13 | Append-only governance event ledger | Supporting | Governance failure | Accountability & Responsibility | Monitoring | Deployer | Operate & Monitor | Implemented |
| 14 | Sovereign deployments fail closed | Core | AI system security vulnerabilities; governance failure | Security & Access Control | Technical Artifacts; Internal Policies | Deployer | Deploy | Implemented |
| 15 | Local companion as the evidence boundary (local-only proof approval) | Core | Compromise of privacy | Privacy & Data Protection; End-use Governance | Technical Artifacts; Practices & Processes | Deployer; User | Outside Lifecycle | Implemented |
| 16 | Test-data isolation and clean-checkout verification gate | Enabling | Governance failure | Security & Access Control; Risk Management & Assurance | Practices & Processes; Technical Artifacts | Developer | Outside Lifecycle | Implemented |
| 17 | Append-only subject contestations (backend primitive) | Core | Overreliance & unsafe use; loss of human agency | End-use Governance; Human Oversight & Agentic Control | Technical Artifacts; Practices & Processes | Deployer | Operate & Monitor | Implemented — backend only |

## Proof, observability and linked mitigations

1. **Pre-AI commitment / sign gate** — Proof: [STATUS.md](../STATUS.md) sequence
   integrity; sign gate refuses a commitment that withholds its plan (private).
   Observable as an integrity check in the signed receipt. Linked to 2, 4, 6.
2. **Per-item HITL disposition** — Proof: Store **Actions** and `POST
   /v2/environments/{env}/actions/{id}/approve|reject` (private test:
   `test_v2_actions_approval.py`). Observable as status, reason and actor on
   the action row. Linked to 1, 3, 4.
3. **Bound chair identity** — Proof: actor id required on approve/reject;
   404 when the actor is not in the environment (private test:
   `test_v2_actions_approval.py`). Observable in the validation and in the
   signed decision's actor. Limit: the action row stores `approved_by` only
   when the actor id is numeric; non-numeric ids are validated but not
   persisted in that column. Linked to 2, 4.
4. **Chair-signed CDR** — Proof: [challenge kit](../challenge-kit/README.md)
   and [claim matrix](claim-matrix.md). Observable as a signature and key id
   in the receipt. Linked to 1, 5, 6, 8.
5. **Offline verifier / challenge kit** — Proof: **externally inspectable** —
   `challenge-kit/` (3 files), [benchmark](../benchmark/README.md),
   `verify_cdr_standalone.html`. Observable as VALID / FAIL labels. Limit:
   bytes and signatures, not clinical truth; parity is artifact-scoped.
   Linked to 4, 6, 10.
6. **Completeness attestation** — Proof: claim matrix *Independent
   verification*; fail-closed missing-reference check (private). Observable
   as an additive verifier check. Limit: relative to the *declared* universe.
   Linked to 4, 5.
7. **Consent guard** — Proof: claim matrix *Governance*; case-scoped
   enforcement (private test: `test_consent_enforcement.py`). Observable as
   consent kind and status in the decision. Limit: environment-level uploads
   are not gated. Linked to 1, 9.
8. **Append-only amendments** — Proof: claim matrix *Governance*; `/amend`
   with `parent_artifact_id` and `prior_cdo_hash`. Observable as a new
   signature and a parent link. Limit: not a transparency log. Linked to 4.
9. **Disclosure profiles** — Proof: `GET .../receipts/{id}/disclosure`
   (private test: `test_disclosure_profiles.py`). Observable as a redaction
   manifest and `source_receipt_hash`. Limit: derived view, not a second
   signature. Linked to 4, 15.
10. **Signer anchor** — Proof: claim matrix *Independent verification*;
    `/.well-known/personavault-trust-anchor.json`; `verify_cdr.py --anchor`.
    Observable as a `Signer anchor` check. Limit: self-published; not an
    external root of trust. Linked to 4, 5.
11. **Tool perimeter** — Proof: claim matrix *Governance*; HTTP-boundary
    allow/deny enforcement and human approval for irreversible tools
    (private). Observable as refusal of denied or undeclared tools. Limit:
    covers successful executions; declared tools without handlers remain.
    Linked to 2, 14.
12. **Drift findings** — Proof: claim matrix *Governance*; deterministic
    scanner (private). Observable as review findings. Limit: never
    auto-invalidates a signature. Linked to 13.
13. **Governance event ledger** — Proof: claim matrix *Independent
    verification*; append-only event table and Studio Governance Calendar
    (private). Observable as a temporal view. Limit: no backfilled history.
    Linked to 4, 12.
14. **Sovereign fail-closed** — Proof: claim matrix *Deployment posture*;
    provider resolution has no silent fallback (private). Observable as a
    refusal when the configured provider is unavailable. Linked to 11.
15. **Local companion boundary** — Proof: [claim matrix](claim-matrix.md)
    *Governance*; local-only proof approval, no web signing. Observable as
    the absence of file-browser and proof-approval controls in Studio. Limit:
    the companion's MCP bridge is a stub. Linked to 9.
16. **Test isolation and verification gate** — Proof: [claim matrix](claim-matrix.md)
    *Deployment posture*; `scripts/verify.sh` and CI (private). Observable as
    a clean-checkout verification run. This is an enabling condition, not a
    product control. Linked to 5, 14.
17. **Subject contestations** — Proof: append-only v2
    `/subjects/{id}/contestations` endpoints and
    `tests/test_subject_contestation.py` (private). Observable as a chain of
    revisions whose statement hash never changes. Limit: **backend only** —
    the filing actor is recorded, so staff file on a subject's behalf; there
    is no subject login, patient-facing surface or subject-held receipt.
    Linked to 2, 4, 9.

## What this register does not report

- **Planned or design-only work.** See the claim matrix's *Not claimed*
  section: external root of trust, transparency log, replayability proofs,
  A2A and multi-agent delegation, post-quantum signatures, zero-knowledge
  consent proofs, cross-jurisdictional certification, the portable CDO
  `trust_anchor` block, and local-device-agent integration.
- **Neglected mitigation domains.** Against the source taxonomy PersonaVault
  reports nothing under Training & Capacity-building, Integrity & Ethics,
  Societal Resilience & Recovery, or Ecosystem Coordination. End-use
  Governance is reported through consent, the local companion and the
  contestation primitive — but there is still no subject-facing surface:
  no subject login, patient portal, subject-held receipt or opt-out.
- **Effectiveness.** No mitigation here has a measured effect on clinical
  outcomes or decision quality. See [STATUS.md](../STATUS.md) *Claim
  boundaries*.
