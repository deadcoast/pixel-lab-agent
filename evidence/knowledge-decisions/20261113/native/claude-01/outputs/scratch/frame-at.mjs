// Scratch re-implementation of the frameAt adapter logic from src/animation.ts.
// Imports nothing from the consumer; the duration arrays below are copied by hand
// from the authored source ([800,120,160,120,400]) and the unadopted proposal (5x100).
// Read-only calculation for the TM-09 decision; it does not change the consumer.
function frameAt(durations, loop, elapsedMs) {
  const duration = durations.reduce((sum, d) => sum + d, 0);
  let at = loop ? Math.max(elapsedMs, 0) % duration
                : Math.min(Math.max(elapsedMs, 0), duration);
  for (let index = 0; index < durations.length; index++) {
    if (at < durations[index]) return index;
    at -= durations[index];
  }
  return durations.length - 1;
}
const times = [0, 799, 800, 919, 920, 1079, 1080, 1199, 1200, 1599, 1600];
const authored = [800, 120, 160, 120, 400];
const uniform = [100, 100, 100, 100, 100];
function boundaries(d) { const b = [0]; for (const x of d) b.push(b[b.length - 1] + x); return b; }
const out = {
  authored: {
    durations_ms: authored,
    total_ms: authored.reduce((a, b) => a + b, 0),
    boundary_times_ms: boundaries(authored),
    frame_at: Object.fromEntries(times.map(t => [t, frameAt(authored, true, t)])),
  },
  uniform_proposal: {
    durations_ms: uniform,
    total_ms: uniform.reduce((a, b) => a + b, 0),
    boundary_times_ms: boundaries(uniform),
    frame_at: Object.fromEntries(times.map(t => [t, frameAt(uniform, true, t)])),
  },
};
console.log(JSON.stringify(out, null, 2));
