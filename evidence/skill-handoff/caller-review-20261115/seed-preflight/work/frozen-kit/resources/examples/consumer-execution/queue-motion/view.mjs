// Protocol promoted from the retained CF-03 renderer-artistic/view.mjs.
// Consumer modules own descriptors, timing and frame selection. No case source rewriting.
const errors = [];
function unavailable(error) { errors.push(String(error)); window.queueUnavailable=String(error); document.body.dataset.ready='true'; }
window.addEventListener('error', e => unavailable(e.message));
window.addEventListener('unhandledrejection', e => unavailable(e.reason));
const config = await (await fetch('/config.json')).json();
const stateModule = await import('/' + config.modules.state);
const view = await import('/' + config.modules.view);
const {stateAfter} = stateModule;
const {statusVisuals, statusCell, compactStatus, display, reducedMotionQuery, motionPreference, frameAt} = view;
const sessionId = crypto.randomUUID();
const absent = ['statusCell','compactStatus','motionPreference','frameAt'].filter(k => typeof view[k] !== 'function');
if (typeof stateAfter !== 'function') absent.push('stateAfter');
if (!display || !Array.isArray(display.cell) || display.cell.length !== 2 || display.cell.some(x => !Number.isInteger(x) || x < 1 || x > 256) || !Number.isFinite(display.frameMs) || display.frameMs <= 0 || display.filter !== 'nearest' || !CSS.supports('color', display.background)) absent.push('display contract');
if (!statusVisuals || typeof reducedMotionQuery !== 'string') absent.push('statusVisuals/reducedMotionQuery');
if (absent.length) {
  window.queueUnavailable = 'Missing queue-motion-v1 capabilities: ' + absent.join(', ');
  document.body.dataset.ready = 'true';
} else {
  const consumers = {statusCell, compactStatus}, media = matchMedia(reducedMotionQuery);
  let motion = motionPreference(media), origin = performance.now(), liveCells = [], active = null;
  const initialMotion = motion, preferenceEvents = [], reconciliations = [], transitions = [], cells = [], assets = new Map();
  document.documentElement.style.setProperty('--panel', display.background);
  const digest = async bytes => [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(x => x.toString(16).padStart(2,'0')).join('');
  async function imageFor(path) {
    if (!/^assets\//.test(path) || path.includes('\\') || path.split('/').some(x => !x || x === '..' || x === '.')) throw new Error('Descriptor path must be a canonical assets path');
    if (!assets.has(path)) assets.set(path, (async () => {
      const response = await fetch('/' + path);
      if (!response.ok) return {available:false,path,status:response.status};
      const data = await response.arrayBuffer(), image = new Image(), url = URL.createObjectURL(new Blob([data],{type:response.headers.get('Content-Type')}));
      try { image.src = url; await image.decode(); } finally { URL.revokeObjectURL(url); }
      return {available:true,path,image,sha256:await digest(data),width:image.naturalWidth,height:image.naturalHeight};
    })());
    return assets.get(path);
  }
  function descriptorFor(consumer,state) {
    const d = consumers[consumer](state,motion);
    if (!d || !Number.isInteger(d.frames) || d.frames < 1 || d.frames > 64 || typeof d.animate !== 'boolean' || d.motion !== motion || (!d.animate && (!Number.isInteger(d.holdFrame) || d.holdFrame < 0 || d.holdFrame >= d.frames))) throw new Error('Unsupported consumer descriptor');
    return {...d};
  }
  function paint(cell,elapsed,at) {
    const {canvas,asset,descriptor:d,scale} = cell, [w,h] = display.cell;
    const frame = frameAt(d,elapsed);
    if (!Number.isInteger(frame) || frame < 0 || frame >= d.frames) throw new Error('Consumer frameAt returned an invalid frame');
    if (canvas) {
      const ctx = canvas.getContext('2d'); ctx.imageSmoothingEnabled = display.filter !== 'nearest';
      ctx.fillStyle = display.background; ctx.fillRect(0,0,canvas.width,canvas.height);
      ctx.drawImage(asset.image,frame*w,0,w,h,0,0,w*scale,h*scale);
    }
    cell.frame = frame; cell.paintElapsed = elapsed; cell.paintAt = at;
  }
  async function makeCell(consumer,state,scale) {
    const descriptor = descriptorFor(consumer,state), asset = await imageFor(descriptor.path), [w,h] = display.cell;
    const node = document.createElement('div'); node.className = 'cell ' + (consumer === 'compactStatus' ? 'compact' : '');
    const geometryMatches = asset.available && asset.width === w*descriptor.frames && asset.height === h;
    const canvas = geometryMatches ? document.createElement('canvas') : null;
    if (canvas) { canvas.width=w*scale; canvas.height=h*scale; node.append(canvas); }
    const label = document.createElement('span'); label.textContent=descriptor.label; node.append(label);
    const cell = {consumer,state,scale,descriptor,asset,geometryMatches,canvas,node}; paint(cell,0,performance.now()); return cell;
  }
  const snapshot = c => ({consumer:c.consumer,state:c.state,scale:c.scale,descriptor:{...c.descriptor},asset:{...c.asset,image:undefined},geometryMatches:c.geometryMatches,frame:c.frame,paintAt:c.paintAt,paintElapsed:c.paintElapsed,expectedFrame:frameAt(c.descriptor,c.paintElapsed),smoothing:c.canvas?.getContext('2d').imageSmoothingEnabled,imageRendering:c.canvas ? getComputedStyle(c.canvas).imageRendering : null,png:c.canvas?.toDataURL()});
  const keys = () => Object.keys(consumers).flatMap(consumer => config.scales.map(scale => ({consumer,scale})));
  for (const state of Object.keys(statusVisuals)) {
    const heading=document.createElement('div'); heading.className='state'; heading.textContent=state; document.querySelector('#matrix').append(heading);
    for (const {consumer,scale} of keys()) { const cell=await makeCell(consumer,state,scale); cells.push(cell); document.querySelector('#matrix').append(cell.node); }
  }
  async function select(event) {
    const state = event === 'idle' ? 'idle' : stateAfter(event);
    if (!statusVisuals[state]) throw new Error('Queue event did not resolve a visual state: ' + event);
    liveCells=await Promise.all(keys().map(({consumer,scale}) => makeCell(consumer,state,scale)));
    document.querySelector('#live').replaceChildren(...liveCells.map(c=>c.node)); origin=performance.now();
    const t={event,state,motion,sessionId,at:origin,consumers:liveCells.map(snapshot)}; transitions.push(t); return t;
  }
  // Reconcile from the source descriptor, including source-selected assets and held frame.
  let reconciling=Promise.resolve();
  media.addEventListener('change', () => {
    const from=motion; motion=motionPreference(media); const at=performance.now();
    const event={from,to:motion,matches:media.matches,at,sessionId}; preferenceEvents.push(event);
    reconciling=reconciling.then(async()=>{
      const repainted=[];
      for (const c of [...cells,...liveCells]) {
        c.descriptor=descriptorFor(c.consumer,c.state); c.asset=await imageFor(c.descriptor.path);
        c.geometryMatches=c.asset.available && c.asset.width===display.cell[0]*c.descriptor.frames && c.asset.height===display.cell[1];
        if (!c.geometryMatches) throw new Error('Preference change has unavailable geometry');
        paint(c,liveCells.includes(c) ? performance.now()-origin : 0,performance.now()); repainted.push({...snapshot(c),live:liveCells.includes(c)});
      }
      reconciliations.push({...event,repainted});
    });
  });
  await select('started');
  function animate(now) {
    try {
      for (const c of liveCells) if (c.descriptor.animate) paint(c,now-origin,now);
      if (active) active.observe(now);
    } catch(error) { errors.push(String(error)); if(active) active.finish('unavailable',String(error)); }
    requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);
  window.queueMotion=()=>({sessionId,motion,initialMotion,matches:media.matches,events:preferenceEvents.length,reconciliations:reconciliations.length});
  window.queueCapture=async name => {
    await reconciling;
    const phaseTransitions=[];
    for (const event of ['idle','started','pause','ok','error']) { phaseTransitions.push(await select(event)); await new Promise(requestAnimationFrame); }
    await select('started');
    const startedAt=performance.now(), samples=[], counts={};
    for (const c of liveCells) counts[c.consumer+'@'+c.scale]={frames:[],transitions:0,wraps:0,skips:0,last:null};
    const phase={name,motion,sessionId,initialMotion,startedAt,status:'unavailable',frameCount:liveCells[0]?.descriptor.frames,frameMs:display.frameMs,rafCount:0,counts,samples,transitions:phaseTransitions};
    return await new Promise(resolve=>{
      let timer;
      const finish=(status,reason)=>{
        if(!active)return; active=null; clearTimeout(timer);
        Object.assign(phase,{status,reason,endedAt:performance.now(),preferenceEvents:structuredClone(preferenceEvents),reconciliations:structuredClone(reconciliations),views:cells.map(snapshot),errors:[...errors]}); resolve(phase);
      };
      active={finish,observe(now){
        const current=liveCells.map(snapshot), changed=current.some(c=>counts[c.consumer+'@'+c.scale].last!==c.frame);
        // rAF's timestamp is the paint clock; actual capture is measured separately.
        const at=performance.now(); phase.rafCount++;
        for(const c of current){
          const x=counts[c.consumer+'@'+c.scale], n=c.descriptor.frames;
          if(!x.frames.includes(c.frame))x.frames.push(c.frame);
          if(x.last!==null && x.last!==c.frame){x.transitions++;if(c.frame!==(x.last+1)%n)x.skips++;else if(x.last===n-1&&c.frame===0)x.wraps++;}x.last=c.frame;
        }
        // Retain each painted frame transition, plus hold samples at a bounded cadence.
        if(changed || !samples.length || (motion==='reduced' && at-samples.at(-1).at>=50)) samples.push({at,elapsed:at-origin,cells:current});
        if(current.some(c=>!c.geometryMatches || !c.png)) { finish('unavailable','Missing consumer image or unsupported sheet geometry');return; }
        if(motion==='normal' && current.some(c=>!c.descriptor.animate || c.descriptor.frames<2)) {finish('unavailable','Running consumer lacks normal animation');return;}
        if(motion==='normal' && Object.values(counts).every(x=>x.frames.length===phase.frameCount && x.wraps>=config.observed_wraps && x.skips===0)) finish('observed','Observed consecutive frames and requested last-to-first wraps in every consumer/scale');
        if(motion==='reduced' && samples.length>1 && samples.at(-1).at-samples[0].at>=config.hold_ms) finish('observed','Observed source-held frame throughout the requested reduced-motion window');
      }};
      timer=setTimeout(()=>finish('timeout','Bounded phase timeout before required observed coverage'),config.phase_timeout_ms);
    });
  };
  window.queueInfo=()=>({sessionId,display,reducedMotionQuery,initialMotion,state_inventory:Object.keys(statusVisuals),views:cells.map(snapshot),errors:[...errors]});
  document.body.dataset.ready='true';
}
