// Execute the actual source consumers; this is not a renderer.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { stateAfter } from './src/queue.ts';
import { statusCell, compactStatus, display } from './src/queue-view.ts';
const expected = process.argv[2];
assert.ok(expected, 'Pass the selected PLAR delivery path');
const state = stateAfter('ok');
assert.equal(state, 'succeeded');
const consumers = [statusCell(state), compactStatus(state)];
for (const consumer of consumers) {
  assert.equal(consumer.path, expected);
  assert.equal(consumer.frames, 1);
}
const data = readFileSync(new URL(expected, import.meta.url));
assert.equal(data.subarray(0,8).toString('hex'), '89504e470d0a1a0a');
assert.deepEqual([data.readUInt32BE(16), data.readUInt32BE(20)], display.cell);
assert.equal(display.filter, 'nearest');
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
console.log(JSON.stringify({state, consumers, display, file: expected,
  sha256: hash(data), sources: Object.fromEntries(['src/queue.ts','src/queue-view.ts'].map(
    p => [p, hash(readFileSync(new URL(p, import.meta.url)))])),
  scope: 'Executed backend-to-view mapping and actual file/header lookup; no renderer, alpha compositing or artistic acceptance.'}, null, 2));
