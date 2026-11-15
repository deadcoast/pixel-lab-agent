export const animation = {
  "viewport": [
    40,
    36
  ],
  "background": "#152635",
  "sampling": "nearest",
  "clips": [
    {
      "id": "idle",
      "label": "Planted idle",
      "loop": true,
      "anchor": [
        20,
        28
      ],
      "frames": [
        {
          "id": "pose-0",
          "path": "assets/motion/frame-0.png",
          "rect": [
            0,
            0,
            16,
            16
          ],
          "duration_ms": 120,
          "pivot": [
            8,
            14
          ]
        },
        {
          "id": "pose-1",
          "path": "assets/motion/frame-1.png",
          "rect": [
            0,
            0,
            16,
            16
          ],
          "duration_ms": 180,
          "pivot": [
            8,
            14
          ]
        },
        {
          "id": "pose-2",
          "path": "assets/motion/frame-2.png",
          "rect": [
            0,
            0,
            16,
            16
          ],
          "duration_ms": 120,
          "pivot": [
            8,
            14
          ]
        },
        {
          "id": "pose-3",
          "path": "assets/motion/frame-3.png",
          "rect": [
            0,
            0,
            16,
            16
          ],
          "duration_ms": 240,
          "pivot": [
            8,
            14
          ]
        }
      ]
    },
    {
      "id": "settle",
      "label": "One-shot settle",
      "loop": false,
      "anchor": [
        20,
        28
      ],
      "frames": [
        {
          "id": "pose-0",
          "path": "assets/motion/frame-0.png",
          "rect": [
            0,
            0,
            16,
            16
          ],
          "duration_ms": 120,
          "pivot": [
            8,
            14
          ]
        },
        {
          "id": "pose-1",
          "path": "assets/motion/frame-1.png",
          "rect": [
            0,
            0,
            16,
            16
          ],
          "duration_ms": 180,
          "pivot": [
            8,
            14
          ]
        },
        {
          "id": "pose-2",
          "path": "assets/motion/frame-2.png",
          "rect": [
            0,
            0,
            16,
            16
          ],
          "duration_ms": 120,
          "pivot": [
            8,
            14
          ]
        },
        {
          "id": "pose-3",
          "path": "assets/motion/frame-3.png",
          "rect": [
            0,
            0,
            16,
            16
          ],
          "duration_ms": 240,
          "pivot": [
            8,
            14
          ]
        }
      ]
    }
  ]
};

export function frameAt(clipId, elapsedMs) {
  const clip = animation.clips.find(clip => clip.id === clipId);
  const total = clip.frames.reduce((sum, frame) => sum + frame.duration_ms, 0);
  const elapsed = Math.max(0, elapsedMs);
  let time = clip.loop ? elapsed % total : Math.min(elapsed, total - 0.001);
  for (let i = 0; i < clip.frames.length; i++) {
    if (time < clip.frames[i].duration_ms) return i;
    time -= clip.frames[i].duration_ms;
  }
  return clip.frames.length - 1;
}
