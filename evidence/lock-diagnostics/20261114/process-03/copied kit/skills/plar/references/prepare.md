# Prepare the selected asset's first request

Use this when a selected PLAR asset needs its first concrete candidate. Read the
selected source/dependency context and the actual PixelLab tool declaration first.
Choose an appropriate first operation and explicit candidate controls. Retain the
ordinary request/criteria packet and let the caller compare it with the original
sources through [request-review](../../pixl/references/request-review.md).

Resolve the exact source/criterion evidence with `pixl_request_review` before the
caller adopts the contract; its report exposes locator problems without certifying
semantic consistency. Use the caller comparison described in the linked operation.

The local preparation operation handles PX2 records and first-job creation. Keep
expert interpretation in the packet: the runtime does not infer a prompt from code,
choose an art style, or certify that all source requirements survived.

1. Save the exact provider arguments as JSON. Point `request-review.json.request`
   to its path/hash/tool with `kind: provider_arguments`; include all selected
   source identities and the focused read's top-level `requirements_hash`.
2. Make its `criteria` artifact a compact candidate plan: version, scope and outputs,
   each with a concrete raster contract and the actual acceptance criteria. See
   [the contract](../../../resources/spec/asset-preparation.md) and
   [schema](../../../runtime/pixl/asset-plan.schema.json).
3. Save the discovered provider/schema/discovery/authorization as `connection.json`.
   Capture the actual host clock for discovery; carry established authorization.
4. Call `pixl_plar_prepare` with asset_id, requirements_hash, packet and connection
   (inline object or project-relative filename). It returns the saved plan, job and
   next action. CLI equivalent:

```text
python /path/to/pixl/scripts/pixl.py plar prepare --root PROJECT --asset ASSET_ID --requirements HASH --packet work/request-review.json --connection work/connection.json
```

The candidate-plan shape is ordinary JSON, not tagged PX2 records:

```json
{
  "version": 1,
  "scope": "First status candidate for review under the actual assignment",
  "outputs": [{
    "id": "status", "name": "Status candidate", "kind": "sprite",
    "contract": {
      "size": [16, 16], "palette": [], "view": "ui",
      "sampling": "nearest", "alpha": "full",
      "intent": "Replace these illustrative values with this asset's sourced or scoped candidate choices."
    },
    "criteria": [{
      "id": "meaning", "domain": "visual", "mode": "visual",
      "check": "The actual requested state is distinguishable at its consumer display size.",
      "basis": "The source brief's state-readability requirement",
      "scope": "This candidate at the declared display conditions",
      "sources": [{"path": "BRIEF.md", "locator": "State readability"}]
    }]
  }]
}
```

Supply every applicable mechanical, qualitative, temporal and destination check;
the example is a shape illustration, not a complete universal acceptance plan.
Do not manufacture a fixed palette or binary-alpha requirement to fill fields.

Scope required candidate checks to the stage being prepared. A representative
sample can establish a direction before dependent assets exist: assess its own
meaning, readability and relevant reference relationships now. Preserve later
family-wide distinction/consistency and renderer obligations in PLAR and the
request/criteria handoff, with their later review stage and prerequisites. Do not
attach a required check to this sample that can pass only after assets depending
on its acceptance have been produced. The caller checks that dependency order as
well as the requirement wording; deferral must not erase the final obligation.

When the caller's comparison is consistent, reread PLAR to ensure requirements are
unchanged, claim the existing durable dispatch and submit its exact arguments to
PixelLab. Record the actual provider response and continue normal retrieval/review.
Keep store/task/output links and next action in PLAR. Preparation uses the existing
sample phase; it does not approve a production family or supply missing reviews.

Read the selected asset's `production` result before deciding the next action. It
combines the allocation with actual store, output acceptance and pending provider
state. Carry its `continuation` in the result and use that immediate action for the
next step; future new requests retain its pending-resolution prerequisites. The operation links single-output work back into PLAR; verify `allocation`
in its response. A concurrent queue edit can leave a prepared job needing its link
repaired. Preserve that job and reread the queue. Multi-output work retains the
explicit current preparation task, so focused reads can resume it before a delivery
output is chosen. All planned outputs remain required. Later bind the actual
collective delivery output; do not label the first frame as the whole package.
Local dispatch advice does not establish provider authentication or availability.

An unchanged call resumes the same preparation. For a changed contract, refresh the
actual source bindings/requirements, retain a new exact packet and obtain the caller's
comparison. Resolve pending jobs using their originating connection before preparing
replacement work. A changed provider or a completed request-only assignment does not
terminate an existing submitted job. Preserve unknown outcomes until evidence resolves
them; never label a real pending request failed just to unlock a revision. Simulated
IDs remain on their controlled connection and cannot become upstream resources.

Then call the same operation with `revise: true` and `expect` from current production
state (CLI: `--revise --expect STATE_HASH`). It appends a candidate generation in the
same store, retaining the earlier plan, inputs, jobs, candidates and verdicts. The
returned task/output/job IDs are the current ones; never assume the first generation's
IDs after a revision. Review/retrieve against the appropriate generation. An interrupted
revision resumes with the same packet and current state hash. Acceptance from an earlier
plan is not inherited. Existing explicit low-level amendments and family/adoption
operations remain available when their broader scope is needed.

If an older store has several unlinked preparations, reread its jobs and resume the
exact intended prepared packet with `--revise --expect STATE_HASH`. Other pending
work must first be resolved. This publishes its preparation focus without creating
another job. An old terminal request cannot reclaim focus; malformed focus metadata
needs reconciliation rather than a guessed selection. Keep the original failure
and use a runtime supporting preparation focus for this recovery.

An isolated direct assignment can still use ordinary PIXL operations without creating
a repository-wide inventory. Neither route turns a sample into approved production.
