# PixelLab platform research and execution constraints

Research date: **2026-09-10, America/Vancouver**. Retrieval timestamp: **2026-09-11T05:58:46.820240Z**. Research used public documentation GET requests only; no account credentials, billable endpoints, generated assets, or actual generation jobs were used.

The deliverable is a documentation-derived inventory of **100 MCP tools and 454 parameters**, not a claim that a particular agent session has those tools connected. [The catalog](../../knowledge/pixellab-capabilities.json) preserves every documented tool name, unconditional required field, parameter annotation, default when published, and parameter description. Its `type` values are normalized JSON types; `source_type` retains the upstream Python annotation. `nullable` and `enum` are separate. A named nested type remains a named type when its complete MCP schema was not publicly published. Conditional requirements are in descriptions and notes, rather than incorrectly added to unconditional `required` arrays.

## Evidence and source authority

| Source | What it establishes | Authority and limitation |
|---|---|---|
| [PixelLab MCP tools guide](https://api.pixellab.ai/mcp/docs) | Current tool names, annotations, defaults, mode behavior, workflow notes, resources | Auto-generated from FastMCP definitions; primary source for this catalog. Live connected `tools/list` remains the authority for an actual call. |
| [PixelLab general documentation](https://www.pixellab.ai/docs) | Product interfaces and artistic workflows | Explicitly acknowledges documentation lag. Editor labels and examples are not MCP signatures. |
| [PixelLab MCP landing page](https://www.pixellab.ai/mcp) | Remote HTTP MCP setup and product overview | Some sample argument names and persistence statements conflict with the tool guide. |
| [REST v1 docs](https://api.pixellab.ai/v1/docs), [v1 OpenAPI](https://api.pixellab.ai/v1/openapi.json) | Legacy REST request and response models | The docs HTML loads this OpenAPI URL. Eight distinct paths were observed. MCP guide calls v1 deprecated. |
| [REST v2 index](https://api.pixellab.ai/v2/llms.txt), [v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json) | Current REST families and precise REST schemas | 86 distinct paths were observed. REST schemas describe REST, not interchangeable MCP arguments or response envelopes. |

The original [links file](../../training/original-docs/PIXEL-LAB-LINKS.md) is preserved. Its v1 authentication fragment is not needed to resolve the current docs. The complete MCP response body is stored unchanged in [pixellab-mcp.txt](snapshots/pixellab-mcp.txt): **100,688 bytes**, SHA-256 **`e9f1b7e541f37a80db0ea81dbc20d9af8c30002dead890dac6e006b8a07f580f`**. The document itself ends with a generated timestamp of `2026-09-10 21:35`; that upstream timestamp is not the local UTC retrieval timestamp. Whitespace or line-ending edits change the snapshot hash.

**WHO:** PixelLab defines remote capabilities; the connected MCP server advertises callable schemas; PIXL records intent, validates requests, retains evidence, and evaluates delivered pixels. **WHAT:** this inventory separates generation, reads, updates, and deletion while retaining mode-specific requirements. **WHERE:** source definitions remain in the immutable snapshot; machine-readable lookup is in `knowledge/pixellab-capabilities.json`; real calls must use an available PixelLab MCP tool. **WHY:** landing-page examples, editor workflows, REST versions, and live MCP schemas differ. Treating them as a single interface causes invalid calls, unexpected spend, and misleading completion claims.

Execution precedence is: actual connected tool identity and `inputSchema`, its current tool description and returned constraints, the dated MCP snapshot, then secondary examples. A stale catalog may reject a new feature until refreshed; it must not invent support. If the actual schema conflicts with the asset contract, stop the dependent call and report the conflict. Do not silently drop an unsupported constraint merely to obtain a valid request. The generic catalog is not itself a complete executable JSON Schema.

## Complete MCP surface

The following grouping covers all 100 names; every field and published default is in the catalog. Categories and `effect` labels are local planning classifications, not server permissions, billing guarantees, or statements of implemented adapters.

| Family | Documented tools |
|---|---|
| Characters | `create_character`, `create_character_state`, `animate_character`, `get_character`, `list_characters`, `delete_character`, `update_character_tags` |
| Top-down terrain | `create_topdown_tileset`, `get_topdown_tileset`, `list_topdown_tilesets`, `delete_topdown_tileset` |
| Sidescroller terrain | `create_sidescroller_tileset`, `get_sidescroller_tileset`, `list_sidescroller_tilesets`, `delete_sidescroller_tileset` |
| Isometric tiles | `create_isometric_tile`, `get_isometric_tile`, `list_isometric_tiles`, `delete_isometric_tile` |
| Objects and variants | `create_map_object`, `get_map_object`, `create_1_direction_object`, `create_8_direction_object`, `get_object`, `list_objects`, `animate_object`, `create_object_state`, `delete_object`, `update_object_tags`, `select_object_frames`, `dismiss_review` |
| Map placements | `place_map_object`, `list_map_objects`, `move_map_object`, `remove_map_object` |
| Conversations | `chat_list_conversations`, `chat_get_messages`, `chat_send_message` |
| Remote sandbox | `sandbox_create_session`, `sandbox_destroy_session`, `sandbox_bash`, `sandbox_run`, `sandbox_read`, `sandbox_write`, `sandbox_edit`, `sandbox_sync`, `sandbox_deploy_worker`, `sandbox_undeploy`, `sandbox_playtest`, `sandbox_read_image` |
| Project and animation management | `add_to_project`, `delete_animation`, `list_projects` |
| UI | `create_ui_asset`, `get_ui_asset`, `list_ui_assets`, `delete_ui_asset` |
| Connected tile kits | `create_tiles_pro`, `create_path_tiles`, `create_building_kit`, `get_tiles_pro`, `list_tiles_pro`, `delete_tiles_pro` |
| Portrait and dialogue | `create_portrait_character`, `get_portrait_character`, `set_character_portrait`, `create_vocal_animation`, `get_vocal_animation`, `create_talking_gif`, `get_lip_sync` |
| Fonts | `create_font`, `get_font` |
| Raw images | `create_image_pixflux`, `create_image_pixen`, `create_image_pro`, `get_image`, `edit_image`, `edit_image_pixen`, `image_to_pixelart`, `unzoom_image`, `correct_pixelart`, `reduce_colors`, `inpaint_image`, `animate_image`, `animate_image_pixminimax` |
| Maps | `create_map`, `delete_map`, `list_maps`, `get_map`, `edit_map`, `view_map` |
| Assistance, deployed agents, account, jobs | `agent_help`, `agent_feedback`, `agent_list`, `agent_inspect`, `agent_talk`, `get_balance`, `search_knowledge`, `cancel_job`, `list_jobs` |

The remote sandbox and chat families are broader than pixel-art generation: they can execute code, send messages, delegate work, mutate projects, or publish a deployment. Inventorying them does not authorize those actions. `sandbox_bash`, `sandbox_run`, `chat_send_message`, and `agent_talk` may produce effects beyond a coarse `update` label. Likewise, `read` does not mean free: some reads invoke a model, and `get_map_object` documents retrying storage persistence. [MCP tool definitions](https://api.pixellab.ai/mcp/docs)

## Character, object, and animation contracts

| Request family | Required operational distinctions |
|---|---|
| Character standard | Four or eight directions, maximum 128 pixels, effective default size 48. Quadrupeds require one of `bear`, `cat`, `dog`, `horse`, `lion`. Humanoid proportions are a JSON **string**, not an object. Oblique is beta, standard only, four directions only, maximum 128. |
| Character pro | Always eight directions, maximum 128. Ignores `n_directions`, `outline`, `shading`, `detail`, `text_guidance_scale`, `proportions`. `style_character_id` must be a completed eight-direction character whose sprite content fits the requested size. |
| Character v3 | Always eight directions, maximum 256. Only this character mode accepts an input south-facing sprite. URL and base64 alternatives are exclusive. A reference determines identity and style; omitted size preserves reference dimensions and a supplied size is advisory. It ignores shading, proportions, and text guidance; reference rotation also ignores outline/detail hints. |
| Character state | Returns a new character ID. Preserve source and variant identity separately. Larger width/height overrides must be paired, multiples of four, and at least the source dimensions. Source auto-wait is bounded at 30 seconds. |
| One-direction object | `style_images` is required, even when `[]`. Effective size 16–256, default 64 without references. Nonempty references exclude explicit size; the largest reference sets it. Candidate counts: size ≤42 gives 64; ≤85 gives 16; ≤170 gives 4; larger gives 1. Multiple candidates require review. |
| Eight-direction object | Explicit size 24–168, default 64. Size excludes reference/style image arguments; those two images exclude each other. Existing object style references require completed eight-direction assets and sufficient canvas. Use character v3 for rotating humanoid character references. |
| Character animation | Presence of a template ID selects template mode unless explicitly overridden; otherwise custom v3 is the default. Template mode defaults to all character directions, custom mode to south. V3 requests even 4–16 generated frames. Character pro ignores requested frame count: canvas ≤64 yields 16, larger yields 4. |
| Object animation | Requires completed source. Never pass `directions` to a one-direction object. For eight-direction objects a new animation defaults to all directions; an existing group defaults to missing directions. Object pro limits differ from character pro: ≤64 only 16 frames; ≤128 allows 4/9/16; ≤170 only 9; larger unsupported. |

V3 character/object animation retains the reference as frame zero by default: eight requested generated frames usually means **nine stored frames**. `keep_first_frame=false` requests only generated frames. Preserve both requested and actual counts. Custom start/end poses require v3, one known direction, a maximum 256×256 start, and a matching end canvas. Where the user has not established directional intent, resolve it before using a custom pose; an arbitrary south-facing assumption changes the requested motion. Character URL pose fields are documented; equivalent object URL fields are **not** advertised in this snapshot. [MCP guide](https://api.pixellab.ai/mcp/docs)

Appending character directions needs the existing `animation_group_id` **and** its current `animation_name`; the name is not inherited. Object groups inherit their animation description when extending. Retrying an entire partially accepted multi-direction request risks generating duplicate work. Inspect actual landed directions and group identity first. Candidate promotion via `select_object_frames` produces new completed object IDs; `dismiss_review` destroys candidates and cannot serve as a successful quality decision. Tags replace the complete set, with at most 20 tags of 50 characters each. [MCP guide](https://api.pixellab.ai/mcp/docs)

## Images, references, masks, and interface assets

Reference roles are distinct: identity, style, pose, palette, and composition cannot be collapsed into a generic image slot. Keep a local record of the source bytes and their hash, dimensions, alpha, permission to send them, and the intended role. Prefer supported HTTPS URL fields for images larger than tiny sprites because the MCP guide repeatedly reports truncated inline base64. Some raw-image and portrait URL fields explicitly also accept `data:` URLs; character reference URLs specify HTTPS. Do not generalize data-URL support across fields, invent absent URL parameters, place filesystem paths in remote image fields, or fabricate encoded image bytes. Use a URL **or** base64 for the same input, never both. A data URL still carries the entire payload and does not solve model-context size. [MCP guide](https://api.pixellab.ai/mcp/docs)

| Tool | Constraint that changes planning or validation |
|---|---|
| `create_image_pixflux` | Each axis is at least 16 and total area is at least 1,024 pixels: 16×16 fails, 16×64 can fit. Init image matches output dimensions. `init_image_strength` preserves more content as it increases; MCP default is 150. Palette image supplies forced colors. |
| `create_image_pixen` | Dimensions are multiples of four. If either side is below 32, the image must be square. No general maximum should be invented from another tool. |
| `create_image_pro` | Up to four labelled references, each with its intended `usage`. Aspect-dependent limits include 512×512 square and 688×384 widescreen. Returns candidates. |
| `edit_image` | One or more inputs up to 512×512; use URL list or base64 list. A description or reference supplies the edit. Default alpha handling follows the inputs. |
| `edit_image_pixen` | Description length 1–500, input at most 256 per side, output area at most 65,536 pixels. Output is re-rendered at the new size; this is not deterministic scaling. |
| `image_to_pixelart` | Default output is one quarter of the source dimensions. Preserve aspect. Faithful mode with strength around 100–300 is documented; excessive strength can preserve the source without a meaningful conversion. |
| `correct_pixelart`, `reduce_colors` | Frame dimensions must agree. Quantization target count and supplied palette are exclusive; a supplied palette has at most 256 colors. Cleanup and quantization require their own pixel review. |
| `inpaint_image` | Input 32×32 through 512×512. Supply one complete rectangle or one full-size mask. White regenerates; black preserves. Independently compare all unmasked pixels after download. |
| `animate_image` | Start image required, maximum 256×256; optional matching end image. Frames are even; large canvases may impose additional limits. Do not assume its storage behavior matches character animation. |
| `animate_image_pixminimax` | Subscription tier two or higher, frames 4–40 in multiples of four, maximum 256×256. Default transparency removes an opaque backdrop. Optional prompt enhancement is extra work and returns changed text. |
| `create_ui_asset` | Minimum published axis size 192. Aspect-gated maxima: 512×512, 688×384, 384×688, 600×448, 448×600. A 688×512 combination is invalid. Shape coordinates use a virtual canvas whose long side is 512, not output-pixel coordinates. |

`create_map_object.background_image`, `inpainting`, character `proportions`, and tiles `style_options` are documented JSON strings. In contrast, pro image `reference_images`, object `style_images`, and UI `pieces` are arrays. The general editor tutorial uses a painted inpainting layer; its description of painting black is **not** the MCP binary-mask convention. The MCP `inpaint_image` and map-object custom mask explicitly use white to regenerate and black to preserve. [MCP guide](https://api.pixellab.ai/mcp/docs), [editor inpainting tutorial](https://www.pixellab.ai/docs/getting-started)

Portrait generation, attaching a portrait, generating mouth positions, and assembling dialogue are separate calls. Portrait-only vocal jobs can feed talking GIFs for eight hours; a stored character supplies persistent spritesheet identity for `get_lip_sync`. Talking GIF timing rounds to 10 ms steps and reports the actual delay. These tools do not establish synthesized voice audio. Font generation records glyph resolution from 8/16/32/64, weight, and job identity; a generated font still needs glyph and export inspection. [MCP guide](https://api.pixellab.ai/mcp/docs)

## Tile topology and import contract

Top-down standard terrain supports square 16/32 tiles. Pro terrain supports 16/32/64 and its own `spread_x`, `slope_size`, `raggedness` controls; it rejects `shape_style`. Standard `shape_style` supports continuous transition width 0–1; otherwise the documented transition values are 0, 0.25, 0.5, and 1. Values beyond 0.5 with shape geometry use an extended 4×8 sheet. At transition size 1.0 the classic result has **25 occupied tiles**, with wall cells beneath the terrain boundary. Four wall tiles have the same corner pattern as another tile. Consequently, `corners` alone is insufficient: import and choose by **`pattern_4x4`** and retain returned source positions. A 4×8 sheet is not proof of 32 usable terrain tiles. [MCP guide](https://api.pixellab.ai/mcp/docs)

REST `Tile` metadata corroborates `id`, `name`, `image`, `corners`, `pattern_4x4`, and `original_position`. Its `connections` field is deprecated and null for newly generated top-down sets. An importer should retain the actual metadata and asset pixels, detect unrecognized schemas, and reject missing placement coverage instead of inventing an atlas order or mapping. [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json)

Connected terrain is an ID graph. Chaining uses actual returned base-tile IDs; equal descriptions do not prove shared terrain identity. A map seed attaches connected sets with matching tile size and shared base IDs. Each terrain pair that touches still needs its **own** transition set. Missing pair coverage produces black cells and is reported by `view_map`. Map edit and placement coordinates are terrain cells, may be negative, and are not pixel offsets. `create_map` without `project_id` does not synchronize the map to a game project. [MCP guide](https://api.pixellab.ai/mcp/docs)

Sidescroller terrain is a separate transparent 16-configuration family with square 16/32 tiles. General pro tiles also differ: independent hex, pointed hex, isometric, octagon, angled square, or supported oblique shapes do not automatically become terrain sets. Explicit terrain sets contain 16 corner configurations for isometric/square/oblique, or 32 coastline configurations for hex shapes. Pro reference tiles define dimensions and shape, overriding shape controls, and cannot combine with a connected terrain feature. [MCP guide](https://api.pixellab.ai/mcp/docs)

`create_path_tiles` produces 18 path configurations: square top-down requires exactly 32 pixels; isometric accepts 48–96, so choosing isometric while leaving the global default 32 is insufficient. `create_building_kit` accepts isometric 32–96 or square/oblique 16–96, with one to three wall tiles of height. Floor, walls, upper floor, shear, and camera elevation have distinct effects. Consume the returned placement rules; a path junction, a terrain corner, and a building doorway do not share one universal bitmask. [MCP guide](https://api.pixellab.ai/mcp/docs)

The MCP guide advertises resources for Python and Godot Wang/sidescroller imports, Godot isometric tiles, and Unity 2D isometric maps. Read the corresponding `pixellab://docs/...` resource through an available MCP host before writing an engine-specific importer. Their contents were not available through this unauthenticated documentation research. Their advertised existence is not verification of a local converter. Required import evidence should include native dimensions, atlas coordinates, frame timing, pivot/origin, alpha handling, filtering, and representative terrain adjacency or animation playback in the actual target engine.

## Jobs, spend, retries, and truthful evidence

The following are **PIXL implementation decisions inferred from the documented asynchronous and paid behavior**, not undocumented server guarantees:

1. Before transmission, durably record intent ID, asset contract/version, tool identity, actual schema hash, canonical argument hash, reference hashes, and authorized budget scope. Keep credentials and opaque image payloads out of readable logs.
2. Submit once, then store the real server response, resource ID, every returned job ID, and animation group/direction associations before polling. Resource IDs, job IDs, and group IDs are distinct. A local request fingerprint is not server idempotency.
3. A transport timeout, disconnect, or malformed response leaves acceptance **unknown**. Do not automatically replay a paid generation. Reconcile via known resource IDs and `list_jobs(include_recent=true)` where useful; its recent history only covers 30 minutes and is not a durable ledger.
4. Poll the tool appropriate to the returned identity. `get_character` and `get_object` use resource IDs; raw images, fonts, portraits, and vocal jobs use job IDs. Preserve pending, processing, review, completed, failed, canceled, and unknown observations without fabricating progress. Completion of character rotations does not prove requested animations completed.
5. Honor a documented cost-quote response separately from job acceptance. Pro character/object animation explicitly requires the first call with `confirm_cost=false`, presenting the returned cost, then explicit user confirmation before `true`. A generic budget allowance must not be presented as a confirmation that the service specifically asks the user to make after the quote.
6. Estimate from the chosen family and mode, then use current returned cost or account evidence when available. Character pro, raw-image pro, states, and UI can cost 20–40 generations; standard top-down tiles are usually three or four, not one. `reduce_colors` and `unzoom_image` are documented as 0.1, despite fast processing. These are dated estimates, never live quotes.
7. After genuine completion, download actual returned URLs, check decode, dimensions, hashes, expected directions/frames/tile coverage, and inspect pixels at native scale and integer zoom. Associate every quality judgment with inspected artifact hashes and concrete observations. Neither a successful API response nor an illustrative local fixture is a passed quality review.
8. Save failures and rejected candidates as evidence. A new attempt after a confirmed failure is a new budgeted revision, not a silent retry. `cancel_job` does not promise a refund. Deletion and candidate dismissal need their own intended scope and must not masquerade as cleanup of a successful asset.

The MCP guide identifies download UUIDs as access keys and describes downloads without authentication. Use returned URLs and preserve their identity; do not place real private asset links in public documentation merely because a URL works without a token. This repository contains no live download links. `chat_send_message` is a documented exception to the broadly asynchronous workflow: it can block for up to ten minutes. [MCP guide](https://api.pixellab.ai/mcp/docs)

`poll_tool` in the catalog is a workflow hint. Three family mappings are explicitly inferred rather than directly named in their individual tool paragraphs: `create_path_tiles` → `get_tiles_pro`, `create_building_kit` → `get_tiles_pro`, and `animate_image_pixminimax` → `get_image`. Confirm returned IDs and live guidance for these before treating them as executable routes. A missing tool is a connection/capability limitation; do not silently switch to guessed HTTP requests.

## Cross-interface discrepancies and decisions

| Observation | Decision |
|---|---|
| MCP landing samples use `animation`, `lower`, `upper`, and `transition`; generated tool docs use `template_animation_id`, `lower_description`, `upper_description`, `transition_description`. | Preserve upstream examples as historical context; compile only advertised fields. |
| Landing says map objects expire after eight hours; current `get_map_object` says permanent. | Record the conflict. Use current runtime status and tool documentation; apply the eight-hour rule only where currently specified, such as standalone vocal-job reuse. |
| MCP raw-image `create_image_pixflux` is asynchronous with `get_image(job_id)`; v2 `/create-image-pixflux` returns `image` plus optional `usage` synchronously. | Do not derive transport or polling from a similar name. REST endpoints must be implemented and verified individually if a future adapter is explicitly added. |
| REST v1 route is `/generate-image-pixflux`; REST v2 is `/create-image-pixflux`; MCP name is `create_image_pixflux`. REST takes `image_size`; MCP exposes width/height. | No mechanical underscore-to-hyphen endpoint synthesis. |
| V2 pixflux default `init_image_strength` is 300; the MCP wrapper default is 150. | Apply the default of the selected interface; keep omission distinct from explicit null. |
| REST pro tile `tile_feature` admits `roads`, `tileset`, `building`; the MCP generic tool admits only `tileset`, exposing separate path/building calls. | Never smuggle a REST enum value or its building-prefixed arguments into an MCP call. |
| REST top-down tiles expose reference images and seed beyond the current MCP signature. | Research coverage is not local or MCP support. Offer only capabilities actually advertised by the selected interface. |
| Some generated doc summaries are visibly truncated; named nested schemas are not expanded. | Retain the exact snapshot, record unknown details, and validate the actual runtime schema rather than reconstructing missing prose. |

Sources for these discrepancies: [MCP tool guide](https://api.pixellab.ai/mcp/docs), [MCP landing page](https://www.pixellab.ai/mcp), [REST v1 OpenAPI](https://api.pixellab.ai/v1/openapi.json), [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json). The v2 index separately marks older endpoint families as legacy without announcing their removal; that is different from the MCP guide's v1 deprecation statement. [REST v2 index](https://api.pixellab.ai/v2/llms.txt)

## Verification boundary

The local catalog was checked against every `####` tool heading and every parameter definition in the preserved snapshot: 100 unique names, 454 matching fields, all unconditional required sets matched, and all non-null poll tools name an inventoried tool. The snapshot hash and size were checked after writing the catalog. No runtime MCP schema, account balance, quoted cost, generation success, engine import, or output quality was verified in this research task. Those are intentionally explicit remaining evidence boundaries, not invented passing results.
