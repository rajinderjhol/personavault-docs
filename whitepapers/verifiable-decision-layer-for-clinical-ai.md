# A Verifiable Decision Layer for Clinical AI

## A whitepaper for academic medical centers operating under the EU AI Act

---

### Abstract

Academic medical centers are deploying AI into consequential clinical decisions faster than they are building the infrastructure to prove what those decisions were, what AI contributed, and who attested to the outcome. The European Union's AI Act makes this gap a legal exposure: deployers of high-risk AI systems must demonstrate logging, transparency, and human oversight. Retrospective reconstruction is inadequate for this requirement, and vendor-supplied logs are not independently verifiable.

This paper describes a class of infrastructure that closes the gap: a cryptographically signed decision receipt that binds the AI provenance, the evidence state, the human deliberation, and the chair's attestation into a single portable object that an independent party can verify without trusting the originating application. The receipt is not a governance dashboard. It is a new clinical record type — the decision, observable in its own right.

The paper is written for the leadership of an academic medical center operating in Switzerland, in the European regulatory perimeter, and with an existing AI strategy that has committed to human-centered deployment. It is not a product pitch. It is an assessment of a capability that does not yet exist as a category, and of the strategic and operational consequences of building it first.

---

### 1. The Problem

Clinical AI has moved from research to deployment. In 2026, an academic medical center is likely to be running at least a handful of AI systems in active clinical use: a pathology classifier, a radiology support tool, a documentation assistant, and one or more language-model-based reasoning tools embedded in decision support. The rate of deployment is increasing.

The governance of these systems has not kept pace. The standard practice today is:

- **Log the model call** in an application-specific log that records input, output, and a timestamp.
- **Document the human decision** in free-text clinical notes.
- **Rely on the vendor** to supply model documentation, versioning, and post-market surveillance.
- **Reconstruct the decision retrospectively** if an audit, an M&M review, or a legal inquiry requires it.

Each of these practices has a structural weakness.

**Application logs are not verifiable.** They are stored by the application that produced them. They can be edited, deleted, or reconstructed after the fact. A regulator, a court, or an auditor cannot check them without trusting the application. Under the AI Act's Article 12, the deployer must retain logs "over the lifetime of the system" — but the article does not specify a form that makes them **independently verifiable**. The result is a record that can be produced on demand but cannot be proven to be unaltered.

**Free-text notes are not comparable.** Two decisions on similar cases will be documented in prose, using different vocabulary, and with different completeness. There is no structured substrate for decision epidemiology, no way to compare decisions across specialists, and no way to ask "how did this institution decide in similar cases."

**Vendor documentation is not neutral.** The model card, the AIBOM, the post-market surveillance report — each is supplied by the party with an interest in the outcome. A hospital that relies on vendor documentation is not building its own evidence base; it is accumulating claims it cannot independently verify.

**Retrospective reconstruction is contaminated.** By the time an audit asks what was known at the moment of a decision, the guidelines have changed, the literature has evolved, and the AI models have been updated. The reconstruction is a guess about a past state, not a record of one.

The consequence is a specific and growing risk. When a clinical decision made with AI assistance is later questioned, the medical center cannot answer, with evidence, the questions that matter:

- What AI system, at what version, contributed to this decision?
- What evidence was available at the moment of decision?
- What did the AI recommend, and what did the human team decide?
- Who attested to the final decision, and to what exact artifact?

The medical center can produce an answer. It cannot produce a **proof**.

---

### 2. The Regulatory Trajectory

The EU AI Act is the regulatory frame that makes this gap urgent rather than merely important.

**Tiered obligations.** The Act classifies AI systems by risk. Clinical decision support with material influence on diagnosis or treatment falls into the **high-risk** category, and the deployer assumes obligations in addition to those of the provider. The relevant articles are:

- **Article 12 — Record-keeping.** High-risk AI systems must technically allow for automatic recording of events over the lifetime of the system. The logs must be sufficient to reconstruct what the system did.

- **Article 13 — Transparency.** Deployers must receive information that allows them to interpret the system's output, including its accuracy, limitations, and appropriate use.

- **Article 14 — Human oversight.** High-risk systems must be designed to allow effective human oversight, including the ability to intervene, override, or halt the system, and to detect automation bias.

- **Article 26 — Deployer obligations.** Deployers must implement human oversight, ensure input data relevance, monitor operations, and retain logs for at least six months.

**Penalties.** Non-compliance with the high-risk obligations attracts administrative fines of up to **€15 million or 3% of global annual turnover**, whichever is higher. Enforcement begins **August 2, 2026**.

**The direction of travel.** The AI Act is being debated for revision under the "AI Omnibus," and some provisions may be softened. But the direction is consistent across jurisdictions: the NIST AI Risk Management Framework, the HL7 AI Transparency effort, and the CHAI guidance all point toward the same requirement — **AI participation in consequential decisions must be documented, traceable, and auditable by parties other than the developer**. A medical center that builds compliance-by-construction is positioned for either regulatory outcome: tightened rules are satisfied, relaxed rules leave the center with a capability competitors lack.

The regulatory case is not "avoid the fine." The regulatory case is that **the infrastructure required to deploy AI responsibly at scale does not yet exist as a clinical standard**, and building it early is a strategic advantage that later becomes a compliance requirement.

---

### 3. The Proposed Infrastructure

The infrastructure described in this paper is a **cryptographically signed decision receipt**. It is not a governance dashboard, not a model card, and not a log aggregator. It is a new clinical record type: an object that records a decision, in the form of a signed, portable, independently verifiable artifact.

The receipt has a specific architecture.

**The Clinical Decision Object (CDO).** Every decision is represented as a canonical, versioned, content-addressable object with the following top-level structure:

- **Case identity** — the subject of the decision, with a pseudonymized patient identifier, the case type, the session, and the chair.
- **Knowledge state** — what could reasonably have been known at the moment of decision: guidelines, literature, pathology, imaging, genomic findings, ontology entities, retrieved passages. Each entry is content-addressed. The composite is hashed.
- **AI provenance** — a graph, not a document. Each node is a model, a prompt, a retrieval set, a tool call, or an external API. Each carries provider, model, version, hash of inputs, hash of outputs. Edges record the causal relationships: which model consumed which retrieval set, which output was consumed by which downstream model.
- **Human deliberation** — the participants, the proposals, the alternatives considered and rejected, the dissent, the rationale, and a link to the transcript.
- **AI recommendation** — what the AI contributed, content-addressed, structurally distinct from the human decision.
- **Human decision** — what the human team decided, content-addressed, with the deciding actor and the timestamp.
- **Attestation** — the chair's Ed25519 signature over the canonical hash of the entire decision state, with the enrolled key identifier and the signature algorithm.
- **Version chain** — the amendment history, with `prior_cdo_hash` linking each version to its predecessor.
- **Integrity** — the CDO's own hashes: the hash of the knowledge state, the AI provenance, the human deliberation, and the composite.

The CDO is the ground truth. Every other artifact — the receipt, the AIBOM, the transcript, the evidence snapshot — is a projection of it.

**The receipt.** The receipt is a signed, self-contained projection of the CDO. It contains the CDO hash, the chair's attestation, the transcript and record bindings, and the verification instructions. A regulator, an auditor, or a legal reviewer sees the receipt. The CDO stays in the system.

**The verification.** The receipt can be exported as a self-contained package and verified **offline, without access to the originating application**. A small verifier — a standalone script with no dependencies on the medical center's systems — recomputes every hash and checks the chair's signature against the enrolled public key. The output is `VALID` or the specific failure.

The critical property is this: **the verification does not require trust in the medical center, the vendor, or any party in the chain**. It requires only the mathematical properties of the content hashes and the Ed25519 signature.

---

### 4. Why This Is Not Just Another Log

The natural objection is that this is a sophisticated logging system with a cryptographic wrapper. The objection is fair, and the answer is that the difference is structural, not cosmetic.

**A log records events. The receipt records a decision state.** An event log records that a model was called, at a timestamp, with an input. It does not record what the model contributed to the decision, what the human team saw, what they considered, or what they chose. The receipt records all of this, and it binds them into a single object whose hash is signed by the accountable human.

**A log is verifiable only if you trust the log store. The receipt is verifiable by anyone.** The content-addressing means that a single byte changed anywhere in the CDO changes its hash, and the signature over that hash fails. There is no place for a silent edit to hide.

**A log is an internal artifact. The receipt is a portable object.** It can be handed to a regulator, a court, an insurer, or a collaborating institution without any of them having access to the originating system. This is the property that makes the receipt a decision record rather than a governance artifact.

**A log is retrospective. The receipt is contemporaneous.** It is created at the moment of the decision, with the knowledge state captured as it existed at that moment. Six months later, when the guidelines have changed and the models have been updated, the receipt still records what was true then.

These four properties together are what make the receipt a new record type rather than a better log.

---

### 5. The Returns

The value of the infrastructure is not primarily financial. It is a combination of risk reduction, capability creation, and strategic position. The financial case is real but secondary; the returns that drive an academic medical center's decision are the ones that follow.

**Regulatory risk reduction.** The receipt implements Article 12 logging, Article 13 transparency, and Article 14 human oversight by construction. A medical center that deploys AI systems with receipts produces the compliance evidence as a byproduct of clinical work, not as a separate administrative task. The avoided exposure under Tier 2 of the AI Act is up to €15 million per violation; the practical value is the ability to demonstrate good-faith compliance without assembling it under enforcement pressure.

**A research asset that does not exist today.** Twenty or more tumor boards across every organ system produce decisions every week. Today, these decisions are documented as free text. With receipts, they become structured, anonymized, comparable objects. The result is a decision corpus — not a patient record corpus — that enables research questions the current data cannot answer: how do tumor boards across organ systems make decisions under uncertainty, how does guideline concordance vary by AI participation, how do dissent patterns correlate with subsequent amendments. These are first-mover publication opportunities in a new research area.

**Reduced cognitive burden on clinicians.** Documentation of a decision today requires reconstruction after the fact, usually in free text, often after hours. The receipt captures the decision at the moment it is made. The non-financial return is a reduction in the administrative load on the clinicians whose time is the scarcest resource in the system.

**A feedback loop for AI performance.** The AI provenance graph records which model, at which version, produced which output, and whether the humans accepted or rejected it. Over time this becomes the medical center's own evidence base on AI performance in its own clinical context — not a vendor benchmark, but a growing record of what works and what does not.

**Trust that scales.** Clinicians systematically under-use AI even when it improves accuracy, because the trust equation is wrong: the clinician is asked to trust the model. A signed receipt changes the equation. The clinician is not asked to trust the AI. The clinician is given a verifiable record of what the AI did. Over time, trust in AI shifts from the model to the verification, which is a different kind of trust — one that does not depend on any vendor's claims.

**Strategic positioning.** Academic medical centers compete for talent, for partnerships, and for research funding. A center that has deployed a decision-level trust layer is a more attractive partner for every institution that needs to collaborate on AI-governed clinical decisions. This is the kind of positioning that shows up in funding applications, in annual reports, and in the willingness of external partners to engage.

**Cross-border interoperability.** Basel is a trinational region. The medical center treats patients from France and Germany, and collaborates with institutions across the Rhine. A decision receipt that is portable, verifiable, and interoperable is a natural standard for cross-border clinical collaboration. The institution that defines the format is the institution that shapes the region's clinical AI practice.

---

### 6. What This Paper Is Not Claiming

This paper is not claiming that the receipt makes the AI better. It records what the AI did; it does not improve the AI.

This paper is not claiming that the receipt replaces clinical judgment. It makes judgment provable, not automated.

This paper is not claiming that the receipt eliminates regulatory risk. It provides the evidentiary infrastructure that reduces the probability and severity of enforcement, and makes good-faith compliance demonstrable.

This paper is not claiming that the infrastructure is finished. It is a proven cryptographic kernel with a defined roadmap. The receipt's core — the signed hash binding the AI provenance, the human decision, and the chair's attestation — is built and tested. The completion of the receipt to the full CDO specification is a bounded engineering effort.

This paper is not claiming a category that already exists. Every competitor in the AI governance space records AI inference. None produces a multi-stakeholder clinical decision receipt. The category this paper describes is unclaimed.

---

### 7. The Question This Paper Leaves with the Reader

The question is not whether a medical center should deploy AI into clinical decisions. That decision has been made, and it is being executed at increasing speed. The question is whether the medical center will have, when the first consequential question is asked about a decision made with AI assistance, the infrastructure to answer it with evidence rather than with reconstruction.

The AI Act's enforcement begins in August 2026. The first serious audit of an AI-assisted clinical decision will occur after that date. The medical center that has already deployed a decision receipt infrastructure will answer that audit with a signed artifact. The medical center that has not will answer it with a reconstruction, and will hope that the reconstruction is accepted.

The infrastructure described in this paper is not a purchase. It is a category. It is the decision layer that sits between the AI systems a medical center deploys and the accountability that the medical center owes to its patients, its regulators, and itself.

The question is whether to build it, or to wait until someone else does.

---

### A note on the current state

The cryptographic kernel of the infrastructure described here — the Ed25519 chair attestation over a canonical decision hash, the transcript binding, the chain verification — is built and tested. It produces a signed receipt with all eight identifiers bound, verifiable by a chain-checking endpoint. The composite test walks the full chain: case creation, deliberation, chat turn, transcript production, record submission, chair signature, and chain verification.

What remains is the completion of the CDO to its full specification — the knowledge state, the full AI provenance graph, the alternatives and dissent as structured fields, the amendment workflow, and the portable export with the offline verifier. These are six defined items, each small enough to be a single engineering cycle. When they are complete, the receipt becomes a portable, independently verifiable clinical decision object, and the category this paper describes becomes real.

Until then, the paper describes a direction and a demonstrated capability, not a finished product. The direction is the one the regulatory environment is already moving toward. The capability is the piece that does not yet exist as a standard, and that a medical center can be first to build.

