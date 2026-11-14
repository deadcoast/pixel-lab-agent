# Check evidence before relying on a release

Run the maintainer integrity check when choosing which existing result supports
a current capability or package. It reads the checkout, the declared bundle and
the retained evidence registry. It prints what is intact, what changed and the
next useful action. It creates no files, rebuilds nothing and invokes no tests,
native hosts, browsers or provider operations.

```powershell
.venv/Scripts/python.exe -B scripts/check_integrity.py
.venv/Scripts/python.exe -B scripts/check_integrity.py --json
```

Use `--claim ID` to inspect a named claim from the report; repeat it for several
claims. Package checks still run. `--root PATH` selects another checkout, and
`--manifest PATH` selects a registry relative to that root. The command remains
an inspection operation in every mode. Save stdout separately when retaining a
new audit; keep earlier results and use a fresh destination.

## Read the result

| Result | Meaning | Next action |
| --- | --- | --- |
| Intact, current bindings | Registered receipts and claim wording match; the declared tested inputs still match current files | Use the result within its recorded scope and evidence tier |
| Intact, historical | The original receipt is unchanged; its outcome belongs to the recorded source/package and assignment | Keep that result as historical evidence; qualify changed work separately |
| Stale current applicability | A source, package or inventory differs from the inputs recorded by a claim that is intended to apply now | Inspect the named paths and rerun the affected proof when current qualification is needed |
| Changed or missing evidence | A pinned receipt/artifact cannot be verified, or a recorded field differs | Recover the exact retained bytes or record the unresolved gap; preserve the original receipt |
| Changed claim wording | The anchored claim line differs from its reviewed registry binding | Review the new wording against its evidence before updating the registry |
| Invalid declaration | The registry, pointer, path or package structure is malformed or unsupported | Correct that declaration; the check does not guess its meaning |

Exit codes are **0** for intact current/historical checks, **1** when review is
needed, and **2** for invalid input. A recorded failed trial can have intact
evidence. It remains a failed trial. Source drift identifies a qualification gap;
it does not prove a runtime regression. A passing integrity check does not run
or repeat the checks inside a receipt.

<a id="integrity-full-verification"></a>The retained SC-06 full-verification result is a historical pass. Applying it to the current checkout requires its recorded source hashes and source inventory to match; later implementation or test changes retain the original pass while making current applicability stale.

<a id="integrity-claim-review"></a>The dated NF-04 capability review remains a historical review. Its original reviewed-source identities can be checked against today's documents, but unchanged receipt bytes do not establish that later claim wording was reviewed.

The default report can therefore need review even when the current bundle still
matches its canonical sources. Keep the full-suite result and newer focused
results separate. Do not regenerate old evidence, overwrite a failed receipt or
change an expected hash simply to obtain a zero exit code.

The [TM-10 qualification](../evidence/release-integrity/README.md) exercises the
actual checkout and isolated changed inputs. Its current declaration covers 15
claims and 54 receipts: two current setup/install claims, eleven historical
outcomes and two stale maintenance claims. The old full-suite and NF-04 reviews
retain their passing outcomes; current applicability needs review. The exact
retained sdist also has a changed README input. These are expected inspection
findings, preserved alongside the 65 passing focused tests, one Windows
privilege skip and ten successful CLI qualification cases.

## What is checked

The [claim registry](../evaluations/evidence-claims.json) connects selected
[core capability rows](CAPABILITY-OUTCOMES.md#core-tasks) and maintenance claims
to explicit retained receipts, exact outcome fields, tested sources and package
identities. Each claim names its scope, evidence tier and limitations. The
registry is reviewed metadata, not an automated interpretation of every sentence
or every advertised domain.

Receipt hashes and exact JSON-pointer assertions protect the registered
historical facts. Source/package bindings compare today's files with hashes
inside those pinned receipts. Whole-source inventory checks additionally detect
new files that an older hash map never tested. The checker follows only explicit
registered references; old Windows temporary paths and Linux `/tmp` execution
locators remain historical context.

Release checks use the same pure payload plan as the bundle builder. They
compare the expected file/source set, payload bytes, supplied-source inventory,
version and generated runtime requirements. This catches an internally
consistent but stale bundle, omitted manifest entries and new source files.
Selected retained wheel/sdist bytes are inspected in place, with no extraction,
installation or build. A package version or matching filename is never used as
a substitute for the exact archive digest.

This command is a maintainer operation. Consumers continue through
[setup and readiness](AGENT-KIT.md#set-up-a-consumer-project) and the
[declared support matrix](INSTALL-SUPPORT.md). Integrity does not establish
authentication, native instruction following, new art, visual quality or
target-engine acceptance. Human acceptance stays separate and unrecorded.

## Maintain the registry

Use a stable claim ID and a unique HTML anchor on the actual claim line. Bind
the line's UTF-8 bytes without its line ending, so unrelated documentation edits
do not invalidate that claim. An intentional wording change requires a review
of its scope before replacing that line binding.

Register exact repository-relative receipt/artifact paths and SHA-256 identities.
Select outcome/assertion fields with explicit JSON pointers. Derive current
source/package bindings from the tested hashes in those receipts; hashing today's
untested code does not create a tested-source binding. Preserve original failed
and partial outcomes alongside recovery evidence. Mark historical claims as
historical and keep their original package identity.

The version-1 registry rejects duplicate IDs/JSON keys, unknown fields, malformed
digests, unsupported versions, ambiguous bindings and paths that escape the
selected checkout. A current claim needs explicit tested-input bindings. Its
limits must continue to distinguish local mechanics, native behavior and actual
task outcomes. The checker reports its own source and registry identities so a
saved report can be tied to the exact inspection implementation.

The mutating [full verifier](VERIFICATION.md) remains a separate operation. Read
its side effects before running it. TM-10 integrity work does not close M1/M2 or
broader M3/M4/M5, and it does not require human approval to continue development.
