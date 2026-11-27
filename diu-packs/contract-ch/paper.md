# Contract Intelligence — Swiss Law: a governed decision pack for Swiss contract review

**Version:** 1.1.0 · **Status:** released pack paper · **Date:** 2026-11-27

## Abstract

Contract Intelligence — Swiss Law is a PersonaVault Domain Intelligence Unit (DIU) that governs how a Swiss contract review decides what to accept, reject, qualify, or escalate. The pack declares a Swiss legal vocabulary, an engagement-letter authority basis, a decision plan for Swiss-law compliance, and a tool perimeter that permits drafting and scheduling but denies outbound notification. It is strict-v2, signed, and accompanied by behavioural conformance vectors that prove its stated grounds and authority rules fire. The paper states what the pack proves today and what it explicitly does not claim: it does not determine legal correctness, provide legal advice, or establish court admissibility.

## 1. What decision it governs

The pack governs one `swiss_contract_review` decision. A named chair reviews clauses such as `Gerichtsstand`, `Rechtswahl`, `Schiedsklausel`, liability caps, nDSG terms, and CISG exclusion. The chair's form requires a `recommendation`; it also supports `grounds`, `rule_version`, `client_authority`, `risk_assessment`, and a nested `swiss_compliance` block with jurisdiction, governing law, arbitration clause, and CISG exclusion. The decision plan projects `swiss_compliance` into the signed record.

The consent floor is the client engagement letter (`Anwaltsvollmacht / Mandatsvereinbarung`), and the authority reference kind is `engagement_letter`. The pack therefore records *under what mandate* a legal decision was made, not merely that a model produced text.

## 2. What the pack declares

| Declaration | Content |
|---|---|
| Identity | `contract-ch`, v1.1.0, `contract_version: 2` |
| Case type | `swiss_contract_review` |
| UI | Subject: Contract; decision: Matter Decision; principal: Signatory |
| Policies | Swiss-law and jurisdiction policies, plus governance rules for stated grounds, named decision maker, rule version, and client authority |
| Signals | Swiss clause detection, OR provisions, nDSG, CISG, and governance-missing signals |
| Decision kinds | `risk_flag`, `clause_recommendation`, `deviation_warning`, `mandatory_provision_violation`, `referral`, `escalation` |
| Evidence rules | Clause evidence requires excerpts and independent sources |
| Sources | OR, ZGB, nDSG, CISG, Swiss Federal Court decisions |
| Tool perimeter | `vault_search`, `recall_patterns`, `gcal.create_event`, `gmail.create_draft`; denies `gmail.send_email`, `twilio.send_sms` |
| Actions | Draft a response, schedule a review meeting |
| Compliance frameworks | Swiss FADP/nDSG, Swiss OR, UN CISG |

The strict contract version means the compiler holds the pack to the contract gate: real capabilities only, no dead fields, and block decisions paired with block actions.

## 3. What is proven

- **Compilation and contract:** strict gate reports 0 errors and 0 warnings; the compiled pack carries an Ed25519 signature sidecar.
- **Behaviour:** conformance vectors call `evaluate_policies()` and assert that:
  - a clean Swiss review with grounds, authority, and rule version does not fire the governance blocks;
  - a decision with missing grounds, named decision maker, rule version, and client authority fires all four governance blocks.
- **Record path:** a seeded Swiss matter produces a CDR carrying a pre-AI commitment, hash-bound case documents, AI provenance, a named chair signature, engagement-letter authority, and the projected `swiss_compliance` plan.
- **Offline verification:** the exported CDR verifies with `DECISION INTEGRITY: VALID`; a one-field tampered copy fails at the CDO hash.
- **Retrieval accounting:** in the seeded matter, two case documents are available and two are retrieved, giving a real `knowledge_adequacy` component rather than a hardcoded value.

These are implementation proofs. They show integrity, sequence, and authority binding; they do not show that the contract analysis was legally correct.

## 4. What the pack does not claim

- It does not give legal advice or determine the validity of a clause.
- It does not establish that any court, regulator, or client must accept the receipt.
- It does not prove that the declared Swiss sources were complete; `retrieved_count` reports what the system actually consulted.
- It does not prove that the chair understood the evidence or that the AI's reasoning was sound.
- It does not send.email or messages; outbound notification capabilities are denied.
- It does not claim nDSG, OR, or CISG compliance certification. The frameworks are declarations for evidence mapping, not legal conclusions.

The `connectivity.not_claimed` block in the CDR states the same boundary in the record: an application-level mode is not a firewall guarantee.

## 5. Reuse for another builder

The reusable pattern is a **jurisdiction overlay on a generic decision substrate**. The substrate owns sequence, evidence hashing, signing, and verification. The pack owns:

1. the vocabulary of the domain;
2. the required fields of the human decision;
3. the policy perimeter;
4. the authority artifact;
5. the action perimeter;
6. the standards that the receipt can cite.

A builder in another jurisdiction can replace the legal vocabulary and authority source without changing the verifier. That is the point of the pack boundary: the same receipt mechanism can serve many professions while the meaning stays local.

## References

- CDR 1.0 specification: `protocols/cdr/v1/specification.md`
- Packs and DIUs: `enterprise/packs-and-dius.md`
- Claim boundaries: `references/claim-boundaries.md`
- Conformance approach: `enterprise/conformance.md`
