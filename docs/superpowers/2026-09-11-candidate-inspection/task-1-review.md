# Task 1 independent renderer review

Status: changes required. Read-only implementation review; no provider/model calls, generated bundle writes, or commits.

Reviewed `AGENTS.md`, the candidate-inspection design and Task 1 report, `pixl/inspection_views.py`, `tests/test_inspection_views.py`, and existing `pixl/assets.py` measurements.

## Findings

1. **P1 — Aggregate decoded-pixel budget is enforced after allocation** (`pixl/inspection_views.py:233`, `:787-790`). `_decode` converts and retains every frame before `render` checks their aggregate pixels. A small compressed animation can therefore allocate up to 1,024 maximum-sized RGBA frames instead of respecting the documented 67,108,864-pixel budget. Pass the remaining aggregate budget into decoding and reject before converting each frame. Safe reproduction: patch `MAX_DECODED_PIXELS=2`, render a 3-frame 2x1 GIF, and spy on `Image.Image.convert`; all three RGBA conversions occur before the final `inspection_limit`. Existing `assets.inspect` checks cumulative pixels before converting each frame.

2. **P1 — Measurement structures make the accepted pixel ceiling impractical** (`pixl/inspection_views.py:262-296`). Measurements simultaneously materialize an RGBA tuple list, a coordinate tuple set, and the copied set inside `assets.components`. This uses much more memory than the raster budget suggests. A local `tracemalloc` probe of `_measurement` on an opaque solid 512x512 PNG measured 86,286,643 bytes peak for a 1,048,576-byte RGBA raster. A simple linear extrapolation to the accepted 4096x4096 frame is approximately 5.14 GiB of Python allocations; this is an estimate, not a full-size executed probe. Retained decoded frames and outputs add further memory. Use a bounded raster-based measurement implementation with equivalent facts, or document and enforce a practical measurement ceiling before materializing these structures. Preserve empty-palette, nonzero-alpha, four-connectivity, and fractional-alpha semantics.

3. **P2 — Comparison strip dimensions are validated after allocation** (`pixl/inspection_views.py:476`, `:483`, `:566-574`). `_frame_strip` allocates and composites the complete strip before its axis/pixel limits are checked. It can therefore exceed the advertised derived-context allocation limit before raising. Calculate and validate strip geometry first, including common-pivot expansion. Safe reproduction: patch `MAX_SOURCE_SIDE=2`; source 2x1, three copies of `[0,0,2,1]`, null durations/pivots. A spy records `Image.new` allocation `(6,1)` before the context-limit rejection.

4. **P2 — Raw frame-comparison and tile-context views lose exact transparent RGB** (`pixl/inspection_views.py:478-489`, `:672-674`). Alpha compositing into a transparent blank canvas rewrites fully transparent source RGB to zero. A source containing `(123,45,67,0)` and `(12,34,56,128)` preserves both in the normal raw view and individual frame raw view, but comparison and neighborhood raw views return `(0,0,0,0)` for the first pixel. This violates exact RGBA placement and makes the emitted neighborhood differ from the pixels used by edge measurements. Use unmasked copies for these nonoverlapping placements; reserve compositing for explicitly selected backgrounds. Add transparent nonzero-RGB tests to both context paths.

## Verification and remaining assessment

`uv run --no-sync python -m unittest tests.test_inspection_views -v`: 12/12 passed. Those tests do not cover the failures above. The three tiny allocation/pixel probes and the 512x512 measurement probe completed successfully in the selected uv environment.

Ordinary image cropping and integer-nearest replication, explicit frame selectors, ordered input retention, duration/pivot nulls, and candidate/reference measurement policy match the inspected design. The measurement vocabulary matches `assets.inspect`; no live execution or artistic acceptance was inferred. Re-review is required after fixes.

## Re-review after implementation fixes

**Gate: PASS for Task 1; Task 2 may proceed.** All four original findings above are resolved in the re-reviewed source. Their original descriptions and pre-fix evidence remain intact.

- Aggregate decoding now receives the remaining global pixel budget and checks each frame before RGBA conversion. The regression observes only the first permitted conversion.
- Measurements use packed color integers and row-based four-connected component labels rather than per-pixel tuples and coordinate sets. The explicit 65,536 visible-color ceiling rejects excess distinct colors instead of truncating observations; both the module docstring and task report document it. The independent 512x512 solid-image probe now peaks at **2,364,562 Python-traced bytes**, compared with **86,286,643** before. This measures Python allocations, not total process/Pillow native memory; no full-limit stress run is claimed.
- Both common-pivot and top-left comparison paths validate derived geometry before allocating the strip.
- Exact unmasked paste preserves all four channels in frame comparisons and tile neighborhoods, including hidden RGB at alpha zero. Declared backgrounds still composite explicitly.

Fresh independent verification:

1. `uv run --no-sync python -m unittest tests.test_inspection_views -v`: **18/18 passed**, including the added decode, color-limit, topology, strip-allocation, and transparent-RGB regressions.
2. Exhaustive comparison of `_components` against `assets.components` for **all 65,536 binary 4x4 alpha masks**: exact match.
3. **150 deterministic random RGBA images** (seed 91026, dimensions 1..17, alpha values 0/1/127/255, unrestricted or explicit palette, binary/full policy, and passing/failing dimensions): complete `_measurement` result objects exactly matched `assets.inspect` on temporary PNG files.
4. Additional direct common-pivot probes preserved `(123,45,67,0)` and `(12,34,56,128)` and rejected oversized common-pivot geometry before any `Image.new` allocation.

No remaining blocking findings within this renderer review scope. This gate covers local rendering and measurement behavior only; state publication, actual host viewing, model profile behavior, provider execution, and engine acceptance remain separate work.
