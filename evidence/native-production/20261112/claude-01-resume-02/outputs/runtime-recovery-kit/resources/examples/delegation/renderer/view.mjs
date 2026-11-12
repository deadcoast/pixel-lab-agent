const directions = ['south', 'east', 'north', 'west'];
const report = {version: 1, consumer: 'directional-robot-v1', directions, scales: [1, 3], background: '#172336', views: [], errors: []};
const cache = new Map(), cells = [];
const digest = async bytes => [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(x => x.toString(16).padStart(2, '0')).join('');
window.addEventListener('error', event => report.errors.push(event.message));
window.addEventListener('unhandledrejection', event => report.errors.push(String(event.reason)));

async function imageFor(path) {
  if (!cache.has(path)) cache.set(path, (async () => {
    const response = await fetch('/' + path);
    if (!response.ok) return {path, available: false, status: response.status};
    const bytes = await response.arrayBuffer(), image = new Image();
    const url = URL.createObjectURL(new Blob([bytes], {type: 'image/png'}));
    try { image.src = url; await image.decode(); } finally { URL.revokeObjectURL(url); }
    return {path, available: true, sha256: await digest(bytes), width: image.naturalWidth, height: image.naturalHeight, image};
  })());
  return cache.get(path);
}

try {
  const {robotSprites, cell, spriteFor} = await import('/src/robot.ts');
  report.cell = cell;
  report.controller_inventory = Object.keys(robotSprites);
  report.controller_mapping = robotSprites;
  report.selected_mapping = Object.fromEntries(directions.map(d => [d, spriteFor(d)]));
  if (cell.width !== 32 || cell.height !== 32 || cell.sampling !== 'nearest') report.errors.push('Controller cell differs from the 32px nearest contract');
  if (JSON.stringify(Object.keys(robotSprites).sort()) !== JSON.stringify([...directions].sort())) report.errors.push('Controller inventory differs from four required directions');
  for (const direction of directions) {
    const path = spriteFor(direction), expected = `assets/robot/${direction}.png`;
    if (path !== expected || robotSprites[direction] !== expected) report.errors.push(`Wrong controller mapping for ${direction}: ${path}`);
  }
  const base = await imageFor('assets/robot-base.png');
  report.base = {...base, image: undefined};
  const matrix = document.querySelector('#matrix');
  for (const direction of directions) {
    const label = document.createElement('span'); label.textContent = direction; matrix.append(label);
    const asset = await imageFor(spriteFor(direction));
    for (const scale of report.scales) {
      const node = document.createElement('div'); node.className = 'cell'; matrix.append(node);
      const view = {direction, scale, path: spriteFor(direction), asset: {...asset, image: undefined}, geometryMatches: asset.width === 32 && asset.height === 32};
      report.views.push(view);
      if (!asset.available || !view.geometryMatches) {
        node.classList.add('missing'); node.textContent = asset.available ? 'Wrong dimensions' : 'Missing image'; continue;
      }
      const canvas = document.createElement('canvas'); canvas.width = 32 * scale; canvas.height = 32 * scale;
      canvas.setAttribute('aria-label', `${direction} ${scale}x`); node.append(canvas);
      const context = canvas.getContext('2d', {willReadFrequently: true}); context.imageSmoothingEnabled = false;
      context.fillStyle = report.background; context.fillRect(0, 0, canvas.width, canvas.height);
      context.drawImage(asset.image, 0, 0, canvas.width, canvas.height);
      cells.push({view, canvas, context});
    }
  }
  const south = await imageFor(spriteFor('south'));
  report.south_matches_base = base.available && south.available && base.sha256 === south.sha256;
  if (!report.south_matches_base) report.errors.push('South does not preserve the exact original source bytes');
  if (report.views.some(v => !v.geometryMatches || !v.asset.available)) report.errors.push('One or more mapped directions is missing or has wrong geometry');
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  for (const {view, canvas, context} of cells) {
    const rect = canvas.getBoundingClientRect();
    Object.assign(view, {png: canvas.toDataURL(), smoothing: context.imageSmoothingEnabled, imageRendering: getComputedStyle(canvas).imageRendering, rect: {x: rect.x, y: rect.y, width: rect.width, height: rect.height}});
  }
} catch (error) { report.errors.push(String(error)); }
window.robotCapture = () => report;
document.querySelector('#status').textContent = report.errors.length ? report.errors.join('; ') : 'All four controller paths loaded. Identity and directional art quality require visual review.';
document.body.dataset.ready = 'true';
