---
title: "Beyond AI Audit Trails: The Three Foundations of Verifiable Decision Evidence"
author: Rajinder Jhol
version: 3.2
status: draft-for-circulation
date: 2026-11-05
audience: external
companions:
  - docs/HEALTHCARE/04-standards/cdo-1.0.md
  - docs/HEALTHCARE/06-decisions/0035-the-cdo-carries-six-governance-references.md
  - docs/evidence/disclosure-gate/passing.cdr.json
---

# Beyond AI Audit Trails: The Three Foundations of Verifiable Decision Evidence

**Rajinder Jhol**

*Draft v3.1 — for external circulation*

---

## Abstract

Organizations document that AI-assisted decisions happened. They rarely produce evidence that an independent party can *believe* without trusting the organization that produced it. The gap is not one of logging fidelity. It is a gap in the structure of what is recorded.

This paper argues that a consequential AI-assisted decision is not independently verifiable unless three distinct propositions can each be established: **sequence** (did the human form a judgment before the AI's output could shape it?), **provenance** (what evidence was available, what was considered, and what was omitted?), and **authority** (by what right was the decision made, and is that right verifiable by a stranger?). These three are orthogonal. They answer different questions, fail in different ways, and are verified by different mechanisms. Sequence evidence addresses retroactive rationalization. Provenance evidence addresses evidentiary incompleteness. Authority evidence addresses portability collapse.

The paper makes four contributions. First, it names the trichotomy and shows that it is a diagnostic, not a taxonomy: different artifact classes require different subsets of the three. Second, it evaluates the principal lineages against a uniform six-level classification—absent, conceptual, specified, implemented, independently verifiable, independently verified—and shows that no lineage identified in this review carries all three at the independently-verified level. Third, it reports an implemented reference case: the Clinical Decision Object (CDO) and its offline verifier, which together carry the sequence and provenance ontologies in a signed payload and pass a verifier that fails a CDR carrying AI policies without a pre-AI commitment. A reviewer can run `docs/evidence/disclosure-gate/verify_demo.sh` and see `DECISION INTEGRITY: VALID` with `Pre-AI commitment` among the fourteen passed checks. Fourth, it decomposes IEEE P3867's requirement for "immutable audit trails" and "verifiable evidence collection" into sequence, provenance, and authority checks, and specifies what each check can and cannot prove.

The paper invites a specific challenge: an existing architecture that can independently establish sequence, provenance, and authority for a consequential AI-assisted decision. If such an architecture exists, the framework fails to distinguish it, and the paper's comparative claim is wrong. The falsification conditions are stated in Section 11.

The paper is also explicit about the limit that matters most: a cryptographic commitment proves the integrity of a recorded sequence. It does not prove the independence of the underlying cognition. That distinction is the boundary between a framework that can survive scrutiny and one that overclaims. The paper's implementation claims are graded on the same scale it applies to others: two of the three ontologies are *independently verifiable* by a separate verifier but have not yet been *independently verified* by an external party; the third is partially implemented and specified. The sequence ontology's "independently verifiable" is qualified: a CDR produced for a query the packs do not fire policies for passes without the verifier's `Pre-AI commitment` check having run. The paper's reference case and the benchmark at `benchmarks/decision-evidence-v0/` demonstrate both states.

---

## 1. Introduction: The Difference Between a Log and Evidence

The governance of AI-assisted decisions has a structural blind spot. Organizations produce logs, dashboards, and attestations. Regulators, insurers, and courts ask a different question: *can you prove that the policy executed, independently of your claim that it did?*

A log is evidence of what the originating system recorded. It is not, by itself, evidence that an independent party can verify without relying on the originating organization. That distinction — between the record a system makes and the evidence a stranger can believe — is the subject of this paper.

The distinction is now being made explicitly in the regulatory literature. A commentary on Article 12 of the EU AI Act puts it plainly: the record-keeping obligation "reads like a storage clause, and most teams treat it that way: capture enough, keep it long enough, produce it on request. The harder requirement is sitting underneath that. The records only matter at the moment someone outside the operator picks them up and tries to use them, and at that moment the question is not 'did you keep a log' but 'can I believe this one without believing you'". The prescription is exact: signed receipts over a canonical form, a second independent checker, a sequence with a terminal marker so gaps are legible, and verification that fails closed.

This paper is about what such a record must contain. It argues that the answer is not one thing but three, and that the field has been building each of the three without naming the relationship between them.

### 1.1 The three propositions

Any consequential decision made with AI assistance raises three separable questions.

**Sequence:** *Did the human form an independent judgment before the AI's output could shape it?*

**Provenance:** *What evidence was available, what was considered, what was excluded, and what is missing?*

**Authority:** *By what right was the decision made, and can that right be verified by a stranger?*

A record can answer the first and fail the third. A record can answer the third and fail the first. The failure modes are distinct, and conflating them is the error this paper exists to correct.

### 1.2 The Verifiable Decision Record

The object that answers all three is not a log, an audit trail, or a signed decision in isolation. It is an **evidence object** that allows an independent party to test three propositions: that the decision evolved in the order claimed, that the evidence supporting it can be accounted for, and that it was made under verifiable authority. This paper calls that object a **Verifiable Decision Record (VDR)**.

The VDR is a conceptual standard, not a product. It defines what must be true of any artifact that claims to be independently verifiable decision evidence. It is separable from any particular implementation: the framework stands whether or not the Clinical Decision Object exists.

The word "ontology" in this paper is not the data-governance sense. A data ontology models business concepts — Customer, Order, Asset — and their relationships, so that the data inside a system means the same thing everywhere. A decision ontology models the evidence claims a decision record must make, so that a stranger can verify them. The two are complementary: a data ontology governs what the data means; a decision ontology governs what the record proves. A record can have perfectly consistent data and still fail to prove the human judged first. The four questions that distinguish any two ontologies — what is the domain, what is the criterion of identity, what are the relations, what is the purpose — are what this paper calls the sequence, provenance, and authority claims for decision evidence.

### 1.3 Two artifacts, two names

This paper distinguishes two artifacts throughout, and holds the distinction.

The **Clinical Decision Object (CDO)** is the signed payload: the structured record of a decision, its deliberation, its AI participation, and its attestation. It is what the decision-maker signs.

The **Clinical Decision Receipt (CDR)** is the portable artifact that carries the CDO and the material an offline verifier needs to check it — the attestation, the chair's public key, the transcript binding, the version chain. The CDR is what a stranger can hold, verify, and keep.

The distinction matters because the CDO can exist inside the producing system without the CDR existing outside it, and the CDR can be verified without the producing system's cooperation. The paper's claims are about the CDO when it is built and about the CDR when it is verified; the two are not the same artifact and are not used interchangeably.

### 1.4 What this paper does not claim

It does not claim that a VDR proves a decision was correct. A perfectly conforming record can document a terrible decision. It does not claim that cryptography proves independent human cognition. It proves the integrity of a recorded sequence, and the paper is explicit about that boundary in Section 2.4.

It does not claim that the CDO is complete. Section 5 states exactly what is shipped and what is not, with a commit and a test for each claim, and grades the implementation on the same six-level scale the paper applies to every other lineage.

It does not claim that no other architecture could satisfy all three propositions. Section 3 defines the criteria by which any architecture can be tested, Section 11 states what would falsify the framework, and Section 12 specifies a benchmark that would let a party who disagrees with the authors test the claims on records the authors did not construct.

---

## 2. The Framework

### 2.1 Sequence

Sequence evidence records the order in which epistemic states occurred. Its unit is the event. Its verification is ordering and binding: the commitment hash was signed before the disclosure timestamp; the revision references the commitment; the rationale references the revision.

The most mature sequence vocabulary in the field is the Decision-Sequence Evidence Schema (DSES). Version 0.1.2 defines a ten-event vocabulary for human-AI decision sequences, an eight-class exposure ontology, an information-state and independence model, four integrity classes, and three conformance levels, with mappings to HL7 FHIR AuditEvent and Provenance, IHE Radiology AI profiles, DICOM, and OpenTelemetry. It is an open, vendor-neutral vocabulary for evidence of how humans and AI make decisions together.

DSES is explicit about its boundary. A single export establishes internal consistency only absent external anchoring. The specification tells the reader what it does not prove, which is a virtue.

### 2.2 Provenance

Provenance evidence records what was considered. Its unit is the reference. Its verification is content addressing and **completeness**: the source's hash matches the artifact's canonical bytes; the record shows what was available and skipped; the gaps are named.

Provenance is the least developed of the three in the clinical literature and the most developed in the agentic and supply-chain literature. The IETF's Verifiable AI Provenance (VAP) framework defines a portable, self-verifying bundle for offline third-party verification: events, Merkle proofs, anchor records, external anchor tokens, and key material references, verifiable without access to the system that produced them. VAP's contribution is the recognition that provenance is not a list of sources but a verifiable structure.

The Five Tests Standard (5TS) makes provenance one of five normative tests and is honest about the maturity gap: provenance is "normative in v1.2.0 but not yet mechanically verifiable," with conformance deferred until input-origin binding is defined.

The provenance question is harder than "what was retrieved." A record that lists three sources and omits that a fourth existed is not incomplete in a way the reader can detect. The provenance ontology must make the incompleteness legible. Section 6 defines the canonical bounded evidence universe that makes this possible.

### 2.3 Authority

Authority evidence records by what right the decision was made. Its unit is the external artifact. Its verification is content addressing and authority-chain validation: the consent reference matches the external artifact's canonical bytes; the trust anchor reference terminates in a recognized registry; the signer's permit was valid at the attested time.

The most sophisticated authority ontology in the field is the Agent Passport System (APS). It specifies Ed25519-based agent passports, scoped delegation chains with monotonic narrowing across seven constraint dimensions, cascade revocation, a three-signature policy chain (intent, evaluation, receipt), and signed receipts that record what an agent declared, what a policy engine decided, and what an enforcement boundary observed. Authority is modeled as an element of a product lattice, and delegation is a monotone function on that lattice, "ensuring that delegated capabilities can only be attenuated, never amplified".

APS is authority-rich and sequence-light. It records what the *agent* declared; it does not record what the *human* concluded before the agent acted. That is the boundary this paper's trichotomy makes visible.

### 2.4 The limit that matters: integrity is not independence

A cryptographic commitment proves something narrower than independent human judgment. It proves that a particular representation was committed at a verifiable point in an ordered chain, that a subsequent record can be bound to it, and that it was not altered afterward without detection.

It does not prove that the human genuinely believed what was recorded, that the human had not already been exposed to equivalent AI advice elsewhere, that the commitment was not produced mechanically or under coercion, or that the human reasoned independently.

This distinction is the difference between **integrity of the recorded sequence** and **independence of the underlying cognition**. The former can be cryptographically verified. The latter can only be supported by evidence and evaluated with appropriate limitations. A framework that claims more than this is overclaiming, and a reviewer who knows what signatures do will find the overclaim.

The clinical evidence shows why the narrower claim still matters. A retrospective evaluation of a generative AI-enabled electronic medical record system across sixteen primary care clinics in Kenya found that clinicians adopted harmful recommendations in 58% of cases and beneficial recommendations in 22%—a pattern invisible without a record of what the clinician thought first. A randomized trial in *NEJM AI* found a 14-percentage-point reduction in diagnostic accuracy among physicians exposed to erroneous LLM suggestions despite AI literacy training and full discretion to reject. These findings do not prove that a commitment gate would fix the problem. They prove that the sequence question is not academic. It is the difference between oversight that is real and oversight that is asserted.

### 2.5 Why the three are orthogonal

| Ontology | The question | Failure mode | What cryptography can prove | What it cannot prove |
|---|---|---|---|---|
| Sequence | What happened, and in what order? | Retroactive rationalization | Ordering, binding, non-alteration | That the human reasoned independently |
| Provenance | What evidence was available and considered? | Evidentiary incompleteness | Content address, internal completeness against a declared universe | That the declared universe was the right one |
| Authority | Who had the right to decide? | Portability collapse | Identity, delegation chain, revocation status | That the decision was lawful in the full legal sense |

A system can be excellent at one and fail catastrophically at another. A signed record does not establish independent judgment. A complete evidence list does not establish lawful authority. A pre-AI commitment does not establish that the evidence base was complete.

The three ontologies are orthogonal in a specific sense that the data-governance use of the word does not carry. A business ontology that standardizes what "Customer" means does not make any claim about whether a human formed a judgment before an AI spoke. It cannot, because its domain is the meaning of terms, and the claim this paper is about is the order of events. The two kinds of ontology answer different questions: one is about consistency of meaning across a system, the other is about verifiability of a sequence by a stranger. A hospital can have a perfectly governed data ontology and no evidence ontology at all. The two are not substitutes; they are not even adjacent.

---

## 3. Evaluation Methodology

### 3.1 The six-level classification

The paper's comparative claim requires a method, not an assertion. Every lineage is classified on each ontology using six levels.

| Level | Meaning |
|---|---|
| **Absent** | No corresponding mechanism |
| **Conceptual** | Described but not specified |
| **Specified** | Defined formally |
| **Implemented** | Present in working software |
| **Independently verifiable** | A separate verifier can test it without relying on the originating system |
| **Independently verified** | An external party has actually tested it |

The distinction between the last two levels is deliberate. A project's own verifier can make an artifact *independently verifiable*: the verifier runs outside the system, against the exported artifact, and needs nothing from the producing system. But only a party outside the project can make an artifact *independently verified*, because only an external party's test is genuinely independent of the project's own assumptions, fixtures, and staging. The paper grades its own implementation on this scale, and Section 5 states plainly which level each ontology reaches.

### 3.2 Classification procedure

The classification is not a survey of everything the author has read. It is an assessment of each lineage against published sources and, where available, reference implementations. The procedure has three parts.

**Sources examined.** For each lineage, the paper reads the published specification (the Zenodo release for DSES, the working paper for DES, the IETF draft for VAP and APS, the working group publication for 5TS, the vendor documentation for Glacis/OVERT) and, where one exists, the reference implementation. The paper does not credit a mechanism that appears only in prose. A described mechanism without a formal specification is `Conceptual`; a formal specification without a working implementation is `Specified`; a working implementation without an external verifier is `Implemented`; a verifier that runs offline against the artifact is `Independently verifiable`; and an external party's test of that verifier is `Independently verified`.

**Absence by design versus absence by omission.** Some lineages do not implement an ontology because it is outside their scope, and some do not implement it because they have not. The two are distinguished in every classification table. DSES's authority is absent *by design*: the v0.1 specification states explicitly that external trust mechanisms are deferred to separate review cycles. Glacis's sequence is absent *by omission*: the receipt records an AI inference and its control decision, not the human judgment that preceded the AI's disclosure, and nothing in the published documentation suggests the omission is deliberate.

**Ambiguity handling.** When a lineage's published material is silent on a category, the classification is `Absent`, not `Conceptual`, and the silence is noted. When a lineage has material that could be read as addressing a category but does not specify how, the classification is `Conceptual` and the ambiguity is named. The classification is the author's; no external inter-rater check has been performed, and the limitation is stated in Section 3.3.

### 3.3 Limitations of the classification

Three limitations apply to every classification in this paper.

First, the author performed the classification. An external reviewer with domain expertise would plausibly disagree on edge cases, particularly on whether a conceptual description in a supplementary document counts as a `Specified` mechanism. The classification reflects the author's reading of the primary sources, and the sources are cited per row so a reader can re-perform the assessment.

Second, the lineages identified are the ones whose published material bears most directly on the three ontologies as defined here. The paper does not claim to have surveyed every relevant system. The set is bounded by the paper's definition of each ontology, and a lineage that addresses "audit" in a sense orthogonal to the three is not included.

Third, the classification is descriptive, not adjudicative. A lineage that scores `Conceptual` on sequence is not a bad lineage; it is a lineage whose published material does not specify the mechanism. The paper's claim is about what is *specified* and *implemented*, not about what a lineage's authors might build next.

---

## 4. The Lineages

### 4.1 DSES: sequence-rich, authority-deferred

DSES is the most complete sequence ontology in the field. Its ten-event vocabulary, eight-class exposure ontology, and independence model are specified and mapped to clinical informatics standards. The v0.2.0 release (October 2026) adds an outcome-evidence layer: denominator-closed eligibility manifests, outcome linkage, pre-consensus adjudication under declared charters, content-addressed executable rules, recomputable reliance metrics (RAIR, RSR, EAR), and governance constraints on unit of analysis. The release ships a reference verifier, an adversarial suite, RFC 9162 proofs, and reader-supplied external anchor trust.

The authority half is specified, not absent. The v0.2.0's reliance metrics are the calibration instrument the paper's Section 11 asks for: they measure the relationship between the human's pre-AI commitment and the post-AI decision. The external trust mechanisms—signatures, independent anchors, trusted time—remain the deferred layer, and the spec states the limit: a single export establishes internal consistency only unless compared with a separately held checkpoint or supported by verified external anchoring.

Provenance is present only implicitly. The event vocabulary records what was rendered and to whom. The completeness of the evidence base—what was available and not consulted—is not a first-class element.

| Ontology | DSES classification | Note |
|---|---|---|
| Sequence | **Independently verifiable** against its own reference verifier | v0.2.0 ships a reference verifier, an adversarial suite, and RFC 9162 proofs. External anchoring (a separately held checkpoint or a verified anchor) is required for the stronger claim; the v0.2.0 notes say so explicitly. |
| Provenance | **Implemented** | The v0.2.0 outcome layer adds denominator-closed eligibility manifests, outcome linkage, pre-consensus adjudication under declared charters, and content-addressed executable rules. |
| Authority | **Specified** | The v0.2.0 adds recomputable reliance metrics (RAIR, RSR, EAR) and governance constraints on unit of analysis. The external trust mechanisms (signatures, independent anchors, trusted time) remain the deferred layer, stated by the spec. |

### 4.2 The Decision Object: a taxonomy without temporal ordering

Decision Engineering Science (DES) proposes the Decision Object as a persistent, structured representation of a bounded decision instance, with components including signals, context, objectives, evidence, constraints, alternatives, rationale, the decision, action, and outcome. It is the most formally complete representation of *what a decision contains*.

It is not a representation of *when each element came to exist in sequence*. The ten components are a taxonomy, not a timeline. The framework does not specify whether the human's assessment of evidence preceded the AI's contribution, or whether the AI's output shaped the framing of objectives. The Decision Object also does not carry an authority ontology that a third party can verify across institutions.

| Ontology | DES classification | Note |
|---|---|---|
| Sequence | **Conceptual** | Components exist; temporal precedence is not a first-class element |
| Provenance | **Conceptual** | Evidence is a component; completeness is not specified |
| Authority | **Conceptual** | Governance gates are internal, not external references |

### 4.3 The Receipt Layer and the CDO: the unification attempt

The Receipt Layer begins from the premise that a log produced by the investigated party is not, by itself, evidence that an independent party can verify. The Receipt Layer's claim is that a verifiable receipt must prove who authorized the action, what constraints were enforced, who was accountable, and what actually happened—portable, tamper-evident, and verifiable by a third party.

The Clinical Decision Object (CDO) is its clinical instantiation. The CDO 1.0 specification defines required fields (`case_identity`, `knowledge_state`, `ai_provenance`, `human_deliberation`, `ai_recommendation`, `human_decision`, `attestation`, `version_chain`, `integrity`) and optional fields (`actions`, `outcome`, `metadata`), with content-addressing rules and schema versioning that dispatches the verifier on `schema_version`【internal: `cdo-1.0.md`】.

The CDO is the only artifact identified in this review that architectures all three ontologies. It is not the only artifact that claims to. It is the only one whose architecture specifies all three in a single signed payload, with a verifier for the sequence half and a specification for the authority half.

| Ontology | CDO classification | Note |
|---|---|---|
| Sequence | **Independently verifiable** | `pre_ai_assessment` and `pre_ai_commitment` are events, CDO blocks, and verifier checks; the pilot exercises the full path. No external party has tested it → not yet `Independently verified`. |
| Provenance | **Independently verifiable** | `declared_universe` in the payload; five-state availability checked by the verifier; count invariant enforced. No external party has tested it → not yet `Independently verified`. |
| Authority | **Implemented** for `consent` (ADR 0036; verifier checks `status_at_decision`); **Specified** for the other five; **unresolved** for the hash match | The verifier reports `Consent reference (unresolved)`; it does not recompute the hash against the FHIR server's bytes. |

### 4.4 The adjacent lineages

**Glacis/OVERT** is authority-first. Utah's Office of Artificial Intelligence Policy now requires vendors in its AI Learning Laboratory to produce a signed receipt for every covered AI inference or control evaluation. The receipt records the control's decision and the time it was made. Glacis is explicit about what a receipt does not prove: it does not prove the decision was right. Authority is strong; sequence for human judgment is absent by omission; provenance is weak.

**Clinical Truth Chain (CTC)** is authority-heavy and sequence-light. It defines canonical signed receipts anchored to an append-only log and fail-closed admissibility rules. Its sequence is the authorization-to-claim binding, not the clinician's pre-AI judgment.

**5TS** is provenance-aware but the fifth test is not yet mechanically verifiable. Its Proof-Carrying Decision objects encode custody, lineage, policy gates, and replay strategy. It is the most explicit about the maturity gap in provenance.

**IETF VAP** is provenance-rich and sequence-light. It provides the Merkle receipt and external anchoring machinery a portable provenance record requires.

**APS** is authority-rich and sequence-light. It is the most complete authority ontology in the field.

The pattern is consistent. Each lineage builds one or two of the three and defers or omits the rest. None identified in this review carries all three at the `Independently verified` level.

---

## 5. The Clinical Decision Object as Reference Implementation

### 5.1 What is shipped and independently verifiable

**The sequence ontology is implemented and independently verifiable.** `pre_ai_assessment` and `pre_ai_commitment` are event types in the deliberation vocabulary, CDO blocks in the payload, and a verifier check. The gate in `_execute` queries the session's commitment; when it exists, the AI recommendation is attached to the CDO; when it does not, the AI recommendation is suppressed and the CDO carries `incomplete: pre_ai_commitment_missing`. The pilot acceptance test exercises the full path for a query that fires the oncology pack: assessment posted, commitment queried, chat turn fires, AI recommendation attached, chair signs, offline verifier passes with `Pre-AI commitment` among fourteen passed checks. The CDR is at `docs/evidence/disclosure-gate/passing.cdr.json`; `verify_demo.sh` runs the verifier against it.

Two qualifications belong with this claim. The first is that the pilot's `passing.cdr.json` was produced under a pipeline state that preceded the current pre-answer gate: the gate now refuses a query whose coverage against the user's prior `DecisionTrace` rows is below 0.5 (`app/services/pre_answer_gate.py:47-50`), and the pilot test does not seed those rows. A reviewer who runs the pilot today gets a passing test, but does not get a fresh `passing.cdr.json` — the committed artifact's provenance is from before the gate, and its file is frozen for that reason. The second is that "the full path" is relative to the query. The oncology pack returns policies for the pilot's MTB case, so the CDR carries `ai_recommendation.policies` and the verifier's `Pre-AI commitment` check runs. A query that the packs match but do not return policies for produces a CDR that carries the commitment, does not carry the policies, and passes 13 of 14 checks with the `Pre-AI commitment` check skipped. The benchmark at `benchmarks/decision-evidence-v0/` demonstrates both: its `e-vdr.json` is the second kind of CDR, produced by the same pipeline against a different query; its `f-vdr-stripped.json` demonstrates the tampering case the verifier detects. Section 5.4 names the three states and the reader's obligation that follows from them.

"Independently verifiable" is the precise level: the verifier runs offline, against the exported CDR, and needs nothing from the producing system. It is not "independently verified" in the Section 3 sense, because no party outside the project has yet run it. That distinction is stated and held.

The claim is precise in a second way, and the precision is worth stating because a careful reviewer will ask. The sequence ontology is independently verifiable for the **enforcement of ordering** — DSES's I3(a) class, in which release of the AI output is mechanically predicated on the existence of a committed decision state. The gate suppresses the AI recommendation when the pre-AI commitment is absent; the verifier checks the commitment's hash and the ordering of its timestamp against the knowledge-state snapshot. It is not independently verifiable for the **strength of the independence claim**, because the CDO does not carry the DSES information-state stamp that would distinguish an `UNEXPOSED` commitment from an `INDIRECTLY_EXPOSED` one. A commitment that was formed after the AI triage reordered the worklist is not the same as a commitment formed before any AI signal reached the human, and the CDO currently records both as "a pre-AI assessment exists." The exposure and independence-class fields are a future CDO schema extension; the mapping file at `docs/papers/mappings-dses-des-cdo.md` (§1.3 and §1.5) names the specific events and fields that would close the gap.

**The provenance ontology is implemented and independently verifiable, but its implementation is a partial mapping of the canonical model.** The CDO carries a `declared_universe`: the repositories queried, the record types, the counts, and the retrieval rules. Every knowledge entry declares one of five availability values. The verifier checks that every entry's availability is one of the five, and that `retrieved_count ≤ available_count`.

The implementation's five values and Section 6's canonical five are **not the same five**, and the mismatch is a real limitation:

| Canonical state (Section 6) | Implementation value | Status |
|---|---|---|
| Retrieved and considered | `referenced` | Mapped |
| Available but not retrieved | `available` | Partial — the implementation records pack knowledge sources as `available` without distinguishing consulted from not |
| Retrieved but excluded | `retrieved_but_excluded` | Mapped |
| Unavailable or inaccessible | `unavailable` | Mapped |
| Outside the declared universe | *not recorded* | **Gap** — the implementation does not yet record items excluded by the declared rules |
| *not in canonical model* | `generated` | Extension — AI-produced content, a domain-specific sixth category |

The paper states this plainly because the assessment of any provenance claim depends on which ontology the claim is against. The implementation is a partial instantiation of the canonical five-state model with a sixth domain-specific value; the "outside the declared universe" state is not yet recorded. The verifier checks internal consistency of the declaration and the entries; it cannot check that the declared universe was the right one, and it cannot check that items outside the declaration were correctly excluded. Those are judgments a reader makes with the declaration in hand.

The DQI reports `pre_commitment_integrity` but does not weight it. The component measures sequence integrity—a precondition for decision quality, not a component of it. The verifier enforces the gate; the DQI reports it.

### 5.2 What is specified and not fully shipped

**Authority hashes.** Of ADR 0035's six references, one—`consent`—is implemented in the payload and status-verified by the verifier. The verifier checks whether `status_at_decision` is `active`, `inactive`, or `revoked`. The status check fires only for records whose `consent.ref_kind` is `fhir_consent`; a record whose `ref_kind` is `pack_basis` takes a different branch and passes regardless of `status_at_decision`. The benchmark at `benchmarks/decision-evidence-v0/` demonstrates both: `j-revoked-consent.json` is a `fhir_consent` record with revoked status and fails at `Consent`; the `J-basis` variant described in the benchmark's README (a `pack_basis` record with `status_at_decision: revoked`) would pass, because the status field is not read. The verifier does **not** recompute `ref_hash` against the FHIR Consent's canonical bytes: the body lives in the FHIR server, not the CDO, and the verifier is offline by design. It reports `Consent reference (unresolved)` rather than failing. The other five references—`disclosure`, `trust_anchor`, `ai_transparency`, `outcome`, `feedback`—are specified in ADR 0035 and post-pilot.

**The collective commitment.** The chair workflow is single-signer. Multiple attendees can author messages, post dissents, and contribute to the deliberation. The `human_deliberation` block captures this multi-author participation (participants, proposals, dissent, rationale, and transcript). However, only the chair holds the cryptographic authority to sign the final record. The "Submit for review" step asks the other attendees to review the record before the chair applies the signature. There is no per-participant pre-AI commitment and no automated aggregation rule. Section 9 specifies the layered commitment model as a design and states what is not yet built.

### 5.3 The honest claim

The CDO instantiates the framework. It does not complete it. In the Section 3 classification:

- Sequence: **independently verifiable** for queries that fire a policy-producing pack (see Section 5.4).
- Provenance: **independently verifiable**, with a partial mapping to the canonical model.
- Authority: **implemented** for `consent` and status-verified; **specified** for the other five; **unresolved** for the hash match.

No ontology is yet **independently verified**, because no party outside the project has tested the verifier. That is the correct classification, and it is what the paper claims.

The paper's Sections 5.1, 5.2, 5.3, 5.4, and its abstract were revised after a companion benchmark (`benchmarks/decision-evidence-v0/`) demonstrated that several of the paper's claims were narrower in the code than the prose implied. The benchmark did not confirm the paper; it corrected it, which is the more valuable outcome. The corrections are visible in the current text — the sequence ontology's coverage depends on the query firing a policy-producing pack, the pre-AI commitment check has both an absence and an ordering branch, the consent status check is conditional on `ref_kind`, and the transcript binding is self-consistency rather than authenticity — and each is demonstrated by a record in the benchmark. A reader who wants the full list of what the verifier does not check should read the benchmark's README, not this paper; the division is deliberate.

The sequence classification is qualified by Section 5.4's third state: a CDR produced for a query whose matched packs return no policies carries the pre-AI commitment but passes without the verifier's `Pre-AI commitment` check having run. The sequence ontology is independently verifiable *for queries the packs fire policies for*; for others the verifier is silent. Section 5.4 names the three states and the reader's obligation that follows from them.

### 5.4 Prevention and detection are the same guarantee at different layers

The verifier fails a CDR that carries AI policies without a matching `pre_ai_commitment`. This check has two failure branches. The first is **absence**: the commitment is not there. The second is **ordering**: the commitment is present, but `pre_ai_commitment.committed_at` does not precede `knowledge_state.captured_at` — the human's committed plan is recorded after the snapshot of what the AI could know, which is the failure a backdated knowledge state would produce. Both branches fail the same check name (`Pre-AI commitment`); the verifier's message distinguishes them. The benchmark at `benchmarks/decision-evidence-v0/` demonstrates both: `b`, `d`, and `f` fail the absence branch; `h-backdated-knowledge.json` fails the ordering branch. The gate ensures a CDR produced by the system never carries AI policies without a commitment: when the commitment is absent, the AI recommendation is suppressed and the CDR carries `incomplete: pre_ai_commitment_missing`.

The two are the same guarantee expressed at different layers. The gate is **prevention**: a system that has not committed to a pre-AI assessment cannot produce an AI-attached decision record through the normal flow. The verifier is **detection**: a CDR that somehow carries AI policies without a commitment fails structural verification, which is what happens if a record is tampered with after signing.

The verifier's `Pre-AI commitment` check is keyed on `ai_recommendation.policies`, not on the `pre_ai_commitment` block. When a CDR carries policies and a commitment, the check passes. When it carries policies and no commitment, the check fails. When it carries a commitment but no policies — because the pack the query matched returned no policies — the check is **skipped**, and the CDR passes without the gate's check having run. The CDO's `incomplete` marker names this state; the verifier does not read it. Three observable states follow, and the verifier distinguishes the first two:

| `ai_recommendation.policies` | `pre_ai_commitment` | verifier behavior |
|---|---|---|
| present | present | passes `Pre-AI commitment` |
| present | absent | fails `Pre-AI commitment` |
| empty | present | **skips** the check |

The third state is not a defect in the gate or the verifier. The gate correctly attaches the AI recommendation only when the commitment exists; the verifier correctly skips a check that has nothing to check against. But it means that a CDR can carry a valid pre-AI commitment and the verifier can be silent about it — and a reader of a passing CDR cannot tell, from the failure column alone, that the check did not run. The reader must check whether `Pre-AI commitment` appears in the passed list, not only whether the CDR failed. The paper states what the verifier checks. The benchmark at `benchmarks/decision-evidence-v0/` states what it does not: ten records, seven failure modes, and the three limits named in this section and the section before it. The two documents are read together.

The benchmark at `benchmarks/decision-evidence-v0/` demonstrates all three states. Its `e-vdr.json` record is the third: a CDR produced by the real pipeline for a query whose matched packs returned zero policies, carrying a valid `pre_ai_commitment` (the pipeline recorded it), and passing 13 of 14 checks because the verifier's check did not run. Its `f-vdr-stripped.json` record is the second: a real CDR from the pilot with the commitment stripped, failing on `Pre-AI commitment`. The pilot's `passing.cdr.json` is the first. The benchmark records the current behavior; the recommendation for a future sprint — key the check on `pre_ai_commitment`'s presence rather than on `ai_recommendation.policies` — is a design change, not a paper claim. A second remedy, orthogonal to the verifier's keying, is the packs' coverage: a query the packs fire policies for produces a CDR that exercises the check. The pipeline's coverage of the `Pre-AI commitment` check depends on both the verifier's design and the packs' behavior, not on the verifier alone.

One further limit is worth stating in this section, because it is a check a reader might assume is stronger than it is. The verifier's transcript check recomputes `canonical_hash(transcript.payload)` and compares it to `transcript.content_hash`; if the CDO carries `human_deliberation.transcript_hash`, the verifier also checks that the two agree. **The transcript guarantee is self-consistency, not authenticity.** A fabricator who rewrites a transcript segment and recomputes the content hash and the deliberation binding — the `i-alt` variant the benchmark describes in its README — passes all fourteen checks. The verifier has no external anchor for the transcript's content; that is a limit of an offline verifier, not a defect of this one. The record `i-fabricated-transcript.json` demonstrates the check working against a naive fabricator who changes the payload without updating the hash.

The unit tests prove the verifier's detection for the second state; the pilot proves the gate's prevention for the first; the benchmark demonstrates the third, and makes the reader's obligation explicit: a passing CDR is a stronger claim than a CDR that did not fail.

---

## 6. Bounded Provenance Completeness

The provenance question is not "what was retrieved?" It is "what was available, and what does the record show about the difference?" Without a boundary, the second question has no answer.

A completeness claim therefore requires a defined **bounded evidence universe**. The system declares the repositories, record types, time window, and retrieval rules against which completeness is asserted. It then classifies every item in the universe into one of five canonical states:

1. **Retrieved and considered** — present in the evidence set and used.
2. **Available but not retrieved** — present in the universe and not returned by the retrieval process.
3. **Retrieved but excluded** — returned and deliberately set aside, with a recorded reason.
4. **Unavailable or inaccessible** — known to exist but not reachable.
5. **Outside the declared universe** — not in scope by the declared rules.

This is the canonical model. Section 5.1 states how the current implementation maps onto it: three of the five are directly recorded, one is partial, one is not yet recorded, and a sixth (`generated`) is a domain-specific extension.

The verifier checks two invariants: every entry's availability is one of the implementation's five values, and `retrieved_count ≤ available_count`. A record that declares a narrow universe is complete against that universe, and the declaration is visible. This turns provenance completeness from an attractive principle into something technically implementable.

It also makes the limit explicit. The verifier can prove that every declared entry carries a valid status and that the counts are consistent. It cannot prove that the declared universe was the right one, and it cannot prove that items outside the declaration were correctly excluded. Those are judgments for the reader, and the record should make the judgment possible rather than foreclose it. The paper's provenance claim is therefore bounded, and it is stated in terms the verifier can support rather than in terms it cannot.

---

## 7. Authority: Identity, Authorization, Legal Validity, Accountability

A cryptographic trust anchor can establish that a credential or authority assertion chains to a recognized issuer. It cannot, by itself, establish that a decision was lawful in the full legal sense.

The authority ontology must therefore distinguish four claims:

**Identity.** Who or what signed?

**Authorization.** What was that entity permitted to do at the moment of signing?

**Legal admissibility.** Was the authority valid under the applicable legal and institutional rules—consent valid and informed, person competent to authorize, decision within scope, applicable requirements satisfied?

**Accountability.** Who is responsible for the resulting decision?

The cryptographic architecture can make the first two independently verifiable. It can carry references that make the third *checkable* against external artifacts. It cannot replace the legal and institutional interpretation of those artifacts. A consent reference proves that a consent artifact existed and was unaltered. It does not prove that the consent was informed.

The CDO's authority references are designed to carry all four claims as content-addressed links: the trust anchor for identity and authorization, the consent and disclosure references for legal basis, and the attestation for accountability. The verifier can check the links. It cannot adjudicate the legal question. That distinction must be visible in the record, or the record will be read as claiming more than it can prove.

---

## 8. Standards Implications

IEEE P3867, "Standard for Risk Quantification and Digital Auditing of Human-Machine Synergy in Medical Artificial Intelligence," was approved as a PAR on 2026-06-04. It establishes a risk quantification and digital auditing framework for human-machine synergy, defines a six-level autonomy matrix (M0–M5), and specifies technical criteria for continuous dynamic supervision mechanisms—including secure data logging, algorithmic transparency, and immutable audit trails—to facilitate "verifiable evidence collection during human-AI collaborative workflows". It names medical liability insurance providers as a stakeholder.

The requirement is underspecified until it is decomposed. An audit trail of what? Evidence of which relationship?

The trichotomy gives the working group a decomposition, but the decomposition is relative to the **artifact class**, not universal.

| P3867 requirement | Sequence check | Provenance check | Authority check |
|---|---|---|---|
| Immutable audit trails | Pre-AI commitment precedes disclosure; commitment hash recomputable; revision references commitment | Evidence references are content-addressed; the declared universe is recorded | Signer identity and permit are referenced and resolve |
| Verifiable evidence collection | — | Every item in the declared universe is classified; omissions are named | Consent, disclosure, and trust-anchor references resolve and validate at decision time |
| Digital auditing | Ordering survives independent replay | Completeness survives independent replay | Authority chain survives independent replay |

A conforming **consequential-decision evidence record** must satisfy the ontology requirements applicable to its declared artifact class. For binding clinical decisions, that means all three. For exploratory research, it means sequence and provenance, without authority. For a control-execution receipt, authority may be the principal requirement.

This is a **proposed** decomposition for the working group, not a requirement already adopted by IEEE. The paper offers a vocabulary the group can use; it does not claim the group has used it. The distinction matters to any reader who might otherwise treat the table as an interpretation of the standard rather than a proposal to it.

---

## 9. The Collective Case

### 9.1 The problem

The chair workflow is the evidence that the collective case is open. The chair is the deliberation's protagonist【internal: `4.11`】. The chair seeds the draft, authors the decision, submits for review, and signs. The `human_deliberation` block carries participants, proposals, dissent, rationale, and transcript. Multiple attendees can author messages and record dissents; the record captures their contributions. But the decision is signed by one actor. The workflow is multi-author, single-signer.

A tumor board, investment committee, credit committee, or public-sector panel is different. Its value is not a single expert's independent judgment; it is collective deliberation with distributed expertise. The pre-AI assessment is not a single commitment. It is a distributed, negotiated, sometimes contested view assembled across specialties and sometimes across sessions.

None of the three lineages handles this. DSES's independence model assumes a single clinician. The Decision Object's bounded instance does not specify collective commitment. The CDO's chair workflow separates authorship from signing: multiple attendees contribute, one signs.

### 9.2 The layered commitment model

The direction this paper proposes is **layered commitments**. The model is specified here as a design, not implemented.

**Per-participant commitment.** Each participant who contributes to the deliberation posts a `pre_ai_assessment` and a `pre_ai_commitment` in the ordinary way. The commitment is the sha256 of the participant's assessment, canonicalized as the single-clinician case already defines. Each participant's commitment is a content-addressed artifact, timestamped and signed by that participant's key.

**Session-level aggregation.** When the deliberation closes and the chair authors the decision, a **session-level commitment** aggregates the individual commitments under a declared rule. The rule is one of three, chosen by the chair and recorded in the aggregation:

- **Consensus:** every participant whose commitment is in the session must have assessed the same plan hash.
- **Chair synthesis:** the chair's plan hash is recorded, and every participant's commitment is retained as an input that was considered.
- **Recorded dissent:** each dissenting participant's commitment is preserved alongside the chair's, and the dissent is a first-class element of the record.

**The aggregation rule is itself a content-addressed artifact.** The rule's canonical form is hashed and referenced from the session-level commitment, so a change to the rule is visible to any verifier. A reader can check not only what was committed but the rule under which the individual commitments were aggregated.

**What the verifier checks.** For a session-level commitment, the verifier checks that: (a) each per-participant commitment is present, signed, and has an `assessed_at` timestamp before the earliest `disclosed_at` timestamp in the session; (b) the aggregation rule's hash matches the rule's canonical bytes; (c) the chair's plan hash is present; (d) if the rule is `consensus`, every participant's plan hash equals the chair's; (e) if the rule is `recorded_dissent`, every dissenting participant's plan hash is preserved and named.

**What the verifier cannot check.** It cannot check that the participants' assessments were formed independently of each other, or that the aggregation rule was the right one to use, or that a participant who was present but did not post a commitment was meaningfully included in the deliberation. Those are judgments for a reader with the record and the deliberation transcript in hand, and the layered model makes the judgment possible by recording what each participant committed and under what rule it was aggregated.

### 9.3 What is not implemented

The layered commitment model is a design, not a build. Section 5's classification reflects this: the collective case is **open**, and the chair workflow is multi-author, single-signer. The paper does not claim otherwise.

---

## 10. Beyond Clinical AI

### 10.1 Finance: the model-risk framework does not cover generative AI

The US model-risk guidance, SR 11-7, required banks to validate quantitative models used in decision-making before deployment. On 17 April 2026, the Federal Reserve issued SR 26-2, superseding SR 11-7. The new guidance narrows the model definition to exclude simple arithmetic and deterministic rules-based calculations as well as generative and agentic AI. Generative and agentic AI are "explicitly outside the guidance's scope, signaling likely future regulatory treatment elsewhere". The World Economic Forum's analysis puts the consequence plainly: the rule "excludes generative and agentic AI models pending future guidance, leaving banks accountable but without specific regulatory playbooks for AI systems".

The revised guidance leaves generative and agentic AI outside its model-risk framework, creating a specific governance gap while their treatment under other supervisory mechanisms develops. A bank can be fully compliant with SR 26-2 and have no evidence that its loan officers formed an independent judgment before an LLM's recommendation appeared, because the LLM is outside the model-risk perimeter. The authority ontology is mandated for traditional models; the sequence ontology is not mandated at all for generative systems.

### 10.2 Agentic systems: authority and provenance without human sequence

The agentic standards space is building two of the three ontologies with sophistication. APS builds authority: passports, delegation chains, a product lattice of authority, cascade revocation, a three-signature policy chain, and signed receipts. VAP builds provenance: Merkle commitments, external anchoring, and self-verifying bundles.

Neither builds sequence for human judgment. APS records what the *agent* declared; it does not record what the *human* concluded before the agent acted. VAP records what the *system* produced; it does not record what the *clinician* thought before the system produced it. The agentic space has solved the machine half and left the human half open.

### 10.3 The cross-domain pattern

| Domain | Sequence | Provenance | Authority |
|---|---|---|---|
| Clinical (DSES) | Strong | Weak | Deferred |
| Clinical (Glacis/OVERT) | Absent by omission | Weak | Strong |
| Clinical (CDO) | Independently verifiable | Independently verifiable | Consent implemented; other five specified |
| Finance (SR 26-2) | Absent | Absent for GenAI | Mandated for traditional models only |
| Agentic (APS) | Absent for human judgment | Partial | Strong |
| Agentic (VAP) | Machine-only | Strong | Partial |

The pattern is structural. The lineages are not competing; they are complementary halves and thirds of a single artifact.

---

## 11. What Would Falsify This Framework

A framework that cannot be tested is a position, not a contribution. The trichotomy would be falsified, or substantially weakened, by any of the following:

1. **An existing architecture satisfies all three at the independently-verified level.** If a lineage not identified in this review already carries sequence, provenance, and authority in a single artifact with an independent verifier, the "only lineage identified" claim is wrong and the comparative contribution shrinks to a survey.

2. **Provenance completeness cannot be meaningfully established in a bounded but practical way.** If every realistic evidence universe is either too large to classify or too narrow to be useful, the provenance ontology is a principle without an implementation.

3. **A pre-AI commitment does not materially improve the ability to distinguish independent judgment from automation bias.** If studies show that commitment gates change recorded behavior without changing the underlying reasoning, the sequence ontology documents a ritual rather than a safeguard.

4. **Authority can be verified portably without a federation of trusted registries.** If a simpler mechanism achieves cross-institution verification, the authority ontology's infrastructure dependency is a cost the field need not pay.

5. **A simpler model achieves the same assurance.** If two dimensions, or one, produce the same verifier outcomes across the benchmark, the trichotomy is overfitted to the cases the authors chose.

The framework should be read as a set of claims that these tests could defeat. That is the posture that makes it useful to someone who disagrees.

---

## 12. The Benchmark

The 3x paper states the framework. The benchmark is what would make it a discipline, and it is the next artifact, not this one. Its design is specified here so that it can be run by someone other than the authors.

**The benchmark constructs one consequential decision and multiple evidence records:**

- A conventional audit log.
- A signed decision record.
- A DSES-style sequence record.
- An authority-rich receipt.
- A complete VDR.

**Independent reviewers are asked to establish:**

1. Did the clinician make a judgment before AI exposure?
2. Was the evidence universe sufficiently accounted for?
3. Was the decision made under valid, verifiable authority?
4. Can the record be verified without access to the originating institution?
5. What can the reviewer still not know?

**Adversarial scenarios are injected:**

- A timestamp is altered.
- A pre-AI assessment is submitted after AI exposure.
- A source is silently omitted.
- A consent reference is revoked.
- A signing credential is compromised.
- A rationale is changed retrospectively.
- A collective decision is presented as an individual decision.

**The benchmark reports which systems detect which failures.** A benchmark where the authors construct all records and grade the results is a demonstration. A benchmark that an independent party can run on records the authors did not construct is a test. The second is the one worth building, and it is the one that would let DSES, APS, VAP, and the CDO demonstrate their strengths rather than be characterized by this paper.

---

## 13. Conclusion

The field has been building three halves of one artifact. DSES builds sequence evidence with technical maturity and defers authority. Glacis/OVERT builds authority evidence for AI inferences and is silent on human sequence. The Decision Object provides a component taxonomy without temporal ordering. 5TS and VAP build provenance, with 5TS explicit that its provenance test is not yet mechanically verifiable. APS builds authority for agents. The Receipt Layer, in the CDO, is the only lineage identified in this review that architectures all three—and its state is now demonstrable, not merely claimed.

The contribution is not the architecture. It is the naming of the trichotomy, the uniform classification of the lineages against it, the identification of the boundary case that shows the framework discriminates, the specification of bounded provenance completeness, the separation of identity, authorization, legal validity, and accountability in the authority ontology, and the decomposition of IEEE P3867's requirement into checks that a verifier can enforce.

The honest sentence the paper ends with is this: *The sequence ontology is shipped for the single-clinician case, and the verifier fails a CDR that carries AI policies without a commitment — and passes a CDR that carries a commitment without policies without reading it. The provenance ontology is shipped for the bounded-universe case; the verifier checks every entry's availability and the count invariant, with a partial mapping to the canonical five-state model. The authority ontology has its first reference—consent—shipped and status-verified when `ref_kind` is `fhir_consent`; the other five are specified and post-pilot; the hash match is unresolved by design. The collective case is open. The architecture is the contribution; the implementation is the demonstration; the benchmark at `benchmarks/decision-evidence-v0/` is the limit.*

That is a 3x claim, honestly made, with an artifact a reviewer can run. It is the paper that makes the next paper possible—the one that reports what the benchmark found, on records the authors did not construct, with results the authors did not predict.

---

## References

### Primary lineages

1. Thornton J, Henderson JM. The missing layer: decision integrity as a verifiable assurance layer in interpretive clinical artificial intelligence. *Journal of the American Medical Informatics Association*. 2026;ocag152. doi:10.1093/jamia/ocag152.

2. Evidify LLC. Decision-Sequence Evidence Schema (DSES). Version v0.1.2. Zenodo. Published 16 August 2026. https://zenodo.org/records/21970152.

3. Pinar A. Decision Objects: The Fundamental Unit of Decision Engineering Science. Zenodo. 2026.

4. Jhol R. AI Governance Requires Independent Evidence Not Logs or Claims. LinkedIn. 9 June 2026.

### Standards and regulation

5. IEEE Standards Association. P3867: Standard for Risk Quantification and Digital Auditing of Human-Machine Synergy in Medical Artificial Intelligence. Active PAR, approved 4 June 2026. https://standards.ieee.org/ieee/3867/12615/.

6. Board of Governors of the Federal Reserve System. SR 26-2: Revised Guidance on Model Risk Management. 17 April 2026 (superseding SR 11-7).

7. World Economic Forum. America's new banking risk regulation overlooks AI and shifts the burden of defence. LSE Business Review. 13 October 2026.

### Adjacent implementations

8. VeritasChain Standards Organization. Verifiable AI Provenance (VAP) Framework. IETF Internet-Draft, February 2026. https://datatracker.ietf.org/doc/draft-ailex-vap-legal-ai-provenance/.

9. Pidlisnyi T. Agent Passport System (APS): Cryptographic Identity, Faceted Authority Attenuation, and Governance for AI Agent Systems. IETF Internet-Draft draft-pidlisnyi-aps-02, July 2026. https://www.ietf.org/archive/id/draft-pidlisnyi-aps-02.html.

10. Meyman E. Verifiable AI Governance: The Five Tests Standard (5TS) and Proof-Carrying Decisions. Version 1.2.0. Zenodo. June 2026. doi:10.5281/zenodo.21040296.

### Internal specifications (PersonaVault repository)

11. Clinical Decision Object Specification (CDO 1.0). `docs/HEALTHCARE/04-standards/cdo-1.0.md`. Status: draft.

12. ADR 0035 — The CDO Carries Six Governance References. `docs/HEALTHCARE/06-decisions/0035-the-cdo-carries-six-governance-references.md`. Status: accepted, 3 November 2026.

13. ADR 0036 — The Consent Is Horizontal. `docs/HEALTHCARE/06-decisions/0036-the-consent-is-horizontal.md`. Status: accepted, 3 November 2026.

14. ADR 0030 — The Execution Evidence Gap. `docs/HEALTHCARE/06-decisions/0030-the-execution-evidence-gap.md`. Status: accepted, 24 October 2026.

15. Chapter 4.11 — The Chair Workflow. `docs/HEALTHCARE/03-implementation/chapters/4.11-the-chair-workflow.md`. Status: proven, verified against code 24 October 2026.

16. The Verification Protocol. `docs/HEALTHCARE/02-architecture/the-verification-protocol.md`.

17. Comparison to Existing Work. `docs/HEALTHCARE/07-research/comparison-to-existing-work.md`. Status: draft.

### Demonstration artifacts

18. `docs/evidence/disclosure-gate/passing.cdr.json` — the CDR produced by the pilot acceptance test.

19. `docs/evidence/disclosure-gate/verify_demo.sh` — runs the offline verifier against the demonstration CDR.

### Commits (studio/wire-up branch)

- `c0024cc` — feat(governance): the disclosure gate — Events 2 and 3
- `8e6ebef` — feat(governance): bounded evidence universe and provenance completeness
- `76fc6bd` — feat(governance): consent reference check in the offline verifier
- `03a672d` — feat(governance): DQI reports pre_commitment_integrity
- `efba3c3` — test(governance): pilot runs the disclosure gate end-to-end; verifier stays offline
- `f97b0c3` — test(governance): pilot exports the passing CDR as evidence

---

**Draft status.** This is v3.1. It is the version that matches what is in the repository and that grades the implementation on the same six-level scale it applies to every other lineage. Five of the paper's structural claims are implemented and independently verifiable; one of the six authority references is implemented and status-verified; the rest are specified and post-pilot. The demonstration is at `docs/evidence/disclosure-gate/`. Every external regulatory and standards claim should be independently verified before external circulation, particularly the characterization of SR 26-2 and the interpretation of IEEE P3867. The DSES→CDO and DES→CDO mapping tables referenced in Section 4 remain under construction; they will be added in a companion file, not inside this paper.
