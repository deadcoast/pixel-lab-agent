"""Build the portable plugin from source; verify hashes of every bundled file."""

import hashlib
import json
import shutil
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "pixl"


def build():
    plan = {}

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
        "agent",
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
    for name in (
        "links.md",
        "AGENT-PIXELART-TRAINING.md",
        "PIXEL-ART-ASSETS.md",
        "pixel-art-deep-research-report.md",
        "research-pixel-art-systems.md",
    ):
        add(ROOT / name, Path("resources") / name)
    add(ROOT / "NOTICE.md", Path("NOTICE.md"))
    entries = []
    for target, source in sorted(plan.items()):
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        data = target.read_bytes()
        entries.append(
            {
                "path": target.relative_to(PLUGIN).as_posix(),
                "source": source.relative_to(ROOT).as_posix(),
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
            }
        )
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    (PLUGIN / "requirements.txt").write_text(
        "\n".join(metadata["project"]["dependencies"]) + "\n", encoding="utf-8"
    )
    manifest = {
        "version": metadata["project"]["version"],
        "files": entries,
        "sources_preserved": True,
        "generated_by": "scripts/build_plugin.py",
    }
    (PLUGIN / "bundle-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return {
        "plugin": str(PLUGIN),
        "files": len(entries),
        "bytes": sum(e["bytes"] for e in entries),
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
