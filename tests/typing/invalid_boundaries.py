"""Intentional static errors. The gate parses this file with mypy; never execute it."""

from pathlib import Path

from pixl import caller_result, candidate_review, handoff, jobs, store
from pixl.codec import Document
from pixl.operation_types import PublicationResult, SectionLocator


def missing_publication() -> PublicationResult:
    return {"revision": 1, "state": ".pixl/state.px"}  # expect: missing-publication-hash [typeddict-item]


def wrong_publication() -> PublicationResult:
    return {"revision": "1", "hash": "hash", "state": ".pixl/state.px"}  # expect: publication-revision-type [typeddict-item]


def producer_result(root: Path, doc: Document) -> None:
    published = store.initialize(root / ".pixl", doc, root=root)
    published["hash"] = 123  # expect: publication-producer-hash-type [typeddict-item]


def observation_is_not_dispatch(root: Path, expected: str) -> object:
    observed = jobs.observe(root / ".pixl", expected, "job", "unknown", {"note": "Lost reply"}, root=root)
    return observed["dispatch_request"]  # expect: observation-has-no-dispatch-request [typeddict-item]


def observation_cannot_be_dispatch_result(root: Path, expected: str) -> jobs.JobDispatchResult:
    return jobs.observe(root / ".pixl", expected, "job", "unknown", {}, root=root)  # expect: observation-is-not-dispatch-result [return-value]


def legacy_has_no_durable_context(row: jobs.JobSummary) -> None:
    if not row["durable"]:
        print(row["context"])  # expect: legacy-has-no-durable-context [typeddict-item]


def invalid_verdict(verdict: candidate_review.CriterionVerdict) -> None:
    verdict["status"] = "accepted"  # expect: verdict-status-enum [typeddict-item]
    verdict["observations"] = ["0"]  # expect: observation-index-type [list-item]


def invalid_review(request: candidate_review.ReviewObservation) -> None:
    request["version"] = 2  # expect: review-version-literal [typeddict-item]
    request["action"] = "dispatch"  # expect: review-action-enum [typeddict-item]


def absent_caller(caller: caller_result.PreparedCaller) -> None:
    if not caller["present"]:
        print(caller["file_verification"])  # expect: absent-caller-has-no-file-verification [typeddict-item]


def invalid_locator(locator: SectionLocator) -> None:
    locator["start"] = "first"  # expect: locator-line-type [typeddict-item]


def receipt_is_not_caller(root: Path, expected: str) -> object:
    receipt = handoff.save(root, "asset", expected, expected, {"status": "partial"}, view="receipt")
    return receipt["caller"]  # expect: receipt-has-no-caller-view [typeddict-item]
