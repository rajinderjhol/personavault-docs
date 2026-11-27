# Sovereignty Claims Need Evidence

## What a signed decision layer can prove — and what it cannot

---

### Status

This is a **perspective whitepaper**, not a peer-reviewed article, a certification,
or a product datasheet. It uses external frameworks as attributed vocabulary.
It makes no claim that PersonaVault delivers AI sovereignty, regulatory
compliance, clinical correctness, or external assurance.

**Date:** 2026-11-26

---

### Abstract

"Sovereign AI" has become a common phrase in clinical and public-sector
procurement. It is also an unusually slippery one. Academic analysis of 92
national AI strategies finds three different concerns behind the word —
strategic autonomy, domestic capability, and normative self-determination — and
warns that vendors can repackage ordinary cloud and AI services as sovereignty
solutions. Enterprise research finds a parallel gap: leaders are confident they
can produce evidence of control, but far fewer can produce evidence that
withstands scrutiny.

This paper takes a narrower question. Not *are we sovereign?*, but *what can we
prove about a governed decision when it is challenged?* It describes a signed
decision layer that binds the chair's attestation, the evidence state, the AI
composition, and the declared connectivity mode into one offline-verifiable
object. It states precisely what that object proves — bytes, attribution,
version binding, recorded mode — and what it does not prove: national
capability, absence of network egress, clinical correctness, legal validity, or
third-party assurance.

The argument is that proof should be built as a discipline at the level of the
decision record, rather than asserted as a property of a product.

---

### 1. The problem with the word

Three external frames are useful, provided they are used as lenses rather than
ratings.

Guenduez and Radu (*Decoding AI sovereignty*, Government Information Quarterly
43, 2026) reconstruct three dimensions from national AI policy documents:
**domestic capability** (skills, research, institutions), **strategic
autonomy** (direction of development, infrastructure control, resilience), and
**normative self-determination** (ethical, legal and risk-management conditions).
They explicitly study policy *articulation*, not achieved state capacity, and
they name the practice of **sovereignty washing** — vendors presenting
commercial services as solutions to political dependency.

IBM's *Digital Sovereignty Index* (November 2026) defines sovereignty as
retained control plus credible evidence of that control, measured across six
dimensions: Responsibility, Trace, Constraint, Intervention, Exit and
Legitimacy. Its survey of 2,003 senior decision-makers reports that confidence
in producing evidence runs well ahead of the strongest evidence tier; it also
notes that participating organisations were **not independently audited** and
that its maturity-outcome association is not causal.

IG eHealth Schweiz (*Künstliche Intelligenz in Klinikinformationssystemen*,
October 2026) describes a Swiss regulatory gap for AI in clinical information
systems without a medical intended purpose, and asks for transparency,
auditability, bias management, human oversight and clear responsibility — even
outside medical-device law.

None of these documents describes a product capability. They describe the
vocabulary in which buyers and regulators now ask questions.

---

### 2. The narrower question

A clinical decision made with AI assistance generates a set of questions when
it is later challenged:

- Who was accountable for this decision?
- What did the AI contribute, and under which model version?
- Which evidence was actually available at the time?
- Was a human able to override, and did they?
- Under what connectivity conditions did the AI run?
- Can another party check any of this without trusting our application?

An organisation can answer these questions narratively. The issue is whether
the answers are **bound to the exact record** that was signed, and whether an
independent party can verify them without an account, a vendor portal, or a
reconstruction exercise months later.

This is the level at which a signed decision layer operates.

---

### 3. What the layer binds

A chair-signed Clinical Decision Record (CDR) is produced from a governed
deliberation. It carries, in canonical form and under a content hash:

- the human decision, including adoption, rejection or deferral of AI items;
- per-field evidence excerpts drawn from the admitted evidence universe;
- the chair's signature, over the canonical bytes;
- an AI Bill of Materials (AIBOM) hash, binding the participating models,
  inference parameters and pack version for that session;
- decision traces recording which patterns were retrieved and applied;
- a versioned `connectivity.v1` block naming the declared mode — `air_gapped`
  or `hybrid` — at the time the draft was built;
- contestations and consent state where applicable.

The connectivity block is deliberately narrow. It says that the **application**
declared a mode and refused its own outbound paths in air-gapped mode. It does
not say that the host, the network or an external process made no call.

Every one of these fields is part of the exact bytes the chair signed. Changing
any of them changes the content hash and breaks the signature. Offline
verifiers check the bytes and the signature; they do not judge the decision.

---

### 4. Claim boundary

| The record proves | The record does not prove |
|---|---|
| That these bytes were signed by the enrolled chair key | That the decision was clinically correct |
| That the named evidence hashes were bound into those bytes | That the evidence was true or complete |
| That a particular model composition and pack version were recorded | That the model behaved identically under a swap |
| That a connectivity mode was declared at signing time | That no data left the host |
| That a contestation or override was recorded | That the challenge was correct or resolved justly |
| That the verifier recomputes hashes and signature offline | That an external auditor accredited the system |

This boundary is not a disclaimer added at the end. It is the design
constraint. A system that claims more than its artifacts prove is precisely the
pattern the sovereignty literature warns about.

---

### 5. Why this is not sovereignty washing

We do not claim to provide AI sovereignty.

Domestic capability — national skills, research and institutional capacity — is
a state-level property that no decision-record product can deliver. Strategic
autonomy at the level of a hospital includes infrastructure and procurement
choices that extend far beyond an application flag. Normative self-determination
includes setting ethical and legal conditions for a jurisdiction; we can make
our own governance inspectable, not define the rules.

What we provide is **one narrow instrument**: a signed, portable record of a
governed decision, with honest provenance and explicit non-claims. It can be
used by a hospital that is pursuing broader sovereignty objectives. It does not
substitute for those objectives.

---

### 6. Evidence discipline

A proof-oriented system must publish its failures as well as its controls.

Our kernel determinism check passes across two processes. Our out-of-sample
extractor validation **failed**; we did not relax its criteria. Model-swap
invariance remains unproven, and a later swap result passed only at the
boundary with zero margin in-sample. The controlled reinforcement evaluation is
preregistered but **unrun** because no independent outcome data exists. A
restore drills were attempted twice and **failed** because orphaned
foreign-key rows in the source database blocked restoration; after those
orphans were removed, a third drill restored 119 tables to a scratch database
and was recorded. That is one successful drill, not a cadence. No external
audit opinion, accreditation or ethics approval exists.

These are not footnotes. They are the reason the remaining claim boundary is
credible. A governance layer that reports only successes is a marketing layer.

---

### 7. Implications for clinical leadership

For a medical centre asking "are we sovereign?", this paper offers a different
standing question:

> For the decisions we sign tomorrow, can we produce the exact evidence,
> attribution and conditions under which they were made — without reconstructing
> them from fragmentary logs?

The answer is a record-level discipline: admitted evidence, attributable acts,
signed attestation, version-bound AI composition, declared runtime conditions,
and offline verifiability. That discipline is necessary for any broader
sovereignty strategy. It is not sufficient for one, and we do not present it as
such.

---

### References (external vocabulary, not evidence of capability)

- Guenduez, A. A. & Radu, R., "Decoding AI sovereignty", *Government Information
  Quarterly* 43 (2026), 102193. DOI 10.1016/j.giq.2026.102193.
- IBM, "Proof, Not Promises: The IBM Digital Sovereignty Index", November 2026.
- IG eHealth Schweiz, "Künstliche Intelligenz in Klinikinformationssystemen",
  V1.0, 8 October 2026.
- PersonaVault internal claim boundary: `docs/CLAIM_MATRIX.md`,
  `docs/CONTROL_EFFECTIVENESS.md`, `docs/REGULATORY_POSITION_IG_EHEALTH.md`,
  `docs/IBM_DIGITAL_SOVEREIGNTY_INDEX.md`,
  `docs/AI_SOVEREIGNTY_IN_POLICY_DISCOURSE.md`.

---

*No external assurance, certification, regulatory approval or clinical
validation is claimed by this document.*
