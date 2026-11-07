## Task 3: Packaged operation and proof

Files: `pixl/cli.py`, `pixl/service.py`, `pixl/mcp.py`, new
`tests/test_inspection_operations.py`, shared skill references,
new `scripts/inspection_probe.py`, current development docs and TODO.

- [ ] Wire `inspection`, `inspection-prepare`, `inspection-review` and the three MCP equivalents to Task 2; CLI reads closed JSON through `service.read_json`.
- [ ] Add process-level CLI/MCP tests with actual temporary stores and saved evidence.
- [ ] Document exact request/result contracts and the prepare/view/review/continue skill sequence; keep artistic authority and unavailable context explicit.
- [ ] Run the missing-feature fixture through a relocated package, record mechanical success, explicit visual failure, new unperformed candidate and cold report.
- [ ] Run a bounded native host trial against the new instruction identity; preserve the earlier host series untouched.
- [ ] Run Ruff/Mypy and the source-aware full verifier after archiving prior receipts; inspect all skips/failures and preserve failed runs.
- [ ] Perform final independent review, update the MIVIM status from observed proof, and leave the next target explicit.

## Execution ledger

- User authorization: continue the next specified development target; no additional design approval is needed.
- Workspace decision: keep the existing development branch because its accumulated uncommitted milestones are required inputs. Archive before replacing receipts and generated files.
- Design decision: reuse existing X/E/V and ordinary graph bindings; no new wire format or registry extension.
- Verification decision: a local fixture verdict tests retention/publication, while a separate native trial tests instruction use. Neither establishes real provider or engine acceptance.

### Interface preflight

| Tasks | Shared boundary | Check |
| --- | --- | --- |
| 1 / 2 | `render(snapshots, candidate_id, contract, options)` | Byte snapshots enter; relative file bytes, view/input metadata and observations leave. Publication owns IDs/paths/state. |
| 2 / 3 | `prepare`, `review`, `report` | CLI/MCP route the same values and use structured errors. |
| 1 | Rendering and pixel tests | No state, artistic policy or file publication; full/cropped native views retain exact logical pixels. |
| 2 | State/publication tests | Existing semantic closure and commit gates remain authoritative; independent design review checks immutable history. |
| 3 | Packaging and operation proof | Preserve baseline first; archived 145 files before any source/package replacement. |

- Renderer work can begin while the design reviewer finishes the independent
  publication/history checks; that review does not affect pixel transformations.
- Design review resolved: retain original tagged semantic record bodies; validate
  closed manifests and typed projections inside the inspection operation without
  changing generic X semantics; require explicit `source_frame` for contexts.
  Evidence bindings exclude mutable T records. Test amendments as readable drift,
  not corruption, and reject new reviews against stale packets.
