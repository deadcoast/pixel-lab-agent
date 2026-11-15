# Compact caller result

`plar handoff DETAILS_JSON --view caller` / `pixl_plar_handoff` with
`view: "caller"` saves the existing immutable version-1 handoff, then returns a
bounded presentation of that same captured selection. The default `view: "receipt"`
and saved bytes for identical inputs are unchanged. There is no new ledger, UDL
record, provider action or acceptance event.

## Agent-authored compact fields

`details.status` retains its existing assignment meaning: `delivered`, `partial`,
`needs_input` or `blocked`. It does not follow automatically from production state.
An optional `details.caller` object supplies the following closed fields:

| Field | Content |
| --- | --- |
| `summary` | Nonempty text, at most 600 characters |
| `artifacts` | At most 12 actual project file references |
| `reports` | At most 12 references to separately retained detailed reports |
| `issues` | At most 12 objects with `category`, `summary` and optional `recovery` |
| `integration` | An agent observation with `status`, `summary` and optional `evidence` file references |

All fields are optional. Omission means not reported, not a pass or an unavailable
check. An absent caller block is returned as `caller.present: false`; arbitrary
legacy details are never heuristically summarized. Existing receipt mode does not
reinterpret a legacy field called `caller`.

File references contain exactly `path`, `sha256` and `role`. Paths are nonempty
forward-slash project-relative paths, at most 512 characters. SHA-256 is 64 lowercase
hexadecimal digits; role is nonempty text of at most 96 characters. The operation
confines and hashes every declared artifact, report and integration-evidence file
before publishing. It does not copy those files or guarantee that they remain
unchanged after that observation. Roles and judgments are supplied by the agent.

Issue categories are `invalid_authoring`, `stale_local_state`, `missing_capability`,
`uncertain_remote_result`, `unavailable_observation` and `unfinished_work`.
Summary and recovery text each have the same 600-character bound. The category is
an agent's classification, not an automatic diagnosis or authorization to retry.

Integration status is `pass`, `fail`, `unavailable`, `not_performed` or
`not_in_scope`. Its summary is required and bounded to 600 characters; evidence
uses the same file-reference array. The report labels this block `agent_authored`.
A claimed integration pass does not establish a stored verdict or artistic acceptance.

The complete caller block must encode to at most 8192 bytes as finite UTF-8 JSON
with compact separators. Oversized or malformed blocks, unreadable files and
hash mismatches fail before a new handoff is published. Detailed observations
belong in linked files or the existing unrestricted expert details, not truncated
inside the compact block. `pixl.caller_result.CALLER_SCHEMA` describes the shape.

## Returned facts and exact retrieval

Caller view retains every default receipt field (`path`, `sha256`, `asset_id`,
`requirements_hash`, `state_hash`, `next`, `scope`) and adds:

- `assignment`: the supplied status and its `agent_authored` basis.
- `caller`: presence, authored fields and the file-verification observation.
- `production`: captured task ID/state, selection currency, criterion counts for
  current nominees, job counts and delivery facts. Unperformed/unavailable checks
  remain unresolved. Counts never imply every operation or visual check succeeded.
- `store`: the exact continuation's project-relative production store.
- `details_ref` and `resume_ref`: immutable file path/hash, physical line range,
  UTF-8 byte count and JSON pointer for the saved section.
- `resume_inline`, `resume_bytes`, and the unchanged `resume` when it occupies at
  most 4096 compact UTF-8 JSON bytes. Larger continuations are omitted as a whole
  and remain retrievable through `resume_ref`; there is no partial rewritten resume.
- `refresh`: the exact focused `pixl_plar_read` operation and arguments. Reread
  after state or source changes and compare requirements/state identities before
  acting. This operation is a read instruction, not automatic execution.

Delivery remains exactly the existing handoff's derived delivery value. If larger
than 2048 compact JSON bytes, `production.delivery_inline` is false and
`delivery_ref` identifies `/resume/delivery`; the containing resume line range is
returned intact. `delivery_complete` and `delivery_observed` remain visible.
Destination bytes and declared family criteria do not establish undeclared engine
or artistic checks. Assignment status remains independent even when delivery is
complete or an external destination subsequently changes without a state revision.

Use existing `source` / `pixl_source` with the locator's path, SHA-256, line bounds
and an adequate byte budget. The field slice is exact JSON source text and can
include its trailing object-member comma. The JSON pointer identifies its meaning;
no new reader tool is required. A larger section may be read in smaller physical
line ranges under the same file hash. When parsing as an object, open the complete
immutable file or wrap the returned member after removing its trailing comma.

Caller-view errors use `caller_result_input`, `caller_result_size`,
`caller_artifact_unavailable` and `caller_artifact_stale`; existing `path_escape`,
`handoff_stale`, `handoff_state` and `handoff_corrupt` retain their meaning. A file
failure identifies the declared file's `path` and `expected_file_sha256`; a hash
mismatch also returns `observed_file_sha256`. Its allocation `plar_path` stays
separate from that artifact path in structured diagnostics. A file
export failure does not undo an already saved handoff. Reconcile its returned
operation result before repeating the save; never treat it as a reason to repeat
remote generation.
