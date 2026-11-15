# Check operation boundaries

Publication, job observation, candidate review and handoff results now have
explicit Python shapes. They help maintainers catch mistakes such as treating an
observation receipt as dispatch permission, losing a publication hash, or reading
caller-only fields from a receipt-only handoff. Public JSON and saved-state formats
retain their existing contracts and runtime validation.

From the repository's selected development environment:

```powershell
.venv/Scripts/python.exe -B scripts/check_boundary_types.py
```

Use `--json` to retain the exact commands, input hashes, diagnostics and limits.
The gate runs configured mypy on the runtime and the
[positive consumers](../tests/typing/valid_boundaries.py), then checks that each
labeled mistake in the [negative fixture](../tests/typing/invalid_boundaries.py)
receives its expected diagnostic and that no extra errors appear. These files are
static examples: the gate never executes their operation calls. They are outside
the `test*.py` naming pattern used by unittest discovery.

Exit 0 means both the valid consumers and every expected refusal passed. Exit 1
means a checker result or diagnostic differed; exit 2 means the gate could not
complete its input/tool setup. Preserve stdout, stderr and the exit code in a
fresh location when recording evidence. Do not remove a negative marker merely
to make a failed gate pass; investigate the affected boundary.

The command uses a temporary mypy cache and removes it afterward. It suppresses
Python bytecode writes and performs no build, runtime fixture, provider operation
or model trial. Redirecting stdout creates the file chosen by the caller.

## Checked scope

`pyproject.toml` enables checking of untyped helper bodies, incomplete annotations
and `Any` returns for `operation_types`, `store`, `jobs`, `candidate_review`,
`handoff` and `caller_result`. Default mypy still checks the other runtime modules
at their existing annotation scope; this is not strict typing of the whole runtime.
The ordinary `.venv/Scripts/python.exe -B -m mypy pixl` command also applies those
overrides. The gate adds examples that demonstrate consumer-side checking and
discriminated legacy/durable job and present/absent caller branches.

Opaque provider requests, journals, lineage/family extensions, production
continuations and flexible UDL record fields retain their own runtime validators.
Known outer result fields are typed separately from those payloads. A typed
observation input does not establish that the observation happened, and a typed
dispatch result does not perform a provider call.

Types do not prove bounded text, valid hashes, safe paths, current state or exact
JSON integer semantics. In Python's static type system, `bool` is a subtype of
`int`; the existing runtime checks must still reject booleans where exact integers
are required. Run affected behavior tests and the appropriate
[verification tier](VERIFICATION.md) after implementation changes. Discovery,
static correctness, native behavior and actual outcomes remain distinct. Human
acceptance and M1/M2 and broader M3/M4/M5 remain open.
