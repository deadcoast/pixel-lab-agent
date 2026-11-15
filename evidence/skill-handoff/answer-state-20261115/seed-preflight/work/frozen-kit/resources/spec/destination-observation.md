# Destination observation import (NF-06)

This read-state operation validates a supplied destination report against an exact,
current family candidate and writes a fresh retained evidence export. It never runs
the renderer, changes `.px` state, creates E/V records, nominates a candidate, or
accepts art. A caller must actually inspect the returned PNG previews and make an
explicit [candidate review](candidate-review.md) when that work is justified.

The operation adds no UDL fields or migration. The existing
[PIXL-2](PIXL-2.md), `pixl/registry-v2.json`, and
[family-delivery](family-delivery.md) semantics remain authoritative. In particular,
a valid historical manifest is insufficient: its member selection and frozen plan
must still be current.

## Operation

Python:

```python
import_observation(doc, root, candidate_id, report_path, out)
```

`doc` is the already loaded state document; `root` is the declared consumer root.
`report_path` and `out` are canonical forward-slash relative paths beneath that root.
`out` must not exist. Absolute, parent-traversal, backslash, drive-prefixed and
redirected symlink paths are rejected. Inputs must be regular files. Source and
destination paths are declarations to validate and retain, never executable commands.

Public adapters expose `destination-import` and `pixl_destination_import`; the
service operation takes `path`, `candidate_id`, `report_path`, and `out`. The tool
reads state and writes evidence. Its state is unchanged, but its filesystem effects
must not be described as read-only.

```text
destination-import STATE CANDIDATE REPORT_JSON --out FRESH_DIR --root ROOT
```

As with ordinary CLI state commands, `STATE` resolves from the working directory
and must stay inside `ROOT`. `REPORT_JSON`, `FRESH_DIR`, and optional
`--result-path` resolve beneath `ROOT`. The MCP state `path` is consumer-relative.
The example queue runner's `renderer/observation.py --help` describes its optional
capture-to-report adapter, including the explicit member-output destination map.

## Version 1 report

The executable closed schema is `REPORT_SCHEMA` in
`pixl/destination_observation.py`. Every object rejects additional fields; every
listed field is required. Hashes are lowercase SHA-256. IDs and ordinary text are
nonblank strings. JSON duplicate keys, booleans used as numbers, nonfinite numbers,
and fractional JSON numbers used as integers are rejected.

| Field | Shape and meaning |
| --- | --- |
| `version` | Integer `1`. |
| `candidate` | Exact family X ID passed to the operation. |
| `binding_hash` | Current `review-context` semantic binding hash for that candidate. A state hash is not a substitute. |
| `manifest` | `{path, sha256}` exactly matching `review-context.candidate_file`. The actual canonical family manifest is verified and retained. |
| `observed_at` | ISO timestamp with an explicit timezone offset, no later than import time. This is supplied metadata, not an independently established capture time. |
| `renderer` | `{name, command, runtime, files}`. `command` is a nonempty argv string array; `runtime` is `{name, version}`; `files` is a nonempty array of `{path, sha256}` source identities. |
| `consumer_sources` | Nonempty array of `{path, sha256}` for declared consumer sources. |
| `destinations` | Exactly one `{output, candidate, path, sha256}` for each manifest member. `output`, `candidate`, and hash must identify that exact member. `path` names the actual supplied served copy to read and retain. |
| `viewport` | `{width, height, device_scale_factor}` with positive integer dimensions and positive finite scale factor. |
| `views` | Array of `{consumer, state, scale, output_id, member_outputs}`. `scale` is positive and finite. `output_id` references a declared PNG. `member_outputs` contains unique manifest output IDs; an empty list can describe a contextual view showing no member. |
| `motion` | Array of motion records described below. |
| `files` | Nonempty array of `{id, path, sha256, role}` with unique IDs and paths. `role` is `image`, `data`, or `log`; every `image` must verify as PNG. |
| `limitations` | Array of nonblank supplied limitations. Import does not replace or resolve them. |

A motion record is:

```json
{
  "consumer": "caller-defined consumer",
  "state": "caller-defined state",
  "mode": "caller-defined playback mode",
  "status": "observed",
  "frame_count": null,
  "frame_ms": null,
  "samples": [{"elapsed_ms": 0, "frame": null, "output_id": "view-0"}],
  "limitation": "Timing metadata was unavailable; sample bytes were supplied."
}
```

`status` is `observed` or `unavailable`. Observed motion requires one or more
samples; unavailable motion requires an empty sample list. `frame_count` is a
positive integer or `null`; `frame_ms` is a positive finite number or `null`.
Each sample has a nonnegative finite `elapsed_ms`, a nonnegative integer `frame`
or `null`, and an image `output_id`. Elapsed times strictly increase within each
motion record. When both frame index and frame count are known, the index must be
less than the count. Null means unknown; zero is not substituted for unknown
timing. Unavailable observations remain distinct from observed samples whose
metadata is partly unknown.

Consumer names, states, playback modes, view scales, frame timing and sample
counts remain caller-defined observations. The operation contains no `full` /
`compact`, 1x / 3x, looping, animation-quality, or artistic acceptance requirement.
Declared source completeness and provenance remain reviewer concerns: the importer
can verify declared bytes but cannot infer undeclared renderer dependencies.

## Validation and retained export

Before creating `out`, import validates the rooted state and exact family candidate,
current semantic binding, canonical manifest, all member destination hashes, every
declared source/output hash, and view/motion references. It snapshots all declared
bytes before export, rechecks them for changes, and revalidates state dependencies.
After writing the bundle and previews, it rechecks input bytes and state dependencies
again before writing the success receipt. This catches changes observed during the
operation; it does not lock the caller's working tree or attest execution history.

The fresh output contains:

- `<sha256>.zip`: a deterministic content-addressed archive with fixed generated
  internal paths. It retains the original report bytes as `report.json`, the actual
  canonical manifest as `package/manifest.json`, all declared renderer and consumer
  source bytes, all served destination copies, all declared output bytes, and
  `index.json`. The index maps original paths, hashes, sizes and output IDs to
  generated archive entries. ZIP timestamps, entry ordering and permissions are
  fixed; output directory names do not affect archive identity.
- `previews/NNNN.png`: exact copies of each declared image output, with measured
  dimensions and hashes returned for actual inspection.
- `result.json`: written last as the successful export receipt. A partially written
  directory is preserved on failure and cannot be reused by retry.

The importer only writes its own archive. It does not extract or execute archives.
The raw report and original paths remain traceable within the ZIP, while all retained
bytes use generated internal names.

The result includes state, candidate, binding, report and manifest identities;
declared renderer/consumer/destination/output identities; bundle and preview
references; supplied viewport/view/motion/limitation values; and explicit
`renderer_executed: false`, `state_changed: false`, and
`automatic_acceptance: false`. `files_verified: true` means declared byte identities
passed these checks, not that a renderer actually ran or art passed review.

`observation` is a ready `{path, sha256, mode: "live", note}` reference to the ZIP for
an explicit candidate review. The mode describes the supplied destination evidence
category. It does not attest execution or create a passing verdict. A reviewer can
also attach the separately inspected PNG previews with the mode required by the
criterion. Existing candidate-review retention copies the complete ZIP, so report
inputs and outputs survive removal of their original files and of this intermediate
export. This is why a report JSON alone is insufficient retention evidence.

## Resource bounds and failure behavior

The report and manifest use the existing codec document-size cap. Each captured
file is at most 64 MiB; unique captured bytes and assembled archive input bytes are
each at most 256 MiB. The final ZIP must be at most 64 MiB, matching the existing
candidate-review per-file limit. PNGs that trigger Pillow decompression-bomb limits
are rejected. Size bounds are retention safeguards, not asset design rules.

The closed schema additionally bounds text to 16,384 characters; argv to 256
entries; renderer files, consumer sources, destinations and motion records to 1,024
each; views to 4,096; files and samples per motion record to 16,384; viewport
dimensions and frame count to 65,536; scale factors to 64; and timing values to
10^12 milliseconds. The overall document and byte limits can be reached sooner.

Malformed/changed input or stale bindings fail before output publication when
detected during preparation. An I/O failure or detected input change after writing
starts preserves the partial export and omits its success receipt. No existing
evidence is overwritten or removed. A caller retains the failure, corrects the
cause, obtains current review context where needed, and chooses a fresh `out`.

These checks establish consistency and durable bytes. Runtime execution,
independent viewing, renderer provenance, useful artistic revision, and final target
acceptance need their own evidence; this import operation does not establish them.
