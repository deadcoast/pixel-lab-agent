"""Verify the reviewed migration of curated pixel-art source ranges.

This script is intentionally read-only.  It compares the preserved pre-migration
resource bytes with the supplied current corpus, validates every migration row,
and checks that the curated methods changed only in their ``sources`` fields.
"""

from __future__ import annotations

import argparse
import copy
import difflib
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OLD_TO_CURRENT = {
    "AGENT-PIXELART-TRAINING.md": (
        "evidence/source-migration/previous/AGENT-PIXELART-TRAINING.md",
        "training/original-docs/AGENT-PIXELART-TRAINING.md",
    ),
    "PIXEL-ART-ASSETS.md": (
        "evidence/source-migration/previous/PIXEL-ART-ASSETS.md",
        "training/original-docs/PIXEL-ART-ASSETS.md",
    ),
    "pixel-art-deep-research-report.md": (
        "evidence/source-migration/previous/pixel-art-deep-research-report.md",
        "training/original-docs/PIXEL-ART-DEEP-RESEARCH.md",
    ),
}
MIGRATION_PATH = ROOT / "knowledge/source-migration.json"
REVIEW_PATH = ROOT / "evidence/source-migration/range-review.json"
KNOWLEDGE_PATH = ROOT / "knowledge/pixel-art.json"
OLD_KNOWLEDGE_PATH = (
    ROOT / "evidence/source-migration/previous/knowledge/pixel-art.json"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_digest(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def source_info(relative_path: str) -> dict[str, Any]:
    data = (ROOT / relative_path).read_bytes()
    text = data.decode("utf-8")
    return {
        "path": relative_path,
        "sha256": sha256_bytes(data),
        "bytes": len(data),
        "lines": len(text.splitlines()),
    }


def lines(relative_path: str) -> list[str]:
    return (ROOT / relative_path).read_text(encoding="utf-8").splitlines()


def normalize_current_research_slice(
    slice_lines: list[str], start: int, inserted_fence_lines: set[int]
) -> list[str]:
    normalized = []
    for offset, line in enumerate(slice_lines):
        current_line = start + offset
        if current_line in inserted_fence_lines:
            continue
        if current_line == 1077 and line == "## Diffuse response":
            line = "### Diffuse response"
        normalized.append(line)
    return normalized


def range_slice(relative_path: str, start: int, end: int) -> list[str]:
    source_lines = lines(relative_path)
    if start < 1 or end < start or end > len(source_lines):
        raise AssertionError(
            f"invalid range {relative_path}:{start}-{end} "
            f"for {len(source_lines)} lines"
        )
    return source_lines[start - 1 : end]


def build_line_map(
    old_path: str, current_path: str
) -> tuple[dict[int, int], list[str], list[int]]:
    old_lines = lines(old_path)
    current_lines = lines(current_path)
    matcher = difflib.SequenceMatcher(a=old_lines, b=current_lines, autojunk=False)
    mapping: dict[int, int] = {}
    changes: list[str] = []
    inserted_fence_lines: list[int] = []
    for tag, old_start, old_end, new_start, new_end in matcher.get_opcodes():
        if tag == "equal":
            for offset in range(old_end - old_start):
                mapping[old_start + offset + 1] = new_start + offset + 1
            continue
        old_part = old_lines[old_start:old_end]
        new_part = current_lines[new_start:new_end]
        if (
            tag == "replace"
            and old_part == ["### Diffuse response"]
            and new_part == ["## Diffuse response"]
        ):
            mapping[old_start + 1] = new_start + 1
            changes.append(
                f"heading level: old {old_start + 1} -> current {new_start + 1}"
            )
            continue
        is_fence = len(new_part) == 1 and new_part[0] in {
            "```TeX",
            "```txt",
            "```",
        }
        is_trailing_marker = old_start == len(old_lines) and new_part == [
            "",
            "---",
            "",
            "M I V I M .spec development",
            "",
            "---",
        ]
        if tag == "insert" and (is_fence or is_trailing_marker):
            inserted_fence_lines.extend(
                new_start + offset + 1
                for offset, line in enumerate(new_part)
                if line in {"```TeX", "```txt", "```"}
            )
            changes.append(
                f"inserted formatting/marker: after old {old_start}, "
                f"current {new_start + 1}-{new_end}"
            )
            continue
        raise AssertionError(
            f"unexpected source change {tag}: old {old_start + 1}-{old_end}, "
            f"current {new_start + 1}-{new_end}: {old_part!r} -> {new_part!r}"
        )
    if len(mapping) != len(old_lines):
        missing = sorted(set(range(1, len(old_lines) + 1)) - mapping.keys())
        raise AssertionError(f"unmapped old research lines: {missing}")
    return mapping, changes, inserted_fence_lines


def mapped_range(
    old_start: int,
    old_end: int,
    line_map: dict[int, int],
    inserted_fence_lines: list[int],
) -> tuple[int, int]:
    """Map a range and keep any newly fenced math block syntactically complete."""

    new_start = line_map[old_start]
    new_end = line_map[old_end]
    fence_pairs = list(zip(inserted_fence_lines[0::2], inserted_fence_lines[1::2]))
    for opening, closing in fence_pairs:
        if opening < new_start <= closing:
            new_start = opening
        if opening <= new_end < closing:
            new_end = closing
    return new_start, new_end


def without_sources(registry: dict[str, Any]) -> dict[str, Any]:
    copy = json.loads(json.dumps(registry, ensure_ascii=False))
    for method in copy["methods"]:
        method.pop("sources", None)
    return copy


def serialized(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def build_artifacts() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    old_registry = json.loads(OLD_KNOWLEDGE_PATH.read_text(encoding="utf-8"))
    migrated_registry = copy.deepcopy(old_registry)
    old_research, current_research = OLD_TO_CURRENT[
        "pixel-art-deep-research-report.md"
    ]
    line_map, deep_changes, inserted_fence_lines = build_line_map(
        old_research, current_research
    )
    old_methods = old_research
    current_methods = "training/original-docs/PIXEL-ART-METHODS.md"
    _, methods_changes, methods_fence_lines = build_line_map(
        old_methods, current_methods
    )

    source_documents: dict[str, Any] = {}
    for old_name, (preserved_path, current_path) in OLD_TO_CURRENT.items():
        preserved = source_info(preserved_path)
        old_identity = {
            "path": old_name,
            "preserved_path": preserved_path,
            "pre_packaging_observed_path": f"plugins/pixl/resources/{old_name}",
            "sha256": preserved["sha256"],
            "bytes": preserved["bytes"],
            "lines": preserved["lines"],
        }
        if old_name == "pixel-art-deep-research-report.md":
            old_identity["pre_packaging_observed_path"] = (
                "plugins/pixl/resources/pixel-art-deep-research-report.md"
            )
        source_documents[old_name] = {
            "old": old_identity,
            "current": source_info(current_path),
            "relationship": (
                "formatting-only-revision"
                if old_name == "pixel-art-deep-research-report.md"
                else "byte-identical-relocation"
            ),
        }

    citations: list[dict[str, Any]] = []
    for old_method, migrated_method in zip(
        old_registry["methods"], migrated_registry["methods"], strict=True
    ):
        assert old_method["id"] == migrated_method["id"]
        for source_index, (old_source, migrated_source) in enumerate(
            zip(old_method["sources"], migrated_method["sources"], strict=True)
        ):
            old_name = Path(old_source["path"]).name
            preserved_path, current_path = OLD_TO_CURRENT[old_name]
            pair = source_documents[old_name]
            if old_name == "pixel-art-deep-research-report.md":
                new_start, new_end = mapped_range(
                    old_source["start"],
                    old_source["end"],
                    line_map,
                    inserted_fence_lines,
                )
                kind = "reviewed-revision-line-migration"
            else:
                new_start = old_source["start"]
                new_end = old_source["end"]
                kind = "byte-identical-relocation"

            migrated_source.clear()
            migrated_source.update(
                {"path": current_path, "start": new_start, "end": new_end}
            )
            old_slice = range_slice(
                preserved_path, old_source["start"], old_source["end"]
            )
            current_slice = range_slice(current_path, new_start, new_end)
            normalization: list[str] = []
            inserted_in_slice = (
                [
                    line
                    for line in inserted_fence_lines
                    if new_start <= line <= new_end
                ]
                if old_name == "pixel-art-deep-research-report.md"
                else []
            )
            if inserted_in_slice:
                normalization.append(
                    "Remove the inserted Markdown math-fence lines at current lines "
                    + ", ".join(str(line) for line in inserted_in_slice)
                    + "."
                )
            if old_source["start"] <= 1039 <= old_source["end"]:
                normalization.append(
                    "Normalize current line 1077 '## Diffuse response' to the "
                    "historical line 1039 '### Diffuse response'."
                )
            normalized_old = old_slice
            normalized_current = normalize_current_research_slice(
                current_slice,
                new_start,
                (
                    set(inserted_fence_lines)
                    if old_name == "pixel-art-deep-research-report.md"
                    else set()
                ),
            )
            assert normalized_old == normalized_current, (
                old_method["id"],
                source_index,
                old_source,
                (new_start, new_end),
                normalized_old,
                normalized_current,
            )
            citations.append(
                {
                    "method_id": old_method["id"],
                    "source_index": source_index,
                    "old_source_name": old_name,
                    "old": {
                        "path": old_name,
                        "sha256": pair["old"]["sha256"],
                        "start": old_source["start"],
                        "end": old_source["end"],
                    },
                    "current": {
                        "path": current_path,
                        "sha256": pair["current"]["sha256"],
                        "start": new_start,
                        "end": new_end,
                    },
                    "correspondence": {
                        "kind": kind,
                        "comparison": (
                            "exact-line-sequence"
                            if old_slice == current_slice
                            else "equal-after-listed-formatting-normalization"
                        ),
                        "normalization": normalization,
                        "old_slice_sha256": json_digest(old_slice),
                        "current_slice_sha256": json_digest(current_slice),
                        "normalized_content_sha256": json_digest(normalized_old),
                        "result": "pass",
                    },
                }
            )

    old_non_source_digest = json_digest(without_sources(old_registry))
    new_non_source_digest = json_digest(without_sources(migrated_registry))
    assert old_non_source_digest == new_non_source_digest
    migrated_text = serialized(migrated_registry)
    migration = {
        "version": 1,
        "reviewed_on": "2026-09-11",
        "scope": "curated pixel-art source locator migration",
        "citation_count": len(citations),
        "slice_digest_encoding": (
            "SHA-256 of the UTF-8 canonical JSON array of split source lines"
        ),
        "source_documents": source_documents,
        "research_correspondence": {
            "old": source_documents["pixel-art-deep-research-report.md"]["old"],
            "current": source_documents["pixel-art-deep-research-report.md"][
                "current"
            ],
            "unchanged_mapped_lines": 1646,
            "heading_only_changes": 1,
            "inserted_markdown_fence_lines": len(inserted_fence_lines),
            "trailing_marker_lines": 6,
            "normalization_rules": [
                "Remove only Markdown fence lines identified as insertions by the full-file alignment.",
                "Normalize only the Diffuse response heading from current level 2 to historical level 3.",
                "Do not remove or substitute prose, equations, examples, citations, or code.",
            ],
            "changes": deep_changes,
            "related_current_methods_document": {
                **source_info(current_methods),
                "relationship": (
                    "Retains the historical research prose with 25 inserted math-fence "
                    "pairs and the same six-line trailing marker; it keeps the historical "
                    "Diffuse response heading level and is not byte-identical to the "
                    "current deep-research revision."
                ),
                "inserted_markdown_fence_lines": len(methods_fence_lines),
                "changes": methods_changes,
            },
        },
        "knowledge_registry": {
            "old": {
                **source_info(
                    "evidence/source-migration/previous/knowledge/pixel-art.json"
                ),
                "non_source_fields_sha256": old_non_source_digest,
            },
            "current": {
                "path": "knowledge/pixel-art.json",
                "sha256": sha256_bytes(migrated_text.encode("utf-8")),
                "bytes": len(migrated_text.encode("utf-8")),
                "methods": len(migrated_registry["methods"]),
                "non_source_fields_sha256": new_non_source_digest,
            },
        },
        "citations": citations,
    }
    migration_text = serialized(migration)
    review = {
        "version": 1,
        "reviewed_on": "2026-09-11",
        "status": "pass",
        "scope": "local source identity, line-range correspondence, and method-field preservation",
        "citation_count": len(citations),
        "counts": {
            "byte_identical_relocations": sum(
                row["correspondence"]["kind"] == "byte-identical-relocation"
                for row in citations
            ),
            "formatting_only_line_migrations": sum(
                row["correspondence"]["kind"]
                == "reviewed-revision-line-migration"
                for row in citations
            ),
            "methods": len(migrated_registry["methods"]),
            "non_source_method_fields_changed": 0,
        },
        "checks": [
            {
                "id": "old-source-identities",
                "status": "pass",
                "detail": "All three archived pre-migration sources match their recorded byte counts, line counts, and SHA-256 digests.",
            },
            {
                "id": "current-source-identities",
                "status": "pass",
                "detail": "All three current citation sources match their recorded byte counts, line counts, and SHA-256 digests.",
            },
            {
                "id": "full-research-correspondence",
                "status": "pass",
                "detail": "All 1,647 historical research lines map in order; 1,646 are exact and one differs only in heading level. The only insertions are 60 Markdown math-fence lines and the six-line trailing marker.",
            },
            {
                "id": "citation-range-correspondence",
                "status": "pass",
                "detail": "All 93 current locators resolve and retain their cited historical line sequences exactly or after only the row-listed formatting normalization.",
            },
            {
                "id": "non-source-method-fields",
                "status": "pass",
                "detail": "The canonical digest of all 43 methods with sources removed is unchanged.",
            },
        ],
        "old_knowledge_sha256": sha256_bytes(OLD_KNOWLEDGE_PATH.read_bytes()),
        "migrated_knowledge_sha256": sha256_bytes(migrated_text.encode("utf-8")),
        "non_source_fields_sha256": new_non_source_digest,
        "migration_manifest_sha256": sha256_bytes(migration_text.encode("utf-8")),
    }
    return migrated_registry, migration, review


def build_documentation() -> str:
    source_path = (
        ROOT
        / "evidence/source-migration/previous/docs/research/pixel-art-knowledge.md"
    )
    text = source_path.read_text(encoding="utf-8")
    old_research, current_research = OLD_TO_CURRENT[
        "pixel-art-deep-research-report.md"
    ]
    line_map, _, inserted_fence_lines = build_line_map(
        old_research, current_research
    )

    replacements = {
        "This document explains the curated registry in [knowledge/pixel-art.json](../../knowledge/pixel-art.json). The registry contains **43 actionable methods**, each with applicability, prerequisites, a procedure, checks, pitfalls, exact local source ranges, and a reproducible proof-of-concept recipe. Research was checked on **2026-09-10**.":
            "This document explains the curated registry in [knowledge/pixel-art.json](../../knowledge/pixel-art.json). The registry contains **43 actionable methods**, each with applicability, prerequisites, a procedure, checks, pitfalls, exact local source ranges, and a reproducible proof-of-concept recipe. The original research curation was checked on **2026-09-10**; supplied-source identities and citation correspondence were reviewed on **2026-09-11**.",
        "**Execution status:** every `poc` in this registry is a recipe; actual observations are recorded separately. The offline runner in [pixl/poc.py](../../pixl/poc.py) contains **39 bounded reference checks covering all 43 methods**, mapped in [method-proof-coverage.json](../../methods/method-proof-coverage.json). The complete reference run passed all 39 checks. Reports bind the runner's `implementation_sha256`, the resolved registry's `knowledge_sha256`, and every uniquely cited original file in `source_sha256`, alongside observations and output-artifact hashes. Missing knowledge or cited source bytes prevent an unbound passing report. This proves the specified primitives, not full PixelLab, engine, performance or aesthetic behavior. The recipes were designed during this curation; they are not a claim that the cited sources used these exact fixtures.":
            "**Historical execution status:** every `poc` in this registry is a recipe; actual observations are recorded separately. The offline runner in [pixl/poc.py](../../pixl/poc.py) contains **39 bounded reference checks covering all 43 methods**, mapped in [method-proof-coverage.json](../../methods/method-proof-coverage.json). The pre-migration reference run passed all 39 checks and bound the old registry and old source identities; that report is retained under `evidence/source-migration/previous/` and is not evidence for the migrated sources. Reports bind the runner's `implementation_sha256`, the resolved registry's `knowledge_sha256`, and every uniquely cited original file in `source_sha256`, alongside observations and output-artifact hashes. Missing knowledge or cited source bytes prevent an unbound passing report. A fresh run is current evidence only after it is executed against the migrated identities. These checks prove their specified primitives, not full PixelLab, engine, performance or aesthetic behavior. The recipes were designed during this curation; they are not a claim that the cited sources used these exact fixtures.",
        "The two local technical documents were read and compared. `AGENT-PIXELART-TRAINING.md` and `pixel-art-deep-research-report.md` have the same content after removing whitespace and Markdown table separator differences. They provide one body of technical research, not two independent confirmations. `research-pixel-art-systems.md` is byte-identical to the research report. Original files remain the source of record.":
            "The current supplied documents in `training/original-docs/` are the source of record. `AGENT-PIXELART-TRAINING.md`, `PIXEL-ART-DEEP-RESEARCH.md`, and `PIXEL-ART-METHODS.md` are related formulations of one technical-research body, so repeated claims across them do not receive independent evidence weight. The current deep-research and methods files are distinct revisions rather than byte-identical duplicates. The reviewed migration and all 93 old/current locator pairs are recorded in [source-migration.json](../../knowledge/source-migration.json), with reproducible results in [range-review.json](../../evidence/source-migration/range-review.json).",
        "| [AGENT-PIXELART-TRAINING.md](../../training/original-docs/AGENT-PIXELART-TRAINING.md) | 1–1657 | Full technical content and formatting comparison | `bb21cee0a39b504f7f4e56f61f13750b57178fe2b6230f27e79b28b40934a050` |\n| [pixel-art-deep-research-report.md](../../training/original-docs/PIXEL-ART-DEEP-RESEARCH.md) | 1–1647 | Canonical local line references for the technical methods | `3edf15db8c02eb3cc7225769416ef6924ef0ebe613cd3430a315389534434727` |\n| [research-pixel-art-systems.md](../../training/original-docs/PIXEL-ART-METHODS.md) | 1–1647 | Duplicate identity verified; no independent evidence weight | `3edf15db8c02eb3cc7225769416ef6924ef0ebe613cd3430a315389534434727` |\n| [PIXEL-ART-ASSETS.md](../../training/original-docs/PIXEL-ART-ASSETS.md) | 1–16070 | Heading inventory plus representative sections and dependency/provenance searches; not a line-by-line audit of every embedded demo | `450a335ed6563a7f4a5cc380f2bbe72f98b70e532ac2c8d16a679bcc545d4900` |":
            "| [AGENT-PIXELART-TRAINING.md](../../training/original-docs/AGENT-PIXELART-TRAINING.md) | 1–1657 | Six current locators plus technical-content comparison | `bb21cee0a39b504f7f4e56f61f13750b57178fe2b6230f27e79b28b40934a050` |\n| [PIXEL-ART-DEEP-RESEARCH.md](../../training/original-docs/PIXEL-ART-DEEP-RESEARCH.md) | 1–1713 | Canonical current line references for 68 locators | `7efc4789ca70dfd9964abc2bc1100af318306236400e3496f7a0a5654f725e28` |\n| [PIXEL-ART-METHODS.md](../../training/original-docs/PIXEL-ART-METHODS.md) | 1–1703 | Related current revision; compared to correct the former duplicate claim, but not cited as independent confirmation | `d2322da8817ec0aaddf82d87844d6fbf289568aff0c15750a40c736c7f5cb466` |\n| [PIXEL-ART-ASSETS.md](../../training/original-docs/PIXEL-ART-ASSETS.md) | 1–16070 | Nineteen current locators plus heading inventory and representative dependency/provenance sections; not a line-by-line audit of every embedded demo | `450a335ed6563a7f4a5cc380f2bbe72f98b70e532ac2c8d16a679bcc545d4900` |\n\nBefore migration, the bundled `pixel-art-deep-research-report.md` and `research-pixel-art-systems.md` were byte-identical 1,647-line files with SHA-256 `3edf15db8c02eb3cc7225769416ef6924ef0ebe613cd3430a315389534434727`. That remains a historical provenance fact, and those bytes are archived under `evidence/source-migration/previous/`; it does not describe the current 1,713-line deep-research or 1,703-line methods revision. Relative to the historical report, the current deep-research file adds 30 Markdown math-fence pairs, changes only the `Diffuse response` heading level, and appends a six-line marker. The current methods file adds 25 math-fence pairs, retains the old heading level, and appends the same marker.",
        "Each method now links to an executable reference fixture. The focused command is `python -W error::DeprecationWarning -m unittest tests.test_poc -v`; final per-test results are in the root verification report. Coverage includes failure injection, all-method coverage, report hashes, runner/source drift, missing-source refusal, temporary working directories and plugin resource resolution. The reference runner writes `poc-report.json` and eight PNGs to its selected output directory. `key-contact-sheet.png` contains positive then deliberately damaged rows; its columns show a flat mask, dark, light and checker backgrounds, with native-size and 4x views in each cell. The geometric check validates hole, shaft and tooth landmarks, while final visual acceptance remains separate.":
            "Each method links to an executable reference fixture. The focused command is `python -W error::DeprecationWarning -m unittest tests.test_poc -v`. The archived pre-migration run covered failure injection, all-method coverage, report hashes, runner/source drift, missing-source refusal, temporary working directories and plugin resource resolution; its results remain historical until the command is re-executed against the migrated registry and current sources. The reference runner writes `poc-report.json` and eight PNGs to its selected output directory. `key-contact-sheet.png` contains positive then deliberately damaged rows; its columns show a flat mask, dark, light and checker backgrounds, with native-size and 4x views in each cell. The geometric check validates hole, shaft and tooth landmarks, while final visual acceptance remains separate.",
    }
    for old, new in replacements.items():
        if text.count(old) != 1:
            raise AssertionError(f"documentation replacement count was not one: {old[:80]!r}")
        text = text.replace(old, new)

    citation_pattern = re.compile(
        r"\[pixel-art-deep-research-report\.md\]"
        r"\(\.\./\.\./training/original-docs/PIXEL-ART-DEEP-RESEARCH\.md\) "
        r"lines (\d+)–(\d+)"
    )

    def replace_citation(match: re.Match[str]) -> str:
        start, end = mapped_range(
            int(match.group(1)), int(match.group(2)), line_map, inserted_fence_lines
        )
        return (
            "[PIXEL-ART-DEEP-RESEARCH.md]"
            "(../../training/original-docs/PIXEL-ART-DEEP-RESEARCH.md) "
            f"lines {start}–{end}"
        )

    text, citation_count = citation_pattern.subn(replace_citation, text)
    if citation_count != 68:
        raise AssertionError(f"expected 68 deep-research citations, got {citation_count}")

    dither_start, dither_end = mapped_range(717, 734, line_map, inserted_fence_lines)
    game_start, game_end = mapped_range(1584, 1645, line_map, inserted_fence_lines)
    palette_start, palette_end = mapped_range(1078, 1126, line_map, inserted_fence_lines)
    text = text.replace(
        "the report's 4×4 masks labeled 25%, 50% and 75% at lines 717–734",
        "the current deep-research file's 4×4 masks labeled 25%, 50% and 75% "
        f"at [lines {dither_start}–{dither_end}]"
        "(../../training/original-docs/PIXEL-ART-DEEP-RESEARCH.md)",
    )
    text = text.replace(
        "the report itself rejects the unverified Metal Slug skeletal claim and Arco subpixel-pipeline claim at lines 13–18 and 1584–1645",
        "the current deep-research file rejects the unverified Metal Slug skeletal "
        "claim at [lines 13–18]"
        "(../../training/original-docs/PIXEL-ART-DEEP-RESEARCH.md) and the Arco "
        f"subpixel-pipeline claim at [lines {game_start}–{game_end}]"
        "(../../training/original-docs/PIXEL-ART-DEEP-RESEARCH.md)",
    )
    text = text.replace(
        "[report lines 1078–1126](../../training/original-docs/PIXEL-ART-DEEP-RESEARCH.md)",
        f"[PIXEL-ART-DEEP-RESEARCH.md lines {palette_start}–{palette_end}]"
        "(../../training/original-docs/PIXEL-ART-DEEP-RESEARCH.md)",
    )
    return text


def verify_documentation(registry: dict[str, Any]) -> None:
    text = (ROOT / "docs/research/pixel-art-knowledge.md").read_text(
        encoding="utf-8"
    )
    assert "[pixel-art-deep-research-report.md]" not in text
    assert "[research-pixel-art-systems.md]" not in text
    required_identities = [
        (
            "PIXEL-ART-DEEP-RESEARCH.md",
            "1–1713",
            "7efc4789ca70dfd9964abc2bc1100af318306236400e3496f7a0a5654f725e28",
        ),
        (
            "PIXEL-ART-METHODS.md",
            "1–1703",
            "d2322da8817ec0aaddf82d87844d6fbf289568aff0c15750a40c736c7f5cb466",
        ),
        (
            "AGENT-PIXELART-TRAINING.md",
            "1–1657",
            "bb21cee0a39b504f7f4e56f61f13750b57178fe2b6230f27e79b28b40934a050",
        ),
        (
            "PIXEL-ART-ASSETS.md",
            "1–16070",
            "450a335ed6563a7f4a5cc380f2bbe72f98b70e532ac2c8d16a679bcc545d4900",
        ),
    ]
    for label, line_range, digest in required_identities:
        assert label in text
        assert line_range in text
        assert digest in text
    assert "byte-identical 1,647-line files" in text
    assert "current 1,713-line deep-research or 1,703-line methods revision" in text

    decision_table = text.split("## WHO / WHAT / WHERE / WHY decisions", 1)[1].split(
        "## Reproducible POC acceptance inventory", 1
    )[0]
    table_lines = {
        match.group(1): match.group(0)
        for match in re.finditer(
            r"^\| `([^`]+)`[^\n]+$", decision_table, re.MULTILINE
        )
    }
    for method in registry["methods"]:
        line = table_lines[method["id"]]
        for source in method["sources"]:
            label = Path(source["path"]).name
            locator = (
                f"[{label}](../../{source['path']}) lines "
                f"{source['start']}–{source['end']}"
            )
            assert locator in line, (method["id"], locator)


def analyze() -> None:
    registry = json.loads(OLD_KNOWLEDGE_PATH.read_text(encoding="utf-8"))
    old_path, current_path = OLD_TO_CURRENT["pixel-art-deep-research-report.md"]
    mapping, changes, inserted_fence_lines = build_line_map(old_path, current_path)
    rows = []
    for method in registry["methods"]:
        for source_index, source in enumerate(method["sources"]):
            old_name = Path(source["path"]).name
            if old_name not in OLD_TO_CURRENT:
                raise AssertionError(f"unknown source path: {source['path']}")
            old_source, current_source = OLD_TO_CURRENT[old_name]
            if old_name == "pixel-art-deep-research-report.md":
                new_start, new_end = mapped_range(
                    source["start"], source["end"], mapping, inserted_fence_lines
                )
            else:
                new_start = source["start"]
                new_end = source["end"]
            rows.append(
                {
                    "method_id": method["id"],
                    "source_index": source_index,
                    "old": {
                        "path": old_source,
                        "historical_path": source["path"],
                        "start": source["start"],
                        "end": source["end"],
                    },
                    "current": {
                        "path": current_source,
                        "start": new_start,
                        "end": new_end,
                    },
                }
            )
    print(json.dumps({"changes": changes, "rows": rows}, indent=2, ensure_ascii=False))


def render(name: str) -> None:
    registry, migration, review = build_artifacts()
    values = {
        "knowledge": registry,
        "migration": migration,
        "review": review,
    }
    print(build_documentation() if name == "docs" else serialized(values[name]), end="")


def render_patch(name: str) -> None:
    registry, migration, review = build_artifacts()
    targets = {
        "knowledge": ("knowledge/pixel-art.json", serialized(registry)),
        "migration": ("knowledge/source-migration.json", serialized(migration)),
        "review": ("evidence/source-migration/range-review.json", serialized(review)),
        "docs": ("docs/research/pixel-art-knowledge.md", build_documentation()),
    }
    relative_path, desired = targets[name]
    path = ROOT / relative_path
    print("*** Begin Patch")
    if not path.exists():
        print(f"*** Add File: {relative_path}")
        for line in desired.splitlines():
            print(f"+{line}")
    else:
        current = path.read_text(encoding="utf-8")
        diff = list(
            difflib.unified_diff(
                current.splitlines(),
                desired.splitlines(),
                fromfile=relative_path,
                tofile=relative_path,
                lineterm="",
            )
        )
        print(f"*** Update File: {relative_path}")
        for line in diff[2:]:
            print("@@" if line.startswith("@@ ") else line)
    print("*** End Patch")


def verify() -> None:
    migration = json.loads(MIGRATION_PATH.read_text(encoding="utf-8"))
    review = json.loads(REVIEW_PATH.read_text(encoding="utf-8"))
    registry = json.loads(KNOWLEDGE_PATH.read_text(encoding="utf-8"))
    expected_registry, expected_migration, expected_review = build_artifacts()

    assert registry == expected_registry
    assert migration == expected_migration
    assert review == expected_review
    verify_documentation(registry)

    assert migration["version"] == 1
    assert migration["citation_count"] == 93
    assert len(migration["citations"]) == 93
    assert review["status"] == "pass"
    assert review["citation_count"] == 93

    source_pairs = migration["source_documents"]
    for old_name, (old_path, current_path) in OLD_TO_CURRENT.items():
        pair = source_pairs[old_name]
        preserved = source_info(old_path)
        assert pair["old"] == {
            "path": old_name,
            "preserved_path": old_path,
            "pre_packaging_observed_path": (
                f"plugins/pixl/resources/{old_name}"
                if old_name != "pixel-art-deep-research-report.md"
                else "plugins/pixl/resources/pixel-art-deep-research-report.md"
            ),
            "sha256": preserved["sha256"],
            "bytes": preserved["bytes"],
            "lines": preserved["lines"],
        }
        assert pair["current"] == source_info(current_path)

    old_research, current_research = OLD_TO_CURRENT[
        "pixel-art-deep-research-report.md"
    ]
    line_map, changes, inserted_fence_lines = build_line_map(
        old_research, current_research
    )
    assert changes == migration["research_correspondence"]["changes"]

    methods = {method["id"]: method for method in registry["methods"]}
    seen: set[tuple[str, int]] = set()
    relocated = 0
    formatted = 0
    for row in migration["citations"]:
        key = (row["method_id"], row["source_index"])
        assert key not in seen
        seen.add(key)
        method = methods[row["method_id"]]
        current = method["sources"][row["source_index"]]
        assert current == {
            "path": row["current"]["path"],
            "start": row["current"]["start"],
            "end": row["current"]["end"],
        }

        old = row["old"]
        current_record = row["current"]
        old_info = source_pairs[row["old_source_name"]]["old"]
        current_info = source_pairs[row["old_source_name"]]["current"]
        assert old["path"] == old_info["path"]
        assert old["sha256"] == old_info["sha256"]
        assert current_record["path"] == current_info["path"]
        assert current_record["sha256"] == current_info["sha256"]

        old_slice = range_slice(
            old_info["preserved_path"], old["start"], old["end"]
        )
        current_slice = range_slice(
            current_record["path"], current_record["start"], current_record["end"]
        )
        assert row["correspondence"]["old_slice_sha256"] == json_digest(old_slice)
        assert row["correspondence"]["current_slice_sha256"] == json_digest(
            current_slice
        )
        if row["correspondence"]["kind"] == "byte-identical-relocation":
            relocated += 1
            assert old_slice == current_slice
            assert row["correspondence"]["normalization"] == []
        else:
            formatted += 1
            assert row["correspondence"]["kind"] == "reviewed-revision-line-migration"
            expected_start, expected_end = mapped_range(
                old["start"], old["end"], line_map, inserted_fence_lines
            )
            assert current_record["start"] == expected_start
            assert current_record["end"] == expected_end
            assert old_slice == normalize_current_research_slice(
                current_slice, current_record["start"], set(inserted_fence_lines)
            )
        assert row["correspondence"]["result"] == "pass"

    assert len(seen) == sum(len(method["sources"]) for method in registry["methods"])
    assert relocated == 25
    assert formatted == 68
    assert review["counts"] == {
        "byte_identical_relocations": relocated,
        "formatting_only_line_migrations": formatted,
        "methods": len(registry["methods"]),
        "non_source_method_fields_changed": 0,
    }
    assert review["migrated_knowledge_sha256"] == sha256_bytes(
        KNOWLEDGE_PATH.read_bytes()
    )
    assert review["non_source_fields_sha256"] == json_digest(without_sources(registry))
    assert review["migration_manifest_sha256"] == sha256_bytes(
        MIGRATION_PATH.read_bytes()
    )
    print(
        "PASS: 93/93 reviewed locators resolve; "
        "25 byte-identical relocations; 68 formatting-only line migrations; "
        "43/43 methods retain the recorded non-source digest."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument(
        "--render", choices=("knowledge", "migration", "review", "docs")
    )
    parser.add_argument("--patch", choices=("knowledge", "migration", "review", "docs"))
    args = parser.parse_args()
    if args.analyze:
        analyze()
    elif args.render:
        render(args.render)
    elif args.patch:
        render_patch(args.patch)
    else:
        verify()


if __name__ == "__main__":
    main()
