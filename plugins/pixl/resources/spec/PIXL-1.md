# PIXL/1 normative specification

Status: implemented version 1.0.0. PIXL is a project-specific, agent-operated UDL; this document is its decoder contract. The wire form has no human usability requirement. Host profiles are a separate translating layer. Reserved notation cannot silently acquire a new meaning.

## Wire grammar

Input is UTF-8, maximum 16 MiB. ASCII whitespace is insignificant outside literals. There are no comments, escapes, implicit coercions, expressions, interpolation, executable imports, or indentation semantics. Parsing is bounded to 64 nested value containers and 100,000 records. ASCII identifiers match `[A-Za-z][A-Za-z0-9_.-]{0,95}`. IDs are case sensitive and document-unique.

```ebnf
document = "PX1", whitespace, revision, whitespace, { record, whitespace } ;
record   = "@", identifier, ":", kind, map ;
map      = "{", [ identifier, "=", value, { ";", identifier, "=", value } ], "}" ;
list     = "[", [ value, { ",", value } ], "]" ;
value    = literal | reference | symbol | integer | list | map | "+" | "-" | "?" ;
reference= "@", identifier ;
symbol   = identifier ;
integer  = [ "-" ], digit, { digit } ;
literal  = "~", unsigned-byte-count, ":", exactly-that-many-UTF8-bytes ;
kind     = one-uppercase-ASCII-letter ;
revision = unsigned-integer ;
```

`+` is true, `-` is false, `?` is absent/null. Integers are signed 64-bit; lengths and revisions are nonnegative. Floating-point wire values are intentionally absent: coordinates are integer pixels; duration is integer milliseconds; fractional quantities use declared fixed-point units in asset metadata, or opaque provider JSON at the boundary. A symbol and a literal with the same visible text are different values. A reference is never a string. Lengths count UTF-8 bytes, not characters. `~0:` is an empty literal. A literal may contain newlines, delimiters, backslashes or NUL without acquiring syntax. A malformed UTF-8 length boundary is an error. Duplicate fields are errors.

Canonical encoding starts `PX1 <revision>\n`, sorts records by ID and map fields by ASCII key, preserves list order, uses decimal integers without leading zeroes and one newline after each record. Canonical map/list values contain no insignificant whitespace. SHA-256 over canonical document bytes is the snapshot identity. SHA-256 over the canonical record bytes (without the trailing newline) is a record identity. Revision is not a record field. Noncanonical valid input can be normalized without changing its semantic values.

## Semantic registry

The complete field/type dictionary is [`registry.json`](../pixl/registry.json). That machine-readable registry and this specification are normative together. Unknown kinds, fields and closed-enum values fail validation; extension requires a new explicit version. All fields are required unless marked optional in the registry. `tg` is an optional list of literal tags on every kind. Map payloads are permitted only in declared fields; they cannot override core fields.

The bundled operational knowledge library is `knowledge/library.px`. Its K `rq` prerequisites and `rk` failure conditions preserve the curated source conditions. `ap` atoms are generated from source applicability phrases with stable SHA-256 suffixes; their exact meanings are in the hash-bound `knowledge/applicability.json` source. They are domain symbols, not inferred new core language rules. Source JSON is retained for curation and host interchange; the compiled K/S/E graph is available directly to contextual operation.

| Kind | Meaning | Operational replacement |
|---|---|---|
| A | actor and responsibility | ownership / agent role |
| P | project and active visual contract | project design envelope |
| S | source with digest and locator | reference tagging / provenance |
| R | runtime/tool dependency with exact version locator | tech stack |
| C | visual contract, dimensions, palette, view, sampling and alpha policy | art design document |
| K | applicable knowledge method, procedure, checks, research and POC references | technical knowledge |
| D | decision: `wh` who, `wt` what, `wr` where, `wy` why, `rs` research, `pc` proof | design rationale |
| T | task, ownership, dependencies, decisions, inputs/outputs, state and evidence | work plan / TODO / dependency graph |
| X | artifact/reference and its expected bytes, contract and metadata | asset manifest / content map |
| E | evidence receipt, outcome, mode, file hash and bound record hashes | test/review result |
| J | external job identity, request digest and observed state | tool execution memory |
| N | resumption focus, next tasks and blockers at a specific revision | contextual handoff |

References resolve within the document and must match the declared target kind. Task `dp` edges are directed from dependent to prerequisite and must be acyclic. Other reference cycles are legal (for example a decision and its proof) and closure uses visited IDs. Ready tasks are open tasks whose prerequisites are all done. Dropped prerequisites do not satisfy a dependency. Active/blocked/done tasks are not advertised as ready. A done task needs at least one current passing evidence receipt and all prerequisites done; those passing receipts must collectively bind every current `io` artifact record. A task cannot be done with no `io` artifact. Evidence binding `{rf=@id;dg=~64:<record-sha256>}` snapshots the full record, not its name. Any record change invalidates that binding. Passing evidence does not erase failing evidence.

Decisions require nonempty research and proof lists, and nonempty who/what/where/why content. Their current proof receipts must collectively bind the decision record itself and its semantic dependency closure. Proof receipts may report failure: a decision can reject a failed method. A K with `pc` must have current receipts binding that method and its semantic sources; an active/done task requires passing receipts covering that scope. K methods without executed proof are retained as researched knowledge, but an agent must execute an applicable POC before adoption. A method's recipe is not an executed proof. Agents preserve conflicting observations in separate source/evidence records and resolve them through a new decision rather than overwriting history.

**Semantic proof scope** traverses only `A/S/R/C/K/D/X`. It stops before workflow/project/proof kinds `P/E/T/J/N`, which would otherwise entangle mutable task states and proof history with the result being proved. X proof bindings must cover its scope, including the linked C. Link source/runtime/contract records directly when their content is part of the proof; a pointer through P does not bind that project's contents. K and D can point to E by ID while E binds their hash: the hash contains reference IDs, not recursive target hashes.

Evidence `ob=+` marks a superseded receipt. Its original outcome, file and old bindings remain preserved; outdated record hashes are allowed only in superseded receipts. Such receipts never count for decisions, method adoption or completion. Store commits forbid modifying existing E fields except one-way supersession; add a new E ID for new execution. Receipt metadata is a caller assertion supported by retained files. Hash validation establishes identity and freshness, not cryptographic attestation that a model, service or test runner told the truth.

File checking is optional for structural validation and mandatory when accepting completion in a store. With a project root, X/E local paths and locally addressed S bytes must exist, remain within that root after symlink resolution, and match their declared SHA-256. URL sources are not downloaded by validation; their digest identifies a recorded snapshot and does not assert current remote truth. Source `ln` ranges are inclusive, one-based and valid for the local source. Empty palettes mean no exact palette restriction, not zero colors. C rules apply only to linked artifacts; source art can intentionally choose a different contract.

## Retrieval and drift

`context(focus)` includes the focus, all project roots and their transitive references, and the focus's transitive reference closure. For T focus it also includes associated J records and handoffs mentioning the focus. This is a conservative correctness baseline; it never silently truncates a required dependency or decision. If canonical packet bytes exceed a requested byte budget it returns a budget error with the required size. Bytes are not claimed to equal model tokens. Large project roots should not reference every task: tasks point to their project. Returned subsets keep the original revision and validate as closed documents.

`impact(id)` traverses reverse references transitively. The changed node itself is included. `ready` returns stable sorted task IDs. A content map is a query over X/S records and `tg`; a stack is a query over R; decisions over D. There are no duplicated authoritative Markdown TODO/stack state files. Source catalogs are derived indexes and can be rebuilt.

## State publication

A store contains `state.px`, immutable `history/<canonical-sha>.px`, and a temporary exclusive `.lock` while writing. Initialize once. A candidate must have exactly current revision + 1; caller must supply the current canonical hash. Under the lock, reload current state, compare revision/hash, validate the complete candidate and its files, write/fsync its history snapshot and a same-directory temporary state, then atomically replace state. The final state is the commit point. A crash may leave an unreferenced valid history snapshot or lock; it must not publish a partial document. A leftover lock fails with recovery guidance; it is never automatically broken while a writer might be alive. Filesystem snapshots provide local recovery, not distributed consensus or protection from a malicious filesystem writer. Direct manual state editing bypasses these guarantees and is unsupported for operation.

Task transitions: open -> active/blocked/dropped; active -> blocked/done/dropped; blocked -> open/active/dropped; done -> open; dropped -> open. Unchanged states are allowed. Existing IDs cannot disappear or change kind during commit; close/drop records instead. Any change to a done task or its complete reference closure requires reopening that task. Supersede invalidated receipts with `ob=+`, retain their original bindings, add new receipt IDs after new execution, and redirect D/K/T evidence references deliberately. Revision increases are mandatory even for resumption changes.

C describes raster dimensions and rendering intent. X of kind `code` or `report` associates with its production contract but is not interpreted as a raster image. X metadata is an opaque declared payload: the core validates wire values and references, not a target engine's atlas/rig schema. Domain knowledge recipes and appropriate project tools validate those additional contracts. A structural/file validation alone does not establish visual acceptance.

## PixelLab boundary

The host retrieves the actual connected PixelLab tool input schema. PIXL prepares a validated intent with exact tool name, arguments, schema digest and request digest. JSON here is the MCP provider's interchange, not PIXL syntax. Preparation has no remote side effect. The host calls the provider and journals the observed real ID. Generation starts prepared -> submitted -> running -> succeeded/failed; submitted/running may become unknown when observation is lost. Unknown is not permission to recreate a paid job. Recovery requires observation of the existing job; there is no automatic generation retry. A generation result is an artifact candidate, not proof of quality or task completion.

Durations/credits reported in research are estimates from a dated documentation snapshot. Discovered schemas take precedence over snapshots. PixelLab credentials remain in host secret configuration. This runtime does not impersonate PixelLab or invent job IDs. Its MCP server exposes local project tools only; the host connects the actual PixelLab MCP separately.

## Verification boundaries

The suite verifies parsing, graph invariants, writes, request validation, job transitions, artifact measurements, deterministic method POCs and local MCP behavior. Image inspection hashes and measures one immutable in-memory byte snapshot, checks every frame's dimensions and cumulative pixel limit, and labels visual/engine acceptance unverified. Token measurements are encoding-specific comparisons with the same semantic payload, including bootstrap overhead separately. They are not a controlled LLM capability or artistic-quality study. A full live PixelLab job and target-engine visual acceptance must be recorded with real evidence before those outcomes are asserted.
