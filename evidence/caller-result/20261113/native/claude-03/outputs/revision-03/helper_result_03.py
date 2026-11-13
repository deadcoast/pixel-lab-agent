"""Revision-03 helper: write work/compact-caller/revision-03/SPECIALIST-RESULT.json.

New file only; verifies the referenced files from their actual bytes first.
Run with: python -I -B helper_result_03.py <consumer-root>
"""
import datetime
import hashlib
import json
import os
import sys

ROOT = sys.argv[1]
os.chdir(ROOT)
H = "88d77c62b47eb8fef5d35015973f67b0f38731cb04e54430efa36aec4b898d64"
R = "ec61d688f752ac1280914d22ba75bdb4e8f7e31c42b18d7d62f7a14038eedea5"
SNAP = ".pixl/handoffs/0f2d80cdc1fdd13c94544116899c9ff053ee061a603d1974997df9194a8765a3.json"


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def ref(p, role=None):
    d = {"path": p, "sha256": sha(p)}
    if role:
        d["role"] = role
    return d


def jl(p):
    with open(p, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


new_compact = jl("work/compact-caller/revision-03/compact.json")
old_compact = jl("work/compact-caller/compact.json")
receipt = jl("work/compact-caller/receipt.json")
details = jl("work/compact-caller/details.json")
handoff = jl(SNAP)
plar = jl("work/compact-caller/revision-03/specialist-plar-read-03.json")
cont = plar["production"]["continuation"]
unk = jl("work/compact-caller/specialist-unknown-jobs.json")

checks = {
    "new_compact_names_snapshot": new_compact["path"] == SNAP and new_compact["sha256"] == sha(SNAP),
    "new_compact_equals_first_child_compact_bytes": sha("work/compact-caller/revision-03/compact.json") == sha("work/compact-caller/compact.json"),
    "receipt_names_snapshot": receipt["path"] == SNAP and receipt["sha256"] == new_compact["sha256"],
    "receipt_sha_retained": sha("work/compact-caller/receipt.json") == "6878691886ac3ab0221a5f03fd7efea96f12e6ce32f7ccfdf437f90cdd33e0e3",
    "handoff_details_equals_details_json": handoff["details"] == details,
    "identities_current_plar_read_03": plar["asset"]["id"] == "queue.working" and plar["path"] == "authoring-plar.txt"
    and plar["requirements_hash"] == R and cont["state_hash"] == H and cont["requirements_hash"] == R
    and cont["action"] == "delivered" and plar["production"]["revision"] == 108 and cont["jobs"] == [],
    "new_compact_identities": new_compact["asset_id"] == "queue.working" and new_compact["requirements_hash"] == R
    and new_compact["state_hash"] == H and new_compact["next"] == "delivered" and new_compact["caller"]["present"] is True
    and new_compact["assignment"]["status"] == "partial",
    "handoff_count_unchanged": len([f for f in os.listdir(".pixl/handoffs") if f.endswith(".json")]) == 11,
    "history_files_unchanged": sha("work/compact-caller/SPECIALIST-REPORT.json") == "7390a062f174405010b9472c952bb7948aa7748684220bb3682650e700c9f303"
    and sha("work/compact-caller/SPECIALIST-RESULT.json") == "ce38956d5f3ddf73e0a5e543385fa5fde5fdc6a67d54f0895220ce809e734236"
    and sha("work/compact-caller/details.json") == "92682b133f09898b20e620fd0e9aea94f2aad3b5aae511f2ceec9defa87a3dc2"
    and sha("work/compact-caller/compact.json") == "ff5c2289915ce12c26cc69073759f6254e154d341a631465d262ff8720900687",
    "unknown_fixture_unchanged_as_read": unk["hash"] == "3ab0c1633edbf21977744bab59eb2a15b2cd8dc81424ea3cfe6c569d5f35e0a9"
    and unk["revision"] == 9 and unk["jobs"][0]["state"] == "unknown" and unk["jobs"][0]["remote_id"] is None,
}
assert all(checks.values()), checks

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
res = {
    "version": 1,
    "kind": "specialist_result",
    "revision": "03",
    "status": "partial",
    "observed_at": now,
    "native_child": {
        "role": "pixl",
        "agent_id": "ab352c80d7f534aae",
        "canonical_task": "pixl:pixl specialist",
        "publication_provenance": {
            "original_caller_view": {
                "published_by": "first child ac98550e535c93d5a",
                "published_on": "2026-11-10",
                "file": ref("work/compact-caller/compact.json", "first child's caller-view return (history, preserved)"),
                "handoff": {"path": SNAP, "sha256": sha(SNAP)},
            },
            "receipt_view": {"performed_by": "ab352c80d7f534aae", "file": ref("work/compact-caller/receipt.json")},
            "caller_view_revision_03": {"performed_by": "ab352c80d7f534aae", "performed_at": now,
                                        "file": ref("work/compact-caller/revision-03/compact.json")},
        },
        "activation": "Native registered pixl:pixl role invoked by the coordinator for the QOL-10/SC-08 SPECIALIST "
                      "reporting assignment. The details.json / SPECIALIST-REPORT.json / caller-view compact.json of "
                      "2026-11-10 were produced by the first child ac98550e535c93d5a, whose session was interrupted. "
                      "This child (ab352c80d7f534aae) resumed on 2026-11-13: reconciled those preserved outputs, "
                      "performed the receipt-view call, wrote work/compact-caller/SPECIALIST-RESULT.json, and in this "
                      "revision performed its own actual caller-view call with the identical details object. No "
                      "existing file was modified; no provider action, acceptance or state change occurred.",
    },
    "assignment": "QOL-10/SC-08 compact-result evaluation, SPECIALIST part: reporting/handoff only; no art "
                  "production, provider call, acceptance, commit, PLAR save, plan, prepare or configuration change.",
    "identities": {"asset_id": "queue.working", "plar_path": "authoring-plar.txt", "store": ".pixl/assets/queue.ready",
                   "state_path": ".pixl/assets/queue.ready/state.px", "state_hash": H, "revision": 108,
                   "requirements_hash": R, "plar_file_sha256": plar["hash"],
                   "hash_domains": {"state_hash": "canonical_state_sha256",
                                    "requirements_hash": "selected_requirements_sha256",
                                    "plar_file_sha256": "file_sha256", "sha256": "file_sha256"}},
    "compact": ref("work/compact-caller/revision-03/compact.json"),
    "compact_names_same_snapshot": True,
    "compact_byte_identical_to_first_child_publication": True,
    "receipt": ref("work/compact-caller/receipt.json"),
    "receipt_names_same_snapshot": True,
    "snapshot": {"path": SNAP, "sha256": sha(SNAP)},
    "details": ref("work/compact-caller/details.json", "exact details object used by all three handoff calls (first child authored)"),
    "detailed_report": ref("work/compact-caller/SPECIALIST-REPORT.json", "history: first child's detailed report"),
    "prior_specialist_result": ref("work/compact-caller/SPECIALIST-RESULT.json", "history: this child's session-2 result (provenance attribution superseded by this file)"),
    "prior_reconciliation": ref("work/compact-caller/specialist-reconcile.json", "history: session-2 reconciliation"),
    "plar_read_revision_03": ref("work/compact-caller/revision-03/specialist-plar-read-03.json", "pixl_plar_read asset_id=queue.working path=authoring-plar.txt (this revision, exact return bytes)"),
    "checks": checks,
    "compact_key_fields": {"next": new_compact["next"], "assignment": new_compact["assignment"],
                           "caller_present": new_compact["caller"]["present"], "details_ref": new_compact["details_ref"],
                           "resume_ref": new_compact["resume_ref"], "refresh": new_compact["refresh"],
                           "store": new_compact["store"]},
    "reconciliation_note": (
        "Publication provenance: the caller view in work/compact-caller/compact.json and the immutable handoff "
        + SNAP + " were published on 2026-11-10 by the first child ac98550e535c93d5a, which also authored "
        "details.json and SPECIALIST-REPORT.json before its session was interrupted. This child "
        "(ab352c80d7f534aae) did not perform that publication; the earlier work/compact-caller/SPECIALIST-RESULT.json "
        "described session 1 as this child's own interrupted session, which was incorrect and is retained as history "
        "rather than rewritten. This child performed the receipt-view call (receipt.json) and, in this revision, its "
        "own actual mcp__pixl-local__pixl_plar_handoff view=caller call with the identical details object and "
        "identities (asset_id queue.working, path authoring-plar.txt, requirements_hash " + R + ", expect " + H + "). "
        "The runtime returned the same existing immutable handoff (no new snapshot, handoff count unchanged at 11) and "
        "the saved return is byte-identical to the first child's compact.json. Nothing changed semantically: the "
        "assignment remains partial (a separately controlled fictional-fixture remote observation, controlled-unknown "
        "member.job, is unknown and was only read), while the artistic production for queue.working remains delivered "
        "(artistic-02.working.task done, 14/14 criteria pass; family artistic-02.delivery.task done and accepted; "
        "assets/working.png cf101610... matches). The fixture member.job (state unknown, remote_id null, provider "
        "fictional-fixture, fixture state hash 3ab0c163... rev 9) is separate from and never attached to the production."
    ),
    "controlled_unknown_fixture": {
        "label": "CONTROLLED FICTIONAL FIXTURE, NOT PRODUCTION; unrelated to queue.working",
        "root": "controlled-unknown", "store": ".pixl", "state_path": ".pixl/state.px", "job_id": "member.job",
        "state": "unknown", "remote_id": None, "provider": "fictional-fixture", "next_action": "reconcile",
        "state_hash": unk["hash"], "revision": unk["revision"], "touched": False,
        "evidence": ref("work/compact-caller/specialist-unknown-jobs.json", "session-1 read; not re-read in this revision"),
    },
    "limits": [
        "No fresh renderer run; integration evidence in the caller block is retained prior captures, labelled not_performed.",
        "No provider observation; the failed official job authoring-01.working.join-01 and the fictional unknown job member.job were only read (the fixture was not re-read in this revision).",
        "Controlled-unknown member.job left state=unknown, untouched.",
        "No acceptance, nomination, commit, PLAR save, plan, prepare or configuration change; no existing file modified.",
        "The details object is first-child authored; this child adopted it unchanged for its own handoff calls rather than re-authoring findings.",
        "SPECIALIST-REPORT.json stale_plan01.diagnostic_state sha 07110fbe... is the historical canonical state hash at revision 92, not the current state.px file hash (report retained unchanged).",
    ],
    "next_action": "Caller: compare the compact result identities against a fresh focused pixl_plar_read, adopt or "
                   "reject the agent-authored caller block, and resolve the controlled-unknown fixture only inside its own root.",
}
q = "work/compact-caller/revision-03/SPECIALIST-RESULT.json"
assert not os.path.exists(q)
with open(q, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(res, indent=2, ensure_ascii=False) + "\n")
print("result", sha(q))
print("compact", sha("work/compact-caller/revision-03/compact.json"))
