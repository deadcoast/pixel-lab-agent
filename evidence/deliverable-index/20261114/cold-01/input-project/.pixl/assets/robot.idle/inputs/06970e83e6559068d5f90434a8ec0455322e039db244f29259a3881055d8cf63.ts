// Prospective consumer contract: the five animation files do not exist yet.
// Actual production and review must supply them; no placeholders are accepted.
export const animation = {
  "viewport": [
    48,
    40
  ],
  "background": "#172336",
  "sampling": "nearest",
  "clips": [
    {
      "id": "east-idle",
      "label": "Planted panel idle",
      "loop": true,
      "anchor": [
        24,
        34
      ],
      "frames": [
        {
          "id": "east-0",
          "path": "assets/robot-idle/east-0.png",
          "rect": [
            0,
            0,
            32,
            32
          ],
          "duration_ms": 800,
          "pivot": [
            16,
            28
          ]
        },
        {
          "id": "east-1",
          "path": "assets/robot-idle/east-1.png",
          "rect": [
            0,
            0,
            32,
            32
          ],
          "duration_ms": 120,
          "pivot": [
            16,
            28
          ]
        },
        {
          "id": "east-2",
          "path": "assets/robot-idle/east-2.png",
          "rect": [
            0,
            0,
            32,
            32
          ],
          "duration_ms": 160,
          "pivot": [
            16,
            28
          ]
        },
        {
          "id": "east-3",
          "path": "assets/robot-idle/east-3.png",
          "rect": [
            0,
            0,
            32,
            32
          ],
          "duration_ms": 120,
          "pivot": [
            16,
            28
          ]
        },
        {
          "id": "east-4",
          "path": "assets/robot-idle/east-4.png",
          "rect": [
            0,
            0,
            32,
            32
          ],
          "duration_ms": 400,
          "pivot": [
            16,
            28
          ]
        }
      ]
    }
  ]
};

export function frameAt(clipId, elapsedMs) {
  const clip = animation.clips.find(value => value.id === clipId);
  if (!clip) throw new Error('Unknown clip');
  const duration = clip.frames.reduce((sum, frame) => sum + frame.duration_ms, 0);
  let at = clip.loop ? Math.max(elapsedMs, 0) % duration
                    : Math.min(Math.max(elapsedMs, 0), duration);
  for (let index = 0; index < clip.frames.length; index++) {
    if (at < clip.frames[index].duration_ms) return index;
    at -= clip.frames[index].duration_ms;
  }
  return clip.frames.length - 1;
}
