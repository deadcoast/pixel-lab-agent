// Fixed binary-corner neighborhood destination; project conventions stay explicit.
import {createServer} from 'node:http';
import {readFile, realpath, readdir, lstat} from 'node:fs/promises';
import {resolve, relative, sep, dirname, extname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {stripTypeScriptTypes} from 'node:module';
import {createHash} from 'node:crypto';

export const rendererRoot = dirname(fileURLToPath(import.meta.url));
export const rendererFiles = ['capture.mjs', 'server.mjs', 'view.mjs', 'index.html', 'check.py', 'observation.py'];
export const hash = bytes => createHash('sha256').update(bytes).digest('hex');
export function canonical(name) {
  return typeof name === 'string' && name.length > 0 && !name.includes('\\') && !name.includes(':') && !name.startsWith('/') && !name.split('/').some(p => ['', '.', '..'].includes(p));
}
export async function confined(root, name) {
  if (!canonical(name)) throw new Error('Noncanonical consumer path');
  const requested = resolve(root, name), actual = await realpath(requested), rel = relative(root, actual);
  if (actual !== requested || rel === '..' || rel.startsWith(`..${sep}`) || !rel || (await lstat(actual)).isSymbolicLink()) throw new Error('Resource escapes or redirects consumer path');
  return actual;
}
export function configuration(config) {
  const exact = (value, keys) => value && typeof value === 'object' && !Array.isArray(value) && JSON.stringify(Object.keys(value).sort()) === JSON.stringify([...keys].sort());
  if (!exact(config, ['version', 'profile', 'modules', 'destinations', 'scales', 'timeout_seconds']) || config.version !== 1 || config.profile !== 'tile-neighborhood-v1') throw new Error('Invalid tile profile configuration');
  if (!exact(config.modules, ['terrain']) || !/^src\/(?:[A-Za-z0-9_-]+\/)*[A-Za-z0-9_.-]+\.(?:js|mjs|ts)$/.test(config.modules.terrain)) throw new Error('One terrain module under src is required');
  if (!config.destinations || Array.isArray(config.destinations) || Object.keys(config.destinations).length !== 16 || Object.values(config.destinations).some(p => !canonical(p) || !p.startsWith('assets/') || !p.endsWith('.png')) || new Set(Object.values(config.destinations)).size !== 16) throw new Error('Map exactly 16 distinct PNG destinations');
  if (!Array.isArray(config.scales) || config.scales.length < 1 || config.scales.length > 4 || new Set(config.scales).size !== config.scales.length || config.scales.some(v => !Number.isInteger(v) || v < 1 || v > 16)) throw new Error('Invalid observation scales');
  if (!Number.isInteger(config.timeout_seconds) || config.timeout_seconds < 5 || config.timeout_seconds > 180) throw new Error('Invalid subprocess deadline');
  return config;
}
export async function sourceFiles(root) {
  const files = []; let bytes = 0;
  async function walk(name) {
    const actual = await confined(root, name);
    for (const item of await readdir(actual, {withFileTypes: true})) {
      const child = name + '/' + item.name;
      if (item.isSymbolicLink()) throw new Error('Redirected source input');
      if (item.isDirectory()) await walk(child);
      else if (item.isFile()) {const path = await confined(root, child); bytes += (await lstat(path)).size; files.push(child);}
      else throw new Error('Unsupported source input');
      if (files.length > 512 || bytes > 64 * 1024 * 1024) throw new Error('Source closure exceeds bounds');
    }
  }
  await walk('src');
  return files.sort();
}
export async function snapshot(project, config) {
  const sources = await sourceFiles(project), names = [...sources, ...Object.values(config.destinations)].sort();
  const files = Object.fromEntries(await Promise.all(names.map(async name => {
    try {const path = await confined(project, name); if ((await lstat(path)).size > 64 * 1024 * 1024) throw new Error('Input exceeds bounds'); return [name, hash(await readFile(path))];}
    catch (error) {if (error.code === 'ENOENT') return [name, null]; throw error;}
  })));
  return {files, sources};
}
export async function serve(project, config) {
  const root = await realpath(project), served = new Map(), sources = await sourceFiles(root);
  configuration(config);
  const allowed = new Set([...sources, ...Object.values(config.destinations)]);
  const server = createServer(async (request, response) => {
    try {
      if (request.method !== 'GET') {response.writeHead(405).end(); return;}
      const path = decodeURIComponent(new URL(request.url, 'http://127.0.0.1').pathname);
      if (path === '/config.json') {response.writeHead(200, {'Content-Type': 'application/json', 'Cache-Control': 'no-store'}).end(JSON.stringify(config)); return;}
      const name = path === '/' ? 'index.html' : path.slice(1), own = ['index.html', 'view.mjs'].includes(name);
      if (!own && !allowed.has(name)) {response.writeHead(404).end('Outside tile consumer'); return;}
      const file = await confined(own ? rendererRoot : root, name), bytes = await readFile(file);
      served.set(`${own ? 'renderer' : 'consumer'}/${name}`, hash(bytes));
      const type = {'.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.ts': 'text/javascript', '.png': 'image/png'}[extname(file)] || 'application/octet-stream';
      response.writeHead(200, {'Content-Type': type, 'Cache-Control': 'no-store'});
      response.end(extname(file) === '.ts' ? stripTypeScriptTypes(bytes.toString('utf8')) : bytes);
    } catch (error) {response.writeHead(error.code === 'ENOENT' ? 404 : 500).end(error.code === 'ENOENT' ? 'Missing tile input' : String(error));}
  });
  await new Promise((yes, no) => {server.once('error', no); server.listen(0, '127.0.0.1', yes);});
  return {server, root, served, url: `http://127.0.0.1:${server.address().port}`};
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = Object.fromEntries(Array.from({length: (process.argv.length - 2) / 2}, (_, i) => [process.argv[2 + i * 2], process.argv[3 + i * 2]]));
  if (!args['--project'] || !args['--config'] || Object.keys(args).some(k => !['--project', '--config'].includes(k))) throw new Error('Use --project ROOT --config CONFIG');
  const running = await serve(resolve(args['--project']), configuration(JSON.parse(await readFile(resolve(args['--config']), 'utf8'))));
  console.log(JSON.stringify({project: running.root, url: running.url, node: process.version}));
}
