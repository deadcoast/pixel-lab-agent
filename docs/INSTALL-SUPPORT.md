# Installation, update and resume support

Use the [consumer setup guide](AGENT-KIT.md#set-up-a-consumer-project) to select a
Python environment, complete kit and consumer root. This matrix states which
combinations have been exercised. The package requirement is **Python 3.11 or
newer**, with Pillow and jsonschema; that minimum is not qualification of every
Python version or operating system. A wheel supplies the local runtime and
resources. Host skills and specialist registration still need the complete kit.

Updated 2026-11-14 (America/Los_Angeles). **TM-05 is bounded complete for the
combinations below.** [Final local receipts](../evidence/install-support/20261114/local-01/FINAL.json)
and [fresh native results](../evidence/install-support/20261114/native/RESULT.json)
retain exact sources, package identities and failures. The
[capability matrix](CAPABILITY-OUTCOMES.md) separately records production outcomes,
provider work, renderer observations and acceptance.

## Choose an installation route

| Route | Use it when | What must remain available |
| --- | --- | --- |
| Complete copied kit | You want the shared skills, host adapters and bundled CLI/MCP runtime without a source checkout | The entire kit, its selected Python environment and the consumer project; invoke `scripts/pixl.py` from that kit |
| Exact wheel | You want an installed `pixl` command or `python -m pixl` runtime | The selected environment and retained wheel identity; load host instructions separately from a complete kit |
| Locked source checkout | You are working from this repository and its lockfile | The checkout and environment created by `uv sync --locked --no-dev`; this does not register a host specialist |

Only Pillow and jsonschema are mandatory PIXL runtime dependencies. Browser
execution has separate optional requirements in the
[consumer execution contract](../spec/consumer-execution.md); installing the
runtime does not install a browser, Node, a host account or provider credentials.
Consumers do not need the repository's build tools or full verifier.

## Local runtime qualification

Each cell first checks the copied-kit bootstrap with missing dependencies, then
checks fresh copied-kit and wheel installation and useful selected-asset
preparation. The missing-dependency probe is not a separate bare-wheel test.
After actual moves,
new processes reread the exact saved pending job, requirements and state. Kit and
consumer move together for the copied route; the wheel environment stays fixed
while its consumer moves. These are read-only cold recovery/status checks after
local preparation, not provider resumption or native conversation continuation.
Synthetic schema/observations and a local dispatch claim occur in the preparation
probe; no PixelLab request occurs. Exact receipts identify the interpreter,
dependencies and executed package bytes.

| OS and interpreter | Copied kit | Wheel | Locked source |
| --- | --- | --- | --- |
| [Windows 11 build 26300 x64, Python 3.11.14](../evidence/install-support/20261114/local-01/windows-py311-02/RESULT.json) | Pass | Pass | Not qualified for this combination |
| [Windows 11 build 26300 x64, Python 3.12.10](../evidence/install-support/20261114/local-01/windows-py312-02/RESULT.json) | Pass | Pass | Not qualified for this combination |
| [Windows 11 build 26300 x64, Python 3.13.12](../evidence/install-support/20261114/local-01/windows-py313-02/RESULT.json) | Pass | Pass | Not qualified for this combination |
| [Windows 11 build 26300 x64, Python 3.14.3](../evidence/install-support/20261114/local-01/windows-py314-06/RESULT.json) | Pass | Pass | Pass: fresh install and useful local operation |
| [Ubuntu WSL2 x86_64, Python 3.12.3; native Linux `/tmp` filesystem](../evidence/install-support/20261114/local-01/wsl-py312-02/RESULT.json) | Pass | Pass | Not qualified for this combination |

All five final rows also reread a genuinely retained production plan after
same-path old-to-current **copied-kit replacement**, preserving its 3,032 non-kit
files. This is not an in-place pip wheel upgrade. The wheel cells qualify fresh
installation and moved-consumer cold reads with a fixed environment. Every copied/
wheel consumer preserves its 56 preexisting files across the move. The locked-source cell covers fresh locked
installation and useful local operation; it does not claim source-checkout or
virtual-environment relocation. [Earlier attempts and harness corrections](../evidence/install-support/README.md#failures-and-exact-identities)
remain retained. The final WSL run uses Linux-native inputs and working paths;
its staging and returned receipts are hash-bound. The earlier Windows-mounted
WSL run also passed, with its earlier evaluator source preserved separately.
The recorded distro name is Ubuntu; an exact distro release was not captured.

The [final local index](../evidence/install-support/20261114/local-01/FINAL.json)
binds 341 executed commands to one final evaluator source. Twelve evaluator
tests and Ruff pass separately from those actual installation commands.

The selected copied kit has manifest
`48120249c0a10672db9c773f0ad89d2e178022f4a93edd80a2d8c4e5f2442b79`.
The fresh retained wheel has SHA-256
`b1bfb390f9a45df4f9663ae62491883c12bec5f15af8a0a7d129fb72715e7846`.
The kit manifest and package label `1.0.0` do not identify a wheel. The production
runtime remains unchanged; the last full verifier is retained SC-06 evidence,
not a new TM-05 run. The new evaluator and its targeted tests are separate
verification. No new local pass is inferred from the existing full suite.

Retained evidence remains useful within its original scope:

- [Fresh three-route setup](../evidence/readiness/20261109/setup/attempt-01/RESULT.json)
  passed on Windows/Python 3.14.3 with its recorded older kit and wheel. It proves
  those installed source reads/readiness checks, not the new matrix's separate final rows.
- [SC-06 installed-kit replacement](../evidence/schema-compatibility/README.md)
  preserved a real saved production plan and four animation/terrain replays after
  an old-to-current kit update. Exact saved files, old cleanup failures and the
  separate local execution scope remain recorded.

macOS, native Linux outside the recorded WSL environment, other architectures and
other Python versions are **unqualified**, unless a later receipt names them.
That is a testing limit, not an assertion that they cannot work. Python below
3.11 is outside the declared package requirement. Host vendors' platform support
does not by itself qualify PIXL on those platforms.

## Host loading and native qualification

| Windows host route | Current TM-05 loading outcome | Retained native evidence and limits |
| --- | --- | --- |
| Codex CLI 0.167.2; explicit `pixl` role configuration and installed-skill wrappers | [Pass, 19/19](../evidence/install-support/20261114/native/codex-clean-01/independent-grade-04.json): named specialist loads and performs useful local retrieval. Original 18/19 inventory-parser grade retained. | [Earlier setup](../evidence/readiness/20261110/RESULT.json) passed 19/19 clean and 16/16 omitted-role checks on Codex 0.167.0. Automatic project discovery and general cross-process continuation are separate claims. |
| Claude Code 2.1.318; explicit complete-kit `--plugin-dir` | [Pass, 18/18](../evidence/install-support/20261114/native/claude-clean-01/independent-grade-03.json): actual plugin child loads and returns useful local retrieval. Original 0/1 reference-wrapper parser failure and the child's self-corrected path error remain retained. | [Earlier setup](../evidence/readiness/20261110/RESULT.json) passed 18/18 clean and 16/16 omitted-plugin checks. Expired-authentication attempts remain retained; later same-child continuation has its own evidence. |

Both [fresh native cases](../evidence/install-support/20261114/native/RESULT.json)
use Windows/Python 3.14.3 and the same 251-file portable kit inventory, excluding
bytecode caches. Their 258/255 original consumer files remain unchanged. The
final grader passes 27 targeted tests and Ruff; corrections regrade the retained
traces rather than replace the native work. These cases establish current loading
and local retrieval, not native continuation through an update or move.

Codex's current [custom-agent contract](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)
describes project `.codex/agents` TOML files and inherited parent permissions,
provider and MCP configuration. Keep the tested explicit registration from
[consumer setup](AGENT-KIT.md#codex-in-another-project); file presence or CLI help
does not establish that a named child loaded and used the profile. Local
`codex plugin --help` describes marketplace installation through `add`, not
Claude's local `--plugin-dir` route. Marketplace installation is not qualified
by a copied-kit result.

Claude documents [session folder loading](https://code.claude.com/docs/en/plugins/create#develop-without-a-marketplace)
and [plugin update/loading boundaries](https://code.claude.com/docs/en/plugins/install#keep-plugins-updated).
Use the complete kit path on each session launch. Selecting `--agent pixl:pixl`
for the primary session is distinct from a caller delegating to that specialist.
A running session can retain its loaded version after on-disk files change;
start a fresh session, or use the host's documented reload, before claiming the
new instructions loaded. Local prerequisite checks do not authenticate PixelLab.

Host facts above were checked against local help and official documentation on
2026-11-14. Vendor [Claude platform requirements](https://code.claude.com/docs/en/setup#system-requirements)
are a separate installation contract. The native rows do not extend to WSL,
other host versions, IDEs, desktop-only loading or cloud sessions without actual
qualification of those routes.

## Update a kit without losing saved production

1. Keep the original complete kit and its manifest, the selected environment's
   dependency information, and the consumer's current state and artifacts. Keep
   mutable work outside the kit. Preserve failed outputs as well as successful
   deliveries.
2. If the project imported library S records from the old kit, run the existing
   [library-retention workflow](../plugins/pixl/skills/pixl/references/library-retention.md)
   while the exact old bytes are available. A project with only direct consumer
   sources does not need library retention merely because the kit changes.
3. Prepare the complete replacement kit, or install the exact new wheel into a
   fresh selected environment and reselect its interpreter. In-place pip upgrades
   are not qualified by this matrix. Keep the old installation available until
   the saved project has been read
   successfully with the new one. Use a fresh output directory for any replay;
   an earlier failed receipt is not disposable scratch space.
4. Run `readiness`, then read the actual selected project's `validate`, `workflow`
   and `jobs` results through the new installation in a fresh process. A passing
   dependency check is only the start: inspect current requirements, state hash,
   retained job identity and next action. Existing unknown jobs stay unknown.
5. Reconcile host paths and start the intended loading route. Verify the actual
   named specialist and local tool access when delegation is needed. Preserve
   the parent's official provider connection; an update is not a provider retry.

An unsupported saved version uses the
[adapter compatibility policy](../spec/adapter-compatibility.md). Keep its bytes
and use a compatible kit or a documented migration; do not relabel versions,
rewrite hashes or transfer acceptance. If historical library bytes are already
missing, use the preserved original kit as the explicit retention donor. A new
kit cannot reconstruct lost original bytes.

## Relocate and resume

Move the complete consumer data tree so relative source, state, artifact and
receipt locators keep their meaning. Carry `.pixl/library-sources` when present.
The copied kit runner resolves its bundled runtime from its own location, but
host configuration can still contain absolute paths. Retarget the paths that
actually changed:

- the selected Python executable and kit runner in local MCP configuration;
- the consumer root passed to local operations;
- Codex's role configuration path, installed-skill paths and wrappers;
- Claude's `--plugin-dir` and any session MCP configuration file.

Recreate a virtual environment at its new location rather than copying it as a
portable runtime; Python's [venv documentation](https://docs.python.org/3/library/venv.html)
explains that environments contain location-specific paths. A stable interpreter
outside the moved project can remain selected if it is still available. On WSL,
use the environment and path syntax of that Linux process, not Windows `Scripts`
paths.

Restart the local MCP process after changing its command or paths. Then use the
[everyday continuation](../plugins/pixl/skills/pixl/references/everyday.md) to read
the selected asset, current production and exact next operation. This is an
artifact-based cold resume in a new process. It does not prove that an old host
conversation or child agent resumed, that a new provider call occurred, or that
saved artistic/human acceptance applies to changed requirements.
