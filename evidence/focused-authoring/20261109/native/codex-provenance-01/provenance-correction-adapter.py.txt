"""Bounded native correction of observed source-time provenance, preserving trials."""
import json
import shutil
from pathlib import Path
from evaluations.request_review_trials import ROOT, inventory, prepare, run, sha, write_json

destination = ROOT / 'evidence/focused-authoring/20261109/native/codex-provenance-01'
predecessor = ROOT / 'evidence/focused-authoring/20261109/native/codex-successor-01'
prepare(destination, 'codex', 'plar-authoring-review', predecessor)
project = destination / 'project'
guidance = '''This is a bounded caller provenance correction after the completed
native successor attempt. PROVENANCE-CORRECTION.md is current. Preserve all old
evidence/results, source, renderer and assets. New files go in work/provenance-correction;
advance state and authoring-plar only through public operations. No global settings
or memory writes. Parse JSON as UTF-8. Existing artistic/renderer judgments retain
their actual limits; this correction does not assign new generation or close
unavailable motion review. No fresh specialist drafting is necessary for a
metadata-only correction of unchanged source bytes and unchanged art obligations.
'''
assignment = '''# Correct unsupported source observation times

The previous caller completed SUCCESSOR-RESULT.json, with Retry/Paused accepted
and Working/family open. Independent maintainer inspection found a concrete
provenance defect: work/successor-adoption/plan-02.py assigns eight successor.source.*
S records the literal at=2026-11-09T20:00:00+00:00. The actual run was earlier that
day (the outer review observed it at about11:12UTC). That precise future time was
not observed. Actual source bytes/hashes and rendered evidence are otherwise
retained; do not discard or rewrite that failed attempt.

Use the current installed kit. Confirm the eight records and read the real clock
for new observations; do not invent another timestamp. Append corrected source
records with the same exact file/line/hash identities and explicitly retain an
erratum identifying each old record and unsupported time. Because old plan and
verdict scopes bind those S records, preserve them and use a NEW explicit successor
plan/allocation through selection.replaces, with corrected source/choice/contract
bindings as needed. Do not mutate an immutable marker/intent or silently rehash old
receipts. Preserve prior caller comparisons and results.

Independently compare the new exact request_review report against the retained
23-check successor contract: only provenance IDs/time bindings and necessary
new-plan references should change. Preserve all20 original criterion mappings,
the3 diagnostic/visual splits, current reduced-motion requirements, same actual
destination, source bytes and exact image candidates. Preserve the current PLAR
semantic requirements/hash; only production/status/next/evidence should advance.

Retain new candidate/criterion verdicts under the corrected scope using the actual
unchanged measurements, viewed images and renderer observations with explicit
continuity evidence and newly verified bindings. Existing observations may be
reused honestly because their inputs and obligations are unchanged; do not claim
a new viewing/render execution if you only verified that continuity. Reopen no
artistic design question solely to fix timestamp metadata. Keep Working motion
unavailable; do not create or accept a family package while it is incomplete.
Complete Retry/Paused only with the required correctly bound fresh verdicts and
retain handoffs. Preserve old records and files, apart from the existing public
project/selection updates required for new records.

Return PROVENANCE-RESULT.json: erratum, actual observed time, old-to-new source
mapping, exact new plan and independent comparison, current source-closure check
showing the unsupported future timestamps are no longer in the active acceptance
scope, corrected candidate/verdict/PLAR/handoff identities, preservation checks,
and the unchanged temporal/family acceptance gap. This is not new generated-art
quality or general host-reliability evidence.
'''
(project/'PROVENANCE-CORRECTION.md').write_text(assignment,encoding='utf-8')
for n in ['AGENTS.md','SESSION.md']:(project/n).write_text(guidance,encoding='utf-8')
(destination/'prompt.txt').write_text('Complete PROVENANCE-CORRECTION.md and return PROVENANCE-RESULT.json.\n'+guidance,encoding='utf-8')
specialist='You are PIXL only for explicitly delegated review work. '+guidance
(project/'.codex/agents/pixl.toml').write_text('name = "pixl"\ndescription = "PixelLab visual asset specialist."\ndeveloper_instructions = '+json.dumps(specialist)+'\n',encoding='utf-8')
launch=json.loads((destination/'launch.json').read_text(encoding='utf-8'));launch['case']='successor-source-provenance-correction';write_json(destination/'launch.json',launch)
identity=json.loads((destination/'identity.json').read_text(encoding='utf-8'))
identity.update(inputs=inventory(project,('pixl-kit',)),prompt_sha256=sha(destination/'prompt.txt'),adapter_sha256=sha(Path(__file__)),scope='Bounded native correction of unsupported source times; preserve completed evidence and unavailable motion review.')
write_json(destination/'identity.json',identity)
for n in ['PROVENANCE-CORRECTION.md','AGENTS.md','SESSION.md']:shutil.copyfile(project/n,destination/'input-project'/n)
shutil.copyfile(project/'.codex/agents/pixl.toml',destination/'input-project/.codex/agents/pixl.toml')
shutil.copyfile(__file__,destination/'provenance-correction-adapter.py.txt')
run(destination)
