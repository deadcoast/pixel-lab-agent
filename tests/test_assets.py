import unittest
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PIL import Image

from pixl import assets
from pixl.codec import PixlError


class AssetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "sprite.png"

    def test_reports_exact_dimensions_palette_alpha_and_components(self):
        image = Image.new("RGBA", (3, 2), (0, 0, 0, 0))
        image.putpixel((0, 0), (255, 0, 0, 255))
        image.putpixel((1, 0), (255, 0, 0, 255))
        image.putpixel((2, 1), (0, 0, 255, 255))
        image.save(self.path)
        result = assets.inspect(
            self.path, width=3, height=2, palette=["#ff0000", "#0000ff"]
        )
        self.assertTrue(result["pass"])
        self.assertEqual(result["frames"][0]["opaque_components"], 2)
        self.assertEqual(result["frames"][0]["visible_pixels"], 3)
        self.assertFalse(result["visual_quality_verified"])

    def test_mismatched_palette_and_fractional_alpha_are_failures(self):
        Image.new("RGBA", (2, 2), (128, 20, 70, 127)).save(self.path)
        result = assets.inspect(self.path, width=3, height=2, palette=["#ffffff"])
        self.assertFalse(result["pass"])
        self.assertEqual(set(result["failures"]), {"dimensions", "palette", "alpha"})

    def test_full_alpha_contract_accepts_translucent_art(self):
        Image.new("RGBA", (2, 2), (128, 20, 70, 127)).save(self.path)
        result = assets.inspect(self.path, alpha="full")
        self.assertTrue(result["pass"])

    def test_all_animation_frames_inspected(self):
        path = self.path.with_suffix(".gif")
        frames = [Image.new("RGB", (2, 2), color) for color in ("red", "blue")]
        frames[0].save(
            path, save_all=True, append_images=frames[1:], duration=[100, 200], loop=0
        )
        result = assets.inspect(path, palette=["#ff0000"])
        self.assertEqual(result["frame_count"], 2)
        self.assertEqual([f["duration_ms"] for f in result["frames"]], [100, 200])
        self.assertFalse(result["pass"])

    def test_invalid_file_has_structured_error(self):
        self.path.write_text("not image")
        with self.assertRaises(PixlError):
            assets.inspect(self.path)

    def test_concurrent_export_cannot_bind_old_measurements_to_new_bytes(self):
        Image.new("RGBA", (8, 8), "red").save(self.path)
        expected = sha256(self.path.read_bytes()).hexdigest()
        original_components = assets.components

        def export_during_measurement(points):
            Image.new("RGBA", (8, 8), "blue").save(self.path)
            return original_components(points)

        with patch.object(assets, "components", export_during_measurement):
            measured = assets.inspect(self.path, palette=["#ff0000"])
        self.assertTrue(measured["pass"])
        self.assertEqual(measured["sha256"], expected)
        self.assertFalse(assets.inspect(self.path, palette=["#ff0000"])["pass"])

    def test_reference_color_regions_measure_actual_coordinates(self):
        reference = Path("evidence/host-evaluation/fixture-inputs/reference.png")
        result = assets.inspect(reference, regions=["#F4DDA2", "#ff00ff"])
        yellow, absent = result["frames"][0]["color_regions"]
        self.assertEqual(yellow["boxes"], [[11, 14, 14, 18], [18, 14, 21, 18]])
        self.assertEqual(yellow["pixels"], 24)
        self.assertEqual(yellow["component_count"], 2)
        self.assertFalse(yellow["boxes_truncated"])
        self.assertEqual(absent["boxes"], [])
        self.assertTrue(result["pass"])
        self.assertFalse(result["visual_quality_verified"])

    def test_regions_are_snapshot_bound_and_do_not_enforce_palette(self):
        Image.new("RGBA", (8, 8), "red").save(self.path)
        original = assets.components
        expected = sha256(self.path.read_bytes()).hexdigest()

        def replace(points):
            Image.new("RGBA", (8, 8), "blue").save(self.path)
            return original(points)

        with patch.object(assets, "components", replace):
            result = assets.inspect(self.path, regions=["red", "blue"])
        self.assertEqual(result["sha256"], expected)
        self.assertEqual(
            [r["pixels"] for r in result["frames"][0]["color_regions"]], [64, 0]
        )
        self.assertTrue(result["pass"])

    def test_regions_bound_report_size_and_validate_queries(self):
        image = Image.new("RGBA", (40, 40))
        for y in range(0, 40, 2):
            for x in range(0, 40, 2):
                image.putpixel((x, y), (255, 0, 0, 128))
        image.save(self.path)
        result = assets.inspect(self.path, alpha="full", regions=["#ff000080"])
        region = result["frames"][0]["color_regions"][0]
        self.assertEqual(region["component_count"], 400)
        self.assertEqual(len(region["boxes"]), 128)
        self.assertTrue(region["boxes_truncated"])
        self.assertEqual(region["boxes"][0], [0, 0, 1, 1])
        self.assertEqual(region["boxes"][-1], [14, 12, 15, 13])
        for query in ([], ["red"] * 17, ["invalid"], [False], "red"):
            with self.subTest(query=query), self.assertRaises(PixlError):
                assets.inspect(self.path, regions=query)

    def test_every_frame_is_checked_against_image_limits_before_conversion(self):
        path = self.path.with_suffix(".tiff")
        Image.new("RGBA", (1, 1), "red").save(
            path, save_all=True, append_images=[Image.new("RGBA", (5, 5), "blue")]
        )
        with (
            patch.object(assets, "MAX_FRAME_PIXELS", 16, create=True),
            self.assertRaisesRegex(PixlError, "image_limit"),
        ):
            assets.inspect(path)
