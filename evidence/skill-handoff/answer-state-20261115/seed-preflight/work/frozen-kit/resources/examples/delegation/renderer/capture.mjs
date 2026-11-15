// Retain one actual browser observation, using only a freshly owned profile.
import {spawn} from 'node:child_process';
import {access, mkdir, readFile, writeFile, mkdtemp, realpath, rm} from 'node:fs/promises';
import {resolve, join, relative, sep, basename} from 'node:path';
import {tmpdir} from 'node:os';
import {serve, rendererRoot, rendererFiles, consumerFiles, confined, hash} from './server.mjs';

const options = {};
for (let i = 2; i < process.argv.length; i += 2) {
  const key = process.argv[i];
  if (!['--project', '--out', '--browser'].includes(key) || options[key] || !process.argv[i + 1]) throw new Error('Use --project ROOT --out FRESH_DIRECTORY [--browser PATH]');
  options[key] = process.argv[i + 1];
}
if (!options['--project'] || !options['--out']) throw new Error('Project and fresh output directory are required');
const project = await realpath(resolve(options['--project'])), out = resolve(options['--out']);
await mkdir(out, {recursive: false});
const execution = {version: 1, consumer: 'directional-robot-v1', project, status: 'unavailable', renderer_executed: false,
  started_at: new Date().toISOString(), cleanup: {complete: false}, limitations: ['Isolated browser observations are not artistic acceptance or an operating-system sandbox.']};
let browser = options['--browser'], profile, profileParent, running, child, socket, exitCode = null, launchError = null, report;
let stdout = '', stderr = '', commandId = 0;
const deadline = Date.now() + 45000, commands = [], pending = new Map(), pause = ms => new Promise(r => setTimeout(r, ms));
const json = (name, value) => writeFile(join(out, name), JSON.stringify(value, null, 2) + '\n');
async function waitFor(check, limit = deadline) {
  while (Date.now() < limit) { const value = await check(); if (value) return value; if (launchError) throw launchError; if (child && exitCode !== null) throw new Error('Browser exited: ' + exitCode); await pause(25); }
  throw new Error('Bounded browser wait timed out');
}
function call(method, params = {}, sessionId, limit = deadline) {
  const id = ++commandId; commands.push({id, method, params, ...(sessionId ? {sessionId} : {})});
  return new Promise((yes, no) => {
    const timer = setTimeout(() => { pending.delete(id); no(new Error('CDP timeout: ' + method)); }, Math.max(1, Math.min(35000, limit - Date.now())));
    pending.set(id, {yes: value => {clearTimeout(timer); yes(value);}, no: error => {clearTimeout(timer); no(error);}});
    try { socket.send(JSON.stringify({id, method, params, ...(sessionId ? {sessionId} : {})})); }
    catch (error) { pending.get(id).no(error); pending.delete(id); }
  });
}
async function evaluate(expression, sessionId) {
  const result = await call('Runtime.evaluate', {expression, awaitPromise: true, returnByValue: true}, sessionId);
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  return result.result.value;
}
async function snapshot() {
  return Object.fromEntries(await Promise.all(consumerFiles.map(async name => {
    try { return [name, hash(await readFile(await confined(project, name)))]; }
    catch (error) { if (error.code === 'ENOENT') return [name, null]; throw error; }
  })));
}

try {
  const inputs = await snapshot();
  const renderer_files = Object.fromEntries(await Promise.all(rendererFiles.map(async name => [name, hash(await readFile(join(rendererRoot, name)))])));
  await json('inputs.json', {version: 1, project, files: inputs, renderer_files});
  if (!browser) for (const path of [join(process.env.PROGRAMFILES || '', 'Google/Chrome/Application/chrome.exe'), join(process.env['ProgramFiles(x86)'] || '', 'Microsoft/Edge/Application/msedge.exe'), '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome']) {
    try { await access(path); browser = path; break; } catch { /* Try installed browsers only. */ }
  }
  if (!browser) throw new Error('No installed Chromium browser; use --browser PATH');
  browser = await realpath(resolve(browser));
  profileParent = await realpath(tmpdir()); profile = await mkdtemp(join(profileParent, 'pixl-robot-'));
  running = await serve(project);
  const args = ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', '--disable-background-networking', `--user-data-dir=${profile}`, '--remote-debugging-address=127.0.0.1', '--remote-debugging-port=0', 'about:blank'];
  const viewport = {width: 900, height: 700, deviceScaleFactor: 1, mobile: false};
  await json('launch.json', {browser, args, project, node: process.version, viewport, renderer_files});
  child = spawn(browser, args, {windowsHide: true, stdio: ['ignore', 'pipe', 'pipe']}); execution.browser_pid = child.pid || null;
  child.stdout.on('data', value => {stdout = (stdout + value).slice(-2000000);}); child.stderr.on('data', value => {stderr = (stderr + value).slice(-2000000);});
  child.once('error', error => {launchError = error;}); child.once('exit', (code, signal) => {exitCode = code ?? -1; execution.browser_exit = {code, signal};});
  const endpoint = await waitFor(() => stderr.match(/DevTools listening on (ws:\/\/127\.0\.0\.1:\d+\/devtools\/browser\/[^\s]+)/)?.[1], Math.min(deadline, Date.now() + 15000));
  socket = new WebSocket(endpoint);
  await new Promise((yes, no) => {
    const timer = setTimeout(() => no(new Error('CDP open timed out')), 5000);
    socket.addEventListener('open', () => {clearTimeout(timer); yes();}, {once: true});
    socket.addEventListener('error', () => {clearTimeout(timer); no(new Error('CDP open failed'));}, {once: true});
  });
  socket.addEventListener('message', event => {const value = JSON.parse(event.data), item = pending.get(value.id); if (!item) return; pending.delete(value.id); value.error ? item.no(new Error(JSON.stringify(value.error))) : item.yes(value.result);});
  socket.addEventListener('close', () => {for (const item of pending.values()) item.no(new Error('CDP closed')); pending.clear();});
  const browser_version = await call('Browser.getVersion');
  const {targetId} = await call('Target.createTarget', {url: 'about:blank'});
  const {sessionId} = await call('Target.attachToTarget', {targetId, flatten: true});
  await call('Page.enable', {}, sessionId); await call('Emulation.setDeviceMetricsOverride', viewport, sessionId);
  await call('Page.navigate', {url: running.url + '/'}, sessionId);
  await waitFor(() => evaluate('document.body?.dataset.ready === "true"', sessionId)); execution.renderer_executed = true;
  report = await evaluate('window.robotCapture()', sessionId);
  Object.assign(report, {project, inputs, renderer_files, browser_version, viewport: {width: 900, height: 700, device_scale_factor: 1}, node: process.version});
  for (const view of report.views) if (view.png) {
    if (!view.png.startsWith('data:image/png;base64,')) throw new Error('Capture must be PNG');
    const bytes = Buffer.from(view.png.split(',')[1], 'base64'), path = `${view.direction}-${view.scale}x.png`;
    await writeFile(join(out, path), bytes); view.image = {path, sha256: hash(bytes)}; delete view.png;
  }
  const captured = await call('Page.captureScreenshot', {format: 'png', fromSurface: true, captureBeyondViewport: false}, sessionId);
  const bytes = Buffer.from(captured.data, 'base64'); await writeFile(join(out, 'destination.png'), bytes);
  report.screenshot = {path: 'destination.png', sha256: hash(bytes)};
  report.served_files = Object.fromEntries(running.served); report.observed_at = new Date().toISOString();
  report.final_inputs = await snapshot();
  if (JSON.stringify(inputs) !== JSON.stringify(report.final_inputs)) throw new Error('Consumer inputs changed during capture');
  for (const [name, expected] of Object.entries(renderer_files)) if (hash(await readFile(join(rendererRoot, name))) !== expected) throw new Error('Renderer changed during capture: ' + name);
  execution.status = !report.errors.length && report.views.length === 8 && report.views.every(view => view.image && view.geometryMatches) ? 'complete' : 'failed';
} catch (error) {execution.error = String(error); execution.status = /timed out|timeout/i.test(String(error)) ? 'timeout' : report ? 'failed' : 'unavailable';}
finally {
  const cleanup = {browser_closed: !child, server_closed: !running, profile_removed: !profile, errors: []};
  if (socket?.readyState === WebSocket.OPEN) try {await call('Browser.close', {}, undefined, Date.now() + 1500);} catch (error) {if (exitCode === null) cleanup.errors.push(String(error));}
  if (socket && socket.readyState !== WebSocket.CLOSED) try {socket.close();} catch (error) {cleanup.errors.push(String(error));}
  for (const item of pending.values()) item.no(new Error('Capture closed')); pending.clear();
  if (child) {
    let until = Date.now() + 2000; while (exitCode === null && !launchError && Date.now() < until) await pause(25);
    if (exitCode === null && !launchError) {child.kill(); until = Date.now() + 1500; while (exitCode === null && Date.now() < until) await pause(25);}
    if (exitCode === null && !launchError) {child.kill('SIGKILL'); until = Date.now() + 1000; while (exitCode === null && Date.now() < until) await pause(25);}
    cleanup.browser_closed = exitCode !== null || !!launchError;
  }
  if (running) try {running.server.closeAllConnections(); await new Promise((yes, no) => {const timer = setTimeout(() => no(new Error('Server close timed out')), 1500); running.server.close(error => {clearTimeout(timer); error ? no(error) : yes();});}); cleanup.server_closed = true;} catch (error) {cleanup.errors.push(String(error));}
  if (profile) try {
    const actual = await realpath(profile), rel = relative(profileParent, actual);
    if (actual !== resolve(profile) || !rel.startsWith('pixl-robot-') || rel.includes(sep) || basename(actual) !== basename(profile) || !cleanup.browser_closed) throw new Error('Owned profile cleanup guard failed');
    await rm(actual, {recursive: true, maxRetries: 4, retryDelay: 150});
    try {await access(actual); throw new Error('Profile still exists');} catch (error) {if (error.code !== 'ENOENT') throw error;}
    cleanup.profile_removed = true;
  } catch (error) {cleanup.errors.push(String(error));}
  cleanup.complete = cleanup.browser_closed && cleanup.server_closed && cleanup.profile_removed;
  execution.cleanup = cleanup; if (!cleanup.complete) execution.status = 'failed'; execution.finished_at = new Date().toISOString();
  if (report) await json('capture.json', report);
  await json('browser-process.json', {exitCode, stdout, stderr, launch_error: launchError ? String(launchError) : null});
  await json('capture-commands.json', commands); await json('execution.json', execution);
}
console.log(JSON.stringify({status: execution.status, capture: report ? join(out, 'capture.json') : null, execution: join(out, 'execution.json'), cleanup: execution.cleanup}));
process.exitCode = execution.status === 'complete' ? 0 : 1;
