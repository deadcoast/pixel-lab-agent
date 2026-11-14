"""Retain read-only current checks and isolated old/new builder byte parity."""
import hashlib
import json
import sys
import traceback
from datetime import UTC, datetime
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from scripts import build_plugin, release_integrity

OUT = Path(__file__).resolve().parent
WORK = ROOT / "build/tm10-package-parity-01"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def ref(path):
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": sha(data), "bytes": len(data)}


def snapshot(paths):
    return {p.relative_to(ROOT).as_posix(): {"sha256": sha(p.read_bytes()), "mtime_ns": p.stat().st_mtime_ns}
            for p in sorted(set(paths)) if p.is_file()}


def write(name, value):
    with (OUT / name).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def file_tree(path):
    return {p.relative_to(path).as_posix(): sha(p.read_bytes())
            for p in sorted(path.rglob("*")) if p.is_file()}


result = {"version": 1, "observed_at": datetime.now(UTC).isoformat(), "status": "running",
          "scope": "Read-only existing package/archive inspection, then builder equivalence in two fresh isolated roots. No live bundle rebuild, installation, native/provider execution or acceptance.",
          "source": ref(Path(__file__)),
          "checker": ref(ROOT / "scripts/release_integrity.py"),
          "builder": ref(ROOT / "scripts/build_plugin.py"),
          "old_builder": ref(OUT / "build_plugin-before.py.txt")}
write("proof-01-freeze.json", result)
try:
    inventory, source_snapshots = build_plugin.capture_inventory(ROOT)
    captured = build_plugin.capture_plan(ROOT, ROOT / "plugins/pixl", inventory, source_snapshots)
    distribution = ROOT / "evidence/install-support/20261114/distribution-02/RESULT.json"
    distribution_result = json.loads(distribution.read_bytes())
    archives = [{"path": Path(row["path"]).resolve().relative_to(ROOT).as_posix(),
                 "sha256": row["sha256"], "kind": "wheel" if row["path"].endswith(".whl") else "sdist"}
                for row in distribution_result["artifacts"] if row["path"].endswith((".whl", ".tar.gz"))]
    observed_paths = set(captured["files"].values()) | {ROOT / "pyproject.toml", ROOT / "setup.py", ROOT / "MANIFEST.in", ROOT / "README.md"}
    observed_paths.update(p for p in (ROOT / "plugins/pixl").rglob("*") if p.is_file())
    observed_paths.update(p for p in (ROOT / "evidence/install-support").rglob("*") if p.is_file())
    before = snapshot(observed_paths)
    invalid_descriptors = [{**row, "path": str(ROOT / row["path"])} for row in archives]
    rejected = release_integrity.check_release(ROOT, invalid_descriptors)
    write("absolute-descriptor-rejection.json", rejected)
    assert rejected["status"] == "invalid"
    actual = release_integrity.check_release(ROOT, archives)
    write("current-package-check.json", actual)
    after = snapshot(observed_paths)
    assert before == after, "Read-only checks changed original bytes or modification times"
    write("read-only-before.json", before)
    write("read-only-after.json", after)
    assert all(row["status"] == "current" for row in actual["checks"] if row["code"].startswith("bundle_"))
    assert all(row["status"] == "current" for row in actual["checks"] if row["code"].endswith(":identity"))
    assert actual["status"] in ("current", "needs_review")
    result["read_only"] = {"files_preserved_with_mtime": len(before), "archives": archives,
                           "distribution_receipt": ref(distribution), "actual_result": ref(OUT / "current-package-check.json"),
                           "descriptor_rejection": "A preliminary absolute Windows execution locator is rejected; the corrected registry uses an explicit repo-relative artifact locator. Original artifact bytes and failed diagnostic remain preserved."}
    assert WORK.resolve().is_relative_to((ROOT / "build").resolve()) and not WORK.exists()
    WORK.mkdir()
    sources = {}
    for target, source in captured["files"].items():
        name = source.relative_to(ROOT).as_posix()
        data = captured["snapshots"][target]
        assert name not in sources or sources[name] == data
        sources[name] = data
    sources["pyproject.toml"] = (ROOT / "pyproject.toml").read_bytes()
    write("parity-inputs.json", {name: sha(data) for name, data in sorted(sources.items())})
    outputs = {}
    for label, script in (("old", OUT / "build_plugin-before.py.txt"), ("new", ROOT / "scripts/build_plugin.py")):
        isolated = WORK / label
        isolated.mkdir()
        for name, data in sources.items():
            target = isolated / name
            assert target.resolve().is_relative_to(isolated.resolve())
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        namespace = {"__name__": "isolated_builder_" + label, "__file__": str(ROOT / "scripts/build_plugin.py")}
        exec(compile(script.read_bytes(), str(script), "exec"), namespace)
        namespace.update(ROOT=isolated, PLUGIN=isolated / "plugins/pixl")
        namespace["build"]()
        assert all((isolated / name).read_bytes() == data for name, data in sources.items()), "Build changed canonical input"
        outputs[label] = file_tree(isolated / "plugins/pixl")
        write("parity-" + label + ".json", outputs[label])
    assert outputs["old"] == outputs["new"], "Old/new isolated builds differ"
    assert outputs["new"]["bundle-manifest.json"] == actual["bundle"]["sha256"], "Isolated bundle differs from unchanged current kit"
    assert before == snapshot(observed_paths), "Isolated parity proof touched original release/evidence inputs"
    result["parity"] = {"isolated_roots": str(WORK), "source_files": len(sources),
                        "portable_output_files": len(outputs["new"]), "same_bytes": True,
                        "manifest_sha256": outputs["new"]["bundle-manifest.json"],
                        "live_bundle_unchanged": True}
    result["status"] = "pass"
except Exception as error:
    result.update(status="fail", error=type(error).__name__ + ": " + str(error), traceback=traceback.format_exc())
write("RESULT.json", result)
print(json.dumps({key: result[key] for key in ("status", "scope")}))
raise SystemExit(0 if result["status"] == "pass" else 1)
