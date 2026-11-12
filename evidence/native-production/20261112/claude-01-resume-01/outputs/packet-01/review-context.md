# Packet 01 review context — CF-10 robot.directions

Specialist: pixl:pixl (this session). Written 2026-11-12 before any paid dispatch.
Everything here is for the caller's independent comparison; nothing in it is owner
approval. Exact artifacts and hashes are listed in `request-review.json`.

## Delivered scope (whole assignment)

| File | Role | Origin |
| --- | --- | --- |
| assets/robot/south.png | controller `south` | exact copy of assets/robot-base.png, sha256 d997cade…70aa7 (already written, `cmp` identical) |
| assets/robot/east.png | controller `east` | to be generated: east view from the rotation job |
| assets/robot/north.png | controller `north` | to be generated: north (back) view |
| assets/robot/west.png | controller `west` | to be generated: west view |

Extra views the tool returns (SE, NE, NW, SW) are retained under
`work/native-production/` and are not delivered. South is never regenerated for
counts; the provider's own south output is kept only as lineage evidence.

Delivery is a PX2 family: baseline = the preserved south candidate (sample task),
members = south, east, north, west, destinations = the four controller paths with
nearest sampling in a 32x32 cell, collective criteria in `family-plan-draft.json`
(continuity, direction mapping, renderer mechanical check, renderer visual check).

## Source image, measured (assets/robot-base.png, 32x32 RGBA)

- 390 visible pixels, one 4-connected opaque component, 0 fractional-alpha pixels.
- Visible bbox `[7,3,25,28)` zero-based, right/bottom exclusive: 18 px wide, 25 px tall,
  last opaque row 27, horizontal centre 16.0 (pixel-edge coordinates).
- Colours: `#25354a` navy frame + two 4x6 antenna posts at columns 7–10 and 21–24,
  rows 3–8 (180 px); `#56b5bc` teal body panel (186 px, box `[9,11,23,26)`);
  `#f4dda2` two 3x4 eyes at `[11,14,14,18)` and `[18,14,21,18)` (24 px).
- Viewed at 1x and 8x (work/native-production/inspect/robot-base-3x.png, -8x.png):
  a strictly frontal, flat, unshaded box robot; no top face, no limbs, no outline
  gradient. ASCII map retained in this session's transcript; reproduce with Pillow.

## Provider image input (how the exact bytes reach the provider)

`get_upload_url` → `curl -F file=@assets/robot-base.png <signed url>` →
reply `{"ref":"upload:57ceb659-b047-49e5-9250-58343f194c5f","width":32,"height":32,"n_frames":1,"expires_in_days":3}`
(raw reply: `work/native-production/upload-response.raw.json`, observed 2026-11-12T08:09:03Z).
The ref goes in `first_frame_url`. The signed URL itself is not retained in any artifact.
Nothing in the text prompt is relied on to carry the image.

## Operation choice

`create_object_pro_flash` (host MCP declaration transcribed into `connection.json`):
- `first_frame_url = upload:57ceb659-…`, `first_frame_direction = south`, `n_directions = 8`,
  `view = side`, `seed = 0`, `name`, `description` (literal description of the observed pixels).
  No width/height/style/palette: the tool docs say to omit size/style when reusing a
  first frame; the 32x32 source is already a native square size, and the capabilities
  report says eight views use the square V3 canvas (32x32 here).
- Cost discovered 2026-11-12T08:08:04Z: `get_pro_flash_capabilities(object,32,32,8)` →
  image 5 + rotations 1 = 6 provisional; tool description: "Reusing a first frame bills
  only the rotation part". Expected charge: **1 generation** (provisional until the receipt).
- Why not `create_character` v3 + reference (also 1 generation, keeps south as drawn):
  its full reference says v3 "assumes a standing humanoid or four-legged animal and
  tends to add limbs" to other bodies; this robot is a limbless box. It is fallback #1
  if the object rotation fails identity. Pro rotate (10 generations) is fallback #3.
  `create_8_direction_object` pads 32→34 px and costs 10; rejected.
- Output cardinality: one object with 8 directions; only E/N/W are delivered.

## Criteria (candidate-plan.json), per generated output

dims, alpha_transparent, palette_preserved, identity, proportions_volume, direction,
anchor_alignment are owner/consumer requirements with file-local line locators.
alpha_binary, ground_line_measure are explicitly scoped specialist proposals.
The exact-set reading of "preserve palette" is flagged as the specialist's
interpretation (choices.palette_exact_set) for the caller to keep or relax.

South baseline criteria: `south-baseline-plan.json` (bytes identical; identity).
Family criteria: `family-plan-draft.json`.

## State plan (fresh store .pixl/assets/robot.directions)

1. `pixl_plar_prepare(robot.directions, requirements_hash de02…bddd0, packet, connection)`
   → sample task `task` with outputs `output.east|north|west`, reference input
   `reference.0` (robot-base.png), durable job prepared (no dispatch). Multi-output →
   `needs_output_link`; the PLAR link is written later to the family delivery output.
2. Caller comparison → corrections in a new packet version if needed (old kept).
3. Confirm the contract choices in state (sources: brief/consumer + COMPARISON.json for
   the specialist proposals the caller adopts), then `pixl_job_dispatch` → one official
   `create_object_pro_flash` call → `pixl_job_observe` with the returned object id →
   `get_object` polling → ZIP download → `pixl_job_import` of the exact east/north/west
   bytes → asset checks + 1x/3x/8x viewing → `pixl_candidate_review` (nominate) →
   `pixl_task_complete` for the sample task.
4. Commit the south baseline sample task (reused bytes) and review/complete it.
5. Decision D adopting the proven method (proof receipt bound to the sample evidence),
   `pixl_production_plan` with three production stages (east/north/west, reusing the
   accepted sample bytes as explicitly labelled reused candidates, no second paid call)
   and the family delivery; copy accepted bytes to assets/robot/*.png; run the renderer
   capture/check; `pixl_family_snapshot`; family review with renderer evidence;
   `pixl_task_complete` for the delivery only if every criterion passes.
6. PLAR update (production link to the delivery task/output, status, evidence),
   `pixl_plar_handoff view=caller`, `get_balance`, SPECIALIST-RESULT.json.

Budget: 20 generations; this plan spends 1 unless a revision is required. A revision
(new seed, or fallback tool) is a new job after the first attempt is reconciled.
