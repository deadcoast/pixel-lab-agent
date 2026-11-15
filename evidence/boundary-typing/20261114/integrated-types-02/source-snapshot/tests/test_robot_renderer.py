"""Bounded robot rendering with synthetic pixels, never directional art acceptance."""
from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "examples/delegation/renderer"
SPEC = importlib.util.spec_from_file_location("robot_renderer_check", RENDERER / "check.py")
assert SPEC and SPEC.loader
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


def write_json(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")


def fixture(root):
    """Copy the existing south sprite to all facings solely to probe the renderer."""
    (root / "src").mkdir(parents=True)
    (root / "assets/robot").mkdir(parents=True)
    shutil.copy2(ROOT / "examples/delegation/src/robot.ts", root / "src/robot.ts")
    shutil.copy2(ROOT / "examples/delegation/assets/robot-base.png", root / "assets/robot-base.png")
    for direction in CHECK.DIRECTIONS:
        shutil.copy2(root / "assets/robot-base.png", root / f"assets/robot/{direction}.png")
    (root / "SYNTHETIC-TEST.md").write_text("Synthetic mechanical test: all facings copy the existing south fixture. No new art, semantic direction or visual acceptance is claimed.\n", encoding="utf-8")


class RobotRendererBoundaryTests(unittest.TestCase):
    def test_noncanonical_references_are_rejected(self):
        for name in ("../outside.png", "assets/../x.png", "assets\\x.png", "a//b", "/absolute", "C:/outside", ""):
            with self.subTest(name=name), self.assertRaises(ValueError):
                CHECK.confined(ROOT, name)

    def test_absent_capture_is_unavailable_not_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            result = CHECK.check(folder, Path(folder) / "missing")
            self.assertEqual(result["status"], "unavailable")
            self.assertFalse(result["pass"])

    @unittest.skipUnless(shutil.which("node"), "Node unavailable")
    def test_unavailable_browser_retains_receipt_without_execution(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            fixture(root)
            result = subprocess.run([shutil.which("node"), str(RENDERER / "capture.mjs"), "--project", str(root), "--out", str(root / "capture"), "--browser", str(root / "missing-browser")], capture_output=True, text=True, timeout=10, check=False)
            self.assertNotEqual(result.returncode, 0)
            receipt = json.loads((root / "capture/execution.json").read_bytes())
            self.assertEqual(receipt["status"], "unavailable")
            self.assertFalse(receipt["renderer_executed"])
            self.assertTrue(receipt["cleanup"]["complete"])
            self.assertTrue((root / "capture/inputs.json").is_file())


class RobotRendererBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.node = shutil.which("node")
        candidates = [Path("C:/Program Files/Google/Chrome/Application/chrome.exe"), Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"), Path("/usr/bin/chromium"), Path("/usr/bin/google-chrome")]
        cls.browser = next((path for path in candidates if path.is_file()), None)
        if not cls.node or not cls.browser:
            raise unittest.SkipTest("Installed local Node/Chromium unavailable")
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        fixture(cls.root)
        shutil.copytree(RENDERER, cls.root / "renderer")
        cls.original_inputs = {name: (cls.root / name).read_bytes() for name in CHECK.INPUTS}
        result = cls.capture(cls.root / "capture")
        if result.returncode:
            raise AssertionError("Synthetic robot capture failed: " + result.stdout + result.stderr)
        cls.original_capture = {path.name: path.read_bytes() for path in (cls.root / "capture").iterdir() if path.is_file()}
        cls.report = json.loads(cls.original_capture["capture.json"])

    @classmethod
    def capture(cls, out):
        return subprocess.run([cls.node, str(cls.root / "renderer/capture.mjs"), "--project", str(cls.root), "--out", str(out), "--browser", str(cls.browser)], capture_output=True, text=True, timeout=55, check=False)

    def setUp(self):
        for name, data in self.original_inputs.items():
            (self.root / name).write_bytes(data)
        for name, data in self.original_capture.items():
            (self.root / "capture" / name).write_bytes(data)

    def recheck(self, capture=None):
        return CHECK.check(self.root, capture or self.root / "capture", self.root / "renderer")

    def test_actual_controller_and_browser_pixels_with_synthetic_fixture(self):
        result = self.recheck()
        self.assertTrue(result["pass"], result["failures"])
        self.assertEqual(result["facts"], {"input_checks": 6, "renderer_checks": 5, "pixel_checks": 8, "screenshot_checks": 8})
        self.assertTrue(any("identical files" in text for text in result["limitations"]))
        for name, expected in self.original_inputs.items():
            self.assertEqual((self.root / name).read_bytes(), expected)
        self.assertEqual(self.report["selected_mapping"], CHECK.MAPPING)

    def test_missing_direction_retains_failed_capture(self):
        (self.root / "assets/robot/north.png").unlink()
        out = self.root / "missing-capture"
        result = self.capture(out)
        self.assertNotEqual(result.returncode, 0)
        receipt = json.loads((out / "execution.json").read_bytes())
        report = json.loads((out / "capture.json").read_bytes())
        self.assertEqual(receipt["status"], "failed")
        self.assertTrue(receipt["cleanup"]["complete"])
        self.assertIsNone(report["inputs"]["assets/robot/north.png"])
        self.assertFalse(self.recheck(out)["pass"])

    def test_actual_wrong_direction_mapping_fails_even_for_identical_images(self):
        source = self.root / "src/robot.ts"
        source.write_text(source.read_text().replace('return robotSprites[facing]', 'return robotSprites[facing === "east" ? "west" : facing]'), encoding="utf-8")
        out = self.root / "wrong-mapping-capture"
        result = self.capture(out)
        self.assertNotEqual(result.returncode, 0)
        report = json.loads((out / "capture.json").read_bytes())
        self.assertEqual(report["selected_mapping"]["east"], "assets/robot/west.png")
        self.assertFalse(self.recheck(out)["pass"])

    def test_modified_source_or_south_cannot_reuse_old_capture(self):
        for name in ("src/robot.ts", "assets/robot/south.png"):
            with self.subTest(name=name):
                path = self.root / name
                before = path.read_bytes()
                path.write_bytes(before + b"changed")
                result = self.recheck()
                self.assertFalse(result["pass"])
                self.assertTrue(any("exact served input" in text for text in result["failures"]))
                path.write_bytes(before)

    def test_altered_view_pixels_fail_even_if_capture_hash_is_rebound(self):
        report = copy.deepcopy(self.report)
        reference = report["views"][0]["image"]
        path = self.root / "capture" / reference["path"]
        image = Image.open(path).convert("RGBA")
        image.putpixel((0, 0), (255, 0, 255, 255))
        image.save(path)
        reference["sha256"] = CHECK.digest(path)
        write_json(self.root / "capture/capture.json", report)
        result = self.recheck()
        self.assertFalse(result["pass"])
        self.assertIn("source alpha/compositing/nearest pixels: south@1", result["failures"])
        self.assertIn("actual screenshot canvas pixels: south@1", result["failures"])

    def test_screenshot_tampering_is_detected_with_rebound_file_hash(self):
        report = copy.deepcopy(self.report)
        path = self.root / "capture/destination.png"
        image = Image.open(path).convert("RGBA")
        rect = report["views"][0]["rect"]
        image.putpixel((int(rect["x"]), int(rect["y"])), (255, 0, 255, 255))
        image.save(path)
        report["screenshot"]["sha256"] = CHECK.digest(path)
        write_json(self.root / "capture/capture.json", report)
        result = self.recheck()
        self.assertFalse(result["pass"])
        self.assertIn("actual screenshot canvas pixels: south@1", result["failures"])

    def test_opaque_or_empty_png_is_not_transparent_visible_art(self):
        path = self.root / "assets/robot/east.png"
        for rgba in ((23, 35, 54, 255), (0, 0, 0, 0)):
            with self.subTest(rgba=rgba):
                Image.new("RGBA", (32, 32), rgba).save(path)
                result = self.recheck()
                self.assertFalse(result["pass"])
                self.assertIn("visible image with transparent background: east", result["failures"])

    def test_wrong_size_and_non_rgba_outputs_fail_the_contract(self):
        path = self.root / "assets/robot/east.png"
        for mode, size in (("RGBA", (31, 32)), ("RGB", (32, 32))):
            with self.subTest(mode=mode, size=size):
                Image.new(mode, size).save(path)
                result = self.recheck()
                self.assertFalse(result["pass"])
                self.assertIn("32x32 RGBA PNG: east", result["failures"])

    def test_repeated_output_is_not_overwritten(self):
        before = (self.root / "capture/capture.json").read_bytes()
        result = self.capture(self.root / "capture")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.root / "capture/capture.json").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
