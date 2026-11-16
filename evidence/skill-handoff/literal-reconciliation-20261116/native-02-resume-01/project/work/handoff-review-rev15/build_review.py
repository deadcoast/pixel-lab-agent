"""Build the version-1 literal handoff review for deliverables/specialist-return-2026-11-16b.json.

Worklist: the inventory written by check_handoff.py (every leaf of /questions, /next, /limitations).
For every leaf one row is written: basis source_comparison with actual source hashes and inclusive
line ranges (read in this session), or basis metadata for identifiers only. Carriers are the exact
current-instruction excerpts of deliverables/continuation-2026-11-16b.md, read from its bytes.
`expected` is the value the source-grounded reading supports; it is written per pointer below and
then compared with the saved value (a mismatch is printed, not silently copied over).

Run from the consumer root: python -B -I work/handoff-review-rev15/build_review.py
Writes exactly one new file (refuses to overwrite). First run wrote handoff-review-01.json, whose check
(handoff-check-01.json, retained) reported invalid_locator for two sources/brief.md ranges ending at line 34
(the file has 33 lines); this corrected version writes handoff-review-02.json.
"""
import hashlib, json, sys

RESULT = "deliverables/specialist-return-2026-11-16b.json"
INVENTORY = "work/handoff-review-rev15/handoff-inventory-01.json"
OUT = "work/handoff-review-rev15/handoff-review-02.json"  # -01 retained: two brief.md ranges ended at 34; the file has 33 lines
NOTE = "deliverables/continuation-2026-11-16b.md"
SCOPES = ["/questions", "/next", "/limitations"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def src(path, lines):
    return {"path": path, "sha256": sha(path), "lines": list(lines)}


# Source files (hashes measured at build time and compared with the values read in this session).
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
    "state.px/state.px": "8284e076c7d3052e69b78e47061b46971fa7b5b81f03e2a41b58cc7a511e565c",
    "CALLER-RESULT-LITERAL-RECONCILIATION.json": "7b033ec23f1307ab3083e8061fb5456a61fc389085b8b00ac36158d0f03229e3",
    NOTE: "6454d5b65397a7d1b647088055dccfb39e5b58173c34218df436584dae8c62f1",
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

# State wire lines (revision 15 head, read in this session): c_sample 3, f_sample 11, handoff_11 16,
# i_backgrounds 27, i_canvas 28, i_display_scale 30, i_outline 33, i_view 38, q_sample_readability 52,
# s_continuation_10 58, t_sample 80.
S = {
    "gates_code": [src(LIFE, (44, 77)), src(JOBS, (717, 743))],
    "plan": [src(STATE, (80, 80)), src(STATE, (11, 11)), src(STATE, (3, 3))],
    "readability": [src(STATE, (52, 52)), src(STATE, (30, 30)), src(STATE, (27, 27))],
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
    "sq": [src(BV2, (142, 171))],
    "shortlist": [src(SHORT, (1, 8)), src(READY, (99, 102))],
    "profile44": [src(PROFILE, (44, 44))],
    "stateauth": [src(SA, (13, 13)), src(JOBS, (731, 731))],
    "deleg69": [src(DELEG, (69, 69))],
    "adoption": [src(LIFE, (65, 75))],
    "planning_only": [src(DELEG, (153, 155))],
    "no_prod_state": [src(DELEG, (153, 155)), src(STATE, (58, 58)), src(STATE, (16, 16))],
    "eval_scope": [src(EVAL, (8, 8)), src(STATE, (33, 33)), src(STATE, (28, 28))],
    "readiness": [src(READY, (99, 102))],
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


# ---- findings per pointer -------------------------------------------------------------------
Q_COMMON = {
    "id": ("identifier of the question entry; non-operational metadata", "metadata", []),
    "addressed_to": None, "required_before": None, "question": None, "unlocks": None,
    "blocks_job_prepare": None, "owner_answer": None, "worksheet_rows": None,
}
Q = {
    "0": {  # Q1 capability input
        "addressed_to": ("Provider identity, tool name, live schema, arguments, discovery and authorization are request fields enforced by platform.py 869-889 / 1017-1023 and jobs.py 739-741; none is an owner art decision (brief.md 3-7 names no provider). Route choice between MCP surface and HTTP adapter is the caller's/host's (SKILL.md 26, PROFILE.md 32).", S["platform"] + S["route"] + S["brief_scope"]),
        "required_before": ("jobs.py 717-743 prepare() requires provider, tool, arguments, schema, discovery, authorization before saving the request; the plan trace (t_sample -> f_sample -> c_sample) is the saved one.", S["gates_code"] + S["plan"]),
        "question": ("Asks exactly for the fields platform.py validates (identity texts 869-870, arguments object 871-872, discovery fields 873/875-876, authorization fields 874/877, nonempty evidence 878-885, no secrets, schema validation 889, observed_at not in the future 1019-1023), the image transport required because a filename in a prompt is not an uploaded reference (PROFILE.md 44), and the route alternative (SKILL.md 26, PROFILE.md 32). The scope text exists at brief.md 6-7.", S["platform"] + S["profile44"] + S["route"] + S["brief_scope"]),
        "unlocks": ("SQ1-SQ4 are the brief's own schema questions (brief-v2 142-171); request_review.py 130-134 accepts only kind provider_arguments; delegation.md 69 requires the caller's request/criteria comparison before adoption; the criteria-v2 supersession is the g note's required step (61-74). Preparation is not submission or acceptance (PROFILE.md 44). Nothing here claims generation or acceptance.", S["sq"] + S["rr"] + S["deleg69"] + S["g1"]),
        "blocks_job_prepare": ("True: jobs.py 739-741 passes these inputs to platform.prepare_discovered, which fails without them (platform.py 869-889); pixl_readiness reports them not observed.", S["gates_code"] + S["platform"]),
        "owner_answer": ("False: no source makes provider discovery or authorization evidence an owner art decision; brief.md 3-7 names the family, destination, references and scope only.", S["brief_scope"] + S["platform"]),
        "worksheet_rows": ("Cross-reference into the note's worksheet rows R10-R15 and A1, which cite the same platform.py / SKILL.md / PROFILE.md lines.", [src(NOTE, (233, 267))]),
    },
    "1": {  # Q2 display scale / backgrounds
        "addressed_to": ("i_display_scale and i_backgrounds are owner choices (wh user) saved unresolved in the state; the caller relays owner questions (delegation.md 61-63 role split is established; the question is an owner answer, not a capability input).", S["readability"]),
        "required_before": ("q_sample_readability.ck: 'The target integer zoom requires i_display_scale before review; the three test backgrounds are the specialist's test set until i_backgrounds is answered.' Review follows import, which follows the one host call (d note 249-255); neither choice is linked through c_sample.ch, so lifecycle.py 57-64 does not gate job-prepare on them.", S["readability"] + S["dseq"] + [src(LIFE, (57, 64)), src(STATE, (3, 3))]),
        "question": ("Matches the two unresolved I records: i_display_scale (ky display_scale, unresolved, wy: target on-screen integer zoom not stated) and i_backgrounds (ky target_backgrounds, unresolved, wy: predominant level backgrounds not stated; the test bands are the agent's test set). Backgrounds are optional because the fallback exists in the criterion text.", S["readability"]),
        "unlocks": ("The criterion text names both effects; the fallback for backgrounds is stated there; no default for the zoom appears in any source.", S["readability"]),
        "blocks_job_prepare": ("False: neither choice is in c_sample.ch, so the choice gates of lifecycle.py 57-64 do not consider them; pixl_workflow lists no blocker for t_sample.", [src(LIFE, (57, 64)), src(STATE, (3, 3)), src(STATE, (80, 80))]),
        "owner_answer": ("True: both records carry wh user and are unresolved; the rationale fields name the owner's game as the only source.", S["readability"]),
        "worksheet_rows": ("Cross-reference to worksheet row A3 in the note, which cites the same records.", [src(NOTE, (233, 267))]),
    },
    "2": {  # Q3 production answers
        "addressed_to": ("Outline, canvas, role differentiation, animation and engine are owner choices (wh user) whose statuses are proposed/unresolved; the controlled answers bind the sample only (eval line 8).", S["eval_scope"] + S["readability"]),
        "required_before": ("lifecycle.py 65-75 applies task_decision, method_poc and choice_unconfirmed only in production/delivery phases; pixl_workflow shows those gates on t_scout, t_medic, t_family and none on t_sample.", S["adoption"] + [src(STATE, (80, 80))]),
        "question": ("Each named item is an I record: i_outline proposed (sample-scoped; family open), i_canvas proposed [32,32] (owner has not chosen, brief.md 23), i_palette observed coupled to i_role_diff, i_animation, i_engine unresolved; the evaluation answers' scope statement (line 8) is why these remain owner questions.", S["eval_scope"] + [src(BRIEF, (23, 23)), src(BRIEF, (28, 33))]),
        "unlocks": ("Production-phase gates per lifecycle.py 65-75 (task_decision 66-67, method_poc 68-72, choice_unconfirmed 72-75) and output_contract 53-56; answering adopts only what it names (intake-sample.md 97-104) and accepts no artwork (acceptance needs E/V, intake-sample.md 49-55).", S["adoption"] + [src(LIFE, (53, 56)), src(INTAKE, (97, 104)), src(INTAKE, (49, 55))]),
        "blocks_job_prepare": ("False: the production-phase gates do not apply to t_sample (phase sample, lifecycle.py 65).", S["adoption"] + [src(STATE, (80, 80))]),
        "owner_answer": ("True: all named choices are wh user and the brief's own 'does not state' list (brief.md 26-34) leaves them to the owner.", [src(BRIEF, (26, 33)), src(STATE, (33, 33)), src(STATE, (28, 28))]),
        "worksheet_rows": ("Cross-reference to worksheet row R6 and the decision table rows in the note.", [src(NOTE, (233, 267)), src(NOTE, (317, 341))]),
    },
}

NEXT = {
    "/next/operation": ("job-prepare is the operation whose inputs are the saved task/outputs/request (jobs.py 717-743); the -B -I prescription comes from handoff-review.md 40-42; the task/output/contract are the saved plan.", S["gates_code"] + S["hr_flags"] + S["plan"]),
    "/next/task": ("t_sample is the only ready task (phase sample, st open, dp [t_study] done, op [f_sample]).", [src(STATE, (80, 80))]),
    "/next/phase": ("t_sample.ph = sample; outside ADOPTION_PHASES (lifecycle.py 65).", [src(STATE, (80, 80)), src(LIFE, (65, 65))]),
    "/next/output": ("f_sample is t_sample's only planned output and carries ct c_sample.", [src(STATE, (11, 11)), src(STATE, (80, 80))]),
    "/next/contract": ("c_sample fields read from the head: al binary, ch 8 choices, pl three colours, px [32,32], sa nearest, vw side; record hash from pixl_validate.", [src(STATE, (3, 3))]),
    "/next/owner_answer_needed": ("False: no gate of job-prepare depends on an unresolved owner choice (lifecycle.py 57-64 over c_sample.ch finds none unresolved; production gates not applicable); the controlled answers already supply the sample's outline and canvas within their scope.", [src(LIFE, (57, 75)), src(STATE, (3, 3))] + S["eval"]),
    "/next/executable_locally_now": ("False: platform.py 869-889 requires provider/tool/schema/arguments/discovery/authorization that no local file supplies; pixl_readiness shows official tools not observed.", S["platform"] + S["readiness"]),
    "/next/expect_rule": ("jobs.py 731 loads with the expected hash; state-authority.md 13 requires the expected current canonical hash; the revision 15 hash is the current one.", S["stateauth"] + [src(STATE, (1, 1))]),
    "/next/job_id_rule": ("jobs.py 732-734: job_exists refuses an ID already present in the records.", [src(JOBS, (732, 734))]),
    "/next/state_side_gates/R1_job_exists": ("jobs.py 732-734; no J record exists in the 88 records (pixl_jobs []).", [src(JOBS, (732, 734))]),
    "/next/state_side_gates/R2_outputs_within_T_op": ("jobs.py 735 _context; t_sample.op [f_sample].", [src(JOBS, (735, 735)), src(STATE, (80, 80))]),
    "/next/state_side_gates/R3_task_prerequisite": ("lifecycle.py 49-52; t_sample.dp [t_study]; t_study st done (pixl_workflow).", [src(LIFE, (49, 52)), src(STATE, (80, 80))]),
    "/next/state_side_gates/R4_output_contract": ("lifecycle.py 53-56; f_sample kd sprite with ct c_sample.", [src(LIFE, (53, 56)), src(STATE, (11, 11))]),
    "/next/state_side_gates/R5_choice_unresolved_or_conflict": ("lifecycle.py 57-64 over the output's choices; c_sample.ch statuses read from the head: i_canvas proposed, i_palette observed, i_view confirmed, i_sampling proposed, i_alpha observed, i_lighting observed, i_outline proposed, i_design_language proposed.", [src(LIFE, (57, 64)), src(STATE, (3, 3)), src(STATE, (28, 28)), src(STATE, (33, 33)), src(STATE, (38, 38))]),
    "/next/state_side_gates/R6_adoption_phase_gates": ("lifecycle.py 65-75 apply only when T.ph in ADOPTION_PHASES; t_sample.ph sample.", S["adoption"] + [src(STATE, (80, 80))]),
    "/next/state_side_gates/R7_family_and_plan_blockers": ("lifecycle.py 76 families.blockers; pixl_workflow and pixl_context report no families and plans [].", [src(LIFE, (76, 76))]),
    "/next/state_side_gates/R8_job_pending": ("jobs.py 738 _pending; pixl_jobs [] (remote_executed false).", [src(JOBS, (738, 738))]),
    "/next/state_side_gates/R9_expect": ("jobs.py 731; state-authority.md 13; the hash exists after this commit and must be reread before the call.", S["stateauth"]),
    "/next/blocked_on/0": ("platform.py 869 _request_identity(provider); readiness: official_pixellab visibility not_observed, authentication not_verified.", [src(PLAT, (869, 869))] + S["readiness"]),
    "/next/blocked_on/1": ("platform.py 870 _request_identity(tool); readiness.md 101-102: a dated pixl_capabilities catalog is documentation, not live visibility; the shortlist file states it is from dated documentation, not discovery.", [src(PLAT, (870, 870))] + S["shortlist"]),
    "/next/blocked_on/2": ("platform.py 888-889 _schema_no_secrets / _validate_schema need the live schema object.", [src(PLAT, (888, 889))]),
    "/next/blocked_on/3": ("platform.py 871-872, 887, 889 (arguments object, no secrets, valid under schema); PROFILE.md 44 (image inputs through supported handles); request_review.py 130-134 (kind provider_arguments); g note 61-74 (criteria-v2 supersession step with validate_criteria_v2.py and a new S beside s_sample_criteria); delegation.md 69 (caller comparison before adoption).", [src(PLAT, (871, 872)), src(PLAT, (887, 889))] + S["profile44"] + S["rr"] + S["g1"] + S["deleg69"]),
    "/next/blocked_on/4": ("platform.py 873, 875-876, 878-885 and 1019-1023: discovery source text, observed_at ISO timestamp not in the future, nonempty evidence object.", S["platform"]),
    "/next/blocked_on/5": ("platform.py 874, 877, 878-885: authorization scope text and nonempty evidence object; the scope text exists in brief.md 6-7 ('Begin the project and make the progress possible in this session').", S["platform"] + [src(BRIEF, (6, 7))]),
    "/next/not_blocked_on": ("lifecycle.py 57-64 gates only the output contract's linked choices (none unresolved); q_sample_readability.ck places i_display_scale/i_backgrounds before review; the d note's sequence places review after import.", [src(LIFE, (57, 64)), src(STATE, (3, 3))] + S["readability"] + S["dseq"]),
    "/next/alternatives/A1_route": ("SKILL.md 26 and PROFILE.md 32 name the MCP surface as primary and the HTTP adapter as an explicitly selected alternative; readiness shows neither observed.", S["route"] + S["readiness"]),
    "/next/alternatives/A2_first_candidate_path": ("intake-sample.md 25 and SKILL.md 24 offer PLAR preparation for a selected PLAR asset; no plar.txt exists in this consumer (directory listing), so the record-level sequence applies.", S["plar"]),
    "/next/alternatives/A3_visual_review_inputs": ("q_sample_readability.ck names the fallback test set and the i_display_scale requirement before review; no default zoom appears in i_display_scale.wy or any source.", S["readability"] + S["dseq"]),
    "/next/preparatory_steps_once_Q1_is_supplied/0": ("SQ1-SQ4 at brief-v2 142-171 ask exactly fixed size, style-image transport, transparency/alpha, output cardinality; the shortlist declares itself a dated catalog, not discovery.", S["sq"] + S["shortlist"]),
    "/next/preparatory_steps_once_Q1_is_supplied/1": ("g note finding 1, lines 23-31 and 61-74: line 20 (optionally 5), five check texts unchanged, validate_criteria_v2.py --criteria <v2> --out <fresh work/ path>, never validate_criteria.py, new S beside the unchanged s_sample_criteria.", S["g1"]),
    "/next/preparatory_steps_once_Q1_is_supplied/2": ("platform.py 871-872, 887, 889 (object, no secrets, schema-valid); PROFILE.md 44 (actual image handles; a filename in a prompt is not an uploaded reference).", [src(PLAT, (871, 872)), src(PLAT, (887, 889))] + S["profile44"]),
    "/next/preparatory_steps_once_Q1_is_supplied/3": ("request_review.py 130-134 requires kind provider_arguments; delegation.md 69 requires the caller's independent comparison before adopting the contract.", S["rr"] + S["deleg69"]),
    "/next/preparatory_steps_once_Q1_is_supplied/4": ("jobs.py 717-743 prepare(); PROFILE.md 44: preparation is not submission, payment, completion or proof of acceptance.", S["gates_code"] + S["profile44"]),
    "/next/sequence_after_prepare/0": ("d note 249-255: the caller's comparison of the saved request with the reviewed packet precedes dispatch.", S["dseq"]),
    "/next/sequence_after_prepare/1": ("d note 249-255 and PROFILE.md 45: publish the single dispatch claim before the one authorized host call.", S["dseq"] + [src(PROFILE, (45, 45))]),
    "/next/sequence_after_prepare/2": ("PROFILE.md 45: use the returned request through the actual PixelLab tool discovered in that session; capture identifiers.", [src(PROFILE, (45, 45))]),
    "/next/sequence_after_prepare/3": ("d note 249-255: job-observe records the returned identifier and states; PROFILE.md 46 observed states only.", S["dseq"] + [src(PROFILE, (46, 46))]),
    "/next/sequence_after_prepare/4": ("d note 249-255: job-import snapshots the download as an unaccepted X for f_sample; PROFILE.md 47 imported provider success is not acceptance.", S["dseq"] + [src(PROFILE, (47, 47))]),
    "/next/sequence_after_prepare/5": ("d note 249-255 names the two mechanical and three visual E/V routes and the i_display_scale / i_backgrounds dependence; intake-sample.md 62 names task-complete after all saved criteria pass.", S["dseq"] + [src(INTAKE, (62, 62))] + S["readability"]),
    "/next/procedural_prescriptions/P1_literal_handoff_review": ("intake-sample.md 147-153 and handoff-review.md 20-24, 26-46, 80-93, 101-126 prescribe the inventory with check_handoff.py, one row per leaf, carriers of the current note, the --review check, keeping review/check hashes out of the result, and that coverage is not semantic acceptance.", S["hr_all"]),
    "/next/procedural_prescriptions/P2_interpreter_flags": ("handoff-review.md 40-42 prescribe -B -I for the helper and other Python reads of a read-only kit; check_handoff.py 9-11 notes that -I ignores PYTHONDONTWRITEBYTECODE; the interpreter path is the session constraint carried since the f note (SESSION.md, mutable, not cited).", S["hr_flags"]),
    "/next/procedural_prescriptions/P3_no_bytecode_cache": ("The 2026-11-16 note 58-66 and the caller result lines 200/208 describe a cache in the previous root; the kit here holds 261 files and no __pycache__ (verify_rev15.py observation, measured in this session); handoff-review.md 40 gives the reason to avoid creating one.", S["n16_cache"] + [src(HR, (40, 42))]),
    "/next/procedural_prescriptions/P4_criteria_validation": ("g note 69-72: re-validate with validate_criteria_v2.py --out a fresh path, never validate_criteria.py; the 2026-11-16 note 270-271 records the artifact that validate_criteria.py would overwrite.", [src(G, (61, 74)), src(N16, (270, 271))]),
    "/next/procedural_prescriptions/P5_current_verifier": ("The 2026-11-16 note 215-239 explains verify_rev13.py's kit-identity exit 1 and verify_rev14.py's manifest-based design; verify_rev15.py follows the same design for revision 15 (run in this session: problems [] on candidate and head; verify_rev14.py problems [] with kit_changed_since_snapshot true).", S["n16_verify"]),
    "/next/procedural_prescriptions/P6_cold_start": ("intake-sample.md 161-190 (cold intake handoff: start with workflow and focused context) and 64 (a cold session starts with workflow and context); g note 23-31 and 74 (read line 19 as line 20 until the successor exists).", S["cold"] + [src(INTAKE, (64, 64))] + S["g1"]),
    "/next/final_wording": ("Same conclusion as R1-R15/A1-A3: gates satisfied (lifecycle.py 44-77), inputs missing (platform.py 869-889), successor packet required (request_review.py 130-134; delegation.md 69; g note 61-74), display scale before review only (q_sample_readability.ck).", S["gates_code"] + S["platform"] + S["rr"] + S["deleg69"] + S["g1"] + S["readability"]),
}

LIM = {
    "/limitations/0": ("pixl_readiness: official tools not_observed, authentication not_verified, execution not_attempted; pixl_jobs []; t_sample open with ca [] (state line 80); delegation.md 153-155: an open task remains an explicit unfinished part.", S["readiness"] + S["planning_only"] + [src(STATE, (80, 80))]),
    "/limitations/1": ("The 2026-11-16 note 85-87 states the previous bytes are not retained; the current diff was measured against work/rev14-protected-snapshot.sha256 kit entries in this session.", [src(N16, (85, 87))]),
    "/limitations/2": ("g note finding 1 (23-31, 61-74): bound bytes keep line 19 until the successor packet; read as line 20 (verbatim line 5 of brief.md).", S["g1"] + [src(BRIEF, (5, 5)), src(BRIEF, (19, 20))]),
    "/limitations/3": ("g note finding 2 table line 92: the 2026-11-14 session's root is not recorded in a retained caller result.", [src(G, (87, 94))]),
    "/limitations/4": ("handoff-review.md 107-113: coverage_complete means declared coverage and bindings match; semantic_verdict remains not_assessed; delegation.md 86-97: the caller reviews every listed value independently.", [src(HR, (107, 113)), src(DELEG, (86, 97))]),
    "/limitations/5": ("Measured in this session (which python -> C:/Python314; ModuleNotFoundError jsonschema when running the runner); handoff-review.md 28 and 40-42 prescribe the assigned interpreter with -B -I.", [src(HR, (26, 46))]),
    "/limitations/6": ("The cache paragraph in the caller result (200, 208) and the 2026-11-16 note (58-66) describe the previous root; verify_rev15.py's kit_bytecode_cache_dirs [] measured here.", S["n16_cache"]),
    "/limitations/7": ("delegation.md 153-155: a planning-only assignment does not need manufactured production state; the two added records are visible at state lines 16 and 58; no plar.txt exists (directory listing), so the PLAR handoff operation does not apply (SKILL.md 24 ties it to plar.txt).", S["no_prod_state"] + [src(SKILL, (24, 24))]),
}

claims = []
for item in inventory["inventory"]:
    ptr = item["pointer"]
    if ptr.startswith("/questions/"):
        idx, field = ptr.split("/")[2], ptr.split("/")[3]
        if field == "id":
            finding, basis, sources = Q_COMMON["id"]
            claims.append(row(ptr, finding, sources, basis))
        else:
            finding, sources = Q[idx][field]
            claims.append(row(ptr, finding, sources))
    elif ptr in NEXT:
        claims.append(row(ptr, *NEXT[ptr]))
    elif ptr in LIM:
        claims.append(row(ptr, *LIM[ptr]))
    else:
        sys.exit(f"no review row authored for inventory leaf {ptr}")
    if json.dumps(claims[-1]["expected"], sort_keys=True) != json.dumps(item["value"], sort_keys=True):
        sys.exit(f"expected differs from the saved value at {ptr}")

# Carriers: exact excerpts of the current-instruction sections of the new note.
note_lines = open(NOTE, "rb").read().decode("utf-8-sig").splitlines(keepends=True)
CARRIERS = [(188, 231), (233, 267), (269, 302), (304, 315), (317, 341), (357, 373), (427, 445)]
carriers = []
for start, end in CARRIERS:
    text = "".join(note_lines[start - 1:end])
    assert len(text.encode("utf-8")) <= 16384, (start, end)
    carriers.append({"path": NOTE, "sha256": sha(NOTE), "lines": [start, end], "text": text})

review = {"version": 1, "result": {"path": RESULT, "sha256": sha(RESULT)}, "scopes": SCOPES,
          "claims": claims, "carriers": carriers}
with open(OUT, "x", encoding="utf-8", newline="\n") as out:
    json.dump(review, out, ensure_ascii=False, indent=1)
    out.write("\n")
meta = sum(1 for c in claims if c["basis"] == "metadata")
print(json.dumps({"review": OUT, "sha256": sha(OUT), "rows": len(claims), "metadata_rows": meta,
                  "carriers": len(carriers), "result_sha256": sha(RESULT)}, indent=1))
