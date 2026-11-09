// A local graphical consumer for the successor queue modules, not an asset generator. Copied from renderer/server.mjs; rendererRoot resolves to this folder.
import { createServer } from 'node:http';
import { readFile, realpath } from 'node:fs/promises';
import { resolve, relative, sep, dirname, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { stripTypeScriptTypes } from 'node:module';
import { createHash } from 'node:crypto';

export const rendererRoot = dirname(fileURLToPath(import.meta.url));
export const hash = bytes => createHash('sha256').update(bytes).digest('hex');

export async function serve(project, onCapture = null) {
  const root = await realpath(project);
  const served = new Map();
  const server = createServer(async (request, response) => {
    try {
      const url = new URL(request.url, 'http://127.0.0.1');
      if (url.pathname === '/__capture' && request.method === 'POST' && onCapture) {
        let body = '';
        for await (const chunk of request) {
          body += chunk;
          if (body.length > 4_000_000) throw new Error('Capture exceeds local limit');
        }
        await onCapture(JSON.parse(body));
        response.writeHead(200, { 'Content-Type': 'text/plain' }).end('retained');
        return;
      }
      if (request.method !== 'GET') {
        response.writeHead(405).end();
        return;
      }
      const pathname = decodeURIComponent(url.pathname);
      const own = pathname === '/' || pathname === '/view.mjs';
      if (!own && !pathname.startsWith('/src/') && !pathname.startsWith('/assets/')) {
        response.writeHead(404).end('Not a consumer resource');
        return;
      }
      const base = own ? rendererRoot : root;
      const name = pathname === '/' ? 'index.html' : pathname.slice(1);
      const path = await realpath(resolve(base, name));
      const rel = relative(base, path);
      if (rel === '..' || rel.startsWith(`..${sep}`) || resolve(base, rel) !== path) {
        response.writeHead(403).end('Outside consumer');
        return;
      }
      const bytes = await readFile(path);
      served.set(`${own ? 'renderer' : 'consumer'}/${rel.replaceAll(sep, '/')}`, hash(bytes));
      const extension = extname(path);
      const type = { '.html': 'text/html', '.mjs': 'text/javascript', '.ts': 'text/javascript', '.png': 'image/png', '.svg': 'image/svg+xml' }[extension];
      if (!type) { response.writeHead(415).end(); return; }
      response.writeHead(200, { 'Content-Type': type, 'Cache-Control': 'no-store' });
      response.end(extension === '.ts' ? stripTypeScriptTypes(bytes.toString('utf8')) : bytes);
    } catch (error) {
      const missing = error.code === 'ENOENT';
      response.writeHead(missing ? 404 : 500).end(missing ? 'Missing consumer asset' : String(error));
    }
  });
  await new Promise((yes, no) => { server.once('error', no); server.listen(0, '127.0.0.1', yes); });
  return { server, root, served, url: `http://127.0.0.1:${server.address().port}` };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const flag = process.argv.indexOf('--project');
  const project = flag < 0 ? resolve(rendererRoot, '..') : resolve(process.argv[flag + 1]);
  const running = await serve(project);
  console.log(JSON.stringify({ url: running.url, project: running.root, node: process.version }));
}
