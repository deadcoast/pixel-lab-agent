# PX-EVAL-004 — delegated PixelLab integration in both hosts

**Status:** selected next milestone, 2026-11-05; implementation and host trials pending.

**Product outcome:** Claude or Codex delegates an asset-generation request to PIXL.
PIXL uses the official PixelLab integration to submit the request, observe the job,
retrieve and inspect its output, and return usable asset files to the caller.

**Test boundary:** exercise that same workflow with the external provider calls
mocked. No real generation requests, PixelLab credits or provider network access
are part of the tests. Retained images are mock response payloads, not a replacement
for the production integration or a shortcut around its generation-request path.
This planning change does not launch model benchmark sessions.

The milestone should reveal which existing mechanisms help production, which need
a simpler interface, and which can remain optional reference infrastructure. Keep
existing knowledge, runtime work, assets and evidence. The maintainer develops and
reviews the tests; PIXL operates inside the identified host trials.

## Production path and test substitution

Keep production wired to the official PixelLab surface supported by the host.
Identify that surface and its actual request/response contract before authoring
fixtures; do not interchange HTTP endpoint schemas and MCP tool schemas by guesswork.
The existing local PIXL state server remains responsible for state and evidence.

Substitute only the outward provider boundary in tests: the host tool dispatcher
or the adapter's HTTP transport, as applicable. Request construction, dispatch
intent, response parsing, job handling, artifact retrieval/import, inspection and
delivery remain the real workflow under test. A separate offline shortcut that
merely copies an image to the output directory does not satisfy this milestone.

Mock responses must follow the selected official operation's documented schema.
Use test identities and clearly label observations as simulated; a fixture is not
proof of a live schema, authenticated access or service success. If a required
schema is unavailable, record the gap rather than invent compatibility. Configure
the trial to expose only the intercepted provider route, with no credentials or
fallback to real provider calls, and check that unexpected outward calls fail.

## Matched delegated request

Use one developer-authored test brief, reference set, expected output and fixture
response sequence in both hosts. The brief describes the asset to generate; it
does not instruct PIXL to find and deliver an existing asset. Its requirements are
local test conditions, not new universal pixel-art rules or assumed user choices.
No user generation budget is needed for this mocked test.

Existing images from the [retained PixelLab material](../training/pixel-art-assets/pixellab)
may supply fixture payloads after inspecting their bytes and available provenance.
Preserve originals. Missing historical metadata stays missing; test response IDs
must not be presented as historical or newly returned live provider identities.

Each host uses a separate project and the same frozen PIXL package. The parent
receives the brief and delegates it to PIXL through the installed host's actual
specialist mechanism. Both know this is a test with mocked external calls. Preserve
parent and specialist identities, invocation, loaded instructions and return.
Directly starting PIXL or loading its skill only in the parent does not demonstrate
that delegation. Verify the specialist can reach the intercepted provider tools.

## Exercise the full workflow

1. The parent assigns the generation brief, references and output requirements.
2. PIXL inspects references, retrieves relevant pixel-art knowledge, and prepares
   the request through its normal intake and provider workflow. The caller does
   not construct UDL records or provider arguments on PIXL's behalf.
3. The production request reaches the mocked external boundary. Assert the selected
   operation and arguments against the actual contract before returning a test job
   response. A malformed request must fail rather than receive unconditional success.
4. PIXL handles the controlled job-status sequence, retrieves the fixture bytes
   through the same artifact path, and imports the candidate. It must not skip
   submission, polling where required, or retrieval because this is a test.
5. PIXL performs applicable measurements and actual native/enlarged image review.
   Rejection remains rejection. A revised request, when the scenario needs one,
   passes through the same intercepted boundary with a separately retained outcome.
6. PIXL returns asset paths, essential metadata, review findings and unfinished
   requirements. The parent opens and inspects the files against the assignment.
   Report these as test outputs, never newly generated PixelLab art.

Add focused failure checks for invalid requests, provider errors and an ambiguous
submission response. Check that unknown outcomes are retained and do not cause a
blind duplicate submission. Keep these bounded to the selected operation. Use the
existing [trial runner](host_trials.py) where suitable, adding the missing delegation
and provider interception rather than building a general simulation framework.

## Acceptance and limits

| Condition | Required evidence |
| --- | --- |
| Official integration | The production route uses the selected official PixelLab contract; fixtures are tied to its recorded version/source. |
| Delegation in both hosts | Actual parent-to-PIXL invocation and returned result, not just direct profile startup. |
| Complete request path | Asserted provider arguments, simulated job observations and artifact retrieval/import through the production workflow. |
| Useful reviewed delivery | Actual measurements/viewing and successful parent consumption of the delivered files under the test brief. |
| Failure behavior | Rejected requests/errors remain failures; an ambiguous submission does not trigger an unexamined retry. |
| No provider side effects | Tests intercept external calls, reject unintended network fallback, and make no live PixelLab requests. |

Keep separate Claude and Codex verdicts. One passing host is partial completion.
Preserve failures and identify changed instructions/runtime in fresh attempts; use
the same final package for the completed pair. A valid state file or a model's
self-reported success cannot substitute for recorded calls and artifact checks.

Passing establishes bounded integration and host behavior with a mocked provider.
It does not establish live authentication, remote availability, actual generation
quality or engine acceptance. Fresh generation belongs to an actual production
assignment with its established authorization; it is not a test prerequisite.
The remaining [PX-EVAL-003 cases](TODO.spec.md#px-eval-003--broaden-outcome-and-recovery-coverage)
stay open and do not precede this milestone.

## Evidence and mechanism assessment

When execution begins, retain a new series under `evidence/delegated-asset-request/`:
brief and fixture identities, package identity, parent/specialist records, asserted
requests and simulated responses, actual delivery files, inspection and independent
review. Keep exact proof resources with the frozen package so an update cannot
replace the evidence used. This does not close the general
[package-update recovery gap](TODO.spec.md#px-ops-002--preserve-project-proof-dependencies-across-kit-updates).

Record local workflow effort, record-edit retries, custom glue, repeated context
reads and maintainer intervention. Mock timing does not measure service latency.
Classify each encountered mechanism with supporting observations:

- **Keep in the normal path:** supports necessary production or recovery work.
- **Simplify the interface:** useful responsibility, but repetitive editing,
  corrective retries or custom glue identify a concrete interface problem.
- **Optional for this assignment:** retain it for tasks that need it.
- **Unassessed:** insufficient evidence from this trial.

Focus on knowledge retrieval, intake/plan construction, provider job handling,
inspection and return to the parent. Do not require family expansion, simulation
research or engine tooling unless the selected brief needs it. No classification
by itself authorizes removing existing work.

## Work remaining

- [ ] Identify the official production interface and its test interception boundary.
- [ ] Prepare the matched generation brief, schema-bound responses and image payloads.
- [ ] Exercise request, job, retrieval and failure behavior without provider access.
- [ ] Run and independently review actual delegation and delivery in Claude.
- [ ] Run and independently review actual delegation and delivery in Codex.
- [ ] Publish per-host outcomes and evidence-backed interface recommendations.

This document defines the work; it does not claim those integration tests or host
trials have already run.
