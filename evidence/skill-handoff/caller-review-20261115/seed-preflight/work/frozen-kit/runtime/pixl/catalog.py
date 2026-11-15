"""Source-preserving Markdown/asset index. Source bytes are never executed."""

import hashlib
import re
from collections import defaultdict
from pathlib import Path

from .codec import PixlError
from .graph import confined
from .sources import INVENTORY_PATH, load_inventory


def build(root, paths=None):
    root = Path(root).resolve()
    expected = {}
    if paths is None:
        if (root / INVENTORY_PATH).exists() or (root / "training/original-docs").exists():
            inventory = load_inventory(root)
            expected = {row["path"]: row["sha256"] for row in inventory["documents"]}
            paths = list(expected)
        else:
            paths = sorted(p.name for p in root.glob("*.md"))
    documents, hashes = [], defaultdict(list)
    for name in sorted(set(paths)):
        path = confined(root, name)
        data = path.read_bytes()
        hash_ = hashlib.sha256(data).hexdigest()
        if name in expected and hash_ != expected[name]:
            raise PixlError("source_hash", f"{name}: source changed during cataloging")
        try:
            lines = data.decode("utf-8-sig").splitlines()
        except UnicodeError as error:
            raise PixlError("source_encoding", name) from error
        sections: list[dict[str, str | int]] = []
        fence = None
        fenced_blocks = []
        for number, line in enumerate(lines, 1):
            if match := re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line):
                marker = match[1]
                if fence is None:
                    fence = (marker[0], len(marker), number)
                    fenced_blocks.append({"start": number, "language": match[2].strip(), "end": None})
                elif marker[0] == fence[0] and len(marker) >= fence[1] and not match[2].strip():
                    fenced_blocks[-1]["end"] = number
                    fence = None
                continue
            heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
            if heading and fence is None:
                if sections:
                    sections[-1]["end"] = number - 1
                sid = f's{hashlib.sha256(f"{hash_}:{number}".encode()).hexdigest()[:20]}'
                sections.append({"id": sid, "title": heading[2], "level": len(heading[1]),
                                 "start": number, "end": len(lines)})
        hashes[hash_].append(name)
        documents.append({"path": name, "sha256": hash_, "bytes": len(data), "lines": len(lines),
                          "sections": sections, "code_blocks": fenced_blocks,
                          "unclosed_code_fence": fence is not None,
                          "urls": sorted(set(re.findall(r"https?://[^\s<>\)\]\"']+", "\n".join(lines))))})
    return {"version": 1, "documents": documents,
            "duplicates": [{"sha256": h, "paths": names} for h, names in sorted(hashes.items()) if len(names) > 1],
            "authority": "derived-index; original bytes and section locators remain authoritative"}
