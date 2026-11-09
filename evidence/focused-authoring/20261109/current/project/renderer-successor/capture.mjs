// Fresh isolated browser capture. No production/profile-wide browser configuration.
import { spawn } from 'node:child_process';
import { access, mkdir, readFile, writeFile, mkdtemp, realpath, rm } from 'node:fs/promises';
import { resolve, join, relative, sep } from 'node:path';
import { tmpdir } from 'node:os';
import { serve, rendererRoot, hash } from './server.mjs';

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
const running = await serve(project, report => { if (observed) throw new Error('Duplicate capture'); observed = report; });
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
  await call('Page.navigate', { url: `${running.url}/?capture=1` }, sessionId);
  await waitFor(() => observed);
  await waitFor(async () => (await call('Runtime.evaluate', { expression: 'document.body.dataset.captureComplete === "true"', returnByValue: true }, sessionId)).result.value);
  await call('Runtime.evaluate', { expression: 'new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve(true))))', awaitPromise: true, returnByValue: true }, sessionId);
  const evaluate = async expression => {
    const value = await call('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true }, sessionId);
    if (value.exceptionDetails) throw new Error(JSON.stringify(value.exceptionDetails));
    return value.result.value;
  };
  const settle = 'new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve(true))))';
  const phases = [];
  await evaluate("window.selectQueue('started')");
  async function samplePhase(name, reduced) {
    await call('Emulation.setEmulatedMedia', {features:[{name:'prefers-reduced-motion',value:reduced?'reduce':'no-preference'}]}, sessionId);
    await evaluate(settle);
    const samples=[];
    for (let i=0;i<40;i++) {
      samples.push(await evaluate('window.motionSnapshot()'));
      await new Promise(resolve=>setTimeout(resolve,25));
    }
    const screenshot=await call('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false},sessionId);
    await writeFile(join(out,`${name}.png`),Buffer.from(screenshot.data,'base64'));
    phases.push({name,reduced,samples,screenshot:{path:`${name}.png`,sha256:hash(Buffer.from(screenshot.data,'base64'))}});
  }
  await samplePhase('normal-before',false);
  await samplePhase('reduced-live',true);
  const reducedReport = await evaluate('window.captureQueue()');
  await writeFile(join(out,'reduced-render.raw.json'),JSON.stringify(reducedReport,null,2)+'\n');
  await evaluate("window.selectQueue('started')");
  await samplePhase('normal-after',false);
  let motionIndex=0;
  for (const phase of phases) for (const sample of phase.samples) for (const cell of sample.cells) if(cell.png) {
    const bytes=Buffer.from(cell.png.split(',')[1],'base64');
    const name=`motion-${String(motionIndex++).padStart(3,'0')}.png`;
    await writeFile(join(out,name),bytes); cell.image={path:name,sha256:hash(bytes)};delete cell.png;
  }
  await writeFile(join(out,'motion.json'),JSON.stringify({phases,scope:'Real requestAnimationFrame samples, actual matchMedia media preference changes through CDP in same page; observed wall-clock sample times are retained, not exact scheduling guarantees.'},null,2)+'\n');
  await evaluate("window.selectQueue('ok')");
  await evaluate(settle);
  const layout = await call('Page.getLayoutMetrics', {}, sessionId);
  const result = await call('Page.captureScreenshot', { format: 'png', fromSurface: true, captureBeyondViewport: false }, sessionId);
  const screenshot = Buffer.from(result.data, 'base64');
  await writeFile(join(out, 'destination.png'), screenshot);
  observed.browser_version = version;
  observed.capture_layout = layout;
  observed.capture_method = 'CDP metrics before navigation, page report, layout, screenshot in the same page session';
  let index = 0;
  for (const item of [...observed.views, ...observed.timeline]) if (item.png) {
    const bytes = Buffer.from(item.png.split(',')[1], 'base64');
    const name = `view-${String(index++).padStart(3, '0')}.png`;
    await writeFile(join(out, name), bytes); item.image = { path: name, sha256: hash(bytes) }; delete item.png;
  }
  observed.served_files = Object.fromEntries(running.served);
  for (const [name, expected] of Object.entries(rendererFiles)) if (hash(await readFile(join(rendererRoot, name))) !== expected) throw new Error(`Renderer changed during capture: ${name}`);
  observed.renderer_files = rendererFiles;
  observed.screenshot = { path: 'destination.png', sha256: hash(screenshot) };
  observed.observed_at = new Date().toISOString();
  await writeFile(join(out, 'render.json'), JSON.stringify(observed, null, 2) + '\n');
  console.log(JSON.stringify({ capture: join(out, 'render.json'), screenshot: join(out, 'destination.png'), missing: observed.missing, errors: observed.errors }));
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
  running.server.closeAllConnections(); await new Promise(yes => running.server.close(yes));
  // Only remove this process's own resolved temporary profile, never a user profile.
  const actual = await realpath(profile);
  const within = relative(profileParent, actual);
  if (within.startsWith('pixl-render-') && !within.includes(sep) && actual === resolve(profile)) {
    try { await rm(actual, { recursive: true, maxRetries: 4, retryDelay: 250 }); } catch { /* OS-held cache may outlive the browser. */ }
  }
}
