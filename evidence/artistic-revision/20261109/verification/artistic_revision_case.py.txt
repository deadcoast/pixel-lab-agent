"""Run the corrected Claude successor through a fresh named Codex specialist."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

from evaluations.host_trials import codex_command, inventory, sha, write_json
from evaluations.native_trial_records import reference
from evaluations.request_review_trials import ROOT, run

PREDECESSOR = ROOT / "evidence/focused-authoring/20261109/native/claude-01"
ARCHIVE_MANIFEST = ROOT / "evidence/focused-authoring/20261109/archives/claude-01-manifest.json"
CONTINUATION = ROOT / "evidence/native-continuation/20261109/outputs"
CONTRACTS = ROOT / "evidence/artistic-revision/20261109/contracts"
KIT = ".agents/skills/artistic-revision-kit"
WORK = "work/artistic-revision"
INPUTS = "work/artistic-revision-inputs"
ENTRYPOINTS = ("AGENTS.md", "SESSION.md", "ARTISTIC-REVISION.md", ".codex/agents/pixl.toml",
              ".agents/skills/pixl/SKILL.md", ".agents/skills/plar/SKILL.md")

ASSIGNMENT = """# Complete the corrected artistic successor

This is the explicit CF-03/TM-04 evaluation. You are a fresh calling agent; select
the native registered pixl role with agent_type="pixl", fork_turns="none". Delegate
the actual specialist work and paths, retain the returned identity, independently
review its work, and use the SAME child for concrete corrections as needed. If the
host cannot invoke that role, retain the exact failure; a generic child is not a
substitute. Do not edit the role, installed kit, host settings or persistent memory.

This consumer is the exact original Claude focused-authoring output, whose 20
original criteria and proposed 29-criterion successor were reconciled in
work/continuation/SPECIALIST-ROUND2.json and PHASE2-CALLER.json. The comparison is
complete; actual successor adoption, rendering and acceptance remain unfinished.
Do not substitute the later accepted Codex 23-criterion family, repeat comparison
alone, or treat the preserved unavailable evidence as a pass.

For this evaluation the caller explicitly chooses P1: hold frame zero of the
existing Working sheet under reduced motion, using the proposed `still` descriptor
extension. Record these as current SCOPED EVALUATION CALLER CHOICES, not historical
owner requirements. Review the held symbol alone and beside its label. Failure to
read as Working is a real failure to retain, not permission to assert acceptance.
Use the original broad adopted aesthetic in FAMILY-RESULT.json: perceptible
cool-blue accent, compact readable silhouettes, deliberate clusters and steps,
transparent exterior, distinct state meaning. Ready is the exact style baseline;
Start is the preserved vector control and color relationship reference. Do not
import a different historical Claude consumer's narrower aesthetic adoption.

1. Read the current installed shared skill/profile and focused public context for
   .pixl/assets/queue.ready/state.px, focus authoring-01.plan, view authoring,
   authoring-plar.txt / queue.working. Save exports under work/artistic-revision.
   Read large JSON programmatically. The original byte snapshots, inventory and
   contract inputs are under work/artistic-revision-inputs. Preserve every old
   assignment, report, proposal, asset, source and renderer. The only existing
   production files allowed to advance are state.px and authoring-plar.txt through
   public operations; old immutable store/history files and records must survive.
   Add new artifacts, reports, history and handoffs in the normal public locations.
2. Resolve obsolete prepared/undispatched authoring-01.working.join-01 through its
   supported failed-observation route with evidenced LOCAL ABANDONMENT. Preserve
   the exact old request and job lineage; do not invent a remote ID/provider
   failure or mutate immutable intent. Then author the connected successor through
   pixl_production_plan with exact current selection.replaces for linked Working,
   Retry and Paused assets. Use current expected hashes and public pixl_commit
   where required for source/contract/destination/candidate records. Do not delete
   production links, rename the asset, bypass pending protection or edit state
   bytes directly. Check actual allocations, not merely a saved plan graph.
3. Preserve all 20 original Q IDs/record hashes and all 29 corrected outcomes.
   Create work/artistic-revision/adopted-criteria.json with original_20 entries
   {id,record_sha256} and corrected_29 entries {source_id,record_id,check,
   authority_label_for_record,clauses,expert_clauses,carries,sources_added,
   evidence_route}. source_id is the round-two criterion ID; record_id is the
   actual new Q. Use corrected_check literally, or original_check when marked
   '(unchanged)'. Retain per-clause authority in this companion mapping. Explicitly
   record any path/fixture-description rederivation: the permitted destination
   changes are src/queue-view-successor.ts to src/queue-view-artistic.ts and
   renderer-successor/ to renderer-artistic/. New actual fixture behavior may
   change descriptive clauses only with exact source/evidence and caller review;
   do not silently weaken an outcome, invent an owner constraint or omit a row.
   Measurements remain observations; seed rotation and held-cell choice remain
   scoped proposals/choices. Alpha diagnostics do not decide visual matte review;
   partial alpha and in-cell margins remain allowed, 100ms owner timing stays
   distinct from expert pacing, and shared-consumer Start distinction is inference.
4. Implement the actual successor in NEW src/queue-view-artistic.ts and
   renderer-artistic/, adapting the retained proposed successor. Keep both older
   modules and renderer directories byte-identical. Re-derive source bindings and
   authoring PLAR destination honestly. Use the same backend state machine and
   both statusCell and compactStatus. Add actual LIVE 1x and 3x cells; the old
   fixture's 1x matrix is static and cannot prove 1x playback. Preserve selective
   AA/full alpha and pixel filtering. Reuse exact accepted art as new candidates
   with provenance; previous acceptance never transfers to the new criteria.
5. Review TM-04 inputs in work/artistic-revision-inputs/contracts, including current
   typed tool declarations and the actual workbench describe edits response.
   Compare affected prepared/proposed arguments and cached preparation schemas to
   current contracts; retain explicit supported/unsupported differences. These
   typed projections are not raw tools/list. No provider execution is assigned to
   this local reuse trial. If P1 requires new art, save the exact useful supported
   request for the connected outer host and retain the failed visual evidence.
   Do not invent REST endpoints, remote observations or paid generation success.
6. Actually run the new isolated browser capture and its checker using the existing
   supported headless route. Adapt and inspect the copied capture.mjs/check.py;
   discover local installed browser tooling without package installs. Capture both
   consumers and scales, all states, normal -> reduced -> normal in the same live
   session, and a separate initially-reduced run. Retain actual timestamps, sampled
   frame indices, observed changes/wraps and rendered pixels. A deterministic
   synthetic timeline is not observed playback; report wall-clock cadence only at
   its measured scope. Prefer report.playback rows {consumer,state:'running',scale,
   elapsed,frame,image:{path,sha256}}, sampled from actual live canvas exposures and
   measured clock values, with relative image paths. Keep synthetic timelines
   separate; a requested timeout duration is not a measured exposure timestamp.
   Verify non-Working states stay unchanged when preference changes. Criteria for
   Retry/Paused consumers require actual live state pixels under both preferences;
   inspect the fixture/checker's coverage and retain any missing evidence honestly.
   Inspect actual output images at native/enlarged scale with available
   image tools, plus live temporal evidence. Retain failed attempts unchanged.
7. Publish fresh candidate/inspection verdicts, completion, collective review and
   public PLAR handoff only where actual mechanical, visual and destination
   evidence supports every required criterion. The parent independently checks
   the specialist's actual files/images, the 20 -> corrected29 mapping, request
   and source authority, renderer results, and original record/byte preservation.
   Send concrete findings to the same child; preserve both initial and corrected
   reports. No self-reported pass substitutes for observed artifacts.

Write work/artistic-revision/SPECIALIST-RESULT.json and CALLER-REVIEW.json, then
CALLER-RESULT.json with native_child, plan_id, state_path, plar_path, candidate_ids,
review_ids, comparison_path, criteria_mapping, specialist_result, renderer_evidence
(list of {path,sha256} for actual render.json captures), handoff ({path,sha256}),
unresolved and next_action. Paths are relative to this consumer; reference exact
large exports rather than repeating them. Include source/requirement identities,
scoped caller choice, actual public operations, retained failures, fresh acceptance
limits and original-history preservation. A partial result must say what remains
and the concrete next operation. M1/M2, broader generated quality and general host
reliability remain open; this trial concerns the actual reused-art successor.
"""


def restore_consumer(consumer: Path, manifest_path: Path) -> dict:
    """Restore only verified original project entries; never overlay a consumer."""
    consumer = consumer.resolve()
    if consumer.exists():
        raise ValueError("Use a fresh consumer")
    manifest = json.loads(manifest_path.read_bytes())
    archive = manifest_path.parent / manifest["archive"]
    if sha(archive) != manifest["archive_sha256"]:
        raise ValueError("Original consumer archive changed")
    entries = {name: digest for name, digest in manifest["files"].items() if name.startswith("project/")}
    if not entries:
        raise ValueError("Archive has no original project entries")
    with zipfile.ZipFile(archive) as saved:
        for name, digest in entries.items():
            target = (consumer / name.removeprefix("project/")).resolve()
            if not target.is_relative_to(consumer) or target == consumer:
                raise ValueError("Archive entry escapes consumer")
            if hashlib.sha256(saved.read(name)).hexdigest() != digest:
                raise ValueError(f"Original consumer entry changed: {name}")
        consumer.mkdir(parents=True)
        for name in entries:
            target = consumer / name.removeprefix("project/")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(saved.read(name))
    return {"manifest": reference(manifest_path), "archive": reference(archive),
            "files": {name.removeprefix("project/"): digest for name, digest in entries.items()}}


def prepare(destination: Path, consumer: Path, *, contracts: Path = CONTRACTS) -> None:
    destination, consumer, contracts = destination.resolve(), consumer.resolve(), contracts.resolve()
    if destination.exists() or consumer.exists():
        raise ValueError("Use a fresh attempt and consumer")
    if consumer.is_relative_to(destination) or destination.is_relative_to(consumer):
        raise ValueError("Attempt and consumer must be separate directories")
    for name in ("current-tool-declarations.json", "workbench-describe-edits-response.json"):
        if not (contracts / name).is_file():
            raise ValueError(f"Missing current contract input: {name}")
    for name in ("SPECIALIST-ROUND2.json", "PHASE2-CALLER.json"):
        if not (CONTINUATION / name).is_file():
            raise ValueError(f"Missing retained reconciliation: {name}")
    original = restore_consumer(consumer, ARCHIVE_MANIFEST)
    destination.mkdir(parents=True)
    kit = consumer / KIT
    shutil.copytree(ROOT / "plugins/pixl", kit, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(CONTINUATION, consumer / "work/continuation")
    shutil.copytree(contracts, consumer / INPUTS / "contracts")
    baseline = consumer / INPUTS / "baseline"
    baseline.mkdir()
    for source, target in ((".pixl/assets/queue.ready/state.px", "state.px"),
                           ("authoring-plar.txt", "authoring-plar.txt"),
                           ("work/focused-successor/specialist-proposal.json", "specialist-proposal.json")):
        shutil.copyfile(consumer / source, baseline / target)
    write_json(baseline / "original-inputs.json", original["files"])
    (consumer / WORK).mkdir()
    python = ROOT / ".venv/Scripts/python.exe"
    guidance = f"""This is the explicit CF-03/TM-04 native artistic revision evaluation.
Follow ARTISTIC-REVISION.md; earlier assignments remain preserved history.
The current installed kit is {KIT}; start at {KIT}/skills/pixl/SKILL.md.
Consumer root: {consumer.as_posix()}. Selected Python: {python.as_posix()}.
New reports belong under {WORK}. Existing state and authoring-plar.txt may advance
through public operations; old immutable evidence and records must survive.
Only new src/queue-view-artistic.ts and renderer-artistic/ implement the successor.
Use the actual named PIXL child; caller owns independent verification.
No provider execution, package installs, global configuration or memory edits.
"""
    for name in ("AGENTS.md", "SESSION.md"):
        (consumer / name).write_text(guidance, encoding="utf-8")
    role = consumer / ".codex/agents/pixl.toml"
    role.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / ".codex/agents/pixl.toml", role)
    for name in ("pixl", "plar"):
        wrapper = consumer / f".agents/skills/{name}/SKILL.md"
        wrapper.parent.mkdir(parents=True, exist_ok=True)
        wrapper.write_text(f"---\nname: {name}\ndescription: Load the installed {name.upper()} production workflow.\n---\n\n"
                           f"Read [the shared skill](../artistic-revision-kit/skills/{name}/SKILL.md), resolving links from that file.\n",
                           encoding="utf-8")
    (consumer / "ARTISTIC-REVISION.md").write_text(ASSIGNMENT, encoding="utf-8")
    (destination / "prompt.txt").write_text(guidance + "\nComplete ARTISTIC-REVISION.md through actual successor acceptance.\n", encoding="utf-8")
    command = codex_command() + [
        "exec", "--ignore-user-config", "--ignore-rules", "--json", "--skip-git-repo-check",
        "--sandbox", "danger-full-access", "-C", str(consumer), "-c", 'approval_policy="never"',
        "-c", "agents.enabled=true", "-c", "agents.max_concurrent_threads_per_session=1",
        "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.memories=false",
        "-c", 'web_search="disabled"', "-c", "agents.pixl.config_file=" + json.dumps(role.as_posix()),
    ]
    server = {"command": str(python), "args": [str(kit / "scripts/pixl.py"), "mcp", "--root", str(consumer)]}
    for key, value in server.items():
        command += ["-c", f"mcp_servers.pixl_local.{key}=" + json.dumps(value)]
    command.append("-")
    write_json(destination / "launch.json", {
        "host": "codex", "case": "artistic-revision", "cwd": str(consumer), "command": command,
        "host_version": subprocess.check_output(codex_command() + ["--version"], text=True).strip(),
        "continuation_mode": "artifact_restart", "predecessor": reference(PREDECESSOR / "record.json"),
        "artifact_roots": [WORK], "role_registration": "explicit", "role_tool_setting": "legacy",
        "configuration_files": {"codex_role": str(role), "package": str(kit / "bundle-manifest.json"),
                                **{name + "_wrapper": str(consumer / f".agents/skills/{name}/SKILL.md") for name in ("pixl", "plar")}},
    })
    write_json(destination / "identity.json", {
        "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "predecessor": reference(PREDECESSOR / "record.json"), "original_consumer": original,
        "original_inputs": original["files"], "consumer": str(consumer),
        "baseline_state": reference(baseline / "state.px"), "baseline_plar": reference(baseline / "authoring-plar.txt"),
        "original_proposal": reference(baseline / "specialist-proposal.json"),
        "reconciliation": reference(consumer / "work/continuation/SPECIALIST-ROUND2.json"),
        "original_role": reference(ROOT / ".codex/agents/pixl.toml"),
        "contracts": inventory(consumer / INPUTS / "contracts"),
        "inputs": inventory(consumer, ("__pycache__",)), "package_files": inventory(kit),
        "current_package": reference(kit / "bundle-manifest.json"), "runner": reference(Path(__file__)),
        "prompt_sha256": sha(destination / "prompt.txt"),
        "scope": "Fresh named specialist adopting corrected29 with scoped P1/still caller choice, actual destination acceptance of reused art; no new generation claim.",
    })
    shutil.copyfile(__file__, destination / "runner.py.txt")


def retain_outputs(destination: Path) -> None:
    """Keep observed outputs and every delta even when a native run is partial."""
    consumer = Path(json.loads((destination / "launch.json").read_bytes())["cwd"])
    baseline = json.loads((destination / "identity.json").read_bytes())["inputs"]
    current = inventory(consumer, ("__pycache__",))
    changed = {name: digest for name, digest in current.items() if baseline.get(name) != digest}
    outputs = consumer / WORK
    if outputs.is_dir():
        shutil.copytree(outputs, destination / "outputs")
    archive = destination / "consumer-delta.zip"
    with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED) as saved:
        for name in changed:
            saved.write(consumer / name, name)
    with zipfile.ZipFile(destination / "consumer-entrypoints.zip", "x", zipfile.ZIP_DEFLATED) as saved:
        for name in ENTRYPOINTS:
            saved.write(consumer / name, name)
    write_json(destination / "consumer-delta.json", {
        "archive": reference(archive), "files": changed,
        "changed_existing": [name for name in changed if name in baseline],
        "removed": [name for name in baseline if name not in current],
        "scope": "Observed output retention, including failed/unexpected changes; not acceptance or a behavioral grade.",
    })


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--consumer", type=Path, default=ROOT / "build/artistic-revision-consumer-01")
    parser.add_argument("--contracts", type=Path, default=CONTRACTS)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--run-prepared", action="store_true")
    parser.add_argument("--timeout", type=float)
    args = parser.parse_args()
    if args.prepare_only and args.run_prepared:
        parser.error("--prepare-only and --run-prepared are mutually exclusive")
    destination = args.destination.resolve()
    if not args.run_prepared:
        prepare(destination, args.consumer, contracts=args.contracts)
    if not args.prepare_only:
        run(destination, timeout=args.timeout)
        retain_outputs(destination)


if __name__ == "__main__":
    main()
