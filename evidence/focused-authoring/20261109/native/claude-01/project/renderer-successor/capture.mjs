// Fresh isolated browser capture driven over the DevTools protocol so the prefers-reduced-motion preference can be
// switched while the same page stays open. No production/profile-wide browser configuration is touched.
// Usage: node renderer-successor/capture.mjs --out NEW_DIR [--project ROOT] [--browser PATH] [--phases a,b,c] [--chrome-flag FLAG]...
// Phases: normal-start (no emulation), reduced (emulate prefers-reduced-motion: reduce), normal-restored (emulate no-preference),
//         as-launched (no emulation; use with --chrome-flag --force-prefers-reduced-motion to test the startup preference).
import { spawn } from 'node:child_process';
import { access, mkdir, readFile, writeFile, mkdtemp, realpath, rm } from 'node:fs/promises';
import { resolve, join, relative, sep } from 'node:path';
import { tmpdir } from 'node:os';
import { serve, rendererRoot, hash } from './server.mjs';

const argv = process.argv.slice(2);
const option = name => { const i = argv.indexOf(name); return i < 0 ? null : argv[i + 1]; };
const options = name => argv.flatMap((value, i) => value === name ? [argv[i + 1]] : []);
const project = resolve(option('--project') || join(rendererRoot, '..'));
const output = option('--out');
if (!output) throw new Error('Use --out NEW_DIRECTORY to retain a fresh capture');
const out = resolve(output);
await mkdir(out, { recursive: false });
const phases = (option('--phases') || 'normal-start,reduced,normal-restored').split(',');
const extraFlags = options('--chrome-flag');
let browser = option('--browser');
if (!browser) {
  for (const file of [join(process.env.PROGRAMFILES || '', 'Google/Chrome/Application/chrome.exe'), join(process.env['ProgramFiles(x86)'] || '', 'Microsoft/Edge/Application/msedge.exe')]) {
    try { await access(file); browser = file; break; } catch { /* Try next installed browser. */ }
  }
}
if (!browser) throw new Error('No local Chromium browser found; pass --browser PATH');
const profileParent = await realpath(tmpdir());
const profile = await mkdtemp(join(profileParent, 'pixl-render-successor-'));
const rendererFiles = Object.fromEntries(await Promise.all(['server.mjs', 'capture.mjs', 'index.html', 'view.mjs', 'check.py'].map(async name => [name, hash(await readFile(join(rendererRoot, name)))])));
const running = await serve(project, null);
const args = ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', '--disable-background-networking', '--force-device-scale-factor=1', `--user-data-dir=${profile}`, '--window-size=1280,1000', '--remote-debugging-port=0', '--remote-allow-origins=*', ...extraFlags, 'about:blank'];
await writeFile(join(out, 'launch.json'), JSON.stringify({ browser, args, phases, project, node: process.version, url: running.url, scope: 'Isolated local fixture renderer driven over the DevTools protocol' }, null, 2) + '\n');
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
let child, stdout = '', stderr = '';
const result = { phases: [] };
try {
  child = spawn(browser, args, { windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'] });
  child.stdout.on('data', chunk => { stdout += chunk; }); child.stderr.on('data', chunk => { stderr += chunk; });
  let port = null;
  for (let i = 0; i < 100 && port === null; i++) {
    try { port = Number((await readFile(join(profile, 'DevToolsActivePort'), 'utf8')).split('\n')[0]); } catch { await sleep(150); }
  }
  if (!port) throw new Error('Browser did not publish a DevTools port');
  let targets = [];
  for (let i = 0; i < 50 && !targets.find(t => t.type === 'page'); i++) {
    try { targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); } catch { /* retry */ }
    if (!targets.find(t => t.type === 'page')) await sleep(100);
  }
  const page = targets.find(t => t.type === 'page');
  if (!page) throw new Error('No page target');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((yes, no) => { ws.addEventListener('open', yes, { once: true }); ws.addEventListener('error', no, { once: true }); });
  let nextId = 1; const pending = new Map();
  ws.addEventListener('message', event => { const message = JSON.parse(event.data); if (message.id && pending.has(message.id)) { const { yes, no } = pending.get(message.id); pending.delete(message.id); message.error ? no(new Error(JSON.stringify(message.error))) : yes(message.result); } });
  const send = (method, params = {}) => new Promise((yes, no) => { const id = nextId++; pending.set(id, { yes, no }); ws.send(JSON.stringify({ id, method, params })); });
  const evaluate = async (expression, awaitPromise = false) => {
    const { result: value, exceptionDetails } = await send('Runtime.evaluate', { expression, awaitPromise, returnByValue: true });
    if (exceptionDetails) throw new Error('Page evaluation failed: ' + JSON.stringify(exceptionDetails).slice(0, 2000));
    return value.value;
  };
  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 1000, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: `${running.url}/` });
  for (let i = 0; i < 200 && !(await evaluate("document.body?.dataset.ready === 'true'")); i++) await sleep(50);
  if (!(await evaluate("document.body?.dataset.ready === 'true'"))) throw new Error('Page did not become ready');
  const emulate = value => send('Emulation.setEmulatedMedia', { media: '', features: [{ name: 'prefers-reduced-motion', value }] });
  const waitMotion = async expected => {
    for (let i = 0; i < 60; i++) { const state = await evaluate('window.queueMotion()'); if (state.motion === expected) return state; await sleep(50); }
    throw new Error(`Preference did not switch to ${expected}`);
  };
  let index = 0;
  for (const phase of phases) {
    let emulated = null;
    if (phase === 'reduced') { await emulate('reduce'); emulated = 'reduce'; await waitMotion('reduced'); }
    else if (phase === 'normal-restored') { await emulate('no-preference'); emulated = 'no-preference'; await waitMotion('normal'); }
    else if (phase !== 'normal-start' && phase !== 'as-launched') throw new Error(`Unknown phase ${phase}`);
    await sleep(450); // Let the live loop run under this preference before sampling.
    const motionBefore = await evaluate('window.queueMotion()');
    const report = await evaluate('window.captureQueue()', true);
    const screenshotData = Buffer.from((await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false })).data, 'base64');
    const screenshotName = `${phase}-destination.png`;
    await writeFile(join(out, screenshotName), screenshotData);
    for (const item of [...report.views, ...report.live, ...report.timeline]) if (item.png) {
      const bytes = Buffer.from(item.png.split(',')[1], 'base64');
      const name = `view-${String(index++).padStart(3, '0')}.png`;
      await writeFile(join(out, name), bytes); item.image = { path: name, sha256: hash(bytes) }; delete item.png;
    }
    result.phases.push({ name: phase, emulated, motionBefore, screenshot: { path: screenshotName, sha256: hash(screenshotData) }, report });
  }
  ws.close();
  result.version = 2; result.browser = browser; result.args = args; result.node = process.version; result.url = running.url;
  result.served_files = Object.fromEntries(running.served);
  for (const [name, expected] of Object.entries(rendererFiles)) if (hash(await readFile(join(rendererRoot, name))) !== expected) throw new Error(`Renderer changed during capture: ${name}`);
  result.renderer_files = rendererFiles;
  result.observed_at = new Date().toISOString();
  result.scope = 'One isolated headless page, no reload between phases; prefers-reduced-motion switched through DevTools media emulation where a phase says so. Mechanical fixture evidence only.';
  await writeFile(join(out, 'render.json'), JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify({ capture: join(out, 'render.json'), phases: result.phases.map(p => ({ name: p.name, motion: p.report.motion, errors: p.report.errors, missing: p.report.missing, events: p.report.preferenceEvents.length })) }));
} finally {
  if (child) { child.kill(); await new Promise(resolve => { child.once('exit', resolve); setTimeout(resolve, 5000); }); }
  await writeFile(join(out, 'browser-process.json'), JSON.stringify({ stdout, stderr, exitCode: child?.exitCode ?? null }, null, 2) + '\n');
  running.server.closeAllConnections(); await new Promise(resolve => running.server.close(resolve));
  // Only remove this process's own resolved temporary profile, never a user profile.
  const actual = await realpath(profile);
  const within = relative(profileParent, actual);
  if (within.startsWith('pixl-render-successor-') && !within.includes(sep) && actual === resolve(profile)) {
    try { await rm(actual, { recursive: true, maxRetries: 4, retryDelay: 250 }); } catch { /* OS-held cache may outlive the browser. */ }
  }
}
