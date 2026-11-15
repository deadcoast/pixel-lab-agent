"""Static-only consumers of the real TM-01 operations; never execute these examples."""

from pathlib import Path
from typing import Literal, assert_type

from pixl import caller_result, candidate_review, handoff, jobs, store
from pixl.codec import Document
from pixl.operation_types import HandoffReceipt, PublicationResult, SectionLocator


def publication(root: Path, current: Document, candidate: Document, expected: str) -> None:
    created = store.initialize(root / ".pixl", current, root=root)
    assert_type(created, PublicationResult)
    assert_type(created["revision"], int)
    assert_type(created["hash"], str)
    assert_type(store.load(root / ".pixl"), Document)
    assert_type(store.commit(root / ".pixl", candidate, expected, root=root), PublicationResult)


def job_operations(root: Path, expected: str, doc: Document, evidence: object) -> None:
    prepared = jobs.prepare(root / ".pixl", expected, "job", "task", ["output"], "provider",
                            "tool", {}, {}, {}, {}, root=root)
    assert_type(prepared, jobs.JobMutationResult)
    observed = jobs.observe(root / ".pixl", expected, "job", "unknown", evidence, root=root)
    assert_type(observed, jobs.JobMutationResult)
    assert_type(observed["job"], jobs.DurableJobSummary)
    assert_type(observed["remote_executed"], Literal[False])
    dispatched = jobs.dispatch(root / ".pixl", expected, "job", root=root)
    assert_type(dispatched, jobs.JobDispatchResult)
    assert_type(dispatched["dispatch_request"], jobs.JsonObject)
    imported = jobs.import_artifact(root / ".pixl", expected, "job", "output", "candidate",
                                    "work/candidate.png", evidence, root=root)
    assert_type(imported, jobs.JobImportResult)
    assert_type(imported["reused_import"], bool)
    report = jobs.report(doc, root, root / ".pixl")
    assert_type(report, jobs.JobReport)
    for row in report["jobs"]:
        if row["durable"]:
            assert_type(row, jobs.DurableJobSummary)
            assert_type(row["context"]["outputs"], list[str])
        else:
            assert_type(row, jobs.LegacyJobSummary)
            assert_type(row["next_action"], Literal["inspect_legacy_history"])


def review(root: Path, doc: Document, expected: str, request: object) -> None:
    context = candidate_review.context(doc, root, "candidate")
    assert_type(context, candidate_review.ReviewContext)
    assert_type(context["current_acceptance"]["all_required_pass"], bool)
    result = candidate_review.submit(root / ".pixl", expected, "candidate", "review", request, root=root)
    assert_type(result, candidate_review.CandidateReviewResult)
    assert_type(result["publications"], list[PublicationResult])
    assert_type(result["reused_review"], bool)
    observation: candidate_review.ReviewObservation = {
        "version": 1, "binding_hash": expected, "reviewer": "reviewer",
        "observed_at": "2026-11-14T00:00:00+00:00", "observations": [],
        "verdicts": [{"criterion": "criterion", "status": "unavailable", "reason": "Not observed",
                      "supersedes": None, "observations": []}],
        "action": "record", "next_action": "Obtain the missing observation", "limitations": [],
    }
    assert_type(observation["verdicts"][0]["observations"], list[int])


def caller(root: Path, expected: str, details: dict[str, object], data: bytes) -> None:
    prepared = caller_result.prepare(root, details)
    assert_type(prepared, caller_result.AbsentCaller | caller_result.PresentCaller)
    if prepared["present"]:
        assert_type(prepared, caller_result.PresentCaller)
        assert_type(prepared["file_verification"], str)
    else:
        assert_type(prepared, caller_result.AbsentCaller)
        assert_type(prepared["reason"], str)
    receipt = handoff.save(root, "asset", expected, expected, details)
    assert_type(receipt, HandoffReceipt)
    assert_type(caller_result._locator(receipt, data, "details"), SectionLocator)
    result = handoff.save(root, "asset", expected, expected, details, view="caller")
    assert_type(result, caller_result.CallerResult)
    assert_type(result["details_ref"]["start"], int)
    assert_type(result["refresh"]["operation"], Literal["pixl_plar_read"])
    assert_type(handoff.save(root, "asset", expected, expected, details, "plar.txt", "caller"),
                caller_result.CallerResult)
