import type { QueueState } from "./queue";
export const statusVisuals = {
  idle: { label: "Start", path: "renderer-successor/assets/start.svg", frames: 1 },
  running: { label: "Working", path: "renderer-successor/assets/working.png", frames: 4 },
  paused: { label: "Paused", path: "renderer-successor/assets/paused.png", frames: 1 },
  succeeded: { label: "Ready", path: "renderer-successor/assets/ready-confirmed.png", frames: 1 },
  failed: { label: "Retry", path: "renderer-successor/assets/error-retry.png", frames: 1 },
};
export const display = { cell: [16, 16], scale: 3, filter: "nearest", frameMs: 100, background: "#172336" };
export function statusCell(state: QueueState) { return statusVisuals[state]; }
export function compactStatus(state: QueueState) { return statusVisuals[state]; }
export function accountBadge(registry: Record<string, string>, account: string) {
  return registry[account]; // Provided by the service; not enumerable in this checkout.
}

// Successor preserves descriptors and sheet geometry. Reduced motion changes the
// selected cell, never the backend state, label, asset identity or sheet dimensions.
export const motionQuery = "(prefers-reduced-motion: reduce)";
export function statusFrame(state: QueueState, elapsed: number, reducedMotion: boolean) {
  if (state === "running" && reducedMotion) return 0;
  return Math.floor(Math.max(0, elapsed) / display.frameMs) % statusVisuals[state].frames;
}
