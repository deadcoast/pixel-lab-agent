"""Preserve a selected production continuation alongside the agent's own judgments."""

import json
from hashlib import sha256
from pathlib import Path

from . import graph, plar, store
from .codec import PixlError


def save(root, asset_id, requirements_hash, expect, details, path="plar.txt"):
    root = Path(root).resolve()
    if not isinstance(details, dict) or details.get("status") not in (
        "delivered", "partial", "needs_input", "blocked"
    ):
        raise PixlError("handoff_details", "details needs the agent's assignment status")
    if {"resume", "next", "asset_id", "requirements_hash", "version"} & details.keys():
        raise PixlError("handoff_details", "Derived fields belong to the snapshot; use caller_actions and future_work for commentary")
    selected = plar.read(root, path, asset_id)
    if selected["requirements_hash"] != requirements_hash:
        raise PixlError("handoff_stale", "Selected requirements changed; reread the asset")
    production = selected.get("production") or {}
    continuation = production.get("continuation")
    if not continuation:
        raise PixlError("handoff_state", "No production continuation is available; retain the allocation diagnostic in the ordinary result")
    if continuation["state_hash"] != expect:
        raise PixlError("handoff_stale", "Production state changed; reread before handing it back")
    document = {
        "version": 1,
        "asset_id": asset_id,
        "requirements_hash": requirements_hash,
        "resume": continuation,
        "next": continuation["action"],
        "selection": {
            "path": graph.confined(root, path).relative_to(root).as_posix(),
            "hash": selected["hash"],
            "current": production["selection_current"],
        },
        "details": details,
        "scope": "Snapshot of derived state plus agent-authored observations. No automatic contract, art or delivery acceptance; reread current PLAR before acting.",
    }
    data = (json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")
    digest = sha256(data).hexdigest()
    folder = graph.confined(root, ".pixl/handoffs")
    with store.lock(folder):
        target = graph.confined(root, f".pixl/handoffs/{digest}.json")
        if target.exists():
            if target.read_bytes() != data:
                raise PixlError("handoff_corrupt", "Retained snapshot bytes changed")
        else:
            store._atomic(target, data)
    return {
        "path": target.relative_to(root).as_posix(),
        "sha256": digest,
        "asset_id": asset_id,
        "requirements_hash": requirements_hash,
        "state_hash": expect,
        "next": document["next"],
        "scope": document["scope"],
    }
