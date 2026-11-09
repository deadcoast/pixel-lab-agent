# Queue UI consumer example

This small source fixture represents an external project using PLA. It is not an application shipped by the agent repository. Start from `BRIEF.md` and `src/queue-view.ts`, then follow the backend states and asset loader. `plar.txt` is a worked requirements inventory, not generated art or runtime acceptance.

Use the installed plugin runner from any directory with `plar read --root /ABS/THIS/DIRECTORY --asset queue.working`. The three missing PNGs are intentional production TODOs. The existing SVG is an intentional hybrid UI control, not a request to replace every vector with pixel art. Runtime-loaded account badges cannot be exhaustively allocated from this checkout.

## Run the actual consumer

With Node supporting `node:module.stripTypeScriptTypes` (verified here on 25.8.1), run
`node renderer/server.mjs` and open the printed loopback URL. The browser imports
these actual backend/view modules, renders both full and compact status consumers,
and uses their dimensions, frame count/timing, nearest sampling and panel color.
The renderer also works with later retained consumers:
`node renderer/server.mjs --project ABSOLUTE_CONSUMER_ROOT`.

For a fresh retained browser capture, run
`node renderer/capture.mjs --project ABSOLUTE_CONSUMER_ROOT --out NEW_DIRECTORY`.
It uses a locally installed Chrome/Edge, or an explicit `--browser PATH`, with its
own temporary profile. The output includes the destination screenshot, decoded
canvas views, clicked-event mappings, frame-boundary observations, source/image
hashes and browser identity. Existing output directories are never overwritten.
On restricted Windows sandboxes, the browser may require the host's ordinary
process permission; a failed browser launch is retained and is not a render pass.

Missing images stay missing, and wrong sheet sizes are visible errors. These
captures establish behavior of this representative browser consumer, not an
unseen application or another engine. Pixel-art/style judgment, full family
continuity and upstream generation provenance remain separately reviewed.
