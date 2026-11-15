# Continuation note, 2026-11-14

Project: scout and medic character family, side-view. Store: `production/state.px` (PX2). Queue: `plar.txt`, assets `character.scout`, `character.medic`, `character.family`. Brief with the owner's verbatim instruction: `brief/BRIEF.md`.

No generation provider is assigned in this evaluation session. Nothing was generated; no candidate exists. The sample task `sample_scout` is open and blocked on two owner choices.

## Decision table

| Choice | Authority / status | Answer needed now? | Effect of the answer |
| --- | --- | --- | --- |
| Family members: scout, medic | Confirmed (owner instruction, BRIEF.md line 7) | No | Fixed. |
| View: side | Confirmed (owner instruction) | No | Fixed; becomes C.vw=side. |
| Outline treatment | Conflict: reference.png = continuous 2px dark outline; reference-b.png = no outline | Yes | Sets the sample contract's edge treatment, the provider prompt and the outline criterion. Needed with canvas before the raster output can get a contract. |
| Canvas size | Unresolved (owner has not chosen; references are 32x32, observation only) | Yes | Sets C.px. A raster output plan needs a concrete C before its task can activate. |
| Color roles (teal body, cream eyes, dark outline where used) | Observed from references; PIXL proposes carrying the roles, not the exact hex | No | If the owner confirms a fixed palette, exact membership becomes a mechanical rule. Otherwise checked visually as roles. |
| Alpha: binary | Observed from references | No | If confirmed, becomes C.al=binary and a mechanical check. |
| Representative sample = scout first | Proposed by PIXL | No, unless the owner prefers the medic first | Orders the work; the medic is produced from the accepted scout baseline. |
| Medic role landmark | Unknown; PIXL proposes at least one visible landmark | Not before the scout sample | Needed when the medic stage is authored. |
| Destination (engine, paths, display scale, import settings) | Unresolved | Not for the sample; yes before delivery activation | Confirms the family's destination choices and enables the engine criterion. |
| Provider connection | Not assigned in this session | Before any generation | Enables request preparation and dispatch; outside the owner's art choices. |

An answer adopts only the rows it names. Unnamed rows keep their status.

## Visual observations (specialist, from work/outline-comparison.png)

Sheet: both references at 1x, 2x, 3x, 4x on a light, a dark and a busy two-tone background. Outlined version left, outline-free right in each pair.

- The continuous dark outline keeps the silhouette separated on all three backgrounds and at 1x.
- The outline-free version is clean on the light and dark backgrounds, but on the busy teal-green background the body edge loses separation because the body teal sits close to the background tones.
- The outline-free version reads slightly larger and softer because the body fill reaches the silhouette edge; the outlined version loses about 2px of body on each side to the line.
- These are observations about these two 32x32 files on these three test backgrounds. They do not decide the owner's aesthetic, and a different game background could change the balance.

Specialist recommendation, not a decision: if the game draws characters over varied or textured backdrops, the continuous dark outline is the safer readability choice. If backdrops are flat and high-contrast, the outline-free treatment is viable and gives more body per pixel. A selective outline (dark line only where the body meets low-contrast areas) is a third option not present in the references and would need an owner adoption plus a sample trial.

On canvas: without a display scale or tile metric there is no basis to recommend a size. The reference body occupies about 19x26 of the 32x32 cell. At 1x that is small for a side-view character with equipment landmarks (scout vs medic); larger canvases give room for a role landmark but the choice depends on the game's scale.

## Knowledge consulted

- `silhouette-readability` (library method): inspect identity landmarks at native scale on representative light, dark and busy backgrounds. Applied as the diagnostic above; its multi-background procedure is an expert proposal, not an owner rule.
- `edge-rhythm` (library method): audit contour runs without imposing one contour style. Relevant once a sample exists; not yet applied.

## State saved this session

- `production/state.px` revision 1: sources (brief, both references), intake choices with their statuses as in the table, sample task `sample_scout` with planned output `scout_sample` (sprite, no contract yet), criteria for the sample, the comparison sheet as a report artifact, and a handoff record.
- `plar.txt`: three rows with requirements, authority labels, references and the production link for the scout.

## Next local operation, once the two answers arrive

1. Add a C record to `production/state.px` with `px` = chosen canvas, `vw=side`, the chosen outline treatment linked through `ch` to the outline and canvas choices, update those I records to confirmed with the owner's instruction retained as a source line, set `scout_sample.ct`, and commit with the current state hash.
2. If a PixelLab connection is assigned, discover its tool schema, then use `pixl_plar_prepare` for `character.scout` with a request packet carrying both references as style inputs and the confirmed outline instruction.
3. After the scout candidate is reviewed and accepted, author the medic stage and family delivery with `pixl_production_plan` using the accepted scout candidate as baseline.
