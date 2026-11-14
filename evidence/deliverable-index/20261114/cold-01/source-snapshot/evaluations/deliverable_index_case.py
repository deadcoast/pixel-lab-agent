"""NF-07: a native cold caller integrates only a public index/package/source set.

This fixture reuses actual CF-09 artwork. It never generates art, edits production
state, or treats browser mechanics as artistic, other-engine or human acceptance.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from evaluations.host_trials import codex_command, sha
from evaluations.request_review_trials import run as native_run

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "evidence/domain-art-revision/20261112/production-01/consumer-final.zip"
STATE = ".pixl/assets/robot.idle/state.px"
OUTPUT = "cf09-idle-family.delivery.output"
RENDERER = ROOT / "examples/consumer-execution/sprite-animation"
RENDERER_FILES = ("capture.mjs", "server.mjs", "view.mjs", "index.html", "check.py", "observation.py", "README.md")
SOURCE_FILES = (
    "pixl/deliverable_index.py", "pixl/service.py", "pixl/cli.py", "pixl/mcp.py",
    "pixl/delivery.py", "pixl/families.py", "pixl/lifecycle.py", "pixl/asset_lineage.py",
    "pixl/plar.py", "pixl/retention.py", "pixl/graph.py", "pixl/codec.py",
    "pixl/registry.json", "pixl/registry-v2.json",
    "evaluations/deliverable_index_case.py", "evaluations/request_review_trials.py",
    "evaluations/native_trial_records.py",
)


def write(path, value):
    """Fresh evidence only. Raw outputs and earlier failures are never replaced."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def confined(root, name):
    if (not isinstance(name, str) or not name or "\\" in name or ":" in name
            or Path(name).is_absolute() or any(p in ("", ".", "..") for p in name.split("/"))):
        raise ValueError("Expected canonical project-relative path")
    root = Path(root).resolve()
    path = (root / name).resolve()
    if path == root or not path.is_relative_to(root):
        raise ValueError("Path escapes its declared root")
    return path


def files(root):
    root = Path(root)
    return {
        path.relative_to(root).as_posix(): {
            "sha256": sha(path), "bytes": path.stat().st_size,
            "mtime_ns": path.stat().st_mtime_ns,
        }
        for path in sorted(root.rglob("*")) if path.is_file()
    }


def forbidden(names):
    """Inventory makes internal records absent, rather than merely inaccessible by instruction."""
    return [name for name in names if Path(name).suffix == ".px"
            or Path(name).name in ("plar.txt", "production-plar.txt", "plar.json")
            or "/plar-history/" in name or "/history/" in name
            or "/handoffs/" in name or "/runtime/" in name]


def command(args, cwd, target):
    result = subprocess.run(args, cwd=cwd, capture_output=True, timeout=180, check=False)
    target = Path(target)
    target.mkdir(parents=True, exist_ok=False)
    (target / "stdout.bin").write_bytes(result.stdout)
    (target / "stderr.bin").write_bytes(result.stderr)
    write(target / "command.json", {"argv": [str(a) for a in args], "cwd": str(cwd), "returncode": result.returncode})
    return result


def prepare(destination, python=None):
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError("Choose a fresh evidence attempt directory")
    destination.mkdir(parents=True)
    python = Path(python or sys.executable).resolve()
    producer = Path(tempfile.mkdtemp(prefix="pixl nf07 producer ")).resolve()
    consumer = Path(tempfile.mkdtemp(prefix="pixl nf07 cold ")).resolve()
    if producer.is_relative_to(ROOT) or consumer.is_relative_to(ROOT):
        raise ValueError("Consumer and producer must be outside repository ancestry")
    write(destination / "locations.json", {"producer": str(producer), "consumer": str(consumer), "python": str(python)})
    with zipfile.ZipFile(ARCHIVE) as archive:
        seen = set()
        for item in archive.infolist():
            if item.is_dir():
                continue
            if item.filename in seen or (item.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("Duplicate or symlink archive member")
            seen.add(item.filename)
            path = confined(producer, item.filename)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(archive.read(item))
    producer_before = files(producer)
    result = command([
        str(python), "-B", "-m", "pixl", "family", str(producer / STATE), OUTPUT,
        "--root", str(producer), "--view", "consumer", "--result-path", "deliverable-index.json",
    ], ROOT, destination / "index-command")
    if result.returncode:
        write(destination / "PREPARATION-FAILURE.json", {"stage": "index", "returncode": result.returncode})
        raise RuntimeError("Index CLI failed; exact output retained")
    default = command([
        str(python), "-B", "-m", "pixl", "family", str(producer / STATE), OUTPUT,
        "--root", str(producer),
    ], ROOT, destination / "full-family-command")
    if default.returncode:
        write(destination / "PREPARATION-FAILURE.json", {"stage": "full_family", "returncode": default.returncode})
        raise RuntimeError("Default family CLI failed; exact output retained")
    index_path = producer / "deliverable-index.json"
    index = json.loads(index_path.read_bytes())
    if index["schema"] != "pixl.deliverable-index/1" or not index["family"]["current_eligible"]:
        write(destination / "PREPARATION-FAILURE.json", {"stage": "index_eligibility", "index": index})
        raise RuntimeError("Retained CF-09 reference did not expose current eligible package")
    public = {index["package"]["manifest"], *(row["path"] for row in index["assets"])}
    public.update(row["path"] for row in index["integration"]["sources"] if row.get("path"))
    if forbidden(public):
        raise ValueError("Index source closure unexpectedly includes an internal record")
    for name in sorted(public):
        source, target = confined(producer, name), confined(consumer, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    shutil.copy2(index_path, consumer / "deliverable-index.json")
    renderer = consumer / "renderer"
    renderer.mkdir()
    for name in RENDERER_FILES:
        shutil.copy2(RENDERER / name, renderer / name)
    assignment = f"""# NF-07 public package consumption

You are a cold calling agent integrating the delivered package in this directory.
Read deliverable-index.json. The index, immutable manifest and exact files, and the
index's cited integration sources are your only production inputs. The renderer
guide describes the supplied sprite-animation-v1 browser consumer. No PIXL state,
PLAR, installed PIXL runtime or prior handoff is supplied. Do not fetch those from
elsewhere or inspect the repository, provider credentials, global settings or memory.
Work within this consumer only. This is an isolated evaluation, not a sandbox claim.

Use the index's names, paths and declared integration choices/source files to:
1. Verify exact manifest and package identities. Distinguish the immutable creation
   acceptance from the index's observed current review; the index is a snapshot.
2. Copy the selected exact package bytes to the declared named destinations. Find
   the cited authored animation module, verify its identity, and place its unchanged
   bytes at the module path declared by the integration choice. Do not reconstruct
   missing metadata or infer an animation from manifest order/numbered filenames.
3. Author config.json from the supplied consumer guide and indexed choices. Preserve
   the authored layout, timing, pivots, sampling and other module decisions. Run the
   actual isolated browser capture and independent Python checker. Write capture to
   work/capture-01 and checker output to work/check-01.json. Keep failures if a fresh
   retry is needed; choose a new suffix and retain all preceding outputs.
4. Write CALLER-RESULT.json with status, index {{path,sha256}}, manifest {{path,sha256}},
   assets [{{output,candidate,path,sha256,bytes}}] for the named integrated destinations,
   module {{path,sha256}}, config {{path,sha256}}, capture {{path,sha256}} for capture.json,
   check {{path,sha256}}, creation_accepted, observed_current_eligible, unresolved,
   provenance_summary and limits. Record actual results, not a self-certified pass.

Only index.json and its referenced public files may establish production facts.
Keep initial inputs byte-for-byte unchanged. New files may be named consumer assets,
the exact consumer module, config.json, work/* and CALLER-RESULT.json. Do not generate
art, call providers, install dependencies, mutate acceptance, or delegate this small
consumer task. Human artistic acceptance and other engines remain separate.
Selected Python: {python.as_posix()}
Node and an installed Chromium browser are available through normal renderer discovery.
""".replace("Only index.json", "Only deliverable-index.json")
    (consumer / "ASSIGNMENT.md").write_text(assignment, encoding="utf-8", newline="\n")
    (consumer / "AGENTS.md").write_text("Follow ASSIGNMENT.md for this explicit isolated NF-07 consumer evaluation.\n", encoding="utf-8", newline="\n")
    prompt = "Complete ASSIGNMENT.md in the current consumer directory. Use only its supplied public package inputs. Retain actual browser/checker evidence and CALLER-RESULT.json."
    (destination / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    native = codex_command()
    launch = {
        "host": "codex", "case": "nf07-public-consumer", "cwd": str(consumer),
        "command": native + ["exec", "--ignore-user-config", "--ignore-rules", "--json",
            "--skip-git-repo-check", "--approve-for-me", "-C", str(consumer),
            "-c", "features.apps=false", "-c", "features.plugins=false",
            "-c", 'web_search="disabled"', "-"],
        "host_version": subprocess.check_output(native + ["--version"], text=True).strip(),
        "configuration_files": {},
    }
    write(destination / "launch.json", launch)
    before = files(consumer)
    if forbidden(before):
        raise ValueError("Cold caller contains internal state")
    source_hashes = {name: sha(ROOT / name) for name in SOURCE_FILES}
    identity = {
        "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "source_hashes": source_hashes, "fixture": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "sha256": sha(ARCHIVE)},
        "producer_root": str(producer), "consumer_root": str(consumer),
        "producer_inputs": producer_before, "inputs": before,
        "prompt_sha256": sha(destination / "prompt.txt"),
        "internal_state_files": forbidden(before), "public_files": sorted(public),
        "isolation": "Fresh external directory with no state/PLAR/runtime; process permissions are not an OS sandbox.",
        "scope": "Current source CLI export and one native package-only consumption of retained actual CF-09 art; no new provider or artistic/human acceptance.",
    }
    write(destination / "identity.json", identity)
    shutil.copytree(consumer, destination / "input-project")
    source_snapshot = destination / "source-snapshot"
    for name in SOURCE_FILES:
        target = source_snapshot / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
    after = files(producer)
    unchanged = all(after.get(name) == row for name, row in producer_before.items())
    write(destination / "preparation.json", {"status": "pass" if unchanged else "fail", "producer_inputs_unchanged": unchanged,
        "producer_input_count": len(producer_before), "consumer_input_count": len(before),
        "index": {"path": "input-project/deliverable-index.json", "sha256": sha(index_path), "bytes": index_path.stat().st_size},
        "full_family_bytes": len(default.stdout),
        "new_producer_files": sorted(set(after) - set(producer_before)), "internal_state_files": forbidden(before)})
    if not unchanged:
        raise RuntimeError("Read-only index changed producer input bytes or mtimes")
    return {"attempt": str(destination), "consumer": str(consumer), "inputs": len(before)}


def run(destination, timeout=900):
    destination = Path(destination).resolve()
    identity = json.loads((destination / "identity.json").read_bytes())
    if any(sha(ROOT / name) != expected for name, expected in identity["source_hashes"].items()):
        raise ValueError("Prepared implementation changed; use a fresh attempt")
    native_run(destination, timeout=timeout)
    retain(destination)


def retain(destination):
    destination = Path(destination).resolve()
    consumer = Path(json.loads((destination / "launch.json").read_bytes())["cwd"])
    target = destination / "project"
    if target.exists():
        raise ValueError("Retained consumer already exists; earlier evidence is immutable")
    shutil.copytree(consumer, target)
    write(destination / "consumer-after.json", files(consumer))


def check(destination, output):
    destination, output = Path(destination).resolve(), Path(output).resolve()
    if output.exists():
        raise ValueError("Choose a fresh independent check receipt")
    identity = json.loads((destination / "identity.json").read_bytes())
    project = Path(identity["consumer_root"])
    checks = []

    def expect(value, name, details=None):
        checks.append({"name": name, "pass": bool(value), **({"details": details} if details is not None else {})})

    after = files(project)
    expect(not forbidden(identity["inputs"]), "initial inputs contain no internal state, PLAR, history or runtime")
    expect(all(after.get(name) == row for name, row in identity["inputs"].items()), "every initial input preserves exact bytes and mtime")
    expect(all(sha(ROOT / name) == expected for name, expected in identity["source_hashes"].items()), "tested implementation source identity")
    expect(sha(ARCHIVE) == identity["fixture"]["sha256"], "historical production archive unchanged")
    record = json.loads((destination / "record.json").read_bytes())
    expect(record["returncode"] == 0 and record["execution_status"] == "host_completed_ungraded", "native host completed")
    index = json.loads((project / "deliverable-index.json").read_bytes())
    manifest = json.loads(confined(project, index["package"]["manifest"]).read_bytes())
    caller_path = project / "CALLER-RESULT.json"
    expect(caller_path.is_file(), "caller retained concrete result")
    if caller_path.is_file():
        caller = json.loads(caller_path.read_bytes())
        expect(caller.get("creation_accepted") is False and manifest["acceptance"]["accepted"] is False,
               "caller preserves immutable creation acceptance false")
        expect(caller.get("observed_current_eligible") is True and index["family"]["current_eligible"] is True,
               "caller separately reports observed current eligibility")
        expect(caller.get("unresolved") == index["unresolved"] == [], "caller preserves index unresolved conditions")
        expect(bool(caller.get("provenance_summary")) and bool(caller.get("limits")), "caller states provenance and acceptance limits")
        for key in ("index", "manifest", "module", "config", "capture", "check"):
            ref = caller.get(key, {})
            path = confined(project, ref.get("path"))
            expect(path.is_file() and sha(path) == ref.get("sha256"), "caller exact " + key + " reference")
        expect(caller["index"]["path"] == "deliverable-index.json" and caller["manifest"]["path"] == index["package"]["manifest"],
               "caller compares supplied index and immutable manifest")
        rows = {row["output"]: row for row in caller.get("assets", [])}
        expect(len(rows) == len(caller.get("assets", [])) == len(index["assets"]) == 5, "caller identifies each package member once")
        for member in index["assets"]:
            row = rows.get(member["output"], {})
            path = confined(project, row.get("path"))
            expect(row.get("candidate") == member["candidate"] and path.is_file() and
                   sha(path) == row.get("sha256") == member["sha256"] and
                   path.stat().st_size == row.get("bytes") == member["bytes"], "exact named destination: " + member["output"])
            expect(row.get("path") == member["source_path"], "authored named destination: " + member["output"])
        config = json.loads(confined(project, caller["config"]["path"]).read_bytes())
        expect(config["destinations"] == {row["output"]: row["source_path"] for row in index["assets"]}, "configured exact output to destination mapping")
        module_sources = [row for row in index["integration"]["sources"] if row["sha256"] == caller["module"]["sha256"]]
        expect(len(module_sources) == 1 and config["modules"]["animation"] == caller["module"]["path"], "exact indexed consumer module used unchanged")
        capture_path = confined(project, caller["capture"]["path"])
        capture = json.loads(capture_path.read_bytes())
        renderer_check = json.loads(confined(project, caller["check"]["path"]).read_bytes())
        expect(renderer_check.get("pass") is True and renderer_check.get("status") == "pass", "caller retained passing actual renderer check")
        frames = capture["animation"]["clips"][0]["frames"]
        expect([f["duration_ms"] for f in frames] == [800, 120, 160, 120, 400], "preserved unequal authored timings")
        expect([f["pivot"] for f in frames] == [[16, 28]] * 5 and [f["rect"] for f in frames] == [[0, 0, 32, 32]] * 5,
               "preserved authored frame crops and pivots")
        expect(capture["animation"]["clips"][0]["anchor"] == [24, 34] and capture["animation"]["viewport"] == [48, 40], "preserved authored anchor and viewport")
        expect([f["path"] for f in frames] == [member["source_path"] for member in index["assets"]], "preserved actual authored frame order")
        expect(len(capture["views"]) == 10 and {v["scale"] for v in capture["views"]} == {1, 3}, "all five frames captured at native and enlarged scale")
        expect(len(capture["playbacks"]) == 2 and all(p["status"] == "observed" and p["frames"] == list(range(5)) and
                   p["wraps"] >= 2 and p["skips"] == 0 for p in capture["playbacks"]), "actual playback observes every frame and two wraps without skips")
        independent = output.with_name(output.stem + "-renderer.json")
        locations = json.loads((destination / "locations.json").read_bytes())
        result = command([locations["python"], "-B", str(project / "renderer/check.py"), "--project", str(project),
                          "--capture", str(capture_path.parent), "--out", str(independent)], project,
                         output.with_name(output.stem + "-renderer-command"))
        expect(result.returncode == 0 and json.loads(independent.read_bytes()).get("pass") is True,
               "independent exact-source renderer check rerun")
        expect(sha(project / "renderer/check.py") == identity["inputs"]["renderer/check.py"]["sha256"], "independent checker bytes unchanged")
    result = {"version": 1, "status": "pass" if all(row["pass"] for row in checks) else "fail",
              "passed": sum(row["pass"] for row in checks), "total": len(checks), "checks": checks,
              "scope": "One native cold caller using only supplied index, immutable package, declared source files and renderer; actual browser mechanics on retained art.",
              "limits": ["Input absence and public trace support the no-internal-state task boundary; filesystem permissions are not an OS sandbox.",
                         "No fresh provider execution, generative improvement, other-engine qualification or human artistic acceptance.",
                         "Current eligibility is the index's observed snapshot, not a claim that an unobserved producer can never change."]}
    write(output, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "run", "retain", "check"))
    parser.add_argument("--attempt", type=Path, required=True)
    parser.add_argument("--python", type=Path)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if args.action == "prepare":
        result = prepare(args.attempt, args.python)
    elif args.action == "run":
        result = run(args.attempt, args.timeout)
    elif args.action == "retain":
        result = retain(args.attempt)
    else:
        if args.out is None:
            parser.error("check requires a fresh --out path")
        result = check(args.attempt, args.out)
    if result is not None:
        print(json.dumps(result if args.action != "check" else {key: result[key] for key in ("status", "passed", "total")}))


if __name__ == "__main__":
    main()
