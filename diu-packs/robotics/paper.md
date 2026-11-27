# Robotics Intelligence: a governed decision pack for safety events

**Version:** 1.1.0 · **Status:** released pack paper · **Date:** 2026-11-27

## Abstract

Robotics Intelligence is a PersonaVault Domain Intelligence Unit (DIU) that governs how a robotics operation decides when a safety event requires emergency stop, slow-down, review, or no action. The pack declares vocabulary, signals, decision kinds, an evidence perimeter, and a tool perimeter. It does not drive hardware. A simulated gateway now demonstrates the command contract a future signed hardware gateway must satisfy: every actuator command must bind to a signed decision, expire, and fail closed when unbound. The paper states what the pack proves today and what remains before it can be described as a safety system.

## 1. What decision it governs

The pack governs one `robotics_operation` decision: a named operations officer or safety officer records whether an operation may proceed, be slowed, stopped, or escalated after a safety event. The chair's form requires `operation_approval`; it also supports `safety_assessment`, `operational_envelope`, `failover_procedure`, and `incident_notes`. The decision plan projects `operational_envelope` and `failover_procedure` into the signed record.

The claim is about the **decision record**: what event was observed, what standard was considered, what the human authorized, and what action was proposed. It is not a claim about real-time motion control.

## 2. What the pack declares

| Declaration | Content |
|---|---|
| Identity | `robotics`, v1.1.0, `contract_version: 2` |
| Case type | `robotics_operation` |
| UI | Subject: Event; decision: Robotics Decision; principal: Operations Officer |
| Policies | 8 across `safety`, `operations`, `interaction` |
| Signals | 10, including critical safety, hazard, proximity, low trust, energy inefficiency |
| Decision kinds | `emergency_stop`, `slow_down`, `flag_review`, `optimize_route`, `update_profile`, `increase_transparency`, `adjust_tone` |
| Evidence rules | `SafetyEvent` and `UserProfile` require two independent sources with excerpts |
| DQI | `temporal_integrity` weighted 0.25; `knowledge_adequacy` 0.15 |
| Standards | ISO 10218-2, ISO/TS 15066, IEC 61508, ANSI/RIA R15.06 |
| Tool perimeter | Read/review capabilities plus simulated `robotics.status`, `robotics.slow_down`, `robotics.emergency_stop`; motion and envelope changes denied |

The persona is safety-first: safety takes priority over task completion, the AI never overrides an emergency stop, and findings are cited to telemetry, events, standards, or applicable ISO limits.

## 3. What is proven

- **Compilation and contract:** the strict gate reports 0 errors and 0 warnings; the compiled pack carries an Ed25519 signature sidecar.
- **Behaviour:** three conformance vectors call `evaluate_policies()` and assert decision types:
  - critical safety event → `emergency_stop`
  - fire/chemical hazard → `emergency_stop`
  - human proximity → `slow_down`
- **Tool perimeter:** `robotics.status` is allowed without HITL; `robotics.emergency_stop` is allowed but requires HITL; `gmail.send_email` is denied.
- **Simulator:** a local gateway accepts `status`, `slow_down`, and `emergency_stop`; it refuses commands that lack `decision_artifact_id`, `decision_cdo_hash`, and `action_id`; it refuses `replan`, `resume`, and `set_envelope`.
- **State proof:** a bound slow-down changes simulated speed; an emergency stop changes simulated mode to `stopped`.

These are implementation proofs, not safety certification.

## 4. The command contract

A future hardware gateway must honour the same contract the simulator enforces:

```json
{
  "robot_id": "sim-robot-01",
  "decision_artifact_id": "artifact-...",
  "decision_cdo_hash": "...",
  "action_id": "ACT-...",
  "expires_at": "...",
  "speed_mps": 0.2,
  "nonce": "..."
}
```

The binding is what distinguishes an authorized command from an arbitrary instruction. Expiry and nonce prevent replay. A hardware gateway must additionally verify the platform signature, check local interlocks, and return a signed acknowledgement bound back to the decision through an outcome receipt.

## 5. What the pack does not claim

- It does not claim ISO 10218-2, ISO/TS 15066, IEC 61508, or ANSI/RIA R15.06 conformance.
- It is not a safety-rated controller and must not be the sole mechanism that stops motion.
- It does not execute physical commands. The only gateway included is a simulator.
- It does not prove that telemetry is complete, that a hazard was correctly classified, or that a human understood the evidence.
- It does not claim real-time performance. Governance and verification are not a substitute for a safety PLC.

## 6. Reuse for another builder

The reusable pattern is not the robot vocabulary. It is the separation between:

1. a governed decision record with a pre-AI commitment and named human;
2. a declarative policy perimeter that says what may be proposed;
3. a command gateway that fails closed when the signed binding is absent;
4. an outcome receipt that binds execution back to the decision.

That pattern applies to drones, clinical devices, industrial automation, and any domain where an AI proposal must not become an unbound physical action.

## References

- PersonaVault CDR 1.0 specification: `protocols/cdr/v1/specification.md`
- Packs and DIUs: `enterprise/packs-and-dius.md`
- Claim boundaries: `references/claim-boundaries.md`
