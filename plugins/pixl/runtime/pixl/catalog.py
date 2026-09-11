"""Source-preserving Markdown/asset index. Source bytes are never executed."""

from collections import defaultdict
import hashlib
from pathlib import Path
import re

from .codec import PixlError
from .graph import confined

SUPPLIED = ("links.md", "AGENT-PIXELART-TRAINING.md", "PIXEL-ART-ASSETS.md",
            "pixel-art-deep-research-report.md", "research-pixel-art-systems.md")


def build(root, paths=None):
    root = Path(root).resolve()
    if paths is None:
        paths = [name for name in SUPPLIED if (root / name).is_file()]
        if not paths:
            paths = sorted(p.name for p in root.glob("*.md"))
    documents, hashes = [], defaultdict(list)
    for name in sorted(set(paths)):
        path = confined(root, name)
        data = path.read_bytes()
        hash_ = hashlib.sha256(data).hexdigest()
        try:
            lines = data.decode("utf-8-sig").splitlines()
        except UnicodeError as error:
            raise PixlError("source_encoding", name) from error
        sections, fence = [], None
        fenced_blocks = []
        for number, line in enumerate(lines, 1):
            match = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
            if match:
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
                sid = "s" + hashlib.sha256(f"{hash_}:{number}".encode()).hexdigest()[:20]
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
