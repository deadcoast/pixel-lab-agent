"""Bounded developer-agent scenario recorder; never executes a remote service.

Run with the selected .venv Python. All operational PIXL commands use a copied
bundle, isolated Python, and dependency site-packages only. Source imports are
permitted solely inside the explicitly marked synthetic fixture preparation.
"""

import base64
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = Path(__file__).with_name("behavior-evaluation.json")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(report):
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run(report, command, cwd, *, stdin=None, purpose, expected=0):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PIXL_PLUGIN_ROOT", None)
    result = subprocess.run(command, cwd=cwd, env=env, input=stdin,
                            text=True, encoding="utf-8", capture_output=True,
                            timeout=30, check=False)
    report["operations"].append({
        "purpose": purpose, "command": list(map(str, command)), "cwd": str(cwd),
        "stdin": stdin, "exit_code": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr,
        "expected_exit_code": expected,
    })
    save(report)
    if result.returncode != expected:
        raise RuntimeError(f"{purpose}: exit {result.returncode}; {result.stderr}; {result.stdout}")
    return result.stdout


def cli(report, project, args, purpose, expected=0):
    return run(report, report["isolation"]["runner"] + list(map(str, args)), project,
               purpose=purpose, expected=expected)


def json_cli(report, project, args, purpose, expected=0):
    output = cli(report, project, args, purpose, expected)
    return json.loads(output if output.strip() else report["operations"][-1]["stderr"])


def write(report, path, text, purpose):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    report["operations"].append({"purpose": purpose, "operation": "write_project_file",
                                  "path": str(path), "sha256": sha(path), "text": text})
    save(report)


def read(report, path, purpose):
    path = Path(path)
    value = path.read_text(encoding="utf-8")
    report["operations"].append({"purpose": purpose, "operation": "read_retained_file",
                                  "path": str(path), "sha256": sha(path), "text": value})
    save(report)
    return value


def mcp(report, project, calls, purpose):
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "bounded-developer-evaluation", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
    ]
    requests.extend({"jsonrpc": "2.0", "id": index + 3, "method": "tools/call", "params": {"name": name, "arguments": arguments}}
                    for index, (name, arguments) in enumerate(calls))
    output = run(report, report["isolation"]["runner"] + ["mcp", "--root", str(project)],
                 project, stdin="".join(json.dumps(row) + "\n" for row in requests), purpose=purpose)
    replies = [json.loads(line) for line in output.splitlines()]
    assert len(replies) == len(requests) - 1
    for reply in replies:
        assert "error" not in reply, reply
        assert not reply["result"].get("isError", False), reply
    return replies


def records(document):
    return {row["id"]: row for row in document["records"]}


def ref(id_):
    return {"$ref": id_}


def symbol(value):
    return {"$symbol": value}


def row(id_, kind, **fields):
    return {"id": id_, "kind": kind, "fields": fields}


def publish(report, project, document, label):
    state = project / ".px2/state.px"
    current = json_cli(report, project, ["validate", state, "--root", project], label + ": read canonical current identity")
    assert document["revision"] == current["revision"] + 1
    json_path, px_path = project / (label + ".json"), project / (label + ".px")
    write(report, json_path, json.dumps(document, indent=2) + "\n", label + ": author exact declared host records")
    cli(report, project, ["encode", json_path, "--out", px_path], label + ": encode through copied public runner")
    json_cli(report, project, ["validate", px_path, "--root", project], label + ": validate candidate against actual project files")
    return json_cli(report, project, ["commit", project / ".px2", px_path, "--expect", current["hash"], "--root", project], label + ": commit against observed hash")


def setup():
    if REPORT.exists():
        raise RuntimeError("Evidence already exists; never overwrite a recorded attempt.")
    temp = Path(tempfile.mkdtemp(prefix="pixl intake agent evaluation "))
    plugin = temp / "kit/pixl"
    shutil.copytree(ROOT / "plugins/pixl", plugin, ignore=shutil.ignore_patterns("__pycache__"))
    dependencies = [path for path in sys.path if path.endswith("site-packages")]
    launch = f"import sys,runpy;sys.path.extend({dependencies!r});p=sys.argv[1];sys.argv=sys.argv[1:];runpy.run_path(p,run_name='__main__')"
    manifest = json.loads((plugin / "bundle-manifest.json").read_text(encoding="utf-8"))
    report = {
        "schema": 1, "recorded_at": datetime.now(timezone.utc).isoformat(),
        "kind": "single developer-agent recorded scenario exercise",
        "role_boundary": "Developer outside the two explicitly fictional scenarios; PIXL profile adopted only while interpreting and operating each scenario. This is not a controlled benchmark.",
        "status": "in_progress", "operations": [], "scenario_results": {},
        "limits": ["No real production assignment or approved project style.", "No provider, generated art, global setting, UI, or engine execution.", "Scenario two visual and engine verdicts are deliberately supplied fixtures, not this agent's actual visual judgment or engine proof.", "Successful commands validate local implemented mechanics; they do not establish artistic quality, cross-agent reliability, or behavioral improvement."],
        "snapshot": {"root": str(plugin), "retained_temporary_root": str(temp),
                     "manifest_sha256": sha(plugin / "bundle-manifest.json"),
                     "manifest": manifest,
                     "files": [{"path": str(path.relative_to(plugin)).replace("\\", "/"), "sha256": sha(path), "bytes": path.stat().st_size}
                               for path in sorted(plugin.rglob("*")) if path.is_file()],
                     "manifest_mismatches": [entry["path"] for entry in manifest["files"] if sha(plugin / entry["path"]) != entry["sha256"]]},
        "isolation": {"python": sys.executable, "dependencies": dependencies,
                      "removed_environment_keys": ["PYTHONPATH", "PIXL_PLUGIN_ROOT"],
                      "runner": [sys.executable, "-I", "-c", launch, str(plugin / "scripts/pixl.py")]},
    }
    save(report)
    assert not report["snapshot"]["manifest_mismatches"], report["snapshot"]["manifest_mismatches"]
    for name in ("scenario1", "scenario2"):
        (temp / name).mkdir()
    isolation_probe = (
        "import sys,runpy,os,json;from pathlib import Path;"
        f"sys.path.extend({dependencies!r});"
        f"launcher=runpy.run_path({str(plugin / 'scripts/pixl.py')!r});"
        "sys.argv=['pixl','sources'];launcher['main']();"
        "import pixl;from pixl.service import resource_root;"
        f"assert Path(pixl.__file__).resolve().parent==Path({str(plugin / 'runtime/pixl')!r});"
        f"assert resource_root()==Path({str(plugin / 'resources')!r});"
        "print(json.dumps({'runtime_module':pixl.__file__,'resource_root':str(resource_root()),'sys_path':sys.path}))"
    )
    run(report, [sys.executable, "-I", "-c", isolation_probe], temp / "scenario1",
        purpose="Verify the copied launcher's actual runtime/resource paths and isolated import routes")
    print(json.dumps({"report": str(REPORT), "snapshot": str(plugin), "manifest_sha256": report["snapshot"]["manifest_sha256"]}))


def resume_setup():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    plugin = Path(report["snapshot"]["root"])
    temp = Path(report["snapshot"]["retained_temporary_root"])
    report["operations"].append({"purpose": "Preserve failed initial snapshot consistency assertion",
        "command": [".venv/Scripts/python.exe", "evidence/intake-sample/helper.py", "setup"],
        "cwd": str(ROOT), "exit_code": 1,
        "stdout": "", "stderr": "AssertionError: ['skills/pixl/references/production.md', 'skills/pixl/references/runtime.md']",
        "judgment": "Manifest inconsistency prevents claiming coherent packaging for this snapshot. Continue scenario mechanics against retained exact copied bytes; do not repair or regenerate this snapshot."})
    for name in ("scenario1", "scenario2"):
        (temp / name).mkdir(exist_ok=True)
    dependencies = report["isolation"]["dependencies"]
    probe = (
        "import sys,runpy,json;from pathlib import Path;"
        f"sys.path.extend({dependencies!r});"
        f"launcher=runpy.run_path({str(plugin / 'scripts/pixl.py')!r});"
        "sys.argv=['pixl','sources'];launcher['main']();"
        "import pixl;from pixl.service import resource_root;"
        f"assert Path(pixl.__file__).resolve().parent==Path({str(plugin / 'runtime/pixl')!r});"
        f"assert resource_root()==Path({str(plugin / 'resources')!r});"
        "print(json.dumps({'runtime_module':pixl.__file__,'resource_root':str(resource_root()),'sys_path':sys.path}))"
    )
    run(report, [sys.executable, "-I", "-c", probe], temp / "scenario1",
        purpose="Verify actual copied launcher/runtime/resource isolation")
    index = json_cli(report, temp / "scenario1", ["knowledge"], "Discover actual installed method identifiers for edge-treatment research")
    print(json.dumps({"snapshot": str(plugin), "knowledge_index": index}, indent=2))


def fresh_snapshot():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    report.setdefault("previous_snapshots", []).append({
        "snapshot": report["snapshot"], "isolation": report["isolation"],
        "operation_range": [0, len(report["operations"]) - 1],
        "status": "packaging_preflight_failed",
        "reason": "Parent confirmed concurrent instruction edits caused the manifest inconsistency, rebuilt the bundle, and requested a fresh scenario snapshot. Old bytes and failed assertion remain retained."})
    temp = Path(tempfile.mkdtemp(prefix="pixl intake agent fresh evaluation "))
    plugin = temp / "kit/pixl"
    shutil.copytree(ROOT / "plugins/pixl", plugin, ignore=shutil.ignore_patterns("__pycache__"))
    manifest = json.loads((plugin / "bundle-manifest.json").read_text(encoding="utf-8"))
    report["snapshot"] = {"root": str(plugin), "retained_temporary_root": str(temp),
        "manifest_sha256": sha(plugin / "bundle-manifest.json"), "manifest": manifest,
        "files": [{"path": str(path.relative_to(plugin)).replace("\\", "/"), "sha256": sha(path), "bytes": path.stat().st_size}
                  for path in sorted(plugin.rglob("*")) if path.is_file()],
        "manifest_mismatches": [entry["path"] for entry in manifest["files"] if sha(plugin / entry["path"]) != entry["sha256"]]}
    report["isolation"] = copy.deepcopy(report["isolation"])
    report["isolation"]["runner"][-1] = str(plugin / "scripts/pixl.py")
    save(report)
    assert not report["snapshot"]["manifest_mismatches"]
    for name in ("scenario1", "scenario2"):
        (temp / name).mkdir()
    dependencies = report["isolation"]["dependencies"]
    probe = (
        "import sys,runpy,json;from pathlib import Path;"
        f"sys.path.extend({dependencies!r});"
        f"launcher=runpy.run_path({str(plugin / 'scripts/pixl.py')!r});"
        "sys.argv=['pixl','sources'];launcher['main']();"
        "import pixl;from pixl.service import resource_root;"
        f"assert Path(pixl.__file__).resolve().parent==Path({str(plugin / 'runtime/pixl')!r});"
        f"assert resource_root()==Path({str(plugin / 'resources')!r});"
        "print(json.dumps({'runtime_module':pixl.__file__,'resource_root':str(resource_root()),'sys_path':sys.path}))"
    )
    run(report, [sys.executable, "-I", "-c", probe], temp / "scenario1", purpose="Fresh coherent copied snapshot: verify launcher/runtime/resource isolation")
    method = json_cli(report, temp / "scenario1", ["knowledge", "silhouette-readability"], "Inspect discovered silhouette method applicable to representative item identity")
    print(json.dumps({"snapshot": str(plugin), "manifest_sha256": report["snapshot"]["manifest_sha256"], "method": method}, indent=2))


def scenario1():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    plugin = Path(report["snapshot"]["root"])
    project = Path(report["snapshot"]["retained_temporary_root"]) / "scenario1"
    prompt = ("Fictional evaluation request: Begin one representative item before its item family. "
              "Canvas size is undecided. One source requests continuous dark outlines; the other "
              "requests selective edges. Preserve both directions. Native identity/readability and "
              "eventual destination-engine import are requirements. No actual images, provider or "
              "target-engine project are supplied. The bundled intake example is syntax data only, "
              "not project-approved style.\n")
    report["scenario_results"]["scenario1"] = {"prompt": prompt, "role": "PIXL explicitly adopted for this fictional scenario only", "status": "in_progress"}
    write(report, project / "scenario-brief.txt", prompt, "Retain fictional requester instruction as project source")
    json_cli(report, project, ["intake", project / ".px2", "--name", "Fictional representative item family", "--brief", prompt, "--root", project], "Scenario one: initialize truthful PX2 intake without style defaults")
    current = json_cli(report, project, ["decode", project / ".px2/state.px"], "Read intake host adapter before authoring")
    assert current["format"] == 2
    assert not any(r["kind"] in {"C", "X", "D"} for r in current["records"])
    copied_brief = plugin / "resources/examples/intake/brief.txt"
    write(report, project / "examples/intake/brief.txt", copied_brief.read_text(encoding="utf-8"), "Copy bundled syntax brief into project; retain explicit fixture disclaimer")
    example = json_cli(report, project, ["decode", plugin / "resources/examples/intake/project.px"], "Decode declared incomplete sample syntax as source data")
    inventory = json_cli(report, project, ["sources"], "Discover exact installed source revisions for relevant sample research")
    method = json_cli(report, project, ["knowledge", "silhouette-readability"], "Read known method for representative item identity")
    cli(report, project, ["context", plugin / "resources/knowledge/library.px", "k.silhouette-readability", "--root", plugin / "resources"], "Read complete method context including reference-proof limits")
    citations = []
    for citation in method["sources"]:
        identity = next(source for source in inventory["documents"] if source["path"] == citation["path"])
        result = json_cli(report, project, ["source", plugin / "resources" / citation["path"], "--expect", identity["sha256"], "--start", citation["start"], "--end", citation["end"]], "Read exact cited method text with verified source hash")
        citations.append({"citation": citation, "source_identity": identity, "retrieved": result})
    research = {"kind": "research only, no adopted decision or executed asset proof", "method": method,
                "citations": citations,
                "applicability": "Inventory-item identity is relevant. Canvas, native scale, intended backgrounds, and named identity landmarks remain unknown; no source determines whether either competing edge treatment matches this project.",
                "reference_proof_limit": "The bundled key fixture does not inspect or accept this project's absent item.",
                "next_proof": "Once canvas, representative item landmarks and backgrounds are supplied, compare the competing edge treatments on one representative item at native scale and enlarged scale, then retain actual visual results."}
    research_path = project / "sample-research.json"
    write(report, research_path, json.dumps(research, indent=2) + "\n", "Retain exact research identities and project applicability boundary")
    amended = copy.deepcopy(current)
    existing = records(amended)
    for record in example["records"]:
        if record["id"] not in existing:
            amended["records"].append(copy.deepcopy(record))
    mapped = records(amended)
    mapped["project"]["fields"]["in"] = [ref("canvas"), ref("edges")]
    mapped["project"]["fields"]["sc"] = [ref("brief"), ref("scenario.source"), ref("research.source")]
    mapped["project"]["fields"]["br"] = prompt
    mapped["make_sample"]["fields"]["st"] = symbol("blocked")
    for choice in ("canvas", "edges"):
        mapped[choice]["fields"]["so"].append(ref("scenario.source"))
    for id_, path in (("scenario.source", project / "scenario-brief.txt"), ("research.source", research_path)):
        amended["records"].append(row(id_, "S", ur=path.name, dg=sha(path), ln=[1, len(path.read_text(encoding="utf-8").splitlines())], at="2026-09-11", au=symbol("local")))
    amended["records"].append(row("handoff", "N", wh=ref("actor"), fo=[ref("make_sample"), ref("canvas"), ref("edges"), ref("research.source")], nx=[ref("make_sample")], bl=[ref("make_sample")], rv=1))
    amended["revision"] = 1
    publish(report, project, amended, "intake-plan")
    workflow = json_cli(report, project, ["workflow", project / ".px2/state.px", "--root", project], "Cold CLI resume: inspect unknowns, blockers and unperformed criteria")
    context = cli(report, project, ["context", project / ".px2/state.px", "make_sample", "--root", project], "Cold CLI resume: retrieve actual focused PX2 state")
    replies = mcp(report, project, [("pixl_workflow", {"path": ".px2/state.px"}), ("pixl_context", {"path": ".px2/state.px", "focus": "make_sample"})], "Independent cold stdio MCP process: discover tools and retrieve workflow/context")
    assert replies[-2]["result"]["structuredContent"] == workflow
    assert replies[-1]["result"]["structuredContent"]["wire"] == context
    saved = json_cli(report, project, ["decode", project / ".px2/state.px"], "Verify committed exact host state without inferred style or artifacts")
    mapped = records(saved)
    assert mapped["canvas"]["fields"]["vl"] is None
    assert mapped["edges"]["fields"]["st"] == symbol("conflict")
    assert not any(r["kind"] in {"C", "X", "D"} for r in saved["records"])
    assert workflow["ready"] == []
    assert all(q["status"] == "unperformed" for task in workflow["tasks"] for output in task["outputs"] for q in output["requirements"])
    report["scenario_results"]["scenario1"].update({"status": "pass", "project": str(project), "workflow": workflow,
        "plain_response": "The representative-item plan is saved. Canvas size is still unknown, and both edge directions remain in conflict. The next useful input is the canvas plus the representative item's identity landmarks and target backgrounds; then compare both edge treatments on that one item. No asset or style approval is recorded, and engine acceptance remains a future requirement.",
        "criteria": [{"criterion": "Unknown and conflict retained without invented C/X/D", "verdict": "pass"}, {"criterion": "Planned output and acceptance conditions saved before candidate results", "verdict": "pass"}, {"criterion": "Independent cold CLI and MCP workflow/context agree", "verdict": "pass"}],
        "outcome_level": "Recorded behavior plus local state outcome only; no actual art outcome."})
    save(report)
    print(json.dumps({"scenario1": report["scenario_results"]["scenario1"]}, indent=2))


def scenario2(resume=False):
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    project = Path(report["snapshot"]["retained_temporary_root"]) / "scenario2"
    prompt = ("Fictional evaluation request: Resume a representative candidate whose supplied "
              "developer fixture observations say mechanical pass, visual failure because the "
              "identity landmark is not distinguishable, and engine unavailable because no target "
              "project is supplied. Preserve the rejected candidate and observations. Record a "
              "specific revision and later import action; do not turn fixtures into actual art judgment.")
    if not resume:
        report["scenario_results"]["scenario2"] = {"prompt": prompt, "role": "PIXL explicitly adopted for this fictional resume only; fixture preparation remains development work", "status": "in_progress"}
    fixture_code = f'''
import copy,json,sys
from pathlib import Path
sys.path[:0] = {[str(ROOT)] + report['isolation']['dependencies']!r}
from tests.lifecycle_support import sample, add_candidate, add_verdict
from pixl.codec import encode,to_data,Symbol
from hashlib import sha256
root = Path({str(project)!r})
doc = sample(root)
source = root / 'source.txt'
source.write_text({prompt!r} + '\\n', encoding='utf-8')
doc.records['source'].fields['dg'] = sha256(source.read_bytes()).hexdigest()
doc.records['source'].fields['ln'] = [1, 1]
doc.records['q.visual'].fields['ck'] = 'Fixture reviewer records whether the named identity landmark remains distinguishable at native scale.'
doc.records['task'].fields['st'] = Symbol('active')
doc.revision = 1
add_candidate(doc, root, 'candidate.old')
def host(document):
    return {{'format':2,'revision':document.revision,'records':[{{'id':r.id,'kind':r.kind,'fields':to_data(r.fields)}} for r in document.records.values()]}}
(root/'fixture-plan.input.json').write_text(json.dumps(host(doc),indent=2)+'\\n',encoding='utf-8')
reasons = {{'pass':'Supplied mechanical fixture result: the PNG is 2 by 2; actual measurement is recorded separately.',
           'fail':'Supplied visual fixture result: the intended identity landmark is not distinguishable. This is not an actual visual inspection by the evaluating agent.',
           'unavailable':'No destination-engine project or engine execution environment was supplied; import sampling, scale and alpha behavior remain unknown.'}}
for criterion,status,id_ in [('q.mechanical','pass','v.mechanical'),('q.visual','fail','v.visual'),('q.engine','unavailable','v.engine')]:
    add_verdict(doc,root,'candidate.old',criterion,status,id_)
    doc.records[id_].fields['wy']=reasons[status]
    if status!='unavailable':
        receipt=doc.records[id_+'.e']
        path=root/receipt.fields['ur']
        body=json.loads(path.read_text(encoding='utf-8'))
        body['reason']=reasons[status]
        path.write_text(json.dumps(body,sort_keys=True)+'\\n',encoding='utf-8')
        receipt.fields['dg']=sha256(path.read_bytes()).hexdigest()
doc.revision=2
(root/'fixture-observations.input.json').write_text(json.dumps(host(doc),indent=2)+'\\n',encoding='utf-8')
attempt=copy.deepcopy(doc)
attempt.revision=3
attempt.records['task'].fields['st']=Symbol('done')
(root/'fixture-invalid-done.px').write_bytes(encode(attempt))
attempt.records['task'].fields['ph']=Symbol('production')
(root/'fixture-invalid-production-done.px').write_bytes(encode(attempt))
print(json.dumps({{'purpose':'Explicit developer-fixture preparation only; serialized before all copied-runtime operational calls','plan':'fixture-plan.input.json','observations':'fixture-observations.input.json','candidate_sha256':sha256((root/'candidate.old.png').read_bytes()).hexdigest(),'source_import_exception':'tests.lifecycle_support and pixl.codec are used only in this setup subprocess'}}))
'''
    if not resume:
        run(report, [sys.executable, "-I", "-c", fixture_code], ROOT,
            purpose="Prepare explicit authored fixture in an isolated setup subprocess; serialize all state before copied runtime operation")
        report["scenario_results"]["scenario2"]["fixture_source_sha256"] = sha(ROOT / "tests/lifecycle_support.py")
        mcp(report, project, [("pixl_intake", {"store": ".px2", "name": "Fictional failed-candidate resume", "brief": prompt})], "Create scenario-two store with copied stdio MCP intake")
        plan = json.loads(read(report, project / "fixture-plan.input.json", "Read serialized fixture plan as data, without source-runtime imports"))
        publish(report, project, plan, "fixture-plan")
        observations = json.loads(read(report, project / "fixture-observations.input.json", "Read deliberately supplied fixture verdicts after saved plan"))
        publish(report, project, observations, "fixture-observations")
    else:
        failures = report.setdefault("recorder_failures", [])
        if not any(failure["error"].startswith("JSONDecodeError") for failure in failures):
            failures.append({"phase": "scenario2", "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)", "cause": "Recorder tried reading the expected commit rejection from stdout; CLI returned its JSON diagnostic on stderr. The original command, rejection and unchanged store are preserved in operations.", "correction": "Parse stderr when stdout is empty, then resume the already saved fixture without recreating its files or state."})
        failures.append({"phase": "scenario2_resume", "error": "AssertionError: {'error': 'completion', 'detail': 'completion: task: candidate.old requirement q.visual is fail'}", "cause": "Recorder incorrectly expected the diagnostic code task_acceptance. The runtime correctly rejected completion with its implemented completion code.", "correction": "Assert the observed completion code and q.visual fail detail; resume unchanged saved state."})
        save(report)
    workflow = json_cli(report, project, ["workflow", project / ".px2/state.px", "--root", project], "Cold resume begins from persisted failed sample workflow")
    context = cli(report, project, ["context", project / ".px2/state.px", "task", "--root", project], "Retrieve cold sample context with actual retained candidate and verdict bindings")
    decoded = json_cli(report, project, ["decode", project / ".px2/state.px"], "Decode retained sample for evidence-aware resumption")
    mapping = records(decoded)
    for id_ in ("v.mechanical.e", "v.visual.e"):
        evidence = mapping[id_]["fields"]
        assert sha(project / evidence["ur"]) == evidence["dg"]
        read(report, project / evidence["ur"], "Inspect retained caller-supplied observation bytes before deciding the next action")
    measurement = json_cli(report, project, ["asset-check", project / "candidate.old.png", "--width", "2", "--height", "2", "--alpha", "binary"], "Measure actual local fixture PNG separately from supplied acceptance verdicts")
    replies = mcp(report, project, [("pixl_workflow", {"path": ".px2/state.px"}), ("pixl_context", {"path": ".px2/state.px", "focus": "task"})], "Independent copied stdio MCP cold resume retains failed and unavailable outcomes")
    assert replies[-2]["result"]["structuredContent"] == workflow
    assert replies[-1]["result"]["structuredContent"]["wire"] == context
    current_hash = workflow["hash"]
    rejection = json_cli(report, project, ["commit", project / ".px2", project / "fixture-invalid-done.px", "--expect", current_hash, "--root", project], "Negative probe: sample completion must reject the deliberately supplied visual failure", expected=2)
    production_rejection = json_cli(report, project, ["commit", project / ".px2", project / "fixture-invalid-production-done.px", "--expect", current_hash, "--root", project], "Negative probe: production completion cannot adopt a proposed fixture contract without proven decisions", expected=2)
    retained = json_cli(report, project, ["validate", project / ".px2/state.px", "--root", project], "Verify both rejected commits left accepted state unchanged")
    assert retained["hash"] == current_hash
    assert rejection["error"] == "completion" and "q.visual is fail" in rejection["detail"], rejection
    handoff_text = ("Fictional developer-fixture handoff. Preserve candidate.old.png and both supplied observation files. "
                    "The supplied visual failure says the named identity landmark is indistinguishable; this is not this agent's art judgment. "
                    "Next, produce a new candidate under a new path that makes that landmark distinguishable, nominate it, and repeat the saved mechanical and native-scale visual criteria. "
                    "No replacement exists yet. When the destination-engine project is supplied, import that revised candidate and retain actual sampling, scale and alpha observations. "
                    "Until all three requirements pass for the new candidate, leave sample acceptance unfinished.\n")
    handoff_path = project / "revision-handoff.txt"
    write(report, handoff_path, handoff_text, "Retain concrete revision and later import action with fixture limits")
    amended = copy.deepcopy(decoded)
    mapping = records(amended)
    mapping["task"]["fields"]["st"] = symbol("blocked")
    mapping["project"]["fields"]["sc"].append(ref("handoff.source"))
    amended["records"].extend([
        row("handoff.source", "S", ur=handoff_path.name, dg=sha(handoff_path), ln=[1, 1], at="2026-09-11", au=symbol("local")),
        row("revise", "T", nm="Create a distinct revised fixture candidate with the named identity landmark; inspect it, then import when the target project exists", ow=ref("actor"), pr=ref("project"), dp=[], dc=[], kn=[], st=symbol("open"), ph=symbol("sample"), ip=[ref("candidate.old")], op=[ref("revision.output")], ca=[], vr=[]),
        row("revision.output", "F", tk=ref("revise"), nm="Revised representative candidate, retained under a new path", kd=symbol("sprite"), ct=ref("contract"), rq=[ref("q.mechanical"), ref("q.visual"), ref("q.engine")]),
        row("handoff", "N", wh=ref("actor"), fo=[ref("task"), ref("revise"), ref("candidate.old"), ref("v.mechanical"), ref("v.visual"), ref("v.engine"), ref("handoff.source")], nx=[ref("revise")], bl=[ref("task")], rv=3),
    ])
    amended["revision"] = 3
    publish(report, project, amended, "revision-handoff")
    final = json_cli(report, project, ["workflow", project / ".px2/state.px", "--root", project], "Final cold resume shows rejected candidate and concrete next revision task")
    final_context = cli(report, project, ["context", project / ".px2/state.px", "revise", "--root", project], "Final focused revision context includes old observations and handoff source")
    final_mcp = mcp(report, project, [("pixl_workflow", {"path": ".px2/state.px"}), ("pixl_context", {"path": ".px2/state.px", "focus": "revise"})], "Final independent MCP handoff remains resumable")
    assert final_mcp[-2]["result"]["structuredContent"] == final
    assert final_mcp[-1]["result"]["structuredContent"]["wire"] == final_context
    after = json_cli(report, project, ["decode", project / ".px2/state.px"], "Verify historical candidate and observations remain unchanged")
    for id_, old in records(decoded).items():
        if old["kind"] in {"X", "E", "V"}:
            assert records(after)[id_] == old
    assert sha(project / "candidate.old.png") == records(decoded)["candidate.old"]["fields"]["dg"]
    original_task = next(task for task in final["tasks"] if task["id"] == "task")
    assert [criterion["status"] for criterion in original_task["outputs"][0]["requirements"]] == ["pass", "fail", "unavailable"]
    assert final["ready"] == ["revise"]
    report["scenario_results"]["scenario2"].update({"status": "pass", "project": str(project), "initial_workflow": workflow, "final_workflow": final,
        "actual_local_measurement": measurement, "sample_done_rejection": rejection, "production_done_rejection": production_rejection,
        "plain_response": "The retained candidate remains unfinished: its supplied fixture record passes dimensions, fails the identity-landmark review, and has no engine check. I preserved that candidate and its observations, and saved a task to create a distinct revision, recheck its identity at native scale, and test import when the target project is available. These are fixture outcomes, not a claim that I visually reviewed production art.",
        "criteria": [{"criterion": "Supplied mechanical pass, visual failure and unavailable engine remain distinct", "verdict": "pass"}, {"criterion": "Done and production-done commits rejected without publishing", "verdict": "pass"}, {"criterion": "Original candidate/E/V preserved with a concrete revision/import handoff", "verdict": "pass"}, {"criterion": "Cold CLI and MCP agree before and after handoff", "verdict": "pass"}],
        "outcome_level": "Recorded resumption behavior and local mechanical fixture outcome; no real artistic or engine acceptance."})
    save(report)
    print(json.dumps({"scenario2_status": "pass", "sample_rejection": rejection, "production_rejection": production_rejection, "final_workflow": final}, indent=2))


def finish():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    plugin = Path(report["snapshot"]["root"])
    original_files = report["snapshot"]["files"]
    changed = [entry["path"] for entry in original_files if sha(plugin / entry["path"]) != entry["sha256"]]
    assert changed == [], changed
    assert all(result["status"] == "pass" for result in report["scenario_results"].values())
    report["snapshot"]["final_original_file_hashes_unchanged"] = True
    critical = ["bundle-manifest.json", "skills/pixl/SKILL.md", "skills/pixl/references/intake-sample.md",
                "resources/agent/PROFILE.md", "resources/spec/PIXL-2.md", "runtime/pixl/registry-v2.json",
                "runtime/pixl/store.py", "runtime/pixl/lifecycle.py", "runtime/pixl/cli.py", "runtime/pixl/mcp.py"]
    report["snapshot"]["critical_identities"] = {path: sha(plugin / path) for path in critical}
    report["snapshot"]["retention"] = "Both complete copied bundles are retained at their named temporary paths; full file identities and manifests are embedded. Current scenario project files are embedded below, including fixture PNG bytes. No copy was overwritten after evaluation. Python-created __pycache__ files are generated caches, outside the inventoried copied source snapshot."
    report["retained_project_files"] = []
    for scenario, result in report["scenario_results"].items():
        project = Path(result["project"])
        for path in sorted(project.rglob("*")):
            if not path.is_file():
                continue
            payload = {"scenario": scenario, "path": str(path.relative_to(project)).replace("\\", "/"), "sha256": sha(path), "bytes": path.stat().st_size}
            if path.suffix == ".png":
                payload["base64"] = base64.b64encode(path.read_bytes()).decode("ascii")
                payload["kind"] = "synthetic mechanical fixture; not generated production art"
            else:
                payload["text"] = path.read_bytes().decode("utf-8")
            report["retained_project_files"].append(payload)
    failures = report.setdefault("recorder_failures", [])
    if not any(failure["phase"] == "fresh_snapshot" for failure in failures):
        failures.insert(0, {
            "phase": "fresh_snapshot", "command": [".venv/Scripts/python.exe", "evidence/intake-sample/helper.py", "fresh_snapshot"],
            "error": "SyntaxError: closing parenthesis '}' does not match opening parenthesis '['",
            "cause": "A bracket was omitted while authoring the recorder's fresh snapshot dictionary; Python rejected the helper before execution.",
            "correction": "Close the list comprehension and rerun the helper. This failed invocation performed no runtime or scenario work."})
    report["verification_levels"] = {
        "discovery_and_format": "Exercised: copied skill/resource/runtime identities; installed method/source discovery; public CLI and actual stdio MCP initialize/tools/list; PX2 encode/decode/rooted validation and commits.",
        "recorded_scenario_behavior": "Exercised once by one developer-agent with explicit fictional profile activation: unresolved intake, contextual research, retained acceptance failures, cold resumption and concrete handoff. Procedures were scripted and inspected; this is not a blind or controlled agent benchmark.",
        "actual_task_outcomes": "Local production-state persistence and actual 2x2 PNG measurement exercised. Real artistic creation, actual visual judgment, provider execution and destination-engine acceptance were not exercised."}
    report["judgment"] = {
        "result": "Both bounded scenarios passed against the coherent fresh copied snapshot.",
        "skill_blockers": [],
        "observations": [
            "The skill gave a usable route for retaining unknown dimensions and conflicting edge directions without selecting fixture defaults or inventing X/C/D.",
            "Acceptance conditions survived publication and independent CLI/MCP cold starts. Supplied visual failure and unavailable engine remained separate from the actual local dimensions measurement.",
            "The unchanged prior candidate and observations remained reachable from the new revision task's focused context through the retained handoff.",
            "The workflow task blockers list describes activation prerequisites: the blocked rejected task has blockers=[] while its output requirements explicitly contain fail/unavailable. Consumers must inspect per-output requirements as the skill directs; an empty blockers list is not acceptance.",
            "The silhouette method's retrieved source passages are contextual notes on identity, semantic changes and UI clarity. They do not settle the fictional edge-treatment conflict or justify adopting the bundled key fixture as this project's style."
        ],
        "failed_attempts": "The first bundle failed manifest preflight during concurrent parent instruction edits and is preserved separately. Recorder syntax/output-parsing/diagnostic-code mistakes are preserved separately from the correct runtime rejection and final scenario verification.",
        "claim_limit": "No controlled improvement, general instruction-following reliability, artistic expertise, successful real PixelLab operation, or finished asset family is established."}
    report["helper_sha256"] = sha(Path(__file__))
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    report["status"] = "complete_bounded_exercise"
    save(report)
    print(json.dumps({"status": report["status"], "scenario_statuses": {name: value["status"] for name, value in report["scenario_results"].items()}, "operations": len(report["operations"]), "project_files": len(report["retained_project_files"]), "manifest_sha256": report["snapshot"]["manifest_sha256"], "skill_sha256": report["snapshot"]["critical_identities"]["skills/pixl/references/intake-sample.md"], "report_sha256": sha(REPORT)}, indent=2))


if __name__ == "__main__":
    if sys.argv[1] == "setup":
        setup()
    elif sys.argv[1] == "resume_setup":
        resume_setup()
    elif sys.argv[1] == "fresh_snapshot":
        fresh_snapshot()
    elif sys.argv[1] == "scenario1":
        scenario1()
    elif sys.argv[1] == "scenario2":
        scenario2()
    elif sys.argv[1] == "scenario2_resume":
        scenario2(resume=True)
    elif sys.argv[1] == "finish":
        finish()
    else:
        raise SystemExit("Unknown recorder phase")
