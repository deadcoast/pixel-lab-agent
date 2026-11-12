import hashlib,json
from pathlib import Path
from PIL import Image

root=Path(__file__).resolve().parents[2]
out=root/'work/domain-consumers'
def read(p): return json.loads((root/p).read_text(encoding='utf-8-sig'))
def digest(p): return hashlib.sha256((root/p).read_bytes()).hexdigest()
def ref(p): return {'path':p,'sha256':digest(p)}
verified={}
def verify_refs(obj):
    if isinstance(obj,dict):
        p,h=obj.get('path'),obj.get('sha256')
        if p and h and (root/p).is_file():
            assert digest(p)==h,(p,'hash mismatch')
            verified[p]=h
        for v in obj.values(): verify_refs(v)
    elif isinstance(obj,list):
        for v in obj: verify_refs(v)

baseline=read('work/domain-consumers/caller-original-hashes.json')
for row in baseline: assert digest(row['path'])==row['sha256'],row['path']
operations={}
details={}
for domain in ['terrain','animation']:
    prefix=f'work/domain-consumers/{domain}-01/'
    result=read(f'work/domain-consumers/{domain}-result.json')
    internal=read(prefix+'result.json')
    assert {k:v for k,v in result.items() if k!='hash_domains'}==internal
    context=read(f'work/domain-consumer-inputs/{domain}-context.json')
    for k in ['state_hash','binding_hash']: assert result[k]==context[k]
    assert result['manifest']==context['candidate_file']
    assert result['status']=='complete' and result['renderer_executed']
    assert not result['state_changed'] and not result['state_written'] and not result['automatic_acceptance']
    assert result['cleanup']['complete']
    check=read(prefix+'check.json')
    assert check['pass'] and not check['failures']
    execution=read(prefix+'capture/execution.json')
    assert execution['cleanup']['complete'] and execution['browser_exit']['code']==0
    imported=read(prefix+'import/result.json')
    observation=read(prefix+'observation.json')
    capture=read(prefix+'capture/capture.json')
    assert imported['renderer_executed'] is False
    assert imported['files_verified'] and not imported['automatic_acceptance'] and not imported['state_changed']
    for k in ['state_hash','binding_hash','manifest']: assert imported[k]==result[k]
    for obj in [result,internal,check,execution,imported,observation,capture]: verify_refs(obj)
    assert read(prefix+'config.json')==read(f'work/domain-consumer-inputs/{domain}-config.json')
    operations[domain]=ref(f'work/domain-consumers/{domain}-result.json')
    details[domain]={'status':result['status'],'state_hash':result['state_hash'],'binding_hash':result['binding_hash'],'manifest':result['manifest'],'checks':ref(prefix+'check.json'),'check_summary':result['check_summary'],'cleanup':result['cleanup'],'execution':ref(prefix+'capture/execution.json'),'nf06':ref(prefix+'import/result.json'),'outer_renderer_executed':True,'nf06_renderer_executed':False,'observation':ref(prefix+'observation.json')}

specialist_path='work/domain-consumers/SPECIALIST-RESULT.json'
specialist=read(specialist_path)
verify_refs(specialist)
images=[]
for n in ['coverage','island']:
    for scale in [1,3]:
        for suffix in ['', '-destination']:
            images.append(ref(f'work/domain-consumers/terrain-01/capture/{n}-{scale}x{suffix}.png'))
for clip in ['idle','settle']:
    for scale in [1,3]:
        for frame in range(4):
            for kind in ['step','screen']:
                images.append(ref(f'work/domain-consumers/animation-01/capture/{kind}-{clip}-{scale}x-{frame}.png'))
terrain_pixels={str(n):[list(Image.open(root/f'assets/terrain/tile-{n}.png').getpixel(p)) for p in [(4,4),(12,4),(12,12),(4,12)]] for n in [6,7]}
alpha_boxes={str(n):list(Image.open(root/f'assets/motion/frame-{n}.png').getbbox()) for n in range(4)}
findings=[{'domain':'terrain','asset':ref('assets/terrain/tile-6.png'),'symptom':'NW quadrant is green where mask 6 requires water. The island left edge has two green teeth; mixed shoreline has corresponding broken material joins. Tile 6 duplicates correctly shaped tile 7.','context':'Island zero-based (column,row) cells (0,1),(0,2); coverage cells (3,0),(1,2),(5,6),(3,7),(5,7). Seen at 1x and nearest 3x.','likely_correction':'In a separately authorized revision, restore tile 6 NW quadrant to water.','preservation_scope':'Preserve tile 7, all other members, source mapping, dimensions, palette and metadata. No revision performed.','evidence':[ref('work/domain-consumers/terrain-01/capture/island-3x.png'),ref('work/domain-consumers/terrain-01/capture/coverage-3x.png')]},{'domain':'animation','asset':ref('assets/motion/frame-2.png'),'symptom':'Pose 2 shifts the entire figure down two native pixels; feet reach viewport row 29 instead of 27. It appears to sink below the established floor, then return. Same defect in idle and settle, at both scales (six display pixels at 3x).','context':'Fixed [8,14] pivots at anchor [20,28] correctly place the rectangle, but opaque foot pixels move.','likely_correction':'In a separately authorized revision, raise pose 2 pixel content two native pixels, preserving the intended arm pose and fixed pivot.','preservation_scope':'Preserve frames 0,1,3, palette, dimensions, transparency, pivots, anchors and durations [120,180,120,240]; no revision performed.','evidence':[ref('work/domain-consumers/animation-01/capture/step-idle-3x-2.png'),ref('work/domain-consumers/animation-01/capture/step-idle-3x-0.png')]}]
report={'native_child':{'id':'/root/pixl_qualification','agent_type':'pixl','fork_turns':'none','status':'completed','earlier_interrupted_child':'/root/domain_consumers (fork_turns all; interrupted and superseded before execution)'},'specialist_result':ref(specialist_path),'operations':operations,'viewed_images':images,'independent_checks':{'complete_saved_results_read':True,'export_matches_internal_result_except_public_hash_domains_annotation':True,'source_context_state_binding_manifest_match':True,'all_reported_existing_file_hashes_verified':True,'verified_file_count':len(verified),'details':details,'original_baseline':ref('work/domain-consumers/caller-original-hashes.json'),'original_files_checked':len(baseline),'all_original_hashes_unchanged':True,'exact_config_content_match':True,'pixel_probes':{'terrain_NW_NE_SE_SW':terrain_pixels,'animation_alpha_bbox_exclusive':alpha_boxes},'specialist_comparison':'Independent image inspection and read-only pixel probes agree: tile 6 NW material is wrong; pose 2 foot contact is two pixels lower. Mechanical checks and cleanup agree with the saved full results.'},'findings':findings,'production_unchanged':True,'acceptance_created':False,'scope':'Explicit TM-08 controlled diagnostic browser consumer qualification only. Two executions total; caller reused evidence without rerunning. Source, pixels, production state and installed kit remain unchanged. No candidate reviews, verdicts, nominations, acceptance, provider calls or installation.','mechanical_vs_visual':'Both scoped mechanical checks pass: terrain 4 pixel / 43 source / 0 clock checks; animation 58 pixel / 12 source / 244 clock checks. Idle observed two wraps at each scale; settle reached terminal frame at each scale. These do not establish visual continuity: both diagnostic families contain visible intent defects.','limitations':['Image-tool viewing was of saved stills, not subjective live playback; RAF samples establish scoped observed timing only.','No continuous video or proof of every display refresh.','NF-06 import consistency alone does not execute a renderer; outer execution receipts retain that evidence.','Controlled authored diagnostics do not establish generated production-art quality or another engine behavior.','M1/M2 and broader M3/M4 remain open. CF-09 actual generated-art correction/revision/exact-successor inspection and human acceptance remain open.'],'next_action':'Retain evidence for the two precise correction proposals. Any pixel revision and successor inspection require separate authorization; continue CF-09 real returned art independently. No acceptance requested or created.'}
(out/'CALLER-RESULT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'caller_result':ref('work/domain-consumers/CALLER-RESULT.json'),'original_files':len(baseline),'verified_evidence_files':len(verified),'viewed_images':len(images)}))

