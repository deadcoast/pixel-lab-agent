import { stateAfter } from '/src/queue.ts';
import { statusVisuals, statusCell, compactStatus, display, motionQuery, statusFrame } from '/src/queue-view-successor.ts';

const motion = matchMedia(motionQuery);
const preferenceChanges = [];
let observedReduced = motion.matches;
const panel = display.background;
document.documentElement.style.setProperty('--panel', panel);
const cache = new Map();
const cells = [];
const consumers = { statusCell, compactStatus };
const events = ['idle', 'started', 'pause', 'ok', 'error'].filter(event => event === 'idle' || statusVisuals[stateAfter(event)]);
document.querySelectorAll('[data-event]').forEach(button => { button.hidden = !events.includes(button.dataset.event); });
const errors = [];
window.addEventListener('error', event => errors.push(event.message));
window.addEventListener('unhandledrejection', event => errors.push(String(event.reason)));
const digest = async bytes => [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(x => x.toString(16).padStart(2, '0')).join('');

async function imageFor(path) {
  if (!cache.has(path)) cache.set(path, (async () => {
    const response = await fetch(`/${path}`);
    if (!response.ok) return { available: false, status: response.status, path };
    const data = await response.arrayBuffer();
    const image = new Image();
    const url = URL.createObjectURL(new Blob([data], { type: response.headers.get('Content-Type') }));
    try { image.src = url; await image.decode(); }
    finally { URL.revokeObjectURL(url); }
    return { available: true, image, path, sha256: await digest(data), width: image.naturalWidth, height: image.naturalHeight };
  })());
  return cache.get(path);
}

function paint(canvas, asset, frames, scale, elapsed, state) {
  const [width, height] = display.cell;
  const frame = statusFrame(state, elapsed, motion.matches);
  const context = canvas.getContext('2d', { willReadFrequently: true });
  context.imageSmoothingEnabled = display.filter !== 'nearest';
  context.fillStyle = panel;
  context.fillRect(0, 0, canvas.width, canvas.height);
  if (asset.available && asset.width === width * frames && asset.height === height) {
    context.drawImage(asset.image, frame * width, 0, width, height, 0, 0, width * scale, height * scale);
  }
  return frame;
}

async function makeCell(consumer, state, scale, elapsed = 0, track = true) {
  const descriptor = consumers[consumer](state);
  const asset = await imageFor(descriptor.path);
  const node = document.createElement('div');
  node.className = `cell ${consumer === 'compactStatus' ? 'compact' : ''}`;
  const glyph = document.createElement('span'); glyph.className = 'glyph';
  const label = document.createElement('span'); label.textContent = descriptor.label;
  node.append(glyph, label);
  const info = { consumer, state, scale, descriptor, asset: { ...asset, image: undefined }, node, canvas: null, frame: 0 };
  if (asset.available) {
    const canvas = document.createElement('canvas');
    canvas.width = display.cell[0] * scale; canvas.height = display.cell[1] * scale;
    canvas.setAttribute('aria-label', `${descriptor.label} icon`);
    info.canvas = canvas; info.frame = paint(canvas, asset, descriptor.frames, scale, elapsed, state);
    info.geometryMatches = asset.width === display.cell[0] * descriptor.frames && asset.height === display.cell[1];
    glyph.append(canvas);
    if (!info.geometryMatches) { const warning = document.createElement('span'); warning.className = 'missing'; warning.textContent = 'Wrong sheet size'; node.append(warning); }
  } else {
    glyph.classList.add('missing'); glyph.textContent = 'Missing asset';
  }
  if (track) cells.push(info);
  return info;
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
  return { event, state, consumers: liveCells.map(({ consumer, descriptor, asset }) => ({ consumer, descriptor, available: asset.available, sha256: asset.sha256 })) };
}
document.querySelectorAll('[data-event]').forEach(button => button.addEventListener('click', () => { livePromise = select(button.dataset.event); }));
await select('ok');
function animate(now) {
  // Some embedded/headless hosts update .matches without dispatching change.
  // This shares the existing loop, preserving one animation scheduler.
  applyMotionPreference('animation-frame');
  for (const cell of liveCells) if (cell.canvas && cell.descriptor.frames > 1) {
    cache.get(cell.descriptor.path).then(asset => { cell.frame = paint(cell.canvas, asset, cell.descriptor.frames, cell.scale, now - origin, cell.state); });
  }
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
function applyMotionPreference(route) {
  if (observedReduced === motion.matches) return;
  observedReduced = motion.matches;
  origin = performance.now();
  preferenceChanges.push({ reduced: observedReduced, at: origin, route });
  for (const cell of [...cells, ...liveCells]) if (cell.canvas) {
    cache.get(cell.descriptor.path).then(asset => {
      cell.frame = paint(cell.canvas, asset, cell.descriptor.frames, cell.scale, 0, cell.state);
    });
  }
}
motion.addEventListener('change', () => applyMotionPreference('media-change-event'));
window.successorReady = true;
window.selectQueue = select;
window.motionSnapshot = () => ({ reduced: motion.matches, changes: [...preferenceChanges],
  errors: [...errors], matrixWorking: cells.filter(cell => cell.state === 'running').map(cell => ({ consumer: cell.consumer, scale: cell.scale, frame: cell.frame, png: cell.canvas?.toDataURL() })),
  at: performance.now(), cells: liveCells.map(cell => ({ consumer: cell.consumer,
    state: cell.state, frame: cell.frame, path: cell.descriptor.path, label: cell.descriptor.label,
    width: cell.canvas?.width, height: cell.canvas?.height,
    smoothing: cell.canvas?.getContext('2d').imageSmoothingEnabled,
    png: cell.canvas?.toDataURL() })) });

async function capture() {
  await document.fonts.ready;
  const transitions = [];
  for (const event of events) {
    const button = document.querySelector(`[data-event="${event}"]`);
    button.click(); transitions.push(await livePromise);
  }
  document.querySelector('[data-event="ok"]').click(); await livePromise;
  const timeline = [];
  for (const state of Object.keys(statusVisuals)) {
    const descriptor = statusCell(state);
    if (descriptor.frames <= 1) continue;
    const boundaries = Array.from({ length: descriptor.frames }, (_, i) => [i * display.frameMs, (i + 1) * display.frameMs - 1]).flat();
    for (const elapsed of [...boundaries, display.frameMs * descriptor.frames]) {
      const cell = await makeCell('statusCell', state, 1, elapsed, false);
      timeline.push({ state, elapsed, available: cell.asset.available, frame: cell.canvas ? cell.frame : null, png: cell.canvas?.toDataURL() });
    }
  }
  const views = cells.map(({ node, canvas, ...info }) => ({ ...info, canvas: undefined,
    smoothing: canvas?.getContext('2d').imageSmoothingEnabled,
    bounds: canvas ? Object.fromEntries(['x', 'y', 'width', 'height'].map(key => [key, canvas.getBoundingClientRect()[key]])) : null,
    imageRendering: canvas ? getComputedStyle(canvas).imageRendering : null,
    png: canvas?.toDataURL(),
  }));
  return { reduced: motion.matches, preferenceChanges: [...preferenceChanges], version: 2, userAgent: navigator.userAgent, devicePixelRatio, viewport: { width: innerWidth, height: innerHeight, clientWidth: document.documentElement.clientWidth }, display, transitions, timeline, views, missing, errors,
    scope: 'Actual browser execution of the supplied queue modules, decode, canvas crop/scale/compositing and DOM event handlers. Image provenance and visual/style acceptance are separate.' };
}
window.captureQueue = capture;
if (new URL(location.href).searchParams.has('capture')) {
  const report = await capture();
  await fetch('/__capture', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(report) });
  document.body.dataset.captureComplete = 'true';
}
