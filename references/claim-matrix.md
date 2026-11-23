# Claim matrix — what we can say, and what proves it

Every claim below is tied to shipped code and a test. A claim without a proof
is not a claim. Limits are part of the claim, not an afterthought.

## Independent verification

| Claim | Proof | Limit |
|---|---|---|
| A third party can verify a CDR offline: no account, network, database or platform trust | `tools/verify_cdr.py`, `tools/verify_cdr_standalone.html`, `challenge-kit/` (3 files); `tests/test_challenge_kit.py` | Verifies bytes and signatures, not clinical truth |
| A verifier can check the signing key's asserted owner/institution binding from a supplied anchor | `tools/verify_cdr.py --anchor`, browser verifier, `tests/test_signer_anchor_verification.py` | Anchor is published by the issuing installation; receiver must obtain it via a trusted channel. Not an external root of trust or identity proof |
| A one-byte content change fails verification | `receipt-tampered.json` → FAIL at `knowledge_state.entry.content_hash`; `tests/test_challenge_kit.py` | Not replay defense; a receipt cannot prove it wasn't made for a different execution |
| Python and browser verifiers agree | `tests/test_browser_verifier_parity.py`, `tests/test_verifier_import_identity.py`, `tests/test_studio_verifier_sync.py` | Parity covers the shipped checks; new checks need new parity tests |
| A one-page human-readable report can be generated offline | `tools/cdr_report.py`, `tests/test_cdr_report.py`; **Report** button in the Governance Library calls `/receipts/{id}/report` | The report is a view over the verifier, not an additional authority |
| Completeness is attested against a declared universe, with a fail-closed missing-ref check | ADR 0068, `completeness.py`, additive Python/browser verifier checks, `tests/test_completeness_attestation.py` | Relative to the *declared* universe only; not proof of a complete chain across decisions |
| MCP Center is read-only diagnostics, not an action console | `studio/src/pages/MCPCenter.tsx`, `/v2/mcp/integrations`, `/v2/mcp/tool-policy` | Direct tool calls and process provisioning are not exposed in Studio |
| A temporal view is built on an append-only, receipt-backed event ledger | ADR 0066, `governance_events` + writers, `GET /governance/events`, Studio **Governance Calendar**, `tests/test_governance_event_ledger.py` | Historical environments have no backfilled events; drift is deliberately not persisted (ADR 0062) |

## Evidence and adequacy

| Claim | Proof | Limit |
|---|---|---|
| Adequacy gaps are surfaced without changing the integrity verdict | `tools/verify_cdr.py` `audit_adequacy`/`audit_completeness`, ADR 0064, `tests/test_verifier_adequacy.py` | Lexical/structural rules; they flag candidates for human review, not correctness |
| Adopted-item vs operative-order contradictions are detected | `adopted_item_order_conflict` rule; the valid kit receipt flags targeted therapy vs carboplatin | Rule matches a small therapy lexicon, not clinical semantics |
| External evidence is append-only and hash-bound | ADR 0065, `migrations/manual/20261120_external_resource_provenance.sql`, `external_state_hash`, `tests/test_external_resource_provenance.py` | Offline verifier cannot fetch the EHR; unresolved without a trust anchor |
| Intent scope is recorded at intake | `IntakeContext`, `document_attachments`, `source_label`, `role_assigner`, `GET /documents/{id}/provenance`, ADR 0056 | Scope is recorded; full retrieval enforcement is partial (ontology entity branch documented) |
| AI presentation is attested at render time, with derived independence | ADR 0067, `POST /governance/presentation`, `presentation_state` in the signed CDO, additive verifier checks, `tests/test_presentation_state.py` | Proves what was rendered and when, not that it was read or understood; interaction gestures and context-signal source not wired |

## Governance

| Claim | Proof | Limit |
|---|---|---|
| Consent is enforced at case-scoped boundaries, not just attested | `app/api/v2/consent_guard.py`, ADR 0063, `tests/test_consent_enforcement.py` | Environment-level uploads have no subject context and are not gated at upload |
| Consent revocation is governed and attributable | `POST /cases/{id}/consent/supersede`, `prior_consent_id`, `revision`, reason, audit row, `tests/test_consent_supersede.py` | Server-side state, not a portable zero-knowledge proof |
| Amendments never rewrite history | `/amend` with `parent_artifact_id` + `prior_cdo_hash`, fresh chair signature, ADR 0062 | Requires a new signature; the chain is not a transparency log |
| Drift findings are deterministic evidence for review | `drift_scanner.py`, ADR 0062 | Never auto-invalidate a signature; no model call |
| The local companion stays the evidence boundary | `docs/LOCAL_EVIDENCE_BOUNDARY.md`; no file browser, proof-approval button or companion admin in Studio | Proof approval is local-only by design. The browser admits or excludes HITL actions (`/actions`) but cannot sign a CDR or a local proof |
| Tool calls produce signed, decision-bound receipts visible in Studio | ADR 0052, `tool_action_binding.py`, `GET /governance/action-receipts`, Studio **Action Receipts**, `tests/test_tool_action_receipt.py` | Covers successful MCP executions. The HITL queue now has a browser consumer: Studio **Actions** (`ActionsWorkspace.tsx`, `POST /v2/environments/{env}/actions/{id}/approve\|reject`, `tests/test_v2_actions_approval.py`) lets a bound chair admit or exclude each proposal. CDR signing remains local-only |
| Google connections are managed from Profile → Connected accounts with admin-only OAuth | Profile sub-tab, admin OAuth endpoints, audit rows, `tests/test_google_provisioning.py` | Installation-wide token until per-user tokens exist; local CLI is the air-gapped fallback |
| Google OAuth material can be provisioned by an admin without secret echo | `/v2/integrations/google/*`, `tests/test_google_provisioning.py` | Provisioning only — no credentials ship by default; browser OAuth flow and GDocs/send-email actions remain unwired |

## Deployment posture

| Claim | Proof | Limit |
|---|---|---|
| Sovereign deployments fail closed | `resolve_provider()`, `_sovereign_guard()` in `chat.py`; no silent `groq` fallback | Provider selection stays in Model Management |
| The regression suite runs from a clean checkout | `scripts/verify.sh`, `.github/workflows/verify.yml`, `docs/HEALTHCARE/05-operations/testing.md` | CI mirrors the local gate; it is not required for offline verification |
| The shipped kit is frozen and independently checkable | 3 files, zero external references, checksums in `tests/test_challenge_kit.py` | Kit verifier does not include checks added after its freeze |

## Not claimed — deliberately deferred

Replayability/re-execution proofs; receiver attestation and transparency-log
registration; multi-agent delegation and A2A receipts (ADR 0052's tool-action
binding is implemented, but ADR 0049 and the A2A card advertisement are not);
post-quantum signatures; zero-knowledge consent proofs;
cross-jurisdictional certification; a portable `trust_anchor` governance
reference (ADR 0035 design only); any Apple / local-device-agent integration
(see `LOCAL_DEVICE_AGENTS_STRATEGY.md` — strategy only, no code).

Do not use the demo deck or the kit to imply any of these exist.
