"""Reusable queue renderer: observed counting, real browser pixels and failure retention."""
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

ROOT=Path(__file__).resolve().parents[1]
RENDERER=ROOT / "examples/consumer-execution/queue-motion"
SPEC=importlib.util.spec_from_file_location("consumer_motion_check",RENDERER / "check.py")
assert SPEC and SPEC.loader
CHECK=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


def config():
    return {"version":1,"profile":"queue-motion-v1","modules":{"state":"src/state.mjs","view":"src/view.mjs"},"destinations":{},"scales":[1,2],"observed_wraps":2,"phase_timeout_ms":3000,"hold_ms":150,"timeout_seconds":30}


def write_json(path,value):
    path.write_text(json.dumps(value),encoding="utf-8")


class ConsumerRendererCountingTests(unittest.TestCase):
    def test_counts_only_actual_adjacent_wraps(self):
        result=CHECK.count_frames([0,0,1,1,2,2,0,1,2,0],3)
        self.assertEqual(result,{"frames":[0,1,2],"transitions":6,"wraps":2,"skips":0,"last":0})

    def test_skips_never_establish_complete_coverage(self):
        result=CHECK.count_frames([0,2,0,2,0],3)
        self.assertEqual(result["skips"],2)
        self.assertEqual(result["frames"],[0,2])

    def test_held_source_frame_does_not_invent_elapsed_wraps(self):
        self.assertEqual(CHECK.count_frames([2]*100,3)["wraps"],0)

    def test_invalid_frame_is_rejected(self):
        for frame in (-1,3,True,1.5):
            with self.subTest(frame=frame),self.assertRaises(ValueError):
                CHECK.count_frames([frame],3)

    def test_reference_cannot_escape_or_use_noncanonical_path(self):
        for name in ("../outside.png","src/../asset.png","assets\\x.png","/absolute.png","a//b.png"):
            with self.subTest(name=name),self.assertRaises(ValueError):
                CHECK.confined(ROOT,name)

    @unittest.skipUnless(shutil.which("node"),"Node unavailable")
    def test_closed_config_bounds_and_no_extra_chrome_arguments(self):
        node=shutil.which("node")
        script="import {validateConfig} from " + json.dumps((RENDERER / "server.mjs").as_uri()) + "; const c=JSON.parse(process.argv[1]);try{validateConfig(c);process.exit(0)}catch{process.exit(1)}"
        good=config()
        self.assertEqual(subprocess.run([node,"--input-type=module","-e",script,json.dumps(good)],capture_output=True,timeout=5,check=False).returncode,0)
        mutations=[("scales",[0]),("scales",[1,1]),("scales",[1,2,3,4,5]),("observed_wraps",0),("phase_timeout_ms",999),("hold_ms",99),("timeout_seconds",181),("chrome_flags",["--user-data-dir=private"]),("modules",{"state":"../private.js","view":"src/view.ts"})]
        for key,value in mutations:
            with self.subTest(key=key,value=value):
                bad={**good,key:value}
                self.assertNotEqual(subprocess.run([node,"--input-type=module","-e",script,json.dumps(bad)],capture_output=True,timeout=5,check=False).returncode,0)

    @unittest.skipUnless(shutil.which("node"),"Node unavailable")
    def test_missing_browser_retains_unavailable_cleanup_receipt(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);write_json(root / "config.json",config())
            result=subprocess.run([shutil.which("node"),str(RENDERER / "capture.mjs"),"--project",str(root),"--out",str(root / "capture"),"--config",str(root / "config.json"),"--browser",str(root / "missing-browser")],capture_output=True,text=True,timeout=10,check=False)
            self.assertNotEqual(result.returncode,0)
            receipt=json.loads((root / "capture/execution.json").read_bytes())
            self.assertEqual(receipt["status"],"unavailable")
            self.assertFalse(receipt["renderer_executed"])
            self.assertTrue(receipt["cleanup"]["complete"])
            self.assertFalse((root / "capture/capture.json").exists())


class ConsumerRendererBrowserTests(unittest.TestCase):
    """One isolated local browser run supplies independent tampering test inputs."""
    @classmethod
    def setUpClass(cls):
        cls.node=shutil.which("node")
        candidates=[Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),Path("/usr/bin/chromium"),Path("/usr/bin/google-chrome")]
        cls.browser=next((p for p in candidates if p.is_file()),None)
        if not cls.node or not cls.browser:
            raise unittest.SkipTest("Installed local Node/Chromium unavailable")
        cls.temp=tempfile.TemporaryDirectory();cls.addClassCleanup(cls.temp.cleanup)
        cls.root=Path(cls.temp.name);(cls.root / "src").mkdir();(cls.root / "assets").mkdir()
        shutil.copytree(RENDERER,cls.root / "renderer")
        (cls.root / "src/state.mjs").write_text('export function stateAfter(event){return {started:"running",pause:"paused",ok:"succeeded",error:"failed"}[event]}',encoding="utf-8")
        # Deliberately three frames, 80 ms timing and held frame 2: never fixture constants.
        (cls.root / "src/view.mjs").write_text('''export const display={cell:[2,2],scale:2,filter:"nearest",frameMs:80,background:"#102030"};
export const reducedMotionQuery="(prefers-reduced-motion: reduce)";
export const statusVisuals=Object.fromEntries(["idle","running","paused","succeeded","failed"].map(s=>[s,{label:s,path:s==="running"?"assets/work.png":"assets/static.png",frames:s==="running"?3:1,still:s==="running"?2:0}]));
export const motionPreference=q=>q.matches?"reduced":"normal";
export function statusCell(s,m){const v=statusVisuals[s],animate=m==="normal"&&v.frames>1;return {...v,motion:m,animate,holdFrame:animate?null:v.still}}
export const compactStatus=statusCell;
export const frameAt=(d,e)=>d.animate?Math.floor(Math.max(0,e)/display.frameMs)%d.frames:d.holdFrame;
''',encoding="utf-8")
        sheet=Image.new("RGBA",(6,2));sheet.paste((255,0,0,255),(0,0,2,2));sheet.paste((0,255,0,255),(2,0,4,2));sheet.paste((0,0,255,255),(4,0,6,2));sheet.save(cls.root / "assets/work.png")
        Image.new("RGBA",(2,2),(255,255,0,200)).save(cls.root / "assets/static.png")
        write_json(cls.root / "config.json",config())
        result=subprocess.run([cls.node,str(cls.root / "renderer/capture.mjs"),"--project",str(cls.root),"--out",str(cls.root / "capture"),"--config",str(cls.root / "config.json"),"--browser",str(cls.browser)],capture_output=True,text=True,timeout=40,check=False)
        if result.returncode:
            raise AssertionError("Local isolated capture failed: "+result.stdout+result.stderr)
        cls.report=json.loads((cls.root / "capture/capture.json").read_bytes())
        cls.launch=(cls.root / "capture/launch.json").read_bytes()
        cls.execution=(cls.root / "capture/execution.json").read_bytes()

    def setUp(self):
        write_json(self.root / "capture/capture.json",copy.deepcopy(self.report))
        (self.root / "capture/launch.json").write_bytes(self.launch)
        (self.root / "capture/execution.json").write_bytes(self.execution)

    def recheck(self):
        return CHECK.check(self.root,self.root / "capture",self.root / "renderer")

    def altered(self,change):
        report=copy.deepcopy(self.report);change(report);write_json(self.root / "capture/capture.json",report)
        result=self.recheck();self.assertFalse(result["pass"]);return result

    def test_actual_source_timing_held_frame_scales_and_same_page_switches(self):
        result=self.recheck();self.assertTrue(result["pass"],result["failures"])
        for phase in ("normal-start","normal-restored"):
            for count in result["facts"]["phases"][phase]["counts"].values():
                self.assertEqual(count["wraps"],2);self.assertEqual(count["skips"],0);self.assertEqual(count["frames"],[0,1,2])
        for phase in ("reduced","initially-reduced"):
            for count in result["facts"]["phases"][phase]["counts"].values():
                self.assertEqual(count["frames"],[2]);self.assertEqual(count["wraps"],0)
        self.assertEqual([p["name"] for p in self.report["phases"]],list(CHECK.PHASES))
        self.assertTrue(json.loads(self.execution)["cleanup"]["complete"])

    def test_capture_clock_cannot_replace_paint_clock(self):
        def mutate(r):
            c=r["phases"][0]["samples"][1]["cells"][0]
            c["paintElapsed"]+=80
        self.assertTrue(any("painted frame uses paint clock" in f for f in self.altered(mutate)["failures"]))

    def test_skipped_frame_and_forged_wrap_counts_fail(self):
        def mutate(r):
            del r["phases"][0]["samples"][1]
        self.assertTrue(any("independently counted" in f for f in self.altered(mutate)["failures"]))

    def test_elapsed_time_without_observed_wraps_fails(self):
        def mutate(r):
            p=r["phases"][0];p["samples"]=p["samples"][:2];p["endedAt"]+=1000
        self.assertTrue(any("actual consecutive coverage" in f for f in self.altered(mutate)["failures"]))

    def test_missing_consumer_scale_is_not_inferred(self):
        self.altered(lambda r:r["phases"][0]["samples"][0]["cells"].pop())

    def test_missing_entire_state_view_is_rejected(self):
        self.altered(lambda r:r.update(views=[v for v in r["views"] if v["state"] != "paused"]))

    def test_unavailable_still_image_cannot_pass(self):
        result=self.altered(lambda r:r["views"][0].pop("image"))
        self.assertEqual(result["status"],"unavailable")

    def test_missing_phase_and_reloaded_switch_are_rejected(self):
        self.altered(lambda r:r["phases"].pop())
        self.altered(lambda r:r["phases"][1].update(sessionId="different-page"))

    def test_removed_preference_reconciliation_is_rejected(self):
        self.altered(lambda r:r["phases"][1]["reconciliations"].clear())

    def test_source_byte_tampering_is_rejected(self):
        path=self.root / "src/view.mjs";before=path.read_bytes()
        try:
            path.write_bytes(before+b"\n// changed after capture\n")
            self.assertTrue(any("served bytes" in f for f in self.recheck()["failures"]))
        finally:
            path.write_bytes(before)

    def test_png_tampering_is_rejected(self):
        reference=self.report["phases"][0]["samples"][0]["cells"][0]["image"]
        path=self.root / "capture" / reference["path"];before=path.read_bytes()
        try:
            Image.new("RGBA",(2,2),(0,0,0,255)).save(path)
            self.assertTrue(any("retained PNG bytes" in f for f in self.recheck()["failures"]))
        finally:
            path.write_bytes(before)

    def test_cleanup_failure_never_passes(self):
        value=json.loads(self.execution);value["cleanup"]["complete"]=False
        write_json(self.root / "capture/execution.json",value)
        self.assertFalse(self.recheck()["pass"])

    def test_bounded_timeout_retains_partial_samples_and_cleanup(self):
        settings={**config(),"observed_wraps":10,"phase_timeout_ms":1000}
        write_json(self.root / "timeout-config.json",settings)
        result=subprocess.run([self.node,str(self.root / "renderer/capture.mjs"),"--project",str(self.root),"--out",str(self.root / "timeout-capture"),"--config",str(self.root / "timeout-config.json"),"--browser",str(self.browser)],capture_output=True,text=True,timeout=15,check=False)
        self.assertNotEqual(result.returncode,0)
        execution=json.loads((self.root / "timeout-capture/execution.json").read_bytes())
        report=json.loads((self.root / "timeout-capture/capture.json").read_bytes())
        self.assertEqual(execution["status"],"timeout");self.assertTrue(execution["cleanup"]["complete"])
        self.assertEqual(report["phases"][0]["status"],"timeout")
        self.assertTrue(report["phases"][0]["samples"])
        self.assertLess(report["phases"][0]["counts"]["statusCell@1"]["wraps"],10)

    def test_missing_source_capability_is_unavailable(self):
        source=self.root / "src/view.mjs";before=source.read_bytes()
        try:
            source.write_bytes(before.replace(b"export const frameAt=",b"export const unrelated="))
            result=subprocess.run([self.node,str(self.root / "renderer/capture.mjs"),"--project",str(self.root),"--out",str(self.root / "unsupported-capture"),"--config",str(self.root / "config.json"),"--browser",str(self.browser)],capture_output=True,text=True,timeout=15,check=False)
            self.assertNotEqual(result.returncode,0)
            execution=json.loads((self.root / "unsupported-capture/execution.json").read_bytes())
            self.assertEqual(execution["status"],"unavailable");self.assertIn("frameAt",execution["error"])
            self.assertTrue(execution["renderer_executed"]);self.assertTrue(execution["cleanup"]["complete"])
        finally:
            source.write_bytes(before)


if __name__ == "__main__":
    unittest.main()
