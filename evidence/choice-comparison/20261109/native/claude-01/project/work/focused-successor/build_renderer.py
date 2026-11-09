"""Versioned consumer; never changes old source, renderer or artwork."""
from pathlib import Path
import shutil

root = Path.cwd()
out = root / 'renderer-successor'
out.mkdir(exist_ok=False)
for name in ['index.html', 'server.mjs', 'capture.mjs', 'check.py', 'view.mjs']:
    shutil.copyfile(root / 'renderer-recheck' / name if (root / 'renderer-recheck' / name).exists() else root / 'renderer' / name, out / name)
source = (root / 'src/queue-view.ts').read_text(encoding='utf-8')
source += '''
// Successor preserves descriptors and sheet geometry. Reduced motion changes the
// selected cell, never the backend state, label, asset identity or sheet dimensions.
export const motionQuery = "(prefers-reduced-motion: reduce)";
export function statusFrame(state: QueueState, elapsed: number, reducedMotion: boolean) {
  if (state === "running" && reducedMotion) return 0;
  return Math.floor(Math.max(0, elapsed) / display.frameMs) % statusVisuals[state].frames;
}
'''
(root / 'src/queue-view-successor.ts').write_text(source, encoding='utf-8')
p = out / 'view.mjs'
s = p.read_text(encoding='utf-8').replace("display } from '/src/queue-view.ts'", "display, motionQuery, statusFrame } from '/src/queue-view-successor.ts'")
s = s.replace('const panel = display.background;', '''const motion = matchMedia(motionQuery);
const preferenceChanges = [];
const panel = display.background;''')
s = s.replace('function paint(canvas, asset, frames, scale, elapsed)', 'function paint(canvas, asset, frames, scale, elapsed, state)')
s = s.replace('const frame = Math.floor(Math.max(elapsed, 0) / display.frameMs) % frames;', 'const frame = statusFrame(state, elapsed, motion.matches);')
s = s.replace('descriptor.frames, scale, elapsed)', 'descriptor.frames, scale, elapsed, state)')
s = s.replace('cell.scale, now - origin)', 'cell.scale, now - origin, cell.state)')
needle = "requestAnimationFrame(animate);\n\nasync function capture()"
s = s.replace(needle, '''requestAnimationFrame(animate);
motion.addEventListener('change', async () => {
  origin = performance.now();
  for (const cell of [...cells, ...liveCells]) if (cell.canvas) {
    const asset = await cache.get(cell.descriptor.path);
    cell.frame = paint(cell.canvas, asset, cell.descriptor.frames, cell.scale, 0, cell.state);
  }
  preferenceChanges.push({ reduced: motion.matches, at: performance.now() });
});
window.successorReady = true;
window.selectQueue = select;
window.motionSnapshot = () => ({ reduced: motion.matches, changes: [...preferenceChanges],
  at: performance.now(), cells: liveCells.map(cell => ({ consumer: cell.consumer,
    state: cell.state, frame: cell.frame, path: cell.descriptor.path, label: cell.descriptor.label,
    width: cell.canvas?.width, height: cell.canvas?.height,
    smoothing: cell.canvas?.getContext('2d').imageSmoothingEnabled,
    png: cell.canvas?.toDataURL() })) });

async function capture()''')
s = s.replace('return { version: 1, userAgent:', 'return { reduced: motion.matches, preferenceChanges: [...preferenceChanges], version: 2, userAgent:')
p.write_text(s, encoding='utf-8')
print('Created versioned successor source and renderer; asset destinations await reviewed proposal.')
