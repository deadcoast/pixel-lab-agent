// Bounded graphical consumer of an authored sprite animation module.
import {createServer} from 'node:http';
import {readFile, realpath, readdir, lstat} from 'node:fs/promises';
import {resolve, relative, sep, dirname, extname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {stripTypeScriptTypes} from 'node:module';
import {createHash} from 'node:crypto';

export const rendererRoot = dirname(fileURLToPath(import.meta.url));
export const rendererFiles = ['server.mjs', 'capture.mjs', 'view.mjs', 'index.html', 'check.py', 'observation.py'];
export const hash = bytes => createHash('sha256').update(bytes).digest('hex');

export async function confined(root, name) {
  if (typeof name !== 'string' || name.includes('\\') || name.includes(':') || name.split('/').some(p => !p || p === '.' || p === '..')) throw new Error('Noncanonical relative resource');
  let current = root;
  for (const part of name.split('/')) { current = resolve(current, part); if ((await lstat(current)).isSymbolicLink()) throw new Error('Resource symlink unsupported'); }
  const actual = await realpath(resolve(root, name));
  const rel = relative(root, actual);
  if (rel === '..' || rel.startsWith(`..${sep}`) || resolve(root, rel) !== actual) throw new Error('Resource escapes consumer root');
  return actual;
}

export async function sourceFiles(project, config) {
  const names = [];
  async function walk(folder) {
    for (const entry of await readdir(resolve(project, folder), {withFileTypes: true})) {
      if (entry.isSymbolicLink()) throw new Error('Source symlink unsupported');
      const name = folder + '/' + entry.name;
      if (entry.isDirectory()) await walk(name);
      else if (entry.isFile()) names.push(name);
      else throw new Error('Nonregular source');
    }
  }
  await walk('src');
  if (names.length > 512) throw new Error('Source tree exceeds 512 files');
  return [...new Set([...names, ...Object.values(config.destinations)])].sort();
}

export async function serve(project, config, configBytes = Buffer.from(JSON.stringify(config))) {
  const root = await realpath(project), served = new Map(), allowed = new Set(await sourceFiles(root, config));
  const server = createServer(async (request, response) => {
    try {
      if (request.method !== 'GET') { response.writeHead(405).end(); return; }
      const path = decodeURIComponent(new URL(request.url, 'http://127.0.0.1').pathname);
      const name = path === '/' ? 'index.html' : path.slice(1);
      if (name === 'config.json') {
        served.set('config', hash(configBytes)); response.writeHead(200, {'Content-Type':'application/json','Cache-Control':'no-store'}).end(configBytes); return;
      }
      const own = ['index.html', 'view.mjs'].includes(name);
      if (!own && !allowed.has(name)) { response.writeHead(404).end('Outside animation consumer'); return; }
      const file = await confined(own ? rendererRoot : root, name), bytes = await readFile(file);
      if (bytes.length > 64 * 1024 * 1024) throw new Error('Resource exceeds 64 MiB');
      served.set(`${own ? 'renderer' : 'consumer'}/${name}`, hash(bytes));
      const type = {'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.ts':'text/javascript','.png':'image/png','.json':'application/json'}[extname(file)];
      response.writeHead(200, {'Content-Type': type || 'application/octet-stream', 'Cache-Control':'no-store'});
      response.end(extname(file) === '.ts' ? stripTypeScriptTypes(bytes.toString('utf8')) : bytes);
    } catch (error) {response.writeHead(error.code === 'ENOENT' ? 404 : 500).end(String(error));}
  });
  await new Promise((yes,no) => {server.once('error',no);server.listen(0,'127.0.0.1',yes);});
  return {server,root,served,url:`http://127.0.0.1:${server.address().port}`};
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = Object.fromEntries(Array.from({length:(process.argv.length-2)/2},(_,i)=>[process.argv[2+i*2],process.argv[3+i*2]]));
  if (!args['--project'] || !args['--config']) throw new Error('Use --project ROOT --config CONFIG');
  const bytes = await readFile(resolve(args['--config']));
  const running = await serve(resolve(args['--project']), JSON.parse(bytes), bytes);
  console.log(JSON.stringify({project:running.root,url:running.url,node:process.version}));
}
