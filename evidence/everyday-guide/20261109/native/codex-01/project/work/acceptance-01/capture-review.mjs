// Fresh isolated browser capture. No production/profile-wide browser configuration.
import { spawn } from 'node:child_process';
import { access, mkdir, readFile, writeFile, mkdtemp, realpath, rm } from 'node:fs/promises';
import { resolve, join, relative, sep } from 'node:path';
import { tmpdir } from 'node:os';
import { serve, rendererRoot, hash } from '../../renderer-successor/server.mjs';

const option = name => { const i = process.argv.indexOf(name); return i < 0 ? null : process.argv[i + 1]; };
const project = resolve(option('--project') || join(rendererRoot, '..'));
const output = option('--out');
if (!output) throw new Error('Use --out NEW_DIRECTORY to retain a fresh capture');
const out = resolve(output);
await mkdir(out, { recursive: false });
let browser = option('--browser');
if (!browser) {
  for (const file of [join(process.env.PROGRAMFILES || '', 'Google/Chrome/Application/chrome.exe'), join(process.env['ProgramFiles(x86)'] || '', 'Microsoft/Edge/Application/msedge.exe')]) {
    try { await access(file); browser = file; break; } catch { /* Try next installed browser. */ }
  }
}
if (!browser) throw new Error('No local Chromium browser found; pass --browser PATH');
const profileParent = await realpath(tmpdir());
const profile = await mkdtemp(join(profileParent, 'pixl-render-'));
const rendererFiles = Object.fromEntries(await Promise.all(['server.mjs', 'capture.mjs', 'index.html', 'view.mjs', 'check.py'].map(async name => [name, hash(await readFile(join(rendererRoot, name)))])));
let observed, child, socket;
let stdout = '', stderr = '', exitCode = null, launchError = null;
const commands = [];
const pending = new Map();
const deadline = Date.now() + 45_000;
const pause = () => new Promise(yes => setTimeout(yes, 25));
const reviewURL = option('--url'); if (!reviewURL?.startsWith('http://127.0.0.1:')) throw Error('Expected local review URL');
// Do not mix --screenshot's late viewport resize with earlier page measurements.
// One CDP page sets device metrics before navigation and captures both artifacts.
const args = ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', '--disable-background-networking', `--user-data-dir=${profile}`, '--remote-debugging-address=127.0.0.1', '--remote-debugging-port=0', 'about:blank'];
const viewport = { width: 1280, height: 1000, deviceScaleFactor: 1, mobile: false };
await writeFile(join(out, 'launch.json'), JSON.stringify({ browser, args, project, node: process.version, viewport, scope: 'Isolated local fixture renderer; one CDP page, metrics set before navigation' }, null, 2) + '\n');

async function waitFor(check) {
  while (true) {
    const value = await check();
    if (value) return value;
    if (launchError) throw launchError;
    if (exitCode !== null) throw new Error(`Browser exited before capture: ${exitCode}`);
    if (Date.now() >= deadline) throw new Error('Browser capture exceeded 45 seconds');
    await pause();
  }
}

let commandId = 0;
function call(method, params = {}, sessionId) {
  const id = ++commandId;
  commands.push({ id, method, params, ...(sessionId ? { sessionId } : {}) });
  return new Promise((yes, no) => {
    const timer = setTimeout(() => { pending.delete(id); no(new Error(`CDP timeout: ${method}`)); }, Math.max(1, deadline - Date.now()));
    pending.set(id, { yes: value => { clearTimeout(timer); yes(value); }, no: error => { clearTimeout(timer); no(error); } });
    socket.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
  });
}

try {
  child = spawn(browser, args, { windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'] });
  child.stdout.on('data', chunk => { stdout += chunk; }); child.stderr.on('data', chunk => { stderr += chunk; });
  child.once('error', error => { launchError = error; });
  child.once('exit', code => { exitCode = code ?? -1; });
  const endpoint = await waitFor(() => stderr.match(/DevTools listening on (ws:\/\/127\.0\.0\.1:\d+\/devtools\/browser\/[^\s]+)/)?.[1]);
  socket = new WebSocket(endpoint);
  await new Promise((yes, no) => { socket.addEventListener('open', yes, { once: true }); socket.addEventListener('error', no, { once: true }); });
  socket.addEventListener('message', event => {
    const message = JSON.parse(event.data);
    const item = pending.get(message.id);
    if (!item) return;
    pending.delete(message.id);
    if (message.error) item.no(new Error(JSON.stringify(message.error))); else item.yes(message.result);
  });
  const version = await call('Browser.getVersion');
  const { targetId } = await call('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await call('Target.attachToTarget', { targetId, flatten: true });
  await call('Page.enable', {}, sessionId);
  await call('Emulation.setDeviceMetricsOverride', viewport, sessionId);
  await call('Emulation.setEmulatedMedia', { features: [{name: 'prefers-reduced-motion', value: 'no-preference'}] }, sessionId);
  await call('Page.navigate', {url: reviewURL}, sessionId);
  const evaluate = async expression => {const r=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true},sessionId); if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
  await waitFor(()=>evaluate("document.querySelector('#status')?.textContent === 'Normal playback ready'"));
  await evaluate("document.querySelector('#record').click()");
  await waitFor(()=>evaluate("document.querySelector('#status')?.textContent.startsWith('Retained')"));
  const normal=await call('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:true},sessionId);
  await writeFile(join(out,'playback.png'),Buffer.from(normal.data,'base64'));
  const status=await evaluate("document.querySelector('#status').textContent");
  await evaluate("document.querySelector('#stationary').click()");
  await evaluate('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
  const still=await call('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:true},sessionId);
  await writeFile(join(out,'stationary.png'),Buffer.from(still.data,'base64'));
  await writeFile(join(out,'result.json'),JSON.stringify({observed_at:new Date().toISOString(),status,browser:version,viewport,url:reviewURL,scope:'Isolated headless browser running the supplemental 1x/3x playback review. Actual destination capture is separate.'},null,2)+'\n');
  console.log(status);
} finally {
  if (socket?.readyState === WebSocket.OPEN) {
    try { await call('Browser.close'); } catch { /* Process may already have exited. */ }
    socket.close();
  }
  for (const item of pending.values()) item.no(new Error('Capture closed'));
  pending.clear();
  if (child && exitCode === null) {
    const until = Date.now() + 2000;
    while (exitCode === null && Date.now() < until) await pause();
    if (exitCode === null) child.kill();
  }
  await writeFile(join(out, 'browser-process.json'), JSON.stringify({ code: exitCode, stdout, stderr, error: launchError ? String(launchError) : null }, null, 2) + '\n');
  await writeFile(join(out, 'capture-commands.json'), JSON.stringify(commands, null, 2) + '\n');
  // Only remove this process's own resolved temporary profile, never a user profile.
  const actual = await realpath(profile);
  const within = relative(profileParent, actual);
  if (within.startsWith('pixl-render-') && !within.includes(sep) && actual === resolve(profile)) {
    try { await rm(actual, { recursive: true, maxRetries: 4, retryDelay: 250 }); } catch { /* OS-held cache may outlive the browser. */ }
  }
}
