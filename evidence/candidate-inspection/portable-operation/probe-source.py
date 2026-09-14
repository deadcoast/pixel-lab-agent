"""Retain an isolated packaged inspection proof using a controlled saved fixture.

This script imports no source runtime. All operations execute the copied plugin.
Its explicitly supplied judgments test evidence publication, not model/art quality.
"""

import argparse
import base64
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inventory(root):
    return {
        p.relative_to(root).as_posix(): sha(p)
        for p in sorted(root.rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts
    }


def run(destination):
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=False)
    package = destination / "package"
    shutil.copytree(
        REPO / "plugins/pixl", package, ignore=shutil.ignore_patterns("__pycache__")
    )
    root = destination / "project"
    root.mkdir()
    fixture_path = REPO / "evidence/candidate-inspection/portable-fixture.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    for row in fixture["files"]:
        path = (root / row["path"]).resolve()
        raw = base64.b64decode(row["content_base64"], validate=True)
        if (
            not path.is_relative_to(root)
            or hashlib.sha256(raw).hexdigest() != row["sha256"]
        ):
            raise ValueError("fixture path or byte identity differs")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    (destination / "probe-source.py").write_bytes(Path(__file__).read_bytes())
    shutil.copy2(fixture_path, destination / "input-fixture.json")
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PIXL_PLUGIN_ROOT", None)
    runner = [sys.executable, "-I", str(package / "scripts/pixl.py")]
    calls = []
    report = {
        "status": "running",
        "fixture_sha256": sha(fixture_path),
        "probe_sha256": sha(__file__),
        "bundle_manifest_sha256": sha(package / "bundle-manifest.json"),
        "calls": calls,
        "limitations": [
            "Controlled saved fixture and explicit developer review declarations; no model trial.",
            "No art generation, provider execution or engine import.",
            "A reference copy is a new candidate for lifecycle testing, not a produced revision.",
        ],
    }

    def invoke(*args, cwd=root, stdin=None):
        arguments = list(map(str, args))
        result = subprocess.run(
            runner + arguments,
            cwd=cwd,
            env=env,
            input=stdin,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=45,
            check=False,
        )
        calls.append(
            {
                "arguments": arguments,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
        if result.returncode:
            raise RuntimeError("packaged operation failed: " + arguments[0])
        return json.loads(result.stdout)

    def fields(doc, id_):
        return next(row["fields"] for row in doc["records"] if row["id"] == id_)

    def require(condition, message):
        if not condition:
            raise RuntimeError(message)

    try:
        manifest = json.loads(
            (package / "bundle-manifest.json").read_text(encoding="utf-8")
        )
        for entry in manifest["files"] + manifest["generated_files"]:
            packaged_file = (package / entry["path"]).resolve()
            require(
                packaged_file.is_relative_to(package)
                and sha(packaged_file) == entry["sha256"],
                "copied package differs from its manifest",
            )
        state, folder = root / ".pixl/state.px", root / ".pixl"
        initial = invoke("validate", state, "--root", root)
        before = invoke("decode", state)
        opts = root / "options.json"
        opts.write_text(
            json.dumps(
                {
                    "references": ["reference"],
                    "scale": 8,
                    "backgrounds": ["#ffffff", "#202838"],
                }
            ),
            encoding="utf-8",
        )
        prepared = invoke(
            "inspection-prepare",
            folder,
            "candidate",
            "packet",
            opts,
            "--expect",
            initial["hash"],
            "--root",
            root,
        )
        require(
            prepared["measurements"]["candidate"]["pass"],
            "fixture lost mechanical pass",
        )
        after_prepare = invoke("decode", state)
        require(
            fields(before, "task") == fields(after_prepare, "task"),
            "prepare changed task acceptance",
        )
        observation = {
            "reviewer": "user",
            "observed_at": datetime.now(UTC).isoformat(),
            "observations": [
                {
                    "view": view["id"],
                    "delivered_size": None,
                    "note": "Developer fixture declaration: no host delivery is attested by this script.",
                }
                for view in prepared["views"]
                if view["source"] == "candidate"
            ],
            "verdicts": [
                {
                    "criterion": "q.mechanical",
                    "status": "pass",
                    "reason": "Saved dimensions, palette and alpha checks pass.",
                    "supersedes": None,
                },
                {
                    "criterion": "q.visual",
                    "status": "fail",
                    "reason": "Controlled fixture comparison: left antenna and right yellow eye absent.",
                    "supersedes": None,
                },
                {
                    "criterion": "q.engine",
                    "status": "unavailable",
                    "reason": "No target browser project exists.",
                    "supersedes": None,
                },
            ],
            "next_action": "Retain a separate corrected candidate and perform its own review.",
            "limitations": [
                "Explicit fixture judgment tests retention; this script does not view images."
            ],
        }
        review_path = root / "review.json"
        review_path.write_text(json.dumps(observation), encoding="utf-8")
        reviewed = invoke(
            "inspection-review",
            folder,
            "packet",
            "review",
            review_path,
            "--expect",
            prepared["hash"],
            "--root",
            root,
        )
        doc = invoke("decode", state)
        require(
            fields(doc, "task")["st"] == {"$symbol": "open"}, "review completed task"
        )
        old_verdicts = {
            row["id"]: row for row in doc["records"] if row["kind"] in ("E", "V")
        }
        statuses = {
            row["fields"]["rq"]["$ref"]: row["fields"]["st"]["$symbol"]
            for row in old_verdicts.values()
            if row["kind"] == "V"
        }
        require(
            statuses
            == {"q.mechanical": "pass", "q.visual": "fail", "q.engine": "unavailable"},
            "review did not retain the exact boundary",
        )
        (root / "revision.png").write_bytes((root / "reference.png").read_bytes())
        revision = copy.deepcopy(
            next(row for row in doc["records"] if row["id"] == "candidate")
        )
        revision["id"] = "revision"
        revision["fields"].update(
            ur="revision.png",
            dg=sha(root / "revision.png"),
            nm="Reference-copy candidate for developer lifecycle proof",
        )
        doc["records"].append(revision)
        fields(doc, "task")["ca"] = [{"$ref": "revision"}]
        doc["revision"] += 1
        adapter = root / "revision.json"
        adapter.write_text(json.dumps(doc), encoding="utf-8")
        draft = root / "revision.px"
        # encode writes a file and returns no stdout.
        command = runner + ["encode", str(adapter), "--out", str(draft)]
        encoded = subprocess.run(
            command,
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=45,
            check=False,
        )
        calls.append(
            {
                "arguments": command[len(runner) :],
                "returncode": encoded.returncode,
                "stdout": encoded.stdout,
                "stderr": encoded.stderr,
            }
        )
        require(encoded.returncode == 0, "encoding new candidate failed")
        invoke("commit", folder, draft, "--expect", reviewed["hash"], "--root", root)
        cold = destination / "cold-project"
        shutil.copytree(root, cold)
        resumed = invoke("workflow", cold / ".pixl/state.px", "--root", cold, cwd=cold)
        output = next(task for task in resumed["tasks"] if task["id"] == "task")[
            "outputs"
        ][0]
        require(
            {row["status"] for row in output["requirements"]} == {"unperformed"},
            "replacement inherited a verdict",
        )
        frozen = invoke("decode", cold / ".pixl/state.px", cwd=cold)
        require(
            all(
                next(row for row in frozen["records"] if row["id"] == id_) == original
                for id_, original in old_verdicts.items()
            ),
            "earlier E/V changed",
        )
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "pixl_inspection",
                "arguments": {"path": ".pixl/state.px", "packet_id": "packet"},
            },
        }
        inspection = invoke(
            "mcp", "--root", cold, cwd=cold, stdin=json.dumps(request) + "\n"
        )["result"]
        require(not inspection["isError"], "copied MCP cannot read retained packet")
        packet = inspection["structuredContent"]["packets"][0]
        require(
            packet["candidate"] == "candidate" and len(packet["reviews"]) == 1,
            "cold report lost old candidate review",
        )
        report.update(
            status="pass",
            prepared_views=len(prepared["views"]),
            original_verdicts=statuses,
            replacement_status="unperformed",
            cold_inspection=inspection["structuredContent"],
            project_files=inventory(root),
            cold_project_files=inventory(cold),
            package_files=inventory(package),
        )
    except Exception as error:
        report.update(status="fail", error=f"{type(error).__name__}: {error}")
        raise
    finally:
        (destination / "report.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.out)
    print(
        json.dumps(
            {
                "status": result["status"],
                "calls": len(result["calls"]),
                "prepared_views": result["prepared_views"],
            }
        )
    )
