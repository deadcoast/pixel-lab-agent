"""Caller-owned builder for CALLER-RESULT-LITERAL-RECONCILIATION-02.json and its literal review.

Run from the consumer root with the selected interpreter:
  python -B -I work/caller-reconciliation-02/build_caller_result.py result
  python -B -I work/caller-reconciliation-02/build_caller_result.py review
"result" exclusively creates the caller result (never overwrites). "review" exclusively creates the
version-1 review of the result's /remaining_questions and /next_action subtrees, bound to the saved
result's actual hash. Every referenced file hash is measured at run time. The result file is never
listed in its own file references.
"""

import hashlib
import json
import sys

RESULT = "CALLER-RESULT-LITERAL-RECONCILIATION-02.json"
REVIEW = "work/caller-reconciliation-02/caller-result-02-review-01.json"
STATE = "state.px/state.px"


def sha(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def ref(path, role):
    assert path != RESULT
    return {"path": path, "sha256": sha(path), "role": role}


def S(path, first, last=None):
    return {"path": path, "sha256": sha(path), "lines": [first, first if last is None else last]}


_wire = open(STATE, encoding="utf-8").read().splitlines()


def L(record_id):
    prefix = "@" + record_id + ":"
    for number, line in enumerate(_wire, 1):
        if line.startswith(prefix):
            return S(STATE, number)
    raise SystemExit("record not found: " + record_id)


class A:
    """An authored leaf with the caller's independent finding and its sources."""

    def __init__(self, value, finding, sources, basis="source_comparison"):
        self.value, self.finding, self.sources, self.basis = value, finding, sources, basis


def plain(node):
    if isinstance(node, A):
        return node.value
    if isinstance(node, dict):
        return {key: plain(value) for key, value in node.items()}
    if isinstance(node, list):
        return [plain(value) for value in node]
    return node


def rows(node, pointer):
    if isinstance(node, A):
        yield {"pointer": pointer, "expected": node.value, "basis": node.basis,
               "finding": node.finding, "sources": node.sources if node.basis != "metadata" else []}
    elif isinstance(node, dict):
        for key, value in node.items():
            yield from rows(value, pointer + "/" + key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from rows(value, pointer + "/" + str(index))
    else:
        raise SystemExit("unannotated leaf at " + pointer)


BRIEF = "sources/brief.md"
EVAL = "sources/controlled-evaluation-answers.md"
LIFE = "pixl-kit/runtime/pixl/lifecycle.py"
JOBS = "pixl-kit/runtime/pixl/jobs.py"
PLAT = "pixl-kit/runtime/pixl/platform.py"
RREV = "pixl-kit/runtime/pixl/request_review.py"
SKILL = "pixl-kit/skills/pixl/SKILL.md"
PROF = "pixl-kit/resources/agent/PROFILE.md"
READY = "pixl-kit/skills/pixl/references/readiness.md"
DELEG = "pixl-kit/skills/pixl/references/delegation.md"
INTAKE = "pixl-kit/skills/pixl/references/intake-sample.md"
HREV = "pixl-kit/skills/pixl/references/handoff-review.md"
NB = "deliverables/continuation-2026-11-16b.md"
NC = "deliverables/continuation-2026-11-16c.md"
NG = "deliverables/continuation-2026-11-15g.md"
ND = "deliverables/continuation-2026-11-15d.md"
BRIEF2 = "deliverables/sample-request/sample-creative-brief-v2.json"
SHORT = "deliverables/sample-request/operation-shortlist.json"
V7 = "review/caller-comparison-2026-11-16-v7.md"
HEAD = sha(STATE)

remaining_questions = [
    {
        "id": A("RQ1", "Identifier of this question; not an operational claim.", [], "metadata"),
        "addressed_to": A(
            "the caller / host: a capability input, not an owner art decision",
            "platform.py 869-889 lists provider, tool, schema, discovery and authorization as request fields; "
            "SKILL.md 26 and PROFILE.md 32 make the route a host/caller selection; no owner choice is involved.",
            [S(PLAT, 869, 889), S(SKILL, 26), S(PROF, 32)]),
        "necessary_for": A(
            "job-prepare for t_sample / f_sample against c_sample, the next operation",
            "jobs.py 717-743 prepare() calls platform.prepare_discovered with these inputs; without them the call "
            "cannot be made. t_sample is the only ready task.",
            [S(JOBS, 717, 743), L("t_sample")]),
        "question": A(
            "Which official PixelLab operation is available in your host, with what exact live inputSchema; how will "
            "reference.png (sha256 d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7, role style) travel "
            "as an actual image input (upload handle, URL or owned asset ID); and will you supply discovery evidence "
            "(source, host-clock observed_at, nonempty evidence) and an authorization evidence object covering one "
            "paid call? Choose the route: the authenticated official MCP tool surface, or the HTTP adapter "
            "explicitly selected for its documented operation.",
            "Each element maps to a required field: identity and tool 869-870, schema 888-889, discovery 873-876 "
            "and 1017-1023, authorization 874-885. PROFILE.md 44: a filename in a prompt is not an uploaded "
            "reference. readiness.md 101-102: a dated catalog is not live visibility. The authorization scope text "
            "already exists in brief.md 6-7; only the evidence object is missing.",
            [S(PLAT, 869, 889), S(PLAT, 1017, 1023), S(PROF, 44), S(READY, 101, 102), S(BRIEF, 6, 7)]),
        "unlocks": A(
            "Answering SQ1-SQ4 of sample-creative-brief-v2.json (lines 143-146; SQ5-SQ9 at 147-151 in the same pass) "
            "against the live declaration, translating the brief into exact provider arguments, the "
            "provider_arguments successor packet with the criteria-v2 supersession of sample-criteria.json, "
            "pixl_request_review on that packet and the caller's comparison, and then job-prepare. It does not "
            "prepare, dispatch, generate or accept anything by itself.",
            "brief-v2 142-152 holds the schema questions (SQ1-SQ4 at 143-146). request_review.py 130-134 accepts only "
            "kind provider_arguments. delegation.md 69 requires the caller comparison before adopting the request. "
            "g note 61-74 makes the criteria-v2 supersession a required step of that successor packet. c note 56-64 "
            "corrected the locator.",
            [S(BRIEF2, 142, 152), S(RREV, 130, 134), S(DELEG, 69), S(NG, 61, 74), S(NC, 56, 64)]),
        "blocks_next_operation": A(
            True,
            "No default exists for provider identity, tool, schema, discovery or authorization evidence; jobs.py "
            "prepare() cannot be called without them.",
            [S(JOBS, 717, 743), S(PLAT, 869, 889)]),
    },
    {
        "id": A("RQ2", "Identifier of this question; not an operational claim.", [], "metadata"),
        "addressed_to": A(
            "the owner, through the caller",
            "i_display_scale and i_backgrounds are owner choices recorded as unresolved in the head.",
            [L("i_display_scale"), L("i_backgrounds")]),
        "necessary_for": A(
            "visual review of a returned sample candidate (pixl_inspection_prepare / pixl_inspection_review), two "
            "steps after job-prepare; not job-prepare itself",
            "q_sample_readability's check requires i_display_scale before review. Neither choice is linked through "
            "c_sample.ch, so lifecycle.py 57-64 does not gate preparation on them. The d note sequence places review "
            "after import.",
            [L("q_sample_readability"), L("c_sample"), S(LIFE, 57, 64), S(ND, 249, 255)]),
        "question": A(
            "What target integer display scale should the sample be reviewed at? Optionally, what are the typical "
            "level backgrounds of the side-view game?",
            "Both are open in the head; the check text names the target zoom and the test backgrounds.",
            [L("i_display_scale"), L("i_backgrounds"), L("q_sample_readability")]),
        "unlocks": A(
            "The target zoom for q_sample_readability and q_sample_outline in inspection, and representative review "
            "backgrounds in place of the specialist's light, dark and busy test set. The test set is an authorized "
            "fallback for backgrounds; no default exists for the scale.",
            "q_sample_readability states the test backgrounds stand until i_backgrounds is answered and requires "
            "i_display_scale before review; no saved default zoom exists.",
            [L("q_sample_readability"), L("i_display_scale")]),
        "blocks_next_operation": A(
            False,
            "Neither choice is in c_sample.ch; t_sample has no blockers in the workflow; lifecycle.py 57-64 gates only "
            "linked choices.",
            [L("c_sample"), S(LIFE, 57, 64)]),
    },
    {
        "id": A("RQ3", "Identifier of this question; not an operational claim.", [], "metadata"),
        "addressed_to": A(
            "the owner, through the caller",
            "The brief leaves outline, canvas, animation and engine unstated, and the controlled answers bind the "
            "sample only.",
            [S(BRIEF, 26, 33), S(EVAL, 8)]),
        "necessary_for": A(
            "scout and medic production (t_scout, t_medic) and family delivery (t_family); not the sample",
            "lifecycle.py 65-75 applies task_decision, method_poc and choice_unconfirmed only in production and "
            "delivery phases; t_scout and t_medic depend on t_sample.",
            [S(LIFE, 12, 14), S(LIFE, 65, 75), L("t_scout"), L("t_medic"), L("t_family")]),
        "question": A(
            "For the family: which outline treatment and final canvas do you choose; what device distinguishes the "
            "scout from the medic (and does the palette gain a reserved accent); is each member one sprite or an "
            "animation set; and which engine or importer is the destination?",
            "Each element is an unresolved or sample-scoped choice: i_outline and i_canvas are proposed under the "
            "sample-scoped answers; i_role_diff, i_animation and i_engine are unresolved.",
            [L("i_outline"), L("i_canvas"), L("i_role_diff"), L("i_animation"), L("i_engine"), S(EVAL, 5, 8)]),
        "unlocks": A(
            "Production contracts for f_scout and f_medic whose linked choices can be confirmed, the evidence-backed "
            "adoption decisions the production phases require, and the engine import check on f_family. Answers adopt "
            "only the choices they name and accept no artwork.",
            "lifecycle.py 53-56 needs a raster contract per production output; 65-75 needs a decision and confirmed "
            "linked choices; q_engine_import needs an engine. intake-sample.md 97-104: project only the supplied answer.",
            [S(LIFE, 53, 56), S(LIFE, 65, 75), S(INTAKE, 97, 104)]),
        "blocks_next_operation": A(
            False,
            "t_sample is in the sample phase, outside the adoption phases; its blockers are empty.",
            [S(LIFE, 12, 14), L("t_sample")]),
    },
]

next_action = {
    "operation": A(
        "pixl_job_prepare (CLI: python -B -I pixl-kit/scripts/pixl.py job-prepare state.px JOB t_sample REQUEST_JSON "
        "--outputs f_sample --expect <current canonical hash> --root <consumer root>)",
        "jobs.py 717-743 is the operation; handoff-review.md 40-42 prescribes -B -I for Python reads of the "
        "read-only kit; the b note's current operation section names the same command.",
        [S(JOBS, 717, 743), S(HREV, 40, 42), S(NB, 233, 238)]),
    "task": A("t_sample", "The only ready task; phase sample; output f_sample.", [L("t_sample")]),
    "output": A("f_sample", "t_sample.op names f_sample; f_sample.ct is c_sample.", [L("t_sample"), L("f_sample")]),
    "contract": A(
        "c_sample: 32 x 32, palette #56B5BC #F4DDA2 #25354A, side view, nearest sampling, binary alpha; sample-scoped",
        "Fields read from the c_sample record; the canvas and outline are sample-scoped controlled-evaluation answers.",
        [L("c_sample"), S(EVAL, 5, 8)]),
    "expect": A(
        "Reread state.px/state.px immediately before the call and pass its canonical hash; when this result was "
        "saved it was 762659d9df9a92dd54a6489289ca5824d4d6fd8507016f04db66fb37bb8d9ce2 (revision 16).",
        "jobs.py 731 loads with the expected hash; the head's measured sha256 equals the canonical hash.",
        [S(JOBS, 731), S(STATE, 1)]),
    "owner_answer_needed": A(
        False,
        "No linked choice of c_sample is unresolved or in conflict; the adoption-phase gates do not apply to the "
        "sample phase.",
        [S(LIFE, 57, 75), L("c_sample"), L("t_sample")]),
    "executable_locally_now": A(
        False,
        "platform.py 869-889 requires inputs no local file supplies; official PixelLab tools are not observed in "
        "this host.",
        [S(PLAT, 869, 889), S(READY, 101, 102)]),
    "state_side_gates": A(
        "Satisfied or not applicable: new job ID, outputs within t_sample, t_study done, f_sample has c_sample, "
        "no unresolved or conflicting linked choice, sample phase outside the adoption gates, no families or "
        "connected plans, no PLAR selection binding, t_sample open, no pending attempt.",
        "lifecycle.py 44-77 and jobs.py 145-161 (plan blockers, PLAR selection bindings, task state) and 320 "
        "(pending) were read by the caller; the head shows t_sample open with dp [t_study], ip [] and no J record. "
        "The worksheet covers the jobs.py 145-161 gates in substance but not by line (caller observation O1).",
        [S(LIFE, 44, 77), S(JOBS, 145, 161), S(JOBS, 732, 738), L("t_sample"), L("t_study"), S(V7, 96, 104)]),
    "blocked_on": [
        A("Provider identity, tool name, the full live inputSchema and discovery evidence with a host-clock "
          "timestamp, from the host's PixelLab connection (RQ1).",
          "platform.py 869-870, 873, 875-876, 888-889 and 1017-1023.",
          [S(PLAT, 869, 889), S(PLAT, 1017, 1023)]),
        A("Exact provider arguments with reference.png as an actual image input, inside the provider_arguments "
          "successor packet that supersedes sample-criteria.json with a v2 criteria file (q_sample_readability brief "
          "source lines [20, 20], optionally [5, 5]; five check texts unchanged; validated only with "
          "validate_criteria_v2.py; bound as a new S beside s_sample_criteria), reviewed with pixl_request_review "
          "and compared by the caller.",
          "platform.py 871-872 and 889; PROFILE.md 44; request_review.py 130-134; g note 23-31 and 61-74; brief.md "
          "line 20 is the side-view destination; delegation.md 69.",
          [S(PLAT, 871, 889), S(PROF, 44), S(RREV, 130, 134), S(NG, 23, 31), S(NG, 61, 74), S(BRIEF, 20),
           S(DELEG, 69)]),
        A("An authorization evidence object covering one paid call; the scope text exists in brief.md lines 6-7.",
          "platform.py 874, 877-885 require scope text and a nonempty evidence object.",
          [S(PLAT, 874, 885), S(BRIEF, 6, 7)]),
    ],
    "alternatives": [
        A("Route: the authenticated official PixelLab MCP tool surface, or the HTTP adapter explicitly selected for "
          "its documented operation; a caller/host selection, not an owner decision.",
          "SKILL.md 26 and PROFILE.md 32 name both routes.", [S(SKILL, 26), S(PROF, 32)]),
        A("First-candidate path: record-level job-prepare is the route here; PLAR preparation is unavailable because "
          "no plar.txt exists in this consumer.",
          "intake-sample.md 25 offers PLAR preparation for a selected PLAR asset; t_sample.ip is empty.",
          [S(INTAKE, 25), L("t_sample")]),
        A("Visual-review inputs: the owner's display scale and backgrounds, or the specialist's light, dark and busy "
          "test set as the authorized fallback for backgrounds only; needed before inspection, not before job-prepare.",
          "q_sample_readability's check text establishes the fallback and the scale requirement.",
          [L("q_sample_readability")]),
    ],
    "preparatory_steps": [
        A("Answer SQ1-SQ9 of sample-creative-brief-v2.json (lines 143-151) against the live declaration; "
          "operation-shortlist.json is a dated catalog and decides nothing.",
          "brief-v2 142-152; readiness.md 101-102.", [S(BRIEF2, 142, 152), S(SHORT, 1), S(READY, 101, 102)]),
        A("Write the v2 criteria file with the corrected brief locator, validate it only with validate_criteria_v2.py "
          "--out to a fresh work/ path, and bind it as a new S record.",
          "g note 61-74; b note prescription P4.", [S(NG, 61, 74), S(NB, 288, 290)]),
        A("Translate the v2 brief into exact provider arguments with reference.png carried as an actual image input "
          "bound to its sha256.",
          "PROFILE.md 44; platform.py 871-872 and 889.", [S(PROF, 44), S(PLAT, 871, 889)]),
        A("Save the successor request-review packet with request kind provider_arguments, run pixl_request_review, and "
          "have the caller compare request and criteria with the sources.",
          "request_review.py 130-134; delegation.md 69.", [S(RREV, 130, 134), S(DELEG, 69)]),
        A("Then call job-prepare with a fresh expect hash; preparation is not submission, payment or acceptance.",
          "jobs.py 717-743 saves a prepared request without remote action.", [S(JOBS, 717, 743)]),
    ],
    "after_prepare": A(
        "Caller comparison of the saved request, job-dispatch, one host call, job-observe, job-import as an "
        "unaccepted candidate, mechanical checks through the local harness, visual inspection (needs the display "
        "scale), then task completion only if all five sample criteria pass.",
        "d note 249-255 and the b note's later-production section state this sequence.",
        [S(ND, 249, 255), S(NB, 357, 373)]),
    "read_first": A(
        "SESSION.md, then deliverables/continuation-2026-11-16c.md, then deliverables/continuation-2026-11-16b.md "
        "(current except the sentences the c note corrects), then review/caller-comparison-2026-11-16-v7.md.",
        "The c note's current-instructions section names this order and the corrected b-note sentences.",
        [S(NC, 71, 96)]),
    "verifier": A(
        "python -B -I work/verify_rev16.py from the consumer root; expect problems [] and no __pycache__ under pixl-kit/.",
        "c note P5 (updated) and the b note's P2/P3; the caller ran it after the final handback with problems [].",
        [S(NC, 81, 85), S(NB, 280, 287)]),
    "shell_note": A(
        "From Git Bash, set MSYS_NO_PATHCONV=1 before check_handoff.py, or use PowerShell.",
        "c note F5 and P7; the caller reproduced the failure and the fix.", [S(NC, 66, 69), S(NC, 86, 89)]),
}


def build_result():
    child = "a94b4dc767b65b243"
    document = {
        "version": 1,
        "date": "2026-11-16",
        "assignment": (
            "Handoff-only continuation of the retained scout/medic character-family project under its original brief "
            "and established authorization, in a new consumer root: retain the prepared work, inspect the actual "
            "current state and relevant artifacts, save a useful current continuation through the registered pixl:pixl "
            "specialist by native delegation, review its returned handoff and state against the sources and the "
            "installed runtime, send discrepancies to the same native child, independently verify the final artifacts "
            "and state, and report what is preserved, what was accomplished, the next operation and remaining input. "
            "No request-packet or fixture production; no provider, engine or network; no new owner answers."),
        "assignment_status": "delivered",
        "status_meaning": (
            "The specialist saved a current continuation (b note, revision 15), and after five caller findings a "
            "corrections note (c note, revision 16), each with a saved structured return covered by the kit's literal "
            "handoff review. The caller verified both revisions, reproduced both coverage checks byte for byte, and "
            "adopted the c note plus the b note as the current continuation. Every earlier artifact is retained. "
            "t_sample is still open and unaccepted; nothing was generated, accepted or decided. The next operation, "
            "job-prepare for t_sample, is blocked on capability inputs and the provider_arguments successor packet, "
            "not on an owner answer."),
        "consumer_root": "C:/Users/ryanf/AppData/Local/Temp/pixl caller review 249faf48d4f549729dad6842462c74ce/consumer",
        "installed_kit": "pixl-kit",
        "interpreter": "C:/github/pixel-lab-agent/.venv/Scripts/python.exe (run with -B -I against the read-only kit)",
        "store": {"folder": "state.px", "head": "state.px/state.px"},
        "target_role": "pixl:pixl",
        "role_observation": {
            "status": "available",
            "basis": (
                "The host listed pixl:pixl as an Agent subagent type and the pixl:pixl skill as invocable. The Agent "
                "call with subagent_type pixl:pixl, run in the foreground, returned native child ID " + child + "; the "
                "child loaded the pixl skill and used the local pixl_* tools, the kit runner and check_handoff.py. "
                "SendMessage to the same ID resumed the same child three times. pixl_readiness (host claude, "
                "installation pixl-kit): manifest verified, 260 files checked, no issues; named_role not_observed "
                "from static files because the .claude adapters are absent, which is expected for plugin loading."),
            "limitations": [
                "Readiness cannot observe host role registration; the evidence is the host's agent-type listing, the "
                "returned child ID and the same-ID continuations.",
                "The previous session's child a2243e0a858503645 was not resumable here; this session's work is an "
                "artifact-based restart, described as such in the delegation.",
                "The correction round was interrupted twice by the host: once when the previous caller process ended, "
                "and once by an API rate-limit error (HTTP 429). Each time the landed files were inspected and the same "
                "child was resumed; nothing was redone or overwritten.",
                "No official PixelLab tool, provider, engine or network was visible or used.",
            ],
        },
        "native_child": {
            "agent_id": child,
            "subagent_type": "pixl:pixl",
            "rounds": [
                {"round": 1, "mechanism": "Agent, foreground", "result": "revision 15 (247b22ba... to 8284e076...); b note, b result, literal review -01 failed and retained, -02 coverage_complete; SESSION.md; status delivered"},
                {"round": 2, "mechanism": "SendMessage with caller findings F1-F5", "result": "revision 16 (8284e076... to 762659d9...), c note, c result and SESSION.md landed; the run stopped when the previous caller process ended, before the literal review"},
                {"round": "2, resume 1", "mechanism": "SendMessage after inspecting landed files", "result": "stopped by an API rate-limit error before writing the review files; no file changed"},
                {"round": "2, resume 2", "mechanism": "SendMessage", "result": "rev16 literal review written in one pass, coverage_complete 81/81, 9 carriers match; verify_rev16 problems []; status delivered"},
            ],
            "previous_session_children": [
                {"agent_id": "a2243e0a858503645", "note": "9f6e7c37 root, revision 14; not resumed; consumed through retained files"},
                {"agent_id": "aa5b126379050c057", "note": "a97de591 root, revisions 12-13; not resumed"},
            ],
        },
        "input_and_source_references_reviewed": [
            ref(BRIEF, "verbatim owner brief: lines 3-7; 19 roster; 20 side view; 23 canvas not chosen; 6-7 authorization scope; 11-15 predecessor provenance"),
            ref(EVAL, "sample-scoped controlled answers, lines 5-6, scope line 8; already applied; unchanged"),
            ref("sources/reference-observations.md", "measured reference study; unchanged"),
            ref("sources/method-research.md", "bundled method excerpts; unchanged"),
            ref("reference.png", "owner reference A (outlined); unchanged"),
            ref("reference-b.png", "owner reference B (no outline); unchanged"),
            ref("deliverables/continuation-2026-11-16.md", "current continuation on entry (s_continuation_9); unchanged"),
            ref(NG, "g note; finding 1 (line 20 locator, criteria-v2 step) still current; unchanged"),
            ref("deliverables/continuation-2026-11-15f.md", "f note; source evidence; unchanged"),
            ref(ND, "d note; sequence after prepare at 249-255; unchanged"),
            ref("deliverables/sample-request/request-review-v2.json", "current pre-discovery packet, kind creative_brief; unchanged"),
            ref(BRIEF2, "current creative brief; schema questions at 142-152; unchanged"),
            ref("deliverables/sample-request/sample-criteria.json", "bound criteria plan; line-19 locator to be superseded by v2; unchanged"),
            ref("deliverables/sample-request/criteria-schema-validation.json", "retained validation artifact; unchanged"),
            ref(SHORT, "dated operation catalog; decides nothing; unchanged"),
            ref("CALLER-RESULT-LITERAL-RECONCILIATION.json", "previous caller result (9f6e7c37 root); read for continuity; unchanged"),
            ref("review/caller-comparison-2026-11-16-v6.md", "previous caller comparison; unchanged"),
            ref("state.px/history/247b22ba715519ef2033fcea6de3dcabed45f288edcbcc5616b235e26e77e4af.px", "store head on entry, revision 14; retained in history"),
            ref("work/verify_rev14.py", "previous verifier; caller run on entry: problems [], kit change reported as an observation"),
            ref("pixl-kit/bundle-manifest.json", "kit manifest; changed from e1fb0065...; 259 files entries plus generated requirements.txt"),
            ref("pixl-kit/requirements.txt", "the manifest's only generated_files entry (finding F1)"),
            ref(DELEG, "244 lines, read in full; changed; caller review steps 71-135, completion 137-157"),
            ref(INTAKE, "190 lines, read in full; changed; worksheet 106-159, literal review item 147-153"),
            ref(HREV, "126 lines, read in full; new; literal handoff review"),
            ref("pixl-kit/scripts/check_handoff.py", "new helper; forces dont_write_bytecode at 9-11"),
            ref("pixl-kit/runtime/pixl/handoff_review.py", "new module; semantic_verdict not_assessed at 122 and 209"),
            ref(LIFE, "gates 12-14 and 44-77; unchanged"),
            ref(JOBS, "prepare 717-743, blockers 145-161, pending 320; unchanged"),
            ref(PLAT, "request fields 869-889 and 1017-1023; unchanged"),
            ref(RREV, "provider_arguments requirement 130-134; unchanged"),
            ref(SKILL, "route sentence line 26; unchanged"),
            ref(PROF, "lines 32 and 44; unchanged"),
            ref(READY, "lines 101-102; unchanged"),
            ref("pixl-kit/skills/pixl/references/state-authority.md", "line 13 expected-hash commit rule; unchanged"),
        ],
        "specialist_outputs": [
            ref(STATE, "published PX2 head, revision 16, 90 records; canonical hash equals file sha256"),
            ref("state.px/history/762659d9df9a92dd54a6489289ca5824d4d6fd8507016f04db66fb37bb8d9ce2.px", "revision 16 history copy"),
            ref("state.px/history/8284e076c7d3052e69b78e47061b46971fa7b5b81f03e2a41b58cc7a511e565c.px", "revision 15 history copy"),
            ref(NC, "c note (s_continuation_11, 123 lines): corrections F1-F5 old-to-new, current instructions, P5 and P7; READ FIRST"),
            ref(NB, "b note (s_continuation_10, 455 lines): full current continuation except the sentences the c note corrects"),
            ref("deliverables/specialist-return-2026-11-16c.json", "current saved specialist return (revision 16)"),
            ref("deliverables/specialist-return-2026-11-16b.json", "revision 15 return; retained as that round's record"),
            ref("SESSION.md", "mutable pointer after round 2: revision 16, read c then b, corrected kit accounting, -B -I, P7"),
            ref("work/build_rev15.py", "revision 15 builder"),
            ref("work/verify_rev15.py", "revision 15 verifier"),
            ref("work/rev15.json", "revision 15 document"),
            ref("work/rev15.px", "revision 15 wire, equal to its history copy"),
            ref("work/rev15-protected-snapshot.sha256", "revision 15 pre-write snapshot, 400 entries"),
            ref("work/build_rev16.py", "revision 16 builder"),
            ref("work/verify_rev16.py", "current verifier; caller run: problems []"),
            ref("work/rev16.json", "revision 16 document"),
            ref("work/rev16.px", "revision 16 wire, equal to the head"),
            ref("work/rev16-protected-snapshot.sha256", "revision 16 pre-write snapshot, 419 entries"),
            ref("work/handoff-review-rev15/build_review.py", "revision 15 review builder"),
            ref("work/handoff-review-rev15/handoff-inventory-01.json", "revision 15 inventory, 78 leaves"),
            ref("work/handoff-review-rev15/handoff-review-01.json", "revision 15 first review; retained"),
            ref("work/handoff-review-rev15/handoff-check-01.json", "revision 15 failed check (coverage_incomplete); retained"),
            ref("work/handoff-review-rev15/handoff-review-02.json", "revision 15 corrected review"),
            ref("work/handoff-review-rev15/handoff-check-02.json", "revision 15 check, coverage_complete"),
            ref("work/handoff-review-rev16/build_review.py", "revision 16 review builder"),
            ref("work/handoff-review-rev16/handoff-inventory-01.json", "revision 16 inventory, 81 leaves"),
            ref("work/handoff-review-rev16/handoff-review-01.json", "revision 16 review, 78 source rows and 3 metadata rows"),
            ref("work/handoff-review-rev16/handoff-check-01.json", "revision 16 check, coverage_complete, semantic not_assessed"),
        ],
        "specialist_claims_summary": {
            "records_added": ["revision 15: s_continuation_10, handoff_11", "revision 16: s_continuation_11, handoff_12"],
            "records_changed": "headers only; every earlier record byte-identical",
            "specialist_status": "delivered (judged against the handoff-only scope; t_sample open and unaccepted)",
            "specialist_choices_preserved": [
                "the worksheet R1-R15 / A1-A3 as the claim set, with the decision table kept as a layout",
                "corrections carried in a short successor note instead of rewriting the bound b note",
                "kit identity checked through the manifest in the verifiers, with any bytecode cache reported as an observation",
            ],
        },
        "caller_review": {
            "distinct_from_specialist_review": True,
            "files": [
                ref(V7, "caller claim-by-claim comparison for revisions 15 and 16, findings, observation O1 and adoption finding (new; v1-v6 retained)"),
                ref("work/caller-reconciliation-02/entry-snapshot.sha256", "caller sha256 snapshot of 135 non-kit files on entry"),
                ref("work/caller-reconciliation-02/specialist-inventory-caller.json", "caller re-run of the rev15 inventory; byte-identical to the specialist's"),
                ref("work/caller-reconciliation-02/specialist-check-caller.json", "caller re-run of the rev15 check; byte-identical to handoff-check-02.json"),
                ref("work/caller-reconciliation-02/rev16-inventory-caller.json", "caller re-run of the rev16 inventory; byte-identical"),
                ref("work/caller-reconciliation-02/rev16-check-caller.json", "caller re-run of the rev16 check; byte-identical"),
                ref("work/caller-reconciliation-02/build_caller_result.py", "builder of this result and its review"),
            ],
            "findings": [
                {"id": "F1", "kind": "discrepancy_corrected", "claim": "b note 78-80 attributed the 261st kit file to resources/pixl/handoff_review.py", "evidence": "bundle-manifest.json files (259 entries) include that path; the unlisted files are bundle-manifest.json and requirements.txt (generated_files, 9cc16454...)", "disposition": "corrected in c note 26-35 and SESSION.md; verified"},
                {"id": "F2", "kind": "discrepancy_corrected", "claim": "b result /handoff_review/paths named the failed -01 check", "evidence": "handoff-check-01.json in rev15 is coverage_incomplete; -02 is the complete binding", "disposition": "c result pre-named fresh rev16 files, produced in one pass; b result retained; verified"},
                {"id": "F3", "kind": "discrepancy_corrected", "claim": "b note 265 listed /status as a carrier but the rev15 review did not cover it", "evidence": "handoff-review.md 20-24, 37-38", "disposition": "rev16 review includes /status; verified 81/81"},
                {"id": "F4", "kind": "discrepancy_corrected", "claim": "locators: handoff_review.py 129, brief-v2 SQ1-SQ4 at 142-171", "evidence": "not_assessed at 122 and 209; schema questions 142-152, SQ1-SQ4 143-146", "disposition": "corrected in c note 56-64 and the c result; verified"},
                {"id": "F5", "kind": "environment_observation", "claim": "check_handoff.py failed from Git Bash with leading-slash scopes", "evidence": "reproduced; succeeds with MSYS_NO_PATHCONV=1", "disposition": "new prescription P7; verified"},
                {"id": "O1", "kind": "observation_not_sent", "claim": "the worksheet cites lifecycle.py for state gates but not jobs.py 145-161 (plan blockers, PLAR selection bindings, task state)", "evidence": "jobs.py 145-161 read by the caller; each gate satisfied now and covered in substance by R7, A2 and the trace", "disposition": "recorded here and in v7 lines 96-104; no revision requested for a locator-only gap"},
            ],
            "integrity_checks": [
                "pixl_validate: revision 16, 90 records, valid, files verified, hash 762659d9...; all 88 revision 15 record hashes identical",
                "sorted wire diffs: 14 to 15 adds s_continuation_10 and handoff_11; 15 to 16 adds s_continuation_11 and handoff_12; headers only otherwise",
                "handoff_11.fo and handoff_12.fo each equal the new S record followed by the previous handoff's full list",
                "notes: b note 455 lines and c note 123 lines equal their bound ranges; neither contains its own revision hash",
                "entry snapshot: only SESSION.md and the head changed; every other pre-existing file unchanged; all new files accounted for",
                "verify_rev15.py and verify_rev16.py run by the caller with -B -I: problems []",
                "check_handoff.py inventory and check re-run by the caller for both revisions: byte-identical outputs",
                "kit: 261 files, manifest 31b64de8... verified, no __pycache__ at any point",
                "pixl_ready [t_sample]; pixl_jobs []; no intake status moved; no candidate, verdict, evidence, decision or job created",
                "validate_criteria.py not run by anyone; criteria-schema-validation.json unchanged",
            ],
        },
        "correction_messages": [
            {"to": child, "mechanism": "SendMessage", "kind": "correction request with source evidence",
             "subject": "F1-F5 with measured evidence; requested a successor corrections note, a corrected return, a fresh literal review with /status, revision 16 and SESSION.md; listed every claim verified consistent",
             "child_reply": "none before the previous caller process ended; landed files were revision 16, c note, c result and SESSION.md"},
            {"to": child, "mechanism": "SendMessage", "kind": "resume after interruption",
             "subject": "named the landed files and the empty review folder; asked to finish without rewriting",
             "child_reply": "stopped by an API rate-limit error after confirming the landed files matched"},
            {"to": child, "mechanism": "SendMessage", "kind": "resume after rate-limit stop",
             "subject": "asked only for the rev16 review builder, inventory, review and check, plus a compact handback",
             "child_reply": "review files written in one pass; coverage_complete 81/81; 9 carriers match; semantic not_assessed; verify_rev16 problems []; no existing file changed"},
        ],
        "final_state": {
            "head": ref(STATE, "published PX2 head, revision 16"),
            "revision": 16,
            "records": 90,
            "canonical_state_hash": HEAD,
            "entry_state_hash": "247b22ba715519ef2033fcea6de3dcabed45f288edcbcc5616b235e26e77e4af",
            "history_copies": 17,
            "contract": {"id": "c_sample", "record_hash": "b7f77964257f1bfdbf54ef0dcadc76117e0a3437f40daae1268210ae07147737", "px": [32, 32], "pl": ["#56B5BC", "#F4DDA2", "#25354A"], "vw": "side", "sa": "nearest", "al": "binary", "scope": "sample only", "unchanged_since": "revision 9"},
            "f_sample_requirements": ["q_sample_canvas", "q_sample_palette", "q_sample_outline", "q_sample_readability", "q_style_match"],
            "handoff_record": "handoff_12 (rv 16; nx [t_sample]; bl [t_scout, t_medic, t_family])",
            "intake_unchanged": True,
            "tasks": {"t_study": "done", "t_aid": "done", "t_sample": "open, ready, no candidate", "t_scout": "open, blocked", "t_medic": "open, blocked", "t_family": "open, blocked"},
            "ready": ["t_sample"],
            "jobs": [],
            "families": [],
            "kit_identity": {"bundle_manifest_sha256": sha("pixl-kit/bundle-manifest.json"), "manifest_verified": True, "files_checked": 260, "kit_files": 261, "bytecode_cache": "none"},
        },
        "remaining_questions": plain(remaining_questions),
        "next_action": plain(next_action),
        "notes": [
            "The specialist's review is in the b and c notes, its two saved returns and its literal-review files; the caller's review is review/caller-comparison-2026-11-16-v7.md and this file.",
            "Earlier versions are retained unchanged: every CALLER-RESULT*.json, caller comparisons v1-v6, all continuation notes, all history copies and the revision 15 return and review files.",
            "The controlled-evaluation answers remain applied within their sample scope; no owner answers were supplied or invented.",
            "This file is excluded from its own file references. Its literal review and coverage check are reported in the caller's final response.",
        ],
    }
    with open(RESULT, "x", encoding="utf-8", newline="\n") as out:
        json.dump(document, out, indent=1, ensure_ascii=False)
        out.write("\n")
    print(json.dumps({"result": RESULT, "sha256": sha(RESULT)}))


def excerpt(path, first, last):
    lines = open(path, "rb").read().decode("utf-8-sig").splitlines(keepends=True)
    return {"path": path, "sha256": sha(path), "lines": [first, last], "text": "".join(lines[first - 1:last])}


def build_review():
    claims = list(rows(remaining_questions, "/remaining_questions")) + list(rows(next_action, "/next_action"))
    carriers = [excerpt(NB, 233, 267), excerpt(NB, 269, 302), excerpt(NB, 357, 373),
                excerpt(NC, 24, 69), excerpt(NC, 71, 96), excerpt(V7, 96, 104), excerpt(V7, 126, 139)]
    review = {"version": 1, "result": {"path": RESULT, "sha256": sha(RESULT)},
              "scopes": ["/remaining_questions", "/next_action"], "claims": claims, "carriers": carriers}
    with open(REVIEW, "x", encoding="utf-8", newline="\n") as out:
        json.dump(review, out, indent=1, ensure_ascii=False)
        out.write("\n")
    print(json.dumps({"review": REVIEW, "rows": len(claims), "carriers": len(carriers), "sha256": sha(REVIEW)}))


if __name__ == "__main__":
    {"result": build_result, "review": build_review}[sys.argv[1]]()
