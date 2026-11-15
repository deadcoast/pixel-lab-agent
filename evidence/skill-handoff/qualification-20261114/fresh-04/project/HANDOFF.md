# Handoff: side-view character family (scout, medic)

Session 2026-11-15, local-only PIXL evaluation. No generation provider was used. No art was generated.

## Where things are

| Item | Path |
| --- | --- |
| Owner instruction | `BRIEF.md` |
| Requirements queue | `plar.txt` (rows `characters.scout`, `characters.medic`, `characters.family`) |
| Production state | `production/characters/state.px` (PX2 revision 1) |
| Saved caller handoff | `.pixl/handoffs/7152c5c248387c907d86cb55254caef86cbc2350e7b0e5180db6d04155726f80.json` |
| Decision card | `research/outline-and-canvas-decision-card.md` |
| Comparison sheet | `research/outline-comparison-sheet.png` |
| Scratch scripts | `work/` (safe to delete) |

Reference images and `pixl-kit/` are unchanged.

## Status

The scout representative sample task (`t_sample`) is blocked on `output_contract`: it cannot get a concrete raster contract until the owner decides two things.

1. Outline treatment: continuous dark outline (`reference.png`), no outline (`reference-b.png`), or PIXL's proposed 1 px outline adaptation.
2. Canvas size per member: PIXL proposes 32x32, alternative 48x48.

Also unassigned: delivery destination / engine / display scale, and a PixelLab connection.

## How to resume

1. `pixl_workflow` on `production/characters/state.px`, then `pixl_plar_read` with `asset_id: characters.scout`.
2. Record the owner's two answers: set intake choices `edge_treatment` and `px` (canvas) to `confirmed` with `BRIEF.md` updated as their source, add a concrete `C` contract to `f_scout_sample`, commit revision 2 with the current state hash.
3. When a PixelLab connection exists, discover the actual tool schema, write the request/criteria packet and call `pixl_plar_prepare` for `characters.scout`.
4. After the sample is reviewed and accepted, use `pixl_production_plan` to bind the medic member and the family delivery with destination choices and the continuity criterion `q_role_distinction`.
