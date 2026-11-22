# Implementation Status — PersonaVault

Last reviewed: 2026-11-22

> This page records what the PersonaVault implementation actually does today.
> It is a separate system from VeriLinkOS: there is no defined interoperation,
> shared trust anchor or cross-verification between them. Where this page
> conflicts with the paper or older material, **this page wins**. All claims
> here are about local implementation, not external certification.

## Verification baseline

- Full implementation suite: **897 passed, 10 skipped, 2 xfailed, 1 xpassed**
  (2026-11-22, private implementation repository).
- Offline CDR verifier parity: browser and standalone verifier agree.
- Challenge kit: **3 files** — `receipt-valid.json`, `receipt-tampered.json`,
  `verify_cdr_standalone.html`. The valid receipt passes all checks; the
  tampered receipt fails. The kit is frozen.

## Shipped capabilities

- **Sequence integrity:** a signed record carries a pre-AI commitment, the
  sealed AI recommendation it relates to, and a chair-authored decision. The
  sign gate refuses a record whose stated commitment withholds its plan.
- **Provenance integrity:** a declared universe of expected evidence, a
  completeness attestation bound at signing, evidence citations on adopted
  items, and a transcript hash bound into the signed decision.
- **Authority integrity:** the chair signs with an enrolled key; consent is
  recorded with a reference kind and status at decision time.
- **Advisory DQI v2 (`dqi.v2`):** consent quality, alternatives considered,
  evidence hierarchy, dissent integration, follow-up commitment and temporal
  integrity. It exists in code and tests as a documentation-quality measure;
  production signing currently freezes `dqi.v1`.
- **Advisory replay calibration:** outcome linkage and counterfactual replay
  reports, which never alter signed receipts or approvals.
- **Offline verifier:** `tools/verify_cdr.py` and the standalone HTML verifier
  run without a network connection, account or platform trust.

## Claim boundaries — read before quoting

- **DQI is not decision correctness.** It scores how well a decision was
  documented. A high DQI does not mean the decision was right, safe or
  clinically appropriate; a conforming record can document a poor decision.
- **Learning and calibration are advisory only.** No outcome, DQI score or
  replay report changes an integrity check, an approval or enforcement.
- **Sequence integrity is not independent cognition.** Cryptography proves a
  commitment was recorded before the AI output and that the record was not
  altered. It cannot prove the human actually formed an independent judgment.
- **This is not a medical device** and does not give clinical advice. It is
  evidence infrastructure for consequential AI-assisted decisions.
- **The offline verifier cannot check the evidence universe.** It can check
  that the declared universe was recorded and attested; it cannot check that
  the declaration was complete or that the right evidence was available.
- **No external certification is claimed.** ARAS covariates, SCITT, W3C DID
  interoperability and any cross-system conformance remain forward-looking.
- **No interoperation with VeriLinkOS is defined or claimed.** The two systems
  are separate repositories with separate evidence models and separate suites.

## Forward-looking only (not present as shipped or Roadmap)

- A Python SDK wrapping the offline CDR verifier for payer/auditor integration.
- A signed, self-contained CDR verification bundle equivalent to VeriLinkOS's
  offline bundle.
- Conformance vectors for the CDR verifier (browser parity tests exist today).
- External audit or accreditation of any kind.
- Validation of clinical outcome correlation — an open empirical question, not
  a property this implementation can establish.
