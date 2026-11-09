# PIXL agent kit

Start with [everyday asset production](../plugins/pixl/skills/pixl/references/everyday.md)
for assignment, selected asset, official request, review and delivery/resume. The
companion [hash/root/locator guide](../plugins/pixl/skills/pixl/references/identities-and-paths.md)
explains the additive public `hash_domains` labels and runnable consumer examples.
Both ship with the common skill; setup and advanced surfaces remain below.

For ordinary candidate/family review, use [review-context and candidate-review](../spec/candidate-review.md):
read exact criteria and bindings, supply actual observations and explicit judgments,
then choose record, nominate or complete. The operation retains evidence and handles
recoverable lifecycle publication through the same CLI/MCP implementation. Prepared
inspection packets keep their own view-coverage contract.

For successor authoring, use `context --view authoring` to read explicitly linked
caller choices and the index of other intake choices. Use `request-review --view
changes --plan NEW --against-plan OLD --root ROOT` for structural changes and
review attention, then follow both full-report locators for literal comparison.
These are optional views of the existing [connected-plan workflow](../spec/production-plan.md);
direct result-file export avoids copying large JSON into commands.

The [native host evaluation](../evaluations/README.md) now records the exact packaged
instructions in authenticated Claude and Codex trials, including repeated visual
rejection and cold intake continuation. The original Claude login failure is preserved
alongside subsequent model activity and interrupted attempts. See the [criterion review](../evidence/host-evaluation/criterion-review.json)
for observed passes, failures and unverified requirements. Earlier scripted kit checks below
remain distinct from these model sessions and from actual provider/engine outcomes.

PIXL is a reusable pixel-art production profile, workflow skill, and local UDL runtime for Claude and Codex. Its job is to turn a brief into a source-specific style contract, researched production choices, representative proofs of concept, actual PixelLab tool execution, inspected artifacts, and durable production state. The [profile](../.agents/PROFILE.md) is the shared behavioral authority. [PIXL-1](../spec/PIXL-1.md) / [registry](../pixl/registry.json) preserve existing state; [PIXL-2](../spec/PIXL-2.md) / [registry](../pixl/registry-v2.json) define the new intake and candidate-acceptance lifecycle.

Markdown instructions, JSON plugin manifests, MCP JSON arguments, and TOML configuration translate this system into each harness. They are not the UDL. The local runtime performs deterministic state and artifact checks. PixelLab's remote service performs generation through separately authenticated tools. The harness model remains responsible for interpreting a brief, making supported artistic judgments, using available tools, and reporting evidence.

## WHO, WHAT, WHERE, WHY

| Decision | WHO | WHAT | WHERE | WHY and evidence |
| --- | --- | --- | --- | --- |
| Shared artistic authority | PIXL and the user | One profile plus project-specific contracts | `.agents/PROFILE.md`, copied to `resources/agent/PROFILE.md` | Prevent Claude/Codex drift while preserving project intent. This is a project design choice, not a model-quality claim. |
| Custom state with explicit adapter boundary | Runtime validates; agent authors | Versioned UDL plus thin harness adapters | `spec/PIXL-1.md`, `pixl/registry.json`, skill/agent/manifests | Stable IDs, relationships, and validation need a source contract; harness formats have their own schemas. |
| Repository Codex discovery | Codex harness | Minimal wrapper skill | `.agents/skills/pixl/SKILL.md` | Official documentation identifies repository `.agents/skills` discovery and explicit skill invocation. [Build skills](https://learn.chatgpt.com/docs/build-skills) |
| Claude skill and agent | Claude harness | Project wrapper and specialist agent | `.claude/skills/pixl/`, `.claude/agents/pixl.md` | Claude documents separate skills and subagent definitions. Omitted tool restrictions allow the available MCP tools to be inherited; the agent discovers real names. [Skills](https://code.claude.com/docs/en/skills), [Subagents](https://code.claude.com/docs/en/sub-agents) |
| Portable distribution | Maintainer builds; harness loads | Dual manifests, one skill, one runtime copy | `plugins/pixl/` | Both harnesses can consume their own manifest without pretending those manifest schemas are identical. Local Codex `plugin-creator` schema and Claude's native validator establish the package shapes. [Claude plugin reference](https://code.claude.com/docs/en/plugins-reference) |
| Keep Python runtime beside the skill | Runtime runner | Resolve the installation from `__file__`; load `runtime/pixl` | `plugins/pixl/scripts/pixl.py` | A plugin may be copied into a cache and invoked from another project. Relative-to-installation resolution prevents a hidden dependency on the original checkout. The relocation proof checks this; dependencies belong in the selected Python environment. |
| Optional local MCP wiring | User chooses the project root; harness starts server | Explicit session/project configuration templates | `plugins/pixl/config/` | Root paths differ per installation and project. Standard stdio MCP configuration is documented in both harnesses. No active connection or authentication is implied by including a template. [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [Claude MCP](https://code.claude.com/docs/en/mcp) |
| Remote generation stays with PixelLab | Authenticated PixelLab service | Discover tools, submit, retain real IDs, poll real status | The harness's PixelLab connection | Local intent and journal state cannot establish that a remote service accepted or completed work. Current tools and schemas must be inspected. [PixelLab MCP tools](https://api.pixellab.ai/mcp/docs) |
| Source-specific acceptance | User sets goals; PIXL measures and inspects | Mechanical, visual, and destination checks | Project artifacts and evidence | Width/palette checks cannot establish motion readability, seamless joins, or correct engine import. Palette restrictions and edge treatment derive from the selected project. |

Research order on 2026-09-10 (America/Vancouver): inspect installed Codex skill/plugin instructions and CLI help first, then verify missing discovery/configuration details with official OpenAI documentation; inspect Claude CLI help and official Claude documentation. The local versions inspected were **codex-cli 0.154.0** and **Claude Code 2.1.263**. CLI flags below are grounded in those versions; inspect current `--help` if another installation differs.

## Source and bundle layout

```text
.agents/PROFILE.md                    Shared source profile
pixl/                                 Python package and normative registry
spec/PIXL-1.md                         UDL specification
knowledge/                            Curated source-backed knowledge
examples/                             Valid production-state examples
.agents/skills/pixl/SKILL.md           Codex repository wrapper
.claude/skills/pixl/SKILL.md            Claude repository wrapper
.claude/agents/pixl.md                 Claude repository agent
plugins/pixl/
  .codex-plugin/plugin.json            Codex manifest
  .claude-plugin/plugin.json           Claude manifest
  skills/pixl/SKILL.md                 Reusable common workflow
  skills/pixl/references/              Conditional production/runtime guidance
  agents/pixl.md                       Claude plugin agent
  scripts/pixl.py                      Portable runtime entrypoint
  config/                             Inactive MCP templates
  runtime/pixl/                        Generated package copy
  resources/{agent,spec,knowledge,examples,docs,training}/  Generated references and provenance
  resources/pixl/registry.json          Companion for the copied specification link
  requirements.txt                     Generated runtime dependency declaration
  bundle-manifest.json                 Generated source/copy hash inventory
```

Run from the repository with Python 3.11 or newer:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e .
.venv/Scripts/python.exe scripts/build_plugin.py
.venv/Scripts/python.exe plugins/pixl/scripts/pixl.py --help
```

On POSIX systems use `.venv/bin/python` in place of `.venv/Scripts/python.exe`. The source package declares **Pillow 10 or newer** for image inspection and **jsonschema 4.18 or newer** for provider-schema validation; `pip install -e .` installs those dependencies into the selected environment. A copied plugin still needs Python and those packages. In its destination project, create an environment and install the dependencies before invoking the copied runner:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r /ABSOLUTE/PLUGIN/pixl/requirements.txt
.venv/Scripts/python.exe /ABSOLUTE/PLUGIN/pixl/scripts/pixl.py --help
```

The complete `plugins/pixl` directory is the portable unit after building; copying only `skills/pixl` loses its runtime and resources. Rebuild after changing the source package, profile, specification, knowledge, or examples. Keep project stores and generated assets outside the installed plugin directory. The runner sets `PIXL_PLUGIN_ROOT` for bundled resource discovery. Bundling the PIXL source does not bundle a Python interpreter, third-party wheels, or PixelLab credentials.

`resources/pixl/` preserves the complete Python source package used by proof receipts, including `__init__.py` and every sibling import. The active launcher loads `runtime/pixl/`; both copies are byte-checked against source by the bundle manifest. The resource package is also exercised independently after relocation, so its POC can resolve its own service and knowledge resources. Wheels retain the same complete source package. Verify a wheel with `uv run python scripts/check_wheel.py`; it builds through an sdist, installs the wheel and its declared production dependencies into a fresh unseeded environment, then exercises the installed runtime and copied plugin there. Development packages are explicitly checked absent. Maintain the repository with `uv sync --locked`; the dev group retains lint, type, build, coverage and benchmark tooling. Consumers can use `uv sync --locked --no-dev`; the optional `benchmark` extra supplies tokenizer measurements when requested.

## Use from this repository

Codex can discover the checked-in repository wrapper. Launch it from the repository, then invoke `$pixl` in the prompt:

```powershell
codex -C . 'Use $pixl to inspect the project references and plan a coherent asset family.'
```

Claude can discover the checked-in skill and agent. Launch from the repository and invoke `/pixl`, or run `claude --agent pixl` to make PIXL the current session's agent. For a session that loads the portable plugin explicitly:

```powershell
claude --plugin-dir ./plugins/pixl
```

Invoke `/pixl:pixl` for the plugin skill, or launch the forward-facing plugin agent directly with `claude --plugin-dir ./plugins/pixl --agent pixl:pixl`. In a checkout that also exposes repository wrappers, use the intended entrypoint explicitly; duplicate names do not imply merged instructions. The installed Codex CLI does not expose Claude's `--plugin-dir` flag. Its plugin command uses marketplace-backed installation; the repository skill route works without modifying marketplace or user configuration. No marketplace entry or global plugin installation is performed by this kit.

## Delegate from a consumer project

Install/load the complete kit using the host route above, then let the calling agent delegate to the native PIXL specialist. Supply the actual consumer root and installed skill location. If a `plar.txt` exists, use `pixl_plar_read` with `asset_id` (or `plar read --root CONSUMER --asset ID`) and pass the focused packet. Its full transitive dependencies and reference bindings carry context that a queue summary cannot.

Example caller assignment:

> Use PIXL at the supplied installation to produce the selected asset in this consumer project. Follow the attached requirements packet, inspect its references in their declared roles, and preserve the existing decisions and authorization. Use the official PixelLab tools available to this host. Return the delivered files, actual review findings and provider/state identifiers; send consequential unresolved questions back to me.

At contract handoff, PIXL returns `request-review.json` pointing to the exact source bytes, provider arguments or creative brief, criteria, and consequential choices. The caller reads and compares those artifacts, including each rejection rule's source, then retains its own review and resolves discrepancies with PIXL. Continue under existing authorization; this exchange does not add a user-approval step. The [request and criteria operation](../plugins/pixl/skills/pixl/references/request-review.md) defines the packet and return links.

A direct brief with the same necessary facts also works. PIXL owns visual design, tool choice and review; the caller supplies application priorities and consumes the returned files. The [delegation contract](../plugins/pixl/skills/pixl/references/delegation.md) defines requests, questions, partial results and resumption. The [worked direction-planning example](../examples/delegation/README.md) demonstrates a reference inherited from an asset dependency.

## Connect official PixelLab

The official server is `https://api.pixellab.ai/mcp`. Include the [complete PixelLab tool overview](https://api.pixellab.ai/mcp/docs) in task context and use the [platform documentation](https://www.pixellab.ai/docs) for design/workflow knowledge. Inspect the tool declaration exposed in the current session before calling it.

Connection templates are examples to merge into the host's configuration; they are not active connections or a request to replace existing settings:

| Host | Template | Authentication supplied by the launching environment |
| --- | --- | --- |
| Codex, direct HTTP | [Native HTTP](../plugins/pixl/config/pixellab.codex.http.example.toml) | `PIXELLAB_API_TOKEN` contains the raw token; `bearer_token_env_var` supplies the header |
| Claude Code, HTTP | [Claude HTTP](../plugins/pixl/config/pixellab.claude.http.example.json) | `PIXELLAB_API_TOKEN` is expanded into the Authorization header |
| Codex, stdio compatibility bridge | [mcp-remote alternative](../plugins/pixl/config/pixellab.codex.proxy.example.toml) | `AUTH_HEADER` contains the full Bearer header and is forwarded through `env_vars` |

Codex supports native HTTP, so the proxy is an available compatibility choice rather than a required extra process. Claude supports environment expansion in project MCP headers. Keep credential values in the connection environment, outside prompts, source control and production receipts. These templates leave existing host settings untouched. [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp), [Claude MCP configuration](https://code.claude.com/docs/en/mcp).

The authenticated official MCP surface is the primary agent interface. The local PIXL MCP server below supports requirements/state/inspection; the separate optional HTTP adapter supports its documented image operation. Neither substitutes for the full current PixelLab platform.

## Connect the local runtime for one session

The CLI works without MCP. MCP lets the agent invoke local state operations through structured tools. The templates have explicit replacement paths and are not active configuration. Generate a concrete Claude session file from the current checkout without modifying harness settings:

```powershell
$pixlRunner = (Resolve-Path './plugins/pixl/scripts/pixl.py').Path
$pixlProject = (Get-Location).Path
$pixlPython = (Resolve-Path './.venv/Scripts/python.exe').Path
$pixlMcp = @{
  mcpServers = @{
    'pixl-local' = @{
      type = 'stdio'
      command = $pixlPython
      args = @($pixlRunner, 'mcp', '--root', $pixlProject)
    }
  }
}
$pixlMcp | ConvertTo-Json -Depth 6 | Set-Content -Encoding utf8 './pixl-mcp.local.json'
claude --plugin-dir ./plugins/pixl --mcp-config ./pixl-mcp.local.json
```

Choose the intended project directory for `$pixlProject`. Do not pass `--strict-mcp-config` when the existing harness PixelLab connection is needed; that flag excludes other configured servers. Session loading is documented by [Claude's CLI and MCP support](https://code.claude.com/docs/en/mcp).

Codex accepts session-only configuration overrides. From this checkout, resolve the selected interpreter, runner and consumer root instead of copying a machine-specific installation path:

```powershell
$pixlPython = (Resolve-Path './.venv/Scripts/python.exe').Path
$pixlRunner = (Resolve-Path './plugins/pixl/scripts/pixl.py').Path
$pixlProject = (Get-Location).Path
$pixlCommand = ConvertTo-Json -Compress -InputObject $pixlPython
$pixlArguments = ConvertTo-Json -Compress -InputObject @($pixlRunner, 'mcp', '--root', $pixlProject)
codex -C $pixlProject `
  -c "mcp_servers.pixl_local.command=$pixlCommand" `
  -c "mcp_servers.pixl_local.args=$pixlArguments" `
  'Use $pixl. Discover the local PIXL tools and report capabilities before remote work.'
```

For reviewed project configuration, translate the paths in [the Codex template](../plugins/pixl/config/codex.mcp.example.toml) into the project's `.codex/config.toml`. Codex documents stdio `command` and `args` configuration. This kit does not write that file or install a global server. [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)

PixelLab authentication remains a separate harness connection. Consult [PixelLab's setup page](https://www.pixellab.ai/mcp) and current MCP documentation; the kit does not embed a remote token or pretend a documentation URL is an MCP server endpoint. Start a session, inspect its actual tool inventory and schemas, and establish access before paid generation.

## Preserve project sources when updating the kit

After a project imports library S records, use `retain-library` / `pixl_retain_library` to keep their exact revisions in the consumer project. An already affected project can recover from its preserved original kit through the same operation. The [agent workflow](../plugins/pixl/skills/pixl/references/library-retention.md) gives the callable sequence; [the contract](../spec/library-retention.md) explains why retained old proof does not establish new implementation or asset quality.

## Local operations and handoff

An optional, separate [HTTP bridge](../plugins/pixl/scripts/pixellab.py) supports
the official PixelLab async image endpoint. Configure another stdio server with
the selected Python interpreter and arguments `PATH/TO/pixellab.py --root PROJECT`.
Supply `PIXELLAB_API_KEY` through that server's environment; keep its value out of
project files. It is not enabled by the local MCP configuration. Its five tools
cover contract discovery, saved preparation, submission, polling and PNG import.
See the [provider operation](../plugins/pixl/skills/pixl/references/provider-recovery.md)
for the sequence. Authentication and live generation have not been tested here.
The [delegated trial runner](../evaluations/delegated_asset_trials.py) substitutes
only HTTP transport and prohibits provider network calls; it needs no PixelLab key.

The CLI is available as `python -m pixl`, as `pixl` after package installation, or through the bundled runner. Run `--help` for exact arguments. New lifecycle work begins with `intake STORE --name NAME --brief TEXT --root ROOT`; its PX2 `state.px` has no invented style contract. Follow the [intake/sample skill](../plugins/pixl/skills/pixl/references/intake-sample.md) to retain choices and save planned outputs/criteria before verdicts. `workflow FILE --root ROOT` reports candidate-specific checks and blockers. Legacy `init` remains a PX1 initializer with scaffold defaults; existing stores are never silently upgraded. Use `context FILE FOCUS --budget BYTES`, `ready FILE` and `impact FILE ID` for focused work, and `commit STORE CANDIDATE --expect SHA256 --root ROOT` after reconciling the current hash. Use the same project root for file checks and commits when the store sits in a subdirectory.

For a method question, follow the [knowledge operation](../plugins/pixl/skills/pixl/references/knowledge.md). `sources` discovers the selected runtime's verified supplied-source inventory; `sources --root ROOT` explicitly checks a source tree. Use `knowledge METHOD_ID`, then retrieve the method's dependency closure from `knowledge/library.px` with the resource root returned by discovery. `source PATH --expect SHA256 --start N --end N` retrieves exact cited text. Through MCP, `pixl_sources` discovers library sources and `pixl_source` with `scope: "library"` resolves their paths within those installed resources; the default `scope: "project"` continues to resolve project files. Current identities never fall back to old bundled filenames.

To edit through the supplied interfaces, `decode FILE` returns a tagged JSON adapter; edit the intended semantic values and revision, then run `encode ADAPTER_JSON --out CANDIDATE`. Validate and commit the resulting UDL candidate. The tagged JSON is interchange, not the authoritative production-state format.

Context budgets are **strict byte budgets**, not model-token estimates. They do not prove token savings. `ready` establishes readiness only under the declared local rules; it does not establish credentials, credit, remote capacity, visual acceptance, or successful game import.

The local MCP tools include `pixl_review_context`, `pixl_candidate_review`, `pixl_production_plan`, `pixl_stage_prepare`, `pixl_plar_handoff`, `pixl_request_review`, `pixl_plar_read`, `pixl_plar_save`, `pixl_plar_prepare`, `pixl_retain_library`, `pixl_validate`, `pixl_context`, `pixl_ready`, `pixl_impact`, `pixl_init`, `pixl_intake`, `pixl_task_complete`, `pixl_workflow`, `pixl_commit`, `pixl_catalog`, `pixl_sources`, `pixl_source`, `pixl_asset_check`, `pixl_encode`, `pixl_knowledge`, `pixl_capabilities`, `pixl_prepare`, `pixl_job`, `pixl_job_prepare`, `pixl_job_dispatch`, `pixl_job_observe`, `pixl_job_import`, `pixl_jobs`, `pixl_family`, `pixl_family_snapshot`, `pixl_inspection`, `pixl_inspection_prepare` and `pixl_inspection_review`. Fetch actual schemas through `tools/list`. Optional `pixl_asset_check(regions=[...])` reports exact-color component boxes with the image hash. `pixl_inspection` can return selected prepared views as actual image blocks with payload dimensions through `packet_id` and `view_ids`, supporting hosts whose file viewer omits that metadata. The [inspection operation](../plugins/pixl/skills/pixl/references/inspection.md) prepares saved views and retains explicit reviews; actual viewing happens through the host. The [provider recovery operation](../plugins/pixl/skills/pixl/references/provider-recovery.md) saves plan-bound requests, claims dispatch before a host call, retains observations and imports local candidates. Legacy `pixl_prepare`/`pixl_job` remain stateless. No local tool submits or polls PixelLab; remote observations are caller-supplied, and imported candidates still require acceptance.

For connected families and staged requests, use [production-plan and stage-prepare](../spec/production-plan.md). Reviewed JSON supplies stages, existing contracts/baseline and collective requirements; the runtime wires dependencies, binds PLAR selections and exact accepted upstream candidates, then retains the executable request. The host still calls official PixelLab and performs artistic/consumer review. These operations are available through CLI and local MCP; neither creates acceptance.

The [family operation](../plugins/pixl/skills/pixl/references/family-delivery.md) binds production members to the exact approved sample, plans collective continuity and destination requirements, and retains selected bytes in an immutable package. `family FILE [OUTPUT] --root ROOT` reports acceptance, pending jobs and historical snapshot drift; `family-snapshot STORE OUTPUT CANDIDATE --expect HASH --root ROOT` copies accepted member bytes and publishes only an unaccepted report candidate. A useful package can retain unavailable engine requirements and a concrete handoff. Copying does not nominate, evaluate or complete delivery.

## Proofs and honest limits

The packaging proof checks that each harness accepts its manifest/frontmatter and that the bundled runner works from an unrelated working directory. The workflow proof checks local state behavior and deterministic artifact constraints. Neither proves that an LLM follows all instructions or that an actual generated asset looks good. Final execution evidence is recorded in the repository's verification report and the validation record below.

| Proof question | Method | Observable acceptance |
| --- | --- | --- |
| Does Codex accept the plugin/skills schema? | Installed `plugin-creator/scripts/validate_plugin.py` and `skill-creator/scripts/quick_validate.py` | Zero exit status for the plugin and all three skills |
| Does Claude accept the agent and skill definitions? | `claude plugin validate ./plugins/pixl`, plus project component directory validation | Native validator reports no errors |
| Does the plugin depend on the source checkout or cwd? | Copy the complete plugin to a temporary directory, run its absolute runner from another directory, initialize and validate local state | Runner imports its copied runtime; state operations succeed outside the source checkout |
| Are referenced resources actually shipped? | Resolve Markdown file links and compare bundled runtime/resource content with source | Required linked files exist; copies correspond to the current source build |
| Can the connected harness actually invoke it? | Start a session with the documented wrapper/plugin and local MCP configuration, inspect the tool list, make a local read call | Actual harness tool-call evidence; schema validation alone is insufficient |
| Can PIXL produce useful remote assets? | Authorized real PixelLab task with real returned IDs, output artifacts, visual review, and target import proof | Real service and artifact evidence; not exercised by local fixtures |
| Is UDL better for an LLM than another representation? | Controlled same-task comparison with declared metrics and representative models | Measured task success, context use, error rates, and quality; no such superiority is claimed |

Every production method proof must identify the uncertain question, source-backed method, smallest representative artifact, prior acceptance criterion, observed result, and consequence for the plan. This contract is part of [PIXL's production reference](../plugins/pixl/skills/pixl/references/production.md). No live PixelLab generation or LLM superiority is established merely by creating this kit.

## Kit validation record

Observed on 2026-09-10 with the local CLI versions listed above:

| Check | Observed result |
| --- | --- |
| Codex `validate_plugin.py plugins/pixl` | Passed |
| Codex `quick_validate.py` | Passed for the reusable skill and both repository wrappers: 3/3 |
| Claude `plugin validate` | Passed for `plugins/pixl`, `.claude/agents`, and `.claude/skills`: 3/3 |
| Claude `--plugin-dir ./plugins/pixl plugin details pixl` | Loaded `pixl@inline`; inventory contains one skill and one agent, no active MCP servers |
| Codex app-server `skills/list` | Returned this repository's `.agents/skills/pixl/SKILL.md`, `scope: repo`, `enabled: true`, and no PIXL errors |
| Codex session MCP overrides | `mcp get pixl_local --json` resolved the documented Python command, runner path, and project root |

The first Codex validator attempt failed because system Python lacked `yaml`. Validation then passed using PyYAML 6.0.3 installed in a temporary virtual environment; no global dependency was installed. The failure was in the validation environment, not a successful plugin check.

The actual Codex discovery proof used an isolated `codex app-server --stdio` process with the following sequential JSON-RPC messages, waiting for the initialize result before listing skills. This is the app-server protocol, distinct from the PIXL MCP server:

```json
{"id":1,"method":"initialize","params":{"clientInfo":{"name":"pixl-local-kit-validation","version":"0.1.0"}}}
{"method":"initialized","params":{}}
{"id":2,"method":"skills/list","params":{"cwds":["C:/Users/ryanf/github/pixel-lab-docsuite"],"forceReload":true}}
```

These observations prove discovery, parsing, and inventory behavior. They do not prove LLM instruction following, actual MCP invocation by a model, or remote generation quality. No model call or paid PixelLab job was part of these harness proofs.

## Independent relocation exercise

Observed 2026-09-11 06:22 UTC (2026-09-10 in America/Vancouver). A separate agent exercised the supplied skill, profile, specification, CLI help, and MCP schemas against a copied bundle, without importing the source checkout's Python package. The test used Windows, Python **3.14.3**, Pillow **12.3.0**, and jsonschema **4.26.0** in `%TEMP%/pixl-kit-validator-20260910`; PyYAML **6.0.3** was present for the separate skill validators.

The plugin was copied to `%TEMP%/pixl-forward-rk010tvr/relocated plugin`, and commands ran from the sibling `fresh project` directory. Both paths contain spaces. Child processes removed `PYTHONPATH` and ran Python with `-I`; `importlib.util.find_spec('pixl')` returned `None` before the runner loaded the bundle. The copied `bundle-manifest.json` SHA-256 was `ea340f2be2f47e4d5106a3e9d09c4445922949bd147c44adfeb70db45d53ca69`.

The exercise copied `resources/examples` and `resources/docs` into the fresh project so the example's root-relative artifact and source references remained meaningful. All **28 manifest-listed files** matched their recorded SHA-256 values, and all **seven relative file links** in the active skill, its references, and the copied specification resolved. Example file validation verified its local research sources, receipt, and image.

| Operation | Observed outcome |
| --- | --- |
| Initialize and validate `.pixl` | Revision 0, three records, valid state; defaults identified as unconfirmed intake |
| Validate `examples/atelier/project.px --root .` | Valid, 13 records, `files_verified: true` |
| `ready` for the example | Exactly `produce`; this is local readiness, not remote availability |
| Retrieve `produce` with budget 8192 | 2,266 UTF-8 bytes; saved packet independently validates with all files checked |
| Retrieve with budget 2265 | Intended rejection, exit 2: `context_budget`, required 2266; no truncated packet emitted |
| Decode/edit/encode two revision-1 candidates | Both candidates encoded through the public CLI |
| Commit first candidate with revision-0 hash | Accepted at revision 1 |
| Commit competing candidate with the same old hash | Intended rejection, exit 2: `stale_write`; accepted state remained byte-identical |
| Inspect local fixture using `asset-check` | 16×16, 80 visible pixels, three visible colors, zero out-of-palette or fractional-alpha pixels; visual and engine verification explicitly false |
| Change one fixture pixel and validate | Intended rejection, exit 2: `file_hash: swatch: examples/atelier/palette-fixture.png` |
| Restore original fixture bytes and validate | Passed again with the original example hash |
| Start local MCP subprocess and initialize | Server `pixl-local` 1.0.0 negotiated protocol `2024-11-05` |
| MCP `tools/list` | 13 local tools with input schemas |
| MCP `tools/call` → `pixl_validate` | `isError: false`, valid 13-record example, `files_verified: true`; structured result matched the text result |

The recorded workflow comprised **16 CLI invocations: 13 successful operations and three intended rejections**. The negative checks are successful failure-handling proofs, not production failures hidden by a final pass. No runtime or runner defect was found in this exercise. That snapshot had 13 MCP tools; source-slice retrieval brought it to 14, source discovery to 15, intake/workflow to 17, durable provider operations to 22, and family operations to the current 24. Current runtime, POC, packaging and protocol results are recorded in [verification](VERIFICATION.md), separately from this earlier exercise.

With `$pixlPython` set to the isolated interpreter and `$pixlRunner` set to the copied runner's absolute path, the key commands were:

```powershell
& $pixlPython -I $pixlRunner init .pixl --name 'Relocated PIXL proof' --root .
& $pixlPython -I $pixlRunner validate examples/atelier/project.px --root .
& $pixlPython -I $pixlRunner ready examples/atelier/project.px
& $pixlPython -I $pixlRunner context examples/atelier/project.px produce --budget 8192
& $pixlPython -I $pixlRunner decode .pixl/state.px
& $pixlPython -I $pixlRunner encode winner.json --out winner.px
& $pixlPython -I $pixlRunner encode stale.json --out stale.px
& $pixlPython -I $pixlRunner commit .pixl winner.px --expect $revisionZeroHash --root .
& $pixlPython -I $pixlRunner commit .pixl stale.px --expect $revisionZeroHash --root .
& $pixlPython -I $pixlRunner context examples/atelier/project.px produce --budget 2265
& $pixlPython -I $pixlRunner asset-check examples/atelier/palette-fixture.png --width 16 --height 16 --palette '#202840' '#486880' '#88b8a8'
& $pixlPython -I $pixlRunner mcp --root .
```

For the competing candidates, the decoded adapter revision was set to 1 and the project name was set to `Accepted local edit` or `Competing stale edit`. The original revision-0 hash was `db7d9e07ab54c7b72a523e7e6812df951e82bec88ea49d185d1ff99a672283f4`. The accepted revision-1 hash was `ac06a94c46251db2e0cfadb27dcc05d2a081749e3e3ce876d5ce16b68d09bafc`. The changed-file proof saved the original PNG bytes, set pixel `(0, 0)` to RGBA `(255, 0, 0, 255)` with Pillow, saved the image, validated the expected hash rejection, and restored the exact original bytes before final validation.

The actual MCP exchange sent these messages over subprocess standard input, waiting for each requested result before the dependent step:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"pixl-forward-proof","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"pixl_validate","arguments":{"path":"examples/atelier/project.px"}}}
```

Discovery and validation were performed in two freshly initialized server processes so the calling agent could inspect the discovered `pixl_validate` schema before issuing its call. These are real local MCP responses, not a mock transport or a model invocation.

Raw command/response evidence was retained under `%TEMP%/pixl-forward-rk010tvr/`: `forward-evidence.json` (SHA-256 `9a80296ac97492c26d3a8e9755b2a50b7e46dc3a638aad31d83024e6d0560935`), `mcp-discovery-evidence.json` (`6cbb22a0cc748463b6d550bd08838babab6652203d9ba81f8e441caa15a0200e`), and `mcp-validation-evidence.json` (`9c46229446e0fa012dcd30cdc84e04589a2a086e94ca5684f54ef4270230a68e`). Those temporary files are session evidence; this document retains the outcomes and reproduction details.

This exercise did not call the platform prepare/job methods or the method-POC command, which were still being completed for the next bundle build. It did not contact PixelLab, use a paid model, visually accept an asset, or test an engine import. The PNG is explicitly a local measurement fixture, not a PixelLab output. No artistic or LLM-performance claim follows from these checks.

## PLAR and current host delegation

Use `$plar` (Codex repository skill) or `/plar` (Claude repository skill) for project-to-asset requirements. The portable Claude plugin exposes `/pixl:plar`. The full plugin now includes `skills/plar/` and the three local PLAR MCP operations. The [format reference](../plugins/pixl/skills/plar/references/format.md) gives focused read/save commands from another project's root. Compare saved allocation with `plar read --root CONSUMER --since PRIOR_PLAR_HASH` to identify tracked changes and dependent assets. Once the exact request and candidate criteria have caller review, use `pixl_plar_prepare` (or `plar prepare`) to retain their inputs and create the first durable job. The [preparation workflow](../plugins/pixl/skills/plar/references/prepare.md) gives the ordinary JSON contract. Dispatch and actual PixelLab execution follow through the existing provider workflow; preparation itself does not create an image or accept art.

Codex's repository agent is [pixl.toml](../.codex/agents/pixl.toml); Claude's remains [.claude/agents/pixl.md](../.claude/agents/pixl.md). For another project, use the [Codex agent template](../plugins/pixl/config/codex-agent.example.toml) with the actual installed plugin path. Templates do not modify user configuration. A host can also explicitly delegate through its ordinary native agent tool and load the shared skill without a custom agent registration.

Give the delegate: absolute consumer root, installed skill location, PLAR path and asset ID (or the complete brief), reference paths, relevant user decisions/authorization, and required deliverables. A natural request is: “Delegate to PIXL to produce asset queue.working from this project's plar.txt using PixelLab, inspect it, and return its paths and integration results.” Requirements-only requests stop after allocation; production requests continue through actual generation and delivery.

For a copied plugin in Codex, place the complete kit under `.agents/skills/pixl-kit/` and add discoverable `.agents/skills/plar/SKILL.md` and `.agents/skills/pixl/SKILL.md` wrappers pointing to `../pixl-kit/skills/plar/SKILL.md` and `../pixl-kit/skills/pixl/SKILL.md`. Keep the kit's sibling resources/runtime intact. Alternatively use the host's supported plugin installation. Shared names are not automatically merged.

The canonical profile is explicitly copied from `.agents/PROFILE.md` to the portable `resources/agent/PROFILE.md` location. Both wheel and plugin checks verify those bytes. A source-only wheel provides runtime resources; the complete plugin also provides host skills and agent adapters.


Focused PLAR reads also join the allocation to retained production: current selected
task, output reviews, provider-bound pending work and next action. Single-output
preparation links its work back to the queue. An interrupted link can be repaired by
resuming the same request. A reviewed changed contract uses the same operation with
`revise: true` and the current state `expect` (CLI `--revise --expect`), after pending
work has been resolved through its originating connection. Old generations and their
reviews remain; the replacement does not inherit acceptance. `ready PATH --root
CONSUMER` and MCP readiness apply the same current-selection checks as dispatch and
completion. See [the allocation/production contract](../spec/asset-preparation.md)
and [cohesion evidence](../evidence/plar-cohesion/README.md) for behavior and limits.

Use `request-review PACKET --root CONSUMER --asset ID` (or `pixl_request_review`) to resolve exact file-local criterion sources for independent caller comparison. Connected authoring and stage preparation return `request_review` arguments for that same tool: the saved state, plan and optional job. This route includes every member and collective criterion, source excerpts, controls and the exact retained request. Pass the saved caller comparison through `comparison` to check its identity and coverage; the caller still judges meaning. It reports bad locators and changed sources without certifying semantic consistency. Focused production includes `continuation` with the current provider-bound action and prerequisites before a later request; carry that object in the returned handoff. See [the evidence contract](../spec/request-review.md) and [connected-plan review](../spec/production-plan.md#exact-criteria-handoff).

## Harness, knowledge and provider responsibilities — checked 2026-11-08

PIXL applies the host model's existing pixel-art expertise together with the shared
profile, curated methods and project evidence. Skills make that expertise reusable;
local MCP operations preserve measurements and state; the host's available tools
provide source/image inspection, code execution, research and delegated work. PixelLab
supplies the actual production generation service. A callable PIXL profile is not a
separately trained global model, and its local runtime is not its whole capability.

| Responsibility | Operational location |
| --- | --- |
| Application purpose, consumer context and established authorization | Calling agent and actual project sources |
| Pixel craft, art direction, method applicability and visual judgment | PIXL profile using host-model knowledge, relevant library material and inspected artifacts |
| Reusable allocation, request/review and delivery procedure | Shared PLAR/PIXL skills, progressively loaded references |
| Model execution, tool availability and permissions | Claude/Codex harness and its actual session configuration |
| Deterministic facts and resumable identities | Shared CLI/local MCP; exact request evidence and `pixl_plar_handoff` |
| Production generation and provider capabilities | Official PixelLab connection and current selected tool declaration |

OpenAI documents skills as reusable workflows loaded progressively, and custom agents
as inheriting parent permissions, provider and MCP servers. The existing thin Codex
adapter keeps that relationship. [Skills](https://learn.chatgpt.com/docs/build-skills),
[subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

Anthropic documents skill preloading and skill discovery during subagent execution;
its subagents start without the parent's conversation history. The existing Claude
adapter explicitly loads the shared profile/skill, and the caller supplies the actual
assignment and references. A skill preload is not a complete consumer handoff.
[Claude subagents](https://code.claude.com/docs/en/sub-agents),
[Claude skills](https://code.claude.com/docs/en/skills).

PixelLab's guide distinguishes MCP tools from REST interfaces and exposes current
operation-specific image/reference and palette controls. Those declarations determine
what a request can do; they do not make a palette, dominant color or provider default
an owner requirement. Use the [platform docs](https://www.pixellab.ai/docs) and
[official MCP guide](https://api.pixellab.ai/mcp/docs), then inspect the connected tool.
The existing HTTP adapter remains separately scoped; these checks do not extend it to
undocumented endpoints or certify every advertised provider operation.

For a retained result, save expert observations in handoff `details` while the tool
preserves `resume` and `next` exactly. Completed caller checks and future work have
separate fields. A later contract correction is retained as a new proposal/comparison,
without rewriting the historical request, generated candidate or accepted verdicts.


### Native continuation correction — checked 2026-11-08

The official [Claude subagent continuation documentation](https://code.claude.com/docs/en/sub-agents#resume-subagents) uses `SendMessage` with the returned agent ID/name; a new `Agent` call creates another instance. The [tool reference](https://code.claude.com/docs/en/tools-reference) also distinguishes this from the removed `TaskOutput` tool. The installed trial host is Claude Code 2.1.318. Earlier handoff-repair trial tool lists omitted `SendMessage`, so their separate child instances establish artifact continuity, not native instance resumption. The evaluator now exposes `SendMessage` for communication with agents created for the assignment. This changes the isolated trial tool list, not user-global configuration. Shared delegation guidance uses the actual host continuation surface and records an artifact-based restart honestly when native continuation is unavailable.
