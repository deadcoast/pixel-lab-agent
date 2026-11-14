"""Read-only local readiness facts and explicitly caller-supplied host observations.

Keep this module importable with the Python standard library alone. Missing
runtime dependencies must be a reportable condition, not a bootstrap traceback.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib
import importlib.metadata
import io
import json
import re
import sys
import tomllib
from datetime import datetime
from pathlib import Path, PurePosixPath

MAX_INPUT_BYTES = 64 * 1024
LOCAL_TOOL = r"^pixl_[a-z][a-z0-9_]{0,90}$"
OFFICIAL_TOOL = r"^[a-z][a-z0-9_]{0,95}$"
VERSION = r"^[0-9]+(?:\.[0-9]+){1,3}(?:[a-z][0-9]+)?$"


def _inventory_schema(pattern):
    return {"type": "object", "additionalProperties": False, "required": ["names", "complete_inventory"],
            "properties": {"names": {"type": "array", "maxItems": 512, "uniqueItems": True,
                                      "items": {"type": "string", "pattern": pattern}},
                           "complete_inventory": {"type": "boolean"}}}


OBSERVATIONS_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["host", "observed_at"],
    "properties": {
        "host": {"enum": ["codex", "claude"]},
        "observed_at": {"type": "string", "format": "date-time", "maxLength": 48},
        "host_version": {"type": "string", "pattern": VERSION, "maxLength": 32},
        "named_role": {"enum": ["available", "unavailable", "not_observed"]},
        "local_tools": _inventory_schema(LOCAL_TOOL),
        "official_tools": _inventory_schema(OFFICIAL_TOOL),
    },
}


class ReadinessError(ValueError):
    def __init__(self, code, detail):
        self.code, self.detail = code, detail
        super().__init__(detail)


def _invalid(detail):
    raise ReadinessError("readiness_input", detail)


def validate_observations(value, host=None):
    """Validate a closed small envelope without returning rejected input values."""
    if value is None:
        return None
    if not isinstance(value, dict) or set(value) - set(OBSERVATIONS_SCHEMA["properties"]):
        _invalid("Observations must be an object containing only documented fields")
    if not {"host", "observed_at"} <= set(value) or value["host"] not in ("codex", "claude"):
        _invalid("Observations require a supported host and timezone-aware observed_at")
    if host is not None and value["host"] != host:
        _invalid("Observation host does not match the selected host")
    stamp = value["observed_at"]
    if not isinstance(stamp, str) or len(stamp) > 48:
        _invalid("observed_at must be a timezone-aware ISO timestamp")
    try:
        instant = datetime.fromisoformat(stamp)
        if instant.utcoffset() is None:
            raise ValueError
    except ValueError:
        _invalid("observed_at must be a timezone-aware ISO timestamp")
    if "host_version" in value and (not isinstance(value["host_version"], str)
            or len(value["host_version"]) > 32 or not re.fullmatch(VERSION, value["host_version"])):
        _invalid("host_version must be a numeric version, not command output or configuration")
    if "named_role" in value and value["named_role"] not in ("available", "unavailable", "not_observed"):
        _invalid("named_role must be available, unavailable or not_observed")
    for field, pattern in (("local_tools", LOCAL_TOOL), ("official_tools", OFFICIAL_TOOL)):
        if field not in value:
            continue
        observed = value[field]
        if not isinstance(observed, dict) or set(observed) != {"names", "complete_inventory"}:
            _invalid("Tool observations require only names and complete_inventory")
        names = observed["names"]
        if (type(observed["complete_inventory"]) is not bool or not isinstance(names, list)
                or len(names) > 512 or any(not isinstance(name, str) or not re.fullmatch(pattern, name) for name in names)
                or len(set(names)) != len(names)):
            _invalid("Tool observations require unique bare operation names and a boolean inventory flag")
    encoded = json.dumps(value)
    if len(encoded.encode("utf-8")) > MAX_INPUT_BYTES:
        _invalid("Observations exceed the 64 KiB limit")
    return json.loads(encoded)


def _json(data):
    def members(items):
        result = {}
        for key, value in items:
            if key in result:
                _invalid("JSON must not contain duplicate fields")
            result[key] = value
        return result

    def constant(_):
        _invalid("JSON must not contain nonfinite values")

    try:
        return json.loads(data, object_pairs_hook=members, parse_constant=constant)
    except (ValueError, UnicodeError, RecursionError):
        _invalid("Input must be valid bounded JSON")


def _confined(root, relative):
    if (not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative
            or PurePosixPath(relative).is_absolute() or ".." in PurePosixPath(relative).parts
            or PurePosixPath(relative).as_posix() != relative):
        _invalid("Expected a normalized forward-slash path inside its declared root")
    result = (root / relative).resolve()
    if result == root or not result.is_relative_to(root):
        _invalid("Resolved path must stay inside its declared root")
    return result


def _hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _file(root, relative, kind="file"):
    result = {"path": relative, "status": "missing"}
    try:
        path = _confined(root, relative)
        if not path.is_file():
            return result
        result.update(status="present", sha256=_hash(path))
        if kind in ("skill", "agent", "codex_role"):
            if path.stat().st_size > MAX_INPUT_BYTES:
                result["status"] = "invalid"
                return result
            text = path.read_text(encoding="utf-8")
            if kind == "codex_role":
                parsed = tomllib.loads(text)
                valid = parsed.get("name") == "pixl" and isinstance(parsed.get("developer_instructions"), str) and bool(parsed["developer_instructions"].strip())
            else:
                head = text.split("---", 2)
                valid = len(head) == 3 and not head[0].strip() and bool(re.search(r"(?m)^name:\s*\S", head[1])) and bool(re.search(r"(?m)^description:\s*\S", head[1]))
            if not valid:
                result["status"] = "invalid"
    except ReadinessError:
        result["status"] = "unsafe_path"
    except (OSError, UnicodeError, ValueError):
        result["status"] = "unreadable_or_invalid"
    return result


def verify_manifest(root):
    try:
        path = _confined(root, "bundle-manifest.json")
        if not path.is_file():
            return {"status": "missing", "files_checked": 0}
        with path.open("rb") as stream:
            manifest_bytes = stream.read(4 * 1024 * 1024 + 1)
        if len(manifest_bytes) > 4 * 1024 * 1024:
            raise ValueError
        manifest = _json(manifest_bytes)
        if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), list) or not manifest["files"]:
            raise ValueError
        generated = manifest.get("generated_files", [])
        if not isinstance(generated, list):
            raise TypeError
        rows = manifest["files"] + generated
        if len(rows) > 10000:
            raise ValueError
        seen, issues = set(), []
        for index, row in enumerate(rows):
            if not isinstance(row, dict) or not isinstance(row.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]):
                raise ValueError
            candidate = _confined(root, row.get("path"))
            if candidate in seen:
                raise ValueError
            seen.add(candidate)
            if not candidate.is_file():
                issues.append({"index": index, "status": "missing"})
            elif _hash(candidate) != row["sha256"]:
                issues.append({"index": index, "status": "hash_mismatch"})
        return {"status": "verified" if not issues else "mismatch", "sha256": hashlib.sha256(manifest_bytes).hexdigest(),
                "files_checked": len(rows), "issues": issues,
                "meaning": "Listed payload bytes match this local manifest; publisher authenticity and host loading are not established."}
    except (OSError, ValueError, TypeError, KeyError):
        return {"status": "invalid_or_unreadable", "files_checked": 0}


def probe_dependencies():
    """Import only known runtime dependencies, suppressing output and bytecode writes."""
    checks = []
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        for distribution, module, minimum in (("pillow", "PIL.Image", (10, 0)),
                                               ("jsonschema", "jsonschema", (4, 18)),
                                               ("referencing", "referencing", None)):
            item = {"distribution": distribution, "module": module, "version": None,
                    "minimum_version": ".".join(map(str, minimum)) if minimum else None}
            try:
                version = importlib.metadata.version(distribution)
                if re.fullmatch(VERSION, version):
                    item["version"] = version
            except importlib.metadata.PackageNotFoundError:
                pass
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    importlib.import_module(module)
            except ModuleNotFoundError:
                item.update(status="missing", importable=False)
            except Exception:  # noqa: BLE001 - Broken dependency imports are diagnostic findings; never echo exception data.
                item.update(status="import_failed", importable=False)
            else:
                status = "available"
                if minimum and item["version"] is None:
                    status = "version_unverified"
                elif minimum:
                    parts = tuple(int(part) for part in re.match(r"[0-9.]+", item["version"]).group().split("."))
                    if parts < minimum:
                        status = "version_too_old"
                item.update(status=status, importable=True)
            checks.append(item)
    finally:
        sys.dont_write_bytecode = previous
    return {"status": "available" if all(item["status"] == "available" for item in checks) else "incomplete",
            "python": ".".join(map(str, sys.version_info[:3])), "checks": checks,
            "probe": "Known local dependency imports only; no provider or host connection is probed."}


def _installation(path):
    explicit = path is not None
    if path is None:
        module = Path(__file__).resolve().parent
        path = module.parent.parent if module.parent.name == "runtime" else module if (module / "resources").is_dir() else module.parent
    try:
        root = Path(path).resolve()
    except (OSError, ValueError, TypeError):
        _invalid("installation must name a local installation directory")
    if not root.is_dir():
        return {"root": str(root), "kind": "unknown", "status": "missing", "files": {}, "bundle_manifest": {"status": "not_observed"}}
    if (root / "runtime").is_dir() or (root / "bundle-manifest.json").is_file():
        kind = "plugin"
        locations = {"profile": ("resources/agent/PROFILE.md", "file"), "pixl_skill": ("skills/pixl/SKILL.md", "skill"),
                     "plar_skill": ("skills/plar/SKILL.md", "skill"), "runtime": ("runtime/pixl/__main__.py", "file")}
    elif (root / "pixl").is_dir() or (root / "pyproject.toml").is_file():
        kind = "source"
        locations = {"profile": (".agents/PROFILE.md", "file"), "pixl_skill": ("plugins/pixl/skills/pixl/SKILL.md", "skill"),
                     "plar_skill": ("plugins/pixl/skills/plar/SKILL.md", "skill"), "runtime": ("pixl/__main__.py", "file")}
    elif (root / "resources").is_dir() and (root / "__init__.py").is_file():
        kind = "wheel"
        locations = {"profile": ("resources/agent/PROFILE.md", "file"), "runtime": ("__main__.py", "file")}
    else:
        return {"root": str(root), "kind": "unknown", "status": "unrecognized", "files": {}, "bundle_manifest": {"status": "not_applicable"}}
    files = {name: _file(root, relative, file_kind) for name, (relative, file_kind) in locations.items()}
    manifest = verify_manifest(root) if kind == "plugin" else {"status": "not_applicable"}
    status = "present" if all(item["status"] == "present" for item in files.values()) and manifest["status"] in ("verified", "not_applicable") else "incomplete"
    if kind == "wheel":
        files.update(pixl_skill={"status": "not_in_distribution"}, plar_skill={"status": "not_in_distribution"})
    return {"root": str(root), "kind": kind, "status": status, "files": files, "bundle_manifest": manifest,
            "selected_by": "explicit_argument" if explicit else "executing_module_location"}


def _visibility(observation, expected=None):
    result = {"status": "not_observed", "basis": "caller_supplied_observation", "names": [], "complete_inventory": None}
    if observation is None:
        return result
    result.update(names=observation["names"], complete_inventory=observation["complete_inventory"])
    result["status"] = "observed" if observation["names"] else "not_listed" if observation["complete_inventory"] else "not_observed"
    if expected:
        result["readiness_operation"] = "observed" if expected in observation["names"] else "not_listed" if observation["complete_inventory"] else "not_observed"
    return result


def report(root, host=None, installation=None, observations=None):
    if host not in (None, "codex", "claude"):
        _invalid("host must be codex or claude")
    try:
        root = Path(root).resolve()
        if not root.is_dir():
            raise ValueError
    except (OSError, ValueError, TypeError):
        raise ReadinessError("readiness_root", "Project root must name an existing directory") from None
    observed = validate_observations(observations, host)
    selected_host = host or (observed["host"] if observed else None)
    if installation is not None:
        try:
            selected = Path(installation)
            if (selected.drive or selected.root) and not selected.is_absolute():
                _invalid("installation must be absolute or relative to the project root, not drive-relative or rooted without a drive")
            installation = selected if selected.is_absolute() else root / selected
        except (TypeError, OSError):
            _invalid("installation must name a local installation directory")
    package = _installation(installation)
    dependencies = probe_dependencies()
    adapters = {}
    for name in (selected_host,) if selected_host else ("codex", "claude"):
        paths = ((".codex/agents/pixl.toml", "codex_role"), (".agents/skills/pixl/SKILL.md", "skill")) if name == "codex" else (
            (".claude/agents/pixl.md", "agent"), (".claude/skills/pixl/SKILL.md", "skill"))
        adapters[name] = {"role_file": _file(root, *paths[0]), "skill_wrapper": _file(root, *paths[1])}
    observations = observed or {}
    actions = []
    if package["status"] != "present":
        actions.append("Select or restore a complete source checkout or plugin installation; inspect the reported file and manifest findings.")
    if dependencies["status"] != "available":
        actions.append("Install the declared runtime dependencies into the Python environment used for this command.")
    if observations.get("named_role", "not_observed") != "available":
        actions.append("Ask the current host to inspect its available specialist roles; a role file alone does not establish registration.")
    if not observations.get("official_tools", {}).get("names"):
        actions.append("Inspect the separately connected official PixelLab tool declarations before affected provider work.")
    return {"version": 1, "status": "reported", "read_only": True, "project": {"root": str(root), "status": "directory_exists"},
            "reporter": {"module": str(Path(__file__).resolve()), "python_executable": sys.executable},
            "installation": package, "dependencies": dependencies,
            "specialist": {"host": selected_host, "static_adapters": adapters,
                           "named_role": observations.get("named_role", "not_observed"),
                           "role_observation_basis": "caller_supplied_observation", "instruction_loading": "not_verified"},
            "local_operations": {"runtime_requirements": "satisfied" if package["status"] == "present" and dependencies["status"] == "available" else "incomplete",
                                 "mcp_visibility": _visibility(observations.get("local_tools"), "pixl_readiness"),
                                 "scope": "Local runtime facts do not establish an active host MCP connection or successful execution of every operation."},
            "official_pixellab": {"visibility": _visibility(observations.get("official_tools")), "authentication": "not_verified",
                                  "execution": "not_attempted", "cached_catalog_is_live_discovery": False},
            "caller_supplied_observations": observed, "actions": actions,
            "limits": ["Static file presence and hashes do not prove host discovery, role registration or instruction loading.",
                       "Host observations are supplied assertions, not authenticated or automatically refreshed by this report.",
                       "Absence from a partial tool inventory remains unobserved; a complete flag applies only to the supplied capture.",
                       "Tool visibility does not prove authentication, generation success, artistic quality or target-engine acceptance.",
                       "No global host configuration, credential values, provider calls or generation probes are read or performed."]}


def configure_parser(parser):
    parser.add_argument("--root", required=True, help="Existing consumer project directory.")
    parser.add_argument("--host", choices=("codex", "claude"))
    parser.add_argument("--installation", help="Source checkout, copied plugin directory, or installed pixl package directory; relative paths use --root, absolute paths may identify a separate installation.")
    parser.add_argument("--observations", help="Optional normalized project-relative JSON file with explicit host observations.")
    return parser


def main(argv=None):
    args = configure_parser(argparse.ArgumentParser(prog="pixl readiness", description=__doc__)).parse_args(argv)
    try:
        observations = None
        if args.observations:
            path = _confined(Path(args.root).resolve(), args.observations)
            try:
                with path.open("rb") as stream:
                    data = stream.read(MAX_INPUT_BYTES + 1)
                if len(data) > MAX_INPUT_BYTES:
                    _invalid("Observation file exceeds the 64 KiB limit")
                observations = _json(data)
            except OSError:
                _invalid("Observation file is unavailable")
        result = report(args.root, args.host, args.installation, observations)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0 if result["local_operations"]["runtime_requirements"] == "satisfied" else 1
    except ReadinessError as error:
        print(json.dumps({"error": error.code, "detail": error.detail}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
