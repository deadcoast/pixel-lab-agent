"""Execute fixed, trusted consumer profiles and retain bounded receipts.

This is process/profile isolation, not an OS sandbox. No production records or
artistic verdicts are written by this operation.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError, validators

from . import candidate_review, codec, delivery, destination_observation, service
from .codec import PixlError

Json = dict[str, Any]
PROFILE_FILES = ("capture.mjs", "server.mjs", "view.mjs", "index.html", "check.py", "observation.py")
MAX_SOURCE_BYTES = 64 * 1024 * 1024
MAX_SOURCE_FILES = 512


def _object(fields: Json) -> Json:
    return {"type": "object", "properties": fields, "required": list(fields), "additionalProperties": False}


PATH = {"type": "string", "minLength": 1, "maxLength": 1024}
MODULE_PATH = {**PATH, "pattern": r"^src/(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_.-]+\.(?:js|mjs|ts)$"}
DESTINATION_PATH = {**PATH, "pattern": r"^assets/"}
PROFILE_RESOURCES = {
    "queue-motion-v1": "queue-motion",
    "sprite-animation-v1": "sprite-animation",
    "tile-neighborhood-v1": "tile-neighborhood",
}
_COMMON_FIELDS = {
    "version": {"type": "integer", "const": 1},
    "destinations": {"type": "object", "minProperties": 1, "maxProperties": 1024,
                     "propertyNames": {"minLength": 1}, "additionalProperties": DESTINATION_PATH},
    "scales": {"type": "array", "minItems": 1, "maxItems": 4, "uniqueItems": True,
               "items": {"type": "integer", "minimum": 1, "maximum": 16}},
    "timeout_seconds": {"type": "integer", "minimum": 5, "maximum": 180},
}
_MOTION_FIELDS = {
    "observed_wraps": {"type": "integer", "minimum": 1, "maximum": 10},
    "phase_timeout_ms": {"type": "integer", "minimum": 1000, "maximum": 30000},
}
PROFILE_SCHEMAS = {
    "queue-motion-v1": _object({**_COMMON_FIELDS,
        "profile": {"const": "queue-motion-v1"},
        "modules": _object({"state": MODULE_PATH, "view": MODULE_PATH}),
        **_MOTION_FIELDS, "hold_ms": {"type": "integer", "minimum": 100, "maximum": 5000}}),
    "sprite-animation-v1": _object({**_COMMON_FIELDS,
        "profile": {"const": "sprite-animation-v1"},
        "modules": _object({"animation": MODULE_PATH}), **_MOTION_FIELDS}),
    "tile-neighborhood-v1": _object({**_COMMON_FIELDS,
        "profile": {"const": "tile-neighborhood-v1"},
        "modules": _object({"terrain": MODULE_PATH})}),
}
# The public object remains visibly closed, while each branch requires exactly
# its own fields. A tile consumer does not invent queue modules or motion values.
CONFIG_SCHEMA = {
    "type": "object",
    "properties": {**_COMMON_FIELDS, **_MOTION_FIELDS,
        "profile": {"enum": list(PROFILE_SCHEMAS)},
        "modules": {"oneOf": [schema["properties"]["modules"] for schema in PROFILE_SCHEMAS.values()]},
        "hold_ms": PROFILE_SCHEMAS["queue-motion-v1"]["properties"]["hold_ms"]},
    "required": [*_COMMON_FIELDS, "profile", "modules"],
    "additionalProperties": False,
    "oneOf": list(PROFILE_SCHEMAS.values()),
}
_Validator = validators.extend(Draft202012Validator, type_checker=Draft202012Validator.TYPE_CHECKER.redefine(
    "integer", lambda _, value: type(value) is int))


def _require(condition: bool, detail: str, code: str = "consumer_execution") -> None:
    if not condition:
        raise PixlError(code, detail)


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def _write(path: Path, value: Any) -> None:
    with path.open("xb") as stream:
        stream.write(_json(value))


def _path(root: Path, name: str) -> Path:
    return destination_observation._path(root, name)


def _hash(path: Path, limit: int = MAX_SOURCE_BYTES) -> str:
    _require(path.is_file() and path.stat().st_size <= limit,
             f"missing or oversized input: {path}", "consumer_input")
    with path.open("rb") as stream:
        digest = hashlib.sha256()
        total = 0
        while data := stream.read(1024 * 1024):
            total += len(data)
            _require(total <= limit, f"input grew beyond limit: {path}", "consumer_input")
            digest.update(data)
    return digest.hexdigest()


def _ref(root: Path, path: Path) -> Json:
    return {"path": path.relative_to(root).as_posix(), "sha256": _hash(path)}


def _sources(root: Path) -> dict[str, str]:
    """Snapshot the confined src closure, including transitive module inputs."""
    directory = _path(root, "src")
    _require(directory.is_dir(), "consumer needs a src directory", "consumer_input")
    result: dict[str, str] = {}
    size = 0
    for path in sorted(directory.rglob("*")):
        _require(not path.is_symlink() and path.resolve() == path,
                 "redirected consumer source", "consumer_input")
        if not path.is_file():
            continue
        size += path.stat().st_size
        _require(size <= MAX_SOURCE_BYTES and len(result) < MAX_SOURCE_FILES,
                 "consumer src closure exceeds 512 files or 64 MiB", "consumer_input")
        result[path.relative_to(root).as_posix()] = _hash(path)
    return result


def _configuration(root: Path, config: Json) -> Json:
    try:
        _Validator(CONFIG_SCHEMA).validate(config)
    except ValidationError as error:
        raise PixlError("consumer_config", error.message[:1024]) from error
    config = json.loads(_json(config))
    for name in config["modules"].values():
        path = _path(root, name)
        _require(name.startswith("src/") and path.suffix in {".js", ".mjs", ".ts"},
                 "modules must be consumer-relative js/mjs/ts files under src", "consumer_config")
        _hash(path)
    if config["profile"] == "queue-motion-v1":
        _require(len(set(config["modules"].values())) == 2,
                 "state and view modules must be distinct", "consumer_config")
    for name in config["destinations"].values():
        _path(root, name)
    _require(len(set(config["destinations"].values())) == len(config["destinations"]),
             "destination paths must be unique", "consumer_config")
    return config


def _executable(value: str | None, default: str | None = None) -> str | None:
    value = value if value is not None else default
    if value is None:
        return None
    _require(isinstance(value, str) and bool(value.strip()) and not any(c in value for c in "\r\n\0"),
             "executable must be a single path or executable name", "consumer_config")
    found = shutil.which(value)
    if not found:
        return None
    path = Path(found).resolve()
    # Batch scripts require shell interpretation on Windows and are not supported.
    return str(path) if path.is_file() and path.suffix.lower() not in {".bat", ".cmd"} else None


def _stop_owned(process: subprocess.Popen[Any]) -> Json:
    """Stop only the child tree/group we created; never search by process name."""
    cleanup: Json = {"attempted": True, "pid": process.pid, "method": "taskkill-tree" if os.name == "nt" else "process-group",
                     "process_reaped": False, "tree_confirmed": False}
    try:
        if os.name == "nt":
            if process.poll() is not None:
                # Its PID is no longer ours to signal; Windows may reuse it.
                return {**cleanup, "attempted": False, "process_reaped": True, "complete": False,
                        "error": "owned parent already exited; descendant cleanup cannot be confirmed"}
            taskkill = shutil.which("taskkill")
            if taskkill is None:
                cleanup["error"] = "taskkill unavailable; descendant cleanup unknown"
            else:
                stopped = subprocess.run([taskkill, "/PID", str(process.pid), "/T", "/F"],
                    stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    timeout=10, check=False, creationflags=subprocess.CREATE_NO_WINDOW)
                cleanup["tree_confirmed"] = stopped.returncode == 0
                cleanup["returncode"] = stopped.returncode
        else:
            try:
                os.killpg(process.pid, signal.SIGTERM)  # type: ignore[attr-defined]
            except ProcessLookupError:
                cleanup["tree_confirmed"] = True
            until = time.monotonic() + 1.0
            while time.monotonic() < until:
                process.poll()
                try:
                    os.killpg(process.pid, 0)  # type: ignore[attr-defined]
                except ProcessLookupError:
                    cleanup["tree_confirmed"] = True
                    break
                time.sleep(0.05)
            if not cleanup["tree_confirmed"]:
                try:
                    os.killpg(process.pid, signal.SIGKILL)  # type: ignore[attr-defined]
                    cleanup["escalated"] = True
                except ProcessLookupError:
                    cleanup["tree_confirmed"] = True
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        cleanup["process_reaped"] = process.poll() is not None
        if os.name != "nt" and not cleanup["tree_confirmed"]:
            try:
                os.killpg(process.pid, 0)  # type: ignore[attr-defined]
            except ProcessLookupError:
                cleanup["tree_confirmed"] = True
    except (OSError, subprocess.SubprocessError) as error:
        cleanup["error"] = str(error)[:1024]
    cleanup["complete"] = cleanup["process_reaped"] and cleanup["tree_confirmed"]
    return cleanup


def _run(argv: list[str], root: Path, directory: Path, name: str, deadline: float) -> Json:
    """Retain process receipts even when a subprocess cannot finish."""
    start = time.monotonic()
    receipt: Json = {"phase": name, "argv": argv, "cwd": str(root), "started_at": _now(),
        "status": "unavailable", "returncode": None, "pid": None,
        "stdout": f"execution/{name}.stdout.log", "stderr": f"execution/{name}.stderr.log",
        "cleanup": {"attempted": False, "process_reaped": True, "tree_confirmed": True, "complete": True}}
    process = None
    try:
        with (directory / receipt["stdout"]).open("xb") as stdout, (directory / receipt["stderr"]).open("xb") as stderr:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                receipt["status"] = "timeout"
            else:
                options: Json = {"creationflags": subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
                process = subprocess.Popen(argv, cwd=root, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                                           shell=False, **options)
                receipt["pid"] = process.pid
                receipt["returncode"] = process.wait(timeout=remaining)
                receipt["status"] = "complete" if receipt["returncode"] == 0 else "failed"
                receipt["cleanup"] = {"attempted": False, "process_reaped": True, "tree_confirmed": None,
                                      "complete": None, "scope": "descendant cleanup requires the fixed renderer receipt"}
    except subprocess.TimeoutExpired:
        receipt["status"] = "timeout"
    except KeyboardInterrupt:
        receipt["status"] = "interrupted"
    except OSError as error:
        receipt["error"] = str(error)[:1024]
    finally:
        if process is not None and receipt["status"] in {"timeout", "interrupted", "unavailable", "failed"}:
            receipt["cleanup"] = _stop_owned(process)
            receipt["returncode"] = process.poll()
        receipt["ended_at"] = _now()
        receipt["elapsed_seconds"] = round(time.monotonic() - start, 6)
        _write(directory / "execution" / f"{name}.json", receipt)
    return receipt


def _read_json(path: Path) -> Json:
    _require(path.stat().st_size <= codec.MAX_BYTES, "receipt exceeds 16 MiB")
    value = json.loads(path.read_bytes())
    _require(isinstance(value, dict), "expected an object receipt")
    return value


def _check_summary(check: Json, profile: str = "queue-motion-v1") -> Json:
    """Publish counts without copying images, transition samples or frame arrays."""
    facts = check.get("facts")
    _require(isinstance(facts, dict), "checker facts are missing", "consumer_check")
    assert isinstance(facts, dict)
    summary: Json = {"phases": {}}
    for field in ("pixel_checks", "source_checks", "clock_checks"):
        value = facts.get(field)
        _require(type(value) is int and 0 <= value <= 10000000, "invalid checker count", "consumer_check")
        summary[field] = value
    phases = facts.get("phases")
    _require(isinstance(phases, dict) and len(phases) <= 4, "invalid checker phase summary", "consumer_check")
    assert isinstance(phases, dict)
    allowed_phases = {
        "queue-motion-v1": {"normal-start", "reduced", "normal-restored", "initially-reduced"},
        "sprite-animation-v1": {"playback"},
        "tile-neighborhood-v1": set(),
    }
    _require(profile in allowed_phases, "unknown checker profile", "consumer_check")
    if profile == "sprite-animation-v1":
        _require(set(phases) == {"playback"}, "sprite animation needs observed playback", "consumer_check")
    if profile == "tile-neighborhood-v1":
        _require(summary["clock_checks"] == 0, "static tile observations do not claim clock checks", "consumer_check")
    for name, value in phases.items():
        _require(name in allowed_phases[profile] and isinstance(value, dict),
                 "invalid checker phase", "consumer_check")
        counts = value.get("counts", {})
        _require(isinstance(counts, dict) and len(counts) <= 16, "invalid checker consumer counts", "consumer_check")
        if profile == "sprite-animation-v1":
            _require(value.get("status") == "observed" and type(value.get("sample_count")) is int
                     and 0 < value["sample_count"] <= 10000000 and bool(counts),
                     "sprite playback summary is not observed", "consumer_check")
        rows = {}
        for consumer, count in counts.items():
            _require(isinstance(consumer, str) and len(consumer) <= 128 and isinstance(count, dict),
                     "invalid checker consumer count", "consumer_check")
            frames = count.get("frames", [])
            _require(isinstance(frames, list), "invalid checker frame count", "consumer_check")
            if profile == "sprite-animation-v1":
                _require(0 < len(frames) <= 16 and all(type(frame) is int and 0 <= frame < 16 for frame in frames)
                         and len(set(frames)) == len(frames)
                         and all(type(count.get(k)) is int and 0 <= count[k] <= 10000000
                                 for k in ("transitions", "wraps", "skips")),
                         "invalid sprite playback counts", "consumer_check")
            rows[consumer] = {"distinct_frames": len(frames), **{k: count.get(k) for k in ("transitions", "wraps", "skips")}}
        summary["phases"][name] = {"status": value.get("status"), "sample_count": value.get("sample_count"), "counts": rows}
    _require(len(_json(summary)) <= 32768, "checker summary exceeds 32 KiB", "consumer_check")
    return summary


def execute(state_path: Path, root: Path, candidate_id: str, config: Json, out: str,
            *, node: str | None = None, browser: str | None = None) -> Json:
    """Run one fixed isolated consumer attempt; leave all acceptance to review."""
    root = Path(root).resolve()
    state_path = Path(state_path).resolve()
    config = _configuration(root, config)
    directory = _path(root, out)
    _require(not directory.exists() and not directory.is_symlink(), "use a fresh execution directory", "consumer_export")
    _require(not directory.is_relative_to(root / "src") and
             (state_path.parent == root or not directory.is_relative_to(state_path.parent)),
             "execution output must be outside src and the production store", "consumer_export")
    state_bytes = state_path.read_bytes()
    doc = service.load_document(state_path)
    context = candidate_review.context(doc, root, candidate_id)
    _require("members" in context, "consumer execution requires a family manifest candidate", "consumer_binding")
    manifest = delivery._manifest(doc, doc.records[candidate_id], root)
    _require(not delivery._stale(doc, doc.records[candidate_id], manifest), "family candidate is not current", "consumer_binding")
    members = {row["output"]: row for row in manifest["files"]}
    _require(set(config["destinations"]) == set(members), "destination map must name every manifest member exactly once", "consumer_binding")
    destinations = []
    for output, name in config["destinations"].items():
        member = members[output]
        _require(_hash(_path(root, name)) == member["sha256"], "served destination differs from package: " + output, "consumer_binding")
        destinations.append({"output": output, "candidate": member["candidate"], "path": name, "sha256": member["sha256"]})
    sources = _sources(root)
    # Resolve optional executable syntax before reserving output; absence is retained below.
    node_path = _executable(node, "node")
    browser_path = _executable(browser)
    directory.parent.mkdir(parents=True, exist_ok=True)
    _require(_path(root, out) == directory, "execution path redirected", "consumer_export")
    directory.mkdir(exist_ok=False)
    result: Json = {"version": 1, "profile": config["profile"], "candidate": candidate_id,
        "state_hash": context["state_hash"], "binding_hash": context["binding_hash"], "manifest": context["candidate_file"],
        "status": "partial", "started_at": _now(), "phases": [], "artifacts": {}, "observation": None,
        "requested_inputs": {}, "timeout_scope": "subprocesses",
        "state_changed": False, "state_written": False, "automatic_acceptance": False, "files_verified": False,
        "renderer_executed": False, "process_started": False,
        "cleanup": {"complete": True, "scope": "no renderer launched"},
        "limitations": ["Trusted fixed-profile process isolation and loopback serving are not an OS sandbox.",
                        "timeout_seconds bounds subprocess work; local preflight, retention and bounded cleanup occur around that deadline.",
                        "Captured playback and exact file identities do not establish artistic quality or reviewer acceptance.",
                        "Failed, unavailable and partial attempts are retained; retry with a fresh output directory."]}
    deadline = time.monotonic() + config["timeout_seconds"]
    resource_files: dict[Path, str] = {}
    generated_inputs: dict[str, str] = {}

    def phase(name: str, argv: list[str]) -> Json:
        verify_inputs()
        receipt = _run(argv, root, directory, name, deadline)
        result["phases"].append({"phase": name, "status": receipt["status"], "returncode": receipt["returncode"],
                                 "receipt": f"{out}/execution/{name}.json"})
        if receipt["status"] != "complete":
            result["status"] = receipt["status"]
            result["cleanup"] = receipt["cleanup"]
        # Capture's postcheck follows receipt ingestion below, preserving truthful
        # process/page/cleanup facts even when changed inputs invalidate the run.
        if name != "capture":
            verify_inputs()
        return receipt

    def verify_inputs() -> None:
        _require(state_path.read_bytes() == state_bytes, "production state changed during execution", "consumer_binding")
        current = service.load_document(state_path)
        current_context = candidate_review.context(current, root, candidate_id)
        _require(current_context["binding_hash"] == context["binding_hash"] and current_context["candidate_file"] == context["candidate_file"],
                 "current package bindings changed during execution", "consumer_binding")
        _require(not delivery._stale(current, current.records[candidate_id]), "family candidate is no longer current", "consumer_binding")
        _require(_sources(root) == sources, "consumer source closure changed during execution", "consumer_input")
        for row in destinations:
            _require(_hash(_path(root, row["path"])) == row["sha256"], "served destination changed during execution", "consumer_binding")
        for path, digest in resource_files.items():
            _require(_hash(path) == digest, "renderer source or retained copy changed during execution", "consumer_input")
        for name, digest in generated_inputs.items():
            _require(_hash(_path(root, name)) == digest,
                     "generated execution request changed: " + name, "consumer_input")

    try:
        (directory / "execution").mkdir()
        (directory / "renderer").mkdir()
        for name, value in (("config.json", config), ("review-context.json", context),
                            ("destinations.json", config["destinations"])):
            relative = f"{out}/{name}"
            digest = hashlib.sha256(_json(value)).hexdigest()
            generated_inputs[relative] = digest
            result["requested_inputs"][name] = {"path": relative, "sha256": digest}
            _write(directory / name, value)
        _write(directory / "inputs.json", {"consumer_sources": sources, "destinations": destinations,
                                          "state_file_sha256": hashlib.sha256(state_bytes).hexdigest()})
        profile_name = config["profile"]
        profile = service.resource_root() / "examples/consumer-execution" / PROFILE_RESOURCES[profile_name]
        provenance = []
        for name in PROFILE_FILES:
            source = profile / name
            if not source.is_file():
                result.update(status="unavailable", error={"code": "consumer_profile", "detail": "installed " + profile_name + " profile is incomplete: " + name})
                break
            digest = _hash(source)
            copied = directory / "renderer" / name
            with copied.open("xb") as stream:
                stream.write(source.read_bytes())
            _require(_hash(copied) == digest, "profile changed while copying", "consumer_input")
            resource_files[source] = resource_files[copied] = digest
            provenance.append({"resource": str(source), "copy": copied.relative_to(root).as_posix(), "sha256": digest})
        _write(directory / "renderer-sources.json", provenance)
        if result["status"] == "unavailable":
            return result
        if node_path is None or (browser is not None and browser_path is None):
            result.update(status="unavailable", error={"code": "consumer_capability", "detail": "Node or explicitly selected browser executable is unavailable; no automatic installation"})
            return result
        assert node_path is not None
        verify_inputs()
        _write(directory / "execution" / "executables.json", {
            "node": {"path": node_path, "sha256": _hash(Path(node_path), 512 * 1024 * 1024)},
            "python": {"path": sys.executable, "version": sys.version}, "browser": browser_path})
        if phase("node-version", [node_path, "--version"])["status"] != "complete":
            return result
        capability_key = "queueMotionCapabilities" if profile_name == "queue-motion-v1" else "consumerCapabilities"
        capability = phase("node-capabilities", [node_path, "-e",
            "const m=require('node:module'); const ok=typeof m.stripTypeScriptTypes==='function' && typeof WebSocket==='function' && typeof fetch==='function'; console.log(JSON.stringify({node:process.version," + capability_key + ":ok})); if(!ok)process.exit(3)"])
        if capability["status"] != "complete":
            if capability["status"] == "failed":
                result.update(status="unavailable", error={"code": "consumer_capability", "detail": "Node needs built-in stripTypeScriptTypes, WebSocket and fetch"})
            return result
        argv = [node_path, str(directory / "renderer/capture.mjs"), "--project", str(root),
                "--out", str(directory / "capture"), "--config", str(directory / "config.json")]
        if browser_path is not None:
            argv += ["--browser", browser_path]
        captured = phase("capture", argv)
        result["process_started"] = captured["pid"] is not None
        result["cleanup"] = {"complete": None, "process": captured["cleanup"], "renderer": None,
                             "scope": "owned process receipt retained; renderer profile/server cleanup unconfirmed"}
        execution_path = directory / "capture/execution.json"
        if execution_path.is_file():
            execution = _read_json(execution_path)
            renderer_cleanup = execution.get("cleanup", {"complete": None, "scope": "renderer cleanup missing"})
            _require(isinstance(renderer_cleanup, dict), "invalid renderer cleanup receipt")
            result["renderer_executed"] = execution.get("renderer_executed") is True
            result["cleanup"] = {"complete": renderer_cleanup.get("complete"), "renderer": renderer_cleanup,
                                 "process": captured["cleanup"]}
            if captured["cleanup"].get("attempted"):
                result["cleanup"]["complete"] = renderer_cleanup.get("complete") is True and captured["cleanup"].get("complete") is True
            if captured["status"] not in {"timeout", "interrupted"} and execution.get("status") in {"unavailable", "failed", "timeout"}:
                result["status"] = execution["status"]
        verify_inputs()
        if captured["status"] != "complete" or result["status"] in {"unavailable", "failed", "timeout"}:
            return result
        if result["cleanup"].get("complete") is not True:
            result.update(status="partial", error={"code": "consumer_cleanup", "detail": "renderer did not confirm owned browser/server cleanup"})
            return result
        if phase("check", [sys.executable, str(directory / "renderer/check.py"), "--project", str(root),
                           "--capture", str(directory / "capture"), "--out", str(directory / "check.json")])["status"] != "complete":
            return result
        check = _read_json(directory / "check.json")
        _require(check.get("status") == "pass" and check.get("pass") is True,
                 "consumer structural and profile observation checks did not pass", "consumer_check")
        result["check_summary"] = _check_summary(check, config["profile"])
        if phase("observation", [sys.executable, str(directory / "renderer/observation.py"), "--project", str(root),
                                 "--capture", str(directory / "capture"), "--context", str(directory / "review-context.json"),
                                 "--renderer", str(directory / "renderer"), "--destinations", str(directory / "destinations.json"),
                                 "--out", str(directory / "observation.json")])["status"] != "complete":
            return result
        verify_inputs()
        imported = destination_observation.import_observation(service.load_document(state_path), root, candidate_id,
                                                              f"{out}/observation.json", f"{out}/import")
        verify_inputs()
        result.update(status="complete", files_verified=True, observation=imported["observation"],
                      bundle=imported["bundle"], import_result=f"{out}/import/result.json")
        return result
    except KeyboardInterrupt:
        result.update(status="interrupted", error={"code": "consumer_interrupted", "detail": "execution interrupted; retained available files"})
        return result
    except (PixlError, OSError, ValueError, KeyError) as error:
        result.update(status="failed", error={"code": error.code if isinstance(error, PixlError) else "consumer_execution",
                                              "detail": str(error)[:4096]})
        return result
    finally:
        try:
            verify_inputs()
        except (PixlError, OSError, ValueError, KeyError) as error:
            result.update(status="failed", files_verified=False, observation=None,
                          error={"code": "consumer_inputs_changed", "detail": str(error)[:4096]})
        try:
            result["state_changed"] = state_path.read_bytes() != state_bytes
        except OSError:
            result["state_changed"] = True
        result["ended_at"] = _now()
        for name in ("config.json", "review-context.json", "destinations.json", "inputs.json", "renderer-sources.json",
                     "execution/executables.json", "capture/execution.json", "capture/capture.json", "check.json", "observation.json"):
            path = directory / name
            if path.is_file():
                try:
                    result["artifacts"][name] = _ref(root, path)
                except (OSError, PixlError) as error:
                    result.update(status="partial", observation=None, files_verified=False)
                    result["artifacts"][name] = {"path": path.relative_to(root).as_posix(), "error": str(error)[:1024]}
        result["result_path"] = f"{out}/result.json"
        try:
            _write(directory / "result.json", result)
        except OSError as error:
            raise PixlError("consumer_export", "result export incomplete; available attempt files were preserved",
                            context={"operation_result": result}) from error
