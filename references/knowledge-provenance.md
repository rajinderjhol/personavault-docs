# Knowledge Provenance Graph

> **Status:** implemented in the private implementation repository as a
> **read-only logical projection** over existing authoritative records. This
> page describes what it answers and what it does not claim. It is not a new
> database, a second source of truth, or a certification.

## The question it answers

> "Show me exactly how this AI system acquired this piece of knowledge, why it
> considers it valid, who authorized its progression, and what evidence
> supports its current status."

An auditor or administrator can open the graph for an environment and follow
one belief from its originating decision to its current state, including
every weight change, correction and maturity transition.

## Node and edge vocabulary

Nodes: `pattern`, `decision_trace`, `artifact`, `reinforcement`,
`transition`, `proposal`, `execution_evidence`. Every node carries an
`authoritative_ref` — the table and row id of the record it came from — and a
`trust_status` read from that record (`unvalidated`, `validated`,
`contradicted`, `signed`, `verified`, `structural`, and so on).

Edges: `DERIVED_FROM`, `ATTESTED_BY`, `MUTATED_BY`, `MATURED_BY`,
`PROPOSED_FOR`, `COMPENSATES`, `EXECUTED_AS`. Edges derive from foreign keys,
existing `fact_edges` rows, or explicit compensation pointers. They are never
invented correlations.

## Boundaries

- **Read-only.** The projection writes nothing; the source rows remain the
  only mutable knowledge.
- **Structural phase is not empirical validation.** A pattern at `ice` may
  still be `unvalidated`. See the
  [claim boundaries](claim-boundaries.md) and the
  [third-party audit path](../enterprise/third-party-audit-path.md).
- **`validated` is not clinically correct.** It means an outcome receipt
  attested a result; it is not independent proof of correctness.
- **Completeness is bounded.** An edge absent from the projection may exist
  in the authoritative records outside the requested filter or limit. The
  projection is a view, not a total inventory.
- Determinism is hash-bound: a manifest hash covers the sorted node ids and
  edge hashes, so two runs over unchanged data produce the same result.

## Inspecting it

In the implementation repository:

```sh
curl -H "Cookie: session_id=..." \
  'http://localhost:8000/v2/environments/{env}/governance/knowledge-provenance'
```

Optional filters: `pattern_id`, `artifact_id`, `limit`.

On a development environment the graph shows patterns, decision traces,
artifacts and maturity transitions, with patterns honestly marked
`unvalidated`. Reinforcement and execution-evidence nodes appear only once
those events have actually been recorded in that environment.
