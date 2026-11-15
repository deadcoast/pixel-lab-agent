"""Bounded local package and skill-discovery checks; no native model sampling."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
KIT = ROOT / "plugins/pixl"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(name, value):
    path = OUT / name
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def files(root):
    return {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in sorted(root.rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts}


def snapshot():
    manifest = json.loads((KIT / "bundle-manifest.json").read_bytes())
    names = {row["source"] for row in manifest["files"]}
    names.update({"scripts/build_plugin.py", "tests/test_packaging.py", "pixl/readiness.py",
                  "pyproject.toml", ".agents/PROFILE.md", "evaluations/skill_handoff_trials.py"})
    for host in (".agents", ".claude"):
        names.update(f"{host}/skills/{skill}/SKILL.md" for skill in ("pixl", "plar"))
    source = {name: (ROOT / name).read_bytes() for name in sorted(names)}
    return {"source_inputs": source, "runtime_source": files(ROOT / "pixl"), "kit": files(KIT)}


def hashes(captured):
    return {group: {name: digest(raw) for name, raw in data.items()} for group, data in captured.items()}


def command(name, args):
    started = time.monotonic()
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run(args, cwd=ROOT, env=environment, capture_output=True)
    for stream in ("stdout", "stderr"):
        with (OUT / f"{name}-{stream}.txt").open("xb") as output:
            output.write(getattr(result, stream))
    return {"name": name, "command": args, "returncode": result.returncode,
            "elapsed_seconds": round(time.monotonic() - started, 3)}


def skills():
    rows = []
    paths = [f"plugins/pixl/skills/{name}/SKILL.md" for name in ("pixl", "plar")]
    paths += [f"{host}/skills/{name}/SKILL.md" for host in (".agents", ".claude") for name in ("pixl", "plar")]
    for name in paths:
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        boundary = lines.index("---", 1) if lines and lines[0] == "---" and "---" in lines[1:] else 0
        metadata = dict(line.split(":", 1) for line in lines[1:boundary] if ":" in line)
        expected = path.parent.name
        frontmatter = bool(boundary and metadata.get("name", "").strip() == expected and metadata.get("description", "").strip())
        links = []
        for _, location in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text):
            if "://" in location or location.startswith("mailto:"):
                continue
            relative, _, anchor = location.partition("#")
            target = (path.parent / relative).resolve() if relative else path
            headings = []
            if target.is_file() and anchor:
                headings = [re.sub(r"[^\w\s-]", "", heading.lower()).replace(" ", "-")
                            for heading in re.findall(r"^#{1,6}\s+(.+?)\s*$", target.read_text(encoding="utf-8"), re.MULTILINE)]
            links.append({"route": location, "target": str(target), "exists": target.is_file(),
                          "anchor": anchor or None, "anchor_exists": anchor in headings if anchor else None})
        rows.append({"path": name, "sha256": digest(path.read_bytes()), "frontmatter": metadata,
                     "frontmatter_valid": frontmatter, "local_routes": links,
                     "routes_valid": all(item["exists"] and (item["anchor_exists"] is not False) for item in links)})
    common = ROOT / "plugins/pixl/skills/pixl/SKILL.md"
    reference = common.parent / "references/intake-sample.md"
    exact_route = "references/intake-sample.md#cold-intake-handoff"
    cold = {"route": exact_route, "linked": f"]({exact_route})" in common.read_text(encoding="utf-8"),
            "heading": "## Cold intake handoff", "heading_exists": "## Cold intake handoff" in reference.read_text(encoding="utf-8").splitlines(),
            "source": str(reference), "source_sha256": digest(reference.read_bytes())}
    return {"skill_count": len(rows), "skills": rows, "cold_handoff": cold,
            "status": "pass" if all(row["frontmatter_valid"] and row["routes_valid"] for row in rows) and cold["linked"] and cold["heading_exists"] else "fail",
            "scope": "Local discovery format and resolvable routes; no claim about native loading or behavior."}


if __name__ == "__main__":
    if (OUT / "before.json").exists():
        raise ValueError("Use a fresh evidence directory; do not overwrite an earlier check")
    sys.path.insert(0, str(ROOT))
    before = snapshot()
    write("before.json", hashes(before))
    commands = [command("packaging", [sys.executable, "-B", "-m", "unittest", "tests.test_packaging", "-v"])]
    commands.append(command("readiness", [sys.executable, "-B", "-c",
        "import json;from pathlib import Path;from pixl.readiness import verify_manifest;print(json.dumps(verify_manifest(Path('plugins/pixl').resolve()),indent=2))"]))
    routing = skills()
    write("skill-routes.json", routing)
    after = snapshot()
    write("after.json", hashes(after))
    changes = {}
    for group in before:
        differences = [name for name in sorted(set(before[group]) | set(after[group])) if before[group].get(name) != after[group].get(name)]
        changes[group] = differences
        if differences:
            for label, state in (("before", before[group]), ("after", after[group])):
                with zipfile.ZipFile(OUT / f"unexpected-{group}-{label}.zip", "x", zipfile.ZIP_DEFLATED) as archive:
                    for name in differences:
                        if name in state:
                            archive.writestr(name, state[name])
    readiness = json.loads((OUT / "readiness-stdout.txt").read_bytes())
    result = {"status": "pass" if all(row["returncode"] == 0 for row in commands) and readiness["status"] == "verified" and routing["status"] == "pass" and not any(changes.values()) else "fail",
        "commands": commands, "packaging_tests": unittest.defaultTestLoader.loadTestsFromName("tests.test_packaging").countTestCases(),
        "source_counts": {group: len(data) for group, data in before.items()}, "changed_files": changes,
        "readiness": readiness, "discovery_routes_status": routing["status"], "discovery_skill_count": routing["skill_count"],
        "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "runner_sha256": digest(Path(__file__).read_bytes()),
        "scope": "Four local packaging tests, manifest readiness, and skill discovery routes. Bundle builder writes are expected; before/after hashes identify any actual byte changes. Synthetic provider/family probes do not execute remote tools or establish artwork, native host, or engine acceptance."}
    write("RESULT.json", result)
    print(json.dumps(result, indent=2))
