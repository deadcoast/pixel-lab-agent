"""Session-2 helper: write specialist-reconcile.json and SPECIALIST-RESULT.json.

Creates new files only; asserts the preserved session-1 files are unchanged.
Run with: python -I -B helper_result_02.py <consumer-root>
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


now = datetime.datetime.now(datetime.timezone.utc).isoformat()
details = jl("work/compact-caller/details.json")
compact = jl("work/compact-caller/compact.json")
receipt = jl("work/compact-caller/receipt.json")
handoff = jl(compact["path"])
plar = jl("work/compact-caller/specialist-plar-read-02.json")
unk = jl("work/compact-caller/specialist-unknown-jobs.json")
cont = plar["production"]["continuation"]
prod = plar["production"]

checks = {
    "handoff_file_exists": os.path.exists(compact["path"]),
    "handoff_file_sha_matches_compact": sha(compact["path"]) == compact["sha256"],
    "handoff_details_equals_details_json": handoff["details"] == details,
    "handoff_identities": handoff["asset_id"] == "queue.working" and handoff["requirements_hash"] == R
    and handoff["resume"]["state_hash"] == H and handoff["resume"]["action"] == "delivered",
    "compact_identities_current": compact["asset_id"] == "queue.working" and compact["requirements_hash"] == R
    and compact["state_hash"] == H,
    "plar_read_02_identities_current": plar["asset"]["id"] == "queue.working" and plar["path"] == "authoring-plar.txt"
    and plar["requirements_hash"] == R and cont["state_hash"] == H and cont["requirements_hash"] == R
    and cont["action"] == "delivered" and prod["revision"] == 108 and prod["task_state"] == "done"
    and prod["store"] == ".pixl/assets/queue.ready" and cont["jobs"] == [],
    "plar_read_02_byte_identical_to_session1": sha("work/compact-caller/specialist-plar-read-02.json")
    == sha("work/compact-caller/specialist-plar-read.json"),
    "receipt_names_same_snapshot": receipt["path"] == compact["path"] and receipt["sha256"] == compact["sha256"],
    "receipt_identities": receipt["asset_id"] == "queue.working" and receipt["requirements_hash"] == R
    and receipt["state_hash"] == H and receipt["next"] == "delivered",
    "no_new_handoff_created_by_receipt_call": len([f for f in os.listdir(".pixl/handoffs") if f.endswith(".json")]) == 11,
    "preserved_session1_files_unchanged":
        sha("work/compact-caller/compact.json") == "ff5c2289915ce12c26cc69073759f6254e154d341a631465d262ff8720900687"
        and sha("work/compact-caller/details.json") == "92682b133f09898b20e620fd0e9aea94f2aad3b5aae511f2ceec9defa87a3dc2"
        and sha("work/compact-caller/SPECIALIST-REPORT.json") == "7390a062f174405010b9472c952bb7948aa7748684220bb3682650e700c9f303",
    "unknown_fixture_read_only_state": unk["hash"] == "3ab0c1633edbf21977744bab59eb2a15b2cd8dc81424ea3cfe6c569d5f35e0a9"
    and unk["revision"] == 9 and unk["jobs"][0]["state"] == "unknown" and unk["jobs"][0]["remote_id"] is None,
}
assert all(checks.values()), checks

HISTORICAL_NOTE = (
    "SPECIALIST-REPORT.json stale_plan01.diagnostic_state cites .pixl/assets/queue.ready/state.px with sha256 "
    "07110fbe5dd6df111c2637ea00acee3a24af0e9614f9e99f4b369e8d9dbc718c and revision 92. That value is the canonical "
    "state hash recorded in work/artistic-revision/request-review-02.json when plan01 was diagnosed (historical "
    "identity), not the current state.px file hash. The current canonical state hash is 88d77c62... revision 108. "
    "The report is retained unchanged; read that field as a historical canonical_state_sha256."
)

rec = {
    "version": 1,
    "kind": "specialist_reconciliation",
    "observed_at": now,
    "assignment": "QOL-10/SC-08 compact-result evaluation, SPECIALIST part, resumed after HTTP 429 / host timeout "
                  "interruption. Read-only reconciliation of the session-1 outputs; no provider call, acceptance, "
                  "commit or edit of existing files.",
    "identities": {"asset_id": "queue.working", "plar_path": "authoring-plar.txt", "store": ".pixl/assets/queue.ready",
                   "state_hash": H, "revision": 108, "requirements_hash": R, "plar_file_sha256": plar["hash"]},
    "snapshot": {"path": compact["path"], "sha256": sha(compact["path"])},
    "checks": checks,
    "helper_verify_02": {"ref": ref("work/compact-caller/helper_verify_02.py"),
                         "result": "172 checks, 1 flagged item (see interpretation_notes)"},
    "interpretation_notes": [
        HISTORICAL_NOTE,
        "The fresh pixl_plar_read return (specialist-plar-read-02.json) is byte-identical to the session-1 return; "
        "the state did not change between sessions.",
        "The receipt-view call used details equal in parsed value to details.json; the runtime returned the "
        "identical immutable snapshot and created no new handoff file.",
    ],
    "tool_returns": [
        ref("work/compact-caller/specialist-plar-read-02.json",
            "pixl_plar_read asset_id=queue.working path=authoring-plar.txt (session 2, exact return bytes)"),
        ref("work/compact-caller/receipt.json", "pixl_plar_handoff view=receipt (tool-saved result_path)"),
        ref("work/compact-caller/compact.json", "pixl_plar_handoff view=caller (session 1, preserved)"),
    ],
    "controlled_unknown_fixture": {
        "label": "CONTROLLED FICTIONAL FIXTURE, NOT PRODUCTION", "root": "controlled-unknown", "store": ".pixl",
        "job_id": "member.job", "state": "unknown", "remote_id": None, "provider": "fictional-fixture",
        "next_action": "reconcile", "state_hash": unk["hash"], "revision": unk["revision"],
        "touched_this_session": False, "evidence": ref("work/compact-caller/specialist-unknown-jobs.json"),
    },
}
p = "work/compact-caller/specialist-reconcile.json"
assert not os.path.exists(p)
with open(p, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")

res = {
    "version": 1,
    "kind": "specialist_result",
    "status": "partial",
    "observed_at": now,
    "native_child": {
        "role": "pixl",
        "agent_id": "ab352c80d7f534aae",
        "canonical_task": "pixl:pixl specialist",
        "activation": "Native registered pixl:pixl role invoked by the coordinator for the QOL-10/SC-08 SPECIALIST "
                      "reporting assignment. Session 1 produced details.json, SPECIALIST-REPORT.json and the "
                      "caller-view compact.json (handoff 0f2d80cd...) and was interrupted by HTTP 429 then a host "
                      "timeout before the receipt view and this result file. Session 2 (this file) re-read state, "
                      "reconciled the preserved outputs byte-for-byte, obtained the receipt view with identical "
                      "details/identities and wrote this result. No existing file was modified.",
    },
    "assignment": "QOL-10/SC-08 compact-result evaluation, SPECIALIST part: reporting/handoff only; no art "
                  "production, provider call, acceptance, commit, PLAR save, plan, prepare or configuration change.",
    "identities": {"asset_id": "queue.working", "plar_path": "authoring-plar.txt", "store": ".pixl/assets/queue.ready",
                   "state_path": ".pixl/assets/queue.ready/state.px", "state_hash": H, "revision": 108,
                   "requirements_hash": R,
                   "hash_domains": {"state_hash": "canonical_state_sha256",
                                    "requirements_hash": "selected_requirements_sha256", "sha256": "file_sha256"}},
    "compact": ref("work/compact-caller/compact.json"),
    "receipt": ref("work/compact-caller/receipt.json"),
    "receipt_names_same_snapshot": True,
    "detailed_report": ref("work/compact-caller/SPECIALIST-REPORT.json"),
    "details": ref("work/compact-caller/details.json"),
    "snapshot": ref(compact["path"]),
    "reconciliation": ref(p),
    "plar_read_session2": ref("work/compact-caller/specialist-plar-read-02.json"),
    "compact_key_fields": {"next": compact["next"], "assignment": compact["assignment"],
                           "caller_present": compact["caller"]["present"], "details_ref": compact["details_ref"],
                           "resume_ref": compact["resume_ref"], "refresh": compact["refresh"],
                           "store": compact["store"]},
    "controlled_unknown_fixture": {
        "label": "CONTROLLED FICTIONAL FIXTURE, NOT PRODUCTION; unrelated to queue.working",
        "root": "controlled-unknown", "store": ".pixl", "state_path": ".pixl/state.px", "job_id": "member.job",
        "state": "unknown", "remote_id": None, "provider": "fictional-fixture", "next_action": "reconcile",
        "state_hash": unk["hash"], "revision": unk["revision"], "touched": False,
        "evidence": ref("work/compact-caller/specialist-unknown-jobs.json"),
    },
    "limits": [
        "No fresh renderer run; integration evidence in the caller block is retained prior captures, labelled not_performed.",
        "No provider observation; the failed official job authoring-01.working.join-01 and the fictional unknown job member.job were only read.",
        "Controlled-unknown member.job left state=unknown, untouched.",
        "Interrupted-and-resumed session: session-1 outputs preserved byte-for-byte; receipt view and this result were produced in session 2 against an unchanged state (revision 108).",
        "No acceptance, nomination, commit, PLAR save, plan, prepare or configuration change; pixl_asset_check is a measurement only.",
    ],
    "interpretation_notes": [HISTORICAL_NOTE],
    "next_action": "Caller: compare the compact result identities against a fresh focused pixl_plar_read, adopt or "
                   "reject the agent-authored caller block, and resolve the controlled-unknown fixture only inside its own root.",
}
q = "work/compact-caller/SPECIALIST-RESULT.json"
assert not os.path.exists(q)
with open(q, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(res, indent=2, ensure_ascii=False) + "\n")

print("reconcile", sha(p))
print("result", sha(q))
print("preserved still:", sha("work/compact-caller/compact.json"), sha("work/compact-caller/details.json"),
      sha("work/compact-caller/SPECIALIST-REPORT.json"))
