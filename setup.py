"""Include immutable agent resources in wheels without duplicating source trees."""

import shutil
import sys
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from pixl.sources import INVENTORY_PATH, capture_inventory


class BuildResources(build_py):
    def run(self):
        inventory, snapshots = capture_inventory(ROOT)
        build_root = Path(self.build_lib).resolve()
        target = build_root / "pixl" / "resources"
        if (
            target.is_symlink()
            or not target.resolve().is_relative_to(build_root)
            or target.resolve() == (ROOT / "pixl/resources").resolve()
        ):
            raise RuntimeError("wheel resources must stay in the owned build output")
        super().run()
        # This resolved, confined directory is generated wheel output, not source.
        if target.exists():
            shutil.rmtree(target)
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
                shutil.copytree(
                    folder,
                    target / name,
                    dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"),
                )
        for name in [
            INVENTORY_PATH,
            *(row["path"] for row in inventory["documents"]),
            "NOTICE.md",
            *(
                ["evidence/source-migration/range-review.json"]
                if (ROOT / "evidence/source-migration/range-review.json").exists()
                else []
            ),
        ]:
            (target / name).parent.mkdir(parents=True, exist_ok=True)
            if name in snapshots:
                (target / name).write_bytes(snapshots[name])
            else:
                shutil.copyfile(ROOT / name, target / name)
        (target / "pixl").mkdir(exist_ok=True)
        for path in (ROOT / "pixl").iterdir():
            if path.suffix in (".py", ".json"):
                shutil.copyfile(path, target / "pixl" / path.name)


setup(cmdclass={"build_py": BuildResources})
