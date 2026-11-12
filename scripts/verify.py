"""Rebuild local proofs, run the full suite and distribution checks, retaining each attempt."""

import io
import json
import logging
import platform
import sys
import traceback
import unittest
import zipfile
from datetime import UTC, datetime
from hashlib import sha256
from importlib.metadata import version
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
logger = logging.getLogger(__name__)


def write(name, data):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def _verify(summary, run, stage):
    stage("sources")
    # Import after recording this attempt: dependency/preflight errors must not leave an old pass.
    from pixl.catalog import build as catalog
    from pixl.codec import digest
    from pixl.graph import file_hash, validate
    from pixl.poc import run_all
    from pixl.service import load_document
    from pixl.sources import load_inventory
    from scripts.benchmark import run as benchmark
    from scripts.build_examples import build as examples
    from scripts.build_intake_example import build as intake_example
    from scripts.build_knowledge import build as knowledge_library
    from scripts.build_plugin import build as bundle
    from scripts.check_wheel import run as check_wheel

    inventory = load_inventory(ROOT)
    source_check = {row["path"]: True for row in inventory["documents"]}
    index = catalog(ROOT)
    write("knowledge/source-catalog.json", index)
    methods = json.loads(
        (ROOT / "knowledge/pixel-art.json").read_text(encoding="utf-8")
    )
    source_ranges = 0
    for method in methods["methods"]:
        for source in method["sources"]:
            lines = (ROOT / source["path"]).read_text(encoding="utf-8").splitlines()
            if not 1 <= source["start"] <= source["end"] <= len(lines):
                raise RuntimeError(f"invalid source range: {method['id']}")
            source_ranges += 1
    stage("references")
    art = run_all(ROOT / "evidence/art-methods")
    write(run / "art-pocs.json", art)
    summary["art_pocs"] = {
        "status": art["status"],
        "total": len(art["checks"]),
        "passed": sum(c["status"] == "pass" for c in art["checks"]),
    }
    if art["status"] != "pass":
        raise RuntimeError("Reference proofs failed; inspect art-pocs.json")
    library = knowledge_library()
    examples()
    intake_example()
    stage("bundle")
    bundle()
    stage("tests")
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(
        str(ROOT / "tests"), top_level_dir=str(ROOT)
    )
    summary["test_inventory"] = list(test_ids(suite))
    if not summary["test_inventory"]:
        raise RuntimeError(
            "No tests discovered; an empty suite cannot verify this repository"
        )
    summary["checked_input_hashes"] = {
        p.relative_to(ROOT).as_posix(): file_hash(p)
        for folder in ("pixl", "scripts", "tests", "evaluations")
        for p in sorted((ROOT / folder).rglob("*.py"))
        if "__pycache__" not in p.parts
    }
    for name in (
        "setup.py",
        "pyproject.toml",
        "uv.lock",
        "MANIFEST.in",
        "pixl/registry.json",
        "pixl/registry-v2.json",
        "spec/PIXL-1.md",
        "spec/PIXL-2.md",
        "training/source-inventory.json",
        "knowledge/pixel-art.json",
        *(p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "examples/plar-project/renderer").iterdir()) if p.is_file()),
        *(p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "examples/consumer-execution").rglob("*")) if p.is_file() and "__pycache__" not in p.parts),
        *(p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "examples/delegation/renderer").iterdir()) if p.is_file()),
        "spec/consumer-execution.md",
        *(row["path"] for row in inventory["documents"]),
    ):
        summary["checked_input_hashes"][name] = file_hash(ROOT / name)
    summary["tests"] = {
        "status": "running",
        "discovered": len(summary["test_inventory"]),
    }
    write(run / "result.json", summary)
    write("evidence/test-results.json", summary)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    (ROOT / "evidence/test-log.txt").write_text(
        stream.getvalue(), encoding="utf-8", newline="\n"
    )
    (run / "test-log.txt").write_text(stream.getvalue(), encoding="utf-8", newline="\n")
    summary["tests"] = {
        "status": "pass" if result.wasSuccessful() else "fail",
        "discovered": len(summary["test_inventory"]),
        "run": result.testsRun,
        "passed": result.testsRun
        - len(result.failures)
        - len(result.errors)
        - len(result.skipped),
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": [
            {"test": str(test), "reason": reason} for test, reason in result.skipped
        ],
    }
    if not result.wasSuccessful() or result.testsRun != len(summary["test_inventory"]):
        raise RuntimeError(
            "Full unittest suite failed or did not execute every discovered test; inspect test-log.txt"
        )
    stage("benchmark")
    measured = benchmark()
    write("evidence/representation-benchmark.json", measured)
    write(run / "representation-benchmark.json", measured)
    summary.update(
        {
            "observed_at": datetime.now(UTC).isoformat(),
            "python": platform.python_version(),
            "Pillow": version("Pillow"),
            "jsonschema": version("jsonschema"),
            "art_pocs": {
                "status": art["status"],
                "total": len(art["checks"]),
                "passed": sum(c["status"] == "pass" for c in art["checks"]),
                "methods_with_reference_checks": len(
                    {m for c in art["checks"] for m in c["method_ids"]}
                ),
            },
            "knowledge_methods": len(methods["methods"]),
            "validated_source_ranges": source_ranges,
            "knowledge_udl": library,
            "source_documents": len(index["documents"]),
            "duplicate_groups": len(index["duplicates"]),
            "source_inventory_sha256": file_hash(
                ROOT / "training/source-inventory.json"
            ),
            "declared_source_revisions_verified": source_check,
            "runtime_hashes": {
                p.name: file_hash(p)
                for p in sorted((ROOT / "pixl").iterdir())
                if p.suffix in (".py", ".json")
            },
            "example_hash": digest(
                validate(load_document(ROOT / "examples/atelier/project.px"), ROOT)
            ),
        }
    )
    bundle()
    summary["bundle_manifest_sha256"] = file_hash(
        ROOT / "plugins/pixl/bundle-manifest.json"
    )
    stage("distribution")
    summary["distribution"] = check_wheel(log_dir=run)
    write("evidence/wheel-check.json", summary["distribution"])
    write(run / "wheel-check.json", summary["distribution"])
    for name, expected in summary["checked_input_hashes"].items():
        if file_hash(ROOT / name) != expected:
            raise RuntimeError(f"Checked source changed during verification: {name}")


def test_ids(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from test_ids(test)
        else:
            yield test.id()


def archive_previous(destination):
    """Preserve outputs that this verifier or its tests can regenerate."""
    paths: set[Path] = set()
    for name in (
        "knowledge",
        "examples",
        "evidence/art-methods",
        "plugins/pixl/runtime",
        "plugins/pixl/resources",
    ):
        paths.update(
            p
            for p in (ROOT / name).rglob("*")
            if p.is_file() and "__pycache__" not in p.parts
        )
    paths.update(p for p in (ROOT / "evidence").glob("*") if p.is_file())
    for name in ("plugins/pixl/bundle-manifest.json", "plugins/pixl/requirements.txt"):
        if (ROOT / name).is_file():
            paths.add(ROOT / name)
    manifest = {}
    with zipfile.ZipFile(
        destination / "previous.zip", "x", zipfile.ZIP_DEFLATED
    ) as archive:
        for path in sorted(paths):
            name = path.relative_to(ROOT).as_posix()
            data = path.read_bytes()
            archive.writestr(name, data)
            manifest[name] = sha256(data).hexdigest()
    write(destination / "previous-manifest.json", manifest)


def verify():
    run = (
        ROOT
        / "evidence/verification-runs"
        / datetime.now(UTC).strftime("%Y%m%dT%H%M%S.%fZ")
    )
    run.mkdir(parents=True, exist_ok=False)
    summary: dict[str, Any] = {
        "status": "running",
        "observed_at": datetime.now(UTC).isoformat(),
        "python": platform.python_version(),
        "executable": sys.executable,
        "run_directory": run.relative_to(ROOT).as_posix(),
        "stage": "archive",
        "stages": {
            name: "not_run"
            for name in (
                "archive",
                "sources",
                "references",
                "bundle",
                "tests",
                "benchmark",
                "distribution",
            )
        },
        "tests": {"status": "not_run"},
        "art_pocs": {"status": "not_run"},
        "distribution": {"status": "not_run"},
        "limitations": [
            "Full unittest discovery executes the listed tests, not every possible behavior of each module.",
            "File hashes establish input identity, not line or branch coverage; read coverage from its separate measurement.",
            "Passing reference POCs cover declared fixture properties only.",
            "Relocation and scripted CLI/MCP fixtures exercise local mechanics, not model instruction following.",
            "Remote PixelLab execution, visual acceptance, target-engine import and new model trials were not run.",
            "Lint and static typing are separate commands; this report does not certify them.",
        ],
    }

    def persist():
        write(run / "result.json", summary)
        write("evidence/test-results.json", summary)

    def stage(name):
        previous = summary["stage"]
        if summary["stages"][previous] == "running":
            summary["stages"][previous] = "pass"
        summary["stage"] = name
        summary["stages"][name] = "running"
        persist()

    try:
        summary["stages"]["archive"] = "running"
        archive_previous(run)
        _verify(summary, run, stage)
        summary["stages"][summary["stage"]] = "pass"
        summary["status"] = "pass"
    except (Exception, KeyboardInterrupt, SystemExit) as error:
        logger.exception("Verification failed during %s", summary["stage"])
        summary.update(status="fail", error=f"{type(error).__name__}: {error}")
        summary["stages"][summary["stage"]] = "fail"
        (run / "error.txt").write_text(traceback.format_exc(), encoding="utf-8")
    finally:
        summary["finished_at"] = datetime.now(UTC).isoformat()
        persist()
    print(
        json.dumps(
            {
                k: summary[k]
                for k in ("status", "stage", "run_directory", "tests", "art_pocs")
            },
            indent=2,
        )
    )
    if summary["status"] != "pass":
        print(summary["error"], file=sys.stderr)
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(verify())
