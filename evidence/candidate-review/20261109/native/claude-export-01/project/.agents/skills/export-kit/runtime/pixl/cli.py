"""Command entry point. JSON is host interchange; context/encode emit PIXL."""

import argparse
import json
import sys
from pathlib import Path

from . import codec, graph, jobs, service, store
from .codec import PixlError


def parser():
    p = argparse.ArgumentParser(
        prog="pixl",
        description="PIXL agent project state and pixel-art tools (PX1/PX2)",
    )
    sub = p.add_subparsers(dest="command", required=True)
    q = sub.add_parser("validate")
    q.add_argument("path")
    q.add_argument("--root")
    q = sub.add_parser("context")
    q.add_argument("path")
    q.add_argument("focus")
    q.add_argument("--budget", type=int)
    q.add_argument("--view", choices=("complete", "authoring"), default="complete")
    q.add_argument("--plar", dest="plar_path")
    q.add_argument("--asset", dest="asset_id")
    q.add_argument("--root")
    q = sub.add_parser("request-review", help="Resolve exact request/criteria sources for caller comparison.")
    q.add_argument("packet")
    q.add_argument("--asset", dest="asset_id")
    q.add_argument("--plan")
    q.add_argument("--job")
    q.add_argument("--comparison")
    q.add_argument("--plar", default="plar.txt")
    q.add_argument("--root", required=True)
    q = sub.add_parser("ready")
    q.add_argument("path")
    q.add_argument("--root")
    q = sub.add_parser("impact")
    q.add_argument("path")
    q.add_argument("id")
    q = sub.add_parser("init")
    q.add_argument("store")
    q.add_argument("--name", default="PIXL project")
    q.add_argument("--root")
    q = sub.add_parser("intake")
    q.add_argument("store")
    q.add_argument("--name", default="PIXL project")
    q.add_argument("--brief", default="")
    q.add_argument("--root")
    q = sub.add_parser(
        "retain-library",
        help="Keep exact project-bound library sources across kit updates.",
    )
    q.add_argument("store")
    q.add_argument(
        "library", help="Project-relative kit directory named by the source records."
    )
    q.add_argument(
        "--from-library",
        help="Project-relative original kit for recovery after replacement.",
    )
    q.add_argument("--expect", required=True)
    q.add_argument("--root")
    q = sub.add_parser("task-complete", help="Complete an already-reviewed PX2 task.")
    q.add_argument("store")
    q.add_argument("task")
    q.add_argument("candidates", nargs="+")
    q.add_argument("--expect", required=True)
    q.add_argument("--root")
    q = sub.add_parser("workflow")
    q.add_argument("path")
    q.add_argument("--root")
    q = sub.add_parser("review-context", help="Read exact candidate/family criteria, bindings and current acceptance.")
    q.add_argument("path")
    q.add_argument("candidate")
    q.add_argument("--root", required=True)
    q = sub.add_parser("candidate-review", help="Retain explicit candidate/family observations and optionally nominate or complete.")
    q.add_argument("store")
    q.add_argument("candidate")
    q.add_argument("review")
    q.add_argument("observation", metavar="REVIEW_JSON")
    q.add_argument("--expect", required=True)
    q.add_argument("--root", required=True)
    q = sub.add_parser("inspection", help="Read retained candidate views and reviews.")
    q.add_argument("path")
    q.add_argument("packet", nargs="?")
    q.add_argument("--root", required=True)
    q = sub.add_parser(
        "inspection-prepare",
        help="Retain exact candidate inspection views without a verdict.",
    )
    q.add_argument("store")
    q.add_argument("candidate")
    q.add_argument("packet")
    q.add_argument("options", metavar="OPTIONS_JSON")
    q.add_argument("--expect", required=True)
    q.add_argument("--root")
    q = sub.add_parser(
        "inspection-review", help="Retain an explicit review without task completion."
    )
    q.add_argument("store")
    q.add_argument("packet")
    q.add_argument("review")
    q.add_argument("observation", metavar="REVIEW_JSON")
    q.add_argument("--expect", required=True)
    q.add_argument("--root")
    q = sub.add_parser(
        "family", help="Read family selection and retained delivery status."
    )
    q.add_argument("path")
    q.add_argument("output", nargs="?")
    q.add_argument("--root", required=True)
    q = sub.add_parser(
        "family-snapshot",
        help="Retain member files as an unaccepted delivery candidate.",
    )
    q.add_argument("store")
    q.add_argument("output")
    q.add_argument("candidate")
    q.add_argument("--expect", required=True)
    q.add_argument("--root")
    q = sub.add_parser("production-plan", help="Author connected family stages from reviewed JSON.")
    q.add_argument("store")
    q.add_argument("plan", metavar="PLAN_JSON")
    q.add_argument("--expect", required=True)
    q.add_argument("--root", required=True)
    q = sub.add_parser("stage-prepare", help="Bind reviewed stage inputs and retain a durable request.")
    q.add_argument("store")
    q.add_argument("plan")
    q.add_argument("stage")
    q.add_argument("job")
    q.add_argument("packet", metavar="PACKET_JSON")
    q.add_argument("--expect", required=True)
    q.add_argument("--root", required=True)
    q = sub.add_parser("job-prepare", help="Save provider intent without executing it.")
    q.add_argument("store")
    q.add_argument("job")
    q.add_argument("task")
    q.add_argument("request", metavar="REQUEST_JSON")
    q.add_argument("--outputs", nargs="+", required=True)
    q.add_argument("--expect", required=True)
    q.add_argument("--root")
    q = sub.add_parser(
        "job-dispatch", help="Save a dispatch claim before host execution."
    )
    q.add_argument("store")
    q.add_argument("job")
    q.add_argument("--expect", required=True)
    q.add_argument("--root")
    q = sub.add_parser(
        "job-observe", help="Save a caller-supplied provider observation."
    )
    q.add_argument("store")
    q.add_argument("job")
    q.add_argument(
        "event", choices=["submitted", "running", "succeeded", "failed", "unknown"]
    )
    q.add_argument("evidence", metavar="EVIDENCE_JSON")
    q.add_argument("--remote-id")
    q.add_argument("--expect", required=True)
    q.add_argument("--root")
    q = sub.add_parser(
        "job-import", help="Snapshot a local download as an unaccepted candidate."
    )
    q.add_argument("store")
    q.add_argument("job")
    q.add_argument("output")
    q.add_argument("candidate")
    q.add_argument("path")
    q.add_argument("evidence", metavar="EVIDENCE_JSON")
    q.add_argument("--expect", required=True)
    q.add_argument("--root")
    q = sub.add_parser(
        "jobs", help="Read saved requests and recovery actions without dispatching."
    )
    q.add_argument("path")
    q.add_argument("--root", required=True)
    q = sub.add_parser("commit")
    q.add_argument(
        "--json",
        action="store_true",
        help="Read the candidate as JSON instead of PX wire text.",
    )
    q.add_argument("store")
    q.add_argument("candidate")
    q.add_argument("--expect", required=True)
    q.add_argument("--root")
    q = sub.add_parser(
        "plar", help="Source-linked asset requirements and focused handoffs."
    )
    actions = q.add_subparsers(dest="plar_action", required=True)
    for action in ("read", "save", "prepare", "handoff"):
        action_parser = actions.add_parser(action)
        action_parser.add_argument("--root", required=True)
        action_parser.add_argument("--path", default="plar.txt")
        if action == "read":
            action_parser.add_argument("--asset", dest="asset_id")
            action_parser.add_argument(
                "--since", help="Compare the queue with a retained PLAR hash."
            )
        elif action == "handoff":
            action_parser.add_argument("--result-path", help="Save exact result under a fresh project-relative path.")
            action_parser.add_argument("details", metavar="DETAILS_JSON")
            action_parser.add_argument("--asset", dest="asset_id", required=True)
            action_parser.add_argument("--requirements", dest="requirements_hash", required=True)
            action_parser.add_argument("--expect", required=True, help="Current production.continuation.state_hash from the selected PLAR read, not its file hash.")
        elif action == "prepare":
            action_parser.add_argument("--asset", dest="asset_id", required=True)
            action_parser.add_argument(
                "--requirements", dest="requirements_hash", required=True
            )
            action_parser.add_argument("--packet", required=True)
            action_parser.add_argument("--connection", required=True)
            action_parser.add_argument("--store")
            action_parser.add_argument("--revise", action="store_true")
            action_parser.add_argument("--expect", help="Current production state hash for an explicit revised plan.")
        else:
            action_parser.add_argument("document", metavar="DOCUMENT_JSON")
            action_parser.add_argument("--expect", required=True)
    q = sub.add_parser("catalog")
    q.add_argument("root")
    q.add_argument("--out")
    q = sub.add_parser("sources")
    q.add_argument("--root")
    q = sub.add_parser("source")
    q.add_argument("path")
    q.add_argument(
        "--root",
        help="Resolve a project-relative source, including explicitly retained revisions.",
    )
    q.add_argument("--expect", required=True)
    q.add_argument("--start", type=int, required=True)
    q.add_argument("--end", type=int, required=True)
    q.add_argument("--budget", type=int, default=16384)
    q = sub.add_parser("asset-check")
    q.add_argument("path")
    q.add_argument("--width", type=int)
    q.add_argument("--height", type=int)
    q.add_argument("--palette", nargs="*")
    q.add_argument("--alpha", choices=["binary", "full"], default="binary")
    q.add_argument("--regions", nargs="+", help="Measure exact-color component boxes")
    q = sub.add_parser("encode")
    q.add_argument("path")
    q.add_argument("--out")
    q = sub.add_parser("decode")
    q.add_argument("path")
    q = sub.add_parser("capabilities")
    q.add_argument("name", nargs="?")
    q = sub.add_parser("knowledge")
    q.add_argument("method", nargs="?")
    q = sub.add_parser(
        "prepare",
        help="Legacy stateless request validation; does not save project intent.",
    )
    q.add_argument("tool")
    q.add_argument("arguments")
    q.add_argument("--schema", required=True)
    q.add_argument("--authorization")
    q = sub.add_parser(
        "job", help="Legacy stateless journal update; does not publish project state."
    )
    q.add_argument("path")
    q.add_argument("event")
    q.add_argument("--remote-id")
    q.add_argument("--evidence")
    q = sub.add_parser("poc")
    q.add_argument("--out", required=True)
    q = sub.add_parser("mcp")
    q.add_argument("--root", required=True)
    for command in ("context", "request-review", "review-context", "candidate-review", "family", "family-snapshot"):
        sub.choices[command].add_argument("--result-path", help="Save exact result under a fresh project-relative path; requires --root.")
    return p


def main(argv=None):
    a = parser().parse_args(argv)
    try:
        cmd, output, binary = a.command, None, None
        if getattr(a, "result_path", None):
            service.result_destination(a.root, a.result_path)
        if cmd == "mcp":
            from .mcp import serve

            serve(Path(a.root).resolve())
            return 0
        if cmd == "request-review":
            from .request_review import report

            output = report(a.root, a.packet, a.asset_id, a.plar, a.plan, a.job, a.comparison)
        elif cmd == "validate":
            output = service.inspect_document(a.path, a.root)
        elif cmd == "context" and a.view == "authoring":
            if a.root is None:
                raise PixlError("authoring_context", "--root is required for authoring context")
            from .authoring_context import report

            if a.budget is not None:
                raise PixlError("context_budget", "budget applies only to complete wire context")
            output = report(a.path, a.focus, a.root, a.plar_path, a.asset_id)
        elif cmd in ("context", "ready", "impact", "decode"):
            doc = service.load_document(a.path)
            graph.validate(doc, getattr(a, "root", None))
            if cmd == "context":
                if a.plar_path is not None or a.asset_id is not None:
                    raise PixlError("context_view", "selection arguments require --view authoring")
                binary = codec.encode(graph.context(doc, a.focus, a.budget))
            elif cmd == "ready":
                output = {"ready": service.workflow(a.path, a.root)["ready"] if doc.format == 2 else graph.ready(doc), "hash": codec.digest(doc)}
            elif cmd == "impact":
                output = {"affected": graph.impact(doc, a.id)}
            else:
                output = {
                    "revision": doc.revision,
                    "records": [
                        {"id": r.id, "kind": r.kind, "fields": codec.to_data(r.fields)}
                        for r in doc.records.values()
                    ],
                }
                if doc.format != 1:
                    output["format"] = doc.format
        elif cmd == "init":
            output = store.initialize(a.store, root=a.root, name=a.name)
        elif cmd == "intake":
            output = store.initialize(
                a.store, doc=store.intake_project(a.name, a.brief), root=a.root
            )
        elif cmd == "retain-library":
            from .retention import retain

            output = retain(a.store, a.expect, a.library, a.root, a.from_library)
        elif cmd == "task-complete":
            from .completion import complete

            output = complete(a.store, a.expect, a.task, a.candidates, a.root)
        elif cmd == "workflow":
            output = service.workflow(a.path, a.root)
        elif cmd == "review-context":
            from . import candidate_review

            output = candidate_review.context(service.load_document(a.path), a.root, a.candidate)
        elif cmd == "candidate-review":
            from . import candidate_review

            output = candidate_review.submit(a.store, a.expect, a.candidate, a.review, service.read_json(a.observation), a.root)
        elif cmd == "inspection":
            output = service.inspection_report(a.path, a.root, a.packet)
        elif cmd == "inspection-prepare":
            from . import inspection

            output = inspection.prepare(
                a.store,
                a.expect,
                a.candidate,
                a.packet,
                service.read_json(a.options),
                a.root,
            )
        elif cmd == "inspection-review":
            from . import inspection

            output = inspection.review(
                a.store,
                a.expect,
                a.packet,
                a.review,
                service.read_json(a.observation),
                a.root,
            )
        elif cmd == "family":
            output = service.family_report(a.path, a.root, a.output)
        elif cmd == "family-snapshot":
            from . import delivery

            output = delivery.snapshot(a.store, a.expect, a.output, a.candidate, a.root)
        elif cmd == "production-plan":
            from . import production_plan

            output = production_plan.author(a.store, a.expect, service.read_json(a.plan), a.root)
        elif cmd == "stage-prepare":
            from . import production_plan

            output = production_plan.prepare(a.store, a.expect, a.plan, a.stage, a.job, service.read_json(a.packet), a.root)
        elif cmd == "job-prepare":
            output = service.job_prepare(
                a.store,
                a.expect,
                a.job,
                a.task,
                a.outputs,
                service.read_json(a.request),
                a.root,
            )
        elif cmd == "job-dispatch":
            output = jobs.dispatch(a.store, a.expect, a.job, a.root)
        elif cmd == "job-observe":
            output = jobs.observe(
                a.store,
                a.expect,
                a.job,
                a.event,
                service.read_json(a.evidence),
                remote_id=a.remote_id,
                root=a.root,
            )
        elif cmd == "job-import":
            output = jobs.import_artifact(
                a.store,
                a.expect,
                a.job,
                a.output,
                a.candidate,
                a.path,
                service.read_json(a.evidence),
                a.root,
            )
        elif cmd == "jobs":
            output = service.job_report(a.path, a.root)
        elif cmd == "commit":
            output = store.commit(
                a.store,
                service.from_json(service.read_json(a.candidate))
                if a.json
                else service.load_document(a.candidate),
                a.expect,
                a.root,
            )
        elif cmd == "plar":
            args = {"path": a.path}
            if a.plar_action == "read":
                if a.asset_id:
                    args["asset_id"] = a.asset_id
                if a.since:
                    args["since"] = a.since
            elif a.plar_action == "handoff":
                args.update(asset_id=a.asset_id, requirements_hash=a.requirements_hash,
                            expect=a.expect, details=service.read_json(a.details))
            elif a.plar_action == "prepare":
                args.update(
                    asset_id=a.asset_id,
                    requirements_hash=a.requirements_hash,
                    packet=a.packet,
                    connection=a.connection,
                    revise=a.revise,
                )
                if a.expect:
                    args["expect"] = a.expect
                if a.store:
                    args["store"] = a.store
            else:
                args.update(document=service.read_json(a.document), expect=a.expect)
            output = service.call("pixl_plar_" + a.plar_action, args, a.root)
        elif cmd == "catalog":
            from .catalog import build

            output = build(a.root)
        elif cmd == "source":
            output = (
                service.call(
                    "pixl_source",
                    {
                        "path": a.path,
                        "expect": a.expect,
                        "start": a.start,
                        "end": a.end,
                        "budget": a.budget,
                    },
                    a.root,
                )
                if a.root
                else service.source_slice(a.path, a.expect, a.start, a.end, a.budget)
            )
        elif cmd == "sources":
            output = service.source_inventory(a.root)
        elif cmd == "asset-check":
            from .assets import inspect

            output = inspect(a.path, a.width, a.height, a.palette, a.alpha, a.regions)
        elif cmd == "encode":
            binary = codec.encode(service.from_json(service.read_json(a.path)))
        elif cmd == "knowledge":
            output = service.knowledge(a.method)
        elif cmd in ("capabilities", "prepare", "job"):
            from . import platform

            if cmd == "capabilities":
                output = service.capability_index(a.name)
            elif cmd == "prepare":
                output = platform.prepare(
                    a.tool,
                    service.read_json(a.arguments),
                    service.read_json(a.schema),
                    service.read_json(a.authorization) if a.authorization else None,
                )
            else:
                output = platform.job_update(
                    service.read_json(a.path),
                    a.event,
                    a.remote_id,
                    service.read_json(a.evidence) if a.evidence else None,
                )
        elif cmd == "poc":
            from .poc import run_all

            output = run_all(a.out)
        if getattr(a, "result_path", None):
            output = service.save_result(output, a.root, a.result_path, binary)
            binary = None
        data = (
            binary
            if binary is not None
            else (json.dumps(output, ensure_ascii=False, indent=2) + "\n").encode(
                "utf-8"
            )
        )
        if getattr(a, "out", None) and cmd != "poc":
            Path(a.out).parent.mkdir(parents=True, exist_ok=True)
            Path(a.out).write_bytes(data)
        else:
            sys.stdout.buffer.write(data)
        return (
            1
            if isinstance(output, dict)
            and (output.get("pass") is False or output.get("status") == "fail" or output.get("result_saved") is False)
            else 0
        )
    except (PixlError, OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        print(
            json.dumps(
                {"error": getattr(error, "code", "operation"), "detail": str(error)}
            ),
            file=sys.stderr,
        )
        return 2
