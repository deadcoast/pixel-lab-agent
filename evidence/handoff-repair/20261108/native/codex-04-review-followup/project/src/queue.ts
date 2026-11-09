export type QueueState = "idle" | "running" | "succeeded" | "failed" | "paused";
export function stateAfter(result: "started" | "ok" | "error" | "pause"): QueueState {
  return { started: "running", ok: "succeeded", error: "failed", pause: "paused" }[result] as QueueState;
}
