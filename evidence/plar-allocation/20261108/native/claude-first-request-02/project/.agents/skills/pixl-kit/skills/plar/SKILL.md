---
name: plar
description: Map a project's code, UI states and references to pixel-art asset requirements; create or update plar.txt and hand a selected asset to PIXL for production.
---

PLAR (Pixel Lab Asset Requirements) turns project context into a usable asset work list. Work in the **consumer project's root**, not this skill's installation. The result is `plar.txt`: ordinary JSON with stable asset IDs, source bindings, consumer locations, requirements, destinations and next actions. It describes what is needed; PIXL's PX2 store retains production jobs, candidates and acceptance evidence.

## Understand and allocate

Read the project's instructions and available source overview/index/MOC, then verify its pointers against the relevant entry points. If no useful overview exists, retain a focused map of the consumers and backend transitions you actually inspect. If it already has `plar.txt`, read the queue and refresh affected rows. Use CodeGraph first when the project has a `.codegraph/` index; otherwise use the host's code tools. Follow actual UI/renderer consumers through imports, manifests, loaders and backend state transitions. Group shared visual roles into one asset with multiple consumers. A function without an image does not automatically need one.

Inspect existing art and the visible UI when available. Distinguish missing files, placeholders, reusable assets, visual mismatches and intentionally procedural/text-only elements. Note dynamic paths or unavailable modules in coverage.unresolved. Scope claims to the code and runtime actually inspected; a filename search is not exhaustive coverage.

For each visual role, connect:
- Purpose and visible states to file/symbol/usage locations.
- Applicable canvas/frame geometry, projection, reference style, edge/alpha policy, timing, pivots, tile rules and import behavior to their sources.
- The output destination, checks at the actual display size, dependencies, unresolved choices and one concrete next action.

Preserve explicit requirements, observations, proposals and unknowns separately. Use only relevant properties; do not invent a palette, alpha ban or resolution to fill a template. Record user instructions in a small project brief file when they are not already addressable. References convey style; measurements of them do not automatically become rejection rules. When visual input is required, add source-bound references with an explicit role (style, identity, pose, layout, palette, mask or motion) and instructions stating what to preserve.

## Save and use

Read [the format and operations](references/format.md) when creating or editing the work list. `pixl_plar_save` validates the supplied document, binds new local sources and retains previous versions using an expected hash. `pixl_plar_read` returns queue summaries; pass `asset_id` for the complete selected row and its source/dependency context. Focused reads also return transitive dependency requirements/issues, actual source hashes, absolute project paths and visual references. Pass the requirements_hash to a delegate; it changes with relevant requirements or source bytes, not unrelated queue progress. The portable CLI provides the same operations. Ordinary file editing is also supported; re-read and validate afterward.

For refresh, read the queue before editing. Its changes report identifies drift and transitive dependents; after a save, or with `plar read --since PRIOR_HASH`, it compares authored requirements against retained history. Treat file-level impact as a prompt to inspect affected consumers, not proof every asset needs regeneration. Check the source overview and changed entry points for newly introduced consumers that no prior row could mention. Preserve unchanged requirements and existing IDs; distinguish a moved destination from a new visual role.

A useful row can remain actionable with open questions. Resolve consequential unknowns for the selected action from the project, references or user; continue independent assets. Preserve stable IDs on refresh, retain superseded work as deferred with a reason, and inspect changed sources before deliberately updating their hashes. Update the queue after production and integration, linking retained evidence rather than copying provider job history.

## Hand off to production

For an asset request, continue through [PIXL](../pixl/SKILL.md) once the selected row is understood. A complete existing brief can go directly to production without a repository-wide scan. Give a delegated specialist the absolute project root, this skill/PIXL locations, PLAR path and asset ID, current user constraints and authorization, available references, and expected files/checks. Do not assume the child has the parent's conversation. Use the [shared delegation contract](../pixl/references/delegation.md) for caller questions and results.

PIXL uses the authenticated **official PixelLab API**, through its exposed MCP tools or the supported HTTP adapter, for paid generation within the user's authorized work. Discover the actual operation schema and carry the selected requirements into its arguments. Existing authorization persists; ask only for a missing consequential choice or scope expansion. Development test settings belong to their harness and do not define production policy.

For the first concrete candidate, use [selected-asset preparation](references/prepare.md): one local operation translates the reviewed contract into the existing PX2 plan and prepares its first durable request. Continue normal dispatch, retrieval and review through the host's actual PixelLab connection. Link its returned store/task/output IDs from the PLAR row. `pixl_commit` accepts inline JSON, so a host need not encode and write a temporary wire file. Keep provider execution, returned bytes, visual judgment and engine integration distinct. Return actual delivered paths, review findings, integration status and the updated next action. An `integrated` label in PLAR is a caller claim, not runtime certification.
