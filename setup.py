"""Include immutable agent resources in wheels without duplicating source trees."""

import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py

ROOT = Path(__file__).resolve().parent


class BuildResources(build_py):
    def run(self):
        super().run()
        target = Path(self.build_lib) / "pixl" / "resources"
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
        for name in (
            "links.md",
            "AGENT-PIXELART-TRAINING.md",
            "PIXEL-ART-ASSETS.md",
            "pixel-art-deep-research-report.md",
            "research-pixel-art-systems.md",
            "NOTICE.md",
        ):
            shutil.copyfile(ROOT / name, target / name)
        (target / "pixl").mkdir(exist_ok=True)
        for path in (ROOT / "pixl").iterdir():
            if path.suffix in (".py", ".json"):
                shutil.copyfile(path, target / "pixl" / path.name)


setup(cmdclass={"build_py": BuildResources})
