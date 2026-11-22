# Findings log

Confirmed results from public review of the frozen challenge kit. A finding is a verifier result that contradicts the expected outcome in [`README.md`](README.md), a crash, an ambiguous message that misleads a reader, or a documentation mismatch. Reporter credit is given unless the reporter asks otherwise.

| ID | Date | Reporter | Class | Summary | Status |
|---|---|---|---|---|---|
| KIT-001 | 2026-11-22 | Internal review | Documentation mismatch | `benchmark/verify_cdr.py` is an older frozen snapshot that reports `VALID` for `receipt-tampered.json`; it predates the `knowledge_state.entry.content_hash` check. The bundled HTML verifier rejects the tampered receipt correctly. | Documented in `README.md`; no code change to the frozen kit. |

## Classification

- **False accept** — the verifier passes a receipt that should fail.
- **False reject** — the verifier fails a receipt that should pass.
- **Crash** — unhandled exception, hang, or unusable output.
- **Ambiguous message** — output that could lead a careful reader to the wrong conclusion.
- **Documentation mismatch** — behaviour differs from what this kit's README states.

## Resolution conventions

- A finding is confirmed when the reproduction is run by a maintainer against the checksummed files.
- Confirmed findings are assigned an ID and a status: `open`, `documented`, `fixed in new kit version`, or `out of scope` with a reason.
- The frozen kit files are not silently replaced. A fix ships as a new versioned kit directory with new checksums; this directory remains the original challenge target.
