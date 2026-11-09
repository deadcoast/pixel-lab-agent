# Retained library sources

This operation preserves the exact library-source revisions referenced by a project across kit replacement. It is an explicit project-local source-resolution facility, version 1; it adds no PIXL record fields, changes no record hashes and does not migrate PX1 to PX2.

## Contract

`retain-library` / `pixl_retain_library` takes a store, its expected canonical hash, and the project-relative kit location referenced by its S records. It selects only local S records inside that kit's `resources/` directory. Their bytes must match both the S digest and the supplied bundle manifest. An optional `from_library` identifies a preserved older kit inside the project when the original installation has already changed.

The operation preflights the selected bytes, retains them under `.pixl/library-sources/objects/<sha256>`, and publishes immutable locator/digest entries under `refs/`. It also retains the original bundle manifest. It does not change the state revision, source locators, receipts, verdicts, tasks or remote jobs. Repeated calls reuse verified existing objects. A stale store hash, missing original bytes, corrupt entry or mismatched provider kit is an error; no digest is recomputed to fit changed input.

Local S validation first checks the declared location. If its bytes are missing or changed, an explicitly retained locator/digest entry can resolve the exact declared revision. The retained object is hash-checked on every use, and the original line range is checked against those bytes. No older revision can satisfy a newly requested digest. Artifact X and evidence E file checks remain at their original paths; their working/delivery files are never silently replaced by a historical copy.

Validation/workflow/job/family/inspection reports identify any retained source used, its actual path, original locator, expected identity and current-locator identity. Source retrieval in project scope can read that same retained revision. Library discovery continues to describe the currently installed library; it does not consult project retention.

## Meaning and limits

A valid old receipt remains evidence about the same old source records and bytes. It is not proof that the updated implementation behaves identically, that a method applies to a new project, or that a new candidate passed review. Changing a source record still invalidates dependent evidence under the existing record-hash rules. Retaining sources supplies no new verdict or completion.

This is for imported library knowledge/proof sources. This resolver does not silently substitute historical consumer files or generated artifacts. The separate selected-asset preparation adapter explicitly binds retained input snapshots and checks current PLAR identity before new dispatch; PLAR continues to report current source drift independently.

If an older project was already affected, supply its original kit (or a complete verified retained source set); the latest kit cannot reconstruct lost original bytes. Without those bytes, the diagnostic identifies the affected S record and expected digest, and dependent work remains unresolved. Never overwrite the installed kit with old receipts.

## Verification

Exercise an original project under a newer runtime, retain its sources, replace the kit, and resume with identical project/record/receipt hashes. Also exercise explicit recovery from the original kit after replacement, missing/corrupt originals, changed requested identities, stale writers, path confinement, current-library discovery, and installed-plugin use. Inspect the returned provenance rather than treating process exit alone as acceptance.
