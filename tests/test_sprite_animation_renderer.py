"""Actual isolated browser and independent sprite timing/pixel checks."""
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

from tests.sprite_animation_support import fixture, write_json

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "examples/consumer-execution/sprite-animation"
SPEC = importlib.util.spec_from_file_location("sprite_animation_check", RENDERER / "check.py")
assert SPEC and SPEC.loader
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class SpriteAnimationBoundaries(unittest.TestCase):
    def test_noncanonical_references_fail(self):
        for name in ("../outside.png", "assets/../x.png", "assets\\x.png", "a//b", "/absolute", "C:/outside", ""):
            with self.subTest(name=name), self.assertRaises(ValueError):
                CHECK.confined(ROOT, name)

    def test_absent_observation_cannot_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertFalse(CHECK.check(folder, Path(folder)/"missing")["pass"])


class SpriteAnimationBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.node = shutil.which("node")
        cls.browser = next((p for p in [Path("C:/Program Files/Google/Chrome/Application/chrome.exe"), Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"), Path("/usr/bin/chromium"), Path("/usr/bin/google-chrome")] if p.is_file()), None)
        if not cls.node or not cls.browser:
            raise unittest.SkipTest("Installed local Node/Chromium unavailable")
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.config = fixture(cls.root)
        shutil.copytree(RENDERER, cls.root / "renderer")
        cls.original_inputs = {p.relative_to(cls.root).as_posix():p.read_bytes() for folder in ("src", "assets", "renderer") for p in (cls.root/folder).rglob("*") if p.is_file()}
        cls.original_inputs["config.json"] = (cls.root / "config.json").read_bytes()
        result = cls.capture(cls.root / "capture")
        if result.returncode:
            raise AssertionError("Synthetic animation capture failed: " + result.stdout + result.stderr)
        cls.original_capture = {p.name:p.read_bytes() for p in (cls.root / "capture").iterdir() if p.is_file()}
        cls.report = json.loads(cls.original_capture["capture.json"])

    @classmethod
    def capture(cls, out):
        return subprocess.run([cls.node,str(cls.root/"renderer/capture.mjs"),"--project",str(cls.root),"--config",str(cls.root/"config.json"),"--out",str(out),"--browser",str(cls.browser)],capture_output=True,text=True,encoding="utf-8",timeout=100,check=False)

    def setUp(self):
        for name, data in self.original_inputs.items():
            (self.root/name).write_bytes(data)
        for name, data in self.original_capture.items():
            (self.root/"capture"/name).write_bytes(data)

    def recheck(self, capture=None):
        return CHECK.check(self.root,capture or self.root/"capture",self.root/"renderer")

    def test_real_loop_and_one_shot_pixels_and_clocks(self):
        result = self.recheck()
        self.assertTrue(result["pass"],result["failures"])
        self.assertEqual(len(self.report["views"]),16)
        self.assertEqual(len(self.report["playbacks"]),4)
        self.assertGreater(result["facts"]["clock_checks"],100)
        counts=result["facts"]["phases"]["playback"]["counts"]
        self.assertEqual(counts["loop@1x"]["wraps"],2)
        self.assertEqual(counts["once@3x"]["wraps"],0)
        for row in counts.values():
            self.assertEqual(row["frames"],[0,1,2,3])
            self.assertEqual(row["skips"],0)

    def test_changed_asset_or_source_cannot_reuse_capture(self):
        for name in ("assets/motion/frame-0.png","src/animation.ts"):
            with self.subTest(name=name):
                before=(self.root/name).read_bytes()
                (self.root/name).write_bytes(before+b"changed")
                result=self.recheck()
                self.assertFalse(result["pass"])
                self.assertIn("exact consumer input: "+name,result["failures"])
                (self.root/name).write_bytes(before)

    def test_wrong_actual_frame_at_is_rejected(self):
        source=self.root/"src/animation.ts"
        source.write_text(source.read_text(encoding="utf-8").replace("let at = clip.loop ?", "elapsedMs *= 2; let at = clip.loop ?"),encoding="utf-8")
        out=self.root/"wrong-clock"
        self.capture(out)
        result=self.recheck(out)
        self.assertFalse(result["pass"])
        self.assertIn("authored uneven-duration frameAt",result["failures"])

    def test_out_of_bounds_crop_retains_failure(self):
        source=self.root/"src/animation.ts"
        source.write_text(source.read_text(encoding="utf-8").replace('"rect": [\n            2,','"rect": [\n            99,',1),encoding="utf-8")
        out=self.root/"bad-crop"
        result=self.capture(out)
        self.assertNotEqual(result.returncode,0)
        receipt=json.loads((out/"execution.json").read_bytes())
        self.assertTrue(receipt["cleanup"]["complete"])
        self.assertFalse(self.recheck(out)["pass"])

    def test_rebound_pixel_tamper_and_screenshot_mismatch_fail(self):
        report=copy.deepcopy(self.report)
        view=report["views"][0]
        path=self.root/"capture"/view["image"]["path"]
        with Image.open(path) as raw:
            changed=raw.convert("RGBA")
        changed.putpixel((0,0),(255,0,255,255));changed.save(path)
        view["image"]["sha256"]=CHECK.digest(path)
        write_json(self.root/"capture/capture.json",report)
        result=self.recheck()
        self.assertFalse(result["pass"])
        self.assertIn("actual crop/anchor/nearest pixels: loop@1/0",result["failures"])
        self.assertIn("actual screenshot pixels: loop@1/0",result["failures"])

    def test_pivot_geometry_cannot_be_relabelled(self):
        report=copy.deepcopy(self.report)
        report["views"][0]["pivot"][1]-=2
        write_json(self.root/"capture/capture.json",report)
        result=self.recheck()
        self.assertFalse(result["pass"])
        self.assertIn("authored placement: loop@1/0",result["failures"])

    def test_capture_timing_tamper_fails(self):
        report=copy.deepcopy(self.report)
        report["playbacks"][0]["ticks"][1]["elapsed_ms"]=0
        write_json(self.root/"capture/capture.json",report)
        self.assertIn("strict actual RAF clock",self.recheck()["failures"])

    def test_actual_wrong_pivot_painting_fails_independent_composition(self):
        source=self.root/"renderer/view.mjs"
        source.write_text(source.read_text(encoding="utf-8").replace("(clip.anchor[1]-f.pivot[1])*s", "(clip.anchor[1]-f.pivot[1]+2)*s"),encoding="utf-8")
        out=self.root/"wrong-pivot-paint"
        result=self.capture(out)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        checked=self.recheck(out)
        self.assertFalse(checked["pass"])
        self.assertIn("actual crop/anchor/nearest pixels: loop@1/0",checked["failures"])

    def test_each_cleanup_subflag_must_confirm_completion(self):
        for flag in ("browser_closed", "server_closed", "profile_removed"):
            with self.subTest(flag=flag):
                execution=json.loads(self.original_capture["execution.json"])
                execution["cleanup"][flag]=False
                write_json(self.root/"capture/execution.json",execution)
                self.assertIn("owned browser/server/profile cleanup",self.recheck()["failures"])

    def test_required_served_display_resources_cannot_be_omitted(self):
        for key in ("renderer/index.html", "renderer/view.mjs"):
            with self.subTest(key=key):
                report=copy.deepcopy(self.report)
                del report["served_files"][key]
                write_json(self.root/"capture/capture.json",report)
                self.assertIn("actual renderer display resources served",self.recheck()["failures"])

    def test_authored_clip_cannot_be_removed_from_capture_inventory(self):
        report=copy.deepcopy(self.report)
        report["animation"]["clips"]=[c for c in report["animation"]["clips"] if c["id"]!="once"]
        report["views"]=[v for v in report["views"] if v["clip"]!="once"]
        report["playbacks"]=[p for p in report["playbacks"] if p["clip"]!="once"]
        write_json(self.root/"capture/capture.json",report)
        self.assertIn("captured source contract/config unchanged",self.recheck()["failures"])

    def test_output_collision_preserves_receipts(self):
        before=(self.root/"capture/execution.json").read_bytes()
        result=self.capture(self.root/"capture")
        self.assertNotEqual(result.returncode,0)
        self.assertEqual((self.root/"capture/execution.json").read_bytes(),before)

    def test_missing_browser_retains_unavailable_owned_cleanup(self):
        out=self.root/"no-browser"
        result=subprocess.run([self.node,str(self.root/"renderer/capture.mjs"),"--project",str(self.root),"--config",str(self.root/"config.json"),"--out",str(out),"--browser",str(self.root/"absent-browser")],capture_output=True,text=True,encoding="utf-8",timeout=10,check=False)
        self.assertNotEqual(result.returncode,0)
        receipt=json.loads((out/"execution.json").read_bytes())
        self.assertEqual(receipt["status"],"unavailable")
        self.assertFalse(receipt["renderer_executed"])
        self.assertTrue(receipt["cleanup"]["complete"])


if __name__ == "__main__":
    unittest.main()
