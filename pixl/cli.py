"""Command entry point. JSON is host interchange; context/encode emit PIXL."""

import argparse
import json
from pathlib import Path
import sys

from . import codec, graph, service, store
from .codec import PixlError


def parser():
    p = argparse.ArgumentParser(prog="pixl", description="PIXL/1 agent project state and pixel-art tools")
    sub = p.add_subparsers(dest="command", required=True)
    q = sub.add_parser("validate"); q.add_argument("path"); q.add_argument("--root")
    q = sub.add_parser("context"); q.add_argument("path"); q.add_argument("focus"); q.add_argument("--budget", type=int); q.add_argument("--root")
    q = sub.add_parser("ready"); q.add_argument("path")
    q = sub.add_parser("impact"); q.add_argument("path"); q.add_argument("id")
    q = sub.add_parser("init"); q.add_argument("store"); q.add_argument("--name", default="PIXL project"); q.add_argument("--root")
    q = sub.add_parser("commit"); q.add_argument("store"); q.add_argument("candidate"); q.add_argument("--expect", required=True); q.add_argument("--root")
    q = sub.add_parser("catalog"); q.add_argument("root"); q.add_argument("--out")
    q = sub.add_parser("source"); q.add_argument("path"); q.add_argument("--expect", required=True); q.add_argument("--start", type=int, required=True); q.add_argument("--end", type=int, required=True); q.add_argument("--budget", type=int, default=16384)
    q = sub.add_parser("asset-check"); q.add_argument("path"); q.add_argument("--width", type=int); q.add_argument("--height", type=int); q.add_argument("--palette", nargs="*"); q.add_argument("--alpha", choices=["binary", "full"], default="binary")
    q = sub.add_parser("encode"); q.add_argument("path"); q.add_argument("--out")
    q = sub.add_parser("decode"); q.add_argument("path")
    q = sub.add_parser("capabilities"); q.add_argument("name", nargs="?")
    q = sub.add_parser("knowledge"); q.add_argument("method", nargs="?")
    q = sub.add_parser("prepare"); q.add_argument("tool"); q.add_argument("arguments"); q.add_argument("--schema", required=True); q.add_argument("--authorization")
    q = sub.add_parser("job"); q.add_argument("path"); q.add_argument("event"); q.add_argument("--remote-id"); q.add_argument("--evidence")
    q = sub.add_parser("poc"); q.add_argument("--out", required=True)
    q = sub.add_parser("mcp"); q.add_argument("--root", required=True)
    return p


def main(argv=None):
    a = parser().parse_args(argv)
    try:
        cmd, output, binary = a.command, None, None
        if cmd == "mcp":
            from .mcp import serve
            serve(Path(a.root).resolve())
            return 0
        if cmd == "validate":
            output = service.inspect_document(a.path, a.root)
        elif cmd in ("context", "ready", "impact", "decode"):
            doc = service.load_document(a.path)
            graph.validate(doc, getattr(a, "root", None))
            if cmd == "context":
                binary = codec.encode(graph.context(doc, a.focus, a.budget))
            elif cmd == "ready":
                output = {"ready": graph.ready(doc), "hash": codec.digest(doc)}
            elif cmd == "impact":
                output = {"affected": graph.impact(doc, a.id)}
            else:
                output = {"revision": doc.revision, "records": [{"id": r.id, "kind": r.kind, "fields": codec.to_data(r.fields)} for r in doc.records.values()]}
        elif cmd == "init":
            output = store.initialize(a.store, root=a.root, name=a.name)
        elif cmd == "commit":
            output = store.commit(a.store, service.load_document(a.candidate), a.expect, a.root)
        elif cmd == "catalog":
            from .catalog import build
            output = build(a.root)
        elif cmd == "source":
            output = service.source_slice(a.path, a.expect, a.start, a.end, a.budget)
        elif cmd == "asset-check":
            from .assets import inspect
            output = inspect(a.path, a.width, a.height, a.palette, a.alpha)
        elif cmd == "encode":
            binary = codec.encode(service.from_json(service.read_json(a.path)))
        elif cmd == "knowledge":
            output = service.knowledge(a.method)
        elif cmd in ("capabilities", "prepare", "job"):
            from . import platform
            if cmd == "capabilities":
                output = service.capability_index(a.name)
            elif cmd == "prepare":
                output = platform.prepare(a.tool, service.read_json(a.arguments), service.read_json(a.schema),
                                          service.read_json(a.authorization) if a.authorization else None)
            else:
                output = platform.job_update(service.read_json(a.path), a.event, a.remote_id,
                                             service.read_json(a.evidence) if a.evidence else None)
        elif cmd == "poc":
            from .poc import run_all
            output = run_all(a.out)
        data = binary if binary is not None else (json.dumps(output, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        if getattr(a, "out", None) and cmd != "poc":
            Path(a.out).parent.mkdir(parents=True, exist_ok=True)
            Path(a.out).write_bytes(data)
        else:
            sys.stdout.buffer.write(data)
        return 1 if isinstance(output, dict) and (output.get("pass") is False or output.get("status") == "fail") else 0
    except (PixlError, OSError, ValueError, KeyError, TypeError, RecursionError) as error:
        print(json.dumps({"error": getattr(error, "code", "operation"), "detail": str(error)}), file=sys.stderr)
        return 2
