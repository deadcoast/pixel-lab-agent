"""Read-only TM-05 evidence audit; only fresh files sharing this script's stem are written.

This verifies retained execution receipts, current fixture bytes and source bindings.
It does not rerun installation, native hosts, the product suite, or acceptance.
"""

from __future__ import annotations

import ast
import hashlib
import io
import json
import subprocess
import sys
import traceback
import zipfile
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath, PureWindowsPath

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
STEM = Path(__file__).stem
BASELINE = "c4b8131d07930e1f5e0b2f821318354796e69e7c"
HARNESS = "7c517c867e877bf469cd299638dbe4259d7c741d0380446ceb284c62a1788f50"
GRADER = "5fb9713fa7ee7e03b0a5a301f7a84253ad83efd7d15e655e8fcfedf523fdc5e4"
OLD_HARNESS = "6d0a0af08a64bbd9f82ec08189fe4c328e2bede3fe590e6f9011c98fc7fa76f7"
REMOTE_ROOT = "/tmp/pixl-tm05-final-20261114-01"
ROWS = []
VERIFIED_REFS = {}
REMOTE = {"files": {}, "trees": {}}
SOURCE_BYTES = Path(__file__).read_bytes()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def need(condition, detail):
    if not condition:
        raise AssertionError(detail)


def meta(data):
    return {"sha256": digest(data), "bytes": len(data)}


def read(path):
    return json.loads(Path(path).read_bytes())


def local(path):
    value = Path(path)
    return value if value.is_absolute() else ROOT / value


def join(path, *parts):
    cls = PurePosixPath if str(path).startswith("/") else PureWindowsPath
    return str(cls(path).joinpath(*parts))


def parent(path):
    cls = PurePosixPath if str(path).startswith("/") else PureWindowsPath
    return str(cls(path).parent)


def name(path):
    cls = PurePosixPath if str(path).startswith("/") else PureWindowsPath
    return cls(path).name


def inventory(folder):
    root = Path(folder).resolve()
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            need(not path.is_symlink() and path.resolve().is_relative_to(root), f"Escaping inventory file: {path}")
            result[path.relative_to(root).as_posix()] = meta(path.read_bytes())
    return result


def live_tree(path):
    return REMOTE["trees"][str(path)] if str(path).startswith("/") else inventory(local(path))


def live_meta(path):
    return REMOTE["files"][str(path)] if str(path).startswith("/") else meta(local(path).read_bytes())


def ref(item, *, actual=None):
    path = actual or item["path"]
    observed = live_meta(path)
    need(observed["sha256"] == item["sha256"], f"Reference SHA mismatch: {path}")
    if "bytes" in item:
        need(observed["bytes"] == item["bytes"], f"Reference size mismatch: {path}")
    VERIFIED_REFS[str(path)] = observed
    return observed


def tree_refs(value):
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and isinstance(value.get("sha256"), str):
            ref(value)
        for entry in value.values():
            tree_refs(entry)
    elif isinstance(value, list):
        for entry in value:
            tree_refs(entry)


def check(label, function):
    try:
        detail = function()
        ROWS.append({"check": label, "pass": True, "detail": detail})
    except Exception as error:
        ROWS.append({"check": label, "pass": False, "error": f"{type(error).__name__}: {error}",
                     "traceback": traceback.format_exc()})


def fresh_write(path, value):
    target = Path(path).resolve()
    need(target.parent == BASE and target.name.startswith(STEM), "Audit write escaped assigned prefix")
    with target.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def command_output(row, attempt):
    # Linux absolute locators are checked in Ubuntu; returned copies supply JSON.
    path = row["stdout"]["path"]
    return read(attempt / name(path))


def commands_check(result, attempt):
    rows = result["commands"]
    need(len(rows) == result.get("command_count", len(rows)), "Command count differs")
    seen = set()
    for row in rows:
        need(row["returncode"] == row["expected_returncode"], f"Unexpected exit: {row['label']}")
        need(row["elapsed_seconds"] >= 0 and row["started_at"] <= row["finished_at"], "Invalid process timing")
        for stream in ("stdout", "stderr"):
            ref(row[stream])
            copied = attempt / name(row[stream]["path"])
            need(meta(copied.read_bytes())["sha256"] == row[stream]["sha256"], "Copied process stream differs")
        receipt = attempt / (name(row["stdout"]["path"]).removesuffix(".stdout.txt") + ".json")
        need(read(receipt) == row, f"Command receipt differs: {receipt}")
        need(str(receipt) not in seen, "Duplicate process receipt")
        seen.add(str(receipt))
    return len(rows)


def collect_remote(local_index):
    row = next(x for x in local_index["qualified_cells"] if x["platform"]["system"] == "Linux")
    result = read(local(row["result"]["path"]))
    work = result["commands"][0]["cwd"]
    staging = BASE / "local-01/wsl-native-staging-01"
    inputs = read(staging / "input-manifest.json")
    files = {join(REMOTE_ROOT, item) for item in inputs}
    files.add(join(REMOTE_ROOT, "input-manifest.json"))
    for item in result["commands"]:
        files.update(item[key]["path"] for key in ("stdout", "stderr"))
    files.add(join(REMOTE_ROOT, "evidence/install-support/20261114/local-01/wsl-py312-02/RESULT.json"))
    for route in ("copied_kit", "wheel"):
        data = result["routes"][route]
        consumer = join(work, "relocated project with spaces" if route == "copied_kit" else "relocated wheel consumer")
        files.add(join(consumer, ".pixl/assets/queue.working/state.px"))
        runtime = join(work, "relocated kit with spaces/runtime/pixl") if route == "copied_kit" else data["readiness"]["installation"]["root"]
        files.update(join(runtime, item) for item in result["expected_runtime_payload"])
        if route == "wheel":
            files.add(data["console"]["path"])
    trees = [join(work, item) for item in ("relocated project with spaces", "relocated wheel consumer", "relocated kit with spaces", "retained consumer", "retired original kit")]
    update = result["routes"]["retained_kit_update"]
    files.update(update[key]["path"] for key in ("old_manifest", "new_manifest"))
    files.add(join(work, "retained consumer", update["state"]["path"]))
    files.add(join(work, "retained consumer", update["comparison_coverage"]["path"]))
    request = {"files": sorted(files), "trees": trees}
    program = '''import hashlib,json,sys
from pathlib import Path
def meta(p):
 b=p.read_bytes();return {"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)}
request=json.load(sys.stdin);out={"files":{},"trees":{}}
for name in request["files"]:
 p=Path(name);assert p.is_absolute() and p.is_file(),name;out["files"][name]=meta(p)
for name in request["trees"]:
 root=Path(name).resolve();assert root.is_dir(),name;rows={}
 for p in sorted(root.rglob("*")):
  if p.is_file():
   assert not p.is_symlink() and p.resolve().is_relative_to(root),str(p)
   rows[p.relative_to(root).as_posix()]=meta(p)
 out["trees"][name]=rows
print(json.dumps(out))
'''
    process = subprocess.run(["wsl", "--distribution", "Ubuntu", "--exec", "python3", "-B", "-c", program],
                             input=json.dumps(request).encode(), capture_output=True, timeout=60, check=False)
    need(process.returncode == 0, "WSL read-only evidence inventory failed: " + process.stderr.decode(errors="replace"))
    REMOTE.update(json.loads(process.stdout))
    return {"distribution": "Ubuntu", "fixture_root": REMOTE_ROOT, "read_only_files": len(files), "read_only_trees": len(trees),
            "command": ["wsl", "--distribution", "Ubuntu", "--exec", "python3", "-B", "-c", "embedded read-only inventory"],
            "returned_inventory_sha256": digest(process.stdout)}


def test_and_source_bindings(local_index, native_index):
    tree_refs(local_index)
    tree_refs(native_index)
    lint = read(local(local_index["harness_checks"]["path"]))
    need(lint["status"] == "pass" and lint["tests_run"] == 12, "Final harness checks differ")
    need(all(x["exit_code"] == 0 for x in lint["commands"]), "Harness test or lint command failed")
    for path, sha in lint["source_sha256"].items():
        ref({"path": path, "sha256": sha})
        snapshot = BASE / "local-01/lint-02/sources" / (path.replace("/", "__") + ".txt")
        ref({"path": str(snapshot), "sha256": sha})
    need("Ran 12 tests" in (BASE / "local-01/lint-02/1-stderr.txt").read_text(), "Missing 12-test output")
    need((BASE / "local-01/lint-02/1-stderr.txt").read_text().rstrip().endswith("OK"), "Harness tests did not end OK")
    need("All checks passed!" in (BASE / "local-01/lint-02/0-stdout.txt").read_text(), "Missing passing Ruff output")
    correction = read(BASE / "grader-checks-01/wrapper-correction-result.json")
    tree_refs(correction["final_sources"])
    tree_refs(correction["validation"]["tests"])
    tree_refs(correction["validation"]["ruff"])
    need(correction["validation"]["tests"]["passed"] == 27, "Final grader test count differs")
    log = local(correction["validation"]["tests"]["log"]["path"]).read_text()
    need("Ran 27 tests" in log and log.rstrip().endswith("OK"), "Missing final 27-test success")
    need(digest((ROOT / "evaluations/grade_readiness.py").read_bytes()) == GRADER, "Grader source drifted")
    return {"harness_tests": 12, "grader_tests": 27, "harness_sha256": HARNESS, "grader_sha256": GRADER,
            "scope": "Existing final focused test logs and exact sources verified; tests were not rerun by this audit."}


def harness_delta():
    before = (BASE / "local-01/windows-py314-05/harness.py.txt").read_bytes()
    after = (ROOT / "evaluations/install_support_check.py").read_bytes()
    need(digest(before) == OLD_HARNESS and digest(after) == HARNESS, "Harness reviewed source drift")
    class StripLogging(ast.NodeTransformer):
        def visit_Import(self, node):
            return None if len(node.names) == 1 and node.names[0].name == "logging" else node
        def visit_Assign(self, node):
            return None if any(isinstance(x, ast.Name) and x.id == "logger" for x in node.targets) else node
        def visit_Expr(self, node):
            value = node.value
            if isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute) and isinstance(value.func.value, ast.Name) and value.func.value.id == "logger" and value.func.attr == "exception":
                return None
            return self.generic_visit(node)
    def normalized(data):
        module = StripLogging().visit(ast.parse(data))
        for node in ast.walk(module):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                node.names.sort(key=lambda x: (x.name, x.asname or ""))
        result, block = [], []
        for node in module.body + [None]:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                block.append(node)
            else:
                result.extend(sorted(block, key=ast.dump)); block = []
                if node is not None:
                    result.append(node)
        module.body = result
        return ast.dump(module, include_attributes=False)
    need(normalized(before) == normalized(after), "Harness delta exceeds import order and diagnostic logging")
    need(after.count(b"logger.exception(") == 2, "Unexpected logging boundaries")
    return {"review": "03", "before_sha256": OLD_HARNESS, "final_sha256": HARNESS,
            "earlier_reviewed_at": "2026-11-14 09:49:04 UTC", "delta": "Import ordering/formatting, logging import/module logger, two existing exception-boundary diagnostics only.",
            "normalized_ast_equal_after_removing_logging": True}


def distribution_check(index):
    result = read(local(index["distribution"]["path"]))
    need(result["status"] == "pass" and result["source_inputs_unchanged"], "Distribution failed")
    ref(result["wheel"])
    need(result["wheel"]["sha256"] == index["tested_wheel"]["sha256"], "Wrong distribution wheel")
    for artifact in result["artifacts"]:
        ref(artifact)
    inputs = read(BASE / "distribution-02/source-inputs.json")
    with zipfile.ZipFile(BASE / "distribution-02/source-inputs.zip") as archive:
        need(set(archive.namelist()) == set(inputs), "Distribution archive path set differs")
        need({k: meta(archive.read(k)) for k in inputs} == inputs, "Distribution frozen ZIP bytes differ")
    need({k: meta((Path(result['frozen_source']) / k).read_bytes()) for k in inputs} == inputs, "Distribution source changed")
    with zipfile.ZipFile(local(index["tested_wheel"]["path"])) as archive:
        expected = {p.name: p.read_bytes() for p in (ROOT / "pixl").iterdir() if p.suffix in (".py", ".json")}
        need(len(expected) == 47, "Unexpected runtime payload count")
        for name_, data in expected.items():
            need(archive.read("pixl/" + name_) == data and archive.read("pixl/resources/pixl/" + name_) == data,
                 "Wheel runtime differs: " + name_)
    commands_check(result, BASE / "distribution-02")
    return {"source_files": len(inputs), "wheel_sha256": result["wheel"]["sha256"], "runtime_payload_files": 47,
            "historical_build_harness_sha256": result["script"]["sha256"],
            "scope": "The build receipt used its earlier recorded harness revision; final installation cells separately bind the final harness and this exact wheel."}


def staging_check(index):
    base = BASE / "local-01/wsl-native-staging-01"
    start, finish, transfer = (read(base / n) for n in ("INPUTS.json", "RESULT.json", "RETURNED.json"))
    inputs, returned = (read(base / n) for n in ("input-manifest.json", "returned-evidence-manifest.json"))
    ref(start["archive"])
    need(digest((base / "input-manifest.json").read_bytes()) == start["input_manifest_sha256"], "Staging manifest drift")
    need(start["harness_sha256"] == HARNESS and start["input_count"] == len(inputs) == 3456, "Staging identity differs")
    need(finish["status"] == transfer["status"] == "pass" and finish["original_inputs_unchanged"] and transfer["all_receipt_bytes_verified"], "Staging failed")
    need(finish["fixture_root"] == REMOTE_ROOT and "/tmp/" in finish["argv"][2], "Wrong Linux-native execution location")
    with zipfile.ZipFile(base / "fixture-inputs.zip") as archive:
        need(set(archive.namelist()) == set(inputs) | {"input-manifest.json"}, "WSL staged archive paths differ")
        need(digest(archive.read("input-manifest.json")) == start["input_manifest_sha256"], "Embedded WSL input manifest differs")
        need({k: meta(archive.read(k)) for k in inputs} == inputs, "WSL staged archive bytes differ")
    need({k: REMOTE["files"][join(REMOTE_ROOT, k)] for k in inputs} == inputs, "Live WSL original inputs changed")
    need(REMOTE["files"][join(REMOTE_ROOT, "input-manifest.json")]["sha256"] == start["input_manifest_sha256"], "Live WSL embedded manifest changed")
    zip_meta = meta((base / "returned-evidence.zip").read_bytes())
    need(zip_meta["sha256"] == finish["returned_archive"]["sha256"] == transfer["returned_archive_sha256"], "Returned archive mismatch")
    with zipfile.ZipFile(base / "returned-evidence.zip") as archive:
        need(set(archive.namelist()) == set(returned), "Returned archive paths differ")
        need({k: meta(archive.read(k)) for k in returned} == returned, "Returned archive bytes differ")
    need(inventory(BASE / "local-01/wsl-py312-02") == returned and len(returned) == transfer["file_count"] == 195, "Returned receipts changed")
    return {"staged_inputs": len(inputs), "returned_receipts": len(returned), "fixture_root": REMOTE_ROOT,
            "path_handling": "POSIX locators hashed through Ubuntu WSL; unchanged returned copies separately verified on Windows."}


def local_cell(row):
    attempt = local(row["result"]["path"]).parent
    result = read(attempt / "RESULT.json")
    need(result["status"] == "pass" and result["input_kit_unchanged"], "Cell not passing")
    need(result["script"]["sha256"] == HARNESS == digest((attempt / "harness.py.txt").read_bytes()), "Cell harness differs")
    need(result["wheel"]["sha256"] == LOCAL_INDEX["tested_wheel"]["sha256"], "Cell wheel differs")
    work = result["commands"][0]["cwd"]
    payload = {p.name: digest(p.read_bytes()) for p in (ROOT / "plugins/pixl/runtime/pixl").iterdir() if p.suffix in (".py", ".json")}
    need(len(payload) == row["runtime_payload_files_verified"] == 47 and result["expected_runtime_payload"] == payload, "Frozen runtime payload differs")
    count = commands_check(result, attempt)
    need(count == row["command_count"], "Index process count differs")
    bare = result["bare_bootstrap"]
    need(bare["status"] == "pass" and bare["report"]["dependencies"]["status"] == "incomplete" and bare["packages"]["pixl_origin"] is None, "Bare setup was not incomplete")
    cold_summary = {}
    for route_name, prefix in (("copied_kit", "kit"), ("wheel", "wheel")):
        route = result["routes"][route_name]
        need(route["status"] == route["probe"]["status"] == "pass", "Useful installed route failed")
        need(route["runtime_payload"] == payload and route["runtime_payload_matches_frozen_kit"], "Installed payload differs")
        need(route["identity"] == route["cold_identity"] and bool(route["identity"]["pending_jobs"]), "Cold saved identity differs")
        cold = [c for c in result["commands"] if c["label"] == "cold-" + prefix + "-read"]
        need(len(cold) == 2, "Cold route must have separate PLAR and jobs process receipts")
        selected, jobs = [command_output(c, attempt) for c in cold]
        root = cold[0]["argv"][cold[0]["argv"].index("--root") + 1]
        state = join(root, selected["asset"]["production"]["store"], "state.px")
        identity = {"requirements_hash": selected["requirements_hash"], "state_sha256": live_meta(state)["sha256"],
                    "pending_jobs": selected["production"]["pending_jobs"], "continuation": selected["production"]["continuation"],
                    "job_states": {x["id"]: x["state"] for x in jobs["jobs"]}}
        need(identity == route["identity"] and selected["production"]["selection_current"], "Raw cold process outputs differ from saved identity")
        need(identity["job_states"]["first_request"] == "failed" and all(identity["job_states"][j] == "prepared" for j in identity["pending_jobs"]), "Failure or prepared successor lost")
        current_files = live_tree(root)
        need(len(current_files) == route["consumer_files_preserved"] == row["cold_project_files_preserved"][route_name] == 56, "Cold consumer count differs")
        need(current_files["BRIEF.md"]["sha256"] == route["consumer_source_sha256"], "Cold source bytes differ")
        runtime = join(work, "relocated kit with spaces/runtime/pixl") if route_name == "copied_kit" else route["readiness"]["installation"]["root"]
        need({n: live_meta(join(runtime, n))["sha256"] for n in payload} == payload, "Live installed runtime differs")
        for n, item in route["executed_runtime"].items():
            ref(item, actual=join(runtime, n))
        operations = [c for c in result["commands"] if c["label"] == prefix + "-operation"]
        sources = next(command_output(c, attempt) for c in operations if c["argv"][-1] == "sources")
        resource_root = join(route["readiness"]["installation"]["root"], "resources")
        need(sources["root"] == resource_root and sources["files_verified"] is True, "Installed library fell back to another root")
        initial_reads = [c for c in operations if "--asset" in c["argv"] and c["argv"][-1] == "queue.working"]
        need(initial_reads and max(x["finished_at"] for x in initial_reads) <= cold[0]["started_at"], "Cold processes predate production setup")
        if route_name == "copied_kit":
            need(route["packages"]["pixl_origin"] is None and route["kit_files_unchanged"], "Copied route imported installed PIXL")
            need(route["readiness"]["reporter"]["python_executable"] == cold[0]["argv"][0], "Copied route moved virtual environment")
            if result["platform"]["system"] == "Linux":
                staged = read(BASE / "local-01/wsl-native-staging-01/input-manifest.json")
                expected_kit = {k[len("plugins/pixl/"):]: v for k, v in staged.items() if k.startswith("plugins/pixl/")}
            else:
                expected_kit = inventory(ROOT / "plugins/pixl")
            need(live_tree(join(work, "relocated kit with spaces")) == expected_kit, "Relocated copied kit files differ from supplied kit")
        else:
            ref(route["console"])
            need(cold[0]["argv"][0] == route["console"]["path"], "Wheel cold route bypassed installed console")
            need(parent(route["packages"]["pixl_origin"]) == runtime and parent(runtime) == route["packages"]["site"], "Wheel imports escaped environment")
        cold_summary[route_name] = {"files": len(current_files), "pending_jobs": identity["pending_jobs"], "state_sha256": identity["state_sha256"], "raw_process_identity_equal": True}
    before, after = (read(attempt / x) for x in ("retained-before.json", "retained-after.json"))
    prefix = ".agents/skills/pixl-kit/"
    nonkit_before = {k: v for k, v in before.items() if not k.startswith(prefix)}
    nonkit_after = {k: v for k, v in after.items() if not k.startswith(prefix)}
    update = result["routes"]["retained_kit_update"]
    need(nonkit_before == nonkit_after and len(nonkit_before) == update["nonkit_files_preserved"] == 3032, "Retained non-kit set or bytes changed")
    need(live_tree(join(work, "retained consumer")) == after, "Live retained consumer differs from after inventory")
    oldkit = {k[len(prefix):]: v for k, v in before.items() if k.startswith(prefix)}
    need(live_tree(join(work, "retired original kit")) == oldkit and update["old_kit_preserved"], "Old kit was not retained exactly")
    ref(update["old_manifest"]); ref(update["new_manifest"])
    need(update["old_manifest"]["sha256"] != update["new_manifest"]["sha256"] == LOCAL_INDEX["kit_manifest"]["sha256"], "Replacement identity not distinct/current")
    need(update["old_installation"] == update["same_path_replacement"] == parent(update["new_manifest"]["path"]), "Replacement was not at the same path")
    old, new = [command_output(next(c for c in result["commands"] if c["label"] == label), attempt) for label in ("retained-old-kit-review", "retained-new-kit-review")]
    labels = new.pop("hash_domains", None)
    need(labels and old == new, "Retained request-review semantics changed")
    coverage = new["comparison_coverage"]
    need(coverage == update["comparison_coverage"] and coverage["expected"] == coverage["observed"] == 23 and coverage["complete"] and coverage["scope_current"] and coverage["semantic_verdict"] == "not_assessed", "Saved comparison coverage changed or overclaimed")
    need(update["state"]["revision"] == 126, "Retained state revision differs")
    for key in ("state", "comparison_coverage"):
        ref(update[key], actual=join(work, "retained consumer", update[key]["path"]))
    if "locked_source" in result["routes"]:
        route = result["routes"]["locked_source"]
        inputs = read(attempt / "locked-source-inputs.json")
        need({k: meta((Path(work) / "locked source" / k).read_bytes()) for k in inputs} == inputs and route["frozen_inputs_unchanged"], "Locked source inputs changed")
        need(route["runtime_payload"] == payload and route["status"] == "pass", "Locked source payload or result differs")
    return {"name": row["name"], "commands": count, "runtime_files": len(payload), "cold_routes": cold_summary,
            "nonkit_files_preserved": len(nonkit_before), "retired_kit_files": len(oldkit), "comparison_rows": 23,
            "consumer_preservation_basis": "Raw saved before/after inventories for retained kit update. Cold route full-tree equality was enforced by the frozen harness; this audit independently checks the current 56-file count, source bytes, state and raw cold identity. No separate pre-move 56-file inventory was persisted."}


def native_check(index):
    sys.path.insert(0, str(ROOT))
    from evaluations.grade_readiness import grade
    results = []
    for case in index["cases"]:
        attempt = local(case["record"]["path"]).parent
        identity = read(local(case["identity"]["path"]))
        consumer = Path(identity["consumer"])
        all_files = inventory(consumer)
        cache_files = {k: v for k, v in all_files.items() if "__pycache__" in PurePosixPath(k).parts}
        need(all(k.startswith("installed pixl/runtime/pixl/__pycache__/") and k.endswith(".pyc") for k in cache_files), "Unexpected cache location or type")
        current = {k: v for k, v in all_files.items() if k not in cache_files}
        need(all(current[k]["sha256"] == h for k, h in identity["inputs"].items()), "Native original inputs changed")
        need(len(identity["inputs"]) == case["original_inputs_unchanged"], "Native original count differs")
        need(len(identity["package_files"]) == case["portable_kit_files"] == 251, "Native payload count differs")
        for key, sha in identity["package_files"].items():
            need(current["installed pixl/" + key]["sha256"] == sha, "Native installed kit changed")
        retained = read(local(case["final_grade"]["path"]))
        replay = grade(attempt)
        need(replay == retained, "Read-only native grade replay differs")
        expected = 19 if case["host"] == "codex" else 18
        need(replay["status"] == "pass" and replay["passed"] == replay["total"] == expected and replay["observed_named_role_loaded"], "Native loading grade not passing")
        preservation = read(local(case["preservation"]["path"]))
        need(not preservation["changed"] and len(preservation["new"]) == case["allowed_new_outputs"], "Native preservation report differs")
        need({k: v["sha256"] for k, v in current.items() if k not in identity["inputs"]} == preservation["new"], "Native actual additions differ")
        results.append({"host": case["host"], "passed": expected, "total": expected, "original_inputs": len(identity["inputs"]), "exact_grade_replayed": True, "excluded_runtime_cache_files": cache_files, "cache_scope": "Recorded separately, matching the original readiness recorder/grader cache exclusion; not part of the 251 shipped files or allowed output count."})
    return {"cases": results, "grader_sha256": GRADER, "scope": "Read-only replay against preserved original native traces and current consumer files; no new native invocation."}


def baseline_check():
    listing = subprocess.run(["git", "ls-tree", "-r", "-z", BASELINE, "--", "pixl", "scripts", "plugins/pixl"], cwd=ROOT, capture_output=True, check=True).stdout
    records = []
    for record in listing.split(b"\0"):
        if record:
            header, path = record.split(b"\t", 1)
            records.append((header.split()[2].decode(), path.decode()))
    payload = "".join(sha + "\n" for sha, _ in records).encode()
    process = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT, input=payload, capture_output=True, check=True)
    stream = io.BytesIO(process.stdout)
    changed, checked = [], {}
    for expected, path in records:
        sha, kind, length = stream.readline().split()
        need(sha.decode() == expected and kind == b"blob", "Git object batch identity differs")
        data = stream.read(int(length)); need(stream.read(1) == b"\n", "Git object framing differs")
        current = (ROOT / path).read_bytes()
        if current != data:
            changed.append(path)
        checked[path] = meta(current)
    need(not changed, "Raw product bytes differ from baseline: " + repr(changed))
    untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "--", "pixl", "scripts", "plugins/pixl"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    need(not untracked, "Untracked product sources: " + repr(untracked))
    baseline = read(BASE / "artifact-baseline.json")
    ref(baseline["retained_full_verification"])
    prior = read(local(baseline["retained_full_verification"]["path"]))
    need(prior["status"] == "pass" and prior["tests"]["passed"] == 1313 and len(prior["tests"]["skipped"]) == 2, "Prior full suite identity/count differs")
    need(prior["bundle_manifest_sha256"] == LOCAL_INDEX["kit_manifest"]["sha256"], "Prior verified kit differs")
    return {"baseline": BASELINE, "raw_blob_equal_files": len(records), "product_inventory_sha256": digest(json.dumps(checked, sort_keys=True).encode()),
            "retained_sc06_full_result": baseline["retained_full_verification"], "prior_passed": 1313, "prior_skipped": 2,
            "fresh_full_suite_run": False, "scope": "All tracked pixl/, scripts/ and plugins/pixl/ bytes compared directly to baseline Git blobs. Prior SC06 result is historical evidence, not a new full-suite run."}


def failures_preserved():
    history = read(BASE / "local-01/development-history.json")
    failures = []
    for item in history["failures"]:
        path = (BASE / "local-01" / item["path"]).resolve()
        value = read(path); need(value["status"] == "fail", "Development failure was lost")
        failures.append({"path": str(path.relative_to(ROOT)), **meta(path.read_bytes())})
    need(read(BASE / "local-01/lint-01/RESULT.json")["exit_code"] == 1, "Original lint failure was lost")
    for host in ("codex", "claude"):
        path = BASE / "native" / (host + "-clean-01") / "independent-grade-01.json"
        need(read(path)["status"] == "fail", "Original native grading failure was lost")
        failures.append({"path": str(path.relative_to(ROOT)), **meta(path.read_bytes())})
    trace = NATIVE_INDEX["preserved_native_failure"]
    data = local(trace["trace"]["path"]).read_text().splitlines()
    need(trace["failure"]["call_id"] in data[trace["failure"]["result_line"] - 1], "Native failure pair missing")
    need(trace["self_correction"]["call_id"] in data[trace["self_correction"]["result_line"] - 1], "Native self-correction pair missing")
    return {"failed_development_and_native_grades": failures, "lint_failure_preserved": True, "native_self_corrected_failure_preserved": True,
            "prior_harness_review_mismatch_receipt": meta((BASE / "harness-review-01.json").read_bytes())}


if __name__ == "__main__":
    output = BASE / (STEM + ".json")
    need(not output.exists(), "Preserve existing audit; choose a fresh script/receipt name")
    freeze = BASE / (STEM + "-freeze.json")
    freeze_value = read(freeze)
    need(freeze_value["sha256"] == digest(SOURCE_BYTES), "Audit source was not frozen at this exact hash")
    LOCAL_INDEX = read(BASE / "local-01/FINAL.json")
    NATIVE_INDEX = read(BASE / "native/RESULT.json")
    initial_evidence = inventory(BASE)
    check("linux_native_live_inventory", lambda: collect_remote(LOCAL_INDEX))
    check("final_reference_test_and_source_bindings", lambda: test_and_source_bindings(LOCAL_INDEX, NATIVE_INDEX))
    check("harness_review03_final_lint_delta", harness_delta)
    check("distribution02_exact_inputs_and_wheel", lambda: distribution_check(LOCAL_INDEX))
    check("wsl_staging_and_byte_exact_return", lambda: staging_check(LOCAL_INDEX))
    need(len(LOCAL_INDEX["qualified_cells"]) == 5, "Expected exactly five final cells")
    for cell in LOCAL_INDEX["qualified_cells"]:
        check("local_cell_" + cell["name"], lambda item=cell: local_cell(item))
    check("native_original_traces_current_grader_replay", lambda: native_check(NATIVE_INDEX))
    check("unchanged_product_and_historical_sc06_verification", baseline_check)
    check("prior_failures_preserved", failures_preserved)
    check("final_process_total", lambda: (need(sum(x["command_count"] for x in LOCAL_INDEX["qualified_cells"]) == 341, "Expected 341 final local commands") or {"commands": 341}))
    check("read_only_audit_preserved_prior_evidence", lambda: (need(all(meta((BASE / k).read_bytes()) == v for k, v in initial_evidence.items()), "Prior evidence changed during audit") or {"files": len(initial_evidence), "independent_additions_allowed": True}))
    need(Path(__file__).read_bytes() == SOURCE_BYTES, "Audit source changed during execution")
    result = {"version": 1, "observed_at": datetime.now(UTC).isoformat(), "status": "pass" if all(x["pass"] for x in ROWS) else "fail",
              "audit_source": {"path": str(Path(__file__).relative_to(ROOT)), **meta(SOURCE_BYTES)},
              "frozen_before_execution": freeze_value, "passed": sum(x["pass"] for x in ROWS), "total": len(ROWS),
              "checks": ROWS, "verified_file_references": len(VERIFIED_REFS),
              "source_indices": [{"path": str(p.relative_to(ROOT)), **meta(p.read_bytes())} for p in (BASE / "local-01/FINAL.json", BASE / "native/RESULT.json")],
              "scope": "Independent assistant evidence audit. Read-only source, receipt, archive and live fixture verification; current grader replay only. No installation or host rerun, fresh full suite, provider execution, native session continuation, visual or human acceptance.",
              "milestones": "M1/M2 and broader M3/M4/M5 remain open."}
    prior = BASE / "independent-final-review-01.json"
    result["preserved_prior_audit"] = {"path": str(prior.relative_to(ROOT)), **meta(prior.read_bytes()), "status": read(prior)["status"], "correction": "The staging ZIP includes its separately hashed input manifest. Native readiness intentionally excludes Python bytecode caches; this audit now records those actual cache bytes separately. No qualification result or prior audit was edited."}
    fresh_write(output, result)
    print(json.dumps({"status": result["status"], "passed": result["passed"], "total": result["total"], "receipt": str(output)}))
    raise SystemExit(result["status"] != "pass")
