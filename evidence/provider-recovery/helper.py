"""One developer-agent scripted/inspected exercise, not a provider simulator or benchmark.

Only setup files are authored directly. PIXL operations use the copied public CLI
or actual stdio MCP process. Runs retain every subprocess result before checking it.
Stages deliberately stop for the evaluating agent to inspect current observations.
"""

import base64
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import traceback
from datetime import datetime, timezone


REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("behavior-evaluation.json")
PYTHON = REPO / ".venv/Scripts/python.exe"
DEPENDENCIES = [str(REPO / ".venv/Lib/site-packages")]
EVIDENCE = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else None


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save():
    EVIDENCE["helper_sha256"] = sha(Path(__file__).read_bytes())
    OUT.write_text(json.dumps(EVIDENCE, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def record(kind, purpose, **fields):
    entry = {"sequence": len(EVIDENCE["transcript"]) + 1, "at": now(),
             "kind": kind, "purpose": purpose, **fields}
    EVIDENCE["transcript"].append(entry)
    save()
    return entry


def root():
    return Path(EVIDENCE["project"])


def kit():
    return Path(EVIDENCE["copied_plugin"])


def command(args):
    launch = (
        "import sys,runpy;from pathlib import Path;"
        f"sys.path.extend({DEPENDENCIES!r});"
        f"assert str(Path({str(REPO)!r}).resolve()) not in sys.path;"
        "p=sys.argv[1];sys.argv=sys.argv[1:];runpy.run_path(p,run_name='__main__')"
    )
    return [str(PYTHON), "-I", "-c", launch, str(kit() / "scripts/pixl.py"), *map(str, args)]


def run(purpose, args, *, project=None, stdin=None, expected=0, raw=False):
    project = Path(project or root())
    argv = command(args)
    process = subprocess.run(argv, cwd=project, input=stdin, capture_output=True,
                             text=True, encoding="utf-8", timeout=60)
    result = record("public_cli" if args[0] != "mcp" else "stdio_mcp",
                    purpose, command=argv, cwd=str(project), stdin=stdin,
                    exit_code=process.returncode, stdout=process.stdout,
                    stderr=process.stderr, expected_exit_code=expected)
    assert process.returncode == expected, result
    if raw or expected:
        return result
    return json.loads(process.stdout)


def cli(purpose, *args, project=None, expected=0, raw=False):
    return run(purpose, args, project=project, expected=expected, raw=raw)


def mcp(purpose, tool, arguments, *, project=None, expected_error=False):
    project = Path(project or root())
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-11-25", "capabilities": {},
            "clientInfo": {"name": "PIXL bounded developer evaluation", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
            "name": tool, "arguments": arguments}},
    ]
    wire = "".join(json.dumps(request, separators=(",", ":")) + "\n" for request in requests)
    result = run(purpose, ["mcp", "--root", project], project=project, stdin=wire, raw=True)
    responses = [json.loads(line) for line in result["stdout"].splitlines()]
    listing = next(response["result"]["tools"] for response in responses if response["id"] == 2)
    assert tool in {entry["name"] for entry in listing}
    response = next(response["result"] for response in responses if response["id"] == 3)
    assert response["isError"] == expected_error, response
    return response if expected_error else response["structuredContent"]


def write(path, value, purpose):
    path = Path(path)
    data = (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode() if not isinstance(value, (str, bytes)) else (value.encode() if isinstance(value, str) else value)
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"Never overwrite a fixture/evidence file: {path}"
    path.write_bytes(data)
    record("host_fixture_write", purpose, path=str(path), bytes=len(data), sha256=sha(data),
           content_base64=base64.b64encode(data).decode())
    return path


def store(project=None):
    return Path(project or root()) / ".pixl"


def state(project=None):
    return store(project) / "state.px"


def current_hash(project=None):
    return sha(state(project).read_bytes())


def snapshot(label, project=None):
    project = Path(project or root())
    files = []
    for path in sorted(project.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            files.append({"path": path.relative_to(project).as_posix(), "bytes": len(data),
                          "sha256": sha(data), "content_base64": base64.b64encode(data).decode()})
    entry = {"label": label, "project": str(project), "at": now(),
             "state_sha256": current_hash(project), "files": files}
    EVIDENCE["project_snapshots"].append(entry)
    save()
    return entry


def decode(project=None):
    return cli("Read current tagged adapter before authoring the next saved revision", "decode", state(project), project=project)


def publish(adapter, slug, project=None):
    project = Path(project or root())
    adapter["revision"] += 1
    adapter_path = write(project / f"{slug}.json", adapter, "Retain authored tagged adapter")
    candidate_path = project / f"{slug}.px"
    cli("Encode through copied public runtime", "encode", adapter_path, "--out", candidate_path,
        project=project, raw=True)
    cli("Validate candidate against actual project bytes", "validate", candidate_path, "--root", project, project=project)
    return cli("Publish with previously observed current canonical state hash", "commit", store(project), candidate_path,
               "--expect", current_hash(project), "--root", project, project=project)


def fields(adapter, id_):
    return next(item["fields"] for item in adapter["records"] if item["id"] == id_)


def ref(id_):
    return {"$ref": id_}


def sym(value):
    return {"$symbol": value}


def rec(id_, kind, **fields_):
    return {"id": id_, "kind": kind, "fields": fields_}


def audit_stage():
    assert EVIDENCE["stage"] == "final_outcome_ready_for_agent_review"
    bundle_checks = []
    for item in EVIDENCE["bundle_identity"]["files"]:
        current = {
            "source": sha((REPO / item["source"]).read_bytes()),
            "plugin": sha((REPO / "plugins/pixl" / item["path"]).read_bytes()),
            "copy": sha((kit() / item["path"]).read_bytes()),
        }
        assert set(current.values()) == {item["sha256"]}, (item["path"], current)
        bundle_checks.append({"path": item["path"], "expected_sha256": item["sha256"], **current})
    retained_bytes = 0
    retained_files = 0
    for snapshot_ in EVIDENCE["project_snapshots"]:
        for item in snapshot_["files"]:
            data = base64.b64decode(item["content_base64"], validate=True)
            assert sha(data) == item["sha256"] and len(data) == item["bytes"]
            if item["path"].startswith(".pixl/history/"):
                assert Path(item["path"]).stem == item["sha256"]
                assert (Path(snapshot_["project"]) / item["path"]).read_bytes() == data
            retained_bytes += len(data)
            retained_files += 1
    final_snapshot_checks = []
    for label in ["changed-contract-rejection-final-preserved", "original-project-final-candidate-and-open-acceptance"]:
        selected = next(s for s in EVIDENCE["project_snapshots"] if s["label"] == label)
        for item in selected["files"]:
            path = Path(selected["project"]) / item["path"]
            assert path.read_bytes() == base64.b64decode(item["content_base64"])
        assert current_hash(selected["project"]) == selected["state_sha256"]
        final_snapshot_checks.append({"label": label, "files_checked_against_actual_disk": len(selected["files"]),
                                      "state_sha256": selected["state_sha256"]})
    jobs_report = EVIDENCE["final_runtime_reports"]["jobs"]
    events = jobs_report["jobs"][0]["events"]
    assert [event["event"] for event in events] == ["dispatch", "unknown", "submitted", "running", "succeeded", "imported"]
    dispatch_calls = [entry for entry in EVIDENCE["transcript"] if entry["kind"] == "public_cli" and "job-dispatch" in entry.get("command", [])]
    assert len(dispatch_calls) == 1
    assert EVIDENCE["dispatch_request"] == jobs_report["jobs"][0]["request"]
    process_runs = [entry for entry in EVIDENCE["transcript"] if entry["kind"] in ("public_cli", "stdio_mcp", "isolation_witness")]
    assert all(entry["exit_code"] == entry.get("expected_exit_code", 0) for entry in process_runs)
    assert EVIDENCE["errors"] == []
    EVIDENCE["verification_levels"] = {
        "discovery_and_format": "Exercised copied CLI help, actual isolated launcher/import identity, repeated MCP initialize/tools/list/tools/call, tagged PX2 encode/validate/commit and 84 source/plugin/copy manifest identities.",
        "behavior_in_recorded_scenario": "One explicit fictional exercise was scripted and inspected by the developer agent. Prompts and interpretations precede operation stages. Under retry pressure the saved unknown attempt was reconciled without another dispatch. This is bounded behavior evidence, not a controlled benchmark or general instruction-following result.",
        "actual_task_outcome": "Actual local PNG bytes were imported and measured, with a passing mechanical verdict; changed-contract association was rejected without changing saved state/history/file. Actual provider execution, art quality/visual inspection and target-engine acceptance were not exercised.",
    }
    EVIDENCE["rubric"] = [
        {"criterion": "Saved plan and exact request before one claim", "result": "observed", "evidence": "Prepared snapshot precedes dispatch; exact dispatch request equals final retained request."},
        {"criterion": "Unknown response resists retry pressure", "result": "observed in this scripted exercise", "evidence": "CLI and MCP cold reports match unknown/null identity/reconcile; transcript and final events contain one dispatch."},
        {"criterion": "Recover the original resource across actual process restarts", "result": "observed with synthetic caller observations", "evidence": "Same job/request recovers one identity through submitted/running/succeeded using restarted CLI and MCP."},
        {"criterion": "Reject changed output context while retaining useful evidence", "result": "observed", "evidence": "job_stale; state hash, entire store inventory and source PNG unchanged; amended plan and handoff retained in separate branch."},
        {"criterion": "Import retains exact local bytes without automatic acceptance", "result": "observed", "evidence": "Original and copied PNG hashes match; immediate workflow has no nominee/verdict and unperformed criteria."},
        {"criterion": "Keep measurement, visual review and engine outcome distinct", "result": "observed for local boundary", "evidence": "Later explicit nomination and actual local mechanical pass leave visual/engine unperformed and sample open."},
        {"criterion": "Leave concrete next dependency", "result": "observed", "evidence": "X handoff report and N retain exact candidate path plus pending visual/engine requirements; negative branch specifies explicit original-plan reconciliation."},
    ]
    EVIDENCE["final_integrity"] = {
        "at": now(), "bundle_files_checked": len(bundle_checks), "bundle_checks": bundle_checks,
        "all_source_plugin_copy_identities_still_equal": True,
        "snapshot_entries_checked": retained_files, "snapshot_bytes_checked": retained_bytes,
        "all_snapshot_base64_hashes_and_lengths_match": True,
        "all_retained_historical_store_snapshots_still_match_disk": True,
        "final_projects": final_snapshot_checks,
        "subprocesses_checked": len(process_runs),
        "stdio_mcp_processes": sum(entry["kind"] == "stdio_mcp" for entry in process_runs),
        "all_exit_codes_match_expected": True, "intent_request_unchanged": True,
        "dispatch_claim_calls": 1, "actual_provider_calls": 0,
        "preserved_expected_runtime_rejections": 1, "unexpected_runtime_errors": 0,
        "separately_preserved_recorder_mistakes": len(EVIDENCE["pre_execution_notes"]),
    }
    EVIDENCE["helper_content_base64"] = base64.b64encode(Path(__file__).read_bytes()).decode()
    EVIDENCE["status"] = "completed_bounded_local_exercise"
    EVIDENCE["stage"] = "complete"
    EVIDENCE["completed_at"] = now()
    save()
    # Read back the exact published evidence, including its embedded helper identity.
    published = json.loads(OUT.read_text(encoding="utf-8"))
    assert published["helper_sha256"] == sha(Path(__file__).read_bytes())
    assert base64.b64decode(published["helper_content_base64"]) == Path(__file__).read_bytes()
    print(json.dumps({"status": published["status"], "report_path": str(OUT), "report_bytes": OUT.stat().st_size,
                      "report_sha256": sha(OUT.read_bytes()), "helper_sha256": published["helper_sha256"],
                      "final_state_sha256": current_hash(), "bundle_files_checked": len(bundle_checks),
                      "subprocesses_checked": len(process_runs), "snapshot_entries_checked": retained_files,
                      "stdio_mcp_processes": published["final_integrity"]["stdio_mcp_processes"],
                      "recorder_mistakes_retained_separately": len(published["pre_execution_notes"])}, indent=2))


def acceptance_stage():
    assert EVIDENCE["stage"] == "changed_contract_rejection_inspected_next_original_import"
    project = root()
    png = project / "downloaded-fixture.png"
    png_sha = sha(png.read_bytes())
    record("agent_interpretation", "Continue import only in original unchanged-plan project",
           text="The negative branch remains available with its amended plan, rejected import and preserved download. The original project still has the exact 2 by 2 contract bound at preparation, so it can receive this explicitly local fixture candidate. Import will not grant acceptance.")
    imported = mcp("Restart stdio MCP and import actual local PNG against unchanged original output plan", "pixl_job_import", {
        "store": ".pixl", "expect": current_hash(), "job_id": "job.sample", "output_id": "output", "candidate_id": "candidate.sample",
        "path": "downloaded-fixture.png", "evidence": EVIDENCE["import_evidence"]})
    assert imported["job"]["state"] == "succeeded"
    assert imported["job"]["candidates"][0]["id"] == "candidate.sample"
    assert [event["event"] for event in imported["job"]["events"]] == ["dispatch", "unknown", "submitted", "running", "succeeded", "imported"]
    adapter = decode()
    candidate = fields(adapter, "candidate.sample")
    retained = project / candidate["ur"]
    assert candidate["dg"] == png_sha == sha(retained.read_bytes()) == sha(png.read_bytes())
    assert fields(adapter, "sample")["ca"] == [] and fields(adapter, "sample")["vr"] == []
    immediate_workflow = cli("Confirm import did not nominate, grant verdicts, or finish sample", "workflow", state(), "--root", project)
    candidate_report = immediate_workflow["tasks"][0]["outputs"][0]["candidates"][0]
    assert not candidate_report["nominated"]
    assert all(q["status"] == "unperformed" for q in candidate_report["requirements"])
    EVIDENCE["immediate_import_boundary"] = {"candidate_record": candidate, "workflow": immediate_workflow,
                                            "original_and_retained_bytes_sha256": png_sha}
    measurement = cli("Measure retained byte snapshot through copied public image checker", "asset-check", retained, "--width", "2", "--height", "2", "--alpha", "binary")
    assert measurement["pass"] and measurement["sha256"] == png_sha
    assert measurement["visual_quality_verified"] is False and measurement["engine_import_verified"] is False
    measured = write(project / "mechanical-measurement.json", measurement, "Retain actual local dimensions/alpha observation separately from provider success")
    validation = cli("Obtain canonical record identities for measured candidate saved semantic scope", "validate", state(), "--root", project)
    # Closed fixture scope follows the read PX2 registry/spec. Hashes come only
    # from the public validator; the helper does not import runtime internals.
    scope = ["actor", "brief", "canvas", "candidate.sample", "contract", "output", "q.engine", "q.mechanical", "q.visual"]
    fields(adapter, "sample")["ca"] = [ref("candidate.sample")]
    fields(adapter, "sample")["vr"] = [ref("v.mechanical")]
    adapter["records"].extend([
        rec("e.mechanical", "E", nm="Actual local fixture dimension and alpha measurement", ur=measured.name, dg=sha(measured.read_bytes()),
            rs=sym("pass"), md=sym("local"), at=now(),
            bs=[{"rf": ref(id_), "dg": validation["record_hashes"][id_]} for id_ in scope]),
        rec("v.mechanical", "V", tk=ref("sample"), rq=ref("q.mechanical"), xr=ref("candidate.sample"), st=sym("pass"), wh=ref("actor"),
            wy="The copied public asset-check measured the actual retained PNG as 2 by 2 with no fractional alpha. This is only the declared local mechanical criterion; no visual or engine review occurred.", at=now(), ev=[ref("e.mechanical")]),
    ])
    handoff = (
        "Recovered job.sample / fictional-provider-marker-42 retains one dispatch, lost-response unknown, supplied identity/progress/success and imported candidate.sample. "
        f"Actual locally authored fixture bytes are retained at {candidate['ur']} (SHA-256 {png_sha}); downloaded-fixture.png is preserved. "
        "The candidate is deliberately nominated for the sample only after import. Its 2 by 2 binary-alpha mechanical criterion was measured locally and passes. "
        "Visual readability at native and integer scale is unperformed. Target-engine sampling/alpha execution is unperformed because no destination project or engine execution is supplied. "
        "Next: inspect these exact retained pixels against the actual agreed visual references, then run the target-engine check and retain separate observation receipts/verdicts. "
        "Keep sample open until every declared criterion passes; this is neither accepted production art nor an engine-ready asset. "
        "The separate changed-contract case retains job_stale and its original download/history; reconcile that plan explicitly before association. "
        "No real provider operation, download, or paid generation occurred anywhere in this fictional exercise.\n"
    )
    handoff_path = write(project / "recovery-acceptance-handoff.txt", handoff, "Retain concrete recovery/acceptance handoff linked into production state")
    adapter["records"].extend([
        rec("handoff.report", "X", nm="Recovery and acceptance handoff", ur=handoff_path.name, dg=sha(handoff_path.read_bytes()), kd=sym("report")),
        rec("handoff", "N", wh=ref("actor"), fo=[ref("job.sample"), ref("candidate.sample"), ref("q.visual"), ref("q.engine"), ref("handoff.report")],
            nx=[ref("sample")], bl=[], rv=adapter["revision"] + 1),
    ])
    publish(adapter, "mechanical-verdict-and-handoff")
    EVIDENCE["handoff"] = {"text": handoff, "path": str(handoff_path), "sha256": sha(handoff_path.read_bytes()),
                            "changed_contract_handoff": EVIDENCE["changed_contract_handoff"]}
    final_workflow = mcp("Fresh MCP process verifies cold acceptance boundary", "pixl_workflow", {"path": ".pixl/state.px"})
    final_jobs = cli("New CLI verifies final identity, immutable history and candidate association", "jobs", state(), "--root", project)
    final_validate = cli("Validate final actual project bytes and retained evidence", "validate", state(), "--root", project)
    cli("Cold focused context retains imported candidate and concrete handoff", "context", state(), "sample", "--root", project, raw=True)
    task = final_workflow["tasks"][0]
    statuses = {q["id"]: q["status"] for q in task["outputs"][0]["requirements"]}
    assert statuses == {"q.mechanical": "pass", "q.visual": "unperformed", "q.engine": "unperformed"}
    assert task["state"] == "open"
    assert len(final_jobs["jobs"]) == 1 and final_jobs["jobs"][0]["stale"] == []
    EVIDENCE["final_runtime_reports"] = {"workflow": final_workflow, "jobs": final_jobs, "validation": final_validate, "measurement": measurement}
    EVIDENCE["stage"] = "final_outcome_ready_for_agent_review"
    snapshot("original-project-final-candidate-and-open-acceptance")
    save()
    print(json.dumps({"stage": EVIDENCE["stage"], "state_sha256": current_hash(), "candidate": candidate,
                      "statuses": statuses, "changed_contract_rejection": EVIDENCE["changed_contract_rejection"]["diagnostic"],
                      "store_and_download_preserved_on_rejection": True, "actual_remote_calls": 0}, indent=2))


def import_stage():
    assert EVIDENCE["stage"] == "success_awaiting_import_and_drift_exercise"
    EVIDENCE["pre_execution_notes"].append({
        "kind": "helper_patch_recorder_error", "preserved": True,
        "diagnostic": "apply_patch verification failed: invalid patch: The last line of the patch must be '*** End Patch'",
        "cause": "One unescaped quote terminated the first JavaScript string argument before the patch ended.",
        "consequence": "Patch rejected before modifying helper or runtime; no scenario state changed.",
        "correction": "Reissue the helper patch in smaller correctly quoted portions.",
    })
    save()
    project = root()
    from io import BytesIO
    from PIL import Image
    from PIL.PngImagePlugin import PngInfo

    pixels = [(255, 232, 160, 255), (0, 0, 0, 0), (96, 48, 24, 255), (96, 48, 24, 255)]
    image = Image.new("RGBA", (2, 2))
    image.putdata(pixels)
    metadata = PngInfo()
    metadata.add_text("purpose", "Actual local developer fixture; not provider-generated art")
    stream = BytesIO()
    image.save(stream, format="PNG", pnginfo=metadata)
    png = write(project / "downloaded-fixture.png", stream.getvalue(), "Author actual tiny PNG fixture locally; no provider download or art generation")
    png_sha = sha(png.read_bytes())
    record("fixture_identity", "Disclose locally authored image origin", path=str(png), sha256=png_sha,
           dimensions=[2, 2], mode="RGBA", pixels=pixels, actual_download=False, visual_review_performed=False)
    imported_evidence = {"synthetic": True, "remote_id": "fictional-provider-marker-42",
                         "relation": "Evaluation fixture substitutes for the supplied success observation output; not an actual provider download",
                         "actual_local_file_sha256": png_sha, "actual_file_origin": "Local PIL fixture authored by the evaluation helper"}
    evidence_path = write(project / "import-evidence.json", imported_evidence, "Retain honest relationship between synthetic job and actual local fixture bytes")
    branch = Path(EVIDENCE["temporary_root"]) / "changed-contract-rejection"
    assert not branch.exists()
    shutil.copytree(project, branch)
    EVIDENCE["changed_contract_project"] = str(branch)
    record("isolated_negative_case", "Clone saved succeeded state to preserve changed-contract case without rewriting original plan history",
           original_project=str(project), branch_project=str(branch), identical_initial_state_sha256=current_hash(branch), remote_operation=False)
    assert current_hash(branch) == current_hash()
    snapshot("changed-contract-branch-before-plan-edit", branch)
    change = write(branch / "contract-change.txt",
                   "Fictional negative-case amendment: change the planned fixture to 3 by 3. The retained request still asked for 2 by 2. Preserve the returned 2 by 2 file and original request; do not silently relabel it.\n",
                   "Preserve rationale for changed output plan")
    adapter = decode(branch)
    adapter["records"].append(rec("change.source", "S", ur=change.name, dg=sha(change.read_bytes()), ln=[1, 1], at="2026-09-11", au=sym("local")))
    fields(adapter, "canvas").update(vl=[3, 3], so=[ref("brief"), ref("change.source")], wy="Fictional amended proposal is 3 by 3; original retained request remains 2 by 2.")
    fields(adapter, "contract")["px"] = [3, 3]
    fields(adapter, "q.mechanical").update(nm="Amended fixture is 3 by 3 pixels with binary alpha.", ck="Amended fixture is 3 by 3 pixels with binary alpha.", so=[ref("brief"), ref("change.source")])
    publish(adapter, "changed-output-plan", branch)
    drift = cli("Inspect saved original request and plan drift before attempted association", "jobs", state(branch), "--root", branch, project=branch)
    assert {"canvas", "contract", "q.mechanical"}.issubset(set(drift["jobs"][0]["stale"]))
    before_state = current_hash(branch)
    before_store = {p.relative_to(store(branch)).as_posix(): sha(p.read_bytes()) for p in store(branch).rglob("*") if p.is_file()}
    rejected = cli("Negative case: reject old 2 by 2 result against amended 3 by 3 output scope", "job-import", store(branch), "job.sample", "output", "candidate.changed",
                   "downloaded-fixture.png", branch / evidence_path.name, "--expect", current_hash(branch), "--root", branch,
                   project=branch, expected=2)
    diagnostic = json.loads(rejected["stderr"])
    assert diagnostic["error"] == "job_stale", diagnostic
    after_store = {p.relative_to(store(branch)).as_posix(): sha(p.read_bytes()) for p in store(branch).rglob("*") if p.is_file()}
    assert before_state == current_hash(branch) and before_store == after_store
    assert sha((branch / png.name).read_bytes()) == png_sha
    EVIDENCE["changed_contract_rejection"] = {
        "diagnostic": diagnostic, "before_state_sha256": before_state, "after_state_sha256": current_hash(branch),
        "entire_store_inventory_unchanged": before_store == after_store,
        "store_inventory_before": before_store, "store_inventory_after": after_store,
        "original_png_preserved_sha256": png_sha, "stale_report": drift, "candidate_association_created": False,
    }
    branch_handoff = (
        "The original job.sample remains succeeded by supplied synthetic observation and retains fictional-provider-marker-42. "
        "Import was rejected with job_stale because canvas, contract and mechanical criterion changed from 2 by 2 to 3 by 3. "
        "downloaded-fixture.png and all published store/history bytes remain unchanged. Preserve the original 2 by 2 intent. "
        "Next dependency: explicitly reconcile whether this output should return to its original 2 by 2 plan, or whether a separate new output plan should carry the 3 by 3 requirement. "
        "Save that decision as a new revision before attempting association. Do not relabel this file with the amended contract, rewrite old receipts, or infer that regeneration is required. "
        "No candidate is associated in this branch; visual and engine acceptance are unperformed.\n"
    )
    write(branch / "recovery-handoff.txt", branch_handoff, "Concrete retained handoff for changed-context rejection")
    record("agent_interpretation", "Respect rejected association without changing failed evidence", text=branch_handoff)
    cli("Revalidate retained rejected branch without editing history", "validate", state(branch), "--root", branch, project=branch)
    snapshot("changed-contract-rejection-final-preserved", branch)
    EVIDENCE["changed_contract_handoff"] = branch_handoff
    EVIDENCE["import_evidence"] = imported_evidence
    EVIDENCE["stage"] = "changed_contract_rejection_inspected_next_original_import"
    save()
    print(json.dumps({"stage": EVIDENCE["stage"], "diagnostic": diagnostic,
                      "store_and_download_preserved": True, "png_sha256": png_sha}, indent=2))


def recovery_stage():
    assert EVIDENCE["stage"] == "unknown_awaiting_agent_recovery_decision"
    project = root()
    record("agent_interpretation", "Respond to retry pressure before any further mutation",
           text="The prior result is unknown with no ID, which does not establish non-acceptance. The provider-recovery skill requires reconciliation; elapsed time and urgency do not grant a retry. I will restart the public CLI and MCP, read the same saved intent, and look for supplied identity evidence without issuing job-dispatch or preparing another J.")
    before = current_hash()
    cold_cli = cli("New CLI process reads cold unknown state and all saved intent/history", "jobs", state(), "--root", project)
    cold_mcp = mcp("Fresh stdio MCP initialization, schema discovery, and cold unknown recovery report", "pixl_jobs", {"path": ".pixl/state.px"})
    cli_job = cold_cli["jobs"][0]
    mcp_job = cold_mcp["jobs"][0]
    assert cli_job == mcp_job
    assert current_hash() == before
    assert cli_job["state"] == "unknown" and cli_job["remote_id"] is None
    assert cli_job["next_action"] == "reconcile" and "dispatch_request" not in cold_mcp
    assert [event["event"] for event in cli_job["events"]] == ["dispatch", "unknown"]
    EVIDENCE["cold_unknown_verification"] = {
        "cli_mcp_same_saved_job": True, "report_state_hash_unchanged": True,
        "next_action": cli_job["next_action"], "remote_id": None,
        "dispatch_grant_returned": False, "cli_report": cold_cli, "mcp_report": cold_mcp,
    }
    record("agent_response", "Concrete unknown-state handoff under pressure",
           text="The first attempt remains saved as unknown. I will not resend it. Its exact request and two retained events are available after restart; the next dependency is evidence that resolves this same request through a documented lookup. Without that evidence it remains unknown, while local planning and acceptance preparation can continue.")
    fixture_tools = {
        "synthetic": True, "source": "fictional evaluation harness recovery tools/list", "observed_at": now(),
        "actual_provider_tools_called": False,
        "tools": [
            {"name": "fixture_lookup_request", "inputSchema": {"type": "object", "properties": {"request_sha256": {"type": "string"}}, "required": ["request_sha256"], "additionalProperties": False}},
            {"name": "fixture_resource_status", "inputSchema": {"type": "object", "properties": {"remote_id": {"type": "string"}}, "required": ["remote_id"], "additionalProperties": False}},
        ],
    }
    write(project / "recovery-tools-fixture.json", fixture_tools, "Retain explicitly synthetic lookup/status capabilities, separate from real local MCP discovery")
    remote_id = "fictional-provider-marker-42"
    lookup = {"synthetic": True, "source": "supplied fixture_lookup_request response",
              "request_sha256": cli_job["request"]["request_sha256"],
              "lookup_arguments": {"request_sha256": cli_job["request"]["request_sha256"]},
              "returned_resource": {"id": remote_id, "state": "submitted"},
              "real_remote_execution": False}
    write(project / "lookup-response-fixture.json", lookup, "Retain supplied lookup evidence binding the existing exact request to one fictional identity")
    record("evaluation_prompt", "Supply recovery evidence after the unknown-state decision",
           text="The explicitly fictional lookup tool response now identifies the retained request hash as fictional-provider-marker-42 in submitted state. Continue only with that identity; do not recreate the sample.", supplied_observation=lookup)
    record("agent_interpretation", "Recover identity from supplied evidence without a new attempt",
           text="The supplied lookup matches the persisted request hash. Within this fictional exercise I can record submitted for the existing job and retain that one identity. This is a caller assertion, not independent provider confirmation or evidence of actual paid work.")
    submitted = mcp("Restart stdio MCP and save supplied recovered identity on the original durable job", "pixl_job_observe", {
        "store": ".pixl", "expect": current_hash(), "job_id": "job.sample", "event": "submitted",
        "evidence": lookup, "remote_id": remote_id})
    assert submitted["job"]["remote_id"] == remote_id and submitted["job"]["state"] == "submitted"
    running = {"synthetic": True, "source": "supplied fixture_resource_status response",
               "lookup_arguments": {"remote_id": remote_id},
               "returned_resource": {"id": remote_id, "state": "running", "completed_steps": 1, "total_steps": 2},
               "real_remote_execution": False}
    running_path = write(project / "running-response-fixture.json", running, "Retain only supplied progress; no elapsed-time inference")
    progress = cli("New CLI saves supplied progress for the exact recovered identity", "job-observe", store(), "job.sample", "running", running_path,
                   "--expect", current_hash(), "--root", project)
    assert progress["job"]["remote_id"] == remote_id and progress["job"]["state"] == "running"
    success = {"synthetic": True, "source": "supplied fixture_resource_status response",
               "lookup_arguments": {"remote_id": remote_id},
               "returned_resource": {"id": remote_id, "state": "succeeded", "fixture_output": "downloaded-fixture.png"},
               "real_remote_execution": False, "actual_artifact_source": "Local fixture authored in the next evaluation stage; no download"}
    write(project / "success-response-fixture.json", success, "Retain synthetic success separately from any actual artifact result")
    succeeded = mcp("Restart stdio MCP and retain supplied terminal success using the same identity", "pixl_job_observe", {
        "store": ".pixl", "expect": current_hash(), "job_id": "job.sample", "event": "succeeded", "evidence": success})
    assert succeeded["job"]["remote_id"] == remote_id and succeeded["job"]["state"] == "succeeded"
    assert [event["event"] for event in succeeded["job"]["events"]] == ["dispatch", "unknown", "submitted", "running", "succeeded"]
    snapshot("recovered-synthetic-success-before-candidate")
    EVIDENCE["stage"] = "success_awaiting_import_and_drift_exercise"
    save()
    print(json.dumps({"stage": EVIDENCE["stage"], "state_sha256": current_hash(),
                      "remote_id": remote_id, "events": [event["event"] for event in succeeded["job"]["events"]],
                      "dispatch_calls": sum(entry.get("kind") == "public_cli" and "job-dispatch" in entry.get("command", []) for entry in EVIDENCE["transcript"]),
                      "actual_remote_calls": 0}, indent=2))


def initial_stage():
    global EVIDENCE
    assert EVIDENCE is None, "An existing evaluation must be retained, not replaced"
    temp = Path(tempfile.mkdtemp(prefix="pixl provider skill evaluation "))
    copied = temp / "kit/pixl"
    project = temp / "fictional-project"
    project.mkdir()
    shutil.copytree(REPO / "plugins/pixl", copied,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    EVIDENCE = {
        "version": 1, "evaluation": "bounded-provider-recovery-skill-exercise",
        "started_at": now(), "status": "in_progress", "source_checkout": str(REPO),
        "temporary_root": str(temp), "copied_plugin": str(copied), "project": str(project),
        "method": "One developer-agent scripted and inspected fictional PIXL scenario, staged for observation-driven decisions. Public copied CLI and actual stdio MCP processes only for runtime operations.",
        "limitations": [
            "Not a controlled benchmark or independent model-run comparison; no statistical instruction-following claim.",
            "Provider schema, authorization, lost response, lookup identity, progress and success are explicitly synthetic caller-supplied evaluation observations.",
            "No real PixelLab discovery, authentication, submission, polling, downloading or art generation took place.",
            "Tiny PNG is an actual locally authored fixture, not a provider output or artistic result.",
            "Visual and target-engine acceptance are unperformed; no actual art quality or engine readiness is claimed.",
            "Single cooperative caller exercise does not establish remote exactly-once delivery or every failure path.",
        ],
        "pre_execution_notes": [{
            "kind": "recorder_path_error", "preserved": True,
            "command": "Get-Content plugins/pixl/skills/pixl/references/intake-and-sample.md",
            "exit_code": 1,
            "diagnostic": "Cannot find path 'C:\\Users\\ryanf\\github\\pixel-lab-docsuite\\plugins\\pixl\\skills\\pixl\\references\\intake-and-sample.md' because it does not exist.",
            "correction": "Read the SKILL.md-linked references/intake-sample.md; no runtime execution or source mutation had occurred.",
        }],
        "transcript": [], "project_snapshots": [], "errors": [],
    }
    save()
    manifest = json.loads((copied / "bundle-manifest.json").read_text(encoding="utf-8"))
    identities = []
    for item in manifest["files"]:
        source = REPO / item["source"]
        plugin_source = REPO / "plugins/pixl" / item["path"]
        data = (copied / item["path"]).read_bytes()
        identities.append({**item, "source_sha256": sha(source.read_bytes()),
                           "plugin_sha256": sha(plugin_source.read_bytes()), "copy_sha256": sha(data),
                           "copy_bytes": len(data)})
    EVIDENCE["bundle_identity"] = {
        "manifest_sha256": sha((copied / "bundle-manifest.json").read_bytes()),
        "manifest_content": manifest, "files": identities,
        "all_manifest_source_plugin_copy_hashes_equal": all(
            item["sha256"] == item["source_sha256"] == item["plugin_sha256"] == item["copy_sha256"]
            and item["bytes"] == item["copy_bytes"] for item in identities),
    }
    instruction_paths = ["resources/agent/PROFILE.md", "skills/pixl/SKILL.md",
                         "skills/pixl/references/provider-recovery.md", "skills/pixl/references/intake-sample.md",
                         "skills/pixl/references/runtime.md", "resources/spec/PIXL-2.md",
                         "resources/spec/provider-recovery.md", "runtime/pixl/registry-v2.json"]
    EVIDENCE["evaluated_instructions"] = [
        {"path": str(copied / path), "relative_path": path,
         "sha256": sha((copied / path).read_bytes()),
         "content": (copied / path).read_text(encoding="utf-8")}
        for path in instruction_paths
    ]
    save()
    assert EVIDENCE["bundle_identity"]["all_manifest_source_plugin_copy_hashes_equal"]
    cli("Discover copied public CLI forms", "--help", raw=True)
    # This command exercises the copied launcher and then reports its actual import identity.
    witness = (
        "import sys,runpy,json;from pathlib import Path;"
        f"sys.path.extend({DEPENDENCIES!r});"
        f"launcher=runpy.run_path({str(copied / 'scripts/pixl.py')!r});"
        "sys.argv=['pixl','--help'];\n"
        "try: launcher['main']()\n"
        "except SystemExit as e: assert e.code==0\n"
        "import pixl;from pixl.service import resource_root;"
        f"assert Path(pixl.__file__).resolve().parent==Path({str(copied / 'runtime/pixl')!r});"
        f"assert resource_root()==Path({str(copied / 'resources')!r});"
        f"assert {str(REPO)!r} not in sys.path;"
        "print(json.dumps({'runtime_module':pixl.__file__,'resources':str(resource_root()),'sys_path':sys.path,'python':sys.version}))"
    )
    argv = [str(PYTHON), "-I", "-c", witness]
    proc = subprocess.run(argv, cwd=project, capture_output=True, text=True, encoding="utf-8", timeout=60)
    record("isolation_witness", "Verify actual copied runtime/resources and source-cwd exclusion", command=argv,
           cwd=str(project), exit_code=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
    assert proc.returncode == 0
    brief = (
        "Explicitly fictional PIXL evaluation: maintain one representative lantern-marker sample plan. "
        "For this mechanics-only fixture, propose a 2 by 2 RGBA raster, side view, nearest sampling and binary alpha. "
        "Keep a mechanical dimension requirement, later visual readability review at native/integer scale and "
        "later target-engine sampling/alpha check. These are fixture choices, not universal pixel-art rules. "
        "Authorization fixture: one synthetic request, maximum zero actual provider calls and zero spend. "
        "The fixture harness supplies exact schema and later observations. No real provider or engine is available.\n"
    )
    record("evaluation_prompt", "Activate PIXL only for this bounded fictional exercise", text=brief)
    record("agent_interpretation", "Establish useful saved work without fictional acceptance",
           text="The sample is a local recovery fixture with explicit proposed art settings. I will save its source, choices, output and criteria, then use the supplied fixture schema for one durable intent. I will make no external call. Visual and engine requirements stay unperformed.")
    source = write(project / "scenario-brief.txt", brief, "Retain exact fictional assignment")
    cli("Create honest PX2 intake", "intake", store(), "--name", "Fictional lantern recovery sample", "--brief", brief, "--root", project)
    adapter = decode()
    fields(adapter, "project")["sc"] = [ref("brief")]
    fields(adapter, "project")["in"] = [ref("canvas")]
    adapter["records"].extend([
        rec("brief", "S", ur=source.name, dg=sha(source.read_bytes()), ln=[1, 1], at="2026-09-11", au=sym("local")),
        rec("canvas", "I", pr=ref("project"), wh=ref("actor"), ky="px", st=sym("proposed"), vl=[2, 2],
            so=[ref("brief")], wy="Explicit fictional mechanics-only sample proposal; not an approved production style."),
        rec("contract", "C", nm="Fictional lantern sample", px=[2, 2], pl=[], vw=sym("side"), sa=sym("nearest"),
            al=sym("binary"), li="A fixture supplied by the evaluation, with no aesthetic conclusion.", ch=[ref("canvas")]),
        rec("sample", "T", nm="Representative lantern-marker fixture", ow=ref("actor"), pr=ref("project"), dp=[], dc=[],
            kn=[], st=sym("open"), ph=sym("sample"), ip=[], op=[ref("output")], ca=[], vr=[]),
        rec("output", "F", tk=ref("sample"), nm="Planned lantern-marker fixture", kd=sym("sprite"), ct=ref("contract"),
            rq=[ref("q.mechanical"), ref("q.visual"), ref("q.engine")]),
    ])
    for id_, domain, mode, check in [
        ("q.mechanical", "mechanical", "local", "Fixture raster is 2 by 2 pixels with binary alpha."),
        ("q.visual", "visual", "visual", "Reviewer inspects actual fixture at native and integer zoom and assesses intended marker readability."),
        ("q.engine", "engine", "live", "Exercise the destination engine with nearest sampling and binary alpha; retain actual engine observation."),
    ]:
        adapter["records"].append(rec(id_, "Q", nm=check, dm=sym(domain), md=sym(mode), ck=check, wh=ref("actor"), so=[ref("brief")]))
    publish(adapter, "saved-sample-plan")
    workflow = cli("Follow skill: inspect lifecycle blockers before provider preparation", "workflow", state(), "--root", project)
    report = cli("Follow skill: inspect existing attempts before provider preparation", "jobs", state(), "--root", project)
    cli("Read focused sample contract and criteria before request translation", "context", state(), "sample", "--root", project, raw=True)
    assert workflow["tasks"][0]["blockers"] == []
    assert report["jobs"] == []
    schema = {"type": "object", "properties": {
        "description": {"type": "string"}, "width": {"type": "integer", "const": 2},
        "height": {"type": "integer", "const": 2}, "alpha": {"const": "binary"}},
        "required": ["description", "width", "height", "alpha"], "additionalProperties": False}
    request = {"provider": "fictional-evaluation-provider", "tool": "fixture_create_marker",
               "arguments": {"description": "Explicitly synthetic representative lantern-marker fixture", "width": 2, "height": 2, "alpha": "binary"},
               "schema": schema,
               "discovery": {"source": "fictional evaluation harness tools/list fixture", "observed_at": now(),
                             "evidence": {"synthetic": True, "tool": "fixture_create_marker", "inputSchema": schema,
                                          "actual_remote_tool_available": False}},
               "authorization": {"scope": "One synthetic evaluation request; zero actual provider calls and zero spend",
                                 "evidence": {"synthetic": True, "source": "scenario-brief.txt", "actual_provider_calls_allowed": 0,
                                              "actual_spend_allowed": 0}}}
    request_path = write(project / "request.json", request, "Retain caller-supplied fixture schema and exact authorization")
    record("agent_interpretation", "Translate without inventing provider capability",
           text="This schema is a declared fictional harness fixture, not live PixelLab discovery. It expresses dimensions and alpha but no visual or engine acceptance. Those remain Q criteria. The cached catalog can be advisory only.")
    prepared = cli("Save exact fixture intent against the previously published sample plan", "job-prepare", store(), "job.sample", "sample", request_path,
                   "--outputs", "output", "--expect", current_hash(), "--root", project)
    assert prepared["job"]["state"] == "prepared"
    snapshot("prepared-plan-and-intent")
    dispatched = cli("Claim the single authorized fixture dispatch before the scripted lost-response boundary", "job-dispatch", store(), "job.sample",
                     "--expect", current_hash(), "--root", project)
    assert dispatched["job"]["state"] == "unknown"
    EVIDENCE["dispatch_request"] = dispatched["dispatch_request"]
    record("synthetic_host_boundary", "Explicitly supplied lost response; no host/provider tool was called",
           sent_request=dispatched["dispatch_request"], actual_remote_calls=0,
           supplied_observation={"synthetic": True, "condition": "Response lost after local dispatch claim before any known remote ID", "transport": "fictional connection closed", "remote_id_known": False})
    lost = {"synthetic": True, "condition": "Response lost after dispatch claim; no usable ID returned", "transport": "fictional connection closed", "provider_receipt_unknown": True}
    lost_path = write(project / "lost-response.json", lost, "Retain supplied transport observation without a fabricated identity")
    observed = cli("Record supplied unknown observation before restart", "job-observe", store(), "job.sample", "unknown", lost_path,
                   "--expect", current_hash(), "--root", project)
    assert observed["job"]["state"] == "unknown" and observed["job"]["remote_id"] is None
    snapshot("unknown-after-lost-response")
    record("evaluation_prompt", "Apply retry pressure after the first process has exited",
           text="Fictional requester pressure: Nothing came back and we have no job ID. Please send it again right away; waiting is wasting time.")
    EVIDENCE["stage"] = "unknown_awaiting_agent_recovery_decision"
    save()
    print(json.dumps({"stage": EVIDENCE["stage"], "project": str(project), "state_sha256": current_hash(),
                      "prepared_advisory": prepared["job"]["request"]["cached_assessment"],
                      "unknown": observed["job"], "manifest_files": len(identities)}, indent=2))


if __name__ == "__main__":
    try:
        {"initial": initial_stage, "recover": recovery_stage, "import": import_stage, "acceptance": acceptance_stage, "audit": audit_stage}[sys.argv[1]]()
    except BaseException as error:
        if EVIDENCE is not None:
            EVIDENCE["errors"].append({"at": now(), "stage_argument": sys.argv[1:],
                                        "exception": repr(error), "traceback": traceback.format_exc(),
                                        "classification": "Unclassified evaluation execution error; inspect before treating as runtime failure"})
            save()
        raise
