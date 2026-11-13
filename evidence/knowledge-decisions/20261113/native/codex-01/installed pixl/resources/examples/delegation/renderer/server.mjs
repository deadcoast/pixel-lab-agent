// Bounded graphical consumer of the existing directional controller.
import {createServer} from 'node:http';
import {readFile, realpath} from 'node:fs/promises';
import {resolve, relative, sep, dirname, extname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {stripTypeScriptTypes} from 'node:module';
import {createHash} from 'node:crypto';

export const rendererRoot = dirname(fileURLToPath(import.meta.url));
export const rendererFiles = ['server.mjs', 'capture.mjs', 'view.mjs', 'index.html', 'check.py'];
export const directions = ['south', 'east', 'north', 'west'];
export const consumerFiles = ['src/robot.ts', 'assets/robot-base.png', ...directions.map(d => `assets/robot/${d}.png`)];
export const hash = bytes => createHash('sha256').update(bytes).digest('hex');

export async function confined(root, name) {
  const actual = await realpath(resolve(root, name));
  const rel = relative(root, actual);
  if (rel === '..' || rel.startsWith(`..${sep}`) || resolve(root, rel) !== actual) throw new Error('Resource escapes consumer root');
  return actual;
}

export async function serve(project) {
  const root = await realpath(project), served = new Map();
  const server = createServer(async (request, response) => {
    try {
      if (request.method !== 'GET') { response.writeHead(405).end(); return; }
      const path = decodeURIComponent(new URL(request.url, 'http://127.0.0.1').pathname);
      const name = path === '/' ? 'index.html' : path.slice(1);
      const own = ['index.html', 'view.mjs'].includes(name);
      if (!own && !consumerFiles.includes(name)) { response.writeHead(404).end('Outside directional consumer'); return; }
      const file = await confined(own ? rendererRoot : root, name), bytes = await readFile(file);
      served.set(`${own ? 'renderer' : 'consumer'}/${name}`, hash(bytes));
      const type = {'.html': 'text/html', '.mjs': 'text/javascript', '.ts': 'text/javascript', '.png': 'image/png'}[extname(file)];
      response.writeHead(200, {'Content-Type': type, 'Cache-Control': 'no-store'});
      response.end(extname(file) === '.ts' ? stripTypeScriptTypes(bytes.toString('utf8')) : bytes);
    } catch (error) {
      response.writeHead(error.code === 'ENOENT' ? 404 : 500).end(error.code === 'ENOENT' ? 'Missing consumer asset' : String(error));
    }
  });
  await new Promise((yes, no) => { server.once('error', no); server.listen(0, '127.0.0.1', yes); });
  return {server, root, served, url: `http://127.0.0.1:${server.address().port}`};
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (process.argv.length !== 4 || process.argv[2] !== '--project') throw new Error('Use --project CONSUMER_ROOT');
  const running = await serve(resolve(process.argv[3]));
  console.log(JSON.stringify({project: running.root, url: running.url, node: process.version}));
}
