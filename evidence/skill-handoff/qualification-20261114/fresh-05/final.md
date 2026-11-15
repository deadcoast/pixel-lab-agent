The project is started and saved. Nothing was generated, because no PixelLab provider is assigned in this session. The scout sample task is blocked on two choices only you can make, so this ends with a question for you.

**What I found in the references.** Both files are 32x32 with the same silhouette, teal body and cream eyes. reference.png adds a continuous 2px dark outline around the whole body. reference-b.png has no outline, so the teal reaches the silhouette edge. That is the whole disagreement.

**What is saved in the consumer project**

- `brief/BRIEF.md` retains your instruction verbatim, the reference measurements marked as observations, and my proposals marked as proposals.
- `production/state.px` is a PX2 store at revision 1. It holds the sources, eight intake choices with their true status (members and side view confirmed, outline in conflict, canvas and destination unresolved, color roles and binary alpha observed, scout-first sample proposed), the open sample task with its planned scout output, and four acceptance criteria. The output has no contract yet, so the workflow correctly reports the task blocked.
- `plar.txt` has three rows: scout (linked to the sample task), medic (depends on the accepted scout), and the family delivery. Next action reads "review_contract".
- `work/outline-comparison.png` shows both treatments at 1x to 4x on light, dark and busy backgrounds.
- `notes/continuation-2026-11-14.md` holds the decision table and the next local operation. A caller handoff is retained under `.pixl/handoffs/`.

**Visual observation from the sheet, scoped to these two files.** The outlined version keeps its edge on all three backgrounds. The outline-free version is clean on flat light and dark backgrounds but loses separation on the busy teal-green one, and it reads slightly larger. My recommendation, not a decision: choose the dark outline if your game draws characters over textured backdrops, and the outline-free treatment if backdrops are flat and contrasty. A selective outline is a third option not in the references and would need your adoption plus a sample trial.

**Two answers I need from you**

1. Outline treatment: continuous dark outline (reference.png), no outline (reference-b.png), or something else?
2. Canvas size for the characters. The references are 32x32, where the body fills about 19x26 pixels. That is one candidate, not a default. If you tell me the display scale or tile size, I can recommend one.

Those two answers let me record them as confirmed choices, write the contract on the scout output, and unblock the sample task. Generation still needs a PixelLab connection assigned to this project. The destination engine, paths and display scale are not needed yet, but they will block family delivery later.
