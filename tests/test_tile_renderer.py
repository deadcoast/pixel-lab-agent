"""Real isolated browser tile checks using explicitly synthetic diagnostic pixels."""
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

from tests.tile_renderer_support import fixture, write_json

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "examples/consumer-execution/tile-neighborhood"
SPEC = importlib.util.spec_from_file_location("tile_renderer_check", RENDERER / "check.py")
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class TileRendererBoundaryTests(unittest.TestCase):
    def test_noncanonical_references_fail(self):
        for name in ("../x", "assets/../x", "assets\\x", "x//y", "/x", "C:/x", ""):
            with self.subTest(name=name), self.assertRaises(ValueError):
                CHECK.confined(ROOT, name)

    def test_missing_capture_is_unavailable(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(CHECK.check(folder, Path(folder) / "missing")["status"], "unavailable")

    @unittest.skipUnless(shutil.which("node"), "Node unavailable")
    def test_missing_browser_retains_inputs_and_cleanup(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            fixture(root)
            result = subprocess.run([shutil.which("node"), str(RENDERER / "capture.mjs"), "--project", str(root), "--config", str(root / "config.json"), "--out", str(root / "capture"), "--browser", str(root / "missing")], capture_output=True, text=True, encoding="utf-8", timeout=15, check=False)
            self.assertNotEqual(result.returncode, 0)
            receipt = json.loads((root / "capture/execution.json").read_text(encoding="utf-8"))
            self.assertFalse(receipt["renderer_executed"])
            self.assertTrue(receipt["cleanup"]["complete"])
            self.assertTrue((root / "capture/inputs.json").is_file())


class TileRendererBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.node = shutil.which("node")
        candidates = [Path("C:/Program Files/Google/Chrome/Application/chrome.exe"), Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"), Path("/usr/bin/chromium"), Path("/usr/bin/google-chrome")]
        cls.browser = next((p for p in candidates if p.is_file()), None)
        if not cls.node or not cls.browser:
            raise unittest.SkipTest("Installed Node/Chromium unavailable")
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.config = fixture(cls.root)
        shutil.copytree(RENDERER, cls.root / "renderer")
        cls.original_inputs = {p.relative_to(cls.root).as_posix(): p.read_bytes() for p in cls.root.rglob("*") if p.is_file()}
        result = cls.capture(cls.root / "capture")
        if result.returncode:
            raise AssertionError("Synthetic tile capture failed: " + result.stdout + result.stderr + (cls.root / "capture/execution.json").read_text(encoding="utf-8"))
        cls.original_capture = {p.name: p.read_bytes() for p in (cls.root / "capture").iterdir() if p.is_file()}
        cls.report = json.loads(cls.original_capture["capture.json"])

    @classmethod
    def capture(cls, out):
        return subprocess.run([cls.node, str(cls.root / "renderer/capture.mjs"), "--project", str(cls.root), "--config", str(cls.root / "config.json"), "--out", str(out), "--browser", str(cls.browser)], capture_output=True, text=True, encoding="utf-8", timeout=100, check=False)

    def setUp(self):
        for name, data in self.original_inputs.items():
            (self.root / name).write_bytes(data)
        for name, data in self.original_capture.items():
            (self.root / "capture" / name).write_bytes(data)
        extra = self.root / "src/new-source.ts"
        if extra.exists():
            extra.unlink()

    def recheck(self):
        return CHECK.check(self.root, self.root / "capture", self.root / "renderer")

    def test_actual_mapping_pixels_screenshots_and_static_facts(self):
        result = self.recheck()
        self.assertTrue(result["pass"], result["failures"])
        self.assertEqual(result["facts"]["pixel_checks"], 4)
        self.assertEqual(result["facts"]["screenshot_checks"], 4)
        self.assertEqual(result["facts"]["clock_checks"], 0)
        self.assertEqual(result["facts"]["phases"], {})
        self.assertEqual({c["tile"] for v in self.report["views"] for c in v["cells"]}, {str(i) for i in range(16)})

    def test_changed_asset_bytes_fail(self):
        path = self.root / "assets/terrain/tile-6.png"
        with Image.open(path) as source:
            changed = source.copy()
        changed.putpixel((0, 0), (255, 0, 255, 255))
        changed.save(path)
        self.assertFalse(self.recheck()["pass"])

    def test_changed_source_closure_fails(self):
        (self.root / "src/new-source.ts").write_text("export const unused = 1;\n", encoding="utf-8")
        self.assertFalse(self.recheck()["pass"])

    def test_tampered_canvas_bytes_fail_even_with_rebound_hash(self):
        report = copy.deepcopy(self.report)
        reference = report["views"][0]["image"]
        path = self.root / "capture" / reference["path"]
        with Image.open(path) as source:
            changed = source.copy()
        changed.putpixel((0, 0), (255, 0, 255, 255))
        changed.save(path)
        reference["sha256"] = CHECK.digest(path)
        write_json(self.root / "capture/capture.json", report)
        self.assertFalse(self.recheck()["pass"])

    def test_tampered_mapping_fails(self):
        report = copy.deepcopy(self.report)
        report["views"][0]["cells"][0]["tile"] = "15"
        write_json(self.root / "capture/capture.json", report)
        self.assertFalse(self.recheck()["pass"])

    def test_omitted_authored_map_cannot_shrink_expected_view_inventory(self):
        report = copy.deepcopy(self.report)
        report["terrain"]["neighborhoods"] = [n for n in report["terrain"]["neighborhoods"] if n["id"] != "island"]
        report["views"] = [view for view in report["views"] if view["neighborhood"] != "island"]
        write_json(self.root / "capture/capture.json", report)
        result = self.recheck()
        self.assertFalse(result["pass"])
        self.assertIn("captured terrain matches separately retained source contract", result["failures"])

    def test_missing_view_fails(self):
        report = copy.deepcopy(self.report)
        report["views"].pop()
        write_json(self.root / "capture/capture.json", report)
        self.assertFalse(self.recheck()["pass"])

    def test_cleanup_uncertainty_fails(self):
        path = self.root / "capture/execution.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value["cleanup"]["browser_closed"] = False
        write_json(path, value)
        self.assertFalse(self.recheck()["pass"])

    def test_capture_collision_preserves_evidence(self):
        before = (self.root / "capture/capture.json").read_bytes()
        result = self.capture(self.root / "capture")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.root / "capture/capture.json").read_bytes(), before)

    def test_wrong_actual_tilefor_fails_in_browser(self):
        path = self.root / "src/terrain.ts"
        path.write_text(path.read_text(encoding="utf-8").replace("return String(corners.reduce((mask, value, bit) => mask + value * 2 ** bit, 0));", "return '0';"), encoding="utf-8")
        result = self.capture(self.root / "wrong-mapping")
        self.assertNotEqual(result.returncode, 0)
        receipt = json.loads((self.root / "wrong-mapping/execution.json").read_text(encoding="utf-8"))
        self.assertTrue(receipt["renderer_executed"])
        self.assertTrue(receipt["cleanup"]["complete"])
        self.assertIn("tileFor mapping differs", receipt["error"])

    def test_missing_tile_fails_in_browser(self):
        (self.root / "assets/terrain/tile-6.png").unlink()
        result = self.capture(self.root / "missing-tile")
        self.assertNotEqual(result.returncode, 0)
        receipt = json.loads((self.root / "missing-tile/execution.json").read_text(encoding="utf-8"))
        self.assertTrue(receipt["cleanup"]["complete"])
        self.assertIn("Missing tile", receipt["error"])

    def test_changed_configuration_fails(self):
        config = copy.deepcopy(self.config)
        config["scales"] = [1, 2]
        write_json(self.root / "config.json", config)
        self.assertFalse(self.recheck()["pass"])

    def test_changed_renderer_fails(self):
        path = self.root / "renderer/view.mjs"
        path.write_text(path.read_text(encoding="utf-8") + "\n// changed renderer\n", encoding="utf-8")
        self.assertFalse(self.recheck()["pass"])

    def test_tampered_screenshot_fails_even_with_rebound_hash(self):
        report = copy.deepcopy(self.report)
        view = report["views"][0]
        reference = view["screenshot"]
        path = self.root / "capture" / reference["path"]
        with Image.open(path) as source:
            changed = source.copy()
        changed.putpixel((int(view["rect"]["x"]), int(view["rect"]["y"])), (255, 0, 255))
        changed.save(path)
        reference["sha256"] = CHECK.digest(path)
        write_json(self.root / "capture/capture.json", report)
        self.assertFalse(self.recheck()["pass"])

    def test_missing_patterns_fail_in_browser(self):
        path = self.root / "src/terrain.ts"
        module = path.read_text(encoding="utf-8")
        declaration, function = module.split(";\nexport function", 1)
        terrain = json.loads(declaration.removeprefix("export const terrain = "))
        terrain["neighborhoods"] = [{"id": "only-water", "label": "Incomplete", "vertices": [[0,0],[0,0]]}]
        path.write_text("export const terrain = " + json.dumps(terrain) + ";\nexport function" + function, encoding="utf-8")
        result = self.capture(self.root / "missing-patterns")
        self.assertNotEqual(result.returncode, 0)
        receipt = json.loads((self.root / "missing-patterns/execution.json").read_text(encoding="utf-8"))
        self.assertTrue(receipt["cleanup"]["complete"])
        self.assertIn("every binary corner pattern", receipt["error"])

    def test_bridge_binds_family_and_static_views(self):
        spec = importlib.util.spec_from_file_location("tile_observation", self.root / "renderer/observation.py")
        bridge = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bridge)
        members = [{"output": output, "candidate": "candidate-" + str(i), "sha256": CHECK.digest(self.root / path)} for i, (output, path) in enumerate(self.config["destinations"].items())]
        manifest = {"candidate": "terrain-family", "files": members}
        write_json(self.root / "manifest.json", manifest)
        context = {"candidate": "terrain-family", "binding_hash": "a" * 64, "candidate_file": {"path": "manifest.json", "sha256": CHECK.digest(self.root / "manifest.json")}, "members": [{**row, "lineage": {"display": "presentation-only"}} for row in members]}
        write_json(self.root / "context.json", context)
        write_json(self.root / "destinations.json", self.config["destinations"])
        observed = bridge.build(self.root, self.root / "capture", self.root / "context.json", self.root / "renderer", self.root / "destinations.json")
        self.assertEqual(observed["motion"], [])
        self.assertEqual(len(observed["views"]), 4)
        self.assertEqual(set(observed["views"][0]["member_outputs"]), set(self.config["destinations"]))
        self.assertEqual(len(observed["destinations"]), 16)
        self.assertEqual(len(observed["renderer"]["files"]), 6)
        self.assertTrue(all(row["sha256"] == CHECK.digest(self.root / row["path"]) for row in observed["files"]))
        context["members"][0]["candidate"] = "wrong-member"
        write_json(self.root / "context.json", context)
        with self.assertRaisesRegex(ValueError, "exact manifest disagree"):
            bridge.build(self.root, self.root / "capture", self.root / "context.json", self.root / "renderer", self.root / "destinations.json")


if __name__ == "__main__":
    unittest.main()
