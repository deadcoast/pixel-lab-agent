"""Build the portable plugin from source; verify hashes of every bundled file."""

import hashlib
import json
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "pixl"
sys.path.insert(0, str(ROOT))

from pixl.graph import confined
from pixl.sources import INVENTORY_PATH, capture_inventory


def build():
    inventory, source_snapshots = capture_inventory(ROOT)
    plan = {}
    captured = {}

    def add(source, relative):
        target = (PLUGIN / relative).resolve()
        if not target.is_relative_to(PLUGIN.resolve()):
            raise ValueError("bundle path escapes plugin")
        plan[target] = Path(source)

    for path in (ROOT / "pixl").iterdir():
        if path.suffix in (".py", ".json"):
            add(path, Path("runtime/pixl") / path.name)
            # Source evidence remains an importable package with the same dependency closure.
            add(path, Path("resources/pixl") / path.name)
    for name in (
        "spec",
        "knowledge",
        "examples",
        "docs/research",
        "methods",
        "evidence/art-methods",
    ):
        folder = ROOT / name
        if folder.exists():
            for path in folder.rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts:
                    add(path, Path("resources") / path.relative_to(ROOT))
    add(ROOT / ".agents/PROFILE.md", Path("resources/agent/PROFILE.md"))
    for name in [INVENTORY_PATH, *(row["path"] for row in inventory["documents"])]:
        add(ROOT / name, Path("resources") / name)
        captured[(PLUGIN / "resources" / name).resolve()] = source_snapshots[name]
    review = ROOT / "evidence/source-migration/range-review.json"
    if review.exists():
        add(review, Path("resources") / review.relative_to(ROOT))
    add(ROOT / "NOTICE.md", Path("NOTICE.md"))
    for plugin_folder in (
        "skills",
        "agents",
        "scripts",
        "config",
        ".claude-plugin",
        ".codex-plugin",
    ):
        for path in (PLUGIN / plugin_folder).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                add(path, path.relative_to(PLUGIN))
    # Preflight all bytes before changing an installed/generated file.
    snapshots = {}
    for target, source in plan.items():
        snapshots[target] = (
            captured[target] if target in captured else source.read_bytes()
        )
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = metadata.get("project", {})
    version, dependencies = project.get("version"), project.get("dependencies")
    if (
        not isinstance(version, str)
        or not version
        or not isinstance(dependencies, list)
        or not all(isinstance(item, str) for item in dependencies)
    ):
        raise ValueError("package metadata requires a version and a dependency list")
    requirements = ("\n".join(dependencies) + "\n").encode("utf-8")
    requirements_path = confined(PLUGIN, "requirements.txt")
    obsolete = []
    manifest_path = confined(PLUGIN, "bundle-manifest.json")
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        for row in previous["files"]:
            target = confined(PLUGIN, row["path"])
            if target in plan or not target.exists():
                continue
            if not row["path"].startswith(("resources/", "runtime/")):
                continue
            if hashlib.sha256(target.read_bytes()).hexdigest() != row["sha256"]:
                raise ValueError(f"obsolete generated file was modified: {row['path']}")
            obsolete.append(target)
    entries = []
    for target, source in sorted(plan.items()):
        target.parent.mkdir(parents=True, exist_ok=True)
        data = snapshots[target]
        if target != source.resolve():
            target.write_bytes(data)
        entries.append(
            {
                "path": target.relative_to(PLUGIN).as_posix(),
                "source": source.relative_to(ROOT).as_posix(),
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
            }
        )
    for path in obsolete:
        path.unlink()
    requirements_path.write_bytes(requirements)
    manifest = {
        "version": version,
        "files": entries,
        "declared_source_revisions_verified": True,
        "source_inventory_sha256": hashlib.sha256(
            source_snapshots[INVENTORY_PATH]
        ).hexdigest(),
        "generated_files": [
            {
                "path": "requirements.txt",
                "sha256": hashlib.sha256(requirements).hexdigest(),
            }
        ],
        "generated_by": "scripts/build_plugin.py",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {
        "plugin": str(PLUGIN),
        "files": len(entries),
        "bytes": sum(e["bytes"] for e in entries),
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
