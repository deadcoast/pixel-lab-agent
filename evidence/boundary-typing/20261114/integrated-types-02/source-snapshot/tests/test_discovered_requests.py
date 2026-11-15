"""Local discovered-request boundaries; no fixture represents live discovery."""

import copy
import json
import os
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import platform
from pixl.codec import PixlError

SCHEMA = {
    "type": "object",
    "$defs": {"text": {"type": "string", "minLength": 1}},
    "properties": {
        "description": {"$ref": "#/$defs/text"},
        "size": {"type": "integer", "minimum": 1, "maximum": 512},
        "optional": {"type": "boolean", "default": True},
    },
    "required": ["description"],
    "additionalProperties": False,
    "description": "Complete synthetic caller schema, including annotations.",
}
DISCOVERY = {
    "source": "fixture MCP tools/list",
    "observed_at": "2026-09-11T12:00:00Z",
    "evidence": {"listing_id": "synthetic-listing-1"},
}
AUTHORIZATION = {
    "scope": "Generate one sample under the agreed fixture budget",
    "evidence": {"user_message": "Create the sample"},
}


class DiscoveredRequestTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            callable(getattr(platform, "prepare_discovered", None)),
            "platform.prepare_discovered must provide the new caller-schema route",
        )
        self.assertTrue(
            callable(getattr(platform, "validate_discovered", None)),
            "platform.validate_discovered must validate saved requests",
        )

    def request(self, **changes):
        values = {
            "provider": "pixellab",
            "tool": "future_render_tool",
            "arguments": {"description": "wizard", "size": 512},
            "schema": copy.deepcopy(SCHEMA),
            "discovery": copy.deepcopy(DISCOVERY),
            "authorization": copy.deepcopy(AUTHORIZATION),
        }
        values.update(changes)
        return platform.prepare_discovered(**values)

    def test_credential_defaults_cannot_hide_in_applicators_or_local_references(self):
        for schema in (
            {
                "type": "object",
                "properties": {"token": {"allOf": [{"default": "fictional-value"}]}},
            },
            {
                "type": "object",
                "$defs": {"credential": {"default": "fictional-value"}},
                "properties": {"api_key": {"$ref": "#/$defs/credential"}},
            },
        ):
            with (
                self.subTest(schema=schema),
                self.assertRaisesRegex(PixlError, "platform_secret"),
            ):
                self.request(arguments={}, schema=schema)
        valid = {
            "type": "object",
            "$defs": {"credential": {"type": "string"}},
            "properties": {"api_key": {"$ref": "#/$defs/credential"}},
        }
        self.assertEqual(self.request(arguments={}, schema=valid)["arguments"], {})

    def test_future_discovery_rejected_on_prepare_without_reinterpreting_history(self):
        future = (datetime.now(UTC) + timedelta(days=1)).isoformat()
        discovery = {**DISCOVERY, "observed_at": future}
        with self.assertRaisesRegex(PixlError, "cannot be in the future"):
            self.request(discovery=discovery)
        # Older version-1 envelopes remain readable with their exact original assertions.
        historical = self.request()
        historical["discovery"]["observed_at"] = future
        self.assertEqual(platform.validate_discovered(historical), historical)

    def test_new_tool_retains_full_schema_arguments_and_caller_assertions(self):
        args = {"description": "wizard", "size": 512}
        schema = copy.deepcopy(SCHEMA)
        discovery = copy.deepcopy(DISCOVERY)
        authorization = copy.deepcopy(AUTHORIZATION)
        result = self.request(
            arguments=args,
            schema=schema,
            discovery=discovery,
            authorization=authorization,
        )
        self.assertEqual(
            set(result),
            {
                "version",
                "provider",
                "tool",
                "arguments",
                "schema",
                "schema_sha256",
                "request_sha256",
                "discovery",
                "authorization",
                "prepared_at",
                "policy",
                "remote_executed",
                "cached_assessment",
            },
        )
        self.assertEqual(result["arguments"], {"description": "wizard", "size": 512})
        self.assertNotIn("optional", result["arguments"])
        self.assertEqual(result["schema"], SCHEMA)
        self.assertEqual(result["discovery"], DISCOVERY)
        self.assertEqual(result["authorization"], AUTHORIZATION)
        self.assertEqual(result["policy"], "caller_schema")
        self.assertIs(result["remote_executed"], False)
        self.assertEqual(result["cached_assessment"]["status"], "unlisted")
        self.assertEqual(platform.validate_discovered(result), result)
        args["size"] = 4
        schema["$defs"]["text"]["minLength"] = 100
        discovery["evidence"]["listing_id"] = "changed"
        authorization["evidence"]["user_message"] = "changed"
        self.assertEqual(result["arguments"]["size"], 512)
        self.assertEqual(result["schema"], SCHEMA)
        self.assertEqual(result["discovery"], DISCOVERY)
        self.assertEqual(result["authorization"], AUTHORIZATION)

    def test_current_schema_beats_cached_constraint_and_retains_dated_diagnostic(self):
        result = self.request(tool="create_character")
        cached = result["cached_assessment"]
        self.assertIs(cached["advisory"], True)
        self.assertEqual(cached["status"], "conflict")
        self.assertTrue(cached["source"])
        self.assertTrue(cached["retrieved_at"])
        self.assertEqual(cached["findings"][0]["code"], "platform_constraint")
        self.assertTrue(cached["findings"][0]["detail"])
        with self.assertRaises(PixlError):
            platform.prepare("create_character", result["arguments"], SCHEMA)

    def test_cache_absence_is_advisory_and_replay_does_not_reread_it(self):
        result = self.request(tool="create_character")
        with (
            TemporaryDirectory() as temp,
            patch.dict(os.environ, {"PIXL_PLUGIN_ROOT": temp}),
        ):
            unavailable = self.request()
            self.assertEqual(unavailable["cached_assessment"]["status"], "unavailable")
            self.assertTrue(unavailable["cached_assessment"]["findings"])
            replayed = platform.validate_discovered(result)
        self.assertEqual(replayed, result)
        replayed["arguments"]["size"] = 1
        self.assertEqual(result["arguments"]["size"], 512)

    def test_unrelated_provider_does_not_inherit_pixellab_rules(self):
        result = self.request(provider="other-provider", tool="create_character")
        self.assertEqual(
            result["cached_assessment"],
            {
                "advisory": True,
                "source": None,
                "retrieved_at": None,
                "status": "not_applicable",
                "findings": [],
            },
        )

    def test_malformed_cache_retains_an_advisory_diagnostic(self):
        with TemporaryDirectory() as temp:
            path = Path(temp) / "resources" / "knowledge" / "pixellab-capabilities.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"tools": [], "retrieved_at": "yesterday"}))
            with patch.dict(os.environ, {"PIXL_PLUGIN_ROOT": temp}):
                result = self.request()
        self.assertEqual(result["cached_assessment"]["status"], "unavailable")
        self.assertTrue(result["cached_assessment"]["findings"])

    def test_request_hash_binds_each_execution_field_but_not_assertion_metadata(self):
        result = self.request()
        for change in (
            {"provider": "fixture"},
            {"tool": "future_render_tool_2"},
            {"arguments": {"description": "knight", "size": 512}},
            {"schema": {**SCHEMA, "title": "revised schema"}},
        ):
            with self.subTest(change=list(change)):
                self.assertNotEqual(
                    result["request_sha256"], self.request(**change)["request_sha256"]
                )
        second = self.request(
            arguments={"size": 512, "description": "wizard"},
            discovery={**DISCOVERY, "source": "second supplied listing"},
            authorization={**AUTHORIZATION, "scope": "second supplied approval"},
        )
        self.assertEqual(second["request_sha256"], result["request_sha256"])
        self.assertEqual(second["schema_sha256"], result["schema_sha256"])

    def test_request_hashes_use_canonical_execution_json(self):
        result = self.request(
            provider="fixture", tool="render", arguments={}, schema={"type": "object"}
        )
        self.assertEqual(
            result["request_sha256"],
            "55c45915355bad943153c52710889f7b4a567642ff8a733f3d8071098eb398a2",
        )
        self.assertEqual(
            result["schema_sha256"],
            "a2c799262a3ce3c19ef5cdd983bf3d12b43ab3c426227091b909dcb7054738c0",
        )

    def test_invalid_timezone_minutes_are_rejected_without_normalizing(self):
        with self.assertRaises(PixlError):
            self.request(
                discovery={**DISCOVERY, "observed_at": "2026-09-11T12:00:00+01:99"}
            )

    def test_changed_argument_shape_leaves_cache_failure_advisory(self):
        result = self.request(
            tool="create_character",
            schema={"type": "object"},
            arguments={"body_type": "quadruped", "template": ["new", "template"]},
        )
        self.assertEqual(result["cached_assessment"]["status"], "unavailable")
        self.assertTrue(result["cached_assessment"]["findings"])
        self.assertEqual(platform.validate_discovered(result), result)

    def test_replay_requires_closed_dated_advisory_findings(self):
        original = self.request(tool="create_character")
        assessment = original["cached_assessment"]
        for field, value in (
            ("advisory", False),
            ("advisory", 1),
            ("extra", True),
            ("source", None),
            ("retrieved_at", None),
            ("status", "verified"),
            ("findings", []),
            ("findings", {}),
            ("findings", [{"code": "constraint", "detail": ""}]),
            ("findings", [{"code": "constraint", "detail": "failure", "extra": True}]),
        ):
            with self.subTest(field=field), self.assertRaises(PixlError):
                platform.validate_discovered(
                    {**original, "cached_assessment": {**assessment, field: value}}
                )

    def test_saved_hash_or_execution_field_drift_is_rejected(self):
        original = self.request()
        for key, value in (
            ("provider", "different"),
            ("tool", "different"),
            ("arguments", {"description": "different"}),
            ("schema", {"type": "object"}),
            ("schema_sha256", "0" * 64),
            ("request_sha256", "0" * 64),
        ):
            with self.subTest(field=key):
                result = copy.deepcopy(original)
                result[key] = value
                with self.assertRaises(PixlError):
                    platform.validate_discovered(result)

    def test_exact_provenance_and_authorization_shapes_are_required(self):
        for field, examples in (
            (
                "discovery",
                [
                    None,
                    {},
                    {**DISCOVERY, "extra": True},
                    {**DISCOVERY, "source": " "},
                    {**DISCOVERY, "observed_at": "2026-09-11"},
                    {**DISCOVERY, "observed_at": "2026-09-11T12:00:00"},
                    {**DISCOVERY, "observed_at": "2026-02-30T12:00:00Z"},
                    {**DISCOVERY, "evidence": {}},
                ],
            ),
            (
                "authorization",
                [
                    None,
                    {},
                    {**AUTHORIZATION, "extra": True},
                    {**AUTHORIZATION, "scope": " "},
                    {**AUTHORIZATION, "evidence": []},
                    {**AUTHORIZATION, "evidence": {}},
                ],
            ),
        ):
            for value in examples:
                with (
                    self.subTest(field=field, value=value),
                    self.assertRaises(PixlError),
                ):
                    self.request(**{field: value})

    def test_request_shape_and_constant_types_are_checked_on_replay(self):
        original = self.request()
        for key in original:
            with self.subTest(missing=key):
                result = copy.deepcopy(original)
                del result[key]
                with self.assertRaises(PixlError):
                    platform.validate_discovered(result)
        for field, value in (
            ("extra", True),
            ("version", True),
            ("version", 2),
            ("remote_executed", 0),
            ("remote_executed", True),
            ("policy", "cached"),
            ("prepared_at", "yesterday"),
            ("cached_assessment", {}),
            ("discovery", {**DISCOVERY, "evidence": {}}),
            ("authorization", {**AUTHORIZATION, "scope": ""}),
        ):
            with self.subTest(field=field):
                result = {**original, field: value}
                with self.assertRaises(PixlError):
                    platform.validate_discovered(result)

    def test_arguments_must_satisfy_the_complete_supplied_schema(self):
        for arguments in (
            [],
            {},
            {"description": 3},
            {"description": ""},
            {"description": "wizard", "extra": True},
        ):
            with self.subTest(arguments=arguments), self.assertRaises(PixlError):
                self.request(arguments=arguments)
        for schema in (
            {"type": "imaginary"},
            {"inputSchema": SCHEMA},
            {"$ref": "https://example.invalid/never-fetch.json"},
            {"$ref": "#/$defs/missing"},
        ):
            with self.subTest(schema=schema), self.assertRaises(PixlError):
                self.request(schema=schema)

    def test_nonfinite_nonjson_and_unbounded_data_fail_before_persistence(self):
        deep = {}
        for _ in range(70):
            deep = {"child": deep}
        for value in (
            float("nan"),
            float("inf"),
            b"bytes",
            {1: "bad key"},
            deep,
            "x" * (16 * 1024 * 1024),
        ):
            with self.subTest(kind=type(value).__name__), self.assertRaises(PixlError):
                self.request(arguments={"payload": value}, schema={"type": "object"})
        cyclic = {}
        cyclic["child"] = cyclic
        with self.assertRaises(PixlError):
            self.request(discovery={**DISCOVERY, "evidence": cyclic})

    def test_provider_and_tool_preserve_only_valid_unmodified_identities(self):
        for field in ("provider", "tool"):
            for value in (None, 1, "", " ", " padded", "line\nbreak", "a" * 257):
                with (
                    self.subTest(field=field, value=value),
                    self.assertRaises(PixlError),
                ):
                    self.request(**{field: value})

    def test_credentials_are_excluded_from_payloads_and_assertions_without_echo(self):
        secret = "DO-NOT-ECHO"
        for changes in (
            {
                "arguments": {"nested": [{"API-Key": secret}]},
                "schema": {"type": "object"},
            },
            {"discovery": {**DISCOVERY, "evidence": {"Authorization": secret}}},
            {"authorization": {**AUTHORIZATION, "evidence": {"access_token": secret}}},
            {"schema": {"type": "object", "examples": [{"password": secret}]}},
            {
                "schema": {
                    "type": "object",
                    "properties": {"token": {"default": secret}},
                }
            },
        ):
            with self.subTest(field=next(iter(changes))):
                with self.assertRaises(PixlError) as caught:
                    self.request(**changes)
                self.assertNotIn(secret, str(caught.exception))

    def test_full_schema_can_describe_optional_credential_fields_without_values(self):
        schema = {"type": "object", "properties": {"token": {"type": "string"}}}
        result = self.request(arguments={}, schema=schema)
        self.assertEqual(result["schema"], schema)
        self.assertEqual(platform.validate_discovered(result), result)


if __name__ == "__main__":
    unittest.main()
