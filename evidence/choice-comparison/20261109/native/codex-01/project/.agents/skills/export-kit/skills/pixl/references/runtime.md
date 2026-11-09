# Runtime and tool boundaries

Read the bundled specification before producing UDL. The runtime's actual CLI help and MCP `tools/list` responses define callable arguments. Resolve `../../../scripts/pixl.py` relative to this reference directory, then invoke it with Python 3.11+ from the user's project directory. The selected Python environment also needs Pillow 10+ and jsonschema 4.18+. Use a project virtual environment; install the source package with `python -m pip install -e .` from the source checkout, or install the bundle's `../../../requirements.txt` with `python -m pip install -r "<resolved requirements path>"` in the destination environment. The plugin includes PIXL's own runtime source, not a Python interpreter or third-party packages.

| Operation | CLI form | What it establishes |
| --- | --- | --- |
| Validate | `validate FILE --root ROOT` | The implemented syntax, schema, and reference checks |
| Focus context | `context FILE FOCUS --budget BYTES` | Dependency closure within a strict byte budget; bytes are not model tokens |
| Authoring context | `context STATE TASK_OR_OUTPUT_OR_PLAN --view authoring --root ROOT [--plar PATH --asset ID]` | Current planning index, exact criteria and source retrieval links; no history expansion or acceptance |
| Ready work | `ready FILE` | State-level readiness according to declared prerequisites |
| Change impact | `impact FILE ID` | Declared relationships affected by a proposed change |
| Commit candidate | `commit STORE CANDIDATE --expect SHA256 --root ROOT` | Validated state replacement if the current canonical hash matches |
| New intake | `intake STORE --name NAME --brief TEXT --root ROOT` | PX2 project with no invented style, ready for explicit intake choices |
| Workflow status | `workflow FILE --root ROOT` | PX2 choices, planned outputs, candidate criteria, failed/unavailable checks and local blockers |
| Family status | `family FILE [OUTPUT] --root ROOT` | Verified retained files, exact baseline/member selection, destination requirements, pending jobs and snapshot drift; no state change |
| Retain delivery | `family-snapshot STORE OUTPUT CANDIDATE --expect HASH [--root ROOT]` | Copied member bytes and manifest published as an unaccepted candidate; no nomination, verdict, task completion or remote action |
| Legacy new state | `init STORE --name NAME --root ROOT` | PX1 compatibility initializer; its scaffold style defaults remain unconfirmed |
| Decode adapter | `decode FILE` | Tagged JSON interchange for inspecting or editing UDL through tools |
| Encode candidate | `encode ADAPTER_JSON --out FILE` | UDL bytes from the tagged interchange form; validate before commit |
| Source catalog | `catalog ROOT --out FILE` | A local source catalog, not remote tool availability |
| Supplied source revisions | `sources [--root ROOT]` | Declared source identities verified against local bytes; defaults to installed knowledge resources |
| Source slice | `source FILE --expect SHA256 --start N --end N --budget BYTES` | Exact source lines from hash-verified bytes, without silent truncation |
| Art knowledge | `knowledge [METHOD_ID]` | Small method index, or the full source-grounded selected method |
| PixelLab catalog | `capabilities [TOOL_NAME]` | Small dated tool index, or one tool's documented parameters |
| Save provider intent | `job-prepare STORE JOB TASK REQUEST_JSON --outputs OUTPUT ... --expect HASH --root ROOT` | Exact request, observed schema, authorization evidence and plan binding persisted before dispatch |
| Claim dispatch | `job-dispatch STORE JOB --expect HASH --root ROOT` | One local claim, saved as unknown before returning the request for the host call |
| Save observation | `job-observe STORE JOB STATE EVIDENCE_JSON --remote-id ID --expect HASH --root ROOT` | One retained caller-supplied observation; no submission or polling |
| Import candidate | `job-import STORE JOB OUTPUT CANDIDATE PATH EVIDENCE_JSON --expect HASH --root ROOT` | Retained local byte snapshot linked to F and J; no automatic acceptance |
| Recover jobs | `jobs FILE --root ROOT` | Exact saved requests, histories, drift and next actions; never a fresh dispatch grant |
| Legacy prepare | `prepare TOOL ARGUMENTS_JSON --schema INPUT_SCHEMA_JSON` | Stateless local request validation; no saved project intent |
| Legacy observe | `job JOURNAL_JSON STATE --remote-id ID --evidence RECEIPT_JSON` | Stateless returned journal; no checked project publication |
| Method proofs | `poc --out DIRECTORY` | Executed bounded reference checks and artifact hashes |
| Image constraints | `asset-check IMAGE --width W --height H --palette HEX ...` | Implemented local image checks; palette is optional |
| Inspection status | `inspection STATE [PACKET] --root ROOT` | Retained inputs, original conditions, declared viewing coverage, reviews and binding drift |
| Prepare inspection | `inspection-prepare STORE CANDIDATE PACKET OPTIONS_JSON --expect HASH --root ROOT` | Saved candidate-bound native/enlarged views and measurements; no verdict or acceptance |
| Retain review | `inspection-review STORE PACKET REVIEW_ID REVIEW_JSON --expect HASH --root ROOT` | Explicit reviewer observations and criterion E/V; no nomination or task completion |
| Local MCP | `mcp --root ROOT` | Local PIXL operations over standard input/output |

These command examples describe argument forms. Substitute actual file paths, IDs, and values; preserve quoting when paths contain spaces. Supply the same project `--root` for file validation and store operations, especially when the store is a subdirectory such as `.pixl/`. `decode` and `encode` expose a tagged JSON adapter, not a second authoritative state format. When a CLI command is unavailable in the installed version, read its help and report the mismatch rather than guessing an alternative.

The local MCP server exposes `pixl_family` with `{path, output?}` and `pixl_family_snapshot` with `{store, output_id, candidate_id, expect}`. The report is read-only; the snapshot changes local storage and requires the current state hash. Neither has remote effects. Follow the [family operation](family-delivery.md) for collective review and concrete cold handoff. A successful snapshot returns `accepted: false` because creating a candidate is not acceptance; this field is not an operation error.

Use `pixl_inspection`, `pixl_inspection_prepare` and `pixl_inspection_review` for the
[candidate inspection operation](inspection.md). Discover their closed envelopes
through `tools/list`. Preparation and review mutate local storage with the current
expected hash. Viewing happens through the host, and the review retains caller
declarations separately from actual host or engine evidence.

The durable provider operations are `pixl_job_prepare`, `pixl_job_dispatch`, `pixl_job_observe`, `pixl_job_import`, and `pixl_jobs`; all four mutations require the current expected hash. Follow the [provider recovery operation](provider-recovery.md) for the request envelope, exact submission handoff and cold resumption. Other tools include `pixl_intake`, `pixl_workflow`, `pixl_validate`, `pixl_context`, `pixl_ready`, `pixl_impact`, `pixl_init`, `pixl_commit`, `pixl_catalog`, `pixl_sources`, `pixl_source`, `pixl_asset_check`, `pixl_encode`, `pixl_knowledge`, `pixl_capabilities`, `pixl_prepare`, and `pixl_job`. Discover complete schemas with the connected server's `tools/list`; the harness may namespace names. `pixl_sources` reads installed knowledge; `pixl_source` defaults to project paths, while `scope: "library"` reads installed source slices. `pixl_capabilities` is dated local information. Legacy `pixl_prepare`/`pixl_job` are stateless helpers. No local tool submits or polls PixelLab, and a saved observation is not independent service verification.

The optional MCP configuration examples live in `../../../config/`. They deliberately contain explicit project and plugin paths, and the manifests do not auto-start the server. Resolve the templates for the current installation and project before use. PixelLab's authenticated remote server is configured separately by the harness; do not store its credentials in the UDL or plugin.

On validation failure, preserve the candidate and report the exact diagnostic. On stale-hash commit failure, reread current state, reconcile the candidate, and validate again. Do not force-write the store. Generated assets and journal records belong under the selected project root, never in the plugin's bundled resources.

## Requirements and direct planning

Retain large JSON reports without embedding the tool result in a shell command:
that can exceed Windows command-length limits and can change quoting or Unicode.
Copy a host-spilled response as bytes when available. Otherwise run the equivalent
bundled CLI command and stream stdout into a binary file with `subprocess.run`:

```python
with open(report_path, "xb") as output:
    subprocess.run([python, runner, "context", state, focus,
                    "--view", "authoring", "--root", project_root],
                   stdout=output, check=True)
```

Use actual resolved paths; create the parent directory first. Parse the saved JSON
explicitly as UTF-8. MCP may return both text `content` and `structuredContent`;
verify they agree before selecting one for a formatted report. The wrapper is not
a second independent observation. When rerunning a read, record its current state
hash rather than claiming it is the exact earlier response after state changed.

Use `pixl_plar_read` / `pixl_plar_save` for the consumer project's requirements queue; [PLAR](../../plar/SKILL.md) defines the semantic inventory operation. Use `pixl_commit` with inline `document` for a complete next-revision JSON plan when available. It accepts the same JSON shape as `pixl_encode` and runs the same state validation, without requiring a temporary wire file. Supply exactly one of `document` or `candidate`, along with `store` and the current `expect` hash. CLI equivalent: `commit STORE PLAN.json --json --expect HASH --root PROJECT`.

## Direct result files

Context, request-review, review-context, candidate-review, family, family-snapshot
and PLAR handoff accept CLI `--result-path` / MCP `result_path`. Supply an explicit
consumer root and fresh relative path. The tool returns a compact path/hash/size
summary and writes the full result (JSON, or CLI full wire context as PX text).
On `result_saved:false`, inspect the returned `operation_result` and current state:
publication may have succeeded even though file export failed. Default output and
existing operation recovery rules remain unchanged.
