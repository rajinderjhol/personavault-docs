# Sovereign decision evidence pack

> **What this is:** a mapping from what PersonaVault actually produces — CDRs,
> the offline verifier, the challenge kit, the local companion and the
> disclosure profiles — to (A) the European Commission's eight sovereignty
> objectives and (B) the procurement evidence checks in T-CAIREM's healthcare
> AI governance framework.
>
> **What this is not:** a claim of sovereignty certification. The Commission's
> Sovereignty Effectiveness Assurance Levels (SEAL-0 … SEAL-4) are awarded to
> **cloud providers** after audit. PersonaVault is software deployed on
> customer-controlled infrastructure; it is not a cloud provider and claims
> **no SEAL level**. Likewise, this pack is a *supplier-evidence input*, not a
> completed hospital assessment — T-CAIREM §8 and Appendix G explicitly
> require local assurance before operational use.
>
> All claims here are bounded by [STATUS.md](../STATUS.md) and the
> [claim matrix](../references/claim-matrix.md), which win on conflict.

## Sources

| Source | Date | Used for |
|---|---|---|
| European Commission, [Sovereign Cloud Framework explained](https://commission.europa.eu/news-and-media/news/sovereign-cloud-framework-explained-2026-06-01_en) | 2026-06-01 | Eight sovereignty categories, 48 criteria, SEAL thresholds |
| European Commission, [Commission advances cloud sovereignty through strategic procurement](https://commission.europa.eu/news-and-media/news/commission-advances-cloud-sovereignty-through-strategic-procurement-2026-04-17_en) | 2026-04-17 | €180M tender, SEAL-2/3/4 meaning, minimum-floor eligibility |
| T-CAIREM, [Healthcare AI Governance Framework](https://tcairem.utoronto.ca/sites/default/files/assets/files/latest-update-15oct26-tcairemhealthcaregovernanceframework.pdf) | 2026-10 | §8.1 procurement standards; Appendix D evidence by tier; Appendix G checks G1.1–G1.3 |

---

## A. Mapping to the Commission's eight sovereignty objectives

The Commission groups 48 scoring criteria into eight categories. The table
below states what the **decision layer** can contribute to a buyer's
assessment of each — not what the hosting stack provides.

| # | Sovereignty objective | What PersonaVault evidences | Proof | Does not establish |
|---|---|---|---|---|
| 1 | **Strategic** | Verification has no dependency on PersonaVault's platform, account system or a network call. A buyer can keep the ability to verify decisions even if the vendor disappears. | [Challenge kit](../challenge-kit/README.md): 3 files, zero external references; standalone HTML verifier works offline | Ownership/control of the underlying infrastructure, or continuity of the application itself |
| 2 | **Legal and jurisdictional** | Receipts carry `environment_id`, chair identity and key binding; the local companion keeps raw audio, transcripts and keys on customer premises. No decision evidence is routed to PersonaVault for verification. | [Local evidence boundary](../references/claim-matrix.md) row; CDR wire format in the [specification](../protocols/cdr/v1/specification.md) | CLOUD Act / FISA exposure of the hosting provider. That is a cloud-provider question and belongs to the SEAL assessment |
| 3 | **Data and AI** | Exact bytes shown to the AI are bound by `content_hash` → `snapshot_hash` → CDO hash → Ed25519 signature. AI components are recorded in the provenance graph; disclosure profiles share a hash-bound redacted view. | [Specification](../protocols/cdr/v1/specification.md) §`knowledge_state.entries`; [STATUS.md](../STATUS.md) provenance/disclosure sections; `tests/test_disclosure_profiles.py` (private) | That the declared evidence universe was complete, or that the AI's claims were true. DQI measures documentation quality, not correctness |
| 4 | **Operational** | Offline verification, self-service tamper challenge, an append-only governance event ledger, and cross-worker deliberation fan-out via Postgres LISTEN/NOTIFY with health-checked reconnection and bounded live-event retention. The hospital can reconstruct a decision without vendor cooperation. | [Challenge kit](../challenge-kit/README.md), [benchmark](../benchmark/README.md), claim matrix event-ledger row; two-worker, failover and retention tests in the private suite | Failover is covered by a deliberate connection-close test, not a full chaos exercise; retention is opportunistic rather than scheduled |
| 5 | **Supply chain** | The receipt names model and provenance nodes; a pilot AIBOM lists participating AI components. Open wire format (JSON, SHA-256, Ed25519) with a standalone verifier means no proprietary runtime is required to check a record. | [STATUS.md](../STATUS.md) AI provenance; benchmark artifact classes | Full software/hardware supply-chain transparency, fourth-party mapping or SEAL-3/4 supply-chain autonomy. Not audited |
| 6 | **Technological** | Verification is implemented twice — Python and browser — with parity tests over frozen artifacts; canonicalization is published. No lock-in to a model or cloud for verification. | Claim matrix *Independent verification*; verifier parity tests (private) | Parity for every future receipt; it is artifact-scoped by construction |
| 7 | **Security and compliance** | Enrolled chair keys, Ed25519 signatures, environment-scoped membership and authority checks, optional signer-anchor binding, fail-closed completeness checks. | [Conformance self-assessment](conformance.md); claim matrix *Governance* and *Independent verification* | External certification, accreditation, or an independent root of trust. The signer anchor is self-published by the issuing installation |
| 8 | **Environmental sustainability** | Nothing specific to the decision layer. | — | — |

**How to use this with SEAL.** A buyer's cloud assessment happens at the
infrastructure layer (SEAL-2 data sovereignty through SEAL-4 full sovereignty).
PersonaVault contributes evidence to objectives 1, 3, 4 and 6 particularly;
it cannot raise a provider's SEAL level and does not try to.

---

## B. Mapping to T-CAIREM procurement checks

T-CAIREM §8.1: *"Procurement must secure the evidence, access, remedies, and
exit rights the hospital will need during use."* Appendix G G1.1–G1.3 makes
that concrete. The mapping below is what the product supplies as evidence;
the hospital still records its own decision, reviewer and date.

### G1.1 — Procurement decision

| T-CAIREM check | PersonaVault evidence | Status |
|---|---|---|
| Intended use, limits, users, inputs/outputs, level of AI involvement, human decision authority, draft/final status | CDR records the chair, the AI recommendation, per-item dispositions and the signed decision; packs declare their own vocabulary and action perimeter | **Partial** — the record evidences each decision; a system-level "maximum operating limits" statement is a dossier/contract artifact, not produced by the runtime |
| Prohibited uses, data, settings, features and reliance | HTTP-boundary tool allow/deny; denied and undeclared tools refused; irreversible tools require human approval | **Partial** — technical enforcement exists for tools; a written prohibition list is a local policy document |
| Supplier evidence: exact version tested, datasets, population, evaluation period, comparator, measures | Model identity and AI provenance are bound into fresh signed decisions; benchmark reports artifact-class results | **Partial** — version and provenance yes; clinical evaluation data no. PersonaVault does not claim diagnostic performance |
| Uncertainty, serious errors, subgroup findings, exclusions | Adequacy findings are advisory and fail-closed checks are explicit; claim matrix states limits per claim | **Partial** — structural/lexical adequacy, not clinical subgroup analysis |
| Where supplier evidence does not apply to local use | The claim matrix's *Limit* column and *Not claimed* section; STATUS.md *Claim boundaries* | **Provided** |
| Setup, mapping and test environment the supplier must support | Published [CDR specification](../protocols/cdr/v1/specification.md), [benchmark](../benchmark/README.md), frozen [challenge kit](../challenge-kit/README.md) | **Provided** |
| Documentation, logs, representative cases, interfaces, personnel | Specification, benchmark artifacts, challenge kit; supplier personnel is a commercial term | **Partial** |
| Enforceable response times and evidence-delivery dates | Not a product capability. Contract matter | **Not provided** |

### G1.2 — Cybersecurity and contract requirements

| T-CAIREM check | PersonaVault evidence | Status |
|---|---|---|
| Dated map of components, connections, data flows, retention, deletion | Local companion boundary documentation; AIBOM in the pilot; no full published supplier data-flow map | **Partial** |
| Gaps recorded with owner, due date and resolution evidence | Claim matrix limits; public mitigation register; private product risk register | **Partial** — the registers are evidence of discipline, not a contractual gap register |
| Privacy/cyber review against actual components | Environment-scoped membership and authority checks, consent guard, disclosure profiles | **Partial** |
| Change notice: what changes, advance period, release IDs, emergency route | `version_chain` in the receipt identifies versions; no contractual notice mechanism | **Partial** |
| Hospital authority to assess, revalidate, approve/defer, disable or roll back | Environment controls and freeze guard; amendments are append-only with a fresh signature — signed history is deliberately **not** rollback-able | **Partial** — disable yes; rollback of the signed record no, by design |
| Logs, retention periods, access rights, delivery deadlines | Governance event ledger, receipts, challenge kit; retention policy is not shipped | **Partial** |
| Hospital can obtain evidence and access supplier personnel for audit/investigation | Self-service offline verification needs no vendor access; personnel access is commercial | **Provided for evidence**, not for personnel |
| Incident clauses: evidence preservation, deadlines, escalation, remedies | Not shipped as a product artifact | **Not provided** |
| Secondary use / training / resale prohibited without authorization | Local companion approval is local-only; learned patterns are environment-scoped and inspectable. Contractual prohibition must be explicit | **Partial** — needs contract language |

### G1.3 — Continuity and accountability

| T-CAIREM check | PersonaVault evidence | Status |
|---|---|---|
| Exit conditions, notice, transition time, service commitments | Receipts and challenge kit are portable and need no platform; transition terms are contractual | **Partial** |
| Export data and configuration, evidence of deletion, credential removal | Receipt export and hash-bound disclosure profiles; raw files remain with the local companion. **Evidence of deletion is not shipped** | **Partial** |
| Responsibility for clinical harm, inaccurate output, privacy/security failure, downtime | Claim boundaries: this is not a medical device and gives no clinical advice. Allocation is contractual | **Not provided as a product artifact** |
| Insurance and indemnity | Contract matter | **Not provided** |
| Rights to evidence, investigate, restrict/pause, export/delete, support on exit | Offline verification, freeze guard, disclosure profiles; deletion evidence gap as above | **Partial** |
| Exit plan rehearsed (technical or tabletop) | Not shipped | **Not provided** |

### Evidence tiers (Appendix D / GAISSF T1–T4)

The insurance-sector evidence catalogue distinguishes T1 primary verified
operating evidence from T4 vendor white papers. Honest placement:

| Tier | What it means | PersonaVault artifacts |
|---|---|---|
| **T1** | Automated logs, immutable decision trails, access records | CDR, governance event ledger, challenge kit, disclosure profiles |
| **T2** | Independent or second-line verification | **None yet** — no third-party audit or accreditation |
| **T3** | Controlled simulation / adversarial exercise | Challenge kit tampered receipt; benchmark artifact classes |
| **T4** | Vendor benchmarks, white papers | The papers in this repository — explicitly insufficient alone |

A buyer should not treat a PersonaVault paper as T1 evidence. The receipt and
the kit are T1; the argument for them is T4.

---

## C. Self-service verification runbook

A procurement reviewer can check the central claim in minutes, with no
account and no call to PersonaVault.

```sh
# 1. Verify the frozen bytes have not changed.
cd challenge-kit
shasum -a 256 -c CHECKSUMS.sha256

# 2. Open verify_cdr_standalone.html with no network connection.
#    Load receipt-valid.json   -> DECISION INTEGRITY: VALID (16 pass-labels)
#    Load receipt-tampered.json -> fails at knowledge_state.entry.content_hash

# 3. Reproduce the benchmark's artifact-class results.
cd ../benchmark
./verify_demo.sh
```

**Read this caveat first:** `benchmark/verify_cdr.py` is a frozen older
snapshot with 14 checks. It lacks the `knowledge_state.entry.content_hash`
check and therefore reports `VALID` for the tampered kit receipt. That
mismatch is recorded as `KIT-001` in [FINDINGS.md](../challenge-kit/FINDINGS.md).
Use the bundled HTML verifier or the current implementation verifier for the
challenge kit. Do not mix results from the three verifier versions.

---

## D. Gaps a buyer will find

Stated plainly so they are found here rather than in diligence:

- **No third-party audit or accreditation.** External verification of the
  *artifact* is possible; external verification of the *implementation* is not.
- **No subject-facing contestability surface.** An append-only, hash-bound
  contestation chain now exists in the backend, but a person who is the
  subject of a decision still has no login, portal, subject-held receipt or
  opt-out. Staff can file on their behalf and the filing actor is recorded.
  This matters for EU fundamental-rights cases and insurance notices.
- **No deletion-evidence artifact.** Export exists; provable erasure does not.
- **Failover is tested at the connection level, not under chaos.** Live
  fan-out works across workers via Postgres LISTEN/NOTIFY with durable payloads,
  health-checked reconnection and an hourly retention sweep. A full network
  partition or database failover exercise has not been run.
- **No clinical outcome evidence.** Decision quality and "better decisions"
  remain unproven; DQI is documentation quality. A separate execution-evidence
  artifact and verifier (ADR 0030) can prove an action was performed by an
  independent party, but a performer must actually record it, and verified
  execution is not proof of a better decision.
- **No external root of trust.** The signer anchor is published by the same
  installation that signs receipts.
- **Incident, retention-policy and exit-rehearsal artifacts are not shipped.**

The product-side open items are tracked in the private risk register; the
public [mitigation register](../references/mitigation-register.md) reports
only implemented and piloted controls.

---

## Related

- [Third-party audit path](third-party-audit-path.md)
- [Conformance self-assessment](conformance.md)
- [Claim matrix](../references/claim-matrix.md) and [claim boundaries](../references/claim-boundaries.md)
- [PRIMER mitigation register](../references/mitigation-register.md)
- [Challenge kit](../challenge-kit/README.md) and [benchmark](../benchmark/README.md)
