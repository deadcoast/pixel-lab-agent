"""Bounded comparisons of retained host declarations; never calls a provider.

The host exposes TypeScript argument declarations, not raw tools/list schemas.
The supported grammar is deliberately small and fails closed on other syntax.
Generated JSON Schemas are local projections, with explicit known-field closure;
they cannot establish undocumented upstream constraints or command-line grammar.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path

from pixl import platform
from pixl.codec import PixlError

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "evidence/artistic-revision/20261109/contracts"
PRIOR = ROOT / "evidence/pixellab-family-production/20261108/project/work/live-family"
TOKEN = re.compile(r'\s+|//[^\n]*|"(?:[^"\\]|\\.)*"|[A-Za-z_][A-Za-z_0-9]*|[{}?:;,<>|]')
LIMITS = [
    "Host-exposed typed declarations are retained verbatim; raw tools/list inputSchema was not exposed.",
    "Projection preserves exposed types, optionality, arrays, objects and string enums only.",
    "TypeScript number remains JSON number; integer and numeric limits cannot be inferred from it.",
    "additionalProperties=false is a local known-argument check, not a claim about upstream unknown-field behavior.",
    "Tool prose and workbench argv command grammar are separate evidence; top-level validity does not validate edit operations.",
    "No discovery authentication, remote acceptance, pixel outcome, generation or host reliability is established by these checks.",
]


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, value) -> None:
    # Evidence is immutable even if another process creates the path after the
    # initial guard. A second run needs a fresh directory with copied inputs.
    with path.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def source_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


class _Arguments:
    def __init__(self, text: str):
        self.tokens = []
        position = 0
        while position < len(text):
            match = TOKEN.match(text, position)
            if match is None:
                raise ValueError("Unsupported TypeScript argument syntax")
            token = match.group()
            if not token.isspace() and not token.startswith("//"):
                self.tokens.append(token)
            position = match.end()
        self.position = 0

    def peek(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def take(self, expected=None):
        token = self.peek()
        if token is None or (expected is not None and token != expected):
            raise ValueError("Malformed TypeScript argument declaration")
        self.position += 1
        return token

    def value(self):
        options = [self.atom()]
        while self.peek() == "|":
            self.take("|")
            options.append(self.atom())
        if len(options) == 1:
            return options[0]
        if all(set(item) == {"type", "enum"} and item["type"] == "string" for item in options):
            return {"type": "string", "enum": sorted({v for item in options for v in item["enum"]})}
        return {"anyOf": options}

    def atom(self):
        token = self.take()
        if token in ("string", "number", "boolean", "null"):
            return {"type": token}
        if token.startswith('"'):
            return {"type": "string", "enum": [json.loads(token)]}
        if token == "Array":
            self.take("<")
            item = self.value()
            self.take(">")
            return {"type": "array", "items": item}
        if token != "{":
            raise ValueError("Unsupported TypeScript type: " + token)
        properties, required = {}, []
        while self.peek() != "}":
            name = self.take()
            if not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", name) or name in properties:
                raise ValueError("Invalid or duplicate argument property")
            optional = self.peek() == "?"
            if optional:
                self.take("?")
            self.take(":")
            properties[name] = self.value()
            if not optional:
                required.append(name)
            if self.peek() in (";", ","):
                self.take()
            elif self.peek() != "}":
                raise ValueError("Missing argument separator")
        self.take("}")
        result = {"type": "object", "properties": properties, "additionalProperties": False}
        if required:
            result["required"] = sorted(required)
        return result


def project_declaration(description: str) -> dict:
    """Project only the complete supported exposed argument declaration."""
    match = re.search(r"declare const tools:\s*\{\s*\w+\(args:\s*", description)
    if match is None:
        raise ValueError("No host-exposed TypeScript declaration")
    end = re.search(r"\):\s*Promise<CallToolResult>;\s*};", description[match.end():])
    if end is None:
        raise ValueError("Incomplete host-exposed declaration")
    parser = _Arguments(description[match.end():match.end() + end.start()])
    result = parser.value()
    if parser.peek() is not None or result.get("type") != "object":
        raise ValueError("Unsupported argument root or trailing syntax")
    return result


def shape(schema: dict) -> dict:
    """Canonical comparable argument structure; annotations are not constraints."""
    allowed = {"type", "properties", "required", "additionalProperties", "items", "anyOf", "enum", "description", "title"}
    if set(schema) - allowed:
        raise ValueError("Unsupported schema constraints: " + ", ".join(sorted(set(schema) - allowed)))
    if "anyOf" in schema or isinstance(schema.get("type"), list):
        if "anyOf" in schema and set(schema) - {"anyOf", "description", "title"}:
            raise ValueError("Unsupported constraints alongside anyOf")
        options = schema["anyOf"] if "anyOf" in schema else [{**schema, "type": t} for t in schema["type"]]
        values = [shape(option) for option in options]
        # Flatten equivalent union spelling; retain all distinct alternatives.
        flat = [v for item in values for v in (item.get("options", [item]) if item.get("kind") == "union" else [item])]
        unique = {json.dumps(value, sort_keys=True): value for value in flat}
        return {"kind": "union", "options": [unique[key] for key in sorted(unique)]}
    kind = schema.get("type")
    if "enum" in schema:
        if kind != "string" or not all(isinstance(value, str) for value in schema["enum"]):
            raise ValueError("Only exposed string enums are supported")
        return {"kind": "enum", "values": sorted(set(schema["enum"]))}
    if kind == "object":
        required = set(schema.get("required", []))
        return {"kind": kind, "fields": {name: {"required": name in required, "shape": shape(value)}
                for name, value in sorted(schema.get("properties", {}).items())}}
    if kind == "array":
        return {"kind": kind, "items": shape(schema["items"])}
    if kind not in ("string", "number", "integer", "boolean", "null"):
        raise ValueError("Unsupported schema type")
    return {"kind": kind}


def compare_schemas(previous: dict, current: dict) -> dict:
    before, after = shape(previous), shape(current)
    if before["kind"] != "object" or after["kind"] != "object":
        raise ValueError("Comparison requires object arguments")
    changes = []
    for name in sorted(set(before["fields"]) | set(after["fields"])):
        old, new = before["fields"].get(name), after["fields"].get(name)
        if old != new:
            changes.append({"field": name, "change": "added" if old is None else "removed" if new is None else "changed",
                            "previous": old, "current": new})
    return {"argument_structure_equal": not changes, "changes": changes}


def compare_declarations(previous: str, current: str) -> dict:
    result = compare_schemas(project_declaration(previous), project_declaration(current))
    result["full_description_equal"] = previous == current
    result["classification"] = ("unchanged" if previous == current else "documentation_only"
                                if result["argument_structure_equal"] else "argument_structure_changed")
    result["previous_description_sha256"] = hashlib.sha256(previous.encode("utf-8")).hexdigest()
    result["current_description_sha256"] = hashlib.sha256(current.encode("utf-8")).hexdigest()
    return result


def validate_locally(tool: str, arguments: dict, schema: dict, observed_at: str) -> dict:
    """Use the public saved-request validator; never send the request."""
    request = platform.prepare_discovered(
        "pixellab", tool, arguments, schema,
        {"source": "Retained host-exposed declaration projection for local TM-04 comparison",
         "observed_at": observed_at, "evidence": {"representation": "projection; not raw tools/list"}},
        {"scope": "Local tool-contract validation only; no provider execution",
         "evidence": {"assignment": "CF-03 prerequisite TM-04"}},
    )
    platform.validate_discovered(request)
    return {"passed": True, "arguments_unchanged": request["arguments"] == arguments,
            "schema_sha256": request["schema_sha256"], "request_sha256": request["request_sha256"],
            "remote_executed": request["remote_executed"], "cached_assessment": request["cached_assessment"]}


def run(output: Path = DEFAULT_OUTPUT) -> dict:
    for name in ("RESULT.json", "current-schema-projections.json"):
        if (output / name).exists():
            raise FileExistsError("Preserve existing evidence; copy inputs to a fresh output directory: " + str(output / name))
    snapshot_path = output / "current-tool-declarations.json"
    snapshot = read(snapshot_path)
    observed = datetime.strptime(snapshot["observed_at"], "%Y-%m-%d %H:%M:%S UTC").replace(tzinfo=UTC).isoformat()
    prior_tools = read(PRIOR / "tool-declarations.json")["tools"] + [read(PRIOR / "workbench-declaration.json")["tool"]]
    previous = {item["name"]: item for item in prior_tools}
    current = {item["name"]: item for item in snapshot["tools"]}
    schemas = {name.removeprefix("mcp__pixellab__"): project_declaration(item["description"]) for name, item in current.items()}
    comparisons = {}
    for name in sorted(set(previous) | set(current)):
        if name not in current:
            comparisons[name] = {"classification": "not_observed_in_current_snapshot", "argument_structure_equal": False,
                                 "limit": "Absence from this selected capture does not prove upstream tool removal."}
        elif name not in previous:
            comparisons[name] = {"classification": "no_retained_declaration"}
        else:
            comparisons[name] = compare_declarations(previous[name]["description"], current[name]["description"])
    missing_retained = sorted(set(previous) - set(current))
    catalog_path = ROOT / "knowledge/pixellab-capabilities.json"
    catalog = read(catalog_path)
    entries = {entry["name"]: entry for entry in catalog["tools"]}
    catalog_comparison = {}
    for name, schema in schemas.items():
        entry = entries.get(name)
        catalog_comparison[name] = {"status": "unlisted"} if entry is None else {
            "status": "listed", "added_parameters": sorted(set(schema["properties"]) - set(entry["parameters"])),
            "removed_parameters": sorted(set(entry["parameters"]) - set(schema["properties"])),
            "required_parameters_equal": set(schema.get("required", [])) == set(entry.get("required", [])),
            "cached_integer_fields_not_proven_by_host_number_type": sorted(
                field for field, parameter in entry["parameters"].items()
                if parameter.get("type") == "integer" and field in schema["properties"]
                and any(option.get("type") == "number" for option in schema["properties"][field].get("anyOf", [schema["properties"][field]]))),
        }
    replay, projections = {}, {}
    for name, filename in (("pixelart_workbench", "working-animation-motion-01-request.json"),
                           ("animate_image", "working-animation-01-request.json"),
                           ("create_image_pro_flash", "working-seed-request.json")):
        old = read(PRIOR / filename)
        if name not in schemas:
            projections[name] = {"prior_request": (PRIOR / filename).relative_to(ROOT).as_posix(),
                                 "status": "not_observed_in_current_snapshot", "argument_structure_equal": False}
            replay[name] = {"passed": False, "status": "not_observed_in_current_snapshot", "remote_executed": False}
            continue
        projections[name] = {"prior_request": (PRIOR / filename).relative_to(ROOT).as_posix(),
                             **compare_schemas(old["schema"], schemas[name])}
        try:
            replay[name] = validate_locally(name, old["arguments"], schemas[name], observed)
        except PixlError as error:
            replay[name] = {"passed": False, "status": "current_projection_rejected_retained_arguments",
                            "error_code": error.code, "remote_executed": False}
    old_contract = read(PRIOR / "workbench-declaration.json")["edit_contract"]
    response_path = output / "workbench-describe-edits-response.json"
    response = read(response_path)
    if response.get("isError") or not response.get("content"):
        raise ValueError("Current read-only command contract lookup failed")
    def texts(value):
        return [block["text"] for block in value["content"] if block["type"] == "text"]
    contract_check = {"response_object_equal": old_contract == response,
                      "all_text_blocks_equal": texts(old_contract) == texts(response),
                      "prior_sha256": sha(PRIOR / "workbench-declaration.json"), "response_sha256": sha(response_path),
                      "operation": "pixelart_workbench describe edits", "remote_generation": False}
    write(output / "current-schema-projections.json", {"observed_at": observed, "source_sha256": sha(snapshot_path),
                                                       "limitations": LIMITS, "schemas": schemas})
    checks = {"six_prior_declaration_structures_unchanged": len(previous) == 6 and not missing_retained
              and all(comparisons[name]["argument_structure_equal"] for name in previous),
              "three_prior_projections_unchanged": all(item["argument_structure_equal"] for item in projections.values()),
              "workbench_edit_contract_text_unchanged": contract_check["all_text_blocks_equal"],
              "three_retained_requests_locally_valid": all(item["passed"] and item.get("arguments_unchanged", False)
                                                          and not item["remote_executed"] for item in replay.values())}
    result = {"status": "completed_scoped_contract_check" if all(checks.values()) else "incompatible_or_incomplete_contract_check",
              "observed_at": observed, "tools_captured": len(current),
              "capture_scope": {"current_selected_names": sorted(current), "retained_comparison_names": sorted(previous),
                                "retained_names_not_observed": missing_retained, "complete_upstream_inventory": False},
              "declaration_comparisons": comparisons, "prior_projection_comparisons": projections,
              "catalog": {"path": catalog_path.relative_to(ROOT).as_posix(), "sha256": sha(catalog_path),
                          "retrieved_at": catalog["retrieved_at"], "comparison": catalog_comparison},
              "workbench_command_contract": contract_check, "local_retained_argument_revalidation": replay,
              "documented_differences": [
                  "Current edit_image_pixen prose requires input and output sides divisible by four; dated catalog and edit-specific runtime checks omit this.",
                  "Current edit_image prose quotes 10-25 generations; dated catalog quotes 20-40. Catalog pricing is not current authority.",
              ],
              "official_documentation": ["https://api.pixellab.ai/mcp/docs", "https://www.pixellab.ai/docs"],
              "limitations": LIMITS,
              "comparison_helper_sha256": sha(Path(__file__)),
              "regression_receipt": ({"path": "regression-attempt-02.json", "sha256": sha(output / "regression-attempt-02.json"),
                                       **read(output / "regression-attempt-02.json")} if (output / "regression-attempt-02.json").exists() else None),
              "checks": checks,
              "inputs": {source_path(path): sha(path) for path in [snapshot_path, response_path,
                         output / "workbench-describe-edits-request.json", PRIOR / "tool-declarations.json", PRIOR / "workbench-declaration.json"]}}
    write(output / "RESULT.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    result = run(parser.parse_args().output)
    print(json.dumps({"status": result["status"], "checks": result["checks"]}, indent=2))
