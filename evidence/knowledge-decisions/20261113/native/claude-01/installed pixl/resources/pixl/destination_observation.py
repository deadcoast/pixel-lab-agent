"""Validate supplied destination observations and retain their complete byte inputs."""

from __future__ import annotations

import hashlib
import io
import json
import math
import re
import warnings
import zipfile
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, ValidationError, validators
from PIL import Image, UnidentifiedImageError

from . import candidate_review, codec, delivery, graph
from .codec import Document, PixlError

Json = dict[str, Any]
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_TOTAL_BYTES = 256 * 1024 * 1024
MAX_ARCHIVE_BYTES = 64 * 1024 * 1024
TEXT = {"type": "string", "minLength": 1, "maxLength": 16384, "pattern": r"\S"}
SHA = {"type": "string", "pattern": "^[a-f0-9]{64}$"}


def _object(fields: Json) -> Json:
    return {"type": "object", "properties": fields, "required": list(fields), "additionalProperties": False}


def _array(item: Json, maximum: int = 1024, minimum: int = 0) -> Json:
    return {"type": "array", "items": item, "minItems": minimum, "maxItems": maximum}


FILE_REF = _object({"path": TEXT, "sha256": SHA})
POSITIVE = {"type": "number", "exclusiveMinimum": 0, "maximum": 1e12}
REPORT_SCHEMA = _object({
    "version": {"type": "integer", "const": 1},
    "candidate": TEXT,
    "binding_hash": SHA,
    "manifest": FILE_REF,
    "observed_at": TEXT,
    "renderer": _object({"name": TEXT, "command": _array(TEXT, 256, 1),
                         "runtime": _object({"name": TEXT, "version": TEXT}),
                         "files": _array(FILE_REF, 1024, 1)}),
    "consumer_sources": _array(FILE_REF, 1024, 1),
    "destinations": _array(_object({"output": TEXT, "candidate": TEXT, "path": TEXT, "sha256": SHA}), 1024, 1),
    "viewport": _object({"width": {"type": "integer", "minimum": 1, "maximum": 65536},
                          "height": {"type": "integer", "minimum": 1, "maximum": 65536},
                          "device_scale_factor": {"type": "number", "exclusiveMinimum": 0, "maximum": 64}}),
    "views": _array(_object({"consumer": TEXT, "state": TEXT,
                              "scale": {"type": "number", "exclusiveMinimum": 0, "maximum": 64},
                              "output_id": TEXT, "member_outputs": {**_array(TEXT), "uniqueItems": True}}), 4096),
    "motion": _array(_object({
        "consumer": TEXT, "state": TEXT, "mode": TEXT,
        "status": {"enum": ["observed", "unavailable"]},
        "frame_count": {"anyOf": [{"type": "integer", "minimum": 1, "maximum": 65536}, {"type": "null"}]},
        "frame_ms": {"anyOf": [POSITIVE, {"type": "null"}]},
        "samples": _array(_object({"elapsed_ms": {"type": "number", "minimum": 0, "maximum": 1e12},
                                    "frame": {"anyOf": [{"type": "integer", "minimum": 0}, {"type": "null"}]},
                                    "output_id": TEXT}), 16384),
        "limitation": TEXT,
    }), 1024),
    "files": _array(_object({"id": TEXT, "path": TEXT, "sha256": SHA,
                              "role": {"enum": ["image", "data", "log"]}}), 16384, 1),
    "limitations": _array(TEXT),
})
_types = Draft202012Validator.TYPE_CHECKER.redefine(
    "integer", lambda checker, value: type(value) is int
).redefine("number", lambda checker, value: type(value) is int or (type(value) is float and math.isfinite(value)))
_Validator = validators.extend(Draft202012Validator, type_checker=_types)


def _require(condition: bool, detail: str, code: str = "destination_observation") -> None:
    if not condition:
        raise PixlError(code, detail)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def _path(root: Path, name: str) -> Path:
    _require(isinstance(name, str) and bool(name) and "\\" not in name, "paths must be nonempty consumer-relative POSIX paths")
    relative = PurePosixPath(name)
    _require(not relative.is_absolute() and relative.as_posix() == name and ".." not in relative.parts
             and name != ".", "noncanonical or outside-root path: " + name)
    actual = graph.confined(root, name)
    _require(actual == root / name, "redirected path: " + name, "destination_file")
    return actual


def _decode(data: bytes) -> Json:
    def pairs(items):
        result = {}
        for key, value in items:
            _require(key not in result, "duplicate JSON key: " + key)
            result[key] = value
        return result
    def constant(value):
        raise ValueError(value)
    try:
        value = json.loads(data, object_pairs_hook=pairs, parse_constant=constant)
        _Validator(REPORT_SCHEMA).validate(value)
        return value
    except (ValueError, UnicodeError, RecursionError, ValidationError) as error:
        location = ".".join(map(str, error.absolute_path)) if isinstance(error, ValidationError) else "JSON"
        raise PixlError("destination_observation", "invalid destination report at " + location) from error


class _Capture:
    def __init__(self, root: Path):
        self.root = root
        self.files: dict[str, bytes] = {}
        self.total = 0

    def read(self, name: str, expected: str | None = None, limit: int | None = None) -> bytes:
        limit = MAX_FILE_BYTES if limit is None else min(limit, MAX_FILE_BYTES)
        path = _path(self.root, name)
        if name not in self.files:
            _require(path.is_file(), "not a regular destination input: " + name, "destination_file")
            try:
                with path.open("rb") as stream:
                    data = stream.read(min(limit, MAX_TOTAL_BYTES - self.total) + 1)
            except OSError as error:
                raise PixlError("destination_file", "cannot read " + name) from error
            _require(len(data) <= limit and self.total + len(data) <= MAX_TOTAL_BYTES,
                     "destination inputs exceed retention limit", "destination_limit")
            self.total += len(data)
            self.files[name] = data
        data = self.files[name]
        _require(len(data) <= limit, "destination file exceeds retention limit", "destination_limit")
        _require(expected is None or _sha(data) == expected, "changed file: " + name, "destination_file")
        return data

    def verify(self) -> None:
        for name, data in self.files.items():
            path = _path(self.root, name)
            try:
                with path.open("rb") as stream:
                    current = stream.read(len(data) + 1)
            except OSError as error:
                raise PixlError("destination_file", "input disappeared during import: " + name) from error
            _require(current == data, "input changed during import: " + name, "destination_file")


def _validate_observations(value: Json, member_outputs: set[str], root: Path) -> dict[str, Json]:
    try:
        at = datetime.fromisoformat(value["observed_at"])
        _require(at.utcoffset() is not None and at <= datetime.now(UTC), "observation time must have an offset and not be future")
    except ValueError as error:
        raise PixlError("destination_observation", "invalid observed_at") from error
    files = {row["id"]: row for row in value["files"]}
    _require(len(files) == len(value["files"]), "duplicate output file ID")
    _require(len({_path(root, row["path"]) for row in files.values()}) == len(files), "duplicate output file path")
    for rows in (value["renderer"]["files"], value["consumer_sources"]):
        _require(len({_path(root, row["path"]) for row in rows}) == len(rows), "duplicate source file path")
    def image_id(ident: str) -> None:
        _require(ident in files and files[ident]["role"] == "image", "observation must reference a declared image: " + ident)
    for view in value["views"]:
        image_id(view["output_id"])
        _require(set(view["member_outputs"]) <= member_outputs, "view names a different package member")
    for motion in value["motion"]:
        samples = motion["samples"]
        _require(bool(samples) == (motion["status"] == "observed"), "unavailable motion has no samples; observed motion needs samples")
        previous = -1.0
        for sample in samples:
            image_id(sample["output_id"])
            _require(sample["elapsed_ms"] > previous, "motion sample timestamps must strictly increase")
            previous = sample["elapsed_ms"]
            frame, count = sample["frame"], motion["frame_count"]
            _require(frame is None or count is None or frame < count, "observed frame is outside the declared count")
    return files


def _suffix(path: str) -> str:
    suffix = PurePosixPath(path).suffix
    return suffix if re.fullmatch(r"\.[A-Za-z0-9]{1,16}", suffix) else ".bin"


def _archive(entries: dict[str, bytes]) -> bytes:
    _require(sum(map(len, entries.values())) <= MAX_TOTAL_BYTES,
             "destination archive inputs exceed retention limit", "destination_limit")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    data = buffer.getvalue()
    _require(len(data) <= MAX_ARCHIVE_BYTES, "destination archive exceeds 64 MiB review-file limit", "destination_limit")
    return data


def import_observation(doc: Document, root: Path, candidate_id: str, report_path: str, out: str) -> Json:
    """Export supplied observations after checking current bindings and exact bytes."""
    root = Path(root).resolve()
    directory = _path(root, out)
    _require(not directory.exists() and not directory.is_symlink(), "use a fresh output directory", "destination_export")
    capture = _Capture(root)
    report_bytes = capture.read(report_path, limit=codec.MAX_BYTES)
    value = _decode(report_bytes)
    context = candidate_review.context(doc, root, candidate_id)
    _require("members" in context, "destination import requires a family manifest candidate")
    artifact = doc.records[candidate_id]
    manifest = delivery._manifest(doc, artifact, root)
    _require(not delivery._stale(doc, artifact, manifest), "family candidate is not current", "destination_binding")
    _require(value["candidate"] == candidate_id and value["binding_hash"] == context["binding_hash"],
             "candidate or review bindings changed; reread review-context", "destination_binding")
    _require(value["manifest"] == context["candidate_file"], "report names a different manifest", "destination_binding")
    manifest_bytes = capture.read(value["manifest"]["path"], value["manifest"]["sha256"], codec.MAX_BYTES)
    members = {row["output"]: row for row in manifest["files"]}
    destinations = value["destinations"]
    _require(len(destinations) == len(members) and {row["output"] for row in destinations} == set(members),
             "destinations must name every manifest member exactly once", "destination_binding")
    _require(len({_path(root, row["path"]) for row in destinations}) == len(destinations), "duplicate destination path")
    files = _validate_observations(value, set(members), root)
    entries = {"report.json": report_bytes, "package/manifest.json": manifest_bytes}
    mapping = []
    previews = []
    groups = [("renderer", value["renderer"]["files"]), ("consumer", value["consumer_sources"]),
              ("destinations", destinations), ("outputs", list(files.values()))]
    for group, rows in groups:
        for index, row in enumerate(rows):
            if group == "destinations":
                member = members[row["output"]]
                _require(all(row[key] == member[key] for key in ("candidate", "sha256")),
                         "served destination differs from manifest member: " + row["output"], "destination_binding")
            data = capture.read(row["path"], row["sha256"])
            name = f"{group}/{index:04d}{_suffix(row['path'])}"
            entries[name] = data
            item = {"group": group, "original_path": row["path"], "archive_path": name,
                    "sha256": row["sha256"], "bytes": len(data)}
            if group == "outputs":
                item.update(id=row["id"], role=row["role"])
                if row["role"] == "image":
                    try:
                        with warnings.catch_warnings():
                            warnings.simplefilter("error", Image.DecompressionBombWarning)
                            with Image.open(io.BytesIO(data)) as image:
                                _require(image.format == "PNG", "image outputs must be PNG")
                                width, height = image.size
                                image.verify()
                    except (UnidentifiedImageError, OSError, ValueError, SyntaxError, Image.DecompressionBombError, Image.DecompressionBombWarning) as error:
                        raise PixlError("destination_file", "invalid PNG output: " + row["path"]) from error
                    previews.append({"id": row["id"], "path": f"{out}/previews/{index:04d}.png", "sha256": row["sha256"],
                                     "bytes": len(data), "width": width, "height": height, "archive_path": name})
            mapping.append(item)
    entries["index.json"] = _json({"version": 1, "report_sha256": _sha(report_bytes),
        "manifest_sha256": value["manifest"]["sha256"], "files": mapping,
        "scope": "Retained supplied observations and their verified byte inputs; not execution attestation or artistic acceptance."})
    archive = _archive(entries)
    archive_hash = _sha(archive)
    bundle = {"path": f"{out}/{archive_hash}.zip", "sha256": archive_hash, "bytes": len(archive)}
    result = {"version": 1, "candidate": candidate_id, "state_hash": context["state_hash"],
        "binding_hash": context["binding_hash"], "manifest": context["candidate_file"],
        "report": {"path": report_path, "sha256": _sha(report_bytes)}, "bundle": bundle,
        "renderer": value["renderer"], "consumer_sources": value["consumer_sources"],
        "destinations": value["destinations"], "files": value["files"],
        "observation": {"path": bundle["path"], "sha256": archive_hash, "mode": "live",
                        "note": "Supplied destination observations with exact package, source and output snapshots; reviewer must judge their scope."},
        "previews": previews,
        "supplied_observations": {key: value[key] for key in ("observed_at", "viewport", "views", "motion", "limitations")},
        "files_verified": True, "renderer_executed": False, "state_changed": False,
        "automatic_acceptance": False, "limitations": [
            "Validation establishes supplied-report consistency and retained bytes, not execution, viewing or reviewer identity.",
            "No artistic verdict, nomination or task completion is created; use explicit candidate-review after actual review.",
            "Motion/viewport values remain supplied observations; no universal scale, timing or playback-quality rule is applied.",
        ]}
    capture.verify()
    _require(candidate_review.context(doc, root, candidate_id)["binding_hash"] == context["binding_hash"],
             "review bindings changed during import", "destination_binding")
    try:
        directory.parent.mkdir(parents=True, exist_ok=True)
        _require(_path(root, out) == directory, "output path redirected", "destination_export")
        directory.mkdir(exist_ok=False)
        with (directory / f"{archive_hash}.zip").open("xb") as stream:
            stream.write(archive)
        for preview in previews:
            target = _path(root, preview["path"])
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(entries[preview["archive_path"]])
        capture.verify()
        _require(candidate_review.context(doc, root, candidate_id)["binding_hash"] == context["binding_hash"],
                 "review bindings changed during export", "destination_binding")
        with (directory / "result.json").open("xb") as stream:
            stream.write(_json(result))
    except OSError as error:
        raise PixlError("destination_export", "export incomplete; retained partial files were not overwritten; use a fresh output directory") from error
    return result
