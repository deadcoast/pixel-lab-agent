"""Read existing release bytes against canonical inputs; never build or install."""

import hashlib
import io
import json
import re
import stat
import tarfile
import zipfile
import zlib
from email.parser import BytesParser
from pathlib import Path, PurePosixPath

from scripts.build_plugin import INVENTORY_PATH, capture_inventory, capture_plan

SHA = re.compile(r"[0-9a-f]{64}")
MAX_MANIFEST_BYTES = 4 * 1024 * 1024
MAX_MEMBERS = 10000
MAX_EXPANDED_BYTES = 256 * 1024 * 1024


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _relative(value):
    _require(isinstance(value, str) and bool(value), "Expected a nonempty relative path")
    path = PurePosixPath(value)
    _require(not path.is_absolute() and not any(c in value for c in ("\\", ":", "\x00"))
             and ".." not in path.parts and path.as_posix() == value and value != ".",
             f"Expected a normalized relative path: {value!r}")
    return value


def _inside(root, name):
    result = (root / _relative(name)).resolve()
    _require(result != root and result.is_relative_to(root), f"Path escapes root: {name}")
    return result


def _object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, f"Duplicate JSON field: {key}")
        result[key] = value
    return result


def _manifest(plugin, root):
    path = _inside(plugin, "bundle-manifest.json")
    data = path.read_bytes()
    _require(len(data) <= MAX_MANIFEST_BYTES, "Bundle manifest exceeds the input limit")
    value = json.loads(data, object_pairs_hook=_object)
    _require(isinstance(value, dict) and set(value) == {
        "version", "files", "declared_source_revisions_verified", "source_inventory_sha256",
        "generated_files", "generated_by"}, "Unsupported bundle manifest fields")
    _require(isinstance(value["version"], str) and bool(value["version"]), "Invalid package version")
    _require(type(value["declared_source_revisions_verified"]) is bool,
             "Source-verification flag must be boolean")
    _require(isinstance(value["source_inventory_sha256"], str) and SHA.fullmatch(value["source_inventory_sha256"]),
             "Invalid source-inventory digest")
    _require(isinstance(value["generated_by"], str), "Invalid bundle generator")
    _require(isinstance(value["files"], list) and 0 < len(value["files"]) <= MAX_MEMBERS,
             "Expected nonempty bounded bundle files")
    _require(isinstance(value["generated_files"], list) and len(value["generated_files"]) == 1,
             "Expected one generated requirements entry")
    _require(isinstance(value["generated_files"][0], dict)
             and set(value["generated_files"][0]) == {"path", "sha256"}
             and value["generated_files"][0]["path"] == "requirements.txt",
             "Expected the generated requirements identity")
    seen = set()
    for row in value["files"] + value["generated_files"]:
        _require(isinstance(row, dict), "Bundle row must be an object")
        generated = set(row) == {"path", "sha256"}
        _require(generated or set(row) == {"path", "source", "sha256", "bytes"},
                 "Unsupported bundle row fields")
        _require(isinstance(row["sha256"], str) and SHA.fullmatch(row["sha256"]), "Invalid bundle digest")
        target = _inside(plugin, row["path"])
        _require(target not in seen, f"Duplicate bundle path: {row['path']}")
        seen.add(target)
        if generated:
            _require(row["path"] == "requirements.txt" and row in value["generated_files"],
                     "Unsupported generated file")
        else:
            _inside(root, row["source"])
            _require(type(row["bytes"]) is int and row["bytes"] >= 0, "Invalid bundle byte count")
    _require(all("source" in row for row in value["files"]), "Payload rows require source identities")
    return value, data


def _bundle(root, plugin, captured, inventory_bytes):
    manifest, data = _manifest(plugin, root)
    rows = {row["path"]: row for row in manifest["files"]}
    expected = {target.relative_to(plugin).as_posix(): source.relative_to(root).as_posix()
                for target, source in captured["files"].items()}
    issues = []
    for name in sorted(set(rows) ^ set(expected)):
        issues.append({"path": name, "reason": "missing_manifest_entry" if name in expected else "unexpected_manifest_entry"})
    for name in sorted(set(rows) & set(expected)):
        if rows[name]["source"] != expected[name]:
            issues.append({"path": name, "reason": "source_mapping_changed"})
    actual_generated = set()
    for folder in ("runtime", "resources"):
        directory = _inside(plugin, folder)
        if directory.is_dir():
            for path in directory.rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts:
                    name = path.relative_to(plugin).as_posix()
                    _inside(plugin, name)
                    actual_generated.add(name)
    for name in sorted(actual_generated - set(expected)):
        issues.append({"path": name, "reason": "unlisted_generated_file"})
    listed = []
    for row in manifest["files"] + manifest["generated_files"]:
        target = _inside(plugin, row["path"])
        if not target.is_file():
            listed.append({"path": row["path"], "reason": "missing"})
        else:
            content = target.read_bytes()
            if _digest(content) != row["sha256"] or ("bytes" in row and len(content) != row["bytes"]):
                listed.append({"path": row["path"], "reason": "manifest_bytes_differ"})
    stale = []
    for target, source in captured["files"].items():
        name = target.relative_to(plugin).as_posix()
        _inside(root, source.relative_to(root).as_posix())
        if not target.is_file() or target.read_bytes() != captured["snapshots"][target]:
            stale.append({"path": name, "source": source.relative_to(root).as_posix(), "reason": "canonical_bytes_differ"})
    metadata = []
    if manifest["version"] != captured["version"]:
        metadata.append("version")
    if manifest["declared_source_revisions_verified"] is not True:
        metadata.append("declared_source_revisions_verified")
    if manifest["source_inventory_sha256"] != _digest(inventory_bytes):
        metadata.append("source_inventory_sha256")
    if manifest["generated_by"] != "scripts/build_plugin.py":
        metadata.append("generated_by")
    requirements = _inside(plugin, "requirements.txt")
    if not requirements.is_file() or requirements.read_bytes() != captured["requirements"]:
        metadata.append("requirements.txt")
    if manifest["generated_files"][0]["sha256"] != _digest(captured["requirements"]):
        metadata.append("generated_files.requirements.sha256")
    return [
        _check("bundle_payload_integrity", listed, "Listed bytes agree with the retained local manifest"),
        _check("bundle_payload_set", issues, "Payload and source mappings match the canonical bundle plan"),
        _check("bundle_source_applicability", stale, "Bundled payload agrees with current canonical bytes"),
        _check("bundle_metadata", metadata, "Version, source inventory and runtime requirements agree"),
    ], {"path": "plugins/pixl/bundle-manifest.json", "sha256": _digest(data),
        "expected_payload_files": len(expected), "listed_payload_files": len(rows)}


def _check(code, issues, success):
    return {"code": code, "status": "needs_review" if issues else "current",
            "detail": issues if issues else success,
            "next_action": "Inspect the changed paths and explicitly rebuild/requalify in a fresh attempt; preserve old receipts." if issues else "None for this bounded byte check."}


def _archive_files(data, kind):
    result = {}
    expanded = 0
    if kind == "wheel":
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            members = archive.infolist()
            _require(len(members) <= MAX_MEMBERS, "Archive has too many members")
            for member in members:
                name = _relative(member.filename.rstrip("/") if member.is_dir() else member.filename)
                _require(name not in result, f"Duplicate archive member: {name}")
                _require(not stat.S_ISLNK(member.external_attr >> 16), f"Archive symbolic link: {name}")
                expanded += member.file_size
                _require(expanded <= MAX_EXPANDED_BYTES, "Archive exceeds expanded-byte limit")
                result[name] = None if member.is_dir() else archive.read(member)
    else:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            members = archive.getmembers()
            _require(len(members) <= MAX_MEMBERS, "Archive has too many members")
            for member in members:
                name = _relative(member.name.rstrip("/") if member.isdir() else member.name)
                _require(name not in result, f"Duplicate archive member: {name}")
                _require(member.isfile() or member.isdir(), f"Unsupported archive member type: {name}")
                expanded += member.size
                _require(expanded <= MAX_EXPANDED_BYTES, "Archive exceeds expanded-byte limit")
                result[name] = archive.extractfile(member).read() if member.isfile() else None
    return {name: content for name, content in result.items() if content is not None}


def _metadata_issues(content, project):
    value = BytesParser().parsebytes(content)
    issues = []
    for key, expected in (("Version", project["version"]), ("Name", project.get("name")),
                          ("Requires-Python", project.get("requires-python"))):
        if expected is not None and value.get_all(key, []) != [expected]:
            issues.append(key)
    mandatory = [re.sub(r"\s+", "", row) for row in value.get_all("Requires-Dist", []) if "extra ==" not in row]
    expected = [re.sub(r"\s+", "", row) for row in project["dependencies"]]
    if sorted(mandatory) != sorted(expected):
        issues.append("Requires-Dist")
    return issues


def _archive(root, descriptor, captured, inventory):
    _require(isinstance(descriptor, dict) and set(descriptor) == {"path", "sha256", "kind"},
             "Archive descriptor requires path, sha256 and kind")
    _require(descriptor["kind"] in ("wheel", "sdist"), "Unsupported archive kind")
    _require(isinstance(descriptor["sha256"], str) and SHA.fullmatch(descriptor["sha256"]), "Invalid archive digest")
    path = _inside(root, descriptor["path"])
    prefix = "archive:" + descriptor["path"]
    if not path.is_file():
        return [_check(prefix + ":identity", [{"path": descriptor["path"], "reason": "missing_retained_artifact"}], "")]
    data = path.read_bytes()
    if _digest(data) != descriptor["sha256"]:
        return [_check(prefix + ":identity", [{"path": descriptor["path"], "reason": "retained_artifact_hash_changed"}], "")]
    files = _archive_files(data, descriptor["kind"])
    expected = {}
    if descriptor["kind"] == "wheel":
        for target, source in captured["files"].items():
            relative = target.relative_to(root / "plugins/pixl").as_posix()
            if relative.startswith("resources/"):
                expected["pixl/" + relative] = captured["snapshots"][target]
            elif relative.startswith("runtime/pixl/"):
                expected[relative.removeprefix("runtime/")] = captured["snapshots"][target]
            elif relative == "NOTICE.md":
                expected["pixl/resources/NOTICE.md"] = captured["snapshots"][target]
        metadata = [name for name in files if re.fullmatch(r"[^/]+\.dist-info/METADATA", name)]
        _require(len(metadata) == 1, "Wheel needs exactly one distribution metadata file")
        metadata_path = metadata[0]
        dist_info = metadata_path.rsplit("/", 1)[0]
        _require(all(dist_info + "/" + name in files for name in ("WHEEL", "RECORD")), "Wheel is missing WHEEL or RECORD")
        tracked = {name for name in files if name.startswith("pixl/resources/") or
                   re.fullmatch(r"pixl/[^/]+\.(?:py|json)", name)}
    else:
        roots = {name.split("/", 1)[0] for name in files}
        _require(len(roots) == 1, "Source archive needs one top-level directory")
        archive_root = next(iter(roots))
        files = {name.removeprefix(archive_root + "/"): content for name, content in files.items()}
        for target, source in captured["files"].items():
            name = source.relative_to(root).as_posix()
            if not name.startswith("plugins/"):
                expected[name] = captured["snapshots"][target]
        for name in ("pyproject.toml", "setup.py", "MANIFEST.in"):
            expected[name] = _inside(root, name).read_bytes()
        readme = _inside(root, "README.md")
        if readme.is_file():
            expected["README.md"] = readme.read_bytes()
        metadata_path = "PKG-INFO"
        _require(metadata_path in files, "Source archive is missing PKG-INFO")
        tracked = {name for name in files if name.startswith(("pixl/", "spec/", "knowledge/", "examples/",
                   "docs/research/", "methods/", "evidence/art-methods/", "training/original-docs/"))}
        # Generated setuptools metadata has no source-applicability claim here.
        tracked -= {name for name in tracked if ".egg-info/" in name}
    issues = [{"path": name, "reason": "missing" if name not in files else "current_source_differs"}
              for name, expected_bytes in sorted(expected.items()) if files.get(name) != expected_bytes]
    issues.extend({"path": name, "reason": "unexpected_payload"} for name in sorted(tracked - set(expected)))
    for row in inventory["documents"]:
        previous = row.get("previous")
        if previous and previous["path"] != row["path"]:
            name = ("pixl/resources/" if descriptor["kind"] == "wheel" else "") + previous["path"]
            if name in files:
                issues.append({"path": name, "reason": "obsolete_source_retained"})
    metadata_issues = _metadata_issues(files[metadata_path], captured["project"])
    return [_check(prefix + ":identity", [], "Exact retained archive SHA-256 matches"),
            _check(prefix + ":source_applicability", issues, f"{len(expected)} expected source/runtime/resource files match current canonical bytes"),
            _check(prefix + ":metadata", metadata_issues, "Distribution name/version/runtime dependencies agree")]


def check_release(root: Path, archives: list[dict]) -> dict:
    """Return bounded release integrity and applicability without changing files."""
    root = Path(root).resolve()
    checks, manifest = [], None
    try:
        _require(isinstance(archives, list), "archives must be a list")
        plugin = _inside(root, "plugins/pixl")
        inventory, snapshots = capture_inventory(root)
        captured = capture_plan(root, plugin, inventory, snapshots)
        for source in captured["files"].values():
            _inside(root, source.relative_to(root).as_posix())
    except (OSError, ValueError, TypeError, KeyError) as error:
        return {"status": "invalid", "checks": [{"code": "canonical_inputs", "status": "invalid",
                "detail": str(error), "next_action": "Inspect source inventory and package inputs; no files were repaired."}]}
    try:
        bundle_checks, manifest = _bundle(root, plugin, captured, snapshots[INVENTORY_PATH])
        checks.extend(bundle_checks)
    except (OSError, ValueError, TypeError, KeyError) as error:
        checks.append({"code": "bundle_manifest", "status": "invalid", "detail": str(error),
                       "next_action": "Inspect the existing manifest and retain its bytes before any explicit rebuild."})
    seen = set()
    for descriptor in archives:
        try:
            _require(isinstance(descriptor, dict), "Archive descriptor must be an object")
            path = _inside(root, descriptor.get("path"))
            _require(path not in seen, "Duplicate archive descriptor")
            seen.add(path)
            checks.extend(_archive(root, descriptor, captured, inventory))
        except (OSError, ValueError, TypeError, KeyError, RuntimeError, EOFError,
                zipfile.BadZipFile, tarfile.TarError, zlib.error) as error:
            checks.append({"code": "archive_input", "status": "invalid", "detail": str(error),
                           "next_action": "Inspect the exact retained archive and descriptor; do not substitute a same-named file."})
    status = "invalid" if any(row["status"] == "invalid" for row in checks) else "needs_review" if any(
        row["status"] == "needs_review" for row in checks) else "current"
    return {"status": status, "checks": checks, "bundle": manifest,
            "scope": "Canonical bundle plan and payload; selected archives' exact identity, expected runtime/resource/source files and name/version/runtime-dependency metadata. Sdist also checks build metadata and README when present. Other archive producer semantics are not qualified. No build, installation, native/provider execution or acceptance."}
