# plar.txt format and operations

Version 1 is UTF-8 JSON, not a new programming language. The normative shape is [plar.schema.json](../../../runtime/pixl/plar.schema.json). A complete worked project is [the queue UI example](../../../resources/examples/plar-project/README.md). Read its source before its example requirements.

Top-level fields:

| Field | Meaning |
| --- | --- |
| version | `1` |
| project | `name` and concise `brief`; no absolute installation paths |
| coverage | Arrays `included`, `excluded`, `unresolved`; authored scan boundary and blind spots, not proof of reading, viewing or execution |
| sources | Stable `id`, project-relative `path`, optional `sha256`; saves bind existing files without a hash |
| assets | Stable rows described below; an empty list is valid when the inspected scope requires no production art |

Each asset has `id`, `kind`, `purpose`, `status`, `consumers`, `existing`, `requirements`, `delivery`, `depends_on`, `questions`, `next`, and `evidence`. Optional `production` links `store`, `task`, `output`. Optional `references` names visual inputs as described below. Kind is a descriptive string; UI panels, fonts, atlases and normal maps need not pretend to be sprites here. Translate to the actual PIXL/provider contract during production.

- `consumers`: `{source, symbol, usage}`; source is an ID from the sources table. Symbol and usage explain the binding, not merely a filename.
- `references`: `{source, role, instructions}`; source is a bound source ID. Role is `style`, `identity`, `pose`, `layout`, `palette`, `mask` or `motion`. Instructions say what to preserve. These are optional for text-only briefs; a filename mentioned in a requirement is not provider image transport.
- `existing`: `{path, role}`; role explains reusable/placeholder/reference or other current use. Missing paths are reported, not rejected. A present path is not a source binding or proof that its bytes were inspected. Use a source/reference binding when that visual input must contribute to the selected contract, and retain file-hash observations for exact byte-preservation claims.
- `requirements`: `{property, value, authority, sources, reason}`. Value is JSON; authority is `requirement`, `observation`, `proposal`, or `unknown`. Sources is an array of source IDs. An empty array is useful for an explicit unsourced proposal/unknown; support adopted requirements with addressable evidence.
- `delivery`: `{path, checks}`; exact destination (file or package path) and applicable mechanical, visual and consumer/import checks.
- `depends_on`: other asset IDs; cycles and dangling IDs are rejected.
- `questions`: unresolved choices relevant to this asset. `next`: one actionable instruction.
- `evidence`: `{path, note}` links to retained results. Source-bind evidence that must remain byte-identical.
- `status`: `todo`, `in_progress`, `review`, `integrated`, or `deferred`. Status is authored by the host. File existence does not prove integration or quality.

All paths are relative to the consumer root and use forward slashes. Source hashes detect local drift; they do not prove the interpretation of the source. Coverage should distinguish present-but-uninspected files, unavailable sources and inspected code whose runtime or visual behavior remains unobserved; retain the corresponding read, visual or execution evidence separately. The reader reports changed/missing/unbound sources and missing files. It does not restamp changed sources, guess readiness, contact PixelLab or certify artistic quality. Refresh a hash only after re-reading and reconciling the dependent claims. Focused reads include the full transitive dependency rows and their issues, so a caller does not lose the style baseline or an unresolved source when delegating a dependent asset.

## MCP

`pixl_plar_read({})` returns the queue, project scope and source binding results. To select an asset:

```json
{"asset_id":"queue.working"}
```

Save through `pixl_plar_save` with `document` holding the complete JSON document and `expect` equal to the last returned file hash, or `"new"` for creation. Optional `path` defaults to `plar.txt`. A stale write is rejected; re-read and merge. Previous changed bytes are retained under `.pixl/plar-history/`. Keep independent queues in separate files when project scope requires it.

Use `pixl_commit({store,expect,document})` for a PX2 document with its next revision. The JSON record format uses `{"$ref":"id"}` and `{"$symbol":"value"}`. Exactly one of `document` or the existing `candidate` wire-file path is accepted. The same revision, dependency, evidence and acceptance checks apply. PLAR does not automatically invent PX2 decisions or criteria.

## CLI and portability

Resolve the plugin runner relative to this skill, then use its **absolute** path with the target project root:

```text
python /ABS/PLUGIN/scripts/pixl.py plar read --root /ABS/PROJECT
python /ABS/PLUGIN/scripts/pixl.py plar read --root /ABS/PROJECT --asset queue.working
python /ABS/PLUGIN/scripts/pixl.py plar save /ABS/document.json --root /ABS/PROJECT --expect new
python /ABS/PLUGIN/scripts/pixl.py commit /ABS/PROJECT/.pixl /ABS/plan.json --json --expect STATE_HASH --root /ABS/PROJECT
```

Copy/install the complete plugin, not the skill directory alone. Requirements and outputs stay in the consumer project. The CLI can support a host without MCP; the MCP server exposes the same deterministic operations when configured with that root.

## Focused delegation identity

A selected read returns `project_root`, `requirements_hash`, `asset`, full `dependencies`, relevant `sources`, `visual_references` and a derived `production` view. Source rows add `observed_sha256` and `absolute_path`; stored source paths remain portable and relative. The full queue's existing `hash` is still the compare-and-swap token for saves.

The requirements hash covers the selected asset and transitive dependency requirements, their bound/current source identities and project brief. It excludes status, next action, evidence lists, production-state links and absolute installation paths. It does not assert readiness or acceptance; read dependency status/issues separately. Changing a style reference changes this hash even before someone refreshes its saved source hash. An unrelated asset's queue progress does not.

This additive version-1 extension keeps existing documents valid. Use a runtime containing the reference-role extension to author documents with `references`; older closed-schema readers cannot interpret new fields.

## Selective refresh

Queue reads include `changes`: tracked source drift, direct and transitively affected asset IDs, and unaffected IDs. Pass `since` (CLI `--since`) with a retained prior PLAR byte hash to compare declarations as well. Saves return this comparison against the replaced version. Queue progress fields (`status`, `next`, `evidence`, `production`) are not requirement changes. Coverage changes are reported separately. History bytes are hash-checked before comparison. Use `since` on the whole queue, then select an affected asset; focused reads include `dependency_issues`.

This is conservative file/dependency impact, not a semantic code scanner. Re-read changed code and look for new states, consumers or dynamic paths. A shared source edit can affect several rows for review without requiring all their requirements or assets to change. Do not merely refresh hashes or clear pre-existing drift outside the reconciled claims. Preserve those stored bindings and report the remaining drift. Stable asset IDs and unchanged authored requirements are distinct from an unchanged requirements hash: the latter also requires an unchanged relevant source/dependency identity. Keep stable roles/IDs on destination moves; retain superseded work as deferred where applicable.

[First-candidate preparation](prepare.md) consumes a focused selection and the exact reviewed request/criteria artifacts, removing handwritten PX2 setup from that path.

## Allocation and production continuity

A focused read joins the selected row to its retained PX2 store. `production` reports
current task/output acceptance, selection identity, provider-bound pending jobs and
one next action. Missing or invalid state is an explicit diagnostic while the
requirements remain readable. Queue `status` remains an authored progress label.
`new_request_allowed` is only a local selection/pending-work advisory; preparation
still validates the exact reviewed request, current source identity and connection.

After the selected task is accepted, `production.delivery` compares its nominated
bytes with the declared destination and reports every saved containing family's
current acceptance and manifest. `next_action: delivered` requires matching bytes,
current requirements and completed containing families, including current explicit
PLAR selections for their production members; it creates no new verdict. An older
sample baseline retains its historical contract and separately scoped adoption.
Missing/changed destination files or unfinished collective review keep
`review_delivery`. Pending jobs and changed requirements retain their earlier
recovery priority. The authored `integrated` label cannot establish completion.

Single-output preparation links the resulting store/task/output and snapshot evidence
back to the row. A failed concurrent queue save leaves the prepared job intact; resume
the same preparation to repair its link. The default asset store is discoverable;
custom stores require the existing link or explicit store argument. Multiple outputs
need a deliberate choice of the delivery output.

Source changes require review of affected/dependent rows, not automatic replacement
of all art. For a revised contract, reconcile pending work on its original connection,
retain the reviewed new packet, then use `plar prepare --revise --expect STATE_HASH`.
The new generation is appended to the existing store; prior inputs, jobs, candidates
and verdicts remain. Use returned IDs. Historical acceptance describes its original
contract and cannot complete the newly selected generation.

Multi-output preparation also retains its explicit current task separately from the
delivery-output link. Focused reads use that task without guessing the newest ID
or timestamp. Prior preparation generations remain visible as history and do not
become current merely because their source requirements still match. A missing
legacy focus with several generations needs an unchanged explicit preparation
retry with `--revise --expect STATE_HASH`; use the exact intended prepared packet
and resolve other pending work first. A corrupt focus is reported for reconciliation,
not silently ignored. This metadata does not change the version-1 PLAR shape or
PX2 records; older readers retain their earlier multiple-unlinked-task limitation.
