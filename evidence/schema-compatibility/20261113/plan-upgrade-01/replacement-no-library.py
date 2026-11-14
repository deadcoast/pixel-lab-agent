"""Replace the kit after proving this consumer has no kit-library S bindings.

The failed public retention attempt is retained separately. No source retention
is needed when no source record names the kit's resources; do not create one.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.parse import urlsplit

from replay import COMPARISON, EVIDENCE, PLAN, PROJECT, REPO, SOURCE, STATE, WORK, digest, inventory, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kit", type=Path, required=True)
    args = parser.parse_args()
    kit = PROJECT / ".agents/skills/pixl-kit"
    archived = WORK / "original-kit"
    before = inventory(PROJECT)
    original = json.loads((EVIDENCE / "original-files.json").read_text())
    old = json.loads((EVIDENCE / "old-stdout.json").read_text())
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(kit / "runtime"))
    from pixl import codec, graph
    doc = codec.parse((PROJECT / STATE).read_bytes())
    sources = [{"id": row.id, "uri": row.fields["ur"], "sha256": row.fields["dg"]}
               for row in doc.records.values() if row.kind == "S"]
    library = [row for row in sources if not urlsplit(row["uri"]).scheme
               and graph.confined(PROJECT, row["uri"]).is_relative_to(kit / "resources")]
    audit = {"version": 1, "state_sha256": digest(PROJECT / STATE), "source_records": sources,
             "sources_in_replaced_kit_resources": library,
             "conclusion": "No kit-library source dependency requires retention" if not library else "Retention required"}
    save("source-dependencies.json", audit)
    if library:
        raise RuntimeError("Kit-library sources must be retained before replacement")
    # Both resolved recursive move targets are verified inside the named workspace.
    if kit.resolve() != (WORK / "project/.agents/skills/pixl-kit").resolve() or not kit.resolve().is_relative_to(WORK.resolve()):
        raise RuntimeError("Unexpected kit move source")
    if archived.exists() or not archived.resolve().is_relative_to(WORK.resolve()):
        raise RuntimeError("Preserve existing old kit or reject outside target")
    old_kit = inventory(kit)
    shutil.move(str(kit.resolve()), str(archived.resolve()))
    shutil.copytree(args.kit.resolve(), kit)
    new_kit = inventory(kit)
    installed = inventory(PROJECT)
    argv = [sys.executable, str(kit / "scripts/pixl.py"), "request-review", STATE,
            "--plan", PLAN, "--comparison", COMPARISON, "--root", str(PROJECT)]
    run = subprocess.run(argv, cwd=PROJECT, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), capture_output=True, text=True)
    for suffix, value in (("stdout.json", run.stdout), ("stderr.txt", run.stderr)):
        output = EVIDENCE / f"replacement-{suffix}"
        if output.exists():
            raise RuntimeError("Preserve previous run output")
        output.write_text(value, encoding="utf-8")
    report = json.loads(run.stdout) if run.returncode == 0 else None
    after = inventory(PROJECT)
    prefix = ".agents/skills/pixl-kit/"
    receipt = {
        "version": 1, "argv": argv, "exit_code": run.returncode,
        "scope": "Actual kit replacement at the same copied-consumer path. No kit-resource S dependencies require retention; the inapplicable public retention failure is preserved. No plan/state/art/acceptance edits or new provider/native model execution.",
        "old_kit_preserved": inventory(archived) == old_kit,
        "original_consumer_unchanged": inventory(SOURCE) == original,
        "all_nonkit_files_unchanged_across_replacement": {p:h for p,h in before.items() if not p.startswith(prefix)} == {p:h for p,h in after.items() if not p.startswith(prefix)},
        "review_read_only": installed == after,
        "new_kit_unchanged": inventory(kit) == new_kit,
        "old_manifest_sha256": digest(archived / "bundle-manifest.json"),
        "new_manifest_sha256": digest(kit / "bundle-manifest.json"),
        "new_runtime_sha256": {p: digest(kit / "runtime/pixl" / p) for p in ("adapter_versions.py", "production_plan.py", "production_review.py")},
        "state_file_sha256": digest(PROJECT / STATE),
        "same_saved_plan_identity": report is not None and old["plan"] == report["plan"],
        "same_review_scope": report is not None and old["review_scope_sha256"] == report["review_scope_sha256"],
        "same_criteria": report is not None and old["criteria"] == report["criteria"],
        "same_coverage": report is not None and old["comparison_coverage"] == report["comparison_coverage"],
        "same_diagnostics": report is not None and old["diagnostics"] == report["diagnostics"],
        "same_report": report == old,
        "comparison_coverage": report.get("comparison_coverage") if report else None,
        "consistent": report.get("consistent") if report else None,
        "script_sha256": digest(Path(__file__)),
        "prior_script_sha256": {name: digest(EVIDENCE / name) for name in ("replay.py", "replace-kit.py")},
    }
    save("replacement-result.json", receipt)
    save("replaced-files.json", after)
    print(json.dumps(receipt, indent=2))
    if run.returncode:
        raise SystemExit(run.returncode)


if __name__ == "__main__":
    main()
