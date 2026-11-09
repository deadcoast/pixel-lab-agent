# Keep library sources usable across kit updates

Use this operation when a project has imported knowledge/proof S records from a PixelLab-agent kit. It keeps the exact source revisions that the project already declared. The runtime does not require a copied library for a simple direct asset brief.

After saving the imported source records, call `pixl_retain_library` with the store, its current `expect` hash and the project-relative kit directory. Through the CLI:

```text
python /ABS/KIT/scripts/pixl.py retain-library /ABS/PROJECT/.pixl .agents/skills/pixl-kit --expect STATE_HASH --root /ABS/PROJECT
```

The kit name above is an example; use the actual source locator. The operation selects S records under that kit's `resources/`, verifies their bytes against their declared digests and the kit manifest, and retains them in the consumer project. State revision, record hashes, receipts and acceptance remain unchanged. Keep the project-owned .pixl/library-sources directory with the project when moving or backing it up.

After the kit changes, ordinary `validate`, `workflow`, `jobs`, `family` and `inspection` reports identify any `retained_sources` used. Read their expected/current identities and actual retained paths. Those sources establish the old declared revision; they do not prove the new implementation or new art.

For exact text retrieval, `pixl_source` in project scope resolves the same retained source. CLI callers can use `source ORIGINAL_RELATIVE_PATH --root PROJECT --expect ORIGINAL_HASH --start N --end N`, or the returned absolute retained path with the ordinary source command. Current-library discovery/retrieval still describes the currently installed kit.

## Recover a project already affected

If normal resumption reports a changed library S source and the project did not retain it yet, locate the original kit from the project's preserved evidence/archive. Keep that copy inside the consumer project and pass its relative location as `from_library` / `--from-library`. The `library` argument stays the old locator used by the project; the additional argument identifies the donor containing the exact expected bytes.

```text
python /ABS/CURRENT/KIT/scripts/pixl.py retain-library /ABS/PROJECT/.pixl .agents/skills/pixl-kit --from-library recovery/original-kit --expect STATE_HASH --root /ABS/PROJECT
```

Then reread workflow and the selected context. The current kit stays installed; original receipts and project state stay intact. If the original bytes are unavailable or do not match, report the named source and expected identity, preserve the failure and continue unaffected work. Do not restamp old evidence or overwrite the current kit with old files.

Retained revisions are useful for understanding and resumption. Adopting a different source, changed implementation, new aesthetic claim or new candidate still needs the existing source/decision/review process. Working artifacts and receipt files remain at their declared project paths.

See the [retention contract](../../../resources/spec/library-retention.md) for exact resolution and integrity rules.
