"""Controlled synthetic sprite pixels for tooling probes, never art acceptance."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from PIL import Image, ImageDraw


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def fixture(root):
    root = Path(root)
    (root / "src").mkdir(parents=True, exist_ok=True)
    (root / "assets/motion").mkdir(parents=True, exist_ok=True)
    frames, destinations = [], {}
    for index, duration in enumerate((120, 180, 120, 240)):
        path = f"assets/motion/frame-{index}.png"
        image = Image.new("RGBA", (20, 18))
        draw = ImageDraw.Draw(image)
        # A conspicuous atlas border must be excluded by the declared crop.
        draw.rectangle((0, 0, 19, 17), outline=(255, 0, 255, 255))
        draw.rectangle((6+index, 3, 10+index, 13), fill=(42+index*40, 170, 210, 255))
        draw.rectangle((5, 14, 14, 15), fill=(100, 200, 80, 255))
        draw.point((7, 5), fill=(245, 210, 70, 128))
        image.save(root / path)
        destinations[f"motion.frame{index}"] = path
        frames.append({"id":f"pose-{index}","path":path,"rect":[2,1,16,16],"duration_ms":duration,"pivot":[8+index%2,14]})
    animation = {"viewport":[40,36],"background":"#172336","sampling":"nearest","clips":[
        {"id":"loop","label":"Synthetic loop","loop":True,"anchor":[20,28],"frames":frames},
        {"id":"once","label":"Synthetic one shot","loop":False,"anchor":[18,27],"frames":copy.deepcopy(frames)}]}
    module = "export const animation = " + json.dumps(animation, indent=2) + ";\n" + """
export function frameAt(clipId, elapsedMs) {
  const clip = animation.clips.find(value => value.id === clipId);
  if (!clip) throw new Error('Unknown clip');
  const duration = clip.frames.reduce((sum, frame) => sum + frame.duration_ms, 0);
  let at = clip.loop ? Math.max(elapsedMs, 0) % duration : Math.min(Math.max(elapsedMs, 0), duration);
  for (let index = 0; index < clip.frames.length; index++) {
    if (at < clip.frames[index].duration_ms) return index;
    at -= clip.frames[index].duration_ms;
  }
  return clip.frames.length - 1;
}
"""
    (root / "src/animation.ts").write_text(module, encoding="utf-8")
    config = {"version":1,"profile":"sprite-animation-v1","modules":{"animation":"src/animation.ts"},"destinations":destinations,"scales":[1,3],"observed_wraps":2,"phase_timeout_ms":10000,"timeout_seconds":90}
    write_json(root / "config.json", config)
    (root / "SYNTHETIC-TEST.md").write_text("Synthetic mechanical animation diagnostic, including atlas borders and partial alpha. No motion/art or human acceptance is claimed.\n",encoding="utf-8")
    return config
