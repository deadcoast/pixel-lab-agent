## Task 2: Saved packet and explicit review

Files: new `pixl/inspection.py`, `tests/test_inspection.py`,
`spec/candidate-inspection.md` (exact implemented artifact/request contract).

Interfaces:

```python
def prepare(folder, expected, candidate_id, packet_id, options, root=None): ...
def review(folder, expected, packet_id, review_id, observation, root=None): ...
def report(doc, root, packet_id=None): ...
```

- [ ] Preserve previous changed-file/runtime receipts under `evidence/candidate-inspection/previous/` with hashes.
- [ ] Write failing operation tests: prepare creates no verdict, stale state/source blocks, exact X file closure, review rejection with E/V, explicit supersession, partial/resized viewing, unavailable engine, cold relocation and candidate replacement.
- [ ] Implement immutable capture and expected-hash publication, using `graph.proof_scope`, `codec.record_hash`, `store.commit` and the renderer interface.
- [ ] Implement the design-review corrections: closed manifest/projection checks,
  original semantic record bodies, immutable per-operation packet IDs, readable
  historical drift, and stale-review rejection. Generic X semantics stay unchanged.
- [ ] Require closed envelopes and precise IDs/dates; retain declared limitations and next action in review X.
- [ ] Run `uv run --no-sync python -m unittest tests.test_inspection -v` and review state/retention boundaries independently.

