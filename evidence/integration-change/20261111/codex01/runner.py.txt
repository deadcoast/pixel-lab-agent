"""CF-07: a source timing change over exact retained art and a fresh local intent."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from evaluations import readiness_case
from evaluations.host_trials import inventory, sha, write_json
from evaluations.native_trial_records import reference
from evaluations.request_review_trials import ROOT, run

WORK = "work/integration-change"
INPUTS = "work/integration-inputs"
KIT = readiness_case.KIT
SOURCE = ROOT / "evidence/pixellab-family-production/20261108/project"
PLAR = "integration-plar.txt"
TIMING = "src/working-timing.ts"
AUTHORITY = "WORKING-TIMING-AMENDMENT.md"
WRAPPER = "src/queue-view-integration.ts"
RENDERER = "renderer-integration"
ASSETS = ("queue.ready", "queue.working", "queue.retry", "queue.start", "queue.paused")
ART = ("assets/start.svg", "assets/working.png", "assets/ready-confirmed.png",
       "assets/error-retry.png", "assets/paused.png")
RENDERER_FILES = ("capture.mjs", "server.mjs", "view.mjs", "index.html", "check.py")
WRAPPER_TEXT = '''import { display as originalDisplay } from "./queue-view.ts";
import { frameMs } from "./working-timing.ts";
export { statusVisuals, statusCell, compactStatus, accountBadge } from "./queue-view.ts";
export const display = { ...originalDisplay, frameMs };
'''


def amendment(frame_ms: int) -> str:
    return f'''# Controlled evaluation authority: Working timing

This explicit CF-07 evaluation amendment supersedes only the Working frame duration
of 100 ms in the preserved historical BRIEF.md and src/queue-view.ts. The current
authorized duration is {frame_ms} ms per frame, four frames, looping, a {4 * frame_ms} ms cycle.
src/working-timing.ts is the dedicated executable timing source. The stable
src/queue-view-integration.ts wrapper applies it to display.frameMs in the actual
renderer while reusing both original statusCell and compactStatus consumers.

All other brief requirements and the retained source-defined visual roles remain.
Reuse the exact existing assets/working.png bytes; this is a timing integration
change, with no new art or provider execution authorized. All five original art
files and original shared sources must remain unchanged. Inspect real rendered
stills in both consumers at 1x and 3x nearest on the existing dark panel. Observe
actual live loop playback at the consumer's enlarged 3x scale in both consumers.
Native 1x live playback remains unperformed; controlled 1x frame-boundary samples
are a separate observation. The original brief requires 1x/3x inspection, not live
playback at every inspection scale.
Fresh current review and acceptance must not be inferred from historical evidence.
'''


def source_paths(source: Path) -> list[str]:
    """An explicit tracked source closure, excluding ignored producer state."""
    document = json.loads((source / "plar.txt").read_bytes())
    paths = {"BRIEF.md", "plar.txt", "src/queue.ts", "src/queue-view.ts", *ART,
             *(row["path"] for row in document["sources"]),
             *(f"renderer-recheck/{name}" for name in RENDERER_FILES)}
    for name in paths:
        target = (source / name).resolve()
        if not target.is_relative_to(source.resolve()) or not target.is_file():
            raise ValueError("The retained source closure is incomplete: " + name)
    # The checked-in closure is the authority even when tests copy it to a temp tree.
    tracked = set(subprocess.check_output(["git", "ls-files", "--", str(SOURCE)], cwd=ROOT,
                                         text=True, encoding="utf-8").splitlines())
    prefix = SOURCE.relative_to(ROOT).as_posix() + "/"
    if any(prefix + name not in tracked for name in paths):
        raise ValueError("The evaluation source closure must be Git tracked")
    return sorted(paths)


def prospective(root: Path) -> dict:
    """Preserve normative clauses, but create no fictional historical state."""
    document = json.loads((root / "plar.txt").read_bytes())
    document["project"]["brief"] = "Fresh prospective CF-07 integration evaluation over retained production art; original allocation and evidence are historical inputs."
    document["coverage"] = {
        "included": ["Original brief, shared source, all five exact art files and source-linked normative clauses retained.",
                     "Fresh prospective allocation and store, not a continuation of ignored original producer state.",
                     "Stable renderer and wrapper established before the controlled Working-only timing change."],
        "excluded": ["New art, provider execution, remote account badge registry, and changes to unrelated assets."],
        "unresolved": ["Current integration review and acceptance require a fresh capture after the timing amendment."],
    }
    for source in document["sources"]:
        source["sha256"] = sha(root / source["path"])
    document["sources"].extend({"id": id_, "path": path, "sha256": sha(root / path)} for id_, path in (
        ("working-timing", TIMING), ("timing-authority", AUTHORITY), ("integration-wrapper", WRAPPER),
        ("integration-renderer", f"{RENDERER}/view.mjs")))
    for asset in document["assets"]:
        asset.pop("production", None)
        asset["evidence"] = []
        asset["status"] = "todo" if asset["id"] == "queue.working" else "deferred"
        asset["next"] = "Fresh timing integration evaluation only." if asset["id"] == "queue.working" else "Preserve exact existing art and allocation; no new production in this evaluation."
        asset["existing"] = [{"path": asset["delivery"]["path"],
                              "role": "Exact retained art; historical origin is not current evaluation acceptance."}]
        if asset["id"] != "queue.working":
            continue
        asset["requirements"] = [r for r in asset["requirements"] if r["property"] != "renderer_frame_extraction"]
        timing = next(r for r in asset["requirements"] if r["property"] == "animation")
        timing.update(value={"frame_duration_ms": 100, "loop": True, "nominal_cycle_ms": 400},
                      sources=["working-timing", "timing-authority"],
                      reason="Explicit evaluation amendment controls timing; the dedicated module drives both consumers through the stable wrapper.")
        asset["consumers"].append({"source": "integration-wrapper", "symbol": "display",
                                   "usage": "Binds the dedicated Working frame duration to both original consumers."})
        asset["requirements"].append({"property": "renderer_frame_extraction", "value": "Retained renderer applies display.frameMs; current rendered observation is still required.",
                                       "authority": "observation", "sources": ["integration-renderer", "integration-wrapper"],
                                       "reason": "Stable evaluation adapter exists before baseline preparation; presence alone is not rendered acceptance."})
        asset["delivery"]["checks"] = ["Preserve the exact existing four-frame 64x16 Working sheet.",
                                        "Inspect statusCell and compactStatus stills at 1x and 3x nearest, and observe current amended live timing at 3x in both consumers; 1x live playback remains unperformed.",
                                        "Freshly review activity, alpha, readability and distinction from success and paused on the actual dark panel."]
    return document


def _seed_packet(root: Path, selected: dict) -> None:
    sources = [{"path": s["path"], "sha256": s["sha256"], "role": "selected source requirement"} for s in selected["sources"]]
    criterion_sources = [{"path": name, "locator": label} for name, label in (
        ("BRIEF.md", "Asset brief and current updates"), (AUTHORITY, "Current Working timing authority"),
        ("src/queue-view.ts", "statusVisuals, statusCell, compactStatus and display"))]
    criteria = [{"id": id_, "domain": domain, "mode": mode, "check": check,
                 "basis": "Preserved source-defined constraints and explicit Working timing amendment.",
                 "scope": "This exact Working candidate in the retained queue consumer.", "sources": criterion_sources}
                for id_, domain, mode, check in (
                    ("canvas", "mechanical", "local", "Exact retained transparent 64x16 sheet, four horizontal 16x16 frames; unchanged art bytes."),
                    ("activity", "visual", "visual", "Readable cool-blue activity at 1x and 3x nearest on the dark panel; distinct from success, retry and paused; scoped coherent treatment with retained Ready reference."),
                    ("integration", "engine", "live", "Observe the exact Working sheet in both actual consumers with four looping frames at current authorized 100 ms each, nearest filtering and transparent compositing."))]
    plan = {"version": 1, "scope": "Controlled local preparation only; no provider execution or acceptance.", "outputs": [{
        "id": "working", "name": "Working timing integration", "kind": "animation",
        "contract": {"size": [64, 16], "palette": [], "view": "ui", "sampling": "nearest", "alpha": "full",
                     "intent": "Reuse exact four-frame Working sheet; 100 ms per frame, looping; activity distinct from success and paused."},
        "criteria": criteria}]}
    write_json(root / INPUTS / "arguments-100.json", {"description": "Controlled unsubmitted Working intent: four horizontal 16x16 activity frames, transparent, cool blue, 100ms each.",
                                                     "width": 64, "height": 16, "no_background": True})
    write_json(root / INPUTS / "criteria-100.json", plan)
    write_json(root / INPUTS / "packet-100.json", {"version": 1, "requirements_hash": selected["requirements_hash"],
        "sources": sources, "request": {"path": f"{INPUTS}/arguments-100.json", "sha256": sha(root / INPUTS / "arguments-100.json"),
        "kind": "provider_arguments", "tool": "create_image_pro_flash"},
        "criteria": {"path": f"{INPUTS}/criteria-100.json", "sha256": sha(root / INPUTS / "criteria-100.json")}, "choices": []})
    schema = {"type": "object", "properties": {"description": {"type": "string"},
        "width": {"type": "integer", "minimum": 16, "maximum": 256, "multipleOf": 4},
        "height": {"type": "integer", "minimum": 16, "maximum": 256, "multipleOf": 4}, "no_background": {"type": "boolean"}},
        "required": ["description", "width", "height", "no_background"], "additionalProperties": False}
    write_json(root / INPUTS / "connection.json", {"provider": "pixellab", "schema": schema,
        "discovery": {"source": "Controlled CF-07 local preparation schema, not a live provider discovery", "observed_at": datetime.now(UTC).isoformat(),
                      "evidence": {"controlled_fixture": True, "live_discovery": False}},
        "authorization": {"scope": "Local intent preparation only; no dispatch execution or provider call authorized", "evidence": {"controlled_fixture": True}}})


def prepare(destination: Path, host: str, python: Path, *, package: Path | None = None,
            consumer: Path | None = None, source: Path = SOURCE) -> Path:
    source = source.resolve()
    paths = source_paths(source)
    consumer = readiness_case.prepare(destination, host, "clean", python, package=package, consumer=consumer)
    destination, python = destination.resolve(), python.resolve()
    kit = consumer / KIT
    original = {}
    for name in paths:
        target = consumer / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)
        original[name] = sha(target)
    (consumer / WORK).mkdir(parents=True)
    (consumer / RENDERER).mkdir()
    for name in RENDERER_FILES:
        shutil.copyfile(ROOT / "examples/plar-project/renderer" / name, consumer / RENDERER / name)
    view = consumer / RENDERER / "view.mjs"
    view.write_bytes(view.read_bytes().replace(b"'/src/queue-view.ts'", b"'/src/queue-view-integration.ts'"))
    shutil.copyfile(ROOT / "examples/plar-project/renderer/observation.py", consumer / RENDERER / "observation.py")
    (consumer / WRAPPER).write_text(WRAPPER_TEXT, encoding="utf-8", newline="\n")
    (consumer / TIMING).write_text("export const frameMs = 100;\n", encoding="utf-8")
    (consumer / AUTHORITY).write_text(amendment(100), encoding="utf-8")
    write_json(consumer / PLAR, prospective(consumer))

    def public(*args):
        command = [str(python), "-B", str(kit / "scripts/pixl.py"), *args, "--root", str(consumer)]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=False, timeout=30)
        if result.returncode:
            raise ValueError("Fixture public operation failed: " + result.stderr + result.stdout)
        return json.loads(result.stdout)

    selected = public("plar", "read", "--path", PLAR, "--asset", "queue.working")
    _seed_packet(consumer, selected)
    prepared = public("plar", "prepare", "--path", PLAR, "--asset", "queue.working", "--requirements", selected["requirements_hash"],
                      "--packet", f"{INPUTS}/packet-100.json", "--connection", f"{INPUTS}/connection.json")
    write_json(consumer / INPUTS / "prepared-100.json", prepared)
    write_json(destination / "baseline-prepare.json", prepared)
    selections = {asset: public("plar", "read", "--path", PLAR, "--asset", asset) for asset in ASSETS}
    write_json(destination / "baseline-selections.json", selections)
    write_json(destination / "baseline-queue.json", public("plar", "read", "--path", PLAR))
    shutil.copyfile(consumer / PLAR, destination / "baseline-plar.txt")
    shutil.copytree(consumer / ".pixl", destination / "baseline-pixl")
    before = inventory(consumer, ("__pycache__",))
    write_json(destination / "before-change-files.json", before)
    (consumer / TIMING).write_text("export const frameMs = 150;\n", encoding="utf-8")
    (consumer / AUTHORITY).write_text(amendment(150), encoding="utf-8")
    after = inventory(consumer, ("__pycache__",))
    changed = sorted(p for p in before if before[p] != after.get(p))
    if changed != sorted([TIMING, AUTHORITY]):
        raise ValueError("Controlled source change altered unexpected files")
    write_json(destination / "source-change.json", {"before": {p: before[p] for p in changed}, "after": {p: after[p] for p in changed},
               "old_frame_ms": 100, "new_frame_ms": 150, "art_changed": False, "remote_executed": False})
    write_json(consumer / INPUTS / "fixture.json", {"plar": PLAR, "asset_id": "queue.working", "old_prepare": f"{INPUTS}/prepared-100.json",
        "old_requirements_hash": selected["requirements_hash"], "old_job_id": prepared["job"]["id"], "store": prepared["store"],
        "changed_sources": [TIMING, AUTHORITY], "old_frame_ms": 100, "new_frame_ms": 150,
        "exact_art": {p: original[p] for p in ART}, "original_state_retained": False,
        "scope": "Fresh prospective state over a tracked historical source/art closure; no provider call authorized."})
    guidance, assignment = instructions(consumer, host, python)
    for name in ("AGENTS.md", "SESSION.md"):
        (consumer / name).write_text(guidance, encoding="utf-8")
    (consumer / "INTEGRATION-ASSIGNMENT.md").write_text(assignment, encoding="utf-8")
    (destination / "prompt.txt").write_text(guidance + "\nComplete INTEGRATION-ASSIGNMENT.md.\n", encoding="utf-8")
    launch = json.loads((destination / "launch.json").read_bytes())
    launch.update(case="integration-change", artifact_roots=[WORK])
    write_json(destination / "launch.json", launch)
    identity = json.loads((destination / "identity.json").read_bytes())
    identity.update(case="integration-change", inputs=inventory(consumer, ("__pycache__",)), original_inputs=original,
                    source_consumer=str(source), baseline_selections=selections, baseline_hash=sha(destination / "baseline-plar.txt"),
                    baseline_prepare=prepared, baseline_document=json.loads((destination / "baseline-plar.txt").read_bytes()),
                    fixture={"plar": PLAR, "changed_asset": "queue.working", "unaffected_assets": [a for a in ASSETS if a != "queue.working"],
                             "timing_source": TIMING, "authority": AUTHORITY, "old_frame_ms": 100, "new_frame_ms": 150,
                             "art": {p: original[p] for p in ART}, "fresh_prospective_store": True,
                             "retained_source_paths": paths, "original_producer_state_retained": False},
                    brief=reference(consumer / "BRIEF.md"), runner=reference(Path(__file__)))
    write_json(destination / "identity.json", identity)
    (destination / "runner.py.txt").rename(destination / "setup-runner.py.txt")
    shutil.copyfile(__file__, destination / "runner.py.txt")
    return consumer


def instructions(root: Path, host: str, python: Path) -> tuple[str, str]:
    kit = root / KIT
    role = "pixl" if host == "codex" else "pixl:pixl"
    guidance = f'''Explicit CF-07/NF-06 native production-profile evaluation.
Root: {root.as_posix()}; frozen kit: {kit.as_posix()}; Python: {python.as_posix()}.
Read INTEGRATION-ASSIGNMENT.md. Delegate to actual named {role}; load its production
profile and PIXL/PLAR skills. No generic substitute or allocation-only exemption.
Preserve original source/art, plar.txt, baseline inputs, all history and old jobs.
Update only {PLAR} and public prospective state; add evidence under {WORK}.
No provider execution, new art, source edits, configuration changes or memory edits.
The two controlled source changes already exist. M1/M2 and broader M3 remain open.
'''
    assignment = f'''# Continue the changed Working integration

This controlled evaluation preserves historical source/art inputs, but has a fresh
prospective allocation {PLAR} and a genuine public prepared, unsubmitted 100ms job.
It does not retain the ignored original producer store. {INPUTS}/fixture.json names
the exact baseline. Only {TIMING} and {AUTHORITY} changed to150ms after preparation.
Original BRIEF100ms remains historical; the explicit amendment supersedes only timing.

Use one actual {role} specialist (Codex agent_type=pixl, fork_turns=none). Give it the
root and this whole assignment. The specialist must read the installed
{(kit / 'skills/pixl/SKILL.md').as_posix()}, its shared production profile and workflow
references plus {(kit / 'skills/plar/SKILL.md').as_posix()}. Use configured local MCP
or the same frozen kit CLI. Save complete actual operation returns, including errors,
to fresh files; never manually transcribe reports, invent observations or overwrite failures.
Prefer direct MCP calls with result_path where supported, or explicit frozen-kit CLI
commands retaining actual stdout/stderr. For helper-mediated operations retain the
exact helper source/hash and operation/result bindings; hidden execution or copied
narrative JSON alone does not establish a public operation happened.

Specialist workflow:
1. Inspect the current brief, amendment, shared source, dedicated timing, wrapper,
   actual retained art and renderer. Read {PLAR} publicly and save initial-read.json.
   Establish source identities and both consumers. Preserve all IDs, unrelated rows,
   existing production lineage and unchanged source bindings. Refresh only Working's
   changed source hashes/timing requirement through pixl_plar_save; save allocation-save.json
   and final-document.json. Save a current focused read as current-selection.json.
2. Attempt the public job-dispatch preparation for the obsolete original job and
   retain the actual refusal as obsolete-dispatch.json. This tool only prepares a
   guarded dispatch description; DO NOT execute any provider call even if returned.
   Also attempt public completion of the old task and save obsolete-completion.json.
   Report the precise actual refusal cause: missing candidate/verdicts is not proof
   that a stale-selection guard ran. Neither refusal permits you to alter old intent.
   Preserve the old job/input bytes. Since the job was never submitted, use public
   job-observe failed with explicit LOCAL abandonment evidence, not a provider failure
   claim. Save old-abandon.json. Inspect actual job/state before choosing arguments.
3. Author a new request packet/criteria/contract at150ms with exact current selected
   sources; all other artistic/source constraints remain. Public pixl_plar_prepare
   revise=true with current state hash must create a successor plan; save revised-prepare.json.
   Abandon this new unsubmitted intent locally as well because exact art reuse makes
   provider execution unnecessary; save new-abandon.json. Never claim remote failure.
4. Append a fresh typed candidate X for the exact existing assets/working.png through
   public commit, binding the revised output and contract and noting historical-byte
   provenance. No job-import because there is no succeeded remote job. Inspect its
   current candidate-review context. Perform fresh local measurements and visual
   review of actual pixels, and the actual both-consumer capture for live criteria.
   Retain all observations and verdicts. Do not reuse historical100ms acceptance.
5. Adopt this freshly accepted revised sample using the public supported workflow.
   Use pixl_production_plan with stages:[] for one existing member output, the accepted
   sample baseline and explicit confirmed destination. Author scoped family criteria
   covering current150ms integration. This delivery-only plan needs no dummy generation
   stage. Build the family/package through public operations and obtain candidate-review
   context for its delivery candidate. Save delivery-context.json and delivery-build.json.
6. Run the real browser capture: node {RENDERER}/capture.mjs --project ROOT --out FRESH_DIR
   under {WORK}. Run {RENDERER}/check.py on capture output and retain command/stdout/stderr.
   The renderer already imports the stable wrapper and measures actual150ms playback
   at3x in statusCell and compactStatus; actual still views cover1x/3x. Controlled1x
   frame-boundary samples are separate; 1x live playback remains unperformed. Do not
   patch sources or synthesize images.
   For sample review you may capture first, then capture the delivery candidate freshly.
   Use {RENDERER}/observation.py --help to bridge raw capture + delivery review context
   + explicit member-output-to-served-path mapping into a structured report. Save it as
   destination-report.json. Call public pixl_destination_import for the exact delivery
   candidate and fresh bundle path; save destination-import.json. Import retains supplied
   observation bytes; it does not execute the renderer, award verdicts or accept the package.
7. Open the actual destination screenshot and native/enlarged Working views. Review
   timing, activity readability, transparency, family distinctions and both consumers;
   record fresh observations and public candidate review with truthful modes. The NF06
   bundle supplies live evidence; visual judgments require actual image inspection.
   Accept/complete only after current required criteria pass. Save delivery-review.json,
   acceptance.json and final-selection.json. Finish public plar handoff, view=caller,
   saving its exact output as handoff.json. Scope acceptance to this controlled reused-art
   timing change; broader artistic production, host reliability and milestones remain open.

All filenames above live under {WORK}. Write SPECIALIST-RESULT.json with exact
path/sha256 references for initial_read, allocation_save, final_document,
current_selection, obsolete_dispatch, obsolete_completion, old_abandon, revised_prepare, new_abandon,
sample_review, delivery_build, delivery_context, capture_report, renderer_check, destination_report,
destination_import, delivery_review, acceptance, final_selection, handoff;
include candidate/output/task IDs, scope, limitations and next_action.

Parent: independently consume actual public reports and final PLAR/state, compare
all five original art hashes and unchanged source identities, verify selected identity
changed only for Working, original prepared intent/history remain and no remote ID or
provider execution was invented. Independently inspect destination screenshot and
both actual consumer views. Check package member hashes against served destinations
and current150ms report, without substituting narrative claims for retained outputs.
Call public PLAR read since the baseline PLAR hash and save parent-refresh.json;
focused reads of all five asset IDs go in parent-selections.json. Save public current
acceptance report as parent-acceptance.json. Write CALLER-RESULT.json with native_child
(actual canonical path/ID), specialist_result, parent_refresh, parent_selections,
parent_acceptance, handoff (all exact path/sha256 refs), independent_checks, scope,
limitations and next_action. A successful controlled timing change is not M1/M2 or
broaderM3 closure. If incomplete, preserve truthful progress and exact blockers.
'''
    return guidance, assignment


def retain(destination: Path) -> None:
    """Retain all prospective state/history and changed-source evidence without overwrite."""
    names = ("preservation.json", "outputs", "final-plar.txt", "final-pixl", "retained-inputs")
    if any((destination / name).exists() for name in names):
        raise ValueError("Preserve prior retention; use a separate continuation record")
    launch, identity = (json.loads((destination / name).read_bytes()) for name in ("launch.json", "identity.json"))
    root = Path(launch["cwd"])
    for source, target in ((WORK, "outputs"), (".pixl", "final-pixl"), (INPUTS, "retained-inputs")):
        if (root / source).is_dir():
            shutil.copytree(root / source, destination / target)
    if (root / PLAR).is_file():
        shutil.copyfile(root / PLAR, destination / "final-plar.txt")
    current = inventory(root, ("__pycache__",))
    write_json(destination / "preservation.json", {"changed": [p for p, digest in identity["inputs"].items() if current.get(p) != digest],
        "added": {p: digest for p, digest in current.items() if p not in identity["inputs"]},
        "final_files": current})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("destination", type=Path)
    prep.add_argument("--host", choices=("codex", "claude"), required=True)
    prep.add_argument("--python", type=Path, default=readiness_case.DEFAULT_PYTHON)
    prep.add_argument("--package", type=Path)
    prep.add_argument("--consumer", type=Path)
    execute = sub.add_parser("run")
    execute.add_argument("destination", type=Path)
    execute.add_argument("--timeout", type=float, default=1200)
    args = parser.parse_args()
    if args.action == "prepare":
        consumer = prepare(args.destination, args.host, args.python, package=args.package, consumer=args.consumer)
        print(json.dumps({"consumer": str(consumer), "launched": False}))
    else:
        run(args.destination.resolve(), timeout=args.timeout)
        retain(args.destination.resolve())


if __name__ == "__main__":
    main()
