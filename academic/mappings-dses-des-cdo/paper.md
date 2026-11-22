---
title: "Companion Mappings: DSES and DES onto the CDO"
author: Rajinder Jhol
version: 0.2
status: complete for DSES event level and DES component level
date: 2026-11-05
audience: external
companions:
  - docs/papers/three-foundations-of-verifiable-decision-evidence.md
  - docs/HEALTHCARE/04-standards/cdo-1.0.md
---

# Companion Mappings: DSES and DES onto the CDO

This file accompanies *Beyond AI Audit Trails: The Three Foundations of Verifiable Decision Evidence* (v3.1). It maps the Decision-Sequence Evidence Schema (DSES v0.1) and the Decision Engineering Science Decision Object (DES) onto the Clinical Decision Object's (CDO) schema, field by field, so a reader can see where the lineages correspond and where they do not.

The word "ontology" here is the paper's sense, not the data-governance sense. These are evidence ontologies — models of what a decision record must prove — not models of business concepts. A field is mapped because it carries an evidence claim, not because it carries a business meaning.

The mappings are at the level of individual DSES events and DES components. Structural gaps are named in Section 3.

---

## 1. DSES → CDO

### 1.1 What DSES defines

DSES v0.2.0 (October 2026) defines a minimal, vendor-neutral event vocabulary for representing human-AI decision sequences, plus an outcome-evidence layer. Its abstract states the gap the specification exists to close: organizations "know which AI system ran, what output it produced, and what the final human decision was. They often cannot establish what the human believed before AI exposure, exactly when and in what form AI output reached the human, or how the human's decision changed afterward. Existing audit infrastructure records that a decision occurred; it does not preserve the decision *trajectory*."

The v0.2.0 release adds denominator-closed eligibility manifests, outcome linkage, pre-consensus adjudication under declared charters, content-addressed executable rules, recomputable reliance metrics (RAIR, RSR, EAR), and governance constraints on unit of analysis. The shipped candidate supplies RFC 8785 commitments, signatures, RFC 9162 proofs, reader-supplied external anchor trust, release lint, an adversarial suite, and a reference verifier. The v0.1.2 sequence layer's limit remains: an I2 single export establishes internal consistency only unless compared with a separately held checkpoint or supported by verified external anchoring.

DSES defines:

- A **ten-event vocabulary** for human-AI decision sequences (§4).
- An **eight-class exposure ontology** (§5) — because "the question 'did the clinician see the AI output' is not answerable with yes or no."
- An **information-state and independence model** (§6) that derives an independence class from the accumulated exposure classes at the moment of commitment.
- Four **integrity classes** (I0–I3) ranging from application log to enforced sequence with external anchoring (§7).
- Three **conformance levels** (L1–L3) describing what is captured, orthogonal to integrity (§8).
- Mappings to HL7 FHIR, IHE Radiology AI, DICOM, and OpenTelemetry (§9).

### 1.2 The ten DSES events

| # | Event type | Meaning |
|---|---|---|
| 1 | `case_context_created` | A case enters the instrumented workflow. Establishes case reference, workflow reference, and applicable AI systems. |
| 2 | `context_signal_recorded` | An upstream signal that may carry indirect AI influence reaches the workflow before any direct exposure (triage reordering, urgency flag, routing). |
| 3 | `human_state_committed` | A human decision state is committed, with the actor's information state at that moment. |
| 4 | `ai_result_available` | An AI system has completed generation of output. Availability is not presentation. |
| 5 | `ai_result_presented` | AI output is rendered, displayed, or otherwise delivered to a specific human actor. "The pivotal event most existing infrastructure does not record." |
| 6 | `ai_result_interacted` | The human interacts with presented output: expands, toggles, dismisses, scrolls. |
| 7 | `human_state_revised` | A previously committed decision state is superseded; the event references both prior and new state. |
| 8 | `final_decision_committed` | The accountable final decision is committed. Every sequence MUST terminate in exactly one. |
| 9 | `attestation_recorded` | A human records a structured rationale attached to a decision event. Optional at all conformance levels. |
| 10 | `integrity_event` | An event about the record itself: export, verification, anchor, gap detection. |

### 1.3 Event-level mapping

| DSES event | CDO block or field | Status | Note |
|---|---|---|---|
| `case_context_created` | `case_identity` (case_id, environment_id, pseudo_id, chair_id) and `version_chain.version` | **Mapped** | The CDO's case identity carries the case, environment, pseudonym, and chair. The DSES event also carries the workflow reference and applicable AI systems; the workflow reference is not a CDO field, and the AI systems are in `ai_provenance`. |
| `context_signal_recorded` | *Not recorded* | **Gap** | The CDO does not record upstream signals that carry indirect AI influence (triage reordering, urgency flags). This is the exposure gap: DSES's `PRIORITY` class has no CDO equivalent. |
| `human_state_committed` | `pre_ai_assessment` (plan_text, plan_structured, recorded_at, recorded_by_actor_id, schema_version) | **Mapped** | The pre-AI assessment block is the committed decision state. The CDO does not carry an explicit `information_state` field at the moment of commitment (DSES §4.1 requires it for events 3, 7, 8). That is the independence-class gap. |
| `ai_result_available` | `ai_recommendation.pack_id`, `pack_version`, `content`; `ai_provenance` | **Mapped** | The CDO records that the AI recommendation exists and what it contains. Availability and presentation are not distinguished in the CDO. |
| `ai_result_presented` | *Not recorded* | **Gap** | The CDO does not record when, how, or in what exposure class the AI output reached the human. This is DSES's "pivotal event" and the CDO does not carry it. |
| `ai_result_interacted` | *Not recorded* | **Gap** | No interaction event in the CDO. |
| `human_state_revised` | `human_decision` (content, content_hash, decision_owner_actor_id) | **Partial** | The CDO records the final human decision. It does not record a revision event that references the prior committed state and computes the change. The `version_chain` block records version lineage at the CDO level, not the decision-state level. |
| `final_decision_committed` | `human_decision` and `attestation` (actor_id, key_id, signature_algorithm, signed_payload_hash, signature_b64, attested_at) | **Mapped** | The chair's signed decision and the attestation are the CDO's final-decision commitment. |
| `attestation_recorded` | `human_deliberation.rationale` (partially) | **Partial** | The chair's rationale is a signed deliberation element. The CDO does not carry structured rationale codes (override reason, disagreement code) as a first-class attestation event. |
| `integrity_event` | *Not recorded as an event* | **Gap** | The CDR's verification is a separate act; the CDO does not carry an `integrity_event` record of exports, verifications, anchors, or gaps. ADR 0030's execution-evidence artifact is the closest structural analog, and it is post-pilot. |

### 1.4 The exposure ontology: DSES §5 and the CDO

DSES's eight exposure classes are the most significant contribution that the CDO does not carry:

| DSES class | What it contaminates | CDO equivalent |
|---|---|---|
| `PRIORITY` | Prior probability | None |
| `PRESENCE` | Expectation | None |
| `CATEGORICAL` | The diagnostic hypothesis | `ai_recommendation.content` records the output, not the class of information conveyed |
| `LOCALIZATION` | Visual search | None |
| `QUANTITATIVE` | Strength of belief | None |
| `NARRATIVE` | Diagnostic framing | None |
| `DIRECTIVE` | The downstream decision | None |
| `AGENTIC` | The decision space itself | None |

The CDO records that an AI recommendation was made and what it contained. It does not record *which class of information* the recommendation conveyed, and it does not distinguish a reordered worklist from a flagged finding from a drafted report. The paper's Section 4.1 names this gap; the CDO's `ai_recommendation` block is the natural home for an `exposure_class` field in a future schema version.

### 1.5 The independence model: DSES §6 and the CDO

DSES derives an independence class from the actor's information state at the moment of commitment: `UNEXPOSED`, `INDIRECTLY_EXPOSED`, `DIRECTLY_EXPOSED`, `POST_ACTION`. The CDO's `pre_ai_assessment` block carries the committed state but not the independence class. A reader of a CDO can see that a pre-AI assessment exists; they cannot see whether it was `UNEXPOSED` (no AI influence at all) or `INDIRECTLY_EXPOSED` (the AI triage moved the case to the top of the worklist, but no content was shown).

The paper's Section 5.1 claims the sequence ontology is "independently verifiable" for the single-clinician case. That claim is accurate for the *enforcement* of ordering (the commitment exists before the disclosure; the verifier checks the timestamp). It is not accurate for the *strength* of the independence claim, because the CDO does not carry the independence class. A future CDO schema version that carries `pre_ai_assessment.independence_class` would close this gap.

### 1.6 Integrity classes: DSES §7 and the CDR verifier

| DSES class | Property | CDR mapping |
|---|---|---|
| I0 — Application log | Mutable, client timestamps | Not the CDR |
| I1 — Controlled log | Append-oriented, server-assigned sequence | Not the CDR |
| I2 — Tamper-evident log | Hash-chained, cryptographic commitment, offline verifier | **The CDR's integrity is I2**: the `integrity.cdo_hash`, the `attestation.signed_payload_hash`, and the offline verifier's hash-chain recomputation are I2 properties |
| I3 — Enforced sequence | I2 plus enforced ordering or external anchoring | **The gate is I3(a)**: the AI recommendation is suppressed when the pre-AI commitment is absent — this is "enforced ordering, in which release of AI output is mechanically predicated on the existence of a committed decision state." The CDR does not have I3(b) external anchoring; that is a future addition. |

The CDO's gate and verifier implement DSES's I3(a) pattern. The `verify_demo.sh` artifact demonstrates the I2 verifier: the CDR's chain is hash-checked offline, and the `Pre-AI commitment` check proves the enforced ordering held. The paper's Section 5.1 claim that the sequence ontology is "independently verifiable" is the I2+I3(a) claim precisely.

### 1.7 What DSES adds that the CDO does not carry

The exposure ontology (§5), the information-state model (§6), and the interaction event (§4, event 6) are the most significant structural contributions DSES makes that the CDO does not carry. Each is a gap in the CDO's current implementation, and each is named in the paper's Section 4.1 as a limit.

### 1.8 What the CDO adds that DSES does not carry

DSES defines the record; the CDO defines the signed receipt. The `attestation` block (Ed25519 signature over the signed payload), the `version_chain` block (prior CDO hash, version), and the offline verifier (`tools/verify_cdr.py`) are the Receipt Layer's contribution to the DSES sequence. DSES §7.2 specifies the fail-closed requirement for I3(a); the CDO's gate and verifier are an implementation of that requirement.

DSES is explicit that it "does not replace model performance monitoring, AI governance platforms, clinical orchestration systems, or interoperability standards" (§2.2). The CDO is the Receipt Layer's clinical instantiation; the two are complementary, and the CDO could be described as one implementation of DSES's I2+I3(a) pattern for clinical decisions with the Receipt Layer's signed receipt on top.

---

## 2. DES → CDO

### 2.1 What DES defines

Decision Engineering Science (DES) proposes the Decision Object as "a persistent, structured, and governable object" that captures "the essential components of a bounded decision instance, including signals, context, objectives, evidence, constraints, alternatives, rationale, the resulting decision, execution, and observed outcomes" .

The ten components:

1. **Signals** — raw data and events entering the decision system
2. **Context** — the environment and conditions surrounding the decision
3. **Objectives** — what the decision is intended to achieve
4. **Evidence** — information supporting the evaluation
5. **Constraints** — boundaries defining what is admissible
6. **Alternatives** — possible courses of action
7. **Rationale** — reasoning behind the selected alternative
8. **Decision** — the selected course of action
9. **Action** — execution resulting from the decision
10. **Outcome** — what actually happened after execution

### 2.2 Component-level mapping

| DES component | CDO block or field | Status | Note |
|---|---|---|---|
| **Signals** | `knowledge_state.entries` (partially) | **Partial** | The CDO records the evidence entries, not the raw signals that produced them. DSES's `context_signal_recorded` event is the closest equivalent, and it is a gap in the CDO (§1.3). |
| **Context** | `case_identity`, `knowledge_state.captured_at` | **Partial** | The case identity and capture time are recorded; the full context (environment, patient state, institutional conditions) is not a first-class block. |
| **Objectives** | *Not recorded* | **Gap** | The CDO's `human_decision.decision_details` carries the treatment intent's shape (regimen, intent, cycles), but not a formal Objectives component. |
| **Evidence** | `knowledge_state.entries` | **Mapped** | Evidence entries are content-addressed and completeness-checked (Section 6 of the paper). |
| **Constraints** | *Not recorded* | **Gap** | The CDO has no Constraints block. Clinical, legal, and resource constraints are not first-class elements. |
| **Alternatives** | `human_deliberation.alternatives` | **Mapped** | The deliberation block carries alternatives proposed by the pack or the room. |
| **Rationale** | `human_deliberation.rationale` | **Mapped** | The chair's rationale is a signed element. |
| **Decision** | `human_decision` | **Mapped** | The decision content, hash, owner, and decision time. |
| **Action** | `actions` (optional) | **Mapped, optional** | The `actions` field is optional and may be empty at decision time. |
| **Outcome** | `outcome` (optional, null at decision time) | **Mapped, optional** | The `outcome` is null at signing; ADR 0030 specifies the separate execution-evidence artifact that would carry it. |

### 2.3 What the CDO adds that DES does not carry

The CDO is a signed object with a content hash and an offline verifier. DES's Decision Object is a structured representation; it does not specify a signature, a hash, or a verifier. The `attestation` block, the `integrity` block, and `tools/verify_cdr.py` are the Receipt Layer's contribution.

The CDO also carries the **sequence ontology**: the pre-AI commitment, the gate, and the verifier's `Pre-AI commitment` check. DES's Decision Object records *what* the decision contains; it does not record *when* each element came to exist relative to the AI's disclosure. The CDO's `pre_ai_assessment` and `pre_ai_commitment` blocks, and the verifier's check, are the sequence contribution.

### 2.4 What DES adds that the CDO does not carry

**Objectives and Constraints** are the two components with no CDO equivalent. A decision record that does not carry the objectives the decision was optimizing for, or the constraints that bounded it, cannot answer "was this decision made in service of the right goal?" It can answer "what was decided" and "what evidence was considered," but not "what was the decision *for*."

DES's separation of authority constructs — Decision Object, Decision Permit, Decision Passport, Capability, Authority, Admissibility, Authorization, Permission — is also absent from the CDO. The CDO conflates several of these into a single `attestation` block (who signed) and a `trust_anchor` reference (whether the signer was authorized). The DES separation is a finer-grained ontology that the CDO's authority profile would need to adopt to be fully aligned.

---

## 3. The cross-lineage gap, stated plainly

The mappings show three structural gaps that neither lineage fills on its own:

**The exposure gap (DSES → CDO).** DSES defines eight exposure classes and an independence model derived from them. The CDO records that an AI recommendation was made and what it contained, but not which class of information it conveyed or what the human's information state was at the moment of commitment. The paper's Section 4.1 names this gap. A future CDO schema version that carries `ai_recommendation.exposure_class` and `pre_ai_assessment.independence_class` would close it.

**The objectives and constraints gap (DES → CDO).** The CDO records what was decided and what evidence was considered, but not what the decision was optimizing for or what constraints bounded it. The paper's Section 5.1 acknowledges this. A future `objectives` block and `constraints` block would close it.

**The authority-construct gap (DES → CDO).** The CDO's `attestation` and `trust_anchor` conflate identity, authorization, and legal admissibility into a single reference. DES's separation of Decision Permit, Capability, Admissibility, Authorization, and Permission is finer-grained. The paper's Section 7 separates identity, authorization, legal validity, and accountability as four claims; the CDO's `consent` and `trust_anchor` references carry the first three, but not with the granularity DES specifies.

---

## 4. What the CDO's implementation does and does not do, per the DSES and DES mappings

The mapping shows that the CDO's implementation:

- Carries the **committed decision state** (DSES event 3, via `pre_ai_assessment`) and enforces it as a precondition for AI disclosure (DSES I3(a)). This is the sequence ontology the paper's Section 5.1 claims.
- Carries the **final decision and its attestation** (DSES event 8, via `human_decision` and `attestation`). This is the Receipt Layer's contribution.
- Carries the **evidence set with a bounded universe and completeness check** (DES Evidence, with the completeness model from Section 6 of the paper). This is the provenance ontology the paper's Section 5.1 claims.
- Does **not** carry the **exposure class, information state, or interaction event** (DSES events 2, 5, 6). This is the exposure gap.
- Does **not** carry **Objectives or Constraints** (DES components 3 and 5). This is the objectives-and-constraints gap.
- Does **not** carry the **authority constructs at DES's granularity** (Decision Permit, Capability, Admissibility, Authorization, Permission). This is the authority-construct gap.

The paper's Section 4.1 classification — sequence and provenance independently verifiable, authority partially implemented — is accurate against the DSES and DES mappings. The mapping file's contribution is to make the "partially" precise: it names the specific DSES events and DES components that the CDO does not carry.

---

## 5. Status of this companion file

This is v0.2. The DSES event-level mapping is complete for the ten events named in DSES v0.1. The DES component-level mapping is complete for the ten components. The exposure, objectives, constraints, and authority-construct gaps are named.

What remains for a future version:

- A mapping of DSES's **independence classes** (`UNEXPOSED`, `INDIRECTLY_EXPOSED`, `DIRECTLY_EXPOSED`, `POST_ACTION`) onto a proposed `pre_ai_assessment.independence_class` field in a future CDO schema version.
- A mapping of DSES's **eight exposure classes** onto a proposed `ai_recommendation.exposure_class` field.
- A mapping of DES's **authority constructs** (Decision Permit, Capability, Admissibility, Authorization, Permission) onto the CDO's `consent`, `trust_anchor`, and `disclosure` blocks.
- A proposed CDO schema extension (`cdo-1.1`) that carries the exposure class and independence class as first-class fields, with the verifier checks that would enforce them.

These are future work, not gaps in the current mapping. The exposure and
independence half is now specified in
[ADR 0067](../HEALTHCARE/06-decisions/0067-ai-exposure-is-attested-not-inferred.md)
(`presentation_state.v1`, fail-closed independence, additive verifier checks);
implementation is pending.

---

## References

### Primary sources

1. Henderson JM. Decision-Sequence Evidence Schema (DSES), version 0.1.0 (Draft for public comment). Evidify LLC, August 15, 2026. §4 (ten-event vocabulary), §5 (eight-class exposure ontology), §6 (information-state and independence), §7 (integrity classes), §8 (conformance levels).

2. Pinar A. Decision Objects: The Fundamental Unit of Decision Engineering Science. Zenodo. Published 25 August 2026. https://zenodo.org/records/22094077

3. Pinar A. Decision Engineering Science — Canonical Definitions and Formal Constructs v1.0. Zenodo. Published 25 September 2026. https://zenodo.org/records/22958726

4. Pinar A. Decision Engineering Science — CRN-02: Canonical Runtime and Evidence Semantics Normalization. Zenodo. 2026.

### Internal sources (PersonaVault repository)

5. Clinical Decision Object Specification (CDO 1.0). `docs/HEALTHCARE/04-standards/cdo-1.0.md`.

6. ADR 0035 — The CDO Carries Six Governance References. `docs/HEALTHCARE/06-decisions/0035-the-cdo-carries-six-governance-references.md`.

7. ADR 0030 — The Execution Evidence Gap. `docs/HEALTHCARE/06-decisions/0030-the-execution-evidence-gap.md`.

### Cross-reference

8. Jhol R. Beyond AI Audit Trails: The Three Foundations of Verifiable Decision Evidence, v3.1. `docs/papers/three-foundations-of-verifiable-decision-evidence.md`. Sections 4.1 and 5.1 cite this mapping file.
