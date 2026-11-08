# Provider submission and recovery operation

Use this operation when a PIXL production task needs an external generation request, a submitted attempt needs resumption, or a returned candidate needs to enter project state. Developing this operation is a maintainer task; only a production assignment or explicit evaluation activates PIXL.

Read the [PX2 specification](../../../resources/spec/PIXL-2.md), its [registry](../../../runtime/pixl/registry-v2.json), and the [journal contract](../../../resources/spec/provider-recovery.md). This operation uses the explicit J.jr/op/xs extension. Existing unjournaled J and PX1 stores keep their earlier meanings; adding fields or changing a header does not manufacture durable history.

## Required context

- The project root, current store state/hash, task and selected planned F outputs. Use the [intake/sample operation](intake-sample.md) first if choices or criteria are missing. Sample tasks may test proposals; dependent production still needs adoption and confirmation.
- The actual connected provider identity, selected tool and exact inputSchema observed through this harness, with a retained discovery source, timestamp and evidence. A cached capabilities list is advisory. If live tools are absent, preserve the plan and explain the missing capability; do not invent a discovery observation.
- The user's established authorized scope and budget, retained as a scope string and evidence object. Existing authorization can support this record; a local tool does not grant new authority. Resolve a consequential missing budget/permission before a paid call while continuing independent work.
- For recovery, the saved intent and every retained observation. For import, the actual already downloaded file and evidence relating it to this returned resource. Keep credentials out of arguments, schema examples, discovery, authorization and response evidence.

Resolve `../../../scripts/pixl.py` relative to this reference directory and invoke its absolute path using the selected Python environment. The commands below omit that common prefix. Use the same project `--root ROOT` throughout; STORE is a subdirectory of ROOT. Every mutation consumes the current `--expect HASH` and returns the next hash. Files and evidence belong in the project, outside installed resources.

## Prepare a saved request

Prefer the actual connected official PixelLab MCP operation when it fits the task. Use [operation and reference selection](pixellab-operations.md) first: confirm the native canvas, reference roles and output packaging. Preserve image transport identifiers with their local source hashes. The optional HTTP route below is a selected integration, not a substitute for every MCP workflow.

When the host exposes the optional PixelLab HTTP bridge, use `pixellab_contract`
to inspect its retained official HTTP schema, source date and simulated/live flag.
It currently supports one async image operation. This is a dated HTTP contract,
not live MCP discovery; HTTP `image_size` is distinct from MCP width/height aliases.
`pixellab_prepare_image` validates and saves the request against the planned task
and output. Then `pixellab_submit` claims, submits once and records the response;
do not call local `job-dispatch` first. `pixellab_poll` observes the saved ID once
(allow the returned interval between real polls), and `pixellab_import_image`
decodes and retains a completed response as an unaccepted candidate. Each mutation
requires the current store hash. Continue with normal inspection and acceptance.
Unknown submission outcomes cannot be resubmitted; preserve and reconcile them.
Mocked bridge observations remain simulated, including in handoffs.

1. Run `workflow STORE/state.px --root ROOT` and `jobs STORE/state.px --root ROOT`. Read both lifecycle blockers and existing provider attempts. An open task does not imply permission to create another remote job. Pending prepared/unknown/submitted/running work on the output must be resolved first.
2. Retrieve the task's focused context. Translate its intended output and relevant inputs, decisions, methods and contract into the actual tool schema. Preserve arguments exactly; describe any requirement the tool cannot express and the later acceptance check that will evaluate it.
3. Write a request JSON object with exactly `provider`, `tool`, `arguments`, `schema`, `discovery`, and `authorization`. `schema` is the full inputSchema object. Discovery has `source`, `observed_at`, `evidence`; authorization has `scope`, `evidence`. Evidence must be nonempty objects. Timestamps require an explicit UTC offset and at most six fractional digits. Capture observation time from the host clock when observing/recording the response (for example, Python datetime.now(UTC).isoformat()); keep provider event time separate. Do not invent a precise time from the session date, and omit optional timestamps that were not observed. Values come from the current assignment and observations, not from a bundled art fixture.
4. Run `job-prepare STORE JOB TASK REQUEST_JSON --outputs OUTPUT ... --expect HASH --root ROOT`. This saves exact request/schema/provenance/authorization and the relevant plan hashes. Read its cached assessment: a conflict is a reason to inspect current documentation and tool semantics, not to silently rewrite the request or substitute the cache for the observed schema. Schema validity alone cannot establish account entitlement, output quality or actual cost.

Preparation is complete when state contains the prepared J and immutable journal X/E. No remote action has occurred. A missing tool, unresolved project requirement or missing authorization leaves useful local planning intact.

## Claim once, then call the actual provider

Run `job-dispatch STORE JOB --expect HASH --root ROOT`. Only a successful publication returns `dispatch_request`. It first records a local dispatch claim and moves the saved job to **unknown**, before the host sends anything. Use exactly the returned provider/tool/arguments for the one authorized host call. Do not add defaults or replace arguments after claiming; that would be a different request.

The local command does not submit, poll, authenticate or download. `remote_executed: false` describes the local tool even when its journal later records a caller-observed success. Real provider effects remain the host's responsibility.

Retain the response without credentials and use `job-observe STORE JOB STATE EVIDENCE_JSON --remote-id RETURNED_ID --expect HASH --root ROOT`. Accepted states submitted/running/succeeded require the actual observed identifier. A supplied failure can be recorded without inventing an ID. After identity is known, omitting `--remote-id` preserves it; it cannot be rebound. Repeat running/unknown observations only when supported by actual observations. A failed or succeeded outcome is terminal for observations.

If submission returns no usable answer, record `unknown` with the actual timeout/transport evidence when available. Never treat the initial unknown claim as evidence that a provider received the request, and never treat a missing ID as evidence that it did not.

For delegated work, compare the saved prepared request with the exact arguments in the [reviewed request packet](request-review.md) before dispatch. Changed arguments or criteria require an updated comparison; an unchanged reviewed contract does not require the user to repeat authorization.

## Resume and reconcile

Start with `jobs STORE/state.px --root ROOT`. It returns the saved request, context, event history, remote identity, candidate associations, drift and next action. Reading a request is not a new dispatch grant.

| Saved state / issue | Next operation |
|---|---|
| Prepared, context current, no blockers | Claim with job-dispatch before one host call |
| Prepared, plan drift or lifecycle blocker | Resolve the specific context; abandon obsolete intent with an evidenced failed observation if appropriate, then prepare a new request ID |
| Unknown | Reconcile using the actual provider's documented lookup/status capabilities and retained evidence; do not dispatch or recreate |
| Submitted/running with ID | Inspect that exact resource using its discovered status tool, then record the observed response |
| Succeeded | Retrieve the actual output through the host, import local candidate bytes, then evaluate acceptance |
| Failed | Preserve failure, establish its consequence and any still-valid retry authorization, then use a new job ID for a new attempt |
| Legacy unjournaled job | Inspect its actual available history manually; do not attach a fictional journal or ignore pending work |
| File/hash error | Preserve the diagnostic and restore the exact retained bytes from available history/backups before continuing; do not rewrite receipts to make a changed file pass |

A crash between claim and host submission also leaves unknown. If no provider lookup can resolve whether the request was sent, leave that uncertainty explicit and continue independent work. Elapsed time cannot authorize a retry. A confirmed non-acceptance or terminal failure may support a failed observation and a newly authorized attempt; record that evidence first. Automatic remote exactly-once delivery is not claimed.

On `stale_write` or `store_locked`, no dispatch grant was returned. Reread the state and owner information, then reconcile the attempted local change. Do not blindly repeat job-dispatch if another writer already claimed it. Immutable blobs left by a failed publication are unreferenced preparation data; state.px is the publication authority.

## Import and hand back to acceptance

Download with the actual host/provider mechanism into the project. Then run `job-import STORE JOB OUTPUT CANDIDATE DOWNLOADED_PATH EVIDENCE_JSON --expect HASH --root ROOT`. DOWNLOADED_PATH is relative to ROOT. This copies a byte snapshot into the store and creates X.of for the original F, plus a retained import event and J.xs reference. It preserves the downloaded original. It does not nominate the candidate, measure the image, grant V, or finish T.

Import rejects changed output/contract/criterion context. Keep the returned file and original history; reconcile the intended plan explicitly before associating it. A new interpretation must not relabel an old generation as though it used the new contract. Submitted observations can still be recorded while the plan has drifted.

Retrieve the imported X to obtain its retained path/hash. Run relevant mechanical inspection, review the actual image at native and enlarged scale, and exercise the required destination checks. Follow the [intake/sample acceptance procedure](intake-sample.md) to nominate a candidate deliberately and record each Q's pass, fail or unavailable verdict. Provider success and journal-retention receipts cannot satisfy those requirements.

The operation stops with a truthful recovery action or an imported candidate ready for its specified acceptance checks. Handoff includes the job and candidate IDs, actual observed state, retained paths, unresolved checks and the next dependency. No finished asset family or engine readiness follows from this local operation alone.
