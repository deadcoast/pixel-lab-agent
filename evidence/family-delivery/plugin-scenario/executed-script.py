"""Scripted copied-plugin walkthrough, run only after the final bundle is built.

Scenario data and prior sample/member verdicts are explicitly fictional. Runtime
operations use a relocated plugin with isolated Python and dependency paths only.
This is bounded operation evidence, not an independent profile-compliance trial.
"""

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY))

from tests.family_support import family


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    destination = Path(__file__).with_name("plugin-scenario")
    destination.mkdir()
    shutil.copyfile(__file__, destination / "executed-script.py")
    kit = destination / "copied-kit"
    shutil.copytree(REPOSITORY / "plugins" / "pixl", kit)
    project = destination / "project"
    project.mkdir()
    family(project)
    state = project / ".pixl" / "state.px"
    dependencies = [path for path in sys.path if path.endswith("site-packages")]
    bootstrap = destination / "isolated-runner.py"
    bootstrap.write_text(
        "import json,runpy,sys\n"
        f"sys.path[:0] = {dependencies!r}\n"
        f"runner = {str(kit / 'scripts' / 'pixl.py')!r}\n"
        "sys.argv[0] = runner\n"
        "runpy.run_path(runner, run_name='__main__')\n",
        encoding="utf-8",
    )
    report = {
        "purpose": "Scripted family workflow through final relocated plugin CLI and MCP",
        "script_sha256": digest(__file__),
        "fixture_builder_sha256": digest(REPOSITORY / "tests" / "family_support.py"),
        "limits": [
            "No independent profile-compliance evaluation or controlled before/after benchmark",
            "Fixture sample/member passing receipts and provider observations are explicitly synthetic",
            "Collective visual review remains unperformed; destination engine remains unavailable",
            "No real remote execution, production art or engine acceptance",
        ],
        "instructions": [],
        "runtime": [],
        "events": [],
        "passed": False,
    }
    for relative in (
        "resources/agent/PROFILE.md",
        "skills/pixl/SKILL.md",
        "skills/pixl/references/family-delivery.md",
        "skills/pixl/references/provider-recovery.md",
        "skills/pixl/references/runtime.md",
    ):
        report["instructions"].append(
            {"path": relative, "sha256": digest(kit / relative)}
        )
    for path in sorted((kit / "runtime" / "pixl").glob("*.py")):
        report["runtime"].append(
            {"path": path.relative_to(kit).as_posix(), "sha256": digest(path)}
        )
    manifest = kit / "bundle-manifest.json"
    if manifest.exists():
        report["bundle_manifest_sha256"] = digest(manifest)
        assert report["bundle_manifest_sha256"] == "2c21250554a42804453ed3ea58810b08fd19b6b1fa08b5f0f3b886e14c3837d1"
        entries = json.loads(manifest.read_bytes())["files"]
        assert len(entries) == 90
        for entry in entries:
            assert digest(kit / entry["path"]) == entry["sha256"], entry
            assert (kit / entry["path"]).stat().st_size == entry["bytes"], entry
            assert digest(REPOSITORY / entry["source"]) == entry["sha256"], entry
        report["verified_manifest_entries"] = len(entries)
    report["bootstrap_sha256"] = digest(bootstrap)

    def run(*arguments, expected=0, json_output=True, request=None):
        command = [sys.executable, "-I", "-S", str(bootstrap), *map(str, arguments)]
        completed = subprocess.run(
            command,
            cwd=project,
            input=request,
            capture_output=True,
            text=True,
            check=False,
            timeout=25,
        )
        entry = {
            "command": command,
            "cwd": str(project),
            "stdin": request,
            "exit": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        report["events"].append(entry)
        assert completed.returncode == expected, entry
        output = completed.stdout if expected == 0 else completed.stderr
        return json.loads(output) if json_output else output

    def cli(*arguments, **options):
        return run(*arguments, **options)

    def mcp(name, arguments, error=False):
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        }
        result = run("mcp", "--root", project, request=json.dumps(request) + "\n")[
            "result"
        ]
        assert result["isError"] == error, result
        return result if error else result["structuredContent"]

    def current():
        return cli("family", state, "delivery.output", "--root", project)

    def amend(name, change):
        previous = current()
        adapter = cli("decode", state)
        adapter["revision"] += 1
        change(adapter, {record["id"]: record for record in adapter["records"]})
        source = project / f"{name}.json"
        candidate = project / f"{name}.px"
        source.write_text(
            json.dumps(adapter, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        cli("encode", source, "--out", candidate, json_output=False)
        cli("validate", candidate, "--root", project)
        return cli(
            "commit",
            project / ".pixl",
            candidate,
            "--expect",
            previous["hash"],
            "--root",
            project,
        )

    def mutation(**extra):
        return {"store": ".pixl", "expect": current()["hash"], **extra}

    def nominate_unavailable(candidate_id, verdict_id, adapter, records):
        records["delivery.task"]["fields"]["ca"] = [{"$ref": candidate_id}]
        records["delivery.task"]["fields"]["vr"].append({"$ref": verdict_id})
        adapter["records"].append(
            {
                "id": verdict_id,
                "kind": "V",
                "fields": {
                    "tk": {"$ref": "delivery.task"},
                    "rq": {"$ref": "q.delivery.engine"},
                    "xr": {"$ref": candidate_id},
                    "st": {"$symbol": "unavailable"},
                    "wh": {"$ref": "actor"},
                    "at": "2026-09-11T12:00:00+00:00",
                    "ev": [],
                    "wy": "Fictional target project is absent. Import the copied PNGs into the named target and execute saved import checks before destination acceptance.",
                },
            }
        )
        handoff = {
            "id": "family.handoff",
            "kind": "N",
            "fields": {
                "wh": {"$ref": "actor"},
                "fo": [
                    {"$ref": "delivery.output"},
                    {"$ref": candidate_id},
                    {"$ref": verdict_id},
                    {"$ref": "member.job"},
                ],
                "nx": [{"$ref": "delivery.task"}],
                "bl": [{"$ref": "delivery.task"}],
                "rv": adapter["revision"],
            },
        }
        if "family.handoff" in records:
            records["family.handoff"].update(handoff)
        else:
            adapter["records"].append(handoff)

    try:
        origin = subprocess.run(
            [
                sys.executable,
                "-I",
                "-S",
                "-c",
                f"import json,sys; sys.path[:0]={([str(kit / 'runtime'), *dependencies])!r}; import pixl.delivery; print(json.dumps({{'delivery':pixl.delivery.__file__,'path':sys.path}}))",
            ],
            cwd=project,
            capture_output=True,
            text=True,
            check=True,
            timeout=25,
        )
        report["isolation"] = json.loads(origin.stdout)
        assert Path(report["isolation"]["delivery"]).is_relative_to(kit)
        assert str(REPOSITORY) not in report["isolation"]["path"]
        first = current()
        assert first["families"][0]["snapshots"] == []
        amend(
            "reopen-member",
            lambda adapter, records: records["member.task"]["fields"].update(
                st={"$symbol": "open"}
            ),
        )
        request = {
            "provider": "fictional-fixture",
            "tool": "fixture_generate",
            "arguments": {},
            "schema": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
            "discovery": {
                "source": "Fictional local fixture",
                "observed_at": "2026-09-11T12:00:00+00:00",
                "evidence": {"fixture": True},
            },
            "authorization": {
                "scope": "Local scripted walkthrough only; no remote execution",
                "evidence": {"fixture": True},
            },
        }
        mcp(
            "pixl_job_prepare",
            mutation(
                job_id="member.job",
                task_id="member.task",
                outputs=["member.output"],
                **request,
            ),
        )
        claim = mcp("pixl_job_dispatch", mutation(job_id="member.job"))
        assert claim["job"]["state"] == "unknown" and not claim["remote_executed"]
        cold = current()
        assert cold["families"][0]["pending_jobs"] == [
            {"id": "member.job", "task": "member.task", "state": "unknown"}
        ]
        jobs = mcp("pixl_jobs", {"path": ".pixl/state.px"})
        assert jobs["jobs"][0]["next_action"] == "reconcile"
        blocked = cli(
            "family-snapshot",
            project / ".pixl",
            "delivery.output",
            "blocked.package",
            "--expect",
            cold["hash"],
            "--root",
            project,
            expected=2,
        )
        assert blocked["error"] == "delivery_blocked"
        mcp(
            "pixl_job_observe",
            mutation(
                job_id="member.job",
                event="failed",
                evidence={
                    "fixture": True,
                    "observation": "Caller-supplied fictional failure settles this simulated request; no provider was called",
                },
            ),
        )
        amend(
            "resume-member",
            lambda adapter, records: records["member.task"]["fields"].update(
                st={"$symbol": "active"}
            ),
        )
        amend(
            "retain-accepted-member",
            lambda adapter, records: records["member.task"]["fields"].update(
                st={"$symbol": "done"}
            ),
        )
        retained = mcp(
            "pixl_family_snapshot",
            mutation(output_id="delivery.output", candidate_id="delivery.first"),
        )
        assert not retained["accepted"] and not retained["remote_executed"]
        first_snapshot = current()["families"][0]["snapshots"][0]
        old_manifest = project / first_snapshot["manifest"]
        old_identities = {str(old_manifest): digest(old_manifest)}
        for item in first_snapshot["files"]:
            copied = old_manifest.parent / item["path"]
            assert copied.read_bytes() == (project / item["source_path"]).read_bytes()
            old_identities[str(copied)] = digest(copied)
        amend(
            "first-destination-boundary",
            lambda adapter, records: nominate_unavailable(
                "delivery.first", "first.engine.unavailable", adapter, records
            ),
        )
        amend(
            "amended-membership",
            lambda adapter, records: records["delivery.output"]["fields"].update(
                mb=[{"$ref": "member.output"}]
            ),
        )
        changed = current()["families"][0]
        assert changed["snapshots"][0]["stale"]
        assert all(
            digest(path) == identity for path, identity in old_identities.items()
        )
        second = cli(
            "family-snapshot",
            project / ".pixl",
            "delivery.output",
            "delivery.second",
            "--expect",
            current()["hash"],
            "--root",
            project,
        )
        assert not second["accepted"]
        amend(
            "second-destination-boundary",
            lambda adapter, records: nominate_unavailable(
                "delivery.second", "second.engine.unavailable", adapter, records
            ),
        )
        final = mcp(
            "pixl_family", {"path": ".pixl/state.px", "output": "delivery.output"}
        )
        row = final["families"][0]
        assert {q["id"]: q["status"] for q in row["requirements"]} == {
            "q.continuity": "unperformed",
            "q.delivery.engine": "unavailable",
        }
        assert row["state"] == "open" and row["pending_jobs"] == []
        snapshots = {snapshot["candidate"]: snapshot for snapshot in row["snapshots"]}
        assert (
            snapshots["delivery.first"]["stale"]
            and snapshots["delivery.second"]["stale"] == []
        )
        assert (
            len(snapshots["delivery.first"]["files"]) == 2
            and len(snapshots["delivery.second"]["files"]) == 1
        )
        assert all(
            digest(path) == identity for path, identity in old_identities.items()
        )
        cli("workflow", state, "--root", project)
        cli("jobs", state, "--root", project)
        report["final_state"] = {
            "path": str(state),
            "revision": final["revision"],
            "hash": final["hash"],
            "family": row,
        }
        report["old_snapshot_identities"] = old_identities
        report["passed"] = True
        (destination / "handoff.md").write_text(
            "# Fictional copied-plugin family handoff\n\n"
            f"State: `{state}`; revision {final['revision']}; hash `{final['hash']}`.\n\n"
            f"Current family `delivery.output`, nominee `delivery.second`; manifest `{snapshots['delivery.second']['manifest']}`. "
            "The manifest contains the exact copied member PNG; the baseline is `sample`. "
            "The previous two-member package `delivery.first` remains byte-identical and is reported stale after saved membership amendment.\n\n"
            "Start the copied runner with family, workflow and jobs using the project directory as root, then inspect family.handoff "
            "and the manifest/copied PNG. member.job was reconciled by an explicitly synthetic failed observation; no provider call occurred. "
            "Collective continuity remains unperformed. Open the baseline and selected member together at native and enlarged scales and "
            "record actual observations before any visual verdict. This static fixture has no animation or tile requirement; other tasks "
            "must perform the playback or neighborhood checks in their own saved criteria.\n\n"
            "Destination verification is unavailable because the fictional target project is absent. The retained requirement asks for "
            "importing these copied PNGs into the named project and executing its saved import checks. There is no real target engine "
            "to accept here. Keep delivery open; useful copied files and local recording checks do not establish artistic or engine acceptance.\n",
            encoding="utf-8",
        )
    finally:
        (destination / "record.json").write_text(
            json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(
        json.dumps(
            {"passed": report["passed"], "record": str(destination / "record.json")}
        )
    )


if __name__ == "__main__":
    main()
