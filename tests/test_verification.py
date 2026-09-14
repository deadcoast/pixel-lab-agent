"""Exercise failed verification and real source-distribution packaging boundaries."""

import json
import shutil
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts import check_wheel

ROOT = Path(__file__).resolve().parents[1]


class VerificationTests(unittest.TestCase):
    def test_missing_source_replaces_old_pass_and_preserves_previous_bytes(self):
        with TemporaryDirectory(prefix="pixl failed verification ") as tmp:
            root = Path(tmp)
            for name in ("pixl", "scripts"):
                shutil.copytree(
                    ROOT / name,
                    root / name,
                    ignore=shutil.ignore_patterns("__pycache__"),
                )
            (root / "training").mkdir()
            shutil.copyfile(
                ROOT / "training/source-inventory.json",
                root / "training/source-inventory.json",
            )
            evidence = root / "evidence"
            evidence.mkdir()
            previous = b'{"status":"pass","old_receipt":true}\n'
            (evidence / "test-results.json").write_bytes(previous)
            result = subprocess.run(
                [sys.executable, str(root / "scripts/verify.py")],
                cwd=root,
                capture_output=True,
                check=False,
                timeout=30,
            )
            self.assertNotEqual(result.returncode, 0)
            report = json.loads((evidence / "test-results.json").read_bytes())
            self.assertEqual(report["status"], "fail", result.stderr.decode())
            self.assertIn("source_missing", report["error"])
            self.assertEqual(report["stage"], "sources")
            self.assertEqual(report["tests"]["status"], "not_run")
            run = root / report["run_directory"]
            self.assertEqual(json.loads((run / "result.json").read_bytes()), report)
            with zipfile.ZipFile(run / "previous.zip") as archive:
                self.assertEqual(archive.read("evidence/test-results.json"), previous)

    def test_wheel_checker_rejects_sources_omitted_from_sdist(self):
        # A direct wheel build would succeed here: the checkout has every source.
        # Only building through the actual sdist exposes the broken manifest.
        with TemporaryDirectory(prefix="pixl broken sdist ") as tmp:
            root = Path(tmp)
            for name in (
                "pixl",
                "spec",
                "knowledge",
                "agent",
                "examples",
                "docs/research",
                "methods",
                "evidence/art-methods",
                "evidence/source-migration",
                "training/original-docs",
            ):
                shutil.copytree(
                    ROOT / name,
                    root / name,
                    ignore=shutil.ignore_patterns("__pycache__", "previous-run"),
                )
            for name in (
                "setup.py",
                "pyproject.toml",
                "NOTICE.md",
                "README.md",
                "training/source-inventory.json",
            ):
                shutil.copyfile(ROOT / name, root / name)
            manifest = (ROOT / "MANIFEST.in").read_text(encoding="utf-8")
            (root / "MANIFEST.in").write_text(
                manifest + "\nprune training/original-docs\n", encoding="utf-8"
            )
            with (
                patch.object(check_wheel, "ROOT", root),
                self.assertRaisesRegex(RuntimeError, "source_missing"),
            ):
                check_wheel.run()
