# NF-07 public package consumption

You are a cold calling agent integrating the delivered package in this directory.
Read deliverable-index.json. The index, immutable manifest and exact files, and the
index's cited integration sources are your only production inputs. The renderer
guide describes the supplied sprite-animation-v1 browser consumer. No PIXL state,
PLAR, installed PIXL runtime or prior handoff is supplied. Do not fetch those from
elsewhere or inspect the repository, provider credentials, global settings or memory.
Work within this consumer only. This is an isolated evaluation, not a sandbox claim.

Use the index's names, paths and declared integration choices/source files to:
1. Verify exact manifest and package identities. Distinguish the immutable creation
   acceptance from the index's observed current review; the index is a snapshot.
2. Copy the selected exact package bytes to the declared named destinations. Find
   the cited authored animation module, verify its identity, and place its unchanged
   bytes at the module path declared by the integration choice. Do not reconstruct
   missing metadata or infer an animation from manifest order/numbered filenames.
3. Author config.json from the supplied consumer guide and indexed choices. Preserve
   the authored layout, timing, pivots, sampling and other module decisions. Run the
   actual isolated browser capture and independent Python checker. Write capture to
   work/capture-01 and checker output to work/check-01.json. Keep failures if a fresh
   retry is needed; choose a new suffix and retain all preceding outputs.
4. Write CALLER-RESULT.json with status, index {path,sha256}, manifest {path,sha256},
   assets [{output,candidate,path,sha256,bytes}] for the named integrated destinations,
   module {path,sha256}, config {path,sha256}, capture {path,sha256} for capture.json,
   check {path,sha256}, creation_accepted, observed_current_eligible, unresolved,
   provenance_summary and limits. Record actual results, not a self-certified pass.

Only deliverable-index.json and its referenced public files may establish production facts.
Keep initial inputs byte-for-byte unchanged. New files may be named consumer assets,
the exact consumer module, config.json, work/* and CALLER-RESULT.json. Do not generate
art, call providers, install dependencies, mutate acceptance, or delegate this small
consumer task. Human artistic acceptance and other engines remain separate.
Selected Python: C:/github/pixel-lab-agent/.venv/Scripts/python.exe
Node and an installed Chromium browser are available through normal renderer discovery.
