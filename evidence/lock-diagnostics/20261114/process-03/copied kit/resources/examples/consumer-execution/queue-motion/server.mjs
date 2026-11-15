// queue-motion-v1: a loopback fixture adapter, not a general application server.
import { createServer } from 'node:http';
import { readFile, realpath } from 'node:fs/promises';
import { resolve, relative, sep, dirname, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { stripTypeScriptTypes } from 'node:module';
import { createHash } from 'node:crypto';
export const rendererRoot = dirname(fileURLToPath(import.meta.url));
export const hash = bytes => createHash('sha256').update(bytes).digest('hex');
export const profileFiles = ['capture.mjs', 'server.mjs', 'view.mjs', 'index.html', 'check.py', 'observation.py'];

export function validateConfig(c) {
  const keys = ['version', 'profile', 'modules', 'destinations', 'scales', 'observed_wraps', 'phase_timeout_ms', 'hold_ms', 'timeout_seconds'];
  if (!c || typeof c !== 'object' || Object.keys(c).sort().join() !== keys.sort().join() || c.version !== 1 || c.profile !== 'queue-motion-v1') throw new Error('Unsupported closed queue-motion-v1 config');
  if (!c.modules || Object.keys(c.modules).sort().join() !== 'state,view') throw new Error('Exactly state and view modules are required');
  for (const p of Object.values(c.modules)) if (typeof p !== 'string' || !/^src\/(?:[A-Za-z0-9_-]+\/)*[A-Za-z0-9_.-]+\.(?:js|mjs|ts)$/.test(p) || p.split('/').some(x => x === '.' || x === '..')) throw new Error('Modules must be canonical src JS/TS paths');
  if (!c.destinations || Array.isArray(c.destinations) || typeof c.destinations !== 'object' || Object.entries(c.destinations).some(([k,v]) => !k || typeof v !== 'string' || !/^assets\//.test(v) || v.includes('\\') || v.split('/').some(x => !x || x === '.' || x === '..'))) throw new Error('Invalid destination map');
  if (!Array.isArray(c.scales) || !c.scales.length || c.scales.length > 4 || new Set(c.scales).size !== c.scales.length || c.scales.some(x => !Number.isInteger(x) || x < 1 || x > 16)) throw new Error('Scales must contain one to four unique integers 1..16');
  for (const [key, lo, hi] of [['observed_wraps',1,10],['phase_timeout_ms',1000,30000],['hold_ms',100,5000],['timeout_seconds',5,180]]) if (!Number.isInteger(c[key]) || c[key] < lo || c[key] > hi) throw new Error(`Invalid ${key}`);
  return c;
}

export async function serve(project, config) {
  validateConfig(config);
  const root = await realpath(project), served = new Map();
  const server = createServer(async (request, response) => {
    try {
      if (request.method !== 'GET') { response.writeHead(405).end(); return; }
      const pathname = decodeURIComponent(new URL(request.url, 'http://127.0.0.1').pathname);
      if (pathname === '/config.json') { response.writeHead(200, {'Content-Type':'application/json','Cache-Control':'no-store'}).end(JSON.stringify(config)); return; }
      const own = pathname === '/' || pathname === '/view.mjs';
      if (!own && !pathname.startsWith('/src/') && !pathname.startsWith('/assets/')) { response.writeHead(404).end(); return; }
      const base = own ? rendererRoot : root, name = pathname === '/' ? 'index.html' : pathname.slice(1);
      const path = await realpath(resolve(base, name)), rel = relative(base, path);
      if (!rel || rel === '..' || rel.startsWith(`..${sep}`) || resolve(base, rel) !== path || (!own && !['src','assets'].includes(rel.split(sep)[0]))) { response.writeHead(403).end(); return; }
      const type = {'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.ts':'text/javascript','.png':'image/png','.svg':'image/svg+xml'}[extname(path)];
      if (!type) { response.writeHead(415).end(); return; }
      const bytes = await readFile(path);
      const key = `${own ? 'renderer' : 'consumer'}/${rel.replaceAll(sep, '/')}`, digest = hash(bytes);
      if (served.has(key) && served.get(key) !== digest) throw new Error(`Source changed while serving ${key}`);
      served.set(key, digest);
      response.writeHead(200, {'Content-Type':type,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});
      response.end(extname(path) === '.ts' ? stripTypeScriptTypes(bytes.toString('utf8')) : bytes);
    } catch (error) { response.writeHead(error.code === 'ENOENT' ? 404 : 500).end(String(error)); }
  });
  await new Promise((yes,no) => { server.once('error',no); server.listen(0,'127.0.0.1',yes); });
  return {server,root,served,url:`http://127.0.0.1:${server.address().port}`};
}
