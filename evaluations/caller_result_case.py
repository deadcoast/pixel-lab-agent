"""Bounded cold caller continuation over retained art and an isolated unknown-job fixture."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from evaluations import readiness_case
from evaluations.host_trials import inventory, sha, write_json
from evaluations.native_trial_records import reference
from evaluations.request_review_trials import ROOT, run

WORK = "work/compact-caller"
INPUTS = "work/compact-caller-inputs"
UNKNOWN = "controlled-unknown"
SOURCE = ROOT / "build/artistic-revision-consumer-01"
UNKNOWN_SOURCE = ROOT / "evidence/family-delivery/adapter-scenario/unknown-member"
KIT = readiness_case.KIT
PROTECTED = {"AGENTS.md", "SESSION.md", ".codex/agents/pixl.toml",
             ".agents/skills/pixl/SKILL.md", ".agents/skills/plar/SKILL.md"}


def copy_preserved(source: Path, destination: Path) -> dict:
    original = inventory(source, ("__pycache__",))
    kept = {p: digest for p, digest in original.items() if p not in PROTECTED}
    for name in kept:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)
    if any(sha(destination / p) != digest for p, digest in kept.items()):
        raise ValueError("Retained consumer copy differs")
    return kept


def prepare(destination: Path, host: str, python: Path, *, package: Path | None = None,
            consumer: Path | None = None, source: Path = SOURCE,
            unknown_source: Path = UNKNOWN_SOURCE) -> Path:
    source, unknown_source = source.resolve(), unknown_source.resolve()
    if not (source / ".pixl/assets/queue.ready/state.px").is_file() or not (unknown_source / ".pixl/state.px").is_file():
        raise ValueError("Both retained real and controlled fixture stores are required")
    consumer = readiness_case.prepare(destination, host, "clean", python, package=package, consumer=consumer)
    destination = destination.resolve()
    original = copy_preserved(source, consumer)
    readiness_assignment = consumer / "READINESS-ASSIGNMENT.md"
    if readiness_assignment.is_file() and "READINESS-ASSIGNMENT.md" not in original:
        readiness_assignment.unlink()
    shutil.copytree(unknown_source, consumer / UNKNOWN)
    (consumer / WORK).mkdir(parents=True)
    (consumer / INPUTS).mkdir(parents=True)
    kit, python = consumer / KIT, python.resolve()
    initial = subprocess.check_output([str(python), "-B", str(kit / "scripts/pixl.py"), "plar", "read",
        "--path", "authoring-plar.txt", "--asset", "queue.working", "--root", str(consumer)], text=True, encoding="utf-8")
    selected = json.loads(initial)
    write_json(consumer / INPUTS / "initial-selection.json", selected)
    fixture = {"accepted": {"root": str(consumer), "path": "authoring-plar.txt", "asset_id": "queue.working",
        "state_path": ".pixl/assets/queue.ready/state.px", "state_hash": selected["production"]["continuation"]["state_hash"],
        "requirements_hash": selected["requirements_hash"], "prior_result": "work/artistic-revision/CALLER-RESULT.json",
        "stale_plan_diagnostic": "work/artistic-revision/request-review-02.json"},
        "unknown": {"root": str(consumer / UNKNOWN), "store": ".pixl", "job_id": "member.job",
                    "scope": "Existing controlled fictional-provider fixture; no real provider execution or fresh observation."}}
    write_json(consumer / INPUTS / "fixtures.json", fixture)
    # One undeclared-tool probe must reach the actual local MCP endpoint, since
    # hosts cannot invoke a nonexistent declared tool. Retain raw protocol bytes.
    probe = '''import json,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parents[2]
out=root/"work/compact-caller/missing-capability-protocol.jsonl"
if out.exists(): raise ValueError("Preserve prior protocol output; do not rerun this probe")
requests=[{"jsonrpc":"2.0","id":1,"method":"tools/list"},
          {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"pixl_missing_capability_probe","arguments":{}}}]
p=subprocess.run([sys.executable,"-B",str(root/"installed pixl/scripts/pixl.py"),"mcp","--root",str(root)],
    input="".join(json.dumps(r)+"\\n" for r in requests).encode("utf-8"),capture_output=True)
with out.open("xb") as stream: stream.write(p.stdout)
with out.with_suffix(".stderr.txt").open("xb") as stream: stream.write(p.stderr)
responses=[json.loads(s) for s in p.stdout.splitlines() if s.strip()]
print(json.dumps({"protocol_response":next(r for r in responses if r.get("id")==2),"process_returncode":p.returncode}))
raise SystemExit(p.returncode)
'''
    (consumer / INPUTS / "missing_capability_probe.py").write_text(probe, encoding="utf-8")
    guidance = f"""This is the explicit QOL-10/SC-08 compact-result evaluation, not new art production.
Consumer root: {consumer.as_posix()}. Kit: {kit.as_posix()}. Runtime: {python.as_posix()}.
Read COMPACT-CALLER.md. Preserve all original bytes, production states, jobs and reviews.
New files belong under {WORK}; public handoff may add immutable .pixl/handoffs files.
No provider calls, new dispatch claims, observations, acceptance, configuration changes or memory edits.
The separate {UNKNOWN} fixture is fictional and its unknown job must remain unknown.
"""
    assignment = f"""# Consume a compact result and continue safely

Use the actual named {'pixl' if host == 'codex' else 'pixl:pixl'} specialist. Codex uses agent_type=pixl,
fork_turns=none. Give it this root and assignment. No generic replacement.

SPECIALIST: read {INPUTS}/fixtures.json and the existing artistic caller result. Inspect the
actual accepted continuation and original observations through public local tools. Retain
a useful detailed report {WORK}/SPECIALIST-REPORT.json describing the accepted reused-art
scope, exact report/artifact references, the retained stale plan01, and the separate
controlled unknown job (obtain it from the pixl_unknown local MCP). Never attach that
fixture's job to artistic production facts. Save {WORK}/details.json with status=partial:
this combined reporting assignment leaves a separately controlled remote observation unresolved,
while the artistic production may remain delivered. Include optional details.caller using
the supplied spec's bounded summary/files/reports/issues/integration schema. Clearly label
integration as retained evidence, not a fresh renderer run. Keep full observations outside
the caller block and keep caller_actions/future_work separate from the runtime next action.
Under details.retained_specialist_observations include the unchanged complete value of
work/artistic-revision/SPECIALIST-RESULT.json. This is relevant existing evidence, not padding;
it makes the compact return measurable against its own full immutable snapshot.
Call public pixl_plar_handoff view=caller with the actual selected requirements and canonical
state identities. Save its full return at {WORK}/compact.json. Save receipt view with the
IDENTICAL details and identities at {WORK}/receipt.json; both must name identical snapshot
bytes. Write {WORK}/SPECIALIST-RESULT.json containing native_child, compact and receipt refs,
detailed_report ref, status and limits. References use path/sha256. Return the compact result
and its locator to the parent, not the full detailed report or handoff document.

CALLER: start from the returned compact result. Actually retrieve both details_ref and
resume_ref through pixl_source using exactly its file hash and physical lines (adequate budget);
save returns to {WORK}/details-read.json and resume-read.json. Preserve exact slice text,
including any trailing member comma. Execute the returned refresh.operation/arguments through
local MCP; save {WORK}/refresh.json. Compare those returned identities, not independently
recomputed state hashes. After the rejected probes and read-only recoveries below, use those
unchanged identities and same details for one guarded receipt
handoff, saved as {WORK}/parent-receipt.json, to establish exact safe continuation without
changing production. Do not confuse partial assignment, delivered artistic production,
historical creation acceptance, stale plan01, or the separate unknown job.

Exercise these rejected local calls yourself and retain original error responses in
{WORK}/errors/<name>.json. Derive category, affected identity and recovery from actual results:
- invalid-authoring: pixl_plar_handoff view=caller with valid current identities but
  details={{"status":"partial","caller":{{"unexpected":true}}}}.
- stale-state: same valid details, requirements and path, but expect="{'0' * 64}".
- unavailable-observation: pixl_source for {WORK}/intentionally-missing.txt, that same
  zero hash, lines1-1. Preserve unavailable status; do not create the file.
- uncertain-remote: read actual pixl_unknown pixl_jobs for .pixl/state.px, then call its
  pixl_job_dispatch for existing member.job with the returned canonical state hash. This
  explicit duplicate must be rejected; if the job is not unknown, stop this probe. Retain
  original error and follow its read-only recovery, saving {WORK}/unknown-recovery.json.
- missing-capability: run {python.as_posix()} -B {INPUTS}/missing_capability_probe.py.
  This invokes the actual local MCP tools/list and unsupported tools/call; retain its raw
  protocol file and result. Do not use a provider, invented host tool or replacement operation.

For stale-state follow the returned read-only recovery and save {WORK}/stale-recovery.json.
For invalid authoring, inspect the actual tool/caller schema, correct the rejected caller block
and reuse the already successful exact guarded receipt operation; no new semantic claim.
Do not automatically retry remote work, treat absence as an artistic failure/pass, or turn
an unknown job into prepared/failed/completed. No manual .px edits or hash substitutes.

Write {WORK}/CALLER-RESULT.json: native_child, compact, receipt, parent_receipt, details_read,
resume_read, refresh, specialist_result, errors (category -> path/sha256), unknown_recovery,
stale_recovery, same_snapshot, assignment_status, production_next, unknown_job_id/state,
scope, unresolved and next_action. Limit this ordinary caller report to 8192 UTF-8 bytes;
this is a scenario bound, not a universal pixel-art rule. Detailed evidence stays retrievable.
"""
    for name in ("AGENTS.md", "SESSION.md"):
        (consumer / name).write_text(guidance, encoding="utf-8")
    (consumer / "COMPACT-CALLER.md").write_text(assignment, encoding="utf-8")
    (destination / "prompt.txt").write_text(guidance + "\nComplete COMPACT-CALLER.md.\n", encoding="utf-8")
    launch = json.loads((destination / "launch.json").read_bytes())
    launch.update(case="compact-caller", artifact_roots=[WORK])
    server = {"command": str(python), "args": ["-B", str(kit / "scripts/pixl.py"), "mcp", "--root", str(consumer / UNKNOWN)]}
    if host == "codex":
        for key, value in server.items():
            launch["command"][-1:-1] = ["-c", "mcp_servers.pixl_unknown." + key + "=" + json.dumps(value)]
    else:
        mcp = json.loads((destination / "mcp.json").read_bytes())
        mcp["mcpServers"]["pixl-unknown"] = {"type": "stdio", **server}
        write_json(destination / "mcp.json", mcp)
        i = launch["command"].index("--allowedTools") + 1
        launch["command"][i] += ",mcp__pixl-unknown__*"
    write_json(destination / "launch.json", launch)
    identity = json.loads((destination / "identity.json").read_bytes())
    identity.update(case="compact-caller", inputs=inventory(consumer, ("__pycache__",)),
                    source_consumer=str(source), original_inputs=original, unknown_source=str(unknown_source),
                    unknown_files=inventory(consumer / UNKNOWN), fixtures=fixture,
                    runner=reference(Path(__file__)))
    identity["brief"] = reference(consumer / "BRIEF.md")
    write_json(destination / "identity.json", identity)
    shutil.copyfile(__file__, destination / "runner.py.txt")
    return consumer


def retain(destination: Path) -> None:
    if (destination / "preservation.json").exists():
        raise ValueError("Preserve the prior retention receipt")
    launch, identity = (json.loads((destination / name).read_bytes()) for name in ("launch.json", "identity.json"))
    root = Path(launch["cwd"])
    if (root / WORK).exists():
        shutil.copytree(root / WORK, destination / "outputs")
    current = inventory(root, ("__pycache__",))
    added = {p: digest for p, digest in current.items() if p not in identity["inputs"]}
    for name in added:
        if name.startswith(".pixl/handoffs/"):
            target = destination / "handoffs" / Path(name).name
            target.parent.mkdir(exist_ok=True)
            shutil.copyfile(root / name, target)
    write_json(destination / "preservation.json", {"changed": [p for p, digest in identity["inputs"].items()
        if current.get(p) != digest], "added": added})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("destination", type=Path)
    prep.add_argument("--host", choices=("codex", "claude"), default="codex")
    prep.add_argument("--python", type=Path, default=readiness_case.DEFAULT_PYTHON)
    prep.add_argument("--package", type=Path)
    prep.add_argument("--consumer", type=Path)
    execute = sub.add_parser("run")
    execute.add_argument("destination", type=Path)
    execute.add_argument("--timeout", type=float, default=900)
    args = parser.parse_args()
    if args.action == "prepare":
        root = prepare(args.destination, args.host, args.python, package=args.package, consumer=args.consumer)
        print(json.dumps({"consumer": str(root), "launched": False}))
    else:
        run(args.destination.resolve(), timeout=args.timeout)
        retain(args.destination.resolve())


if __name__ == "__main__":
    main()
