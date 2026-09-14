"""Project-local PIXL planning and reference measurement. Never generates artwork."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from collections import Counter
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / '.agents/skills/pixl-kit/scripts/pixl.py'
STORE = ROOT / '.pixl'

def cli(*args):
    result = subprocess.run([sys.executable, str(RUNNER), *map(str, args)], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout

def dump(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def ref(value): return {'$ref': value}
def sym(value): return {'$symbol': value}
def refs(*values): return [ref(value) for value in values]

def publish(doc, name):
    current = json.loads(cli('validate', STORE / 'state.px', '--root', ROOT))
    dump(f'.pixl/adapters/{name}.json', doc)
    candidate = ROOT / f'.pixl/candidates/{name}.px'
    candidate.parent.mkdir(parents=True, exist_ok=True)
    cli('encode', ROOT / f'.pixl/adapters/{name}.json', '--out', candidate)
    validated = json.loads(cli('validate', candidate, '--root', ROOT))
    dump(f'evidence/{name}-validation.json', validated)
    result = json.loads(cli('commit', STORE, candidate, '--expect', current['hash'], '--root', ROOT))
    dump(f'evidence/{name}-commit.json', result)
    print(json.dumps(result))

def plan():
    doc = json.loads(cli('decode', STORE / 'state.px'))
    assert doc['revision'] == 0, 'Intake planning is a one-time step.'
    doc['revision'] = 1
    records = doc['records']
    def add(id_, kind, **fields): records.append({'id': id_, 'kind': kind, 'fields': fields})
    def source(id_, path, lines=None):
        add(id_, 'S', ur=path, dg=digest(path), ln=lines or [], at='2026-09-11', au=sym('local'))
    source('s.brief', 'evidence/brief.txt', [1,3])
    source('s.reference_a', 'reference.png')
    source('s.reference_b', 'reference-b.png')
    base = '.agents/skills/pixl-kit/resources/'
    source('s.clusters', base+'training/original-docs/PIXEL-ART-DEEP-RESEARCH.md', [857,867])
    source('s.motion', base+'training/original-docs/PIXEL-ART-DEEP-RESEARCH.md', [1563,1573])
    source('s.edges', base+'training/original-docs/PIXEL-ART-DEEP-RESEARCH.md', [1402,1431])
    source('s.archive', base+'training/original-docs/PIXEL-ART-ASSETS.md', [11,15])
    source('s.methods', base+'knowledge/pixel-art.json')
    source('s.applicability', base+'knowledge/applicability.json')
    source('s.fixture_receipt', base+'evidence/art-methods/poc-report.json')
    for suffix, path in [('a','reference.png'),('b','reference-b.png')]:
        add('x.reference_'+suffix, 'X', nm=path, ur=path, dg=digest(path), kd=sym('reference'), mt={'origin':'user-supplied reference', 'source':ref('s.reference_'+suffix)})
    choices = []
    def choice(id_, key, status, value, why, sources=('s.brief',), owner='user'):
        add(id_, 'I', pr=ref('project'), wh=ref(owner), ky=key, st=sym(status), vl=value, so=refs(*sources), wy=why)
        choices.append(ref(id_))
    choice('i.members','family_members','confirmed',['scout','medic'],'The user explicitly names both roles.')
    choice('i.view','vw','confirmed',sym('side'),'The user specifies a side-view game; these references do not establish an in-game facing direction.')
    choice('i.canvas','px','unresolved',None,'The user has not chosen the final canvas. The 32x32 source dimensions do not confirm output dimensions.')
    choice('i.outline','edge_treatment','conflict',['dark contour in reference.png','turquoise edge without a separate dark contour in reference-b.png'],'The user identifies disagreement; both alternatives are preserved pending a representative comparison.',('s.brief','s.reference_a','s.reference_b'))
    choice('i.pose','sample_pose','proposed','one right-facing idle scout pose','A single pose limits initial work and tests a side-view silhouette; direction and animation scope are not confirmed.',owner='actor')
    choice('i.role_design','role_landmarks','proposed',{'scout':'compact forward hood or visor and slim rear utility pack','medic':'shared body proportions with a wider medical satchel and a light band or badge'},'Use equipment silhouettes as proposed role cues while retaining the references\' turquoise body and pale feature language; no role detail has been approved.',('s.brief','s.reference_a','s.reference_b'),owner='actor')
    choice('i.trial_canvas','trial_canvas','proposed',[32,32],'32x32 is a useful first trial because both references use it. This is neither a final size nor a concrete raster contract.',('s.reference_a','s.reference_b'),owner='actor')
    choice('i.palette','palette_policy','unresolved',None,'Source colors can be measured, but permitted new role colors and exact palette limits are unspecified.')
    choice('i.alpha','al','unresolved',None,'Source transparency can be measured; output alpha policy remains a separate choice.')
    choice('i.light','lighting','unresolved',None,'Flat references do not establish a shading direction or ramp policy.')
    choice('i.engine','destination_engine','unresolved',None,'No target engine, project, version, or import scene is supplied.')
    choice('i.display','display_scale_backgrounds','unresolved',None,'No gameplay backgrounds or intended display scale are supplied; neutral review backgrounds are diagnostic only.')
    choice('i.animation','animation_scope','unresolved',None,'Actions, directions, frame counts and timing are not specified. The first proposed proof is static.')
    choice('i.pivot','pivot','unresolved',None,'Establish a shared ground contact and pivot after the representative pose and canvas are chosen.')
    for rec in records:
        if rec['id']=='project':
            rec['fields']['in']=choices
            rec['fields']['sc']=refs('s.brief','s.reference_a','s.reference_b')
    add('k.silhouette_candidate','K',nm='Candidate silhouette-readability method; no project adoption',ap=[sym('characters_25d939ff')],rq=['Intended viewing scale, representative backgrounds and identity landmarks'],op=['Render a flat opaque mask before detailing.','Inspect major proportions, negative spaces and landmark separation at native logical scale.','Compare the colored asset on representative light, dark and busy backgrounds.'],ck=['Named identity landmarks remain visible at the target size.','Required gaps stay open and interactive forms separate from their surroundings.'],rk=['Silhouette alone cannot validate faces, materials or fine symbols.','No contrast ratio or component count proves aesthetic quality.','Bundled key fixture is not a scout or medic proof.'],so=refs('s.methods','s.applicability','s.clusters','s.motion','s.archive','s.fixture_receipt'))
    add('k.edge_candidate','K',nm='Candidate edge-rhythm method; no project adoption',ap=[sym('hard_silhouettes_99485584')],rq=['A contour mask and declared intentional corners or irregular regions'],op=['Trace boundary runs and highlight sudden run-length changes.','Regularize only contours intended to read as smooth.','Preserve corners, damage and organic asymmetry identified in the brief.'],ck=['A supplied straight diagonal retains its declared repeating step pattern.','No protected corner changes during cleanup.'],rk=['Not every uneven run is a jaggy.','This method does not choose dark versus body-colored outlines.','The bundled staircase fixture cannot establish this character family\'s appearance.'],so=refs('s.methods','s.applicability','s.edges','s.clusters','s.fixture_receipt'))
    def criterion(id_, name, domain, mode, condition, sources=('s.brief',)):
        add(id_,'Q',nm=name,dm=sym(domain),md=sym(mode),ck=condition,wh=ref('actor'),so=refs(*sources))
    criterion('q.analysis_numbers','Measured reference properties','mechanical','local','The report records each input hash, actual canvas, alpha, palette, occupied bounds and cross-reference differences, and does not imply output style confirmation.',('s.brief','s.reference_a','s.reference_b'))
    criterion('q.analysis_look','Reference inspection','visual','visual','Inspect both actual inputs at native scale and integer enlargement; describe shared forms and conflicting edge treatment separately from proposed role designs.',('s.brief','s.reference_a','s.reference_b'))
    criterion('q.research','Source-grounded applicability','other','local','Retain method IDs, exact source hashes and line ranges, relevant quoted text, applicability and unresolved prerequisites, bounded fixture limitations, and the smallest next project proof.',('s.brief','s.methods','s.applicability','s.clusters','s.motion','s.edges','s.archive','s.fixture_receipt'))
    criterion('q.style','Resolved trial scope','other','local','Record the chosen or explicitly proposed trial canvas, one resolved edge alternative per trial contract, role landmarks, alpha, color and lighting interpretation, facing and intended review backgrounds; preserve final choices that remain undecided.')
    criterion('q.file','Raster mechanics','mechanical','local','The actual PNG matches its saved concrete canvas and applicable alpha/palette contract; content is not clipped and any proposed ground anchor is recorded.')
    criterion('q.readability','Native role and style readability','visual','visual','Inspect the actual sprite at native scale and integer zoom on declared test backgrounds. Its role cues remain legible, shared body/features resemble the selected reference interpretation, and edges follow its saved trial contract. Diagnostic backgrounds cannot establish gameplay contrast.')
    criterion('q.scout','Scout landmarks','visual','visual','Identify the scout by the agreed equipment and stance without relying only on a color swap; preserve readable separation between face, body and equipment.')
    criterion('q.medic','Medic landmarks','visual','visual','Identify the medic by the agreed satchel and badge or band; retain shared body proportions, feature placement and ground contact against the accepted scout baseline.')
    criterion('q.family','Collective family continuity','continuity','visual','Compare actual scout and medic with the still-nominated sample at native size and integer zoom; shared scale, body volume, feature placement, ground contact, palette interpretation and outline treatment agree while role silhouettes remain distinct.')
    criterion('q.engine','Destination import','engine','live','In the supplied target engine/project, inspect imported member sprites for intended sampling, display scale, transparency and shared pivot/contact; verify slicing and timing only if animation enters scope. Record actual engine version and test scene.')
    def task(id_, name, phase, state, deps, output, inputs=(), knowledge=()):
        add(id_,'T',nm=name,ow=ref('actor'),pr=ref('project'),dp=refs(*deps),dc=[],kn=refs(*knowledge),st=sym(state),ph=sym(phase),ip=refs(*inputs),op=refs(output),ca=[],vr=[])
    def output(id_, task_id, name, kind, criteria):
        add(id_,'F',tk=ref(task_id),nm=name,kd=sym(kind),rq=refs(*criteria))
    inputs=('x.reference_a','x.reference_b')
    task('t.inspect','Inspect and compare supplied references','research','active',(),'f.analysis',inputs)
    output('f.analysis','t.inspect','Reference analysis and comparison viewer','report',('q.analysis_numbers','q.analysis_look'))
    task('t.research','Assess silhouette and edge methods against actual source text','research','active',(),'f.research',inputs,('k.silhouette_candidate','k.edge_candidate'))
    output('f.research','t.research','Applicable methods, limits and representative proof plan','report',('q.research',))
    task('t.style','Resolve trial outline and canvas interpretation','research','blocked',('t.inspect','t.research'),'f.style',inputs)
    output('f.style','t.style','Trial style interpretation; final unknowns retained','report',('q.style',))
    task('t.scout','Produce and inspect a representative scout pose','sample','open',('t.inspect','t.research','t.style'),'f.scout',inputs,('k.silhouette_candidate',))
    output('f.scout','t.scout','Scout representative side-view idle sprite','sprite',('q.file','q.readability','q.scout'))
    task('t.medic','Extend the accepted scout sample into the medic','production','open',('t.scout',),'f.medic',inputs,('k.silhouette_candidate',))
    output('f.medic','t.medic','Medic side-view idle sprite','sprite',('q.file','q.readability','q.medic'))
    task('t.delivery','Bind accepted baseline and members, compare family and test import','delivery','blocked',('t.scout','t.medic'),'f.delivery')
    output('f.delivery','t.delivery','Scaffold for retained scout and medic family delivery','report',('q.family','q.engine'))
    add('n.handoff','N',wh=ref('actor'),fo=refs('i.canvas','i.outline','i.engine','f.scout','f.medic','f.delivery'),nx=refs('t.inspect','t.research'),bl=refs('t.style','t.scout','t.medic','t.delivery'),rv=1)
    publish(doc,'r1-plan')

def measure():
    result={'observed_at':datetime.now(timezone.utc).isoformat(),'purpose':'Inspection of supplied references; no generated character or final style adoption.','references':[]}
    images=[]
    for name in ['reference.png','reference-b.png']:
        measurement=json.loads(cli('asset-check',ROOT/name))
        im=Image.open(ROOT/name).convert('RGBA')
        images.append(im)
        colors=Counter(p for p in im.get_flattened_data() if p[3])
        measurement['palette_rgba_counts']={'#'+''.join(f'{c:02x}' for c in pixel):count for pixel,count in sorted(colors.items())}
        measurement['path']=name
        result['references'].append(measurement)
    a,b=images
    result['comparison']={'same_canvas':a.size==b.size,'same_alpha_mask':a.getchannel('A').tobytes()==b.getchannel('A').tobytes(),'changed_rgba_pixels':sum(x!=y for x,y in zip(a.get_flattened_data(),b.get_flattened_data()))}
    transitions=Counter((x,y) for x,y in zip(a.get_flattened_data(),b.get_flattened_data()) if x!=y)
    result['comparison']['color_transitions']=[{'from':list(x),'to':list(y),'pixels':n} for (x,y),n in transitions.items()]
    dump('evidence/reference-measurements.json',result)
    board=Image.new('RGB',(800,416),'#e8e6de')
    draw=ImageDraw.Draw(board)
    draw.text((16,12),'SUPPLIED REFERENCES - inspection only, no new sprites',fill='#172433')
    for idx,(im,label) in enumerate(zip(images,['A: reference.png','B: reference-b.png'])):
        x=16+idx*400
        draw.text((x,40),label,fill='#172433')
        draw.text((x,62),'Native 32 x 32',fill='#172433')
        board.paste(im,(x,82),im)
        draw.text((x+68,62),'8x nearest-neighbor inspection',fill='#172433')
        board.paste(im.resize((256,256),Image.Resampling.NEAREST),(x+68,82),im.resize((256,256),Image.Resampling.NEAREST))
        draw.text((x,364),'Source size does not choose the output canvas.',fill='#172433')
    board.save(ROOT/'evidence/reference-comparison.png')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    {'plan':plan,'measure':measure}[sys.argv[1]]()
