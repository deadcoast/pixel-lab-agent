export type Facing = "south" | "east" | "north" | "west";
export const robotSprites: Record<Facing, string> = {
  south: "assets/robot/south.png", east: "assets/robot/east.png",
  north: "assets/robot/north.png", west: "assets/robot/west.png",
};
export const cell = { width: 32, height: 32, sampling: "nearest" };
export function spriteFor(facing: Facing) { return robotSprites[facing]; }
