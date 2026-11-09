"""Independent caller comparison and reproducible mechanical analysis; UTF-8 only."""
from pathlib import Path
import json, hashlib, importlib.util, base64
from collections import Counter, deque
from PIL import Image, ImageChops

root=Path.cwd(); work=root/'work/focused-successor'
def read(p): return json.loads((root/p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256((root/p).read_bytes()).hexdigest()
def save(name,obj): (work/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
proposal=read('work/focused-successor/specialist-proposal-r3.json')
context_raw=read('work/focused-successor/context.raw.json')
context=json.loads(context_raw['content'][0]['text'])
save('context.json',context)
assert read('work/focused-successor/context.json')==context
original=read('work/export-review-01/request-review.json')
prior=read('work/export-review-01/caller-comparison.json')
assert len(proposal['criteria'])==20
originals={c['id'] if 'id' in c else c['criterion']:c for c in original['criteria']}
assert set(c['criterion'] for c in proposal['criteria'])==set(originals)
spec=importlib.util.spec_from_file_location('successor_checker',root/'renderer-successor/check.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
pixels=module.check(root,work/'render-02');save('pixel-check-02.json',pixels)
assert pixels['status']=='pass',pixels['failures']
render=read('work/focused-successor/render-02/render.json')
motion=read('work/focused-successor/render-02/motion.json')
motion_results=[]
for phase in motion['phases']:
    times=[s['at'] for s in phase['samples']]
    each=[]
    for consumer in ['statusCell','compactStatus']:
        cells=[next(c for c in s['cells'] if c['consumer']==consumer) for s in phase['samples']]
        frames=sorted({c['frame'] for c in cells});hashes=sorted({c['image']['sha256'] for c in cells})
        assert all(c['state']=='running' and c['label']=='Working' and c['smoothing'] is False and c['width']==48 and c['height']==48 for c in cells)
        for c in cells:
            p=work/'render-02'/c['image']['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==c['image']['sha256']
        assert frames==([0] if phase['reduced'] else [0,1,2,3])
        assert len(hashes)==(1 if phase['reduced'] else 4)
        each.append({'consumer':consumer,'frames':frames,'pixel_hashes':hashes,'samples':len(cells)})
    assert times[-1]-times[0]>=800
    assert all(s['reduced']==phase['reduced'] for s in phase['samples'])
    assert all(s['cells'][0]['frame']==s['cells'][1]['frame'] for s in phase['samples'])
    motion_results.append({'phase':phase['name'],'reduced':phase['reduced'],'span_ms':times[-1]-times[0],'consumers':each,'preference_changes':phase['samples'][-1]['changes']})
reduced=read('work/focused-successor/render-02/reduced-render.raw.json')
assert reduced['reduced'] is True and not reduced['missing'] and not reduced['errors']
assert all(v['frame']==0 for v in reduced['views'])
assert all(s['frame']==0 for s in reduced['timeline'])
assert len(reduced['views'])==20
save('motion-check.json',{'status':'pass','phases':motion_results,'reduced_all_states_views':20,'reduced_timeline_all_frame_zero':True,'all_backend_transitions':[t['event'] for t in reduced['transitions']], 'limits':'Actual browser rAF samples and CDP media emulation in one page; exact compositor scheduling and human temporal playback are not measured. 100ms phase arithmetic is independently checked at boundaries. No global preference changed.'})

# Alpha measurements remain diagnostics. Occupancy is never an artistic verdict.
diagnostics=[]
for name in ['working.png','paused.png','error-retry.png','ready-confirmed.png']:
    image=Image.open(root/'renderer-successor/assets'/name).convert('RGBA')
    frames=[]
    for i in range(image.width//16):
        frame=image.crop((i*16,0,(i+1)*16,16));points={(x,y) for y in range(16) for x in range(16) if frame.getpixel((x,y))[3]}
        components=[]
        while points:
            todo=[points.pop()]; component=[]
            while todo:
                x,y=todo.pop();component.append((x,y))
                for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if n in points:points.remove(n);todo.append(n)
            xs,ys=zip(*component);box=[min(xs),min(ys),max(xs)+1,max(ys)+1]
            components.append({'pixels':len(component),'box_half_open':box,'review_flag_only':len(component)>128 or box==[0,0,16,16]})
        frames.append({'frame':i,'alpha_histogram':dict(Counter(frame.getchannel('A').getdata())),'components_4_connected':components})
    diagnostics.append({'path':f'renderer-successor/assets/{name}','sha256':sha(f'renderer-successor/assets/{name}'),'size':list(image.size),'frames':frames})
save('alpha-diagnostics.json',{'measurements':diagnostics,'scope':'Nonzero-alpha 4-connected components; alpha-zero RGB ignored. Flag alone never rejects a matte, backing, margin, AA or artwork. Visual review decides intended exterior.'})

# These obligations and alternatives are the calling agent's own comparison.
def reason(c):
    q=c['criterion']; key=q.split('.q.')[1];stage=c['stage']
    if key=='geometry':
        return (('BRIEF.md:3 fixes four horizontal16px frames at100ms; source view supplies frame counts and renderer supplies slicing.' if stage=='working' else 'BRIEF.md:3,7 and src/queue-view.ts:5-7 require the static status in a16px cell.'), 'Required canvas/layout; renderer mechanism observed. No in-cell margin prohibition.', 'A 64x16 Working sheet with generous transparent in-cell margins passes; an extra gutter changes slice coordinates and fails for a source-supported reason. Static members may likewise retain margins.', 'Clarified geometry retained. Normal advance explicitly no-preference; reduced frame0 retains four-cell source geometry.')
    if key=='transparent-exterior':
        return ('BRIEF.md:3 requires transparent backgrounds; adopted style keeps transparency/full alpha, with no fixed palette or binary-alpha requirement.', 'Visual obligation plus a separate observational diagnostic; full alpha and selective AA remain permitted.', 'A deliberate broad backing shape with transparent exterior may trigger the occupancy flag but can pass visual review; a thin unintended gray matte must fail appearance even if a diagnostic misses it.', 'Keep split measured histogram/component record and deciding visual check. Alpha-zero magenta RGB does not make Paused opaque.')
    if key=='frame-assembly':
        return ('FOCUSED-SUCCESSOR.md:29-42 allows reviewed existing art; authoring construction policy only binds that chosen join/rotation path.', 'Reuse is a reviewed expert implementation choice; byte identity establishes provenance, not new provider execution.', 'A copied existing accepted sheet needs no new join/patch or generated frames. A redesigned expressive motion could be valid but would require a new reviewed construction.', 'Replace construction-only obligations with exact-byte copy checks for this successor; retain original policy/requests unchanged and explicitly non-applicable to reuse.')
    if key=='activity-not-success':
        return ('BRIEF.md:3 requires activity without success; AUTHORING-UPDATE.md:2-5 requires stationary Working distinct from Ready/Paused.', 'Owner outcomes; frame0 and the broken orbital motif are specialist choices. Start/Retry distinction is shared-consumer inference.', 'Another existing frame or dedicated pending ellipsis could satisfy the stationary requirement; paired pause bars cannot satisfy Working-vs-Paused distinction.', 'Adopt frame0 locally after actual native/3x, grayscale and renderer comparison; do not promote it to a universal owner motif.')
    if key=='motion-continuity':
        return ('BRIEF.md:3 fixes four100ms frames and activity; contract adds stable anchor/volume quality assessment.', '100ms is required timing; even angular pacing/no near-hold is expert quality for this rotating design only.', 'A source-conforming expressive hold with valid100ms frame cadence might pass the brief but fail this narrower expert construction; changing design requires review rather than rewriting the owner requirement.', 'Keep explicit normal-motion scope and wrap review; freeze tested separately. Browser sample sequence supports functional playback; human real-time temporal appraisal remains limited.')
    if key=='style-coherence':
        return ('BRIEF.md:3 requires readable silhouettes/cool blue, no fixed palette; scoped caller style decision carries exact Ready baseline, deliberate clusters/stepped edges.', 'Required original outcome plus adopted consumer style. Visual judgment; no identical weight/stroke/footprint rule.', 'A lighter thin pause mark or selective-AA curve can be coherent despite different weight, dimensions of occupied shape and alpha values.', 'Keep outcome-based style check, full alpha and selective AA; inspected actual small and enlarged family, not a numeric palette/stroke test.')
    if key=='consumers':
        transition={'working':'started -> running','retry':'error -> failed','paused':'pause -> paused'}[stage]
        return (f'src/queue.ts:1-4 maps {transition}; src/queue-view.ts:2-11 shares statusVisuals between both consumers. FOCUSED-SUCCESSOR authorizes versioned destination; changed PLAR requires stationary Working.', 'Required consumer mapping; new destinations are caller-adopted local successor, not historical render.choice.destination migration.', 'A renderer freezing one consumer but leaving compactStatus animated fails shared mapping. Renaming backend running to paused to suppress motion would violate state meaning.', 'Keep actual browser/live route. All20 state/scale views and all5 event mappings checked; working preference switches both ways with>800ms stationary evidence.')
    if key in ['retry-meaning-without-color','pause-meaning-without-color']:
        return ('BRIEF.md:3 requires Retry distinguishable without color alone; :7 explicitly separates Paused from activity/completion/retry; shared status set contains preserved Start.', 'Owner non-color distinction; Start comparison is consumer inference. No owner arrow/pause-bar recipe.', 'A readable non-arrow retry symbol or non-bar paused symbol can pass; similar blue hue alone cannot establish or defeat distinction.', 'Keep qualitative shape comparison against every Working frame and stationary0. Actual grayscale views distinguish connected Retry arrow, disconnected Working arcs, check and pause bars.')
    if key=='continuity':
        return ('BRIEF.md:3 asks coherent pixel-art family, adopted Ready style scopes comparison; normal loop and reduced stationary mode both need readability.', 'Collective visual obligation and expert continuity assessment, not identical weight.', 'Paused can have longer tall bars than Ready check or thinner Working segments while retaining coherent blue stepped craft; mandatory identical footprint would wrongly reject it.', 'Keep readable coherent weight without comparable/identical thickness constraint; normal playback scoped separately from stationary reduced case.')
    if key=='distinction':
        return ('BRIEF.md:3,7 gives activity-not-success and Retry/Paused non-color outcomes; changed PLAR adds stationary Working distinct from Ready/Paused.', 'Owner outcomes plus explicit shared-consumer inference for Start; grayscale is an adopted comparison method.', 'Static Working arcs and connected Retry arrow may share orbital direction but remain shape-distinct; copying Ready check into Working would fail regardless of label.', 'Keep all frames, normal loop and stationary0 in comparison; frame0 visually distinct from Ready/Paused with Working label. Start inference is labelled, not falsely attributed to preserve-vector wording.')
    if key=='destination':
        return ('FOCUSED-SUCCESSOR.md requires untouched old src/renderer, new successor destination, same backend and both consumers, media preference changes and actual render evidence.', 'Assignment-mandated versioned implementation and destination evaluation; historical destination choice is not rebound.', 'A code-only mapping or screenshot without real state events cannot establish integration. Changing global preference or old source would violate scope.', 'Local successor destination adopted after fresh actual browser/pixel review. UDL generation retention/acceptance remains separate and unresolved; no acceptance transfer.')
    raise AssertionError(q)

rows=[]
for c in proposal['criteria']:
    old=originals[c['criterion']]
    assert c['record_sha256']==old['record_sha256']
    # Historical literal is retained without silently editing any Q.
    oldcheck=old.get('check',old.get('fields',{}).get('ck'))
    if oldcheck is not None: assert c['original_check']==oldcheck
    obligation,authority,alternative,disposition=reason(c)
    rows.append({'criterion':c['criterion'],'record_sha256':c['record_sha256'],'original_literal':c['original_check'],'prior_r2_literal':c['prior_r2_check'],'successor_checks':c['successor_checks'],'source_obligation':obligation,'authority_basis':authority,'scope':f"{c['stage']} successor reuse, same consumer family; original Q unmodified",'literal_delta':disposition,'discriminating_alternative':alternative,'disposition':'consistent for locally reviewed successor; '+disposition})
save('caller-comparison.json',{'reviewer_role':'Independent native calling agent /root, not PIXL self-review','review_scope_sha256':original['review_scope_sha256'],'reviewed_proposal':{'path':'work/focused-successor/specialist-proposal-r3.json','sha256':sha('work/focused-successor/specialist-proposal-r3.json')},'criterion_comparisons':rows,'status':'consistent','adoption_scope':'Local versioned successor source/renderer and exact reused bytes; not new UDL verdicts, provider success or lifecycle completion.','sources':'Shared index in exact specialist proposal, plus actual opened brief, source backend/view, current selected requirement, actual source/renderer implementation, prior caller D1-D4 and actual composited/rendered images.','corrections_requested':['r1 unconditional animation advance corrected in r2/r3 to normal only, retaining old proposals','r2 confirmed destination wording corrected in r3 to caller-reviewed proposal pending adoption'],'prior_corrections_verified':{'D1':'Alpha measurements remain diagnostic; deciding check visual.','D2':'100ms owner cadence separated from expert even pacing/no near-hold.','D3':'Coherence imposes no identical/comparable footprint or weight.','D4':'Start distinction attributed to shared consumer inference.'},'art_decision':{'choice':'Adopt frozen Working frame0 for this labelled UI in reduced mode','basis':'Three disconnected stepped orbital segments remain clearly unlike asymmetrical Ready check and paired Paused bars at native/3x and in grayscale; connected Retry arrow and Start triangle remain distinct. Other frames would also be plausible, frame0 gives deterministic entry.','limits':'Static spinner may suggest waiting/stall; this is scoped to visible Working label. No new AI quality claim; no transferred acceptance.'},'verification':{'mechanical':'pixel-check-02.json and motion-check.json','visual':'Actual host-opened specialist-native-3x.png, specialist-grayscale.png, render-01 destination/reduced-live; final render-02 screenshot also opened before final result. Native-size assets included in views; no universal motif/alpha/palette recipe.','temporal_limit':'Actual browser animation executed and all phases sampled; host image viewer displays stills. Human real-time temporal playback appraisal not asserted.'},'remaining':'Supported retained-generation revision for reuse-only connected plan with existing PLAR links; no new criterion acceptance published.'})
save('visual-review.json',{'reviewer':'/root independent caller','viewed':['specialist-native-3x.png','specialist-grayscale.png','render-01/destination.png','render-01/reduced-live.png'],'outcomes':{'stationary_meaning':'pass scoped to labelled Working: segmented orbit, not check or bars','matte':'pass visually: intended exterior shows dark panel, no visible rectangular matte/halo','coherence':'pass scoped: blue stepped compact symbols, deliberately different occupied weights','non_color_distinction':'pass for displayed native/3x all frames, check, arrow and bars','temporal':'Browser executed actual rAF, sample crops show four phases and wrap; still host views limit direct human temporal appraisal.'},'old_concern_correction':'Raw Paused image display showed hidden magenta RGB; compositing plus alpha proves those pixels transparent. Concern not treated as a failure or edited away from specialist history.','no_new_provider_execution':True,'udl_acceptance_published':False})
print(json.dumps({'criteria':len(rows),'pixels':pixels['status'],'motion':motion_results},ensure_ascii=False))
