"""TM-04 regression examples validate requests locally; no provider calls."""

import copy
import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from evaluations import tool_contract_checks as contracts
from pixl import platform
from pixl.codec import PixlError


def declaration(arguments: str, prose: str = "Fixture description") -> str:
    return prose + "\n```ts\ndeclare const tools: { fixture(args: {" + arguments + "}): Promise<CallToolResult>; };\n```"


class ToolContractTests(unittest.TestCase):
    def validate(self, arguments, text):
        return contracts.validate_locally("fixture_tool", arguments, contracts.project_declaration(text), "2000-01-01T00:00:00Z")

    def inputs(self, directory: str) -> Path:
        target = Path(directory)
        for name in ("current-tool-declarations.json", "workbench-describe-edits-request.json", "workbench-describe-edits-response.json"):
            shutil.copyfile(contracts.DEFAULT_OUTPUT / name, target / name)
        return target

    def omit_tool(self, folder: Path, name: str) -> None:
        path = folder / "current-tool-declarations.json"
        data = contracts.read(path)
        data["tools"] = [item for item in data["tools"] if item["name"] != name]
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_documentation_change_is_separate_from_argument_change(self):
        old = declaration("mode?: \"low\" | \"high\";", "Old docs")
        new = declaration('// Changed comment\nmode?: "high" | "low";', "Current docs")
        result = contracts.compare_declarations(old, new)
        self.assertEqual(result["classification"], "documentation_only")
        self.assertTrue(result["argument_structure_equal"])
        self.assertFalse(result["full_description_equal"])

    def test_removed_optional_argument_rejected_without_rewriting_historical_request(self):
        old = contracts.project_declaration(declaration("value: string; optional?: boolean;"))
        new = contracts.project_declaration(declaration("value: string;"))
        arguments = {"value": "keep", "optional": True}
        historical = platform.prepare_discovered(
            "pixellab", "fixture_tool", arguments, old,
            {"source": "Synthetic regression", "observed_at": "2000-01-01T00:00:00Z", "evidence": {"fixture": "removed_optional"}},
            {"scope": "Local validation only", "evidence": {"assignment": "local regression"}},
        )
        original = copy.deepcopy(historical)
        with self.assertRaises(PixlError):
            contracts.validate_locally("fixture_tool", arguments, new, "2000-01-01T00:00:00Z")
        self.assertEqual(platform.validate_discovered(historical), original)
        self.assertEqual(arguments, {"value": "keep", "optional": True})
        self.assertEqual(contracts.compare_schemas(old, new)["changes"][0]["change"], "removed")

    def test_new_optional_argument_does_not_require_or_insert_it(self):
        old = declaration("value: string;")
        new = declaration("value: string; optional?: boolean;")
        self.assertEqual(contracts.compare_declarations(old, new)["changes"][0]["change"], "added")
        args = {"value": "keep"}
        result = self.validate(args, new)
        self.assertTrue(result["arguments_unchanged"])
        self.assertFalse(result["remote_executed"])
        self.assertEqual(args, {"value": "keep"})

    def test_changed_optional_type_rejects_previously_valid_value(self):
        old, new = declaration("seed?: number;"), declaration("seed?: string;")
        self.validate({"seed": 12}, old)
        with self.assertRaises(PixlError):
            self.validate({"seed": 12}, new)
        self.assertEqual(contracts.compare_declarations(old, new)["classification"], "argument_structure_changed")

    def test_removed_enum_value_rejects_old_argument(self):
        old = declaration('mode?: "low" | "high";')
        new = declaration('mode?: "low";')
        self.validate({"mode": "high"}, old)
        with self.assertRaises(PixlError):
            self.validate({"mode": "high"}, new)
        self.assertEqual(contracts.compare_declarations(old, new)["changes"][0]["field"], "mode")

    def test_new_required_argument_rejects_missing_value(self):
        old, new = declaration("value?: string;"), declaration("value: string;")
        self.validate({}, old)
        with self.assertRaises(PixlError):
            self.validate({}, new)
        change = contracts.compare_declarations(old, new)["changes"][0]
        self.assertFalse(change["previous"]["required"])
        self.assertTrue(change["current"]["required"])

    def test_nested_reference_change_is_retained_and_validated(self):
        old = declaration("reference?: {url?: string | null; usage_description?: string | null;} | null;")
        new = declaration("reference?: {url?: string | null;} | null;")
        args = {"reference": {"url": "upload:fixture", "usage_description": "identity"}}
        self.validate(args, old)
        with self.assertRaises(PixlError):
            self.validate(args, new)
        self.assertFalse(contracts.compare_declarations(old, new)["argument_structure_equal"])

    def test_nullable_array_projection_matches_prior_schema_spelling(self):
        current = contracts.project_declaration(declaration("palette?: Array<string> | null;"))
        prior = {"type": "object", "properties": {"palette": {"type": ["array", "null"], "items": {"type": "string"}}}, "additionalProperties": False}
        self.assertTrue(contracts.compare_schemas(prior, current)["argument_structure_equal"])
        self.validate({"palette": None}, declaration("palette?: Array<string> | null;"))

    def test_number_projection_does_not_invent_integer_bounds(self):
        result = self.validate({"width": 12.5}, declaration("width?: number;"))
        self.assertTrue(result["passed"])
        self.assertFalse(result["remote_executed"])

    def test_unsupported_syntax_and_constraints_fail_closed(self):
        for fields in ("value: unknown;", "value: [string, number];", "value: Record<string,string>;", "value: string; value: number;"):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                contracts.project_declaration(declaration(fields))
        with self.assertRaises(ValueError):
            contracts.shape({"type": "number", "minimum": 1})

    def test_captured_workbench_projection_and_actual_command_contract(self):
        snapshot = contracts.read(contracts.DEFAULT_OUTPUT / "current-tool-declarations.json")
        tools = {item["name"]: item["description"] for item in snapshot["tools"]}
        self.assertEqual(len(tools), 10)
        prior = contracts.read(contracts.PRIOR / "workbench-declaration.json")
        comparison = contracts.compare_declarations(prior["tool"]["description"], tools["mcp__pixellab__pixelart_workbench"])
        self.assertTrue(comparison["argument_structure_equal"])
        response = contracts.read(contracts.DEFAULT_OUTPUT / "workbench-describe-edits-response.json")
        self.assertEqual(response["content"], prior["edit_contract"]["content"])
        self.assertFalse(response.get("isError", False))

    def test_missing_retained_tool_is_incomplete_without_claiming_upstream_removal(self):
        with TemporaryDirectory() as directory:
            folder = self.inputs(directory)
            name = "mcp__pixellab__get_upload_url"
            self.omit_tool(folder, name)
            result = contracts.run(folder)
        self.assertEqual(result["status"], "incompatible_or_incomplete_contract_check")
        self.assertFalse(result["checks"]["six_prior_declaration_structures_unchanged"])
        self.assertEqual(result["capture_scope"]["retained_names_not_observed"], [name])
        self.assertFalse(result["capture_scope"]["complete_upstream_inventory"])
        self.assertEqual(result["declaration_comparisons"][name]["classification"], "not_observed_in_current_snapshot")

    def test_missing_replay_tool_is_reported_without_keyerror(self):
        with TemporaryDirectory() as directory:
            folder = self.inputs(directory)
            self.omit_tool(folder, "mcp__pixellab__animate_image")
            result = contracts.run(folder)
        self.assertEqual(result["status"], "incompatible_or_incomplete_contract_check")
        self.assertFalse(result["checks"]["three_retained_requests_locally_valid"])
        replay = result["local_retained_argument_revalidation"]["animate_image"]
        self.assertEqual(replay["status"], "not_observed_in_current_snapshot")
        self.assertFalse(replay["remote_executed"])

    def test_changed_type_records_failed_revalidation_instead_of_success(self):
        with TemporaryDirectory() as directory:
            folder = self.inputs(directory)
            path = folder / "current-tool-declarations.json"
            snapshot = contracts.read(path)
            for item in snapshot["tools"]:
                if item["name"] == "mcp__pixellab__animate_image":
                    item["description"] = item["description"].replace("action: string;", "action: number;")
            path.write_text(json.dumps(snapshot), encoding="utf-8")
            result = contracts.run(folder)
        self.assertEqual(result["status"], "incompatible_or_incomplete_contract_check")
        replay = result["local_retained_argument_revalidation"]["animate_image"]
        self.assertEqual(replay["status"], "current_projection_rejected_retained_arguments")
        self.assertFalse(replay["passed"])

    def test_repeat_run_preserves_both_existing_outputs(self):
        with TemporaryDirectory() as directory:
            folder = self.inputs(directory)
            contracts.run(folder)
            before = {name: (folder / name).read_bytes() for name in ("RESULT.json", "current-schema-projections.json")}
            with self.assertRaises(FileExistsError):
                contracts.run(folder)
            self.assertEqual(before, {name: (folder / name).read_bytes() for name in before})

    def test_either_existing_output_prevents_all_writes(self):
        for name in ("RESULT.json", "current-schema-projections.json"):
            with self.subTest(name=name), TemporaryDirectory() as directory:
                folder = Path(directory)
                sentinel = folder / name
                sentinel.write_bytes(b"preserved incomplete prior evidence")
                with self.assertRaises(FileExistsError):
                    contracts.run(folder)
                self.assertEqual(sentinel.read_bytes(), b"preserved incomplete prior evidence")
                self.assertEqual([path.name for path in folder.iterdir()], [name])


if __name__ == "__main__":
    unittest.main()
