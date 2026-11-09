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
let observed;
const running = await serve(project, report => { if (observed) throw new Error('Duplicate capture'); observed = report; });
const args = ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', '--disable-background-networking', '--force-device-scale-factor=1', `--user-data-dir=${profile}`, '--window-size=1280,1000', '--virtual-time-budget=4000', '--run-all-compositor-stages-before-draw', `--screenshot=${join(out, 'destination.png')}`, `${running.url}/?capture=1`];
await writeFile(join(out, 'launch.json'), JSON.stringify({ browser, args, project, node: process.version, scope: 'Isolated local fixture renderer' }, null, 2) + '\n');
let processResult;
try {
  processResult = await new Promise((yes, no) => {
    const child = spawn(browser, args, { windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '', stderr = '';
    child.stdout.on('data', chunk => { stdout += chunk; }); child.stderr.on('data', chunk => { stderr += chunk; });
    const timer = setTimeout(() => { child.kill(); no(new Error('Browser capture exceeded 45 seconds')); }, 45_000);
    child.once('error', error => { clearTimeout(timer); no(error); });
    child.once('exit', code => { clearTimeout(timer); yes({ code, stdout, stderr }); });
  });
  await writeFile(join(out, 'browser-process.json'), JSON.stringify(processResult, null, 2) + '\n');
  if (processResult.code !== 0 || !observed) throw new Error('Browser did not return a complete capture');
  const screenshot = await readFile(join(out, 'destination.png'));
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
  running.server.closeAllConnections(); await new Promise(yes => running.server.close(yes));
  // Only remove this process's own resolved temporary profile, never a user profile.
  const actual = await realpath(profile);
  const within = relative(profileParent, actual);
  if (within.startsWith('pixl-render-') && !within.includes(sep) && actual === resolve(profile)) {
    try { await rm(actual, { recursive: true, maxRetries: 4, retryDelay: 250 }); } catch { /* OS-held cache may outlive the browser. */ }
  }
}
