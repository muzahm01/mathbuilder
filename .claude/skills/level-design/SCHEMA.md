# Level JSON Schema Reference

## Complete Schema with Annotations

```json
{
  // Sequential level number (1-based)
  "id": 1,

  // Display name shown in LevelSelectScene
  "name": "First Steps",

  // Theme key — determines tile textures and background
  // World 1 = "grasslands"
  "world": "grasslands",

  // Total level width in grid tiles
  // Camera is static if <= 12, scrolls if > 12
  "gridWidth": 25,

  // Total level height — ALWAYS 9
  // 9 tiles × 64px = 576px, fits in 600px viewport
  "gridHeight": 9,

  // Player spawn position in tile coordinates
  // gridY should be platformGridY - 1 (standing ON the platform)
  "start": { "gridX": 1, "gridY": 7 },

  // Goal flag position — must be reachable after all gaps bridged
  "goal": { "gridX": 23, "gridY": 7 },

  // Array of platform rectangles
  // Platforms are drawn using tile sprites repeated horizontally
  "platforms": [
    {
      "gridX": 0,       // Left edge (tile coords)
      "gridY": 8,       // Top edge (tile coords) — usually 8 for ground level
      "width": 8,       // Width in tiles
      "tile": "grass-top" // Optional texture key, default "grass-top"
    },
    {
      "gridX": 11,
      "gridY": 8,
      "width": 14,
      "tile": "grass-top"
    }
  ],

  // Array of gap definitions
  // Each gap is where the player must answer a math question
  "gaps": [
    {
      "id": "gap1",       // Unique within level: "gap1", "gap2", etc.
      "gridX": 8,         // Left edge matches end of previous platform
      "gridY": 8,         // Same Y as adjacent platforms
      "width": 3,         // Width in tiles — THIS IS THE ANSWER
      "correctAnswer": 3  // Must equal width (redundant for clarity)
    }
  ]
}
```

## Layout Constraint

Platforms and gaps must form a continuous ground line. Given:

```
Platform A: gridX=0, width=8    → occupies tiles 0-7
Gap 1:      gridX=8, width=3    → occupies tiles 8-10
Platform B: gridX=11, width=14  → occupies tiles 11-24
```

The rule: `Platform A gridX + width = Gap 1 gridX` and `Gap 1 gridX + width = Platform B gridX`.

## Elevation Changes

Platforms can be at different gridY values. For elevated platforms:
- The gap's gridY matches the LOWER platform's gridY
- After building the bridge, the player jumps up to the higher platform

```json
{
  "platforms": [
    { "gridX": 0, "gridY": 8, "width": 10 },
    { "gridX": 13, "gridY": 8, "width": 5 },
    { "gridX": 23, "gridY": 7, "width": 7 }  // One tile higher
  ],
  "gaps": [
    { "id": "gap1", "gridX": 10, "gridY": 8, "width": 3 },
    { "id": "gap2", "gridX": 18, "gridY": 8, "width": 5 }
  ]
}
```

## Tile Types

| Key | Asset | Description |
|-----|-------|-------------|
| `grass-top` | `tiles/grass-top.png` | Green grass on brown dirt — default |
| `dirt` | `tiles/dirt.png` | Plain dirt block |
| `stone` | `tiles/stone.png` | Grey stone block |
