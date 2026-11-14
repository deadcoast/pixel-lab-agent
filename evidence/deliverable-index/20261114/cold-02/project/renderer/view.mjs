// The consumer owns frame order, uneven timing, crop geometry and pivots.
const $ = id => document.getElementById(id);
const canvas = $('canvas'), ctx = canvas.getContext('2d', {willReadFrequently:true});
const errors=[], assets={}, report={version:1,consumer:'sprite-animation-v1',errors};
const integer=(v,lo,hi)=>Number.isInteger(v)&&v>=lo&&v<=hi;
function demand(value,message){if(!value)throw new Error(message);}
function pair(value,lo,hi){return Array.isArray(value)&&value.length===2&&value.every(v=>integer(v,lo,hi));}
function canonical(path){return typeof path==='string'&&/^assets\/[A-Za-z0-9_.-]+(?:\/[A-Za-z0-9_.-]+)*\.png$/.test(path)&&!path.split('/').some(v=>v==='.'||v==='..');}
let config, animation, frameAt, active, scale=1, frame=0, paused=true, token=0, playElapsed=0;
function info(clip,index,s){
  const f=clip.frames[index], image=assets[f.path];
  return {clip:clip.id,frame:index,frame_id:f.id,scale:s,anchor:clip.anchor,pivot:f.pivot,source_rect:f.rect,path:f.path,
    asset:{path:f.path,sha256:image.sha256,width:image.bitmap.width,height:image.bitmap.height},smoothing:ctx.imageSmoothingEnabled,
    imageRendering:getComputedStyle(canvas).imageRendering,rect:{x:canvas.getBoundingClientRect().x,y:canvas.getBoundingClientRect().y,width:canvas.width,height:canvas.height}};
}
function paint(clip,index,s){
  demand(integer(index,0,clip.frames.length-1),'frameAt returned an invalid frame');
  canvas.width=animation.viewport[0]*s;canvas.height=animation.viewport[1]*s;
  ctx.imageSmoothingEnabled=false;ctx.fillStyle=animation.background;ctx.fillRect(0,0,canvas.width,canvas.height);
  const f=clip.frames[index];ctx.drawImage(assets[f.path].bitmap,...f.rect,(clip.anchor[0]-f.pivot[0])*s,(clip.anchor[1]-f.pivot[1])*s,f.rect[2]*s,f.rect[3]*s);
  $('anchor').style.left=(clip.anchor[0]*s)+'px';$('anchor').style.top=(clip.anchor[1]*s)+'px';
  $('caption').textContent=`${clip.label} / frame ${index+1} of ${clip.frames.length} / ${f.duration_ms} ms / ${s}x`;
  return info(clip,index,s);
}
function select(clipId,s,index=0){
  paused=true;token++;active=animation.clips.find(c=>c.id===clipId);demand(active,'Unknown clip');scale=s;frame=index;playElapsed=active.frames.slice(0,index).reduce((n,f)=>n+f.duration_ms,0);
  $('clip').value=clipId;$('scale').value=String(s);$('play').textContent='Play';return paint(active,index,s);
}
function play(){
  paused=!paused;$('play').textContent=paused?'Play':'Pause';if(paused){token++;return;}
  const duration=active.frames.reduce((n,f)=>n+f.duration_ms,0);
  if(!active.loop&&playElapsed>=duration)playElapsed=0;
  const current=++token,base=playElapsed;let origin=null;
  function tick(now){
    if(paused||current!==token)return;if(origin===null)origin=now;
    try{
      playElapsed=base+now-origin;frame=frameAt(active.id,playElapsed);paint(active,frame,scale);
      if(!active.loop&&playElapsed>=duration){paused=true;$('play').textContent='Play';return;}
      requestAnimationFrame(tick);
    }catch(e){$('error').textContent=String(e);paused=true;$('play').textContent='Play';}
  }
  requestAnimationFrame(tick);
}
window.animationStep=(clipId,index,s)=>{const value=select(clipId,s,index);return {...value,png:canvas.toDataURL('image/png')};};
window.animationPlayback=(clipId,s,wrapTarget,timeout)=>new Promise(resolve=>{
  const clip=animation.clips.find(c=>c.id===clipId);select(clipId,s);const current=++token;
  let origin=null,last=null,wraps=0,transitions=0,skips=0;const frames=new Set(),samples=[],ticks=[];
  const duration=clip.frames.reduce((n,f)=>n+f.duration_ms,0);
  const finish=(status,reason)=>resolve({clip:clipId,scale:s,loop:clip.loop,status,reason,frames:[...frames].sort((a,b)=>a-b),wraps,transitions,skips,samples,ticks});
  function tick(now){
    if(current!==token)return finish('unavailable','Playback interrupted by another view');
    if(origin===null)origin=now;const elapsed=now-origin;
    try{
      const index=frameAt(clipId,elapsed),view=paint(clip,index,s);frame=index;playElapsed=elapsed;ticks.push({elapsed_ms:elapsed,frame:index});
      if(last===null||index!==last){
        if(last!==null){transitions++;if(index===0&&last===clip.frames.length-1)wraps++;if(index!==(last+1)%clip.frames.length)skips++;}
        samples.push({elapsed_ms:elapsed,...view,png:canvas.toDataURL('image/png')});frames.add(index);last=index;
      }
      const complete=frames.size===clip.frames.length&&(clip.loop?wraps>=wrapTarget:elapsed>=duration&&index===clip.frames.length-1);
      if(complete)return finish('observed',clip.loop?'Actual frame transitions reached the requested wrap count':'Actual one-shot playback reached and held its terminal frame');
      if(elapsed>=timeout||ticks.length>20000)return finish('unavailable','Live playback did not cover required frames/wraps before its bound');
      requestAnimationFrame(tick);
    }catch(error){errors.push(String(error));finish('unavailable',String(error));}
  }
  requestAnimationFrame(tick);
});
try{
  config=await(await fetch('/config.json',{cache:'no-store'})).json();
  demand(config.profile==='sprite-animation-v1'&&Array.isArray(config.scales),'Wrong execution profile');
  const module=await import('/'+config.modules.animation);animation=module.animation;frameAt=module.frameAt;
  demand(typeof frameAt==='function'&&animation&&pair(animation.viewport,1,128),'Missing animation/frameAt or invalid viewport');
  demand(animation.sampling==='nearest'&&/^#[0-9a-f]{6}$/i.test(animation.background),'Expected nearest sampling and opaque hex background');
  demand(Array.isArray(animation.clips)&&animation.clips.length>=1&&animation.clips.length<=4,'Use one to four named clips');
  const ids=new Set(),paths=new Set();
  for(const clip of animation.clips){
    demand(/^[A-Za-z0-9_.-]{1,64}$/.test(clip.id)&&!ids.has(clip.id),'Invalid or duplicate clip ID');ids.add(clip.id);
    demand(typeof clip.label==='string'&&clip.label.length<=160&&typeof clip.loop==='boolean'&&pair(clip.anchor,0,128),'Invalid clip label, loop or anchor');
    demand(Array.isArray(clip.frames)&&clip.frames.length>=2&&clip.frames.length<=16,'Use two to sixteen frames per clip');
    const frameIds=new Set();
    for(const f of clip.frames){
      demand(typeof f.id==='string'&&f.id.length<=64&&!frameIds.has(f.id),'Invalid or duplicate frame ID');frameIds.add(f.id);
      demand(canonical(f.path)&&integer(f.duration_ms,1,60000)&&pair(f.pivot,-128,128),'Invalid frame path, duration or pivot');
      demand(Array.isArray(f.rect)&&f.rect.length===4&&f.rect.every(v=>integer(v,0,4096))&&f.rect[2]>0&&f.rect[3]>0,'Invalid source crop');paths.add(f.path);
    }
  }
  demand(JSON.stringify([...paths].sort())===JSON.stringify([...new Set(Object.values(config.destinations))].sort()),'Every mapped destination must be used by a clip');
  for(const path of paths){
    const response=await fetch('/'+path,{cache:'no-store'});demand(response.ok,'Missing animation asset: '+path);
    const bytes=await response.arrayBuffer(),sha256=[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(v=>v.toString(16).padStart(2,'0')).join('');
    const bitmap=await createImageBitmap(new Blob([bytes],{type:'image/png'}));assets[path]={bitmap,sha256};
  }
  for(const clip of animation.clips)for(const f of clip.frames){const bitmap=assets[f.path].bitmap;demand(f.rect[0]+f.rect[2]<=bitmap.width&&f.rect[1]+f.rect[3]<=bitmap.height,'Crop exceeds source image: '+f.id);}
  report.animation=JSON.parse(JSON.stringify(animation));report.config=config;
  for(const clip of animation.clips)$('clip').add(new Option(clip.label,clip.id));for(const s of config.scales)$('scale').add(new Option(s+'x',s));
  $('clip').onchange=()=>select($('clip').value,scale);$('scale').onchange=()=>select(active.id,Number($('scale').value),frame);
  $('play').onclick=play;$('previous').onclick=()=>select(active.id,scale,(frame+active.frames.length-1)%active.frames.length);$('next').onclick=()=>select(active.id,scale,(frame+1)%active.frames.length);
  $('show-anchor').onchange=()=>{$('anchor').hidden=!$('show-anchor').checked;};select(animation.clips[0].id,config.scales[0]);
}catch(error){errors.push(String(error));$('error').textContent=String(error);}
window.animationReport=()=>JSON.parse(JSON.stringify(report));document.body.dataset.ready='true';
