export type QueueState = "idle" | "running" | "succeeded" | "failed";
export function stateAfter(result: "started" | "ok" | "error"): QueueState {
  return { started: "running", ok: "succeeded", error: "failed" }[result] as QueueState;
}
