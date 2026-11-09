from pathlib import Path
import shutil, json, hashlib

root = Path.cwd()
folder = root/'renderer-successor'
(folder/'assets').mkdir(exist_ok=False)
files = ['working.png','paused.png','ready-confirmed.png','error-retry.png','start.svg']
copied = []
for name in files:
    src = root/'assets'/name
    dst = folder/'assets'/name
    shutil.copyfile(src,dst)
    copied.append({'source':src.relative_to(root).as_posix(),'destination':dst.relative_to(root).as_posix(),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'equal':src.read_bytes()==dst.read_bytes()})
p=root/'src/queue-view-successor.ts'
p.write_text(p.read_text(encoding='utf-8').replace('"assets/', '"renderer-successor/assets/'),encoding='utf-8')
p=folder/'server.mjs'
s=p.read_text(encoding='utf-8').replace("!pathname.startsWith('/assets/')", "!pathname.startsWith('/assets/') && !pathname.startsWith('/renderer-successor/assets/')")
p.write_text(s,encoding='utf-8')
p=folder/'capture.mjs'
s=p.read_text(encoding='utf-8')
s=s.replace("await call('Page.navigate'", "await call('Emulation.setEmulatedMedia', { features: [{name: 'prefers-reduced-motion', value: 'no-preference'}] }, sessionId);\n  await call('Page.navigate'",1)
needle="  const layout = await call('Page.getLayoutMetrics', {}, sessionId);"
insert='''  const evaluate = async expression => {
    const value = await call('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true }, sessionId);
    if (value.exceptionDetails) throw new Error(JSON.stringify(value.exceptionDetails));
    return value.result.value;
  };
  const settle = 'new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve(true))))';
  const phases = [];
  await evaluate("window.selectQueue('started')");
  async function samplePhase(name, reduced) {
    await call('Emulation.setEmulatedMedia', {features:[{name:'prefers-reduced-motion',value:reduced?'reduce':'no-preference'}]}, sessionId);
    await evaluate(settle);
    const samples=[];
    for (let i=0;i<24;i++) {
      samples.push(await evaluate('window.motionSnapshot()'));
      await new Promise(resolve=>setTimeout(resolve,25));
    }
    const screenshot=await call('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false},sessionId);
    await writeFile(join(out,`${name}.png`),Buffer.from(screenshot.data,'base64'));
    phases.push({name,reduced,samples,screenshot:{path:`${name}.png`,sha256:hash(Buffer.from(screenshot.data,'base64'))}});
  }
  await samplePhase('normal-before',false);
  await samplePhase('reduced-live',true);
  const reducedReport = await evaluate('window.captureQueue()');
  await writeFile(join(out,'reduced-render.raw.json'),JSON.stringify(reducedReport,null,2)+'\\n');
  await evaluate("window.selectQueue('started')");
  await samplePhase('normal-after',false);
  let motionIndex=0;
  for (const phase of phases) for (const sample of phase.samples) for (const cell of sample.cells) if(cell.png) {
    const bytes=Buffer.from(cell.png.split(',')[1],'base64');
    const name=`motion-${String(motionIndex++).padStart(3,'0')}.png`;
    await writeFile(join(out,name),bytes); cell.image={path:name,sha256:hash(bytes)};delete cell.png;
  }
  await writeFile(join(out,'motion.json'),JSON.stringify({phases,scope:'Real requestAnimationFrame samples, actual matchMedia media preference changes through CDP in same page; observed wall-clock sample times are retained, not exact scheduling guarantees.'},null,2)+'\\n');
  await evaluate("window.selectQueue('ok')");
  await evaluate(settle);
'''
assert needle in s
s=s.replace(needle,insert+needle)
p.write_text(s,encoding='utf-8')
(root/'work/focused-successor/reuse-copy.json').write_text(json.dumps(copied,indent=2)+'\n',encoding='utf-8')
print(json.dumps(copied))
