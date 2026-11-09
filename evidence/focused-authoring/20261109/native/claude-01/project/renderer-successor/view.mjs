// Successor fixture: executes the actual src/queue.ts and src/queue-view-successor.ts modules and follows the
// prefers-reduced-motion media query, including changes while the page stays open. renderer/view.mjs is retained unchanged.
import { stateAfter } from '/src/queue.ts';
import { statusVisuals, statusCell, compactStatus, display, reducedMotionQuery, motionPreference, frameAt } from '/src/queue-view-successor.ts';

const panel = display.background;
document.documentElement.style.setProperty('--panel', panel);
const sessionId = crypto.randomUUID(); // Same value across every capture of one open page: proves no reload between preference switches.
const cache = new Map();
const decoded = new Map();
const cells = [];
const consumers = { statusCell, compactStatus };
const media = matchMedia(reducedMotionQuery);
let motion = motionPreference(media);
const preferenceEvents = [];
const events = ['idle', 'started', 'pause', 'ok', 'error'].filter(event => event === 'idle' || statusVisuals[stateAfter(event)]);
document.querySelectorAll('[data-event]').forEach(button => { button.hidden = !events.includes(button.dataset.event); });
const errors = [];
window.addEventListener('error', event => errors.push(event.message));
window.addEventListener('unhandledrejection', event => errors.push(String(event.reason)));
const digest = async bytes => [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(x => x.toString(16).padStart(2, '0')).join('');
const motionText = () => `Motion: ${motion} (${reducedMotionQuery} ${media.matches ? 'matches' : 'does not match'})`;
document.querySelector('#motion').textContent = motionText();

async function imageFor(path) {
  if (!cache.has(path)) cache.set(path, (async () => {
    const response = await fetch(`/${path}`);
    if (!response.ok) { const asset = { available: false, status: response.status, path }; decoded.set(path, asset); return asset; }
    const data = await response.arrayBuffer();
    const image = new Image();
    const url = URL.createObjectURL(new Blob([data], { type: response.headers.get('Content-Type') }));
    try { image.src = url; await image.decode(); }
    finally { URL.revokeObjectURL(url); }
    const asset = { available: true, image, path, sha256: await digest(data), width: image.naturalWidth, height: image.naturalHeight };
    decoded.set(path, asset);
    return asset;
  })());
  return cache.get(path);
}

function paint(canvas, asset, descriptor, scale, elapsed) {
  const [width, height] = display.cell;
  const frame = frameAt(descriptor, elapsed);
  const context = canvas.getContext('2d', { willReadFrequently: true });
  context.imageSmoothingEnabled = display.filter !== 'nearest';
  context.fillStyle = panel;
  context.fillRect(0, 0, canvas.width, canvas.height);
  if (asset.available && asset.width === width * descriptor.frames && asset.height === height) {
    context.drawImage(asset.image, frame * width, 0, width, height, 0, 0, width * scale, height * scale);
  }
  return frame;
}

const publicDescriptor = descriptor => ({ ...descriptor });

async function makeCell(consumer, state, scale, elapsed = 0, track = true) {
  const descriptor = consumers[consumer](state, motion);
  const asset = await imageFor(descriptor.path);
  const node = document.createElement('div');
  node.className = `cell ${consumer === 'compactStatus' ? 'compact' : ''}`;
  const glyph = document.createElement('span'); glyph.className = 'glyph';
  const label = document.createElement('span'); label.textContent = descriptor.label;
  node.append(glyph, label);
  const info = { consumer, state, scale, motion, descriptor: publicDescriptor(descriptor), asset: { ...asset, image: undefined }, node, canvas: null, frame: 0 };
  if (asset.available) {
    const canvas = document.createElement('canvas');
    canvas.width = display.cell[0] * scale; canvas.height = display.cell[1] * scale;
    canvas.setAttribute('aria-label', `${descriptor.label} icon`);
    info.canvas = canvas; info.frame = paint(canvas, asset, descriptor, scale, elapsed);
    info.geometryMatches = asset.width === display.cell[0] * descriptor.frames && asset.height === display.cell[1];
    glyph.append(canvas);
    if (!info.geometryMatches) { const warning = document.createElement('span'); warning.className = 'missing'; warning.textContent = 'Wrong sheet size'; node.append(warning); }
  } else {
    glyph.classList.add('missing'); glyph.textContent = 'Missing asset';
  }
  if (track) cells.push(info);
  return info;
}

// Re-derive a tracked cell from the same consumer under the current preference and repaint it in place.
function refresh(cell, elapsed) {
  const descriptor = consumers[cell.consumer](cell.state, motion);
  cell.descriptor = publicDescriptor(descriptor); cell.motion = motion;
  const asset = decoded.get(descriptor.path);
  if (cell.canvas && asset) cell.frame = paint(cell.canvas, asset, descriptor, cell.scale, elapsed);
  return { consumer: cell.consumer, state: cell.state, scale: cell.scale, live: liveCells.includes(cell), animate: descriptor.animate, holdFrame: descriptor.holdFrame, frame: cell.frame };
}

const matrix = document.querySelector('#matrix');
for (const text of ['State', 'Full · 1×', `Full · ${display.scale}×`, 'Compact · 1×', `Compact · ${display.scale}×`]) {
  const node = document.createElement('div'); node.className = 'heading'; node.textContent = text; matrix.append(node);
}
for (const state of Object.keys(statusVisuals)) {
  const label = document.createElement('div'); label.className = 'row-label'; label.textContent = state; matrix.append(label);
  for (const consumer of Object.keys(consumers)) for (const scale of [1, display.scale]) matrix.append((await makeCell(consumer, state, scale)).node);
}
const missing = [...cache.keys()].filter(path => !cells.find(cell => cell.descriptor.path === path)?.asset.available);
document.querySelector('#coverage').textContent = missing.length ? `${missing.length} status assets are still missing: ${missing.join(', ')}` : 'Every mapped status asset is available; visual review remains separate.';

let livePromise;
let liveCells = [];
let origin = performance.now();
async function select(event) {
  const state = event === 'idle' ? 'idle' : stateAfter(event);
  liveCells = await Promise.all(Object.keys(consumers).map(consumer => makeCell(consumer, state, display.scale, 0, false)));
  document.querySelector('#live').replaceChildren(...liveCells.map(cell => cell.node));
  document.querySelector('#live-title').textContent = `Current queue state · ${state}`;
  origin = performance.now();
  return { event, state, motion, consumers: liveCells.map(({ consumer, descriptor, asset }) => ({ consumer, descriptor, available: asset.available, sha256: asset.sha256 })) };
}
document.querySelectorAll('[data-event]').forEach(button => button.addEventListener('click', () => { livePromise = select(button.dataset.event); }));
await select('ok');

media.addEventListener('change', () => {
  const before = motion;
  motion = motionPreference(media);
  const now = performance.now();
  const repainted = [...cells, ...liveCells].map(cell => refresh(cell, cell.scale === display.scale && liveCells.includes(cell) ? now - origin : 0));
  document.querySelector('#motion').textContent = motionText();
  preferenceEvents.push({ at: now, sessionId, matches: media.matches, from: before, to: motion, repainted });
});

function animate(now) {
  for (const cell of liveCells) if (cell.canvas && cell.descriptor.animate) {
    const asset = decoded.get(cell.descriptor.path);
    if (asset) cell.frame = paint(cell.canvas, asset, cell.descriptor, cell.scale, now - origin);
  }
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);

async function capture() {
  await document.fonts.ready;
  const transitions = [];
  for (const event of events) {
    const button = document.querySelector(`[data-event="${event}"]`);
    button.click(); transitions.push(await livePromise);
  }
  document.querySelector('[data-event="started"]').click(); await livePromise;
  await new Promise(resolve => setTimeout(resolve, 250)); // Let the live loop run under the current preference before sampling.
  const timeline = [];
  for (const state of Object.keys(statusVisuals)) {
    if (statusVisuals[state].frames <= 1) continue;
    const boundaries = Array.from({ length: statusVisuals[state].frames }, (_, i) => [i * display.frameMs, (i + 1) * display.frameMs - 1]).flat();
    for (const consumer of Object.keys(consumers)) for (const elapsed of [...boundaries, display.frameMs * statusVisuals[state].frames]) {
      const cell = await makeCell(consumer, state, 1, elapsed, false);
      timeline.push({ consumer, state, motion, elapsed, available: cell.asset.available, descriptor: cell.descriptor, frame: cell.canvas ? cell.frame : null, png: cell.canvas?.toDataURL() });
    }
  }
  const snapshot = ({ node, canvas, ...info }) => ({ ...info, canvas: undefined,
    smoothing: canvas?.getContext('2d').imageSmoothingEnabled,
    bounds: canvas ? Object.fromEntries(['x', 'y', 'width', 'height'].map(key => [key, canvas.getBoundingClientRect()[key]])) : null,
    imageRendering: canvas ? getComputedStyle(canvas).imageRendering : null,
    png: canvas?.toDataURL(),
  });
  const views = cells.map(snapshot);
  const live = liveCells.map(cell => ({ ...snapshot(cell), elapsed: performance.now() - origin }));
  return { version: 2, sessionId, userAgent: navigator.userAgent, devicePixelRatio, viewport: { width: innerWidth, height: innerHeight, clientWidth: document.documentElement.clientWidth }, display, reducedMotionQuery,
    motion, mediaMatches: media.matches, motionText: document.querySelector('#motion').textContent, preferenceEvents: preferenceEvents.map(event => ({ ...event })), transitions, timeline, views, live, missing, errors,
    scope: 'Actual browser execution of the successor queue modules, decode, canvas crop/scale/compositing, DOM event handlers and the prefers-reduced-motion media query. Image provenance and visual/style acceptance are separate.' };
}
window.captureQueue = capture;
window.queueMotion = () => ({ sessionId, motion, matches: media.matches, events: preferenceEvents.length });
document.body.dataset.ready = 'true';
if (new URL(location.href).searchParams.has('capture')) {
  const report = await capture();
  await fetch('/__capture', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(report) });
  document.body.dataset.captureComplete = 'true';
}
