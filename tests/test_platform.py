"""Offline request and journal contracts; all response records are test fixtures."""

import base64
import hashlib
import io
import json
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PIL import Image

from pixl.codec import PixlError

try:
    from pixl import platform
except ImportError:
    platform = None


OBJECT = {"type": "object"}


def png(width=32, height=32):
    stream = io.BytesIO()
    Image.new("RGBA", (width, height), (10, 20, 30, 255)).save(stream, format="PNG")
    return base64.b64encode(stream.getvalue()).decode("ascii")


def prepared():
    return {"intent_sha256": "a" * 64, "tool": "create_character",
            "state": "prepared", "remote_id": None, "observations": []}


class PlatformTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(platform, "PIXL offline platform adapter is not implemented")

    def reject(self, tool, arguments, schema=None, authorization=None):
        with self.assertRaises(PixlError):
            platform.prepare(tool, arguments, schema or OBJECT, authorization)

    def test_catalog_lookup_and_plugin_resource_root(self):
        result = platform.capabilities("create_1_direction_object")
        self.assertIn("style_images", result["required"])
        with self.assertRaises(PixlError):
            platform.capabilities("imaginary_generation_tool")
        with TemporaryDirectory() as temp:
            path = Path(temp) / "resources/knowledge"
            path.mkdir(parents=True)
            (path / "pixellab-capabilities.json").write_text(json.dumps({"version": 1, "tools": []}))
            with patch.dict(os.environ, {"PIXL_PLUGIN_ROOT": temp}):
                self.assertEqual(platform.capabilities()["tools"], [])

    def test_installed_wheel_reads_packaged_resources_outside_source_checkout(self):
        with TemporaryDirectory() as temp:
            package = Path(temp) / "pixl"
            resources = package / "resources/knowledge"
            resources.mkdir(parents=True)
            (resources / "pixellab-capabilities.json").write_text(json.dumps({
                "version": 1, "tools": [{"name": "packaged-tool", "effect": "read"}]}))
            with patch.dict(os.environ, {}, clear=True), patch.object(platform, "__file__", str(package / "platform.py")):
                self.assertEqual(platform.capabilities("packaged-tool")["effect"], "read")

    def test_preparation_is_deterministic_offline_and_does_not_mutate_inputs(self):
        args = {"description": "wizard", "size": 48}
        schema = {"type": "object", "properties": {"size": {"type": "integer"},
                  "description": {"type": "string"}}, "required": ["description"],
                  "additionalProperties": False}
        result = platform.prepare("create_character", args, schema)
        again = platform.prepare("create_character", dict(reversed(list(args.items()))), schema)
        self.assertEqual(result["intent_sha256"], again["intent_sha256"])
        expected = hashlib.sha256(json.dumps(schema, sort_keys=True, separators=(",", ":"),
                                            ensure_ascii=False).encode()).hexdigest()
        self.assertEqual(result["schema_sha256"], expected)
        self.assertFalse(result["remote_executed"])
        self.assertFalse(result["discovery_verified"])
        self.assertEqual(result["schema_source"], "caller_supplied")
        self.assertEqual(result["state"], "prepared")
        self.assertIsNone(result["remote_id"])
        result["arguments"]["description"] = "changed"
        self.assertEqual(args["description"], "wizard")

    def test_schema_changes_and_argument_changes_change_intent_identity(self):
        first = platform.prepare("create_character", {"description": "wizard"}, OBJECT)
        second = platform.prepare("create_character", {"description": "knight"}, OBJECT)
        third = platform.prepare("create_character", {"description": "wizard"},
                                 {"type": "object", "required": ["description"]})
        self.assertNotEqual(first["intent_sha256"], second["intent_sha256"])
        self.assertNotEqual(first["intent_sha256"], third["intent_sha256"])

    def test_exact_schema_rejects_invalid_types_unknown_fields_and_missing_requirements(self):
        schema = {"type": "object", "properties": {"description": {"type": "string"}},
                  "required": ["description"], "additionalProperties": False}
        for args in ({}, {"description": 3}, {"description": "wizard", "size": 48}):
            with self.subTest(args=args):
                self.reject("create_character", args, schema)
        self.reject("create_character", {"description": "wizard"}, {"type": "imaginary"})
        self.reject("create_character", {"description": "wizard"},
                    {"name": "create_character", "inputSchema": OBJECT})

    def test_local_schema_references_work_and_external_references_never_resolve(self):
        schema = {"type": "object", "$defs": {"text": {"type": "string", "minLength": 2}},
                  "properties": {"description": {"$ref": "#/$defs/text"}}}
        platform.prepare("create_character", {"description": "wizard"}, schema)
        self.reject("create_character", {"description": "x"}, schema)
        for ref in ("https://example.invalid/schema", "file:///private/schema", "other.json", "//example.invalid/schema"):
            with self.subTest(ref=ref):
                self.reject("create_character", {"description": "wizard"}, {"$ref": ref})
        self.reject("create_character", {"description": "wizard"}, {"$ref": "#/$defs/missing"})

    def test_secrets_and_non_json_values_are_rejected_without_echoing_secrets(self):
        for args in ({"api_key": "DO-NOT-ECHO"}, {"nested": {"Authorization": "DO-NOT-ECHO"}},
                     {"description": float("nan")}, {1: "invalid key"}):
            with self.subTest(args=args):
                with self.assertRaises(PixlError) as caught:
                    platform.prepare("create_character", args, OBJECT)
                self.assertNotIn("DO-NOT-ECHO", str(caught.exception))

    def test_character_modes_sizes_and_ignored_controls(self):
        for extra in ({"size": 129}, {"mode": "v3", "size": 257},
                      {"mode": "pro", "n_directions": 4}, {"mode": "v3", "shading": "flat shading"},
                      {"view": "oblique"}, {"view": "oblique", "mode": "pro", "n_directions": 4},
                      {"body_type": "quadruped"}):
            with self.subTest(extra=extra):
                self.reject("create_character", {"description": "wizard", **extra})
        platform.prepare("create_character", {"description": "cat", "body_type": "quadruped", "template": "cat"}, OBJECT)
        platform.prepare("create_character", {"description": "wizard", "mode": "v3", "size": 256}, OBJECT)
        platform.prepare("create_character", {"description": "wizard", "view": "oblique", "n_directions": 4}, OBJECT)

    def test_character_reference_modes_transport_and_dimensions(self):
        ref = png()
        self.reject("create_character", {"description": "wizard", "reference_image_base64": ref})
        self.reject("create_character", {"description": "wizard", "mode": "v3",
                    "reference_image_base64": ref, "reference_image_url": "https://example.test/ref.png"})
        self.reject("create_character", {"description": "wizard", "mode": "v3", "reference_image_url": "file:///sprite.png"})
        self.reject("create_character", {"description": "wizard", "mode": "v3", "reference_image_base64": "truncated"})
        self.reject("create_character", {"description": "wizard", "mode": "v3", "reference_image_base64": png(257, 32)})
        platform.prepare("create_character", {"description": "wizard", "mode": "v3", "reference_image_base64": ref}, OBJECT)

    def test_character_state_requires_paired_valid_canvas_overrides(self):
        for extra in ({"override_width": 64}, {"override_width": 65, "override_height": 64}):
            self.reject("create_character_state", {"character_id": "source", "edit_description": "wings", **extra})
        platform.prepare("create_character_state", {"character_id": "source", "edit_description": "wings",
                         "override_width": 64, "override_height": 64}, OBJECT)

    def test_animation_modes_frames_and_custom_pose_direction(self):
        for extra in ({"frame_count": 5}, {"frame_count": 18}, {"mode": "template"},
                      {"mode": "template", "template_animation_id": "walking", "frame_count": 8},
                      {"custom_start_frame_base64": png()},
                      {"custom_start_frame_base64": png(), "directions": ["south", "north"]},
                      {"custom_start_frame_base64": png(), "directions": ["south"], "end_frame_base64": png(64, 32)}):
            with self.subTest(extra=list(extra)):
                self.reject("animate_character", {"character_id": "character", "action_description": "walk", **extra})
        result = platform.prepare("animate_character", {"character_id": "character", "action_description": "walk",
                                  "frame_count": 8, "keep_first_frame": False}, OBJECT)
        self.assertEqual(result["arguments"]["frame_count"], 8)
        self.assertFalse(result["arguments"]["keep_first_frame"])

    def test_pro_animation_confirmation_needs_quote_and_explicit_approval_evidence(self):
        args = {"character_id": "character", "mode": "pro", "action_description": "walk", "confirm_cost": True}
        for authorization in (None, {}, {"approved": True}, {"cost_quote": {"generations": 40}},
                              {"cost_quote": {"generations": 40}, "approval": {"explicit": True}}):
            self.reject("animate_character", args, authorization=authorization)
        authorized = {"cost_quote": {"generations": 40, "response_id": "quote-fixture"},
                      "approval": {"explicit": True, "evidence": {"user_message": "Approve the quoted 40 generations"}}}
        result = platform.prepare("animate_character", args, OBJECT, authorized)
        self.assertFalse(result["remote_executed"])
        platform.prepare("animate_character", {**args, "confirm_cost": False}, OBJECT)
        self.reject("animate_object", {"object_id": "object", "mode": "pro",
                    "animation_description": "spin", "confirm_cost": True})

    def test_object_reference_and_direction_specific_ranges(self):
        self.reject("create_1_direction_object", {"description": "pot"})
        self.reject("create_1_direction_object", {"description": "pot", "size": 64,
                    "style_images": [{"base64": png(), "format": "png"}]})
        self.reject("create_8_direction_object", {"description": "pot", "size": 16})
        self.reject("create_8_direction_object", {"description": "pot", "size": 64, "reference_image_base64": png()})
        self.reject("create_8_direction_object", {"description": "pot", "reference_image_base64": png(), "style_image_base64": png()})
        platform.prepare("create_1_direction_object", {"description": "pot", "size": 16, "style_images": []}, OBJECT)

    def test_topdown_terrain_modes_and_geometry_are_not_interchangeable(self):
        args = {"lower_description": "water", "upper_description": "grass"}
        for extra in ({"tile_size": 64}, {"tile_size": {"width": 16, "height": 32}},
                      {"mode": "pro", "shape_style": "round"}, {"transition_size": 0.3},
                      {"mode": "standard", "raggedness": 0.8}):
            self.reject("create_topdown_tileset", {**args, **extra})
        platform.prepare("create_topdown_tileset", {**args, "mode": "pro", "tile_size": 64}, OBJECT)
        platform.prepare("create_topdown_tileset", {**args, "shape_style": "round", "transition_size": 0.3}, OBJECT)

    def test_path_and_building_ranges_and_pro_reference_shape_conflicts(self):
        self.reject("create_path_tiles", {"description": "road", "tile_type": "isometric"})
        self.reject("create_path_tiles", {"description": "road", "tile_size": 48})
        platform.prepare("create_path_tiles", {"description": "road", "tile_type": "isometric", "tile_size": 64}, OBJECT)
        self.reject("create_building_kit", {"wall_description": "stone", "floor_description": "wood", "wall_tiles": 4})
        self.reject("create_tiles_pro", {"description": "tiles", "tile_feature": "roads"})
        self.reject("create_tiles_pro", {"description": "tiles", "tile_feature": "tileset", "style_images": [{"base64": png()}]})

    def test_image_sizes_and_mask_forms(self):
        self.reject("create_image_pixflux", {"description": "potion", "width": 16, "height": 16})
        platform.prepare("create_image_pixflux", {"description": "potion", "width": 16, "height": 64}, OBJECT)
        for width, height in ((33, 32), (16, 32)):
            self.reject("create_image_pixen", {"description": "potion", "width": width, "height": height})
        self.reject("create_ui_asset", {"description": "panel", "width": 688, "height": 512})
        self.reject("inpaint_image", {"description": "grass", "image_base64": png(), "mask_x": 1})
        self.reject("inpaint_image", {"description": "grass", "image_base64": png(),
                    "mask_x": 0, "mask_y": 0, "mask_width": 8, "mask_height": 8, "mask_image_base64": png()})
        platform.prepare("inpaint_image", {"description": "grass", "image_base64": png(),
                         "mask_x": 0, "mask_y": 0, "mask_width": 8, "mask_height": 8}, OBJECT)

    def test_image_source_alternatives_and_palette_conflicts(self):
        self.reject("edit_image", {"description": "hat"})
        self.reject("edit_image_pixen", {"description": "", "image_base64": png()})
        self.reject("reduce_colors", {"images_base64": [png()], "num_colors": 16, "palette_image_base64": png()})
        self.reject("correct_pixelart", {"images_base64": [png(), png(64, 32)]})
        self.reject("animate_image_pixminimax", {"description": "fire", "first_frame_base64": png(), "frame_count": 6})

    def test_journal_requires_remote_evidence_and_preserves_inputs(self):
        initial = prepared()
        for remote_id, evidence in ((None, {"response": "accepted"}), ("", {"response": "accepted"}),
                                    ("job-1", None), ("job-1", {})):
            with self.assertRaises(PixlError):
                platform.job_update(initial, "submitted", remote_id, evidence)
        result = platform.job_update(initial, "submitted", "job-fixture-1", {"response": "accepted fixture"})
        self.assertEqual(initial, prepared())
        self.assertEqual(result["state"], "submitted")
        self.assertEqual(result["remote_id"], "job-fixture-1")
        self.assertEqual(len(result["observations"]), 1)
        self.assertFalse(result["remote_executed"])
        self.assertEqual(result["observations"][0]["evidence_origin"], "caller_supplied")

    def test_prepared_result_can_be_journaled_without_losing_request_identity(self):
        intent = platform.prepare("create_character", {"description": "wizard"}, OBJECT)
        accepted = platform.job_update(intent, "submitted", "job-fixture", {"response": "accepted fixture"})
        self.assertEqual(accepted["arguments"], {"description": "wizard"})
        self.assertEqual(accepted["intent_sha256"], intent["intent_sha256"])
        self.assertFalse(accepted["discovery_verified"])

    def test_unknown_submission_does_not_recreate_and_requires_identity_recovery(self):
        unknown = platform.job_update(prepared(), "unknown", evidence={"transport": "response lost"})
        self.assertIsNone(unknown["remote_id"])
        self.assertEqual(unknown["state"], "unknown")
        with self.assertRaises(PixlError):
            platform.job_update(unknown, "prepared")
        with self.assertRaises(PixlError):
            platform.job_update(unknown, "running", evidence={"response": "processing"})
        recovered = platform.job_update(unknown, "running", "job-fixture-2", {"response": "processing fixture"})
        self.assertEqual(recovered["remote_id"], "job-fixture-2")
        self.assertEqual(recovered["intent_sha256"], "a" * 64)

    def test_terminal_results_need_evidence_and_identity_cannot_change(self):
        submitted = platform.job_update(prepared(), "submitted", "job-fixture-1", {"response": "accepted fixture"})
        with self.assertRaises(PixlError):
            platform.job_update(submitted, "succeeded")
        with self.assertRaises(PixlError):
            platform.job_update(submitted, "running", "different-job", {"response": "running"})
        done = platform.job_update(submitted, "succeeded", evidence={"response": "completed fixture"})
        self.assertEqual(done["state"], "succeeded")
        self.assertEqual(done["remote_id"], "job-fixture-1")
        for state in ("running", "submitted", "failed", "succeeded"):
            with self.assertRaises(PixlError):
                platform.job_update(done, state, evidence={"response": "fixture"})

    def test_local_failure_is_terminal_without_inventing_an_id(self):
        failed = platform.job_update(prepared(), "failed", evidence={"error": "transport rejected before acceptance"})
        self.assertIsNone(failed["remote_id"])
        self.assertEqual(failed["state"], "failed")
        with self.assertRaises(PixlError):
            platform.job_update(failed, "submitted", "job-1", {"response": "fixture"})

    def test_tampered_journal_cannot_rebind_intent_or_skip_acceptance(self):
        with self.assertRaises(PixlError):
            platform.job_update(prepared(), "succeeded", "job-1", {"response": "completed"})
        accepted = platform.job_update(prepared(), "submitted", "job-fixture", {"response": "accepted fixture"})
        accepted["intent_sha256"] = "b" * 64
        with self.assertRaises(PixlError):
            platform.job_update(accepted, "running", evidence={"response": "processing"})
        forged = {**prepared(), "state": "submitted", "remote_id": "job-fixture"}
        with self.assertRaises(PixlError):
            platform.job_update(forged, "succeeded", evidence={"response": "completed"})

    def test_journal_rejects_secret_receipts_without_mutation(self):
        initial = prepared()
        with self.assertRaises(PixlError):
            platform.job_update(initial, "submitted", "job-fixture", {"Authorization": "secret"})
        self.assertEqual(initial, prepared())


if __name__ == "__main__":
    unittest.main()
