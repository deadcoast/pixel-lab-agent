"""Rebuild reproducible evidence, execute the suite, and verify the final bundle."""

import io
import json
import platform
import sys
import unittest
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pixl.catalog import build as catalog
from pixl.codec import digest
from pixl.graph import file_hash, validate
from pixl.poc import run_all
from pixl.service import load_document
from scripts.benchmark import run as benchmark
from scripts.build_examples import build as examples
from scripts.build_knowledge import build as knowledge_library
from scripts.build_plugin import build as bundle

ORIGINAL_HASHES = {
    "links.md": "8d25924d3085fa0307f3cc698c252fb9195555885def82951bf070da770b37b8",
    "AGENT-PIXELART-TRAINING.md": "bb21cee0a39b504f7f4e56f61f13750b57178fe2b6230f27e79b28b40934a050",
    "pixel-art-deep-research-report.md": "3edf15db8c02eb3cc7225769416ef6924ef0ebe613cd3430a315389534434727",
    "research-pixel-art-systems.md": "3edf15db8c02eb3cc7225769416ef6924ef0ebe613cd3430a315389534434727",
    "PIXEL-ART-ASSETS.md": "450a335ed6563a7f4a5cc380f2bbe72f98b70e532ac2c8d16a679bcc545d4900"}


def write(name, data):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def verify():
    source_check = {name: file_hash(ROOT / name) == expected for name, expected in ORIGINAL_HASHES.items()}
    if not all(source_check.values()):
        raise RuntimeError(f"supplied source changed: {source_check!r}")
    index = catalog(ROOT)
    write("knowledge/source-catalog.json", index)
    methods = json.loads((ROOT / "knowledge/pixel-art.json").read_text(encoding="utf-8"))
    source_ranges = 0
    for method in methods["methods"]:
        for source in method["sources"]:
            lines = (ROOT / source["path"]).read_text(encoding="utf-8").splitlines()
            if not 1 <= source["start"] <= source["end"] <= len(lines):
                raise RuntimeError(f"invalid source range: {method['id']}")
            source_ranges += 1
    art = run_all(ROOT / "evidence/art-methods")
    library = knowledge_library()
    examples()
    bundle()
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), top_level_dir=str(ROOT))
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    (ROOT / "evidence/test-log.txt").write_text(stream.getvalue(), encoding="utf-8", newline="\n")
    measured = benchmark()
    write("evidence/representation-benchmark.json", measured)
    summary = {"status": "pass" if result.wasSuccessful() and art["status"] == "pass" else "fail",
               "observed_at": datetime.now(UTC).isoformat(),
               "python": platform.python_version(), "Pillow": version("Pillow"), "jsonschema": version("jsonschema"),
               "tests": {"run": result.testsRun, "passed": result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
                         "failures": len(result.failures), "errors": len(result.errors),
                         "skipped": [{"test": str(test), "reason": reason} for test, reason in result.skipped]},
               "art_pocs": {"total": len(art["checks"]), "passed": sum(c["status"] == "pass" for c in art["checks"]),
                            "methods_with_reference_checks": len({m for c in art["checks"] for m in c["method_ids"]})},
               "knowledge_methods": len(methods["methods"]), "validated_source_ranges": source_ranges,
               "knowledge_udl": library,
               "source_documents": len(index["documents"]), "duplicate_groups": len(index["duplicates"]),
               "original_source_hashes_unchanged": source_check,
               "runtime_hashes": {p.name: file_hash(p) for p in sorted((ROOT / "pixl").iterdir()) if p.suffix in (".py", ".json")},
               "example_hash": digest(validate(load_document(ROOT / "examples/atelier/project.px"), ROOT)),
               "limitations": ["One Windows symlink test may skip without OS privilege; all skips are listed.",
                               "Remote PixelLab generation, target-engine import and controlled model reasoning trials were not run.",
                               "Passing reference POCs cover declared fixture properties only."]}
    write("evidence/test-results.json", summary)
    bundle()
    print(json.dumps({k: summary[k] for k in ("status", "tests", "art_pocs", "knowledge_methods", "validated_source_ranges")}, indent=2))
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(verify())
