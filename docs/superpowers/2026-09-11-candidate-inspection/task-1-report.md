# Task 1 report: exact inspection views

## Scope

Implemented the rendering-only candidate inspection boundary in
`pixl/inspection_views.py` and its focused pixel and validation tests in
`tests/test_inspection_views.py`. The module accepts caller-captured source bytes
and caller-assigned source IDs. It returns bytes and metadata without publishing
state, assigning semantic IDs, recording acceptance, or issuing artistic verdicts.

No existing `pixl.assets.inspect` behavior was changed. The renderer reports the
same factual measurement vocabulary for in-memory snapshots: candidate dimensions,
palette, and alpha are checked against the supplied contract; references are
measured as observations without adding candidate restrictions. Every measurement
keeps `visual_quality_verified` and `engine_import_verified` false.

## Interface and deterministic output

`render(snapshots, candidate_id, contract, options)` returns exactly:

- `files`: exact original encoded inputs plus deterministic PNG view bytes;
- `views`: path, source, decoded frame, context tag, integer scale, declared
  background, complete logical crop, delivered dimensions, and byte hash;
- `measurements`: one existing-style factual measurement object per source;
- `inputs`: source, retained relative path, and original-byte hash, ordered as the
  candidate followed by explicit references;
- `options`: a detached canonical copy with lowercase hex backgrounds and explicit
  defaults for `max_side` and `contexts`;
- `context_observations`: supplied context facts plus pivot alignment or exact
  neighboring tile-edge difference counts.

Input files use `inputs/NNNN.ext`. Derived views use `views/NNNN.png`. Normal and
context images retain an alpha-preserving native PNG (`background: null`) and a
native plus requested integer-nearest view for each declared background. A
checkerboard is fixed at 8 logical pixels with `#c0c0c0` and `#808080`; solid
backgrounds use exact `#RRGGBB` values. Fractional alpha is composed before nearest
enlargement.

Large outputs are divided into a complete row-major set of logical-pixel crops
before enlargement. Crop origins remain in source coordinates for normal decoded
frames and individual declared frame rectangles. Comparison strips and tile
neighborhoods use their own logical coordinates.

## Context behavior

Every frame and tile context has a required explicit `source_frame`. It must select
an existing zero-based decoded frame, including when the input has only one frame.

Frame contexts require closed, equal-length `rects`, `durations_ms`, and `pivots`
arrays. Rectangles are positive and fully contained. Durations are positive
integers or null. Pivots are local in-bounds integer coordinates or null. Each
declared frame is retained separately. The comparison strip aligns frames in
uniform common-pivot cells only when every pivot is supplied; otherwise it keeps
the nulls and uses top-left sequential placement. Timing is retained as an
observation and is not manufactured into an animation.

Tile contexts require a closed schema, an exactly dividing tile size, a nonempty
rectangular grid, and valid zero-based row-major indices. The declared neighborhood
is placed exactly. Each horizontal and vertical adjacency records the number of
differing RGBA edge pixels. These counts have no pass/fail field.

## Validation and fixed limits

Contract, options, frame-context, and tile-context objects are closed. JSON integer
positions reject booleans and floats. References, backgrounds, and context names
must be distinct where applicable. Snapshots must contain exactly the candidate
and explicitly requested references as nonempty bytes.

The module docstring records all fixed caps. The principal limits are 64 MiB per
input, 256 MiB input aggregate, 16,384 pixels per decoded axis, 16,777,216 pixels
per frame, 1,024 frames per input, 67,108,864 decoded pixels total, 65,536 exact
visible RGBA colors per measured frame, 4,096 returned views, 2,048 pixels per
delivered axis, 64 MiB per encoded view, 512 MiB for all returned files, and
134,217,728 rendered pixels. Context counts, frame rectangles, and tile placements
are also bounded. The function raises `PixlError` and returns nothing when a bound
is exceeded; publication remains a caller responsibility. Visible color counts are
never truncated: the 65,537th distinct visible color rejects the request.

## Test-first evidence

The required first run failed because `pixl.inspection_views` did not exist. Its
exact command, exit code, and traceback are retained in
`evidence/candidate-inspection/task-1-red.txt`. Production code was added after that
failure. Five independent-review regression failures were separately retained in
`evidence/candidate-inspection/task-1-review-red.txt` before their fixes.

The focused suite covers:

- exact RGBA preservation and fractional-alpha composition;
- native and integer-nearest pixel replication;
- full crop coverage before enlargement and delivered-side bounds;
- candidate-first input ordering and exact original bytes;
- all decoded animation frames without truncation;
- explicit frame selection, timing, pivots, common-pivot alignment, and null pivot
  preservation;
- exact tile placement and factual adjacent-edge difference counts;
- closed schemas, strict JSON types, invalid geometry, invalid frame selectors, and
  rendering limit rejection;
- deterministic declared checkerboard output.

The review regressions additionally prove that the aggregate decode budget rejects
before converting the next frame, distinct visible colors are counted exactly up
to the documented ceiling, four-connected topology remains exact, oversized frame
strips reject before allocation, and frame/tile context placement preserves hidden
RGB in fully transparent pixels.

A separate 65 by 65 maximum-scale probe produced 289 scale-16 crops. Their logical
crop areas summed to all 4,225 source pixels, every delivered side was at most the
requested 64 pixels, and all 297 emitted view paths were unique.

Independent re-review passed after the regression fixes. It exhaustively compared
all 65,536 binary 4 by 4 alpha masks with `assets.components`, and 150 seeded random
RGBA measurement objects with `assets.inspect`; both comparisons matched exactly.
Its 512 by 512 solid-image probe measured 2,364,562 bytes of peak Python-traced
allocation after the bounded rewrite, compared with 86,286,643 bytes before. This
tracks Python allocations, not Pillow native memory, and is not a full-limit stress
claim. Common-pivot allocation and hidden-RGB probes also passed. The retained
review now marks Task 1 passed with no remaining blocking renderer findings.

## Verification

Focused unit behavior, Ruff checks and formatting, and Mypy for the new module were
run with the existing uv environment. The complete final output is retained in
`evidence/candidate-inspection/task-1-final.txt`. The command receipts were:

```text
uv run --no-sync python -m unittest tests.test_inspection_views -v
Ran 18 tests ... OK

uv run --no-sync ruff check pixl/inspection_views.py tests/test_inspection_views.py
All checks passed!

uv run --no-sync ruff format --check pixl/inspection_views.py tests/test_inspection_views.py
2 files already formatted

uv run --no-sync mypy pixl/inspection_views.py
Success: no issues found in 1 source file
```

This exercises the local rendering and recorded pixel-behavior level. It does not
exercise profile discovery, state publication, a live PixelLab provider, visual
art review, browser/device scaling, or target-engine import. Those remain separate
operation and acceptance layers.
