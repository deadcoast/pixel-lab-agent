# Runtime and tool boundaries

Read the bundled specification before producing UDL. The runtime's actual CLI help and MCP `tools/list` responses define callable arguments. Resolve `../../../scripts/pixl.py` relative to this reference directory, then invoke it with Python 3.11+ from the user's project directory. The selected Python environment also needs Pillow 10+ and jsonschema 4.18+. Use a project virtual environment; install the source package with `python -m pip install -e .` from the source checkout, or install the bundle's `../../../requirements.txt` with `python -m pip install -r "<resolved requirements path>"` in the destination environment. The plugin includes PIXL's own runtime source, not a Python interpreter or third-party packages.

| Operation | CLI form | What it establishes |
| --- | --- | --- |
| Validate | `validate FILE --root ROOT` | The implemented syntax, schema, and reference checks |
| Focus context | `context FILE FOCUS --budget BYTES` | Dependency closure within a strict byte budget; bytes are not model tokens |
| Ready work | `ready FILE` | State-level readiness according to declared prerequisites |
| Change impact | `impact FILE ID` | Declared relationships affected by a proposed change |
| Commit candidate | `commit STORE CANDIDATE --expect SHA256 --root ROOT` | Validated state replacement if the current canonical hash matches |
| New state | `init STORE --name NAME --root ROOT` | A valid initial local store; initial style defaults remain unconfirmed |
| Decode adapter | `decode FILE` | Tagged JSON interchange for inspecting or editing UDL through tools |
| Encode candidate | `encode ADAPTER_JSON --out FILE` | UDL bytes from the tagged interchange form; validate before commit |
| Source catalog | `catalog ROOT --out FILE` | A local source catalog, not remote tool availability |
| Source slice | `source FILE --expect SHA256 --start N --end N --budget BYTES` | Exact source lines from hash-verified bytes, without silent truncation |
| Art knowledge | `knowledge [METHOD_ID]` | Small method index, or the full source-grounded selected method |
| PixelLab catalog | `capabilities [TOOL_NAME]` | Small dated tool index, or one tool's documented parameters |
| Prepare intent | `prepare TOOL ARGUMENTS_JSON --schema INPUT_SCHEMA_JSON` | Validated local request and its hashes, without submission |
| Observe job | `job JOURNAL_JSON STATE --remote-id ID --evidence RECEIPT_JSON` | Returned journal with caller-supplied observation; persist deliberately |
| Method proofs | `poc --out DIRECTORY` | Executed bounded reference checks and artifact hashes |
| Image constraints | `asset-check IMAGE --width W --height H --palette HEX ...` | Implemented local image checks; palette is optional |
| Local MCP | `mcp --root ROOT` | Local PIXL operations over standard input/output |

These command examples describe argument forms. Substitute actual file paths, IDs, and values; preserve quoting when paths contain spaces. Supply the same project `--root` for file validation and store operations, especially when the store is a subdirectory such as `.pixl/`. `decode` and `encode` expose a tagged JSON adapter, not a second authoritative state format. When a CLI command is unavailable in the installed version, read its help and report the mismatch rather than guessing an alternative.

The local MCP server exposes `pixl_validate`, `pixl_context`, `pixl_ready`, `pixl_impact`, `pixl_init`, `pixl_commit`, `pixl_catalog`, `pixl_source`, `pixl_asset_check`, `pixl_encode`, `pixl_knowledge`, `pixl_capabilities`, `pixl_prepare`, and `pixl_job`. Discover their complete schemas with the connected server's `tools/list`. Tool names may be namespaced by the harness. `pixl_capabilities` describes local integration information; inspect the actual connected PixelLab tools to establish remote availability. `pixl_prepare` creates local intent, and `pixl_job` manages local journal state. No local tool submits or polls PixelLab, and a journal entry is not independent verification of a service result.

The optional MCP configuration examples live in `../../../config/`. They deliberately contain explicit project and plugin paths, and the manifests do not auto-start the server. Resolve the templates for the current installation and project before use. PixelLab's authenticated remote server is configured separately by the harness; do not store its credentials in the UDL or plugin.

On validation failure, preserve the candidate and report the exact diagnostic. On stale-hash commit failure, reread current state, reconcile the candidate, and validate again. Do not force-write the store. Generated assets and journal records belong under the selected project root, never in the plugin's bundled resources.
