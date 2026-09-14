# PixelLab surface discovery in this session

Recorded 2026-09-11 by PIXL, before any attempt to prepare or dispatch a provider request.

## What was actually inspected

1. **The harness tool surface exposed to the agent in this session.** The only MCP server
   connected is `pixl-local`, which provides `pixl_asset_check`, `pixl_capabilities`,
   `pixl_catalog`, `pixl_commit`, `pixl_context`, `pixl_encode`, `pixl_family`,
   `pixl_family_snapshot`, `pixl_impact`, `pixl_init`, `pixl_intake`, `pixl_job`,
   `pixl_job_dispatch`, `pixl_job_import`, `pixl_job_observe`, `pixl_job_prepare`,
   `pixl_jobs`, `pixl_knowledge`, `pixl_prepare`, `pixl_ready`, `pixl_source`,
   `pixl_sources`, `pixl_validate` and `pixl_workflow`. That server's own instructions
   state: "All tools are local. PixelLab must be connected separately."
2. **The environment.** No environment variable whose name contains `PIXEL` is set in the
   shell available to this session, so no PixelLab credential is exposed here either.

## Result

**No PixelLab tool is callable in this session.** There is no `create_character`,
`create_image_pixflux`, `create_image_pixen`, `create_image_pro`, `image_to_pixelart`,
`get_image`, `get_character`, `get_balance` or any other PixelLab endpoint in the harness
tool list, and no authenticated PixelLab MCP server is configured. The session instructions
also forbid changing host settings, so connecting one is out of scope for this agent.

Consequently no generation request can be submitted, and no real remote job identifier,
job state or returned asset can exist for this project yet.

## What `pixl_capabilities` is and is not

`sources/pixellab-capabilities-snapshot.json` is the runtime's bundled documentation
inventory, retrieved by its author from <https://api.pixellab.ai/mcp/docs> and stamped
`retrieved_at: 2026-09-11T05:58:46.820240Z`. It reports `"live_discovery": false` in its own
payload. It lists 100 documented tool names with their required-argument names and polling
tool, for example:

- `create_character` (generate, requires `description`, polled with `get_character`)
- `create_image_pixflux` / `create_image_pixen` / `create_image_pro` (generate, require
  `description`, polled with `get_image`)
- `image_to_pixelart` (generate, polled with `get_image`)

This is dated local documentation. It is **not** live discovery, **not** a full input
schema, **not** proof that any of these tools exist in their documented form today, and
**not** evidence of an account, credit balance or entitlement. PIXL's durable
`job-prepare` operation requires the exact schema observed from the connected provider, so
this snapshot cannot be used in its place: doing so would save a fabricated request.

## Precise missing capability

An authenticated PixelLab MCP server connected to this harness, exposing at minimum a
generation tool that accepts a textual description plus a 32x32 output size and a style
reference image, and its matching polling and download tools. Until that exists, the sample
task `t.sample` stays blocked at its generation step; every local plan, contract, criterion
and mechanical tool in this project is already in place to evaluate the returned PNG.
