"""Include immutable agent resources in wheels without duplicating source trees."""

from pathlib import Path
import shutil

from setuptools import setup
from setuptools.command.build_py import build_py

ROOT = Path(__file__).resolve().parent


class BuildResources(build_py):
    def run(self):
        super().run()
        target = Path(self.build_lib) / "pixl" / "resources"
        for name in ("spec", "knowledge", "agent", "examples", "docs/research", "methods", "evidence/art-methods"):
            folder = ROOT / name
            if folder.exists():
                shutil.copytree(folder, target / name, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
        for name in ("links.md", "AGENT-PIXELART-TRAINING.md", "PIXEL-ART-ASSETS.md",
                     "pixel-art-deep-research-report.md", "research-pixel-art-systems.md"):
            shutil.copyfile(ROOT / name, target / name)
        (target / "pixl").mkdir(exist_ok=True)
        shutil.copyfile(ROOT / "pixl/registry.json", target / "pixl/registry.json")
        shutil.copyfile(ROOT / "pixl/poc.py", target / "pixl/poc.py")


setup(cmdclass={"build_py": BuildResources})
