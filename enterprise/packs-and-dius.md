# Packs and Domain Intelligence Units

One substrate, many regulated domains. PersonaVault's data model — subject, case, session, decision, principal — is domain-independent. The **pack** supplies the vocabulary, the form, the decision kinds, the evidence sources, and the AI's action perimeter for a specific domain. The substrate stores the decision; the pack decides what the decision means to the people using it.

This document describes what ships today. For the theory of why the receipt is portable, see [Beyond AI Audit Trails](../academic/three-foundations/paper.md).

## The pack catalogue

Fifteen packs declare a `pack.yaml` and compile successfully. They are organised by the work they govern:

| Domain | Packs |
|---|---|
| Clinical | `oncology-tumor-board-governance`, `molecular-tumor-board-governance`, `infection-control-governance`, `ethics-committee-governance` |
| Legal | `contract`, `contract-ch`, `contract-eu` |
| Risk and compliance | `compliance`, `insurance`, `security`, `procurement`, `swiss-tax-advisory`, `robotics` |
| Employment and education | `employment-governance`, `education-governance` |

The last two target the Annex III high-risk categories that take effect on
**2 December 2027** under the EU AI Act as amended by Regulation (EU)
2026/1744 (employment, workers management, and education). They are governed
record packs, **not** conformity assessments, certifications or legal advice.
See the [third-party audit path](third-party-audit-path.md) for what a buyer
can independently verify.

A pack changes the entire working environment: the sidebar's decision and receipt labels, the chair's form, the AI's proposal kinds, and the weights used by the decision-quality index. Switching packs switches the vocabulary, not the underlying record.

## What a pack declares

The manifest has sixteen top-level keys, enforced at load time:

| Key | Purpose |
|---|---|
| `pack` | Identity: id, name, version, domain, description |
| `ui` | Seven labels per domain, including `subject_label` and `decision_label` |
| `case_types` | The case types the pack governs |
| `subject_spec` | The data source declaration (FHIR, openEHR, or empty) |
| `human_decision_schema` | The chair's form fields, including which are required |
| `dqi_weights` | Six weights summing to 1.0 |
| `intent_prompts` | Four prompts in the domain's language |
| `proposal_item_schema` | The AI's permitted proposal kinds |
| `knowledge_sources` | Guideline or regulation corpus declarations |
| `detection` | Primary, secondary, and negative keywords |
| `persona` | Identity, tone, constraints, citation format |
| `compliance` | Frameworks the domain's decisions touch |
| `tools` | Allowed and denied tools — the action perimeter |
| `belief` | Verification rules and contradiction detection |
| `autonomy` | Autonomy level and escalation rules |
| `metadata` | Author, homepage, license |
| `actions` | Decision options the AI may offer: description, capability, confidence (optional boost), linked policy ids |

A pack directory contains `pack.yaml`, `extraction/` (entity schema and signals), `policies/`, `persona/`, and a compiler-generated `compiled/` directory holding the Python module and manifest.

## Subject vocabulary

The model field is always `subject_id` / `subject_type`. The pack chooses the label. Examples that ship:

| Pack label | Domain |
|---|---|
| Patient | Clinical tumor board |
| Matter / Contract | Legal review |
| Account / Policy | Insurance, tax advisory |
| Supplier | Procurement |
| Case / Incident / Event | Compliance, security, robotics |
| Employment matter | Employment governance |
| Student matter | Education governance |

The sign guard reads the pack's `human_decision_schema` and refuses to sign unless the pack declares at least one required field and the chair has populated it. Verifier requirements are likewise pack-declared: a check can be mandatory for one pack and optional for another. This prevents a generic "signed blob" from counting as a domain decision.

## Authoring and compilation

- **Compiler page** at `/compiler`: nine tabs, four authoring, three inspection, two runtime. The Record tab shows the provenance chain `source_checksum → pack_hash → compiled_hash`.
- **Save endpoint** `POST /compiler/save/{pack_id}` validates the merged manifest — pack plus extraction and policies — before an atomic write.
- **CLI** `scripts/compile_packs.py` for pipeline use.
- **Pack signing**: when `PACK_SIGNING_KEY` is configured, compilation writes a `<pack>_SIGNATURE` sidecar containing an Ed25519 signature over `pack_hash` with a stable signer key id. Verify offline with `python3 tools/verify_pack.py packs/<id>/compiled/<id>_pack.py`. Without a key, compilation succeeds but the pack is honestly unsigned; there is no ephemeral fallback key.

## What makes the employment and education packs governed

Each of the two Annex III packs declares, beyond vocabulary and form:

- **16 policies**, including block rules for decisions with no stated reason,
  no named decision maker, no rubric/policy version, and automated adverse
  actions;
- a **tool perimeter** denying consequential write and notification actions
  (for example `ams.reject_candidate`, `sis.write_grade`, and email/SMS sends);
- **evidence rules** requiring an excerpt for every recorded entity;
- an **appeal route and deadline** field in the chair's decision schema;
- an explicit **legal consent basis** and four escalation rules.

These are pack declarations enforced by the substrate's sign gate and HTTP
tool perimeter. They are what separates a governed pack from a scaffold that
merely compiles. A minimal manifest with identity, keywords and persona
validates in milliseconds; it would have none of the above.

Both packs declare `contract_version: 2`, which makes the compiler hold them
to a **pack contract** in addition to schema validation: every allowed tool
must have a real implementation, declared governance fields must be ones the
runtime actually reads, block policies must carry a block action, and DQI
weights must sum to 1. Older packs are reported as warnings rather than build
failures. A pack's `actions:` section declares the decision options the AI may
offer; each must resolve to a real capability, and the router reads them
directly — adding a pack requires no application code change. Run
`python scripts/check_packs.py --strict` in the implementation
repository to see the catalogue's declaration status — several legacy packs
still declare tools that have no handler.

Both packs compiled **unsigned** in development because no `PACK_SIGNING_KEY`
was configured. Compilation without a key succeeds and is reported honestly;
no ephemeral fallback key is generated.

## Marketplace — what it actually is

`/marketplace` is a card list backed by `GET /v2/dius`. Each card shows the pack's name, domain, version, description, policy/signal/entity counts, its vocabulary labels, and its compliance frameworks. A domain filter narrows the list. Installing a pack writes a `PackInstallation` row via `POST /v2/dius/{id}/install`; uninstalling deletes it.

**There is no upload endpoint, no package registry, no reviews, and no usage statistics.** A `MarketplaceRegistry` with reviews and statistics was designed and never built. Do not infer a marketplace ecosystem from the word "Marketplace" in the UI.

## Boundaries today

- Cross-pack composition — one pack referencing another pack's knowledge sources — is deferred.
- The OAuth flow for pack dependencies is deferred.
- The Basic/Advanced toggle on the compiler page is deferred.
- The marketplace has no third-party publishing path; packs are authored on the filesystem, compiled, then installed.

## Evidence

Pack behaviour is covered by `tests/test_pack_manifest.py`, `test_pack_signing.py`, `test_case_packs.py`, `test_subject_packs.py`, `test_session_pack_set.py`, `test_seed_pack_reaches_record.py`, `test_seed_resolves_pack_from_diu.py`, `test_diu_domain_filter.py`, `test_subject_spec_from_pack.py`, `test_subject_type_from_pack.py`, `test_deliberation_by_pack.py`, and `test_legaltech_signs.py` (which proves the sign guard works for a non-clinical pack).
