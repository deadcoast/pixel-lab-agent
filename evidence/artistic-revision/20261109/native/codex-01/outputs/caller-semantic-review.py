"""Caller-authored semantic comparisons, bound to actual adopted records at execution."""
import json, pathlib, hashlib
R=pathlib.Path(__file__).resolve().parents[2]
O=R/'work/artistic-revision'
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
# Each tuple: source obligation; literal additions/scope; discriminating alternative.
BASIS=[
('BRIEF paragraph 1 requires four horizontal 16px cells; original queue-view display fixes geometry.', 'No-gutter is sheet addressing; transparent margin inside each cell remains permitted. Fixture description is destination-scoped.', 'A 64x16 strip with narrower centered marks and transparent in-cell margins passes; an inter-cell gutter breaks the addressing contract.'),
('BRIEF requires transparent backgrounds, without prescribing alpha counts.', 'Component flags are diagnostic; equality to seed rotation applies only to the recorded construction proposal.', 'An intentional full-span X or partially transparent contour can satisfy the owner and must receive visual review rather than automatic rejection.'),
('BRIEF requires a transparent exterior at actual display scales.', 'Visual judgment decides matte/fringe; deliberate backing can belong to the mark; partial alpha allowed.', 'A deliberate opaque emblem plate with clear exterior can pass; an unintended opaque square matte fails.'),
('AUTHORING-STAGE frame assembly must retain exact frame selection and provenance.', 'Already-exact sheet needs no new assembly; future assembly must retain raw inputs and visible RGBA/alpha losslessly.', 'A documented repeated phase is allowed; silently dropping a provider frame is not.'),
('BRIEF says activity without success; reduced-motion update adds stationary Working.', 'Single transient-frame reading is an explicit specialist choice; loop and held reading remain required.', 'A loop whose transients are abstract but whose motion reads activity could satisfy owner wording yet fail this explicitly scoped expert clause.'),
('BRIEF fixes 100ms per frame and requires activity; existing family acceptance requires loop continuity.', 'Actual playback with wrap at both scales is required; no preferred pacing is promoted to owner timing.', 'A continuous loop with different apparent angular velocity can pass at 100ms; 120ms cells fail the timing requirement.'),
('BRIEF readability/cool blue plus FAMILY-RESULT scoped Ready adoption.', 'No exact palette, alpha, weight or margins; intentional selective AA allowed.', 'A mostly neutral readable mark with perceptible blue accent can pass; palette equality is unnecessary.'),
('Original stateAfter started maps running, both consumers share visual; reduced-motion update preserves normal behavior.', 'Descriptor is implementation fact; synthetic arithmetic proves indexing only; live playback remains separate.', 'A synthetic timeline with correct indices and a frozen live canvas cannot establish motion-continuity acceptance.'),
('ARTISTIC-REVISION current caller chooses P1 frame zero; historical brief did not choose that cell.', 'Crop/count/centroid are observations; still=0 is a scoped evaluation choice.', 'Another distinguishable still would satisfy broad update, but would require a changed caller choice and fresh identity/reviews.'),
('AUTHORING-UPDATE requires stationary Working distinct from Ready and Paused.', 'Color/non-color view is review method for structural distinction.', 'A different-colored check still fails shape distinction; an incomplete segmented ring may pass.'),
('BRIEF Retry distinguishability extends to displayed held status; shared Start comparison is inference.', 'Start remains explicitly inferred, not owner-authored motif restriction.', 'A held triangle could avoid Ready/Paused but fail the adopted shared-consumer Start inference.'),
('Reduced-motion update requires a stationary Working symbol; current brief explicitly demands alone and label review.', 'Label cannot rescue an otherwise unreadable symbol.', 'A generic dot that only becomes Working because of its label fails; a familiar incomplete progress ring can pass alone.'),
('Reduced-motion update requires stationary mapping in both consumers, original geometry unchanged.', 'still/holdFrame/matchMedia are implementation-scoped; explicit override has matching semantics.', 'Changing frames to 1 under reduced motion would hide original sheet geometry and fail even if a still appeared.'),
('FOCUSED-SUCCESSOR and current assignment require preference changes while open.', 'Same session repaint and restart are required; static-state pixel invariance now needs actual assertion.', 'Reloading to change preference fails; correct same-page descriptors with unchanged pixels for Retry/Paused/Ready/Start can pass.'),
('BRIEF requires static 16x16 Retry at updated destination.', 'One frame, not a strip; no motif chosen.', 'A static outline-free retry symbol can pass; a 32x16 two-cell strip fails.'),
('BRIEF transparency has no static-member alpha recipe.', 'Counts/components are diagnostics only, not rejection rules.', 'A large intentional backing may trigger diagnostics while passing visual exterior review.'),
('BRIEF transparent Retry at native/enlarged scale.', 'Visual matte decision allows partial alpha and intentional subject backing.', 'Selective AA can pass; gray canvas matte fails.'),
('BRIEF says Error/retry distinguishable without color; Paused update extends comparison set.', 'Failure/retry meaning required; arrow is example only; Start comparison remains inference.', 'A readable failure/retry motif without an arrow is permitted; an activity spinner recolored red fails.'),
('BRIEF readable/cool blue; FAMILY-RESULT broad Ready style adoption.', 'Qualitative clusters/steps/coherence, not exact Ready geometry.', 'Thicker but coherent readable Retry with blue accent can pass.'),
('Original error maps failed and same Retry asset in both consumers.', 'Descriptor extension is implementation fact; actual live static pixels under both preferences required.', 'Correct descriptors without any live Retry capture leave evidence incomplete.'),
('BRIEF paused update requires static status in existing display contract.', '16x16 single frame; no required paired-bar construction.', 'A distinct paused-work motif other than bars can pass.'),
('BRIEF transparency has no Paused alpha-set requirement.', 'Static measurements diagnostic only.', 'A mark with partial alpha can pass despite differing histogram from current asset.'),
('BRIEF transparent Paused at actual scales.', 'Unintended matte fails; selective alpha allowed.', 'Intentional foreground backing with transparent exterior can pass.'),
('BRIEF paused must differ from activity, completion and Retry without color.', 'Start is shared-consumer inference; paired bars are not mandatory.', 'A readable paused motif without bars can pass; a two-color clone of Working fails.'),
('BRIEF and FAMILY-RESULT broad readability and Ready coherence.', 'No numerical thickness/footprint restriction.', 'A Paused mark with different weight but coherent deliberate treatment can pass.'),
('Original pause maps paused through both consumers.', 'Static behavior under normal/reduced plus actual live output; descriptor is destination fact.', 'Static metadata alone with missing live Paused pixels cannot pass integration.'),
('BRIEF coherent family and exact adopted Ready baseline; update includes held cell.', 'Qualitative weight, transparency and blue; actual loop/wrap and held review required.', 'Coherent family with unequal stroke widths is allowed; inspecting stills alone cannot pass playback leg.'),
('BRIEF activity/not success and Retry/Paused shape distinctions; update adds held state.', 'Grayscale comparison method; Start distinction inferred explicitly.', 'A color-only distinction fails; visually different silhouettes can pass despite palette identity.'),
('Current assignment moves only new successor destination; original backend/assets preserved.', 'Fixture arithmetic is bounded; current task additionally requires measured live playback and all-state pixels.', 'A synthetic 400ms timeline cannot prove wall-clock playback; correct source hashes cannot substitute for actual rendered pixels.')
]
def main():
    source=load('work/continuation/SPECIALIST-ROUND2.json')['corrected_criteria']
    mapping=load('work/artistic-revision/adopted-criteria.json')
    by={x['source_id']:x for x in mapping['corrected_29']}
    rows=[]
    for r,(obligation,delta,alternative) in zip(source,BASIS,strict=True):
        m=by[r['id']]
        rows.append({'source_id':r['id'],'criterion':m['record_id'],'source_obligation':obligation,
          'authority_basis':m['authority_label_for_record'],'scope':r['original_scope'],
          'literal_delta':delta,'discriminating_alternative':alternative,
          'check_sha256':hashlib.sha256(m['check'].encode()).hexdigest(),
          'disposition':'Keep required outcome and attributed scoped clauses; destination rederivations assessed separately against actual code/capture.'})
    out={'reviewer':'independent calling agent /root','mapping':{'path':'work/artistic-revision/adopted-criteria.json','sha256':sha('work/artistic-revision/adopted-criteria.json')},
      'source_round2':{'path':'work/continuation/SPECIALIST-ROUND2.json','sha256':sha('work/continuation/SPECIALIST-ROUND2.json')},
      'criterion_comparisons':rows,'scope':'Semantic source/authority comparison; not candidate acceptance. Literal mapping and production evidence checked independently.'}
    (O/'caller-criterion-comparisons.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
