# Updated PLAR handoff

Refreshed `plar.txt` against the changed `BRIEF.md`, `src/queue.ts` and `src/queue-view.ts`. Preserved all four established asset IDs, existing evidence fields and useful requirements. Added `queue.paused`; the queue now has five rows.

| Asset ID | Current destination | Allocation |
| --- | --- | --- |
| `queue.ready` | `assets/ready.png` | Existing proposed representative sample; static 16x16. |
| `queue.working` | `assets/working.png` | Existing four-frame horizontal 64x16 strip; 100 ms per frame. |
| `queue.retry` | `assets/error-retry.png` | Same failure/retry purpose and stable ID; destination changed from `assets/retry.png`. |
| `queue.start` | `assets/start.svg` | Preserve existing vector unchanged; production remains deferred. |
| `queue.paused` | `assets/paused.png` | New static 16x16 status; distinguish from activity, completion and retry without color alone. |

Ready remains the proposed style sample. Working, Retry and Paused depend on its review. Pause bars are a proposal, not an imposed source requirement. Added family comparison checks for the Paused silhouette to the active status rows. No duplicate Retry asset or retired role was created: the failure purpose persists and only its consumer destination moved. Prior allocation history retains the superseded destination.

Coverage: re-read the full changed brief and both source files, then followed `pause -> paused` and the unchanged started/ok/error transitions into the shared map used by `statusCell` and `compactStatus`. All four PNG destinations are missing. The Start SVG and source map remain unchanged. Existing 16x16 cells, transparency, nearest filtering, 1x/3x inspection, cool blue direction, 100 ms Working timing and `#172336` panel remain in effect. Server-registry account badges remain outside scope and locally unenumerable. No consumer source was rewritten.

Actual checks: the initial PLAR read reported exactly three changed sources. After reconciliation, compare-and-swap save, full queue read, focused Paused read and focused Retry read all exited 0 with empty stderr. All five source bindings are current. Focused Paused and Retry reads include Ready's full dependency requirements. Verified stable prior IDs, unchanged prior row evidence/production links, unchanged raw consumer bytes during this refresh, and unchanged prior allocation artifacts.

The previous queue is preserved byte-for-byte at `.pixl/plar-history/6fab557dee66b7b6e2957514f63647acf3e15453fea8b30f8f16cabb4b3adbe3.json`. The original `HANDOFF.md` and `.pixl/allocation-*` artifacts remain untouched. Refresh evidence is in `.pixl/refresh-before-read.json`, `.pixl/refresh-inputs.json`, `.pixl/refresh-save.json`, `.pixl/refresh-read.json`, `.pixl/refresh-paused-read.json`, `.pixl/refresh-retry-read.json` and `.pixl/refresh-checks.json`.

Current queue hash: `3901a2e7cea7eea6bc616715c64962f665e93a2b0804bcf9dfd45a51f1d0ac56`.
Paused requirements hash: `f65a00d27b547b62c8f115fa7219574640699124b0f7f2422221881170fe6616`.
Retry requirements hash: `e4e52b68427c6df90006e3ac381ff9392b8201228af41e8f9c10bf6915c5cad9`.

Unresolved: no approved style reference or executable renderer/importer/runtime capture is supplied. No art was generated, no rendered UI or animation was tested, and no visual acceptance or engine integration is claimed. No tool failure occurred during this refresh.

Next action: when production is assigned, prepare and review the representative Ready sample at 1x and 3x nearest on the actual dark panel. Bind that approved reference before producing Working, Retry at its new destination, and Paused. Obtain the executable renderer to verify the actual paused/error transitions, frame behavior, compositing and non-color differentiation.
