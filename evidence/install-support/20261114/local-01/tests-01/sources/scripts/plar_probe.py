"""Installed/copyable PLAR refresh and first-request probe, with local fixture observations."""

import hashlib
import json
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path


def run_plar_probe(cli, root):
    root = Path(root).resolve()

    def write(name, value):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        return {"path": name, "sha256": sha256(path.read_bytes()).hexdigest()}

    packet = cli(["plar", "read", "--root", str(root), "--asset", "queue.working"])
    arguments = {
        "description": "Four-frame queue activity loop, transparent, cool blue, distinct from success. Fixture preparation probe.",
        "width": 64,
        "height": 16,
        "no_background": True,
    }
    request = write("probe/arguments.json", arguments)
    plan = {
        "version": 1,
        "scope": "First working-loop candidate, local installation probe; no art acceptance",
        "outputs": [
            {
                "id": "working",
                "name": "Working loop",
                "kind": "animation",
                "contract": {
                    "size": [64, 16],
                    "palette": [],
                    "view": "ui",
                    "sampling": "nearest",
                    "alpha": "full",
                    "intent": "Scoped first candidate with four frames at 100 ms; verify packing at integration.",
                },
                "criteria": [
                    {
                        "id": "meaning",
                        "check": "Activity remains readable without implying completion at native and 3x scale.",
                        "domain": "visual",
                        "mode": "visual",
                        "basis": "Fixture BRIEF.md",
                        "scope": "Working candidate",
                        "sources": [
                            {
                                "path": "BRIEF.md",
                                "locator": "Activity, display and style requirements",
                                "lines": [3, 3],
                            }
                        ],
                    }
                ],
            }
        ],
    }
    criteria = write("probe/criteria.json", plan)
    review = {
        "version": 1,
        "requirements_hash": packet["requirements_hash"],
        "sources": [
            {"path": s["path"], "sha256": s["sha256"], "role": "consumer source"}
            for s in packet["sources"]
        ],
        "request": {
            **request,
            "kind": "provider_arguments",
            "tool": "create_image_pro_flash",
        },
        "criteria": criteria,
        "choices": [],
    }
    write("probe/request-review.json", review)
    resolved = cli(
        [
            "request-review",
            "probe/request-review.json",
            "--root",
            str(root),
            "--asset",
            "queue.working",
        ]
    )
    if (
        resolved["request"]["arguments"] != arguments
        or resolved["source_evidence"][0]["status"] != "resolved"
        or resolved["consistent"] is not None
    ):
        raise RuntimeError(
            "installed request/criteria evidence resolution lost identity or claimed acceptance"
        )

    connection = {
        "provider": "pixellab",
        "schema": {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "width": {"type": "integer"},
                "height": {"type": "integer"},
                "no_background": {"type": "boolean"},
            },
            "required": ["description", "width", "height", "no_background"],
            "additionalProperties": False,
        },
        "discovery": {
            "source": "Installed-operation fixture schema",
            "observed_at": datetime.now(UTC).isoformat(),
            "evidence": {"fixture": True},
        },
        "authorization": {
            "scope": "Local installation probe with synthetic observations",
            "evidence": {"fixture": True},
        },
    }
    write("probe/connection.json", connection)
    command = [
        "plar",
        "prepare",
        "--root",
        str(root),
        "--asset",
        "queue.working",
        "--requirements",
        packet["requirements_hash"],
        "--packet",
        "probe/request-review.json",
        "--connection",
        "probe/connection.json",
    ]
    prepared = cli(command)
    if (
        prepared["job"]["request"]["arguments"] != arguments
        or prepared["remote_executed"]
    ):
        raise RuntimeError("installed preparation changed the request")
    packet = cli(["plar", "read", "--root", str(root), "--asset", "queue.working"])
    if (
        packet["production"]["pending_jobs"] != [prepared["job"]["id"]]
        or packet["production"]["continuation"]["before_another_request"][0]["job"]
        != prepared["job"]["id"]
        or prepared["allocation"]["status"] != "linked"
    ):
        raise RuntimeError("prepared work was not connected to its allocation")
    write("probe/handoff-details.json", {"status": "partial", "future_work": ["Inspect the actual candidate"]})
    handoff = cli(["plar", "handoff", str(root / "probe/handoff-details.json"),
                   "--root", str(root), "--asset", "queue.working",
                   "--requirements", packet["requirements_hash"], "--expect", prepared["hash"]])
    handoff_bytes = (root / handoff["path"]).read_bytes()
    handoff_document = json.loads(handoff_bytes)
    if (hashlib.sha256(handoff_bytes).hexdigest() != handoff["sha256"]
            or handoff_document["resume"] != packet["production"]["continuation"]
            or handoff_document["next"] != packet["production"]["next_action"]):
        raise RuntimeError("installed handoff lost the exact continuation")
    caller = cli(["plar", "handoff", str(root / "probe/handoff-details.json"),
                  "--root", str(root), "--asset", "queue.working",
                  "--requirements", packet["requirements_hash"], "--expect", packet["production"]["continuation"]["state_hash"],
                  "--view", "caller", "--result-path", "probe/caller-result.json"])
    saved_caller = json.loads((root / caller["result_path"]).read_bytes())
    if (caller["path"] != handoff["path"] or caller["sha256"] != handoff["sha256"]
            or caller["assignment"]["status"] != "partial" or caller["caller"]["present"]
            or caller["resume_ref"]["sha256"] != handoff["sha256"]
            or caller["next"] != handoff["next"] or saved_caller["resume_ref"] != caller["resume_ref"]):
        raise RuntimeError("installed caller view/export lost immutable receipt or continuation")
    write("probe/preparation.json", prepared)
    document = json.loads((root / "plar.txt").read_text(encoding="utf-8"))
    working = next(r for r in document["assets"] if r["id"] == "queue.working")
    working.update(
        status="in_progress",
        next="Continue the prepared request",
        production={
            "store": prepared["store"],
            "task": prepared["task"],
            "output": prepared["outputs"][0],
        },
        evidence=working["evidence"]
        + [
            {
                "path": "probe/preparation.json",
                "note": "Actual local preparation receipt; no provider or image acceptance",
            }
        ],
    )
    write("probe/update.json", document)
    linked = cli(
        [
            "plar",
            "save",
            str(root / "probe/update.json"),
            "--root",
            str(root),
            "--expect",
            packet["hash"],
        ]
    )
    state = root / prepared["store"] / "state.px"
    original_state = state.read_bytes()
    original_working = json.dumps(working, sort_keys=True)
    write(
        "probe/retry-note.json",
        {
            "observation": "Scoped inspection note for retry only; other visual roles unchanged."
        },
    )
    document["sources"].append({"id": "retry-note", "path": "probe/retry-note.json"})
    retry = next(r for r in document["assets"] if r["id"] == "queue.retry")
    retry["requirements"].append(
        {
            "property": "inspection_note",
            "value": "Review retry in its existing failure role",
            "authority": "observation",
            "sources": ["retry-note"],
            "reason": "Synthetic scoped update for allocation isolation.",
        }
    )
    write("probe/update.json", document)
    refreshed = cli(
        [
            "plar",
            "save",
            str(root / "probe/update.json"),
            "--root",
            str(root),
            "--expect",
            linked["hash"],
        ]
    )
    retained = json.loads((root / "plar.txt").read_text(encoding="utf-8"))
    if (
        refreshed["changes"]["affected_assets"] != ["queue.retry"]
        or json.dumps(
            next(r for r in retained["assets"] if r["id"] == "queue.working"),
            sort_keys=True,
        )
        != original_working
        or state.read_bytes() != original_state
    ):
        raise RuntimeError(
            "scoped refresh changed unrelated requirements or production history"
        )
    if cli(command)["hash"] != prepared["hash"]:
        raise RuntimeError("unrelated queue update changed prepared identity")
    dispatched = cli(
        [
            "job-dispatch",
            str(state.parent),
            "first_request",
            "--root",
            str(root),
            "--expect",
            prepared["hash"],
        ]
    )
    if dispatched["dispatch_request"]["arguments"] != arguments:
        raise RuntimeError("dispatch changed reviewed arguments")
    original_view = (root / "src/queue-view.ts").read_bytes()
    (root / "src/queue-view.ts").write_bytes(
        original_view
        + b"\n// Source changed after the retained local dispatch claim.\n"
    )
    write(
        "probe/observation.json",
        {"fixture": "Synthetic submitted observation; no provider call"},
    )
    observed = cli(
        [
            "job-observe",
            str(state.parent),
            "first_request",
            "submitted",
            str(root / "probe/observation.json"),
            "--remote-id",
            "fixture-installed-request",
            "--root",
            str(root),
            "--expect",
            dispatched["hash"],
        ]
    )
    report = cli(["jobs", str(state), "--root", str(root)])
    retained_view = root / prepared["retained_inputs"]["src/queue-view.ts"]["path"]
    if (
        observed["job"]["state"] != "submitted"
        or report["jobs"][0]["selection_bindings"][0]["status"] != "changed"
        or retained_view.read_bytes() != original_view
    ):
        raise RuntimeError(
            "changed source obstructed observation or lost original bytes"
        )
    focused = cli(["plar", "read", "--root", str(root), "--asset", "queue.working"])
    if (
        focused["production"]["next_action"] != "observe"
        or focused["production"]["selection_current"]
    ):
        raise RuntimeError("cold allocation report lost changed-source pending work")
    write(
        "probe/terminal.json",
        {
            "fixture": "Synthetic terminal failure of the retained request; no provider cancellation is implied."
        },
    )
    terminal = cli(
        [
            "job-observe",
            str(state.parent),
            "first_request",
            "failed",
            str(root / "probe/terminal.json"),
            "--root",
            str(root),
            "--expect",
            observed["hash"],
        ]
    )
    changed = json.loads((root / "plar.txt").read_bytes())
    for source in changed["sources"]:
        if source["path"] == "src/queue-view.ts":
            source.pop("sha256", None)
    write("probe/revised-allocation.json", changed)
    cli(
        [
            "plar",
            "save",
            str(root / "probe/revised-allocation.json"),
            "--root",
            str(root),
            "--expect",
            focused["hash"],
        ]
    )
    selected = cli(["plar", "read", "--root", str(root), "--asset", "queue.working"])
    revised_arguments = {
        **arguments,
        "description": f"{arguments['description']} Current consumer revision.",
    }
    review["requirements_hash"] = selected["requirements_hash"]
    review["sources"] = [
        {"path": row["path"], "sha256": row["sha256"], "role": "consumer source"}
        for row in selected["sources"]
    ]
    review["request"].update(write("probe/arguments-r2.json", revised_arguments))
    write("probe/request-review-r2.json", review)
    revised = cli(
        [
            "plar",
            "prepare",
            "--root",
            str(root),
            "--asset",
            "queue.working",
            "--requirements",
            selected["requirements_hash"],
            "--packet",
            "probe/request-review-r2.json",
            "--connection",
            "probe/connection.json",
            "--revise",
            "--expect",
            terminal["hash"],
        ]
    )
    current = cli(["plar", "read", "--root", str(root), "--asset", "queue.working"])
    if (
        revised["task"] == prepared["task"]
        or revised["job"]["request"]["arguments"] != revised_arguments
        or current["asset"]["production"]["task"] != revised["task"]
        or len(current["production"]["jobs"]) != 2
        or retained_view.read_bytes() != original_view
        or not current["production"]["selection_current"]
    ):
        raise RuntimeError(
            "revised preparation lost old work or current allocation identity"
        )
    return {
        "status": "pass",
        "checks": [
            "selected artifact to exact prepared request",
            "exact source excerpts for independent caller comparison without automatic consistency",
            "provider-bound pending prerequisite in resumable handoff",
            "immutable exact handoff preserves continuation and expert details",
            "compact caller view and export preserve exact immutable continuation",
            "populated production/evidence links survive unrelated scoped refresh",
            "prepared state unchanged by unrelated allocation update",
            "unchanged preparation resumes without duplicate",
            "exact dispatch payload",
            "existing job remains observable after source change",
            "retained source bytes remain exact",
            "first preparation links allocation with pending job",
            "cold selection reports changed requirements and original pending identity",
            "explicit terminal observation permits reviewed revision",
            "revised generation links current work and preserves original job and inputs",
        ],
        "scope": "Local installed operation with synthetic schema/observation; no model judgment, provider execution, generated image or engine acceptance",
    }
