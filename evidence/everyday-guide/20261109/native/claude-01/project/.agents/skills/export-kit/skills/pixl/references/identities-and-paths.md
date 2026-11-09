# Hash identities and project paths

Use returned identities rather than recomputing a different hash from a similarly
named object. Public JSON results include additive `hash_domains` labels for the
write guards and report identities below. Keys are dot-separated field paths.
Existing fields and digest algorithms are unchanged. These presentation labels
are outside existing state, binding and comparison identities; they are included
in the bytes of a newly exported result file.

## Which identity belongs where?

| Domain | Returned field | Use |
| --- | --- | --- |
| `canonical_state_sha256` | `validate.hash`, workflow/context `hash`, `review-context.state_hash`, selected PLAR `production.continuation.state_hash` | `expect` for production store publication, review, jobs, completion and handoff. SHA-256 of canonical encoded whole PX state, including revision; not arbitrary input-file bytes or the focused subset. |
| `file_sha256` | PLAR `hash`; artifact, source, manifest or retained handoff `sha256`; export `result_sha256` | Exact file-byte identity. PLAR save takes the current PLAR file hash (`new` only for first creation). Source retrieval takes the expected source-file hash. A manifest hash identifies manifest bytes, not current task acceptance. |
| `selected_requirements_sha256` | Selected PLAR `requirements_hash` | Preparation, allocation binding and handoff selection. Includes relevant sourced/dependency requirements, excludes queue progress and installation paths; not the whole PLAR file. |
| `candidate_bindings_sha256` | Review-context `binding_hash` | Copy into the observation JSON. Protects the candidate and its semantic dependencies; refreshing `expect` does not fix a changed binding. |
| `review_scope_sha256` | Full request-review `review_scope_sha256`; changes view `before/after.review_scope_sha256` | Caller comparison of the exact retained criteria/request scope. Ordinary job observations may leave it unchanged. |
| `comparison_report_sha256` | Changes view `comparison_sha256` | Identifies the structural comparison, including current observations. Excludes itself and the added display labels. It may change while the literal review scope remains stable. |
| `provider_intent_sha256` | Request/job `intent_sha256` | Retained canonical request/context identity. It is neither a provider job ID nor a production publication guard. |

`record_sha256` fields elsewhere identify canonical PX records, not source files.
For an exported JSON file, verify `result_sha256` against the bytes on disk. Then
parse that file to get the required state/binding/scope value. Export summaries may
also carry a state hash; their `hash_domains` distinguishes it from the file hash.
JSON reformatting changes file bytes while some semantic identities stay the same.

Example for the queue successor, after the setup in [everyday production](everyday.md):

```powershell
$Selected = pixl plar read --path $Queue --asset $Asset --root $Project | ConvertFrom-Json
$RequirementsHash = $Selected.requirements_hash
$ProductionStateHash = $Selected.production.continuation.state_hash
pixl plar handoff work/handoff-details.json --path $Queue --asset $Asset --requirements $RequirementsHash --expect $ProductionStateHash --root $Project --result-path work/handoff-result.json
```

Create `work/handoff-details.json` from actual expert findings, for example
`{"status":"delivered","caller_actions":[],"future_work":[]}` only when that
status is warranted. Do not copy a delivered status into an unfinished assignment.
This saves a continuation; it does not accept art. Both result destinations must
follow their operation's retention/no-clobber rules.

## Keep the three locations distinct

| Location | Meaning |
| --- | --- |
| Plugin installation | Read-only workflow/runtime/resources. Resolve its runner and skill links from the installation. |
| Consumer root | The actual project containing source, queue and `.pixl/`. Supply CLI `--root`; configure local MCP with that same absolute root. |
| Production store | A directory inside the consumer, such as `.pixl/assets/queue.ready`. Its name need not match the selected asset; use the queue's saved continuation. |

The local MCP accepts forward-slash, root-relative paths such as
`.pixl/assets/queue.ready/state.px`. It rejects absolute/drive-prefixed paths,
backslashes, root itself and traversal/symlink escapes. CLI paths have two forms:

| CLI argument | Resolution |
| --- | --- |
| `validate`, `context`, `workflow`, `jobs`, `family`, `review-context` input state; mutation store directories; ordinary JSON input files | Shell working-directory path, or absolute path. Use an absolute `$StateFile`, `$StoreFolder` or JSON file when working outside the consumer. `--root` does not rebase these arguments. |
| `request-review` packet/state and comparison files; PLAR `--path`, `--packet`, `--connection`; `stage-prepare` packet; imported artifact path; `--result-path` | Relative to explicit consumer root. Use `$State`, not `$StateFile`, for request-review. Some inline arguments have their own documented forms. |
| `source PATH --root ROOT` | Relative to ROOT and expected source file SHA-256; retained source resolution is supported. Without `--root`, PATH is an ordinary filesystem path. |

The same assignment works after copying its whole consumer to a new root, including
a path containing spaces. Update the root/absolute CLI input paths; keep saved
project-relative locations intact. Do not rewrite retained files to change hashes
or weaken confinement to accommodate an incorrectly formed call.

## Follow source locators exactly

A source ID, a file path and a line range serve different purposes. Follow the
report's `retrieve.tool` and `retrieve.arguments` against the same MCP root. For
project text, the equivalent CLI is:

```powershell
pixl source BRIEF.md --root $Project --expect $SourceFileHash --start 3 --end 3 --budget 4096
```

`$SourceFileHash` comes from that source's returned `sha256`, not `record_sha256`.
Line bounds are one-based and inclusive. Read the returned exact text; a locator
label is not a substitute. Hash mismatch means source drift to reassess. A budget
failure requires a narrower range, not silent truncation. For JSON, retain the
whole-file byte hash and identify the actual JSON pointer during review. New
authoring should bind precise clause ranges/pointers; leave old broad bindings
unchanged and report their limitation.

Library retrieval is a separate root: MCP `pixl_source` with `scope:"library"`
uses installed resources. For CLI, resolve that resource directory explicitly and
use it as `--root`. Keep consumer and bundled-source locators distinct.

## Recover from the actual error

- `stale_write`: reread the correct domain, reconcile the intended change, then
  retry according to the operation. PLAR save needs its file hash; production
  writes need canonical state. A fresh hash does not authorize changed semantics.
- `handoff_stale`: refresh both selected requirements and production continuation;
  do not substitute the top-level PLAR file hash for production state.
- `path_escape`: the diagnostic names the declared root. Use its relative path for
  the rejected argument. Do not switch roots to an ancestor merely to admit it.
- `result_exists`: choose a fresh export name; retain earlier evidence.
- `result_saved:false`: inspect `operation_result` and current state. Publication
  may already have succeeded; recover using the same operation ID/payload rather
  than treating the export failure as permission to repeat generation.
