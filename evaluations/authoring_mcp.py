"""Real copied local runtime with explicit, once-only evaluation fault injections."""

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path


def install(root, events, production_plan, plar):
    original_links = production_plan._links
    original_prepare = production_plan.prepare

    def observed(kind):
        return events.exists() and any(
            json.loads(line)["kind"] == kind
            for line in events.read_text(encoding="utf-8").splitlines()
        )

    def record(kind, **details):
        with events.open("a", encoding="utf-8") as stream:
            stream.write(
                json.dumps(
                    {"kind": kind, "at": datetime.now(UTC).isoformat(), **details}
                )
                + "\n"
            )

    def interrupted_links(plan, folder, project, snapshot):
        if any(
            s.get("selection", {}).get("path") == "authoring-plar.txt"
            for s in plan["stages"]
        ) and not observed("allocation_write_interrupted"):
            record("allocation_write_interrupted", plan=plan["id"], snapshot=snapshot)
            raise OSError(
                "Evaluation event: allocation write interrupted after successful plan publication"
            )
        return original_links(plan, folder, project, snapshot)

    def prepare(*args, **kwargs):
        result = original_prepare(*args, **kwargs)
        if not observed("caller_requirement_updated"):
            path = root / "authoring-plar.txt"
            document = json.loads(path.read_text(encoding="utf-8"))
            before = plar.read(
                root,
                path="authoring-plar.txt",
                asset_id="queue.working",
                include_production=False,
            )
            asset = next(a for a in document["assets"] if a["id"] == "queue.working")
            asset["purpose"] += (
                " Caller update for this authoring branch: the reduced-motion mode must use a stationary Working symbol distinguishable from Ready and Paused. Confirm its consumer mapping before any further generation."
            )
            saved = plar.save(root, document, before["hash"], "authoring-plar.txt")
            after = plar.read(
                root,
                path="authoring-plar.txt",
                asset_id="queue.working",
                include_production=False,
            )
            (root / "AUTHORING-UPDATE.md").write_text(
                """# Scoped caller update after preparation
The authoring branch now requires reduced-motion support: a stationary Working
symbol distinct from Ready and Paused. Its consumer mapping needs comparison with
the existing source before a revised request. The older animation-only plan/request
remains retained, but cannot be treated as current without that comparison.
This is an explicit evaluation caller change, not a new requirement on the already
accepted original production. Do not remove or rewrite the prepared request or
claim revised acceptance. Report the changed requirement identity, observed local
blockers and the next concrete consumer/contract review. This assignment stops at
that truthful recovery; no additional generation is requested.
""",
                encoding="utf-8",
            )
            record(
                "caller_requirement_updated",
                previous_requirements=before["requirements_hash"],
                current_requirements=after["requirements_hash"],
                allocation_hash=saved["hash"],
            )
            result["evaluation_observation"] = {
                "kind": "caller_requirement_updated",
                "path": "AUTHORING-UPDATE.md",
                "asset": "queue.working",
            }
        return result

    production_plan._links = interrupted_links
    production_plan.prepare = prepare


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--kit", type=Path, required=True)
    parser.add_argument("--events", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.kit / "runtime"))
    os.environ["PIXL_PLUGIN_ROOT"] = str(args.kit)
    from pixl import mcp, plar, production_plan

    install(args.root, args.events, production_plan, plar)
    mcp.serve(args.root)


if __name__ == "__main__":
    main()
