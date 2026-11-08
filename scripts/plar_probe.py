"""Installed/copyable PLAR refresh and first-request probe, with local fixture observations."""

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
        evidence=[
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
    return {
        "status": "pass",
        "checks": [
            "selected artifact to exact prepared request",
            "populated production/evidence links survive unrelated scoped refresh",
            "prepared state unchanged by unrelated allocation update",
            "unchanged preparation resumes without duplicate",
            "exact dispatch payload",
            "existing job remains observable after source change",
            "retained source bytes remain exact",
        ],
        "scope": "Local installed operation with synthetic schema/observation; no model judgment, provider execution, generated image or engine acceptance",
    }
