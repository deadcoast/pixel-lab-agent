import json,hashlib,datetime,subprocess
from pathlib import Path
O=Path('work/artistic-revision');PY='C:/github/pixel-lab-agent/.venv/Scripts/python.exe';RUN='.agents/skills/artistic-revision-kit/scripts/pixl.py';S='.pixl/assets/queue.ready';ROOT=str(Path.cwd())
def save(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def call(tag,*args):
 p=subprocess.run([PY,RUN,*args],capture_output=True,text=True,encoding='utf-8');Path(O/(tag+'.json')).write_text(p.stdout,encoding='utf-8')
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return json.loads(p.stdout)
visual={
 'transparent-exterior-visual':'Viewed native and3x colour/gray marks and rendered panel exterior. Negative space remains panel; no unintended solid tile, fringe or halo. Alpha diagnostics were not used as the deciding visual rule.',
 'activity-not-success':'All four exposed poses and chronological observed rotations show separated perimeter clusters. None forms the Ready check or terminal success pose; held frame0 reads a stationary incomplete progress ring.',
 'motion-continuity':'Inspected actual ordered normal-start and normal-restored exposures, including repeated 3-to-0 wraps at both scales in retained render. Quarter-turn phases preserve one rotating activity motif without a visible end-pose discontinuity. Sampled paint/exposure clocks distinguish actual exposure from synthetic timeline; continuous exact100ms cadence is not claimed.',
 'style-coherence':'Native/3x colour and gray views show compact readable silhouettes, deliberate stepped clusters and related perceptible cool-blue accents against exact Ready. Start remains vector control/color reference. No palette-count,alpha,stroke-width or margin gate imposed.',
 'stationary-distinct-ready-paused':'Held broken ring differs from Ready diagonal check and paired upright pause bars in colour and grayscale at1x/3x; it has neither completion nor pause structure.',
 'stationary-distinct-retry-start':'Held incomplete separated-cluster ring has no Retry arrowhead and differs from solid Start triangle in colour/gray1x/3x. Start distinction remains adopted shared-consumer inference.',
 'stationary-meaning':'Viewed held symbol alone in native/3x family strip, then beside Working label in reduced screenshot: incomplete segmented ring reads ongoing/incomplete progress by itself. Label corroborates; no check or pause symbol is present.',
 'retry-meaning-without-color':'The circular return arrow with visible arrowhead conveys retry and remains distinct from Ready check, separated activity clusters, paired pause bars and Start triangle in grayscale/native/3x.',
 'pause-meaning-without-color':'Two stable upright separated bars read as pause in native/3x colour and grayscale, structurally different from the activity ring, Ready check and Retry return arrow.',
}
local={
 'geometry':'Fresh decode records exact target geometry: Working64x16, Retry/Paused16x16. All actual rendered crops match source dimensions and horizontal cell rectangles.',
 'transparent-exterior-measured':'Fresh per-cell alpha histograms, exact RGBA boxes and4-connected components retained. Flags are diagnostic only. Working seed-rotation alpha and visibleRGBA equality pass all4cells under the scoped seed-rotation proposal; selective/full alpha remains permitted.',
 'frame-assembly':'No assembly executed: cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc reused byte-identically from live.working-animation-motion-01.candidate. Fresh rotation checks identify cells0..3 as clockwise seed rotations and preserve all cells.',
 'stationary-cell-identity':'Fresh frame0 measurement matches224alpha0/32alpha255, three4-connected boxes [[3,10,8,14],[5,3,10,5],[12,6,14,11]], centroid[7.90625,9.0]pixel-edge coordinates; visibleRGBA/alpha equals seed. still=0 is current scoped evaluation caller choice.',
}
engine={
 'consumers-normal-motion':'Fresh frozen renderer capture-switch04 and checker pass: both consumers at live1x/3x plus matrix1x/3x show shared running descriptor and source pixels; deterministic boundaries retained separately. Observed live paint clocks cover0..3 and wraps; actual exposures match reported painted frame.',
 'reduced-motion-consumer-mapping':'Reduced phase and separate initially-reduced03 run hold exact frame0 in both consumers/live scales/matrix. All31exposures frame0; animation gate false and stored paint time unchanged across held exposures. All static descriptors unchanged. Geometry remains4cells; source supplies default query and identical explicit override semantics.',
 'live-preference-switch':'One sessionId across normal/reduced/restored; actual change events list in-place repaint of both consumers and live1x/3x plus matrix. Held0under reduced, observed cycling and3-to-0wrap after restoration. Added checker explicitly verifies non-Working pixel hashes unchanged across preferences.',
 'consumers':'Fresh all-state live snapshots include error->failed and pause->paused under normal and reduced, both consumers/scales. Static pixels equal decoded matrix/source pixels, frame0held, correct labels/path/geometry, nearest filtering; checker pass.',
}
observations=[{'path':str(O/'fresh-measurements.json').replace('\\','/'),'mode':'local','note':'Fresh decoded candidate measurements, geometry/provenance and construction-scoped rotation checks.'}]
for path,note in [('work/focused-successor/specialist-views/specialist-family-color-1x.png','Viewed actual exact reused art native colour; Working cells0..3 then Ready,Paused,Retry,Start.'),('work/focused-successor/specialist-views/specialist-family-color-3x.png','Viewed exact reused art3x nearest colour; shape/clusters/alpha exterior/family relation.'),('work/focused-successor/specialist-views/specialist-family-gray-1x.png','Viewed native grayscale structural distinction without colour.'),('work/focused-successor/specialist-views/specialist-family-gray-3x.png','Viewed3xgrayscale structure; no colour-only distinction.'),('work/artistic-revision/capture-switch-04/reduced-destination.png','Viewed actual reduced-motion label context and standalone matrix/live1x/3x.'),('work/artistic-revision/observed-sequence-normal-start.png','Viewed actual ordered temporal exposures through repeated wrap.'),('work/artistic-revision/observed-sequence-normal-restored.png','Viewed actual ordered resumed exposures through repeated wrap.')]:observations.append({'path':path,'mode':'visual','note':note})
for path in ['work/artistic-revision/capture-switch-04/render.json','work/artistic-revision/capture-initial-reduced-03/render.json','work/artistic-revision/check-switch-04.json','work/artistic-revision/check-initial-reduced-03.json']:observations.append({'path':path,'mode':'live','note':'Actual isolated browser execution and checked retained pixel/descriptor/clock/preference evidence; measured scope only.'})
for ob in observations:ob['sha256']=sha(ob['path'])
for kind in ['working','retry','paused']:
 ctx=call('review-context-final-'+kind,'review-context',S+'/state.px','artistic2.'+kind+'.candidate','--root',ROOT)
 verdicts=[]
 for q in ctx['criteria']:
  key=q['id'].split('.q.')[1];mode=q['mode'];reason=(local if mode=='local' else visual if mode=='visual' else engine)[key]
  verdicts.append({'criterion':q['id'],'status':'pass','reason':reason,'supersedes':None,'observations':[i for i,o in enumerate(observations) if o['mode']==mode]})
 review={'version':1,'binding_hash':ctx['binding_hash'],'reviewer':'actor','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'observations':observations,'verdicts':verdicts,'action':'complete','next_action':'Collective fresh family snapshot/review; caller independently verifies retained evidence.','limitations':['Exact continuous100mswall-clock cadence is not established; sampled rAFpaint/exposure and source100msindexing are established.','Reused art only; no provider execution or broader generated quality claim.']};save(O/('review-'+kind+'.json'),review);res=call('review-result-'+kind,'candidate-review',S,'artistic2.'+kind+'.candidate','artistic2.'+kind+'.review',str(O/('review-'+kind+'.json')),'--expect',ctx['state_hash'],'--root',ROOT);print(kind,res.get('task_status'),res.get('state_hash'))
