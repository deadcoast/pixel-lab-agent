"""Consumer rendering boundaries and independently rechecked pixel evidence."""

import importlib.util
import json
import shutil
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.error import HTTPError
from urllib.request import urlopen

from PIL import Image

from evaluations.plar_family_case import setup
from evaluations.plar_render_recheck_case import setup as recheck_setup

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "examples/plar-project/renderer"
SPEC = importlib.util.spec_from_file_location("queue_render_check", RENDERER / "check.py")
assert SPEC and SPEC.loader
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class QueueRendererTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_server_uses_real_modules_and_confines_resources(self):
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node unavailable")
        shutil.copytree(ROOT / "examples/plar-project/src", self.root / "src")
        (self.root / "private.txt").write_text("not a consumer resource", encoding="utf-8")
        process = subprocess.Popen(
            [node, str(RENDERER / "server.mjs"), "--project", str(self.root)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        try:
            assert process.stdout
            launch = json.loads(process.stdout.readline())
            with urlopen(launch["url"] + "/src/queue.ts", timeout=5) as response:
                self.assertIn(b"return { started:", response.read())
            source = self.root / "src/queue.ts"
            source.write_text(source.read_text().replace('ok: "succeeded"', 'ok: "failed"'), encoding="utf-8")
            with urlopen(launch["url"] + "/src/queue.ts", timeout=5) as response:
                self.assertIn(b'ok: "failed"', response.read())
            for path in ("/private.txt", "/assets/missing.png", "/src/%2e%2e/private.txt"):
                with self.assertRaises(HTTPError) as caught:
                    urlopen(launch["url"] + path, timeout=5)
                caught.exception.close()
        finally:
            process.terminate()
            process.communicate(timeout=10)

    def test_style_stage_preserves_consumer_and_copies_executable_sources_only(self):
        project, destination, predecessor = (self.root / name for name in ("project", "attempt", "previous"))
        for folder in (project, destination, predecessor):
            folder.mkdir()
        (predecessor / "provider-state.json").write_text('{"jobs":[]}\n', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "completed handoff"):
            setup(project, destination, None, predecessor)
        (project / "HANDOFF-RESULT.json").write_text('{"historical":true}\n', encoding="utf-8")
        (project / "PHASE.md").write_text("Earlier scoped assignment\n", encoding="utf-8")
        before = {p.name: p.read_bytes() for p in project.iterdir()}
        setup(project, destination, None, predecessor)
        for name, data in before.items():
            self.assertEqual((project / name).read_bytes(), data)
        self.assertEqual((destination / "provider-state.json").read_bytes(), (predecessor / "provider-state.json").read_bytes())
        self.assertEqual({p.name for p in (project / "renderer").iterdir()}, {"server.mjs", "capture.mjs", "view.mjs", "index.html", "check.py"})
        self.assertTrue((project / "RENDER-STAGE.md").is_file())

    def test_renderer_recheck_keeps_old_implementation_and_result(self):
        project, destination, predecessor = (self.root / name for name in ("project", "attempt", "previous"))
        for folder in (project, destination, predecessor):
            folder.mkdir()
        (predecessor / "provider-state.json").write_text('{"jobs":[]}\n', encoding="utf-8")
        (project / "FAMILY-RESULT.json").write_text('{"render":"failed"}\n', encoding="utf-8")
        (project / "RENDER-STAGE.md").write_text("Original family assignment\n", encoding="utf-8")
        (project / "renderer").mkdir()
        old = project / "renderer/capture.mjs"
        old.write_text("// Retained old implementation\n", encoding="utf-8")
        recheck_setup(project, destination, None, predecessor)
        self.assertEqual(old.read_text(), "// Retained old implementation\n")
        self.assertEqual(json.loads((project / "FAMILY-RESULT.json").read_text()), {"render": "failed"})
        self.assertEqual((project / "renderer-recheck/capture.mjs").read_bytes(), (RENDERER / "capture.mjs").read_bytes())
        self.assertTrue((project / "RENDER-RECHECK.md").is_file())

    def test_interrupted_family_recheck_keeps_drafts_without_inventing_a_decision(self):
        project, destination, predecessor = (self.root / name for name in ("project", "attempt", "previous"))
        for folder in (project, destination, predecessor):
            folder.mkdir()
        (predecessor / "provider-state.json").write_text('{"jobs":[]}\n', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "retained family assignment"):
            recheck_setup(project, destination, None, predecessor)
        (project / "RENDER-STAGE.md").write_text("Original family assignment\n", encoding="utf-8")
        draft = project / "review-draft.json"
        draft.write_text('{"decision":"unresolved"}\n', encoding="utf-8")
        recheck_setup(project, destination, None, predecessor)
        self.assertEqual(draft.read_text(), '{"decision":"unresolved"}\n')
        self.assertFalse((project / "FAMILY-RESULT.json").exists())
        self.assertIn("Interrupted original delivery", (project / "RENDER-RECHECK.md").read_text())

    def pixel_fixture(self):
        project, capture = self.root / "project", self.root / "capture"
        (project / "assets").mkdir(parents=True)
        capture.mkdir()
        image = Image.new("RGBA", (2, 2), (0, 0, 0, 0))
        image.putpixel((0, 0), (112, 185, 237, 255))
        image.save(project / "assets/ready.png")
        panel = Image.alpha_composite(Image.new("RGBA", (2, 2), (23, 35, 54, 255)), image)
        panel.save(capture / "view.png")
        panel.save(capture / "destination.png")
        report = {
            "errors": [], "devicePixelRatio": 1, "served_files": {}, "missing": [], "timeline": [],
            "display": {"cell": [2, 2], "background": "#172336"},
            "screenshot": {"path": "destination.png", "sha256": CHECK.digest(capture / "destination.png")},
            "views": [{"consumer": "statusCell", "state": "succeeded", "scale": 1, "frame": 0,
                       "asset": {"available": True, "sha256": CHECK.digest(project / "assets/ready.png")},
                       "descriptor": {"path": "assets/ready.png", "frames": 1}, "geometryMatches": True,
                       "smoothing": False, "imageRendering": "pixelated",
                       "bounds": {"x": 0, "y": 0, "width": 2, "height": 2},
                       "image": {"path": "view.png", "sha256": CHECK.digest(capture / "view.png")}}],
        }
        (capture / "render.json").write_text(json.dumps(report), encoding="utf-8")
        return project, capture, report

    def test_rehashed_rgb_difference_cannot_hide_behind_opaque_alpha(self):
        project, capture, report = self.pixel_fixture()
        self.assertEqual(CHECK.check(project, capture)["status"], "pass")
        with Image.open(capture / "destination.png") as source:
            changed = source.copy()
        changed.putpixel((0, 0), (0, 0, 0, 255))
        changed.save(capture / "destination.png")
        report["screenshot"]["sha256"] = CHECK.digest(capture / "destination.png")
        (capture / "render.json").write_text(json.dumps(report), encoding="utf-8")
        result = CHECK.check(project, capture)
        self.assertEqual(result["status"], "fail")
        self.assertTrue(any("screenshot matches canvas" in failure for failure in result["failures"]))

    def playback_fixture(self):
        project, capture, report = self.pixel_fixture()
        report['display']['frameMs'] = 100
        sheet = Image.new('RGBA', (8, 2))
        for frame, color in enumerate(('#70b9ed', '#4488aa', '#225577', '#99ccff')):
            sheet.paste(Image.new('RGBA', (2, 2), color), (frame * 2, 0))
        sheet.save(project / 'assets/working.png')
        samples = []
        for step in range(13):
            frame = step % 4
            path = capture / f'live-{step}.png'
            sheet.crop((frame * 2, 0, (frame + 1) * 2, 2)).save(path)
            cells = [{'consumer': consumer, 'descriptor': {'path': 'assets/working.png', 'frames': 4}, 'frame': frame, 'scale': 1, 'sha256': CHECK.digest(project / 'assets/working.png'), 'image': {'path': path.name, 'sha256': CHECK.digest(path)}} for consumer in ('statusCell', 'compactStatus')]
            samples.append({'elapsed': step * 100 + 5, 'cells': cells})
        report['playback'] = {'status': 'observed', 'frameMs': 100, 'frameCount': 4, 'samples': samples}
        (capture / 'render.json').write_text(json.dumps(report), encoding='utf-8')
        self.assertEqual(CHECK.check(project, capture)['status'], 'pass')
        return project, capture, report

    def test_live_playback_rejects_clock_frame_mismatch_and_skipped_frames(self):
        project, capture, report = self.playback_fixture()
        report['playback']['samples'][1]['elapsed'] = 205
        (capture / 'render.json').write_text(json.dumps(report), encoding='utf-8')
        result = CHECK.check(project, capture)
        self.assertIn('live frame follows actual clock', result['failures'])
        self.assertIn('live playback observes consecutive frames without skips', result['failures'])

    def test_live_playback_rejects_changed_pixels_even_with_updated_capture_hash(self):
        project, capture, report = self.playback_fixture()
        image = Image.new('RGBA', (2, 2), 'red')
        image.save(capture / 'live-1.png')
        for cell in report['playback']['samples'][1]['cells']:
            cell['image']['sha256'] = CHECK.digest(capture / 'live-1.png')
        (capture / 'render.json').write_text(json.dumps(report), encoding='utf-8')
        self.assertIn('live painted frame matches source and nearest scale', CHECK.check(project, capture)['failures'])

    def test_changed_source_and_fractional_destination_are_not_accepted(self):
        project, capture, report = self.pixel_fixture()
        report["views"][0]["bounds"]["x"] = 0.5
        (capture / "render.json").write_text(json.dumps(report), encoding="utf-8")
        with Image.open(project / "assets/ready.png") as source:
            changed = source.copy()
        changed.putpixel((1, 1), (255, 0, 0, 255))
        changed.save(project / "assets/ready.png")
        result = CHECK.check(project, capture)
        self.assertEqual(result["status"], "fail")
        self.assertTrue(any("integer destination bounds" in failure for failure in result["failures"]))
        self.assertTrue(any("actual asset identity" in failure for failure in result["failures"]))
        self.assertTrue(any("alpha compositing" in failure for failure in result["failures"]))


if __name__ == "__main__":
    unittest.main()
