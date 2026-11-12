"""NF-08: read retained generated, constructed and reused family lineage natively."""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path

from evaluations import consumer_execution_case, readiness_case
from evaluations.host_trials import inventory, sha, write_json
from evaluations.native_trial_records import reference
from evaluations.request_review_trials import run
from pixl import store

WORK = "work/asset-lineage"
INPUTS = "work/asset-lineage-inputs"
KIT = readiness_case.KIT
STATE = consumer_execution_case.STATE
PLAR = "authoring-plar.txt"
FAMILIES = {"original": "live.family.candidate", "reused": "artistic2.delivery.candidate"}
MEMBERS = {
    "ready": ("ready.retained", "ready.retained"),
    "working": ("live.working-animation-motion-01.candidate", "artistic2.working.candidate"),
    "retry": ("live.retry.candidate", "artistic2.retry.candidate"),
    "paused": ("live.paused-cutout-01.candidate", "artistic2.paused.candidate"),
}
SOURCES = {
    "working_construction": "work/live-family/working-animation-motion-01-construction.json",
    "ready_fixture": ".pixl/assets/queue.ready/jobs/e7cc448003dc41409ef16591c3793a118859d4e9b4e5f44ff18be8ad07783922.json",
}
KEY_CLAIMS = {
    "ready_is_controlled_fixture": True,
    "ready_is_authenticated_provider_generation": False,
    "working_has_retained_deterministic_construction_record": True,
    "working_final_is_provider_generated_animation": False,
    "paused_has_recorded_generation_and_deterministic_cutout": True,
    "retry_has_recorded_generation_request": True,
    "same_bytes_proves_reuse_direction": False,
    "remote_execution_authenticated": False,
}
READS = {
    "original_context": ("pixl_review_context", {"path": STATE, "candidate_id": FAMILIES["original"]}),
    "reused_context": ("pixl_review_context", {"path": STATE, "candidate_id": FAMILIES["reused"]}),
    "original_family": ("pixl_family", {"path": STATE, "output": "family.delivery.output"}),
    "reused_family": ("pixl_family", {"path": STATE, "output": "artistic-02.delivery.output"}),
    **{f"plar_{role}": ("pixl_plar_read", {"path": PLAR, "asset_id": "queue." + role}) for role in MEMBERS},
}


def prepare(destination: Path, host: str, python: Path, *, package: Path | None = None,
            consumer: Path | None = None) -> Path:
    """Reuse the verified closure and current isolated host setup; never run a host."""
    consumer = consumer_execution_case.prepare(destination, host, python, package=package, consumer=consumer)
    destination, python = destination.resolve(), python.resolve()
    doc = store.load(consumer / Path(STATE).parent)
    identities = {}
    for role, candidates in MEMBERS.items():
        identities[role] = [{"candidate": candidate, "path": doc.records[candidate].fields["ur"],
                             "sha256": doc.records[candidate].fields["dg"]} for candidate in candidates]
        if identities[role][0]["sha256"] != identities[role][1]["sha256"]:
            raise ValueError("Retained original and revised member bytes differ: " + role)
        for item in identities[role]:
            if sha(consumer / item["path"]) != item["sha256"]:
                raise ValueError("Retained member bytes changed: " + item["candidate"])
    (consumer / WORK).mkdir(parents=True)
    reads = dict(READS)
    for name, path in SOURCES.items():
        lines = (consumer / path).read_bytes().decode("utf-8-sig").splitlines(keepends=True)
        end = (next(i for i, line in enumerate(lines, 1) if '"required_review"' in line)
               if name == "working_construction" else len(lines))
        reads[name] = ("pixl_source", {"path": path, "expect": sha(consumer / path),
                                      "start": 1, "end": end, "budget": 16384})
    fixture = {"state": STATE, "plar": PLAR, "families": FAMILIES, "members": identities,
               "reads": {key: {"tool": tool, "arguments": arguments,
                                "result_path": f"{WORK}/{key.replace('_', '-')}.json"}
                         for key, (tool, arguments) in reads.items()},
               "caller_reads": {key: {"tool": READS[key][0], "arguments": READS[key][1],
                                      "result_path": f"{WORK}/caller-{key.replace('_', '-')}.json"}
                                for key in ("original_context", "reused_context")},
               "source_evidence": {key: {"path": path, "sha256": sha(consumer / path)}
                                   for key, path in SOURCES.items()},
               "restoration": reference(consumer / consumer_execution_case.INPUTS / "restoration.json"),
               "scope": "Existing byte identities only. The specialist must resolve retained lineage evidence and its limits through public reads; no new provenance or acceptance is authored."}
    write_json(consumer / INPUTS / "fixture.json", fixture)
    guidance, assignment = instructions(consumer, host, python)
    for name in ("AGENTS.md", "SESSION.md"):
        (consumer / name).write_text(guidance, encoding="utf-8")
    (consumer / "ASSET-LINEAGE.md").write_text(assignment, encoding="utf-8")
    (destination / "prompt.txt").write_text(guidance + "\nComplete ASSET-LINEAGE.md.\n", encoding="utf-8")
    launch = json.loads((destination / "launch.json").read_bytes())
    launch.update(case="asset-lineage", artifact_roots=[WORK])
    write_json(destination / "launch.json", launch)
    identity = json.loads((destination / "identity.json").read_bytes())
    identity.update(case="asset-lineage", inputs=inventory(consumer, ("__pycache__",)), fixture=fixture,
                    baseline_state=reference(consumer / STATE), baseline_production=inventory(consumer / ".pixl"),
                    runner=reference(Path(__file__)))
    write_json(destination / "identity.json", identity)
    (destination / "runner.py.txt").rename(destination / "consumer-setup-runner.py.txt")
    shutil.copyfile(__file__, destination / "runner.py.txt")
    return consumer


def instructions(root: Path, host: str, python: Path) -> tuple[str, str]:
    role = "pixl" if host == "codex" else "pixl:pixl"
    kit = root / KIT
    guidance = f'''Explicit NF-08 retained asset-lineage evaluation.
Root: {root.as_posix()}; current kit: {kit.as_posix()}; Python: {python.as_posix()}.
Follow ASSET-LINEAGE.md using the actual named {role} specialist. Older assignments
and host configuration are preserved history. Add reports only under {WORK}.
Keep original art, source, state, PLAR, installed kit and all history unchanged.
No provider calls, new generation, rendering, reviews, verdicts, nomination,
completion, handoff, acceptance, package installation, settings or memory edits.
This is read-only lineage qualification. M1/M2 and broader M3 remain open.
'''
    assignment = f'''# Explain the retained family lineage through public reads

The original live.family.candidate and later artistic2.delivery.candidate are
restored exactly from retained archives. Fixture {INPUTS}/fixture.json provides
their IDs and existing member hashes, public read arguments and fresh result paths.
No current provider, generation, renderer, review or acceptance work is assigned.

Invoke one actual named `{role}` specialist (Codex agent_type="pixl", fork_turns="none")
with the consumer root and this whole assignment; retain the actual child identity.
Do not replace a missing named specialist with a generic child. The specialist must
read the installed common skill {(kit / 'skills/pixl/SKILL.md').as_posix()}, shared
production profile {(kit / 'resources/agent/PROFILE.md').as_posix()}, workflow
reference {(kit / 'skills/pixl/references/family-delivery.md').as_posix()} and the fixture.

Specialist:
1. Perform the ten public read operations named in fixture.reads through the
   current installed local MCP or CLI. Preserve their complete actual returns at
   the named fresh paths. Use result_path only if advertised. For other reads,
   capture complete CLI stdout or save the actual returned object programmatically;
   do not invent or manually transcribe its content. Read large JSON programmatically.
   After saving them, read both complete source excerpt JSON returns
   (working_construction and ready_fixture) so their exact content is visible in
   the native transcript, including when CLI stdout was redirected.
2. Inspect the returned lineage beside the original/reused family members,
   review contexts and selected PLAR delivery. Compare exact candidate identities,
   artifact hashes and retained source/job/event/transform/reuse relationships.
   Inspect actual cited source evidence needed to distinguish Working's generated
   seed from its delivered deterministic construction, generated Retry, generated
   Paused plus deterministic cutout, Ready's earlier controlled fixture provenance, and
   the later exact-byte reused revisions. Do not infer a provider-generated final
   animation from a provider job merely being present; keep unsuccessful or unused
   alternatives distinct. Verify cited evidence hashes. Unknown or unsupported
   links must remain unknown, with the report's evidence limits intact.
3. Write {WORK}/COMPARISON.json with families={{"original":original family ID, "reused":reused family ID}}, a members object
   keyed ready/working/retry/paused (original_candidate, reused_candidate,
   original_sha256, reused_sha256, same_bytes, findings, evidence refs and limits),
   plus overall limitations and key_claims: an object of explicit boolean answers to
   {', '.join(KEY_CLAIMS)}. Answer from evidence, not from the wording of these keys.
   Findings must distinguish retained facts from declared
   or unknown relationships. This is source interpretation, not new provenance.
4. Write {WORK}/SPECIALIST-RESULT.json with operations (fixture.reads keys mapped
   to exact saved result refs), comparison (exact ref), inspected_sources (exact
   refs to evidence actually read), production_unchanged, new_provider_execution=false,
   acceptance_created=false, limitations and next_action. References use
   {{"path":"consumer-relative/path","sha256":"actual hash"}}; annotations are allowed.
   Do not publish any mutation or new acceptance to fix an unknown lineage.

Caller: wait for the same child. Independently perform fixture.caller_reads via
public operations, retaining exact returns. Read the complete compact comparison
and both saved source excerpt returns (working_construction and ready_fixture);
inspect the larger saved results programmatically, compare identities/hashes across
all public surfaces, and inspect the cited evidence supporting key distinctions. Verify
unchanged initial files and production history. Write {WORK}/CALLER-RESULT.json
with native_child, specialist_result, operations, caller_operations, comparison, inspected_sources,
independent_checks, production_unchanged, new_provider_execution=false,
acceptance_created=false, scope, limitations and next_action. Use exact file refs.
No new provider execution or artistic/target-engine acceptance is established.
Keep M1/M2 and broader M3 open; CF-10 follows this bounded lineage increment.
'''
    return guidance, assignment


def retain(destination: Path, *, baseline: Path | None = None) -> None:
    """Keep only new reports and unexpected deltas; original archives are referenced."""
    if any((destination / name).exists() for name in ("outputs", "preservation.json", "unexpected-delta.zip")):
        raise ValueError("Preserve prior retention; use a separate continuation record")
    launch = json.loads((destination / "launch.json").read_bytes())
    baseline = baseline.resolve() if baseline is not None else destination.resolve()
    identity = json.loads((baseline / "identity.json").read_bytes())
    root = Path(launch["cwd"])
    original = json.loads((baseline / "launch.json").read_bytes())
    if (Path(original["cwd"]).resolve() != root.resolve() or baseline != destination.resolve()
            and launch.get("predecessor") != reference(baseline / "continuation.json")):
        raise ValueError("Continuation retention must name the exact original consumer and predecessor")
    if (root / WORK).is_dir():
        shutil.copytree(root / WORK, destination / "outputs")
    current = inventory(root, ("__pycache__",))
    changed = [name for name, digest in identity["inputs"].items() if current.get(name) != digest]
    unexpected = [name for name in current if name in changed or
                  name not in identity["inputs"] and not name.startswith(WORK + "/")]
    if unexpected:
        with zipfile.ZipFile(destination / "unexpected-delta.zip", "x", zipfile.ZIP_DEFLATED) as archive:
            for name in unexpected:
                archive.write(root / name, name)
    write_json(destination / "preservation.json", {
        "changed": changed, "removed": [name for name in identity["inputs"] if name not in current],
        "new": {name: digest for name, digest in current.items() if name not in identity["inputs"]},
        "production_unchanged": inventory(root / ".pixl") == identity["baseline_production"],
        "baseline_identity": reference(baseline / "identity.json"),
        "scope": "Only new lineage reports are copied. Original image/state history remains identified by verified restoration archives, not duplicated or accepted again.",
    })


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
    execute.add_argument("--timeout", type=float, default=900)
    args = parser.parse_args()
    if args.action == "prepare":
        consumer = prepare(args.destination, args.host, args.python, package=args.package, consumer=args.consumer)
        print(json.dumps({"consumer": str(consumer), "launched": False}))
    else:
        run(args.destination.resolve(), timeout=args.timeout)
        retain(args.destination.resolve())


if __name__ == "__main__":
    main()
