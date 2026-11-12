"""CF-10: useful real-provider assignments in the existing isolated consumers."""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path

from evaluations import integration_change_case, readiness_case
from evaluations.host_trials import inventory, sha, write_json
from evaluations.native_trial_records import reference
from evaluations.request_review_trials import ROOT

WORK = "work/native-production"
INPUTS = "work/native-production-inputs"
PLAR = "production-plar.txt"
AUTHORITY = "NATIVE-PRODUCTION.md"
KIT = readiness_case.KIT
CASES = {"codex": "queue-ready", "claude": "robot-directions"}


def prospective(root: Path, case: str) -> dict:
    """Create explicit new production scope without fabricating historic state."""
    doc = json.loads((root / "plar.txt").read_bytes())
    doc["project"]["brief"] = f"CF-10 authorized {case} production; original allocation remains in plar.txt."
    doc["sources"].append({"id": "cf10-authority", "path": AUTHORITY,
                           "sha256": sha(root / AUTHORITY)})
    for source in doc["sources"]:
        if case == "queue-ready" and source["path"] == "assets/ready-confirmed.png":
            source["path"] = f"{INPUTS}/original-ready.png"
        source["sha256"] = sha(root / source["path"])
    selected = "queue.ready" if case == "queue-ready" else "robot.directions"
    doc["coverage"]["included"].append("Explicit CF-10 production addendum and bounded actual consumer renderer")
    doc["coverage"]["unresolved"] = ["Current generated quality and destination acceptance require actual production and review."]
    for asset in doc["assets"]:
        asset.pop("production", None)
        asset["evidence"] = []
        asset["status"] = "todo" if asset["id"] == selected else "deferred"
        asset["next"] = ("Complete the explicit native production assignment." if asset["id"] == selected
                         else "Preserve existing art/source; no new production assigned for this row.")
        if case == "queue-ready":
            for requirement in asset["requirements"]:
                value = requirement.get("value")
                if isinstance(value, dict) and value.get("path") == "assets/ready-confirmed.png":
                    value["path"] = f"{INPUTS}/original-ready.png"
        if asset["id"] == selected:
            asset["requirements"].append({
                "property": "cf10_production_scope", "value": f"Official {case} production, actual inspection and caller consumption under NATIVE-PRODUCTION.md.",
                "authority": "requirement", "sources": ["cf10-authority"],
                "reason": "New explicit development-evaluation production authority; old plan-only/preserve-Ready scope is historical."})
            if case == "queue-ready":
                asset["existing"] = [{"path": f"{INPUTS}/original-ready.png",
                                      "role": "Preserved controlled-fixture style/meaning reference, not official generation."}]
            asset["questions"] = []
    return doc


def instructions(root: Path, host: str, python: Path) -> tuple[str, str]:
    case, role = CASES[host], "pixl" if host == "codex" else "pixl:pixl"
    kit = root / KIT
    guidance = f'''Explicit CF-10 native real-provider production evaluation: {case}.
Consumer root: {root.as_posix()}. Current kit: {kit.as_posix()}.
Python: {python.as_posix()}. Follow {AUTHORITY} as the current assignment.
Historical briefs and assignments remain evidence; this later addendum authorizes
only the specified useful production. Invoke the actual named {role} specialist.
Official PixelLab MCP and local PIXL are separately configured. Discover actual tools.
Do not inspect credential files/environment, change settings or persistent memory,
install packages, modify the installed kit, or work outside this consumer.
M1/M2 and broader M3 remain open. Retain all failures and actual provider identities.
'''
    if case == "queue-ready":
        task = f'''## Useful assignment: official Ready replacement

The accepted queue has real generated/revised Working, Retry and Paused but its
Ready member is still a controlled-fixture sample. Produce a useful official Ready
replacement for this existing consumer. This addendum supersedes only the old
PRODUCTION-STAGE.md preserve-Ready exclusion, within this isolated copy. The old
Ready bytes are preserved at {INPUTS}/original-ready.png with their origin identity.
The prospective queue's approved-ready source/requirement locator points to that
unchanged snapshot so delivering a new Ready cannot rewrite its style authority.
Preserve BRIEF.md, src/*, Start, Working, Retry and Paused exactly. Replace only
assets/ready-confirmed.png after preserving every candidate under {WORK} or the
new store. Original plar.txt and historical receipts remain unchanged.

Read the full current BRIEF.md and actual src/queue-view.ts. Ready remains a static
transparent 16x16 asymmetric check mark conveying success, coherent with the cool
blue queue family, distinguishable from Working/activity and Retry without color
alone. No fixed palette is imposed. Use actual uploaded reference pixels when
conditioning style. The existing Ready is a style/meaning reference, not evidence
that its historical simulated job was real. Preserve the distinction.

Select queue.ready from {PLAR}; create fresh production in .pixl/assets/queue.ready.
No historical producer state is reconstructed. Use the existing local public
operations for request preparation, durable jobs, candidate inspection/review,
delivery and handoff. The original source closure and art identities are in
{INPUTS}/origin.json. Existing accepted sibling art is destination context, not
newly generated work. Judge this Ready in both real queue consumers at 1x and 3x
nearest on #172336, including grayscale distinction and collective appearance.

The bounded actual renderer is renderer-native/. Run its existing capture and check:
`node renderer-native/capture.mjs --project . --out {WORK}/render-01`
`"{python.as_posix()}" renderer-native/check.py --project . --capture {WORK}/render-01`
Save full check stdout to a fresh JSON file. Inspect actual destination.png and
relevant retained native/3x cell PNGs with the host image tool; mechanical success
does not supply visual acceptance. Retain rejected captures; retry to a new output.
This directly exercises the existing renderer; do not invent a queue-motion
family manifest merely to fit a one-member production assignment.
'''
    else:
        task = f'''## Useful assignment: complete missing robot directions

The existing examples/delegation consumer has an approved identity fixture and
missing directional files. This later CF-10 addendum explicitly authorizes actual
official production, superseding only the old BRIEF.md plan-only/no-runner scope.
Keep the original brief, controller, source image and original plar.txt unchanged.
The old approval is within this representative fixture, not a real-game art claim.

Select robot.directions from {PLAR}, including robot.base's identity reference.
Inspect assets/robot-base.png first. Preserve its exact south PNG bytes as
assets/robot/south.png. Use the actual source pixels as the provider's existing
identity/south input, not a filename in a text description or a redesigned robot.
Generate the useful missing east, north and west views, separate transparent
32x32 PNGs at the controller's exact assets/robot/<direction>.png paths.
Inspect subject identity, proportions, palette, volume, direction and anchor/alignment
at native size and 3x nearest. Extra returned directions may be retained but are
not required delivered work. Do not regenerate the approved south for counts.

Use fresh .pixl/assets/robot.directions with ordinary public plan/job/review/family
operations. Multi-output plans require an explicit family delivery output/link;
do not declare the first single direction to satisfy the whole assigned family.
The bounded renderer-native/ imports actual src/robot.ts and observes all four
controller states. Run the copied renderer with these consumer-root paths:
`node renderer-native/capture.mjs --project . --out {WORK}/render-01`
`"{python.as_posix()}" renderer-native/check.py --project . --capture {WORK}/render-01 --out {WORK}/renderer-check-01.json`
Read renderer-native/README.md for its contract. Save exact returned reports and
inspect destination.png and all actual 1x/3x cells
with the host image tool. It is a supporting CF-10 renderer, not broad TM-08 or
game-engine qualification. Current acceptance requires actual visual judgment.
'''
    assignment = f'''# CF-10 native production assignment

{guidance}
{task}
## Scope, payment and source authority

This is authorized useful official PixelLab work in the existing representative
consumer. Use the current official platform docs https://www.pixellab.ai/docs and
MCP reference https://api.pixellab.ai/mcp/docs and actual discovered declarations.
The scoped evaluation spending limit is **20 subscription generations for this
host assignment**, including revisions. It is an execution budget, not an aesthetic
rule. Discover current operation cost before each paid call; keep actual reported
usage and starting/ending balance. Free reference upload, discovery, retrieval and
deterministic PixelLab corrections are authorized. No unrelated account changes,
deletion, publication or repeated calls just for test counts. Stop new paid work
if the remaining limit cannot cover it; preserve a useful partial continuation.
Never silently retry an ambiguous paid submission; reconcile its actual identifier.

Do not read tokens, auth configuration or secret environment variables. The host
connection supplies authentication. Save tool schemas/discovery with the observed
clock, exact arguments and authorization scope, without credentials. Preserve
failed results, mistaken calls and revisions rather than rewriting receipts.

## Native caller and specialist collaboration

The caller must invoke one actual named `{role}` specialist with this whole
assignment, consumer root, kit and Python. Codex uses agent_type="pixl" with
fork_turns="none". A generic substitute is not qualification. Retain the actual
child identity, wait for it, and use the same child for feedback/recovery.
The specialist reads the installed shared skill {kit.as_posix()}/skills/pixl/SKILL.md
and profile, then the relevant public workflow references and actual consumer.

First the specialist saves a concrete source-bound request/criteria packet and
literal review context for the caller, including actual provider image inputs and
the full delivered scope. Before paid dispatch, the caller independently reads
the original sources/reference pixels and exact packet, compares **every criterion**
and source/choice interpretation, writes {WORK}/COMPARISON.json, and sends its
findings to the same child. Correct contradictions before dispatch. Scope expert
choices honestly; do not promote a sample recipe into an owner requirement.
The caller must remain active through the complete result. A background child
launch plus a final 'waiting' message is an incomplete assignment.

The specialist then completes the authorized useful production: durable local
preparation and dispatch claim BEFORE each official host call, actual returned ID
and observations, retrieval/import of exact downloaded bytes, native/enlarged
inspection, appropriate revision if required, actual consumer rendering, explicit
candidate/family review and acceptance only when justified, PLAR and caller handoff.
Use `--help`/actual MCP schemas; only supply result_path where advertised. Existing
CLI stdout capture is a valid full-result route. Read full exact report locators.
The host's actual official call establishes provider execution; local J records or
handwritten assertions do not. Do not create fake provider IDs or fixture responses.

Write {WORK}/SPECIALIST-RESULT.json with: status, scope, source_refs,
comparison_ref, provider_operations (tool, actual_id, job, arguments_ref,
response_ref, observed_usage), delivered_files (path/sha256 and role),
state_ref, plar_ref, review_refs, renderer_report_ref, renderer_check_ref,
viewed_images (path/sha256), handoff_ref, lineage_findings, preservation,
failures_and_recovery, limitations, next_action. Use exact file references;
include actual operations only, and keep generated/edited/reused members distinct.
All fresh work reports/art candidates belong under {WORK} or the fresh .pixl store;
only assigned delivered destinations and {PLAR} may change outside those folders.

Caller: independently inspect the specialist result, provider receipts, actual
files and renderer evidence. Use an image tool to inspect the final generated
files/reference and rendered destination at 1x/3x, compare actual identities and
source mapping, and consume the compact public caller handoff including exact
full retrievals where needed. Do not duplicate paid work for verification. Write
{WORK}/CALLER-RESULT.json with native_child, specialist_result, comparison_ref,
provider_operations, delivered_files, viewed_images, renderer_report_ref,
renderer_check_ref, handoff_ref, independent_checks, status, preservation,
guided_recovery, limitations and next_action. A status of delivered requires the
whole assignment and actual consumption. Honest incomplete output retains its
specific missing acceptance and resumable next action. Do not close M1/M2 or
broader M3, general artistic quality or host reliability.
'''
    return guidance, assignment


def prepare(destination: Path, host: str, python: Path, *, package: Path | None = None,
            consumer: Path | None = None) -> Path:
    case = CASES[host]
    destination, python = destination.resolve(), python.resolve()
    root = readiness_case.prepare(destination, host, "clean", python, package=package, consumer=consumer)
    source = integration_change_case.SOURCE if case == "queue-ready" else ROOT / "examples/delegation"
    paths = (integration_change_case.source_paths(source) if case == "queue-ready" else
             ["BRIEF.md", "README.md", "plar.txt", "src/robot.ts", "assets/robot-base.png"])
    if case == "queue-ready":
        paths = sorted(set(paths) | {"PRODUCTION-STAGE.md"})
    for name in paths:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)
    (root / WORK).mkdir(parents=True)
    (root / INPUTS).mkdir(parents=True)
    renderer = (root / KIT / "resources/examples/plar-project/renderer" if case == "queue-ready"
                else root / KIT / "resources/examples/delegation/renderer")
    shutil.copytree(renderer, root / "renderer-native", ignore=shutil.ignore_patterns("__pycache__"))
    if case == "queue-ready":
        shutil.copyfile(root / "assets/ready-confirmed.png", root / INPUTS / "original-ready.png")
    write_json(root / INPUTS / "origin.json", {
        "source": str(source), "files": {name: sha(root / name) for name in paths},
        "scope": "Exact tracked consumer/source/art closure; fresh production, no reconstructed historical producer store.",
        "old_ready_provenance": "controlled fixture" if case == "queue-ready" else None,
    })
    guidance, assignment = instructions(root, host, python)
    (root / AUTHORITY).write_text(assignment, encoding="utf-8")
    for name in ("AGENTS.md", "SESSION.md"):
        (root / name).write_text(guidance, encoding="utf-8")
    write_json(root / PLAR, prospective(root, case))
    (destination / "prompt.txt").write_text(guidance + f"\nComplete {AUTHORITY}.\n", encoding="utf-8")
    launch = json.loads((destination / "launch.json").read_bytes())
    launch.update(case="native-production-" + case, artifact_roots=[WORK, ".pixl", "assets/robot", PLAR])
    write_json(destination / "launch.json", launch)
    identity = json.loads((destination / "identity.json").read_bytes())
    identity.update(case=case, inputs=inventory(root, ("__pycache__",)),
                    origin=reference(root / INPUTS / "origin.json"),
                    assignment=reference(root / AUTHORITY), runner=reference(Path(__file__)),
                    authorized_changes=[PLAR, *( ["assets/ready-confirmed.png"] if case == "queue-ready" else [])],
                    authorized_new_prefixes=[WORK + "/", ".pixl/", *( ["assets/robot/"] if case == "robot-directions" else [])])
    write_json(destination / "identity.json", identity)
    (destination / "runner.py.txt").rename(destination / "setup-runner.py.txt")
    shutil.copyfile(__file__, destination / "runner.py.txt")
    return root


def retain(destination: Path, *, baseline: Path | None = None) -> None:
    """Retain all production changes, including ignored state, and preserve failures."""
    if (destination / "preservation.json").exists():
        raise ValueError("Use a fresh continuation destination; prior receipts are immutable")
    identity = json.loads(((baseline or destination) / "identity.json").read_bytes())
    root = Path(json.loads((destination / "launch.json").read_bytes())["cwd"])
    current = inventory(root, ("__pycache__",))
    changed = [name for name, digest in identity["inputs"].items() if current.get(name) != digest]
    new = {name: digest for name, digest in current.items() if name not in identity["inputs"]}
    allowed = identity["authorized_changes"]
    prefixes = tuple(identity["authorized_new_prefixes"])
    unexpected = [name for name in changed if name not in allowed] + [name for name in new if not name.startswith(prefixes)]
    if (root / WORK).is_dir():
        shutil.copytree(root / WORK, destination / "outputs")
    delta = sorted(set(changed) | set(new))
    with zipfile.ZipFile(destination / "consumer-delta.zip", "x", zipfile.ZIP_DEFLATED) as archive:
        for name in delta:
            if (root / name).is_file():
                archive.write(root / name, name)
    write_json(destination / "preservation.json", {
        "changed": changed, "new": new,
        "removed": [name for name in identity["inputs"] if name not in current],
        "unexpected": unexpected, "delta": reference(destination / "consumer-delta.zip"),
        "scope": "Actual production delta and original input preservation; no artistic acceptance inferred."})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("destination", type=Path)
    prep.add_argument("--host", choices=CASES, required=True)
    prep.add_argument("--python", type=Path, default=readiness_case.DEFAULT_PYTHON)
    prep.add_argument("--package", type=Path)
    execute = sub.add_parser("run")
    execute.add_argument("destination", type=Path)
    execute.add_argument("--timeout", type=float, default=1800)
    args = parser.parse_args()
    from evaluations import native_provider
    if args.action == "prepare":
        root = prepare(args.destination, args.host, args.python, package=args.package)
        native_provider.configure(args.destination)
        print(json.dumps({"consumer": str(root), "launched": False}))
    else:
        native_provider.run(args.destination, timeout=args.timeout)
        retain(args.destination)


if __name__ == "__main__":
    main()
