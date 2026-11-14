"""SC-06 pre-fix adapter guards; disposable synthetic fixture, no art claim.

Run from the repository root with .venv/Scripts/python.exe and retain stdout.
Only TemporaryDirectory contents are mutated; existing evidence is untouched.
The receipt records the executing source hashes so later executions cannot be
mistaken for the original observation.
"""

import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from pixl import codec, production_plan, production_review, store
from tests.family_support import family
from tests.test_production_plan import plan


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def observed(call):
    try:
        return {"outcome": "returned", "value": call()}
    except Exception as error:
        return {"outcome": "raised", "type": type(error).__name__, "message": str(error)}


def main():
    result = {
        "version": 1,
        "scope": "SC-06 synthetic compatibility baseline; no native host, provider, art quality or human acceptance claim",
        "source_head": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "source_sha256": {
            name: sha(ROOT / name)
            for name in (
                "pixl/production_plan.py", "pixl/production_review.py",
                "tests/family_support.py", "tests/test_production_plan.py",
            )
        },
        "cases": {},
    }
    cases = result["cases"]
    with tempfile.TemporaryDirectory(prefix="pixl-sc06-baseline-") as temporary:
        root = Path(temporary)
        folder = root / ".pixl"
        family(root)
        current = store.load(folder)
        authored = plan()
        production_plan.author(folder, codec.digest(current), authored, root)
        current = store.load(folder)
        original_state = (folder / "state.px").read_bytes()
        marker = current.records["next.plan"]
        snapshot = root / marker.fields["ur"]
        original_snapshot = snapshot.read_bytes()

        cases["known_v1_clean"] = observed(
            lambda: production_plan.blockers(current, "next.motion.task", root, folder)
        )
        changed = copy.deepcopy(current)
        scope_id = next(iter(changed.records["next.plan"].fields["mt"]["scope"]))
        changed.records[scope_id].fields["nm"] += " (changed after authoring)"
        cases["known_v1_changed_scope"] = observed(
            lambda: production_plan.blockers(changed, "next.motion.task", root, folder)
        )
        future = copy.deepcopy(changed)
        future.records["next.plan"].fields["mt"]["binding"] = "pixl.production.plan/2"
        cases["future_binding_changed_scope"] = observed(
            lambda: production_plan.blockers(future, "next.motion.task", root, folder)
        )
        unrelated = copy.deepcopy(current)
        unrelated.records["next.plan"].fields["mt"]["binding"] = "example.unrelated/2"
        cases["unrelated_binding"] = observed(
            lambda: production_plan.blockers(unrelated, "next.motion.task", root, folder)
        )

        for label, value in (("future_wrapper", 2), ("numeric_v1_wrapper", 1.0)):
            replacement = json.loads(original_snapshot)
            replacement["version"] = value
            snapshot.write_text(json.dumps(replacement), encoding="utf-8")
            wrapped = copy.deepcopy(current)
            wrapped.records["next.plan"].fields["dg"] = sha(snapshot)
            cases[label] = observed(
                lambda: production_plan.blockers(wrapped, "next.motion.task", root, folder)
            )
        snapshot.write_bytes(original_snapshot)
        numeric_plan = copy.deepcopy(authored)
        numeric_plan["version"] = 1.0
        cases["numeric_v1_authored_schema"] = observed(
            lambda: production_plan._validate(numeric_plan, production_plan.SCHEMA)
        )

        comparison = {
            "review_scope_sha256": "scope",
            "criterion_comparisons": [{
                "criterion": "q.example", "record_sha256": "record",
                **{key: "Synthetic nonempty text; not semantic acceptance" for key in (
                    "source_obligation", "authority_basis", "scope", "literal_delta",
                    "discriminating_alternative", "disposition",
                )},
            }],
        }
        for label, version in (("legacy_unversioned_comparison", None), ("future_comparison", 2)):
            value = copy.deepcopy(comparison)
            if version is not None:
                value["version"] = version
            (root / "comparison.json").write_text(json.dumps(value), encoding="utf-8")
            cases[label] = observed(lambda: production_review._coverage(
                root, "comparison.json", "scope",
                [{"id": "q.example", "record_sha256": "record"}],
            ))
        result["retained_fixture_unchanged"] = {
            "state": (folder / "state.px").read_bytes() == original_state,
            "snapshot": snapshot.read_bytes() == original_snapshot,
        }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
