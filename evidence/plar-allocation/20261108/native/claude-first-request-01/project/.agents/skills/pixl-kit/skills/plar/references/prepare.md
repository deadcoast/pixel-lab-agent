# Prepare the selected asset's first request

Use this when a selected PLAR asset needs its first concrete candidate. Read the
selected source/dependency context and the actual PixelLab tool declaration first.
Choose an appropriate first operation and explicit candidate controls. Retain the
ordinary request/criteria packet and let the caller compare it with the original
sources through [request-review](../../pixl/references/request-review.md).

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

When the caller's comparison is consistent, reread PLAR to ensure requirements are
unchanged, claim the existing durable dispatch and submit its exact arguments to
PixelLab. Record the actual provider response and continue normal retrieval/review.
Keep store/task/output links and next action in PLAR. Preparation uses the existing
sample phase; it does not approve a production family or supply missing reviews.

An unchanged repeated call resumes the same preparation. A pending/unknown job
needs reconciliation, not another submission. A changed reviewed contract or an
existing different store needs explicit resumption/replanning through the existing
operations. Keep older contracts and work. An isolated direct assignment can still
use the ordinary PIXL workflow without creating a repository-wide inventory.
