# Consumer setup and observed readiness

Use this reference when loading PIXL in another project, diagnosing a missing
specialist/tool, or checking a changed host installation. Continue an established
asset assignment when its required capabilities are already observed. Readiness
is a small setup report, not a new approval step or an artistic review.

PIXL is the host's visual specialist using the [shared skill](../SKILL.md) and
profile. The official connected PixelLab tools perform generation and editing.
The local Python runtime supports requirements, retained state, inspection and
handoff. Installing that runtime does not register a specialist or authenticate
PixelLab, and a visible skill is not proof that a named child was invoked.

## Load the complete kit in the consumer

Keep the complete plugin directory, including `skills`, `agents`, `config`,
`scripts`, `runtime`, `resources` and `bundle-manifest.json`. Copying only a skill
loses required resources. Keep the installed kit separate from mutable consumer
state and generated assets.

Choose Python 3.11 or newer in the consumer's environment. Install the supplied
`../../../requirements.txt` for ordinary local operations; it declares Pillow and
jsonschema. Maintainer lint, build and test dependencies are not required. A wheel
installs the local runtime and profile resources; it does not install host skills
or register a named role.

- **Claude Code:** load the complete kit with `--plugin-dir <absolute-kit-path>`.
  The plugin skill is `pixl:pixl`; use the actual plugin specialist exposed by the
  host. The [local MCP template](../../../config/claude.mcp.example.json) needs the
  selected Python, absolute runner and consumer root.
- **Codex:** the [agent template](../../../config/codex-agent.example.toml) belongs
  in the consumer's `.codex/agents/pixl.toml` after replacing its installation
  placeholder. Project skill wrappers can point to the kit's shared PIXL/PLAR
  skills. The invocation-scoped `agents.pixl.config_file` route has native
  evaluation evidence; merely copying a role file does not establish discovery
  or loading. Retain the actual child identity when delegation is assigned.
- **Official PixelLab:** use the parent host's configured connection and inspect
  the current tool declarations. The [HTTP connection templates](../../../config/pixellab.codex.http.example.toml)
  and [Claude template](../../../config/pixellab.claude.http.example.json) are
  inactive examples. Local MCP setup does not create that connection. Preserve
  existing parent configuration rather than copying isolated-evaluation flags
  that exclude its servers.

## Read the setup report

The bootstrap command uses only the standard library, so it can report missing
runtime dependencies before ordinary local operations are available. With the
selected Python, run either the installed package or the copied runner:

```text
python -m pixl readiness --root CONSUMER --host codex --installation KIT
python ABSOLUTE_KIT/scripts/pixl.py readiness --root CONSUMER --host claude --installation ABSOLUTE_KIT
```

Use actual paths, quoting those containing spaces. `--host` and `--installation`
are optional when the available local context is sufficient; supplying them
makes the intended installation and host explicit. The command reads inputs and
resolves a relative installation path from the consumer root, never the server's
working directory. An absolute installation path can point outside the consumer.
It returns JSON without publishing project state. When local MCP is already loaded,
`pixl_readiness` exposes the same report; discover its exact argument schema.
The existing `ready`/`pixl_ready` operation still means production-state readiness.

Exit 0 means the local runtime requirements are satisfied, exit 1 means they are
incomplete, and exit 2 means invalid input. A zero exit is not proof of named-role
loading, official-tool access or authentication. Read each report group; the
top-level `status: reported` describes a report, not overall production readiness.

The report separates project/installation checks, dependency presence, specialist
observations, local operations and official tool visibility. File presence is a
static fact. Native role declarations, invocation/completion and successful local
tool calls are separate host observations. The runtime does not launch a child,
discover remote servers, test authentication, submit generation or infer artistic
acceptance. Authentication remains unverified by this report.
`specialist.instruction_loading` likewise stays `not_verified`; a caller's
availability observation is not an instruction-loading trace.

## Supply only observed host facts

If the caller has actual session observations, save a small JSON file inside the
consumer and pass its project-relative path with `--observations`. Its closed
envelope requires `host` (`codex` or `claude`) and an ISO timestamp with timezone
in `observed_at`. Optional fields are:

- `host_version`: the numeric version string reported by the executable.
- `named_role`: `available`, `unavailable` or `not_observed` in that invocation.
- `local_tools`: `{names: [...], complete_inventory: boolean}` using bare
  `pixl_*` operation names.
- `official_tools`: the same shape, using bare official names such as
  `pixelart_workbench`.

Record the actual observation time and version. Keep native identities, returned
files and invocation evidence in the caller's report; `named_role: available`
alone does not claim that the specialist completed work. Do not include raw host
configuration, credential values, authorization headers or environment dumps.
These supplied observations remain explicitly caller-supplied; the runtime does
not certify them as direct host discovery.

Missing observations remain unobserved. A tool absent from a partial inventory
is not known missing. Absence from a caller-supplied complete inventory means
only that it was not listed in that capture. A dated `pixl_capabilities` catalog
is documentation, not live official-tool visibility.

For useful local proof, read a known consumer source with `pixl_source` using its
exact file hash and retrieve installed library sources with `pixl_sources`.
Those successful calls establish the selected project root and installed
resources; a tool list alone does not. Preserve the source bytes and distinguish
these local observations from the official provider connection.

Return the observed root/installation, available evidence, specific missing setup
and next useful action. If official tools were not configured in an isolated
invocation, say that; do not invent an authentication failure or service outage.
Then follow [everyday production](everyday.md) under the caller's existing scope.
