import hashlib
import io
import unittest
from unittest.mock import patch

from PIL import Image

from pixl import inspection_views
from pixl.codec import PixlError


def png(image):
    stream = io.BytesIO()
    image.save(stream, format="PNG")
    return stream.getvalue()


def gif(frames):
    stream = io.BytesIO()
    frames[0].save(
        stream,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=[100 + index * 100 for index in range(len(frames))],
        loop=0,
    )
    return stream.getvalue()


def opened(data):
    with Image.open(io.BytesIO(data)) as image:
        return image.convert("RGBA")


def pixels(image):
    return list(zip(*(band.tobytes() for band in image.split()), strict=True))


class InspectionViewTests(unittest.TestCase):
    def setUp(self):
        self.contract = {"px": [2, 1], "pl": [], "al": "binary"}
        self.options = {
            "references": [],
            "scale": 2,
            "backgrounds": ["#0000ff"],
        }

    def test_preserves_native_alpha_and_uses_exact_nearest_pixels(self):
        source = Image.new("RGBA", (2, 1))
        source.putdata([(255, 0, 0, 255), (0, 255, 0, 128)])
        result = inspection_views.render(
            {"candidate": png(source)}, "candidate", self.contract, self.options
        )

        self.assertEqual(
            result["options"],
            {
                "references": [],
                "scale": 2,
                "backgrounds": ["#0000ff"],
                "max_side": 1024,
                "contexts": [],
            },
        )
        raw = next(view for view in result["views"] if view["background"] is None)
        native = next(
            view
            for view in result["views"]
            if view["background"] == "#0000ff" and view["scale"] == 1
        )
        nearest = next(
            view
            for view in result["views"]
            if view["background"] == "#0000ff" and view["scale"] == 2
        )
        self.assertEqual(
            pixels(opened(result["files"][raw["path"]])),
            [(255, 0, 0, 255), (0, 255, 0, 128)],
        )
        self.assertEqual(
            pixels(opened(result["files"][native["path"]])),
            [(255, 0, 0, 255), (0, 128, 127, 255)],
        )
        self.assertEqual(
            pixels(opened(result["files"][nearest["path"]])),
            [
                (255, 0, 0, 255),
                (255, 0, 0, 255),
                (0, 128, 127, 255),
                (0, 128, 127, 255),
            ]
            * 2,
        )
        self.assertEqual(nearest["crop"], [0, 0, 2, 1])
        self.assertEqual((nearest["width"], nearest["height"]), (4, 2))
        self.assertEqual(
            nearest["sha256"],
            hashlib.sha256(result["files"][nearest["path"]]).hexdigest(),
        )
        self.assertEqual(result["measurements"]["candidate"]["failures"], ["alpha"])
        self.assertFalse(result["measurements"]["candidate"]["visual_quality_verified"])
        self.assertFalse(result["measurements"]["candidate"]["engine_import_verified"])

    def test_crops_scaled_views_before_enlargement_with_full_coverage(self):
        source = Image.new("RGBA", (65, 2))
        for x in range(65):
            source.putpixel((x, 0), (x, 0, 0, 255))
            source.putpixel((x, 1), (0, x, 0, 255))
        options = {**self.options, "max_side": 64}
        result = inspection_views.render(
            {"candidate": png(source)},
            "candidate",
            {**self.contract, "px": [65, 2]},
            options,
        )

        scaled = [
            view
            for view in result["views"]
            if view["context"] is None
            and view["background"] == "#0000ff"
            and view["scale"] == 2
        ]
        self.assertEqual(
            [view["crop"] for view in scaled],
            [[0, 0, 32, 2], [32, 0, 32, 2], [64, 0, 1, 2]],
        )
        self.assertTrue(
            all(max(view["width"], view["height"]) <= 64 for view in scaled)
        )
        delivered = []
        for view in scaled:
            image = opened(result["files"][view["path"]])
            delivered.extend(image.getpixel((x, 0)) for x in range(0, image.width, 2))
        self.assertEqual(delivered, [(x, 0, 0, 255) for x in range(65)])

    def test_retains_inputs_in_candidate_then_explicit_reference_order(self):
        candidate = png(Image.new("RGBA", (2, 1), "red"))
        first = png(Image.new("RGBA", (1, 1), "green"))
        second = png(Image.new("RGBA", (1, 1), "blue"))
        result = inspection_views.render(
            {"second": second, "candidate": candidate, "first": first},
            "candidate",
            self.contract,
            {**self.options, "references": ["first", "second"]},
        )

        self.assertEqual(
            [item["source"] for item in result["inputs"]],
            ["candidate", "first", "second"],
        )
        self.assertEqual(
            [result["files"][item["path"]] for item in result["inputs"]],
            [candidate, first, second],
        )
        self.assertEqual(set(result["measurements"]), {"candidate", "first", "second"})
        self.assertTrue(result["measurements"]["first"]["pass"])

    def test_renders_every_decoded_frame_without_silent_truncation(self):
        data = gif(
            [
                Image.new("RGB", (2, 1), "red"),
                Image.new("RGB", (2, 1), "green"),
                Image.new("RGB", (2, 1), "blue"),
            ]
        )
        result = inspection_views.render(
            {"candidate": data}, "candidate", self.contract, self.options
        )

        raw = [view for view in result["views"] if view["background"] is None]
        self.assertEqual([view["frame"] for view in raw], [0, 1, 2])
        self.assertEqual(result["measurements"]["candidate"]["frame_count"], 3)

    def test_frame_context_retains_timing_pivots_and_common_pivot_strip(self):
        source = Image.new("RGBA", (4, 2), (0, 0, 0, 0))
        source.paste(Image.new("RGBA", (2, 2), "red"), (0, 0))
        source.paste(Image.new("RGBA", (2, 2), "blue"), (2, 0))
        context = {
            "name": "walk",
            "kind": "frames",
            "source": "candidate",
            "source_frame": 0,
            "rects": [[0, 0, 2, 2], [2, 0, 2, 2]],
            "durations_ms": [100, None],
            "pivots": [[0, 0], [1, 1]],
        }
        result = inspection_views.render(
            {"candidate": png(source)},
            "candidate",
            {**self.contract, "px": [4, 2]},
            {**self.options, "contexts": [context]},
        )

        self.assertEqual(
            result["context_observations"],
            [
                {
                    "name": "walk",
                    "kind": "frames",
                    "source": "candidate",
                    "source_frame": 0,
                    "rects": [[0, 0, 2, 2], [2, 0, 2, 2]],
                    "durations_ms": [100, None],
                    "pivots": [[0, 0], [1, 1]],
                    "alignment": "common_pivot",
                }
            ],
        )
        raw_contexts = {
            view["context"]: opened(result["files"][view["path"]])
            for view in result["views"]
            if view["background"] is None and view["context"] is not None
        }
        self.assertEqual(raw_contexts["walk:frame:0"].size, (2, 2))
        self.assertEqual(raw_contexts["walk:frame:1"].size, (2, 2))
        strip = raw_contexts["walk:comparison"]
        self.assertEqual(strip.size, (6, 3))
        self.assertEqual(strip.getpixel((1, 1)), (255, 0, 0, 255))
        self.assertEqual(strip.getpixel((3, 0)), (0, 0, 255, 255))

    def test_frame_context_preserves_unknown_pivots_without_alignment(self):
        source = png(Image.new("RGBA", (2, 1), "red"))
        context = {
            "name": "unknown",
            "kind": "frames",
            "source": "candidate",
            "source_frame": 0,
            "rects": [[0, 0, 1, 1], [1, 0, 1, 1]],
            "durations_ms": [None, None],
            "pivots": [None, None],
        }
        result = inspection_views.render(
            {"candidate": source},
            "candidate",
            self.contract,
            {**self.options, "contexts": [context]},
        )
        self.assertEqual(result["context_observations"][0]["pivots"], [None, None])
        self.assertEqual(result["context_observations"][0]["alignment"], "top_left")

    def test_tile_context_places_declared_indices_and_reports_edge_differences(self):
        source = Image.new("RGBA", (4, 2))
        for y in range(2):
            source.putpixel((0, y), (0, 255, 0, 255))
            source.putpixel((1, y), (255, 0, 0, 255))
            source.putpixel((2, y), (255, 0, 0, 255))
            source.putpixel((3, y), (0, 0, 255, 255))
        context = {
            "name": "path",
            "kind": "tiles",
            "source": "candidate",
            "source_frame": 0,
            "tile_size": [2, 2],
            "grid": [[0, 1, 0]],
        }
        result = inspection_views.render(
            {"candidate": png(source)},
            "candidate",
            {**self.contract, "px": [4, 2]},
            {**self.options, "contexts": [context]},
        )

        observation = result["context_observations"][0]
        self.assertEqual(
            observation["adjacent_edges"],
            [
                {
                    "orientation": "horizontal",
                    "at": [0, 0],
                    "first": 0,
                    "second": 1,
                    "differing_pixels": 0,
                },
                {
                    "orientation": "horizontal",
                    "at": [0, 1],
                    "first": 1,
                    "second": 0,
                    "differing_pixels": 2,
                },
            ],
        )
        raw = next(
            view
            for view in result["views"]
            if view["context"] == "path:neighborhood" and view["background"] is None
        )
        neighborhood = opened(result["files"][raw["path"]])
        self.assertEqual(neighborhood.size, (6, 2))
        self.assertEqual(
            [neighborhood.getpixel((x, 0)) for x in range(6)],
            [
                (0, 255, 0, 255),
                (255, 0, 0, 255),
                (255, 0, 0, 255),
                (0, 0, 255, 255),
                (0, 255, 0, 255),
                (255, 0, 0, 255),
            ],
        )

    def test_context_always_requires_explicit_source_frame(self):
        data = gif([Image.new("RGB", (2, 1), "red"), Image.new("RGB", (2, 1), "blue")])
        context = {
            "name": "walk",
            "kind": "frames",
            "source": "candidate",
            "rects": [[0, 0, 2, 1]],
            "durations_ms": [100],
            "pivots": [None],
        }
        with self.assertRaisesRegex(PixlError, "inspection_context"):
            inspection_views.render(
                {"candidate": data},
                "candidate",
                self.contract,
                {**self.options, "contexts": [context]},
            )

    def test_rejects_closed_schema_and_type_violations(self):
        source = png(Image.new("RGBA", (2, 1), "red"))
        invalid = [
            ({**self.contract, "unknown": 1}, self.options),
            ({**self.contract, "px": [True, 1]}, self.options),
            (self.contract, {**self.options, "unknown": 1}),
            (self.contract, {**self.options, "scale": 2.0}),
            (self.contract, {**self.options, "backgrounds": []}),
            (self.contract, {**self.options, "backgrounds": ["#0000ff", "#0000FF"]}),
            (self.contract, {**self.options, "references": ["candidate"]}),
        ]
        for contract, options in invalid:
            with (
                self.subTest(contract=contract, options=options),
                self.assertRaises(PixlError),
            ):
                inspection_views.render(
                    {"candidate": source}, "candidate", contract, options
                )

    def test_rejects_invalid_context_geometry_and_source_frame(self):
        source = png(Image.new("RGBA", (4, 2), "red"))
        invalid_contexts = [
            {
                "name": "bad",
                "kind": "frames",
                "source": "candidate",
                "source_frame": 1,
                "rects": [[0, 0, 2, 2]],
                "durations_ms": [100],
                "pivots": [None],
            },
            {
                "name": "bad",
                "kind": "frames",
                "source": "candidate",
                "source_frame": 0,
                "rects": [[3, 0, 2, 2]],
                "durations_ms": [100],
                "pivots": [None],
            },
            {
                "name": "bad",
                "kind": "tiles",
                "source": "candidate",
                "source_frame": 0,
                "tile_size": [3, 2],
                "grid": [[0]],
            },
        ]
        for context in invalid_contexts:
            with (
                self.subTest(context=context),
                self.assertRaisesRegex(PixlError, "inspection_context"),
            ):
                inspection_views.render(
                    {"candidate": source},
                    "candidate",
                    {**self.contract, "px": [4, 2]},
                    {**self.options, "contexts": [context]},
                )

    def test_rejects_requests_that_exceed_fixed_rendering_limits(self):
        source = png(Image.new("RGBA", (2, 1), "red"))
        with (
            patch.object(inspection_views, "MAX_VIEWS", 2),
            self.assertRaisesRegex(PixlError, "inspection_limit"),
        ):
            inspection_views.render(
                {"candidate": source}, "candidate", self.contract, self.options
            )

    def test_rejects_aggregate_decode_limit_before_converting_next_frame(self):
        data = gif(
            [
                Image.new("RGB", (2, 1), "red"),
                Image.new("RGB", (2, 1), "green"),
                Image.new("RGB", (2, 1), "blue"),
            ]
        )
        converted = []
        original_convert = Image.Image.convert

        def observed_convert(image, *args, **kwargs):
            converted.append(image.tell())
            return original_convert(image, *args, **kwargs)

        with (
            patch.object(inspection_views, "MAX_DECODED_PIXELS", 2),
            patch.object(Image.Image, "convert", observed_convert),
            self.assertRaisesRegex(PixlError, "inspection_limit"),
        ):
            inspection_views.render(
                {"candidate": data}, "candidate", self.contract, self.options
            )
        self.assertEqual(converted, [0])

    def test_rejects_visible_color_limit_without_truncating_measurement(self):
        source = Image.new("RGBA", (2, 1))
        source.putdata([(255, 0, 0, 255), (0, 255, 0, 255)])
        with (
            patch.object(inspection_views, "MAX_MEASURED_COLORS", 1, create=True),
            self.assertRaisesRegex(PixlError, "inspection_limit"),
        ):
            inspection_views.render(
                {"candidate": png(source)},
                "candidate",
                self.contract,
                self.options,
            )

    def test_measurement_keeps_exact_four_connected_topology(self):
        source = Image.new("RGBA", (3, 3), (0, 0, 0, 0))
        for point in ((0, 0), (2, 0), (2, 1), (1, 1), (0, 2)):
            source.putpixel(point, (255, 0, 0, 255))
        result = inspection_views.render(
            {"candidate": png(source)},
            "candidate",
            {**self.contract, "px": [3, 3]},
            self.options,
        )
        measured = result["measurements"]["candidate"]["frames"][0]
        self.assertEqual(measured["visible_pixels"], 5)
        self.assertEqual(measured["opaque_components"], 3)

    def test_rejects_oversized_frame_strip_before_allocating_it(self):
        source = png(Image.new("RGBA", (2, 1), "red"))
        context = {
            "name": "wide",
            "kind": "frames",
            "source": "candidate",
            "source_frame": 0,
            "rects": [[0, 0, 2, 1]] * 3,
            "durations_ms": [None] * 3,
            "pivots": [None] * 3,
        }
        original_new = Image.new

        def bounded_new(mode, size, *args, **kwargs):
            if size == (6, 1):
                raise AssertionError("oversized strip allocated before validation")
            return original_new(mode, size, *args, **kwargs)

        with (
            patch.object(inspection_views, "MAX_SOURCE_SIDE", 2),
            patch.object(inspection_views.Image, "new", bounded_new),
            self.assertRaisesRegex(PixlError, "inspection_limit"),
        ):
            inspection_views.render(
                {"candidate": source},
                "candidate",
                self.contract,
                {**self.options, "contexts": [context]},
            )

    def test_frame_comparison_preserves_transparent_rgb_exactly(self):
        source = Image.new("RGBA", (2, 1))
        source.putdata([(123, 45, 67, 0), (12, 34, 56, 128)])
        context = {
            "name": "hidden-rgb",
            "kind": "frames",
            "source": "candidate",
            "source_frame": 0,
            "rects": [[0, 0, 2, 1]],
            "durations_ms": [None],
            "pivots": [None],
        }
        result = inspection_views.render(
            {"candidate": png(source)},
            "candidate",
            self.contract,
            {**self.options, "contexts": [context]},
        )
        comparison = next(
            view
            for view in result["views"]
            if view["context"] == "hidden-rgb:comparison" and view["background"] is None
        )
        self.assertEqual(
            pixels(opened(result["files"][comparison["path"]])),
            [(123, 45, 67, 0), (12, 34, 56, 128)],
        )

    def test_tile_neighborhood_preserves_transparent_rgb_exactly(self):
        source = Image.new("RGBA", (2, 1))
        source.putdata([(123, 45, 67, 0), (12, 34, 56, 128)])
        context = {
            "name": "hidden-rgb",
            "kind": "tiles",
            "source": "candidate",
            "source_frame": 0,
            "tile_size": [1, 1],
            "grid": [[0, 1]],
        }
        result = inspection_views.render(
            {"candidate": png(source)},
            "candidate",
            self.contract,
            {**self.options, "contexts": [context]},
        )
        neighborhood = next(
            view
            for view in result["views"]
            if view["context"] == "hidden-rgb:neighborhood"
            and view["background"] is None
        )
        self.assertEqual(
            pixels(opened(result["files"][neighborhood["path"]])),
            [(123, 45, 67, 0), (12, 34, 56, 128)],
        )

    def test_checkerboard_is_a_declared_deterministic_background(self):
        source = Image.new("RGBA", (2, 1), (0, 0, 0, 0))
        result = inspection_views.render(
            {"candidate": png(source)},
            "candidate",
            self.contract,
            {**self.options, "backgrounds": ["checkerboard"]},
        )
        native = next(
            view
            for view in result["views"]
            if view["background"] == "checkerboard" and view["scale"] == 1
        )
        self.assertEqual(
            pixels(opened(result["files"][native["path"]])),
            [(192, 192, 192, 255), (192, 192, 192, 255)],
        )


if __name__ == "__main__":
    unittest.main()
