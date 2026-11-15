# Measure retained operation costs

Use performance measurements to decide whether a real caller operation needs
optimization. Measure representative retained production histories first; keep
the source, state and evidence identities with the results. A large history or
report is a workload characteristic, not by itself a defect or a reason to add
a cache.

Run from the repository root in the selected development environment:

```powershell
.venv/Scripts/python.exe -B scripts/measure_performance.py --manifest path/to/measurement-manifest.json
```

The manifest selects the retained inputs and operations. Read it before running
the command. Use the manifest and source identities from an earlier result when
comparing runs; changing a path, history, focus or source revision changes the
comparison. The [TM-02 ledger](../evidence/performance/README.md) records the
selected workloads, exact replay driver and actual optimization decision. Its
driver reconstructs retained inputs in temporary roots and supplies a fresh
manifest; a manifest from a previous temporary directory is not a reusable
input after that directory is removed.

The version-1 manifest contains `cases`, each with `id`, `root`, `path` and
`focus`. `root` identifies the fixture root, relative to the checkout or as an
absolute path; `path` identifies its state relative to that root. Optional
`output_id` selects a family report. Optional `expected_errors` declares accepted
error codes by operation for a retained failing input. The measured refusal
remains an error observation, not a successful validation or context result.
Each declared refusal must actually occur; an unexpected success also fails.
Unexpected errors and changed inputs make the run fail.

Defaults are two warmups, 15 repeated samples and three fresh-process samples.
Use `--warmups`, `--iterations` and `--fresh-processes` to set these explicitly,
and retain the values with the result. `--timeout` limits each child process
(120 seconds by default). The command emits JSON on stdout and performs no
built-in evidence write, build, provider operation or network call. Exit 0 means
the measurement and preservation expectations were met, including any declared
refusals; exit 1 means a check failed, and exit 2 means configuration was invalid.

## What the measurements mean

Keep these costs distinct:

| Measurement | Interpretation |
| --- | --- |
| Context assembly | `authoring_context` and `complete_context`, including their actual dependencies |
| Parsing and loading | `parse` and `store_load`, measured separately from whole public operations |
| Hashing | `canonical_digest` and `raw_state_sha256`; canonical-state and raw file hashes are different domains |
| Validation | `structural_validation`, `file_validation` and public `validate_report`, with their current source dependencies |
| Reports and size | Optional `family_report`, plus separate public JSON serialization time and UTF-8 bytes; not a token count or a model-quality score |

Read each operation's recorded boundaries before comparing it with another.
Context and report operations may themselves load, validate, hash or serialize
inputs. Their timings overlap with component measurements and must not be added
together as if they were independent stages. Input counts and bytes describe the
tested history; synthetic scaling, if used, must be labeled separately from
retained production work.

Repeated samples in one process are warmed measurements: imports, runtime state
and filesystem caches may already be populated. A fresh Python process resets
that process's imports and memory, but does not flush the operating system's file
cache. Neither is a guaranteed cold-disk measurement. The fresh-process
authoring samples include startup, imports and full-result serialization, but
transport only a compact probe result. They do not measure full CLI output
transport. Keep those samples separate from warmed operation timings;
subprocess wall time is not pure operation time.

Use the raw nanosecond samples and reported median, p95, minimum and maximum,
together with the exact command,
interpreter, host and input identities. Background work, antivirus activity,
filesystem placement and scheduler variation can affect timings. A small
difference between runs does not establish an improvement. These measurements
set no service-level objective, responsiveness threshold or general scaling
guarantee.

## Retain a fresh attempt

The measurement operation reads the selected inputs. Capturing its output is a
separate write by the caller. Choose a new destination outside the measured
inputs, preserve stdout and stderr, and record the actual exit code even when a
run fails. For example:

```powershell
$perfRun = 'evidence/performance/20261114/measurement-NEW'
$perfManifest = 'path/to/measurement-manifest.json'
New-Item -ItemType Directory -Path $perfRun -ErrorAction Stop | Out-Null
@{
    working_directory = (Get-Location).Path
    executable = '.venv/Scripts/python.exe'
    arguments = @('-B', 'scripts/measure_performance.py', '--manifest', $perfManifest)
} | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath "$perfRun/command.json" -Encoding utf8
.venv/Scripts/python.exe -B scripts/measure_performance.py --manifest $perfManifest > "$perfRun/stdout.json" 2> "$perfRun/stderr.txt"
$perfExit = $LASTEXITCODE
@{ exit_code = $perfExit } | ConvertTo-Json | Set-Content -LiteralPath "$perfRun/exit.json" -Encoding utf8
```

Replace `measurement-NEW` with an unused attempt name. Directory creation must
succeed before invoking the command; never reuse a failed attempt's output
paths. A failure remains part of the evidence. Correct its cause and create a
separate attempt rather than editing the original samples or result.

The harness suppresses bytecode writes in its process and child processes.
`-B` alone does not make arbitrary commands read-only. Inspect a changed harness
or replay driver before running it. The harness compares its declared input,
runtime and manifest inventories, bytes and mtimes outside the timed region;
those checks establish only the recorded scope. The replay driver creates
temporary inputs and retained evidence outputs separately. Do not include
snapshotting, archive reconstruction or evidence capture in an operation timing
unless that is the operation being measured.

## Decide from evidence

Optimize only an observed cost that matters to the core workflow. Retain a
no-change decision when the measurements do not demonstrate a useful target.
If a bottleneck is demonstrated, preserve the baseline, change the narrowest
relevant implementation and repeat the same workloads and correctness checks.
The improvement must preserve exact output meaning and fail on changed inputs
when the existing contract requires it. A cache must respect source/content
identity; stale source files and old receipts must remain visible.

Do not run the [full verifier](VERIFICATION.md#rebuild-local-evidence-deliberately)
merely to obtain timings or validate documentation. It rebuilds tracked evidence
and the bundle, and its total duration measures a different workflow. Select
focused tests for an actual implementation change, and use the
[read-only integrity check](EVIDENCE-INTEGRITY.md) to inspect current applicability
without rewriting old results.

Local timings and output sizes do not establish native instruction following,
provider performance, artistic quality, target-engine acceptance or model
reasoning quality. Human acceptance stays separate; M1/M2 and broader M3/M4/M5
remain open.
