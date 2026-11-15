// Own only the loopback server, CDP connection and freshly allocated browser profile.
import {spawn} from 'node:child_process';
import {access,mkdir,readFile,writeFile,mkdtemp,realpath,rm} from 'node:fs/promises';
import {resolve,join,relative,sep,basename} from 'node:path';
import {tmpdir} from 'node:os';
import {serve,rendererRoot,profileFiles,hash,validateConfig} from './server.mjs';

const options={};
for(let i=2;i<process.argv.length;i+=2){const key=process.argv[i];if(!['--project','--out','--config','--browser'].includes(key)||options[key]||!process.argv[i+1])throw new Error('Expected --project ROOT --out FRESH_DIRECTORY --config FILE [--browser PATH]');options[key]=process.argv[i+1];}
if(!options['--project']||!options['--out']||!options['--config'])throw new Error('Project, fresh output and config are required');
const project=await realpath(resolve(options['--project'])),out=resolve(options['--out']);
await mkdir(out,{recursive:false});
const execution={version:1,profile:'queue-motion-v1',project,status:'unavailable',renderer_executed:false,started_at:new Date().toISOString(),cleanup:{complete:false},limitations:['Isolated browser profile and loopback fixture; this is not an operating-system sandbox or artistic acceptance.']};
let config,browser=options['--browser'],profile,profileParent,running,child,socket,exitCode=null,launchError=null,report;
let stdout='',stderr='',deadline=Date.now()+5000,commandId=0;
const commands=[],pending=new Map(),pause=ms=>new Promise(r=>setTimeout(r,ms));
const json=(name,value)=>writeFile(join(out,name),JSON.stringify(value,null,2)+'\n');
async function waitFor(check,limit=deadline){while(Date.now()<limit){const v=await check();if(v)return v;if(launchError)throw launchError;if(child&&exitCode!==null)throw new Error('Browser exited: '+exitCode);await pause(25);}throw new Error('Bounded browser wait timed out');}
function call(method,params={},sessionId,limit=deadline){
  const id=++commandId;commands.push({id,method,params,...(sessionId?{sessionId}:{})});
  return new Promise((yes,no)=>{
    const timer=setTimeout(()=>{pending.delete(id);no(new Error('CDP timeout: '+method));},Math.max(1,Math.min(35000,limit-Date.now())));
    pending.set(id,{yes:v=>{clearTimeout(timer);yes(v);},no:e=>{clearTimeout(timer);no(e);}});
    try{socket.send(JSON.stringify({id,method,params,...(sessionId?{sessionId}:{})}));}catch(e){pending.get(id).no(e);pending.delete(id);}
  });
}
async function evaluate(expression,sessionId){const r=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true},sessionId);if(r.exceptionDetails)throw new Error(r.exceptionDetails.text+': '+(r.exceptionDetails.exception?.description||''));return r.result.value;}
let imageIndex=0;
async function retainImages(value){
  if(!value||typeof value!=='object')return;
  if(typeof value.png==='string'){
    if(!value.png.startsWith('data:image/png;base64,'))throw new Error('Non-PNG consumer capture');
    const bytes=Buffer.from(value.png.split(',')[1],'base64'),name=`cell-${String(imageIndex++).padStart(5,'0')}.png`;
    await writeFile(join(out,name),bytes);value.image={path:name,sha256:hash(bytes)};delete value.png;
  }
  for(const v of Object.values(value))await retainImages(v);
}
async function persist(){if(!report)return;report.served_files=Object.fromEntries(running?.served||[]);report.observed_at=new Date().toISOString();await json('capture.json',report);}
try{
  config=validateConfig(JSON.parse(await readFile(resolve(options['--config']),'utf8')));deadline=Date.now()+config.timeout_seconds*1000-2000;
  if(!browser){for(const path of [join(process.env.PROGRAMFILES||'','Google/Chrome/Application/chrome.exe'),join(process.env['ProgramFiles(x86)']||'','Microsoft/Edge/Application/msedge.exe'),'/usr/bin/chromium','/usr/bin/chromium-browser','/usr/bin/google-chrome']){try{await access(path);browser=path;break;}catch{}}}
  if(!browser)throw new Error('No installed Chromium browser; supply an explicit browser executable');
  browser=await realpath(resolve(browser));
  const renderer_files=Object.fromEntries(await Promise.all(profileFiles.map(async name=>[name,hash(await readFile(join(rendererRoot,name)))])));
  profileParent=await realpath(tmpdir());profile=await mkdtemp(join(profileParent,'pixl-consumer-'));
  running=await serve(project,config);
  const args=['--headless=new','--disable-gpu','--hide-scrollbars','--no-first-run','--no-default-browser-check','--disable-background-networking',`--user-data-dir=${profile}`,'--remote-debugging-address=127.0.0.1','--remote-debugging-port=0','about:blank'];
  const viewport={width:1280,height:1000,deviceScaleFactor:1,mobile:false};
  await json('launch.json',{browser,args,project,node:process.version,viewport,config,renderer_files});
  child=spawn(browser,args,{windowsHide:true,stdio:['ignore','pipe','pipe']});
  execution.browser_pid=child.pid||null;
  child.stdout.on('data',x=>{stdout=(stdout+x).slice(-2000000);});child.stderr.on('data',x=>{stderr=(stderr+x).slice(-2000000);});
  child.once('error',e=>{launchError=e;});child.once('exit',(code,signal)=>{exitCode=code??-1;execution.browser_exit={code,signal};});
  const endpoint=await waitFor(()=>stderr.match(/DevTools listening on (ws:\/\/127\.0\.0\.1:\d+\/devtools\/browser\/[^\s]+)/)?.[1],Math.min(deadline,Date.now()+15000));
  socket=new WebSocket(endpoint);
  await new Promise((yes,no)=>{const timer=setTimeout(()=>no(new Error('CDP open timed out')),Math.max(1,Math.min(5000,deadline-Date.now())));socket.addEventListener('open',()=>{clearTimeout(timer);yes();},{once:true});socket.addEventListener('error',()=>{clearTimeout(timer);no(new Error('CDP open failed'));},{once:true});});
  socket.addEventListener('message',event=>{const m=JSON.parse(event.data),item=pending.get(m.id);if(!item)return;pending.delete(m.id);m.error?item.no(new Error(JSON.stringify(m.error))):item.yes(m.result);});
  socket.addEventListener('close',()=>{for(const item of pending.values())item.no(new Error('CDP connection closed'));pending.clear();});
  const browser_version=await call('Browser.getVersion');
  report={version:1,profile:'queue-motion-v1',project,config,renderer_files,browser_version,viewport:{width:1280,height:1000,device_scale_factor:1},node:process.version,views:[],phases:[],screenshots:[],errors:[]};
  async function page(preference){
    const {targetId}=await call('Target.createTarget',{url:'about:blank'}),{sessionId}=await call('Target.attachToTarget',{targetId,flatten:true});
    await call('Page.enable',{},sessionId);await call('Emulation.setDeviceMetricsOverride',viewport,sessionId);
    await call('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:preference}]},sessionId);
    await call('Page.navigate',{url:running.url+'/'},sessionId);
    await waitFor(()=>evaluate('document.body?.dataset.ready === "true"',sessionId));
    execution.renderer_executed=true;
    const unavailable=await evaluate('window.queueUnavailable || null',sessionId);if(unavailable){const error=new Error(unavailable);error.code='UNAVAILABLE';throw error;}
    return sessionId;
  }
  async function phase(name,sessionId){
    const observed=await evaluate(`window.queueCapture(${JSON.stringify(name)})`,sessionId);await retainImages(observed);report.phases.push(observed);
    const info=await evaluate('window.queueInfo()',sessionId);await retainImages(info);report.display=info.display;report.reducedMotionQuery=info.reducedMotionQuery;report.state_inventory=info.state_inventory;report.errors.push(...info.errors);
    if(!report.views.length)report.views=info.views;
    const snap=await call('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false},sessionId),bytes=Buffer.from(snap.data,'base64'),path=name+'.png';
    await writeFile(join(out,path),bytes);report.screenshots.push({phase:name,path,sha256:hash(bytes)});await persist();
    return observed;
  }
  const first=await page('no-preference');await phase('normal-start',first);
  for(const [name,value,motion] of [['reduced','reduce','reduced'],['normal-restored','no-preference','normal']]){
    await call('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value}]},first);
    await waitFor(async()=>{const s=await evaluate('window.queueMotion()',first);return s.motion===motion&&s.reconciliations===s.events;});await phase(name,first);
  }
  const second=await page('reduce');await phase('initially-reduced',second);
  for(const [name,expected]of Object.entries(renderer_files))if(hash(await readFile(join(rendererRoot,name)))!==expected)throw new Error('Renderer changed during capture: '+name);
  execution.status=report.phases.every(p=>p.status==='observed')&&report.views.every(v=>v.geometryMatches&&v.image)&&!report.errors.length?'complete':report.phases.some(p=>p.status==='timeout')?'timeout':'unavailable';
}catch(error){execution.error=String(error);execution.status=error.code==='UNAVAILABLE'?'unavailable':/timed out|timeout/i.test(String(error))?'timeout':report?'failed':'unavailable';}
finally{
  const cleanup={browser_closed:!child,server_closed:!running,profile_removed:!profile,errors:[]};
  if(socket?.readyState===WebSocket.OPEN){try{await call('Browser.close',{},undefined,Date.now()+1500);}catch(e){if(exitCode===null)cleanup.errors.push(String(e));}}
  // close() aborts a connecting WebSocket as well; failed open must not leave it alive.
  if(socket && socket.readyState!==WebSocket.CLOSED){try{socket.close();}catch(e){cleanup.errors.push(String(e));}}
  for(const item of pending.values())item.no(new Error('Capture closed'));pending.clear();
  if(child){
    let until=Date.now()+2000;while(exitCode===null&&!launchError&&Date.now()<until)await pause(25);
    if(exitCode===null&&!launchError){child.kill();until=Date.now()+1500;while(exitCode===null&&Date.now()<until)await pause(25);}
    if(exitCode===null&&!launchError){child.kill('SIGKILL');until=Date.now()+1000;while(exitCode===null&&Date.now()<until)await pause(25);}
    cleanup.browser_closed=exitCode!==null||!!launchError;
  }
  if(running){try{running.server.closeAllConnections();await new Promise((yes,no)=>{const timer=setTimeout(()=>no(new Error('Loopback close timed out')),1500);running.server.close(e=>{clearTimeout(timer);e?no(e):yes();});});cleanup.server_closed=true;}catch(e){cleanup.errors.push(String(e));}}
  if(profile){try{const actual=await realpath(profile),rel=relative(profileParent,actual);if(actual!==resolve(profile)||!rel.startsWith('pixl-consumer-')||rel.includes(sep)||basename(actual)!==basename(profile)||!cleanup.browser_closed)throw new Error('Owned profile cleanup guard failed');await rm(actual,{recursive:true,maxRetries:4,retryDelay:150});try{await access(actual);throw new Error('Profile still exists');}catch(e){if(e.code!=='ENOENT')throw e;}cleanup.profile_removed=true;}catch(e){cleanup.errors.push(String(e));}}
  cleanup.complete=cleanup.browser_closed&&cleanup.server_closed&&cleanup.profile_removed;
  execution.cleanup=cleanup;if(!cleanup.complete)execution.status='failed';execution.finished_at=new Date().toISOString();
  await persist();await json('browser-process.json',{exitCode,stdout,stderr,launch_error:launchError?String(launchError):null});await json('capture-commands.json',commands);await json('execution.json',execution);
}
console.log(JSON.stringify({status:execution.status,capture:report?join(out,'capture.json'):null,execution:join(out,'execution.json'),cleanup:execution.cleanup}));
process.exitCode=execution.status==='complete'?0:1;
