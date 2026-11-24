# The Horizontal Claim — What the CDR Proves and What It Does Not

> **Verified against code at commit `36313fe` (2026-10-25).**
> This is the document to show a compliance officer, a researcher,
> or a partner who asks "why should I believe the horizontal claim?"
> It states what the product is, what it proves, what it does not
> prove, and what is not yet built.

---

## The claim, in one sentence

**A decision can be recorded in a form that any third party can
verify offline, that survives the platform, that names the human
and the AI, and that can be queried across a population.**

That is the leapfrog. It is not a feature. Every competitor sells
"authorization and containment" — the agent was allowed to act,
here is the log. This product sells "verifiable judgment" — the
decision was made by this person, with this evidence, and here is
the artifact that proves it.

---

## What the CDR proves

A Clinical Decision Receipt (CDR) is a JSON file produced by a
signed deliberation. The verifier (`tools/verify_cdr.py`, 322
lines, offline, depends only on `cryptography` and `json`)
performs ten checks:

1. **Schema version** — the record is `cdr.v1`, the payload is `cdo.v1`
2. **CDO hash** — the canonical hash of the CDO payload matches
   the recorded hash
3. **Attestation signed payload hash** — matches the CDO hash
4. **Ed25519 signature** — the chair's signature verifies against
   the embedded public key
5. **Transcript hash** — the transcript's canonical hash matches
   its recorded hash
6. **Transcript binding** — the transcript's hash equals the CDO's
   `human_deliberation.transcript_hash`
7. **Record hash** — the record's canonical hash matches its
   recorded hash (and, since `36313fe`, the record's `payload`
   matches its `payload_canonical`)
8. **Version chain** — the version is consistent with its
   `prior_cdo_hash` (null for v1)
9. **Attestation timestamp** — `attestation.attested_at` is
   present and >= `human_decision.decided_at` (ADR 0029)
10. **AI provenance graph** — if `ai_provenance` is present, the
    graph is well-formed

**Verified AI-provenance fields (2026-10-26).** A signed
record produced after the fix carries:

- `metadata.model_id` — the runtime model (`qwen2.5:1.5b`)
- `metadata.provider` — the runtime provider (`ollama`)
- `ai_provenance.nodes[0].model` — same model, on the graph
- `ai_provenance.nodes[0].provider` — same provider
- `ai_provenance.nodes[0].output_hash` — SHA-256 of the
  model's full response (64 hex chars)
- `ai_provenance.nodes[0].prompt_chars` and
  `completion_chars` — the sizes of the prompt and answer

Verified on `artifact-7b9fe0ace90e` (session
`delib-abbfc3c7b2c3`, 2026-10-26). The fields are present on
the artifact and covered by the chair's Ed25519 signature.

**The AI's free-text answer is not in `ai_recommendation.content`.**
It lives in the deliberation transcript, bound by
`transcript_hash`. `ai_recommendation.content` carries the
pack's formal verdict (decision type, severity, confidence).
Both are on the record; they answer different questions.


**The verifier returns exit 0 if all ten pass, exit 1 otherwise.**
The current record `rcpt-c8f950d1f3bf8c9f` passes all ten. The
5-case tamper regression (signature flip, CDO hash zero,
attested_at null, payload mutation, payload_canonical mutation)
all correctly return exit 1.

**This is proven, not asserted.** The verifier is 322 lines. A
second party can read it in an hour and run it in a second.

---

## What the CDR does not prove

The proposal document (22 October) already states this. Repeating
it here because it is the correct discipline:

> "A valid signature establishes that the signed payload has not
> changed relative to the signature and that the signature
> validates under the public key used for verification. It does
> not, by itself, establish the signer's real-world identity, the
> authenticity of the clinical facts, the completeness of the
> record, or the security of the originating system."

The CDR does **not** prove:

1. **Clinical correctness.** Whether the decision was medically
   right. The CDR is a process record, not a quality judgment.
2. **Signer identity.** That the public key belongs to the named
   chair. Key enrollment and revocation are a separate trust
   question. The CDR records the key; it does not vouch for it.
3. **Execution.** That the treatment was administered, the
   contract was signed, the policy was issued, the robot
   performed the action. This is ADR 0030's execution-evidence
   gap. A separate verifier (`tools/verify_execution_evidence.py`)
   now exists and checks a signed artifact from an independent
   performer, bound to the decision by hash. The CDR itself still
   proves *attested*, not *executed*.
4. **Completeness.** That every relevant piece of evidence was
   seen by the board. The CDR records what was referenced; it
   does not guarantee that nothing was missed.
5. **Automation bias prevention.** That the board critically
   evaluated the AI's recommendation. The proposal states this
   explicitly in Section 3.

6. **Divergence between the AI and the human decision, or between
   an action and its delegated authority.** The CDR carries the AI's
   free-text answer in the transcript and the human decision in
   `human_decision.content`. It does not carry a computed field
   saying whether the human agreed with, overrode, or partially
   accepted the AI's recommendation. It also does not distinguish
   "the chair accepted the AI's recommendation" from "the chair
   made the decision and the AI happened to agree" — a failure
   mode called *authority laundering*. The divergence primitive is
   under design; three candidate schemas (single field, typed
   family, per-pack) are under consideration. See
   `CHAMPION_READINESS.md` Q2 for the decision and the failure-mode
   analysis.

**The discipline is: state the boundary before the audience finds
it.** A compliance officer trusts a vendor who volunteers the
limitation. A vendor who claims "we prove everything" is
dismissed.

---

## Why this is horizontal

The five entities the CDR depends on are not clinical:

- **Subject** — patient, contract, matter, policy, robot
- **Case** — a bundle for deliberation
- **Session** — the deliberation event
- **Decision** — the signed artifact
- **Principal** — the human actor

None of them is domain-specific. The **vocabulary** that labels them
is domain-specific, and it lives in the DIU pack:

```yaml
# clinical
subject_label: "Patient"
decision_label: "Tumor board decision"
principal_label: "Board member"

# legal
subject_label: "Matter"
decision_label: "Contract review decision"
principal_label: "Reviewer"

# insurance
subject_label: "Policy"
decision_label: "Underwriting decision"
principal_label: "Underwriter"
The same page renders a patient's decision history and a
matter's decision history, with different labels. That is the
horizontal claim.

What the horizontal claim requires that is not yet built
The data model is horizontal. The product surface is not yet.

Missing surface (one week of work):

Subjects page — the subject registry is a field inside
CaseDetail.tsx. There is no list, no detail, no identity
vault view. Requires 1 day of backend + 1 day of frontend.

Principals page — the principal registry is inside
EnvironmentAdmin.tsx. There is no first-class page for "who
is on my board, and are their signing keys enrolled?"
Frontend-only. One day.

`decision_chain_schema` in `pack.yaml` — the schema block that
carries the chain key and relations (ADR 0058). This supersedes the
earlier `longitudinal_view_vocab` proposal, which was never in the
schema.

Shipped instead of `SubjectLongitudinalView`: `SubjectDetail.tsx`
now has a **Chain** tab that renders each signed decision sequence
with its predecessor hashes and relation labels, plus an offline
bundle export. In-browser verification of the bundle is still not
built — `tools/verify_decision_chain.py` does it offline.

Patterns page — the learning loop made visible. The
semantic_patterns table has 2 ice, 1 liquid, and 2
transitions. No page shows them.

verify_execution_evidence.py — ADR 0030's second
verifier. Exists as a standalone offline tool for a separate
artifact. The CDR alone still proves attested, not executed.

Missing from the product entirely:

Multi-pack demonstration — one subject, one trajectory,
rendered across three packs. The data model supports it. No
demo exists.

The record's `metadata.packs` is the session's governing set; the environment's installed list is separate, and the record's `packs` is not it. The page renders the set.

---

## Since this snapshot (2026-10-25 → 2026-11-03)

Three of the "missing surface" items shipped since the verification
at `36313fe`:

- **The Subjects page.** `studio/src/pages/Subjects.tsx` (the list)
  and `SubjectDetail.tsx` (the detail, 2026-10-28). The subject
  registry is no longer a field inside `CaseDetail.tsx`; it is a
  first-class page.
- **The Principals page.** `studio/src/pages/Principals.tsx` — the
  environment's actors and their signing keys.
- **The Patterns section.** `LearningWorkspace.tsx` renders the
  learning loop's patterns.

Still missing, as of this note:

- In-browser chain verification — the bundle verifier is offline CLI
  only; `SubjectDetail`'s Chain tab exports a bundle instead.
- `longitudinal_view_vocab` — never existed; `decision_chain_schema`
  (ADR 0058) is the pack-declared block for decision continuity.
- `verify_execution_evidence.py` — ADR 0030's second verifier.
- The multi-pack demonstration — one subject, one trajectory,
  rendered across three packs.

The snapshot above is the record of 2026-10-25. This section is the
record of what has changed. The horizontal claim's data model was
always complete; the product surface is the gap, and the gap is
smaller than the snapshot says.

---

What to show a compliance officer
30 minutes, three artifacts:

A signed CDR, verified offline in front of them.
python3 tools/verify_cdr.py receipt.cdr.json. Exit 0. Then
mutate one byte, run again, exit 1. Two commands. That is the
demonstration.

The one-page "What a CDR proves and does not prove." The
same discipline as the proposal's Section 2 and 3, at a
glance. This document, condensed to one page.

The compliance mapping table. Six rows: nDSG, FMH/SAMW,
EU AI Act (Art. 12, 14, 15), FDA/EMA. For each: the regime
requirement, the CDR field that satisfies it, the verification
method. Nothing more.

Do not bring: a pitch deck, an architecture diagram, a
competitive landscape. The compliance officer does not need those.

What to show a researcher
30 minutes, one artifact:

A SubjectLongitudinalView — one subject (patient, matter,
policy), all decisions in order, each with:

What the AI recommended

What the human decided

Where they diverged (the interesting case)

The DQI (stable, signed at decision time)

The receipt (one click to download, one click to verify)

The outcome (if linked)

And then swap the pack. Same page. Different vocabulary. The
subject becomes a contract. The decisions become contract reviews.
The AI recommendation becomes a clause extraction. The pattern
feedback becomes "OR Art. 100 redlines reinforced."

That is the horizontal claim in code. It does not exist yet.
It is the highest-value page to build after the two entity pages.

What this document is not
It is not a promise that the horizontal claim is fully realized.
It is a statement that:

The data model is horizontal

The CDR proves what it claims

Two of five entities have no UI surface

The execution-evidence chain is built but needs an independent performer to record evidence

The multi-pack demonstration is not yet a page

A vendor who says "we have it all" is dismissed. A vendor who
says "here is exactly what we have, and here is exactly what we
do not" is taken seriously. This document is the second kind.

References
ADR 0028 — canonical serialization for signing

ADR 0029 — attestation timestamps

ADR 0030 — the execution-evidence gap (artifact and verifier shipped; client recording flow pending)

docs/BACKEND_WIRING_PLAN.md — the live wiring state

docs/HEALTHCARE/02-architecture/the-verification-protocol.md —
the verifier spec, reconciled with the code at 36313fe

tools/verify_cdr.py — the verifier, 322 lines, offline

docs/HEALTHCARE/06-decisions/0028-0030 — the three most recent
ADRs
