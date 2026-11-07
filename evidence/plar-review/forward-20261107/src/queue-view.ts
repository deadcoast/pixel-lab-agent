import type { QueueState } from "./queue";
export const statusVisuals = {
  idle: { label: "Start", path: "assets/start.svg", frames: 1 },
  running: { label: "Working", path: "assets/working.png", frames: 4 },
  succeeded: { label: "Ready", path: "assets/ready.png", frames: 1 },
  failed: { label: "Retry", path: "assets/retry.png", frames: 1 },
};
export const display = { cell: [16, 16], scale: 3, filter: "nearest", frameMs: 100, background: "#172336" };
export function statusCell(state: QueueState) { return statusVisuals[state]; }
export function compactStatus(state: QueueState) { return statusVisuals[state]; }
export function accountBadge(registry: Record<string, string>, account: string) {
  return registry[account]; // Provided by the service; not enumerable in this checkout.
}
