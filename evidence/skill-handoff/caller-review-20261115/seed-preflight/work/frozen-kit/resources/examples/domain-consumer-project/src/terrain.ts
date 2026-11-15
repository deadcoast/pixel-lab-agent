export const terrain = {
  "tile_size": [
    16,
    16
  ],
  "background": "#152635",
  "sampling": "nearest",
  "corner_order": [
    "nw",
    "ne",
    "se",
    "sw"
  ],
  "tiles": {
    "0": {
      "path": "assets/terrain/tile-0.png"
    },
    "1": {
      "path": "assets/terrain/tile-1.png"
    },
    "2": {
      "path": "assets/terrain/tile-2.png"
    },
    "3": {
      "path": "assets/terrain/tile-3.png"
    },
    "4": {
      "path": "assets/terrain/tile-4.png"
    },
    "5": {
      "path": "assets/terrain/tile-5.png"
    },
    "6": {
      "path": "assets/terrain/tile-6.png"
    },
    "7": {
      "path": "assets/terrain/tile-7.png"
    },
    "8": {
      "path": "assets/terrain/tile-8.png"
    },
    "9": {
      "path": "assets/terrain/tile-9.png"
    },
    "10": {
      "path": "assets/terrain/tile-10.png"
    },
    "11": {
      "path": "assets/terrain/tile-11.png"
    },
    "12": {
      "path": "assets/terrain/tile-12.png"
    },
    "13": {
      "path": "assets/terrain/tile-13.png"
    },
    "14": {
      "path": "assets/terrain/tile-14.png"
    },
    "15": {
      "path": "assets/terrain/tile-15.png"
    }
  },
  "neighborhoods": [
    {
      "id": "coverage",
      "label": "Mixed shoreline",
      "vertices": [
        [
          1,
          1,
          0,
          0,
          1,
          0,
          0,
          0,
          0
        ],
        [
          0,
          1,
          0,
          0,
          1,
          0,
          1,
          1,
          0
        ],
        [
          1,
          0,
          1,
          0,
          0,
          0,
          0,
          1,
          1
        ],
        [
          1,
          0,
          1,
          1,
          1,
          1,
          1,
          0,
          0
        ],
        [
          1,
          0,
          0,
          0,
          1,
          1,
          0,
          1,
          0
        ],
        [
          0,
          1,
          1,
          0,
          0,
          1,
          1,
          0,
          1
        ],
        [
          0,
          0,
          0,
          1,
          0,
          0,
          1,
          1,
          1
        ],
        [
          1,
          1,
          1,
          0,
          1,
          0,
          1,
          0,
          1
        ],
        [
          1,
          1,
          0,
          0,
          1,
          0,
          1,
          0,
          0
        ]
      ]
    },
    {
      "id": "island",
      "label": "Island corners",
      "vertices": [
        [
          0,
          0,
          0,
          0,
          0
        ],
        [
          0,
          1,
          1,
          1,
          0
        ],
        [
          0,
          1,
          0,
          1,
          0
        ],
        [
          0,
          1,
          1,
          1,
          0
        ],
        [
          0,
          0,
          0,
          0,
          0
        ]
      ]
    }
  ]
};

export function tileFor(corners) {
  return String(corners[0] + 2 * corners[1] + 4 * corners[2] + 8 * corners[3]);
}
