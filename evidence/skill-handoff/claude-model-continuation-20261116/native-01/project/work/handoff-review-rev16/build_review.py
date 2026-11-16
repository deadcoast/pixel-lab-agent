"""Build the version-1 literal handoff review for deliverables/specialist-return-2026-11-16c.json.

Worklist: the inventory written by check_handoff.py (every leaf of /status, /questions, /next,
/limitations). One row per leaf: basis source_comparison with actual source hashes and inclusive
line ranges (read in this session), or basis metadata for identifiers only. Carriers are exact
current-instruction excerpts of the b note (current sections) and the c note (corrections and
current-instructions sections). State-file line numbers are located by record id in the revision 16
head, not hard-coded. Every expected value is compared with the inventory value; a mismatch or a
leaf without an authored row stops the build.

Run from the consumer root: python -B -I work/handoff-review-rev16/build_review.py
Writes exactly one new file: work/handoff-review-rev16/handoff-review-01.json (refuses to overwrite).
"""
import hashlib, json, sys

RESULT = "deliverables/specialist-return-2026-11-16c.json"
INVENTORY = "work/handoff-review-rev16/handoff-inventory-01.json"
OUT = "work/handoff-review-rev16/handoff-review-01.json"
BNOTE = "deliverables/continuation-2026-11-16b.md"
CNOTE = "deliverables/continuation-2026-11-16c.md"
SCOPES = ["/status", "/questions", "/next", "/limitations"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def src(path, lines):
    return {"path": path, "sha256": sha(path), "lines": list(lines)}


MEASURED = {
    "pixl-kit/runtime/pixl/lifecycle.py": "5e37cefb2bcb357373332af4970b7c30df4e18df6d78e36022fe349a616a6a23",
    "pixl-kit/runtime/pixl/jobs.py": "18d543f7d81134b46c5282728be7e7681c94789c554a9f6e3abe0f882c92ecc3",
    "pixl-kit/runtime/pixl/platform.py": "7693533dea30d9027cd7f89b47629227b87b18f23e993ae6eab848cb78efbea0",
    "pixl-kit/runtime/pixl/request_review.py": "af7bf5bf1f599a03645d12e6faadb14db050dec5a31eae067ed3fc36295a1c23",
    "pixl-kit/skills/pixl/SKILL.md": "04a46dae9b55e5e54eec5b1a033e6e597f3e44170d930e96da3554289b34a5a2",
    "pixl-kit/resources/agent/PROFILE.md": "8aeaedb1f345af7f80d289f3f8372de00e20619ccf4ec685ed6db229c4d99265",
    "pixl-kit/skills/pixl/references/intake-sample.md": "9fd421030d44e104ff36446409d4562a976daec1650f7a956a950ae8043846ef",
    "pixl-kit/skills/pixl/references/delegation.md": "72bd2cdfd03333ae0cc3bcd325c4a231f0730ca2f42fbece1955b18b5648199b",
    "pixl-kit/skills/pixl/references/handoff-review.md": "42f73d779736ce90738542f7d5fb52d78d0f6c65c6ea81ddf151f181f794204f",
    "pixl-kit/skills/pixl/references/readiness.md": "fd9156896d7789046d45a09dc5e94330f59a1949ad44953843ac128a1a823d4f",
    "pixl-kit/skills/pixl/references/state-authority.md": "4f883c6832d63a5e8ff134f69dbbf6d90abdc96c3004b39cae7aec6a87715112",
    "pixl-kit/scripts/check_handoff.py": "ac1afd38549c6e951ab02afdfcc1695f3dcd309b3e357bca524a679271c02acc",
    "sources/brief.md": "a78aca77135c5e533b8000272558b5b65e40ee421d1913cab961d7adc4cf5324",
    "sources/controlled-evaluation-answers.md": "87cf7eec2d97fdd994d338054b578c330b0c69253fdfe4b540bd45d3952f6e30",
    "deliverables/continuation-2026-11-15g.md": "001065a3422bfb76997b375f9f66d22324e87a2841eb06d742e166d44fef2e4f",
    "deliverables/continuation-2026-11-15d.md": "826460e5ff96f7dae2bccff8b8df1278e5457614cfaadd3c0510e0f64feeb1dc",
    "deliverables/continuation-2026-11-16.md": "157d131cd3979d2b4e7e1729e4accbd2f8446f3573beed6e0fea543eb68fd420",
    "deliverables/sample-request/sample-creative-brief-v2.json": "f84b262818bbf044eb22716ab5d02eed1103cc65714360fcfc5d9efd019a5b80",
    "deliverables/sample-request/operation-shortlist.json": "7294d9d779982ee6602412eaed925ca2dab6e0b0c787f314455de6f53ed00186",
    "state.px/state.px": "762659d9df9a92dd54a6489289ca5824d4d6fd8507016f04db66fb37bb8d9ce2",
    "CALLER-RESULT-LITERAL-RECONCILIATION.json": "7b033ec23f1307ab3083e8061fb5456a61fc389085b8b00ac36158d0f03229e3",
    BNOTE: "6454d5b65397a7d1b647088055dccfb39e5b58173c34218df436584dae8c62f1",
    CNOTE: "0758e2aa19caf60fa0c86af9201adb0d5f4774f34239bcc04bc3df5c13dbfa16",
}
for p, h in MEASURED.items():
    assert sha(p) == h, f"source drifted since the session read it: {p}"

LIFE, JOBS, PLAT, RR = ("pixl-kit/runtime/pixl/lifecycle.py", "pixl-kit/runtime/pixl/jobs.py",
                        "pixl-kit/runtime/pixl/platform.py", "pixl-kit/runtime/pixl/request_review.py")
SKILL, PROFILE = "pixl-kit/skills/pixl/SKILL.md", "pixl-kit/resources/agent/PROFILE.md"
INTAKE, DELEG = "pixl-kit/skills/pixl/references/intake-sample.md", "pixl-kit/skills/pixl/references/delegation.md"
HR, READY, SA = ("pixl-kit/skills/pixl/references/handoff-review.md", "pixl-kit/skills/pixl/references/readiness.md",
                 "pixl-kit/skills/pixl/references/state-authority.md")
CHK = "pixl-kit/scripts/check_handoff.py"
BRIEF, EVAL = "sources/brief.md", "sources/controlled-evaluation-answers.md"
G, D, N16 = ("deliverables/continuation-2026-11-15g.md", "deliverables/continuation-2026-11-15d.md",
             "deliverables/continuation-2026-11-16.md")
BV2, SHORT = "deliverables/sample-request/sample-creative-brief-v2.json", "deliverables/sample-request/operation-shortlist.json"
STATE, CRL = "state.px/state.px", "CALLER-RESULT-LITERAL-RECONCILIATION.json"

_wire = open(STATE, encoding="utf-8").read().splitlines()


def L(record_id):
    """1-based line of a record in the revision 16 head, located by its id prefix."""
    hits = [i + 1 for i, ln in enumerate(_wire) if ln.startswith("@" + record_id + ":")]
    assert len(hits) == 1, (record_id, hits)
    return src(STATE, (hits[0], hits[0]))


S = {
    "gates_code": [src(LIFE, (44, 77)), src(JOBS, (717, 743))],
    "plan": [L("t_sample"), L("f_sample"), L("c_sample")],
    "readability": [L("q_sample_readability"), L("i_display_scale"), L("i_backgrounds")],
    "platform": [src(PLAT, (869, 889)), src(PLAT, (1017, 1023))],
    "rr": [src(RR, (130, 134))],
    "route": [src(SKILL, (26, 26)), src(PROFILE, (32, 32))],
    "plar": [src(INTAKE, (25, 25)), src(SKILL, (24, 24))],
    "brief_scope": [src(BRIEF, (3, 7))],
    "eval": [src(EVAL, (3, 8))],
    "g1": [src(G, (23, 31)), src(G, (61, 74))],
    "dseq": [src(D, (249, 255))],
    "hr_all": [src(HR, (20, 24)), src(HR, (26, 46)), src(HR, (80, 93)), src(HR, (101, 126)), src(INTAKE, (147, 153))],
    "hr_flags": [src(HR, (40, 46)), src(CHK, (9, 11))],
    "n16_cache": [src(N16, (58, 66)), src(CRL, (200, 200)), src(CRL, (208, 208))],
    "n16_verify": [src(N16, (215, 239))],
    "cold": [src(INTAKE, (161, 190)), src(DELEG, (137, 157))],
    "sq": [src(BV2, (142, 152))],
    "shortlist": [src(SHORT, (1, 8)), src(READY, (99, 102))],
    "profile44": [src(PROFILE, (44, 44))],
    "stateauth": [src(SA, (13, 13)), src(JOBS, (731, 731))],
    "deleg69": [src(DELEG, (69, 69))],
    "adoption": [src(LIFE, (65, 75))],
    "planning_only": [src(DELEG, (145, 145)), src(DELEG, (153, 155))],
    "no_prod_state": [src(DELEG, (153, 155)), L("s_continuation_11"), L("handoff_12"), L("s_continuation_10"), L("handoff_11")],
    "eval_scope": [src(EVAL, (8, 8)), L("i_outline"), L("i_canvas")],
    "readiness": [src(READY, (99, 102))],
    "c_corr": [src(CNOTE, (24, 69))],
    "c_current": [src(CNOTE, (71, 96))],
}

result = json.load(open(RESULT, encoding="utf-8"))
inventory = json.load(open(INVENTORY, encoding="utf-8"))
assert inventory["result"]["path"] == RESULT and inventory["result"]["sha256"] == sha(RESULT), "inventory binds another result"
assert inventory["scopes"] == SCOPES, inventory["scopes"]


def resolve(ptr):
    v = result
    for tok in ptr.split("/")[1:]:
        tok = tok.replace("~1", "/").replace("~0", "~")
        v = v[int(tok)] if isinstance(v, list) else v[tok]
    return v


def row(ptr, finding, sources, basis="source_comparison"):
    return {"pointer": ptr, "expected": resolve(ptr), "basis": basis, "finding": finding, "sources": sources}


STATUS = ("'delivered' judged against the handoff-only scope including the correction round: delegation.md 145 defines the status values against the assignment; 153-155 say a planning-only assignment is delivered when its reviewed result is returned, needs no manufactured production state, and both facts (delivered; task still open) are stated. t_sample remains open with ca [] in the head; the only added records are the S/N pairs of revisions 15 and 16.",
          S["planning_only"] + [L("t_sample")] + S["no_prod_state"])

Q = {
    "0": {
        "addressed_to": ("Provider identity, tool name, live schema, arguments, discovery and authorization are request fields enforced by platform.py 869-889 / 1017-1023; none is an owner art decision (brief.md 3-7 names no provider). Route choice between MCP surface and HTTP adapter is the caller's/host's (SKILL.md 26, PROFILE.md 32).", S["platform"] + S["route"] + S["brief_scope"]),
        "required_before": ("jobs.py 717-743 prepare() requires provider, tool, arguments, schema, discovery, authorization before saving the request; the plan trace t_sample -> f_sample -> c_sample is the saved one.", S["gates_code"] + S["plan"]),
        "question": ("Asks exactly for the fields platform.py validates (identity 869-870, arguments 871-872, discovery 873/875-876, authorization 874/877, nonempty evidence 878-885, no secrets, schema 889, observed_at not in the future 1019-1023), the image transport required because a filename in a prompt is not an uploaded reference (PROFILE.md 44), and the route alternative (SKILL.md 26, PROFILE.md 32). The scope text exists at brief.md 6-7.", S["platform"] + S["profile44"] + S["route"] + S["brief_scope"]),
        "unlocks": ("Corrected locator (c note F4b): the schema_questions_for_the_live_declaration array spans brief-v2 142-152, SQ1-SQ4 at 143-146, SQ5-SQ9 at 147-151. request_review.py 130-134 accepts only kind provider_arguments; delegation.md 69 requires the caller comparison; the criteria-v2 supersession is the g note's required step (61-74). Nothing here claims generation or acceptance.", S["sq"] + S["rr"] + S["deleg69"] + S["g1"] + S["c_corr"]),
        "blocks_job_prepare": ("True: jobs.py 739-741 passes these inputs to platform.prepare_discovered, which fails without them (platform.py 869-889); pixl_readiness reports them not observed.", S["gates_code"] + S["platform"]),
        "owner_answer": ("False: no source makes provider discovery or authorization evidence an owner art decision; brief.md 3-7 names the family, destination, references and scope only.", S["brief_scope"] + S["platform"]),
        "worksheet_rows": ("Cross-reference to the b note worksheet rows R10-R15 and A1, which cite the same platform.py / SKILL.md / PROFILE.md lines.", [src(BNOTE, (233, 267))]),
    },
    "1": {
        "addressed_to": ("i_display_scale and i_backgrounds are owner choices (wh user) saved unresolved in the head; the caller relays owner questions.", S["readability"]),
        "required_before": ("q_sample_readability.ck: the target integer zoom requires i_display_scale before review; the test backgrounds stand until i_backgrounds is answered. Review follows import, which follows the one host call (d note 249-255); neither choice is in c_sample.ch, so lifecycle.py 57-64 does not gate job-prepare on them.", S["readability"] + S["dseq"] + [src(LIFE, (57, 64)), L("c_sample")]),
        "question": ("Matches the two unresolved I records (display_scale; target_backgrounds); backgrounds optional because the criterion text supplies the fallback.", S["readability"]),
        "unlocks": ("The criterion text names both effects and the backgrounds fallback; no default zoom appears in any source.", S["readability"]),
        "blocks_job_prepare": ("False: neither choice is in c_sample.ch; pixl_workflow lists no blocker for t_sample.", [src(LIFE, (57, 64)), L("c_sample"), L("t_sample")]),
        "owner_answer": ("True: both records carry wh user and are unresolved; their rationales name the owner's game as the only source.", S["readability"]),
        "worksheet_rows": ("Cross-reference to worksheet row A3 in the b note.", [src(BNOTE, (233, 267))]),
    },
    "2": {
        "addressed_to": ("Outline, canvas, role differentiation, animation and engine are owner choices (wh user) whose statuses are proposed/unresolved; the controlled answers bind the sample only (eval line 8).", S["eval_scope"] + S["readability"]),
        "required_before": ("lifecycle.py 65-75 applies task_decision, method_poc, choice_unconfirmed only in production/delivery phases; those gates show on t_scout, t_medic, t_family and not on t_sample.", S["adoption"] + [L("t_sample")]),
        "question": ("Each named item is an I record: i_outline proposed (sample-scoped), i_canvas proposed (owner has not chosen, brief.md 23), i_palette observed coupled to i_role_diff, i_animation and i_engine unresolved; eval line 8 keeps them owner questions.", S["eval_scope"] + [src(BRIEF, (23, 23)), src(BRIEF, (26, 33))]),
        "unlocks": ("Production-phase gates per lifecycle.py 65-75 and output_contract 53-56; an answer adopts only what it names (intake-sample.md 97-104) and accepts no artwork (intake-sample.md 49-55).", S["adoption"] + [src(LIFE, (53, 56)), src(INTAKE, (97, 104)), src(INTAKE, (49, 55))]),
        "blocks_job_prepare": ("False: production-phase gates do not apply to t_sample (phase sample, lifecycle.py 65).", S["adoption"] + [L("t_sample")]),
        "owner_answer": ("True: all named choices are wh user and the brief's 'does not state' list (brief.md 26-33) leaves them to the owner.", [src(BRIEF, (26, 33)), L("i_outline"), L("i_canvas")]),
        "worksheet_rows": ("Cross-reference to worksheet row R6 and the decision-table rows in the b note.", [src(BNOTE, (233, 267)), src(BNOTE, (317, 341))]),
    },
}

NEXT = {
    "/next/operation": ("job-prepare takes the saved task/outputs/request (jobs.py 717-743); -B -I from handoff-review.md 40-42; task/output/contract are the saved plan.", S["gates_code"] + S["hr_flags"] + S["plan"]),
    "/next/task": ("t_sample is the only ready task (phase sample, open, dp [t_study], op [f_sample]).", [L("t_sample")]),
    "/next/phase": ("t_sample.ph = sample; outside ADOPTION_PHASES (lifecycle.py 65).", [L("t_sample"), src(LIFE, (65, 65))]),
    "/next/output": ("f_sample is t_sample's only planned output and carries ct c_sample.", [L("f_sample"), L("t_sample")]),
    "/next/contract": ("c_sample fields read from the head: al binary, ch 8 choices, pl three colours, px [32,32], sa nearest, vw side.", [L("c_sample")]),
    "/next/owner_answer_needed": ("False: lifecycle.py 57-64 over c_sample.ch finds none unresolved; production gates not applicable; the controlled answers supply the sample's outline and canvas within their scope.", [src(LIFE, (57, 75)), L("c_sample")] + S["eval"]),
    "/next/executable_locally_now": ("False: platform.py 869-889 requires inputs no local file supplies; official tools not observed.", S["platform"] + S["readiness"]),
    "/next/expect_rule": ("jobs.py 731 loads with the expected hash; state-authority.md 13; the revision 16 hash is current.", S["stateauth"] + [src(STATE, (1, 1))]),
    "/next/job_id_rule": ("jobs.py 732-734: job_exists refuses an existing ID.", [src(JOBS, (732, 734))]),
    "/next/state_side_gates/R1_job_exists": ("jobs.py 732-734; no J record in the 90 records (pixl_jobs []).", [src(JOBS, (732, 734))]),
    "/next/state_side_gates/R2_outputs_within_T_op": ("jobs.py 735 _context; t_sample.op [f_sample].", [src(JOBS, (735, 735)), L("t_sample")]),
    "/next/state_side_gates/R3_task_prerequisite": ("lifecycle.py 49-52; t_sample.dp [t_study]; t_study done.", [src(LIFE, (49, 52)), L("t_sample")]),
    "/next/state_side_gates/R4_output_contract": ("lifecycle.py 53-56; f_sample kd sprite with ct c_sample.", [src(LIFE, (53, 56)), L("f_sample")]),
    "/next/state_side_gates/R5_choice_unresolved_or_conflict": ("lifecycle.py 57-64; c_sample.ch statuses from the head: 4 proposed, 3 observed, 1 confirmed.", [src(LIFE, (57, 64)), L("c_sample"), L("i_canvas"), L("i_outline"), L("i_view")]),
    "/next/state_side_gates/R6_adoption_phase_gates": ("lifecycle.py 65-75 apply only in ADOPTION_PHASES; t_sample.ph sample.", S["adoption"] + [L("t_sample")]),
    "/next/state_side_gates/R7_family_and_plan_blockers": ("lifecycle.py 76 families.blockers; no families or plans.", [src(LIFE, (76, 76))]),
    "/next/state_side_gates/R8_job_pending": ("jobs.py 738 _pending; pixl_jobs [].", [src(JOBS, (738, 738))]),
    "/next/state_side_gates/R9_expect": ("jobs.py 731; state-authority.md 13; reread before the call.", S["stateauth"]),
    "/next/blocked_on/0": ("platform.py 869 provider identity; official tools not_observed.", [src(PLAT, (869, 869))] + S["readiness"]),
    "/next/blocked_on/1": ("platform.py 870 tool identity; readiness.md 101-102 dated catalog is not live visibility; the shortlist says it is from dated documentation.", [src(PLAT, (870, 870))] + S["shortlist"]),
    "/next/blocked_on/2": ("platform.py 888-889 need the live schema object.", [src(PLAT, (888, 889))]),
    "/next/blocked_on/3": ("platform.py 871-872, 887, 889; PROFILE.md 44; request_review.py 130-134; g note 61-74; delegation.md 69.", [src(PLAT, (871, 872)), src(PLAT, (887, 889))] + S["profile44"] + S["rr"] + S["g1"] + S["deleg69"]),
    "/next/blocked_on/4": ("platform.py 873, 875-876, 878-885, 1019-1023.", S["platform"]),
    "/next/blocked_on/5": ("platform.py 874, 877, 878-885; scope text at brief.md 6-7.", S["platform"] + [src(BRIEF, (6, 7))]),
    "/next/not_blocked_on": ("lifecycle.py 57-64 gates only linked choices; q_sample_readability.ck places the two choices before review; d note places review after import.", [src(LIFE, (57, 64)), L("c_sample")] + S["readability"] + S["dseq"]),
    "/next/alternatives/A1_route": ("SKILL.md 26 and PROFILE.md 32; neither route observed.", S["route"] + S["readiness"]),
    "/next/alternatives/A2_first_candidate_path": ("intake-sample.md 25 and SKILL.md 24 tie PLAR preparation to a selected plar.txt asset; none exists here.", S["plar"]),
    "/next/alternatives/A3_visual_review_inputs": ("q_sample_readability.ck names the fallback test set and the zoom requirement before review.", S["readability"] + S["dseq"]),
    "/next/preparatory_steps_once_Q1_is_supplied/0": ("Corrected locator (c note F4b): SQ1-SQ4 at brief-v2 143-146 in the array 142-152, SQ5-SQ9 at 147-151; the shortlist is a dated catalog.", S["sq"] + S["shortlist"] + S["c_corr"]),
    "/next/preparatory_steps_once_Q1_is_supplied/1": ("g note finding 1 (23-31, 61-74).", S["g1"]),
    "/next/preparatory_steps_once_Q1_is_supplied/2": ("platform.py 871-872, 887, 889; PROFILE.md 44.", [src(PLAT, (871, 872)), src(PLAT, (887, 889))] + S["profile44"]),
    "/next/preparatory_steps_once_Q1_is_supplied/3": ("request_review.py 130-134; delegation.md 69.", S["rr"] + S["deleg69"]),
    "/next/preparatory_steps_once_Q1_is_supplied/4": ("jobs.py 717-743; PROFILE.md 44 preparation is not submission or acceptance.", S["gates_code"] + S["profile44"]),
    "/next/sequence_after_prepare/0": ("d note 249-255.", S["dseq"]),
    "/next/sequence_after_prepare/1": ("d note 249-255; PROFILE.md 45.", S["dseq"] + [src(PROFILE, (45, 45))]),
    "/next/sequence_after_prepare/2": ("PROFILE.md 45.", [src(PROFILE, (45, 45))]),
    "/next/sequence_after_prepare/3": ("d note 249-255; PROFILE.md 46.", S["dseq"] + [src(PROFILE, (46, 46))]),
    "/next/sequence_after_prepare/4": ("d note 249-255; PROFILE.md 47.", S["dseq"] + [src(PROFILE, (47, 47))]),
    "/next/sequence_after_prepare/5": ("d note 249-255; intake-sample.md 62; q_sample_readability.", S["dseq"] + [src(INTAKE, (62, 62))] + S["readability"]),
    "/next/procedural_prescriptions/P1_literal_handoff_review": ("intake-sample.md 147-153; handoff-review.md 20-24, 26-46, 80-93, 101-126.", S["hr_all"]),
    "/next/procedural_prescriptions/P2_interpreter_flags": ("handoff-review.md 40-42; check_handoff.py 9-11.", S["hr_flags"]),
    "/next/procedural_prescriptions/P3_no_bytecode_cache": ("2026-11-16 note 58-66 and caller result 200/208 describe the previous root's cache; handoff-review.md 40-42 give the reason; verify_rev16 reports none here.", S["n16_cache"] + [src(HR, (40, 42))]),
    "/next/procedural_prescriptions/P4_criteria_validation": ("g note 61-74; 2026-11-16 note 270-271.", [src(G, (61, 74)), src(N16, (270, 271))]),
    "/next/procedural_prescriptions/P5_current_verifier": ("c note 'Current instructions after this note' updates P5 to verify_rev16.py; 2026-11-16 note 215-239 explains the older verifiers.", S["c_current"] + S["n16_verify"]),
    "/next/procedural_prescriptions/P6_cold_start": ("intake-sample.md 161-190 and 64; c note current-instructions section (read c then b); g note finding 1.", S["cold"] + [src(INTAKE, (64, 64))] + S["c_current"] + S["g1"]),
    "/next/procedural_prescriptions/P7_shell_path_conversion": ("c note F5 (corrections section) and P7 (current-instructions section); handoff-review.md 30-34 show the leading-slash scope syntax the shell rewrites.", S["c_corr"] + S["c_current"] + [src(HR, (28, 34))]),
    "/next/final_wording": ("Same conclusion as R1-R15/A1-A3: gates satisfied, inputs missing, successor packet required, display scale before review only.", S["gates_code"] + S["platform"] + S["rr"] + S["deleg69"] + S["g1"] + S["readability"]),
}

LIM = {
    "/limitations/0": ("Official tools not observed; pixl_jobs []; t_sample open with ca []; delegation.md 153-155.", S["readiness"] + S["planning_only"] + [L("t_sample")]),
    "/limitations/1": ("2026-11-16 note 85-87: previous bytes not retained.", [src(N16, (85, 87))]),
    "/limitations/2": ("g note finding 1; brief.md 5 and 19-20.", S["g1"] + [src(BRIEF, (5, 5)), src(BRIEF, (19, 20))]),
    "/limitations/3": ("g note finding 2 table (87-94).", [src(G, (87, 94))]),
    "/limitations/4": ("handoff-review.md 107-113; delegation.md 86-97.", [src(HR, (107, 113)), src(DELEG, (86, 97))]),
    "/limitations/5": ("handoff-review.md 26-46 (assigned interpreter, -B -I); bare python lacked jsonschema (measured).", [src(HR, (26, 46))]),
    "/limitations/6": ("The cache paragraphs describe the previous root.", S["n16_cache"]),
    "/limitations/7": ("delegation.md 153-155; the S/N records of revisions 15 and 16 in the head; SKILL.md 24 ties the PLAR handoff to plar.txt.", S["no_prod_state"] + [src(SKILL, (24, 24))]),
    "/limitations/8": ("c note F1-F4 (corrections section) record the b result's -01 paths and the b note sentences it corrects; both retained unchanged.", S["c_corr"]),
}

claims = []
for item in inventory["inventory"]:
    ptr = item["pointer"]
    if ptr == "/status":
        claims.append(row(ptr, *STATUS))
    elif ptr.startswith("/questions/"):
        idx, field = ptr.split("/")[2], ptr.split("/")[3]
        if field == "id":
            claims.append(row(ptr, "identifier of the question entry; non-operational metadata", [], "metadata"))
        else:
            claims.append(row(ptr, *Q[idx][field]))
    elif ptr in NEXT:
        claims.append(row(ptr, *NEXT[ptr]))
    elif ptr in LIM:
        claims.append(row(ptr, *LIM[ptr]))
    else:
        sys.exit(f"no review row authored for inventory leaf {ptr}")
    if json.dumps(claims[-1]["expected"], sort_keys=True) != json.dumps(item["value"], sort_keys=True):
        sys.exit(f"expected differs from the saved value at {ptr}")


def excerpt(path, start, end):
    lines = open(path, "rb").read().decode("utf-8-sig").splitlines(keepends=True)
    text = "".join(lines[start - 1:end])
    assert len(text.encode("utf-8")) <= 16384, (path, start, end)
    return {"path": path, "sha256": sha(path), "lines": [start, end], "text": text}


CARRIERS = [(BNOTE, 188, 231), (BNOTE, 233, 267), (BNOTE, 269, 302), (BNOTE, 304, 315),
            (BNOTE, 317, 341), (BNOTE, 357, 373), (BNOTE, 427, 445), (CNOTE, 24, 69), (CNOTE, 71, 96)]
carriers = [excerpt(p, a, b) for p, a, b in CARRIERS]

review = {"version": 1, "result": {"path": RESULT, "sha256": sha(RESULT)}, "scopes": SCOPES,
          "claims": claims, "carriers": carriers}
with open(OUT, "x", encoding="utf-8", newline="\n") as out:
    json.dump(review, out, ensure_ascii=False, indent=1)
    out.write("\n")
print(json.dumps({"review": OUT, "sha256": sha(OUT), "rows": len(claims),
                  "metadata_rows": sum(1 for c in claims if c["basis"] == "metadata"),
                  "carriers": len(carriers), "result_sha256": sha(RESULT)}, indent=1))
