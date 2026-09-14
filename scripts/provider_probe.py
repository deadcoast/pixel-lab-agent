"""Shared distribution probe using only public CLI calls and synthetic host data.

The caller supplies its installed-wheel or copied-plugin isolated runner. This
module never imports the source runtime or executes a provider tool.
"""

import json
from hashlib import sha256
from pathlib import Path

from PIL import Image


def run_provider_probe(invoke, project):
    project = Path(project)
    checks = []

    def cli(label, *arguments):
        result = invoke(list(arguments))
        checks.append({"command": arguments[0], "check": label, "status": "pass"})
        return result

    def require(condition, message):
        if not condition:
            raise RuntimeError(f"provider distribution probe: {message}")

    def write_json(name, value):
        (project / name).write_text(json.dumps(value), encoding="utf-8")
        return name

    def ref(id_):
        return {"$ref": id_}

    def symbol(value):
        return {"$symbol": value}

    root = str(project)
    folder = ".provider-fixture"
    state = folder + "/state.px"
    initialized = cli(
        "initialize synthetic PX2 intake",
        "intake",
        folder,
        "--root",
        root,
        "--brief",
        "Distribution fixture only; no real provider, art or engine acceptance.",
    )
    plan = cli("read saved PX2 intake", "decode", state)
    require(plan["format"] == 2, "intake did not retain PX2")
    records = plan["records"]

    def add(id_, kind, fields):
        records.append({"id": id_, "kind": kind, "fields": fields})
        return ref(id_)

    source_path = project / "provider-brief.txt"
    source_path.write_text(
        "Synthetic local distribution fixture; no paid generation or art acceptance.\n",
        encoding="utf-8",
    )
    source = add(
        "fixture_source",
        "S",
        {
            "ur": source_path.name,
            "dg": sha256(source_path.read_bytes()).hexdigest(),
            "ln": [1, 1],
            "at": "2026-09-11",
            "au": symbol("local"),
        },
    )
    choice = add(
        "fixture_choice",
        "I",
        {
            "pr": ref("project"),
            "wh": ref("user"),
            "ky": "px",
            "st": symbol("proposed"),
            "vl": [2, 2],
            "so": [source],
            "wy": "A tiny fixture exercises storage only; this is not an art recommendation.",
        },
    )
    contract = add(
        "fixture_contract",
        "C",
        {
            "nm": "Synthetic distribution raster",
            "px": [2, 2],
            "pl": [],
            "vw": symbol("side"),
            "sa": symbol("nearest"),
            "al": symbol("binary"),
            "li": "Synthetic fixture; no aesthetic claim.",
            "ch": [choice],
        },
    )
    project_record = next(row for row in records if row["id"] == "project")
    project_record["fields"]["sc"] = [source]
    project_record["fields"]["in"] = [choice]
    criteria = []
    for domain, mode, condition in (
        ("mechanical", "local", "The actual raster measures 2 by 2."),
        ("visual", "visual", "A reviewer accepts the fixture's native appearance."),
        ("engine", "live", "The target engine accepts sampling, scale and alpha."),
    ):
        criteria.append(
            add(
                "fixture_" + domain,
                "Q",
                {
                    "nm": condition,
                    "dm": symbol(domain),
                    "md": symbol(mode),
                    "ck": condition,
                    "wh": ref("user"),
                    "so": [source],
                },
            )
        )
    output = add(
        "fixture_output",
        "F",
        {
            "tk": ref("fixture_task"),
            "nm": "Synthetic planned sprite",
            "kd": symbol("sprite"),
            "ct": contract,
            "rq": criteria,
        },
    )
    add(
        "fixture_task",
        "T",
        {
            "nm": "Exercise local provider recovery",
            "ow": ref("actor"),
            "pr": ref("project"),
            "dp": [],
            "dc": [],
            "kn": [],
            "st": symbol("open"),
            "ph": symbol("sample"),
            "ip": [],
            "op": [output],
            "ca": [],
            "vr": [],
        },
    )
    plan["revision"] += 1
    plan_json = write_json("provider-plan.json", plan)
    cli("encode the fixture plan", "encode", plan_json, "--out", "provider-plan.px")
    published = cli(
        "save the plan before intent",
        "commit",
        folder,
        "provider-plan.px",
        "--expect",
        initialized["hash"],
        "--root",
        root,
    )
    request = {
        "provider": "fictional-distribution-fixture",
        "tool": "generate_distribution_fixture",
        "arguments": {"description": "Synthetic local recovery fixture"},
        "schema": {
            "type": "object",
            "properties": {"description": {"type": "string"}},
            "required": ["description"],
            "additionalProperties": False,
        },
        "discovery": {
            "source": "Synthetic fixture tools/list",
            "observed_at": "2026-09-11T12:00:00+00:00",
            "evidence": {"fixture": True},
        },
        "authorization": {
            "scope": "Local distribution check only; no real provider execution",
            "evidence": {"fixture": True},
        },
    }
    request_json = write_json("provider-request.json", request)
    evidence_json = write_json(
        "provider-observation.json",
        {
            "fixture": "Synthetic caller observation; not a real provider response",
        },
    )
    prepared = cli(
        "persist exact synthetic intent",
        "job-prepare",
        folder,
        "fixture_job",
        "fixture_task",
        request_json,
        "--outputs",
        "fixture_output",
        "--expect",
        published["hash"],
        "--root",
        root,
    )
    require(prepared["job"]["state"] == "prepared", "intent not prepared")
    require("dispatch_request" not in prepared, "prepare granted dispatch")
    require(prepared["remote_executed"] is False, "prepare claimed remote execution")
    dispatched = cli(
        "publish dispatch claim before request handoff",
        "job-dispatch",
        folder,
        "fixture_job",
        "--expect",
        prepared["hash"],
        "--root",
        root,
    )
    require(
        dispatched["job"]["state"] == "unknown", "dispatch did not retain uncertainty"
    )
    require(dispatched["remote_executed"] is False, "dispatch claimed remote execution")
    require(
        all(
            dispatched["dispatch_request"][key] == value
            for key, value in request.items()
        ),
        "dispatch changed the saved host request",
    )
    cold = cli(
        "recover unknown submission in a new process", "jobs", state, "--root", root
    )
    retained = cold["jobs"][0]
    require(
        cold["hash"] == dispatched["hash"] and cold["files_verified"],
        "cold read lost publication",
    )
    require(
        retained["state"] == "unknown" and retained["next_action"] == "reconcile",
        "cold read did not require reconciliation",
    )
    require(
        "dispatch_request" not in cold and cold["remote_executed"] is False,
        "cold read granted execution",
    )
    require(
        retained["request"] == dispatched["dispatch_request"],
        "cold read lost the exact request",
    )
    observed = cli(
        "retain supplied success and synthetic identity",
        "job-observe",
        folder,
        "fixture_job",
        "succeeded",
        evidence_json,
        "--remote-id",
        "synthetic-remote-id",
        "--expect",
        cold["hash"],
        "--root",
        root,
    )
    require(
        observed["job"]["remote_id"] == "synthetic-remote-id",
        "remote identity not retained",
    )
    require(
        observed["remote_executed"] is False, "observation claimed remote execution"
    )
    download = project / "provider-download.png"
    Image.new("RGBA", (2, 2), "magenta").save(download)
    imported = cli(
        "import actual local candidate bytes",
        "job-import",
        folder,
        "fixture_job",
        "fixture_output",
        "fixture_candidate",
        download.name,
        evidence_json,
        "--expect",
        observed["hash"],
        "--root",
        root,
    )
    require(
        imported["job"]["candidates"][0]["id"] == "fixture_candidate",
        "candidate not linked to job",
    )
    require(imported["remote_executed"] is False, "import claimed remote execution")
    decoded = cli("verify imported candidate identity and bytes", "decode", state)
    candidate = next(
        row["fields"] for row in decoded["records"] if row["id"] == "fixture_candidate"
    )
    require(
        candidate["of"] == ref("fixture_output") and candidate["ct"] == contract,
        "candidate links changed",
    )
    copied = (project / candidate["ur"]).resolve()
    require(
        copied.is_relative_to((project / folder).resolve()),
        "candidate was not snapshotted into store",
    )
    require(
        copied.read_bytes() == download.read_bytes(), "candidate snapshot bytes differ"
    )
    require(
        candidate["dg"] == sha256(download.read_bytes()).hexdigest(),
        "candidate hash differs",
    )
    task = next(
        row["fields"] for row in decoded["records"] if row["id"] == "fixture_task"
    )
    require(
        task["st"] == symbol("open") and task["ca"] == [] and task["vr"] == [],
        "import invented acceptance or completion",
    )
    workflow = cli(
        "retain all acceptance obligations as unperformed",
        "workflow",
        state,
        "--root",
        root,
    )
    planned = workflow["tasks"][0]["outputs"][0]
    require(workflow["files_verified"], "workflow skipped candidate file verification")
    require(planned["candidate"] is None, "import nominated a candidate")
    requirements = planned["candidates"][0]["requirements"]
    require(
        len(requirements) == 3
        and {row["status"] for row in requirements} == {"unperformed"},
        "import fabricated mechanical, visual or engine acceptance",
    )
    return {
        "status": "pass",
        "checks": checks,
        "remote_executed": False,
        "scope": "Separate isolated CLI processes; synthetic discovery, authorization and observations; local raster import; no real provider, visual or engine acceptance.",
    }
