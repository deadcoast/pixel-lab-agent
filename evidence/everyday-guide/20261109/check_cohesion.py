"""Read-only integrity check for this increment's package and document chain."""

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


root = Path(__file__).resolve().parents[3]
base = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


receipt_path = root / "evidence/verification-runs/20261109T191851.620905Z/result.json"
receipt = json.loads(receipt_path.read_bytes())
drift = [name for name, expected in receipt["checked_input_hashes"].items()
         if not (root / name).is_file() or sha(root / name) != expected]
plugin = root / "plugins/pixl"
manifest = json.loads((plugin / "bundle-manifest.json").read_bytes())
bundle_errors = [entry["path"] for entry in manifest["files"]
                 if not (plugin / entry["path"]).is_file()
                 or sha(plugin / entry["path"]) != entry["sha256"]]
manifest_hash = sha(plugin / "bundle-manifest.json")
native_packages = {
    host: sha(base / "native" / f"{host}-01/project/.agents/skills/export-kit/bundle-manifest.json")
    for host in ("claude", "codex")
}
documents = [
    "README.md", "TODO.md", "PLAN.md", "SHELVED.md", "docs/IDENTIFIED.md",
    "docs/AGENT-KIT.md", "docs/VERIFICATION.md", "evaluations/TODO.spec.md",
    "plugins/pixl/skills/pixl/SKILL.md",
    "plugins/pixl/skills/pixl/references/runtime.md",
    "plugins/pixl/skills/pixl/references/everyday.md",
    "plugins/pixl/skills/pixl/references/identities-and-paths.md",
    "evidence/everyday-guide/README.md",
]
missing = []
link_count = 0
for name in documents:
    path = root / name
    for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
        target = target.strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        link_count += 1
        if not (path.parent / unquote(target)).exists():
            missing.append({"document": name, "target": target})
identified = re.findall(r"^- \*\*((?:NF|SC|QOL|CF|TM)-\d+)\b",
                        (root / "docs/IDENTIFIED.md").read_text(encoding="utf-8"), re.M)
shelved = re.findall(r"^\| \[((?:NF|SC|QOL|CF|TM)-\d+)\]",
                    (root / "SHELVED.md").read_text(encoding="utf-8"), re.M)
findings_match = len(identified) == 50 and Counter(identified) == Counter(shelved)
ledger = json.loads((base / "RESULT.json").read_bytes())
references = []


def collect(value):
    if isinstance(value, dict):
        if {"path", "sha256", "bytes"} <= value.keys():
            references.append(value)
        for child in value.values():
            collect(child)
    elif isinstance(value, list):
        for child in value:
            collect(child)


collect(ledger)
bad_references = [entry["path"] for entry in references
                  if not (root / entry["path"]).is_file()
                  or sha(root / entry["path"]) != entry["sha256"]
                  or (root / entry["path"]).stat().st_size != entry["bytes"]]
status = (not drift and not bundle_errors and not missing and not bad_references and findings_match
          and receipt["bundle_manifest_sha256"] == manifest_hash
          and all(h == manifest_hash for h in native_packages.values()))
result = {
    "status": "pass" if status else "fail",
    "verifier": {"path": receipt_path.relative_to(root).as_posix(), "sha256": sha(receipt_path)},
    "tested_inputs": len(receipt["checked_input_hashes"]), "tested_input_drift": drift,
    "bundle_entries": len(manifest["files"]), "bundle_errors": bundle_errors,
    "bundle_manifest_sha256": manifest_hash, "native_manifest_sha256": native_packages,
    "bundle_matches_verified_revision": receipt["bundle_manifest_sha256"] == manifest_hash,
    "local_links_checked": link_count, "missing_links": missing,
    "finding_count": len(identified), "findings_once_in_shelved": findings_match,
    "result_references_checked": len(references), "bad_result_references": bad_references,
    "result_ledger_sha256": sha(base / "RESULT.json"),
    "documents": {name: sha(root / name) for name in documents},
    "limits": "Read-only integrity, links and finding coverage; no new test-suite, native or artistic acceptance.",
}
(base / "verification/cohesion-final.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in result.items() if k not in {"documents", "native_manifest_sha256"}}, indent=2))
