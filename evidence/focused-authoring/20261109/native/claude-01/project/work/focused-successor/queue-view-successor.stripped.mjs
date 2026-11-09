// Successor of queue-view.ts for the reduced-motion requirement. queue-view.ts is retained unchanged.
// Same backend state machine (./queue), same shared statusVisuals map and the same two consumers.
                                          
                                                    
export const reducedMotionQuery = "(prefers-reduced-motion: reduce)";
export const statusVisuals = {
  idle: { label: "Start", path: "assets/start.svg", frames: 1, still: 0 },
  running: { label: "Working", path: "assets/working.png", frames: 4, still: 0 },
  paused: { label: "Paused", path: "assets/paused.png", frames: 1, still: 0 },
  succeeded: { label: "Ready", path: "assets/ready-confirmed.png", frames: 1, still: 0 },
  failed: { label: "Retry", path: "assets/error-retry.png", frames: 1, still: 0 },
};
export const display = { cell: [16, 16], scale: 3, filter: "nearest", frameMs: 100, background: "#172336" };
// `frames` is always the sheet's cell count (geometry); `still` is the cell held when motion is reduced.
                                                              
                                                                                                                       
export function motionPreference(query                                          = globalThis.matchMedia?.(reducedMotionQuery))                   {
  return query?.matches ? "reduced" : "normal";
}
export function describe(visual              , motion                  )                   {
  const animate = motion === "normal" && visual.frames > 1;
  return { ...visual, motion, animate, holdFrame: animate ? null : visual.still };
}
export function frameAt(descriptor                  , elapsed        ) {
  return descriptor.animate ? Math.floor(Math.max(elapsed, 0) / display.frameMs) % descriptor.frames : descriptor.holdFrame ?? 0;
}
export function statusCell(state            , motion                   = motionPreference()) { return describe(statusVisuals[state], motion); }
export function compactStatus(state            , motion                   = motionPreference()) { return describe(statusVisuals[state], motion); }
export function accountBadge(registry                        , account        ) {
  return registry[account]; // Provided by the service; not enumerable in this checkout.
}
