# Agent-to-agent handoff evidence — 2026-11-07

This increment makes PIXL's visual expertise callable with complete requirements and explicit image-reference roles. It extends the selected PLAR packet and the shared profile/workflows; it does not introduce another orchestration service.

## Runtime and distribution

[Full verification](../verification-runs/20261107T221438.176103Z/result.json): 421 tests executed, **420 passed**, one Windows symlink-privilege skip; **39/39** reference checks passed. Source-distribution → wheel → temporary installation passed, including the new dependency-reference handoff. Copied-plugin relocation exercises the same operation.

[Validation summary](20261107/validation.json) also records 14 focused PLAR tests, four final relocation/packaging tests, Ruff, Mypy, six skill validators, template parsing, bundle hashes and link checks. Later documentation/adapter polish was separately checked; the runtime implementation did not change after the full run.

Claude's native plugin validator caught an unquoted colon in an updated agent description. The [failed attempt](20261107/claude-validation-before-fix.json) is retained; quoting the descriptions fixed the error and validation passed. Its separate catalog checks still identify absent license/listing-icon metadata; this work does not certify marketplace submission.

## Fresh specialist behavior

The independent agent received [this assignment](20261107/forward/prompt.txt), a copied kit, raw consumer files and [the selected packet](20261107/forward/assignment.json). The [frozen input inventory](20261107/forward/input-manifest.json) binds 155 files. The task asked for a four-direction production plan using an existing identity; it did not supply the intended tool selection or correction.

The [returned caller result](20261107/forward/consumer/planning/caller-result.json), [plan](20261107/forward/consumer/planning/production-plan.md) and [input mapping](20261107/forward/consumer/planning/provider-input-mapping.json) show that the specialist:

- Recovered the identity reference from the selected asset's dependency and inspected the actual source.
- Chose the connected `create_character` v3 reference route with four directions.
- Prepared the exact PNG bytes in `reference_image_base64`, rather than substituting a filename in prose.
- Preserved native dimensions, mapped outputs by controller direction name and planned to keep south byte-identical.
- Kept the camera interpretation, unseen geometry and unavailable engine checks explicit.

The [parent review](20261107/forward/review.json) independently checked input preservation, returned hashes, requirements identity, exact base64 round trip and output mapping, and opened the plan/request and inspection image. **The bounded planning assignment passed.** It establishes source-to-request handoff behavior, not provider acceptance or generated-art quality. Earlier [native Claude/Codex delivery trials](../delegated-asset-request/README.md) remain separate under their original instruction snapshots.

The copied consumer retains its original paths and an inspection composite; these are reference/test artifacts, not new production art.

## Official platform discovery

[Live discovery](20261107/live-discovery.json) preserves the tool declarations inspected and a read-only Pro Flash capability response, including the initially rejected operation enum and corrected request. Capability limits and provisional pricing describe that response, not permanent platform policy.

The operating sources are the [official platform documentation](https://www.pixellab.ai/docs), [MCP tool guide](https://api.pixellab.ai/mcp/docs), and declarations exposed by the authenticated host. Credential values are absent from this evidence and the connection templates.

See the [A–E development review](../../docs/AGENT-HANDOFF-REVIEW.md) for the design decisions and responsibility boundaries.
