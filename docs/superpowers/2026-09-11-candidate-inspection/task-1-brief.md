## Task 1: Exact inspection views

Files: new `pixl/inspection_views.py`, `tests/test_inspection_views.py`.

Interface:

```python
def render(snapshots: dict[str, bytes], candidate_id: str, contract: dict, options: dict) -> dict:
    # Returns files: {relative_path: bytes}, views: [metadata], measurements: dict,
    # inputs: [metadata], options: canonical rendering options, context_observations: list.
    # Each input: {source, path, sha256}; each view: {path, source, frame, context,
    # scale, background, crop:[x,y,w,h], width, height, sha256}.
    # Contract values are plain JSON: px:[w,h], pl:[...], al:"binary"|"full".
    ...
```

- [ ] Write and run failing pixel tests for nearest/native, fractional alpha, full coverage crops, explicit frame timing/pivots and tile placement/seam observations.
- [ ] Implement limits and deterministic rendering with no state mutation or artistic verdict.
- [ ] Run `uv run --no-sync python -m unittest tests.test_inspection_views -v`; retain failures before fixes.
- [ ] Review interface, pixels and boundary cases independently.

