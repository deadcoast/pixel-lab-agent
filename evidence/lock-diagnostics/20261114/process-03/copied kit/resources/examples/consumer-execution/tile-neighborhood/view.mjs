const report = {version: 1, consumer: 'tile-neighborhood-v1', views: [], errors: []};
const cache = new Map(), select = document.querySelector('#neighborhood'), zoom = document.querySelector('#scale'), canvas = document.querySelector('#terrain');
let terrain, tileFor, config;
const digest = async bytes => [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(v => v.toString(16).padStart(2, '0')).join('');
const exact = (value, keys) => value && typeof value === 'object' && !Array.isArray(value) && JSON.stringify(Object.keys(value).sort()) === JSON.stringify([...keys].sort());
const require = (condition, message) => {if (!condition) throw new Error(message);};
const integer = (v, lo, hi) => Number.isInteger(v) && v >= lo && v <= hi;
window.addEventListener('error', e => report.errors.push(e.message));
window.addEventListener('unhandledrejection', e => report.errors.push(String(e.reason)));
async function imageFor(path) {
  const response = await fetch('/' + path);
  require(response.ok, 'Missing tile: ' + path);
  const bytes = await response.arrayBuffer(), image = new Image(), url = URL.createObjectURL(new Blob([bytes], {type: 'image/png'}));
  try {image.src = url; await image.decode();} finally {URL.revokeObjectURL(url);}
  return {path, sha256: await digest(bytes), width: image.naturalWidth, height: image.naturalHeight, image};
}
function validate(value) {
  require(exact(value, ['tile_size', 'background', 'sampling', 'corner_order', 'tiles', 'neighborhoods']), 'Invalid terrain declaration');
  require(Array.isArray(value.tile_size) && value.tile_size.length === 2 && value.tile_size.every(v => integer(v, 1, 64)), 'Tile size must be two bounded positive integers');
  require(value.sampling === 'nearest' && /^#[0-9a-fA-F]{6}$/.test(value.background), 'Explicit nearest sampling and RGB background required');
  require(JSON.stringify(value.corner_order) === JSON.stringify(['nw', 'ne', 'se', 'sw']), 'This profile requires the declared NW/NE/SE/SW corner convention');
  require(exact(value.tiles, Array.from({length: 16}, (_, i) => String(i))), 'Declare all 16 binary-corner tiles');
  const paths = Object.values(value.tiles).map(v => {require(exact(v, ['path']), 'Tile entry must name one path'); return v.path;});
  require(new Set(paths).size === 16 && JSON.stringify([...paths].sort()) === JSON.stringify(Object.values(config.destinations).sort()), 'Tiles and explicit package destinations must match exactly');
  require(Array.isArray(value.neighborhoods) && value.neighborhoods.length > 0 && value.neighborhoods.length <= 16, 'Provide one to 16 neighborhoods');
  const ids = new Set(), patterns = new Set(); let pixels = 0;
  for (const n of value.neighborhoods) {
    require(exact(n, ['id', 'label', 'vertices']) && /^[a-z][a-z0-9-]{0,63}$/.test(n.id) && typeof n.label === 'string' && n.label.length > 0 && n.label.length <= 120 && !ids.has(n.id), 'Neighborhood identity/label must be distinct and bounded'); ids.add(n.id);
    require(Array.isArray(n.vertices) && integer(n.vertices.length, 2, 17) && Array.isArray(n.vertices[0]) && integer(n.vertices[0].length, 2, 17), 'Neighborhood vertex grid must be 2 to 17 rows/columns');
    require(n.vertices.every(row => Array.isArray(row) && row.length === n.vertices[0].length && row.every(v => v === 0 || v === 1)), 'Rectangular binary vertex grid required');
    for (let row = 0; row < n.vertices.length - 1; row++) for (let col = 0; col < n.vertices[0].length - 1; col++) patterns.add(cornersAt(n, row, col).reduce((sum, v, bit) => sum + v * 2 ** bit, 0));
    for (const scale of config.scales) {
      const width = (n.vertices[0].length - 1) * value.tile_size[0] * scale, height = (n.vertices.length - 1) * value.tile_size[1] * scale;
      require(width <= 2048 && height <= 2048, 'Scaled neighborhood exceeds 2048 pixels'); pixels += width * height;
    }
  }
  require(patterns.size === 16, 'Neighborhoods must exercise every binary corner pattern');
  require(pixels <= 16 * 1024 * 1024, 'Requested neighborhood capture exceeds total pixel bound');
}
function cornersAt(n, row, col) {return [n.vertices[row][col], n.vertices[row][col + 1], n.vertices[row + 1][col + 1], n.vertices[row + 1][col]];}
async function paint(id, scale) {
  require(terrain && config.scales.includes(scale), 'Unavailable terrain or scale');
  const n = terrain.neighborhoods.find(v => v.id === id); require(n, 'Unknown neighborhood');
  select.value = id; zoom.value = String(scale); document.querySelector('#label').textContent = n.label;
  const [tw, th] = terrain.tile_size, columns = n.vertices[0].length - 1, rows = n.vertices.length - 1;
  canvas.width = columns * tw * scale; canvas.height = rows * th * scale;
  const context = canvas.getContext('2d', {willReadFrequently: true}); context.imageSmoothingEnabled = false;
  context.fillStyle = terrain.background; context.fillRect(0, 0, canvas.width, canvas.height);
  const cells = [];
  for (let row = 0; row < rows; row++) for (let col = 0; col < columns; col++) {
    const corners = cornersAt(n, row, col), expected = String(corners.reduce((sum, v, bit) => sum + v * 2 ** bit, 0)), selected = tileFor([...corners]);
    require(typeof selected === 'string' && selected === expected, `tileFor mapping differs at ${id}[${row},${col}]: ${String(selected)} versus ${expected}`);
    const asset = cache.get(selected); require(asset, 'Mapped tile unavailable');
    context.drawImage(asset.image, col * tw * scale, row * th * scale, tw * scale, th * scale);
    cells.push({row, column: col, corners, tile: selected, path: asset.path, sha256: asset.sha256});
  }
  await new Promise(yes => requestAnimationFrame(() => requestAnimationFrame(yes)));
  const rect = canvas.getBoundingClientRect();
  return {neighborhood: id, label: n.label, scale, rows, columns, cells, png: canvas.toDataURL(), smoothing: context.imageSmoothingEnabled,
    imageRendering: getComputedStyle(canvas).imageRendering, rect: {x: rect.x, y: rect.y, width: rect.width, height: rect.height}};
}
try {
  config = await (await fetch('/config.json')).json(); report.config = config;
  const module = await import('/' + config.modules.terrain); terrain = module.terrain; tileFor = module.tileFor;
  require(typeof tileFor === 'function', 'Consumer must export tileFor(corners)'); validate(terrain);
  report.terrain = JSON.parse(JSON.stringify(terrain)); report.tile_assets = {};
  for (const [id, tile] of Object.entries(terrain.tiles)) {
    const asset = await imageFor(tile.path);
    require(asset.width === terrain.tile_size[0] && asset.height === terrain.tile_size[1], 'Wrong tile geometry: ' + tile.path);
    cache.set(id, asset); report.tile_assets[id] = {...asset, image: undefined};
  }
  for (const n of terrain.neighborhoods) {const option = document.createElement('option'); option.value = n.id; option.textContent = n.label; select.append(option);}
  for (const scale of config.scales) {const option = document.createElement('option'); option.value = String(scale); option.textContent = scale + 'x'; zoom.append(option);}
  const change = () => paint(select.value, Number(zoom.value)).catch(error => {report.errors.push(String(error)); document.querySelector('#status').textContent = String(error);});
  select.addEventListener('change', change); zoom.addEventListener('change', change);
  await paint(terrain.neighborhoods[0].id, config.scales[0]);
  document.querySelector('#status').textContent = 'All 16 mapped tiles loaded. Material and corner continuity require visual review.';
} catch (error) {report.errors.push(String(error)); document.querySelector('#status').textContent = String(error);}
window.tileSummary = () => report;
window.tileObserve = async (id, scale) => paint(id, scale);
document.body.dataset.ready = 'true';
