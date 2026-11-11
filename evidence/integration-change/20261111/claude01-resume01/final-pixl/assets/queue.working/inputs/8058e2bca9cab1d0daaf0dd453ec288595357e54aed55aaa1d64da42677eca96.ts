import { display as originalDisplay } from "./queue-view.ts";
import { frameMs } from "./working-timing.ts";
export { statusVisuals, statusCell, compactStatus, accountBadge } from "./queue-view.ts";
export const display = { ...originalDisplay, frameMs };
