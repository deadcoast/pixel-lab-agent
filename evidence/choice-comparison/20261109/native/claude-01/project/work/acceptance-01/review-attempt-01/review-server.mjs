// Supplemental observation surface; does not replace or alter the destination renderer.
import {createServer} from 'node:http';
import {readFile,writeFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {stripTypeScriptTypes} from 'node:module';
const here=dirname(fileURLToPath(import.meta.url)), project=resolve(here,'../..');
const allowed=new Set(['src/queue-view-successor.ts','renderer-successor/assets/working.png','renderer-successor/assets/ready-confirmed.png','renderer-successor/assets/error-retry.png','renderer-successor/assets/paused.png','renderer-successor/assets/start.svg']);
const server=createServer(async(req,res)=>{
  try {
    const path=new URL(req.url,'http://127.0.0.1').pathname;
    if(path==='/capture' && req.method==='POST'){
      let body='';for await(const chunk of req){body+=chunk;if(body.length>4000000)throw Error('Capture too large');}
      const value=JSON.parse(body);await writeFile(resolve(here,'playback-observation.json'),JSON.stringify(value,null,2)+'\n',{flag:'wx'});
      res.end('retained');return;
    }
    const name=path.slice(1), local=path==='/'?'review.html':path==='/review.mjs'?'review.mjs':null;
    if(req.method!=='GET'||(!local&&!allowed.has(name))){res.writeHead(404).end();return;}
    const file=resolve(local?here:project,local||name), bytes=await readFile(file);
    res.setHeader('Cache-Control','no-store');res.setHeader('Content-Type',file.endsWith('.html')?'text/html':file.endsWith('.png')?'image/png':file.endsWith('.svg')?'image/svg+xml':'text/javascript');
    res.end(file.endsWith('.ts')?stripTypeScriptTypes(bytes.toString()):bytes);
  } catch(e){res.writeHead(500).end(String(e));}
});
server.listen(0,'127.0.0.1',()=>console.log(JSON.stringify({url:`http://127.0.0.1:${server.address().port}`,project})));
