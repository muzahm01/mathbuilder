---
name: level-design
description: Create and validate MathBuilder game level JSON files. Use when the user wants to add new levels, edit existing levels, validate level layouts, or design level progression for the platformer game.
---

# Level Design

Create, edit, and validate game levels for MathBuilder. Each level is a JSON file defining platforms, gaps, and player/goal positions on a tile grid.

## When to Use

- User wants to create a new level
- User wants to edit an existing level layout
- User wants to validate level JSON files
- User mentions "level design", "add level", "gap placement", or "difficulty curve"

## Level JSON Schema

Levels live at `public/levels/world1/levelNN.json`:

```json
{
  "id": 1,
  "name": "First Steps",
  "world": "grasslands",
  "gridWidth": 25,
  "gridHeight": 9,
  "start": { "gridX": 1, "gridY": 7 },
  "goal": { "gridX": 23, "gridY": 7 },
  "platforms": [
    { "gridX": 0, "gridY": 8, "width": 8, "tile": "grass-top" }
  ],
  "gaps": [
    { "id": "gap1", "gridX": 8, "gridY": 8, "width": 3, "correctAnswer": 3 }
  ]
}
```

## Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | number | Yes | Sequential level number |
| `name` | string | Yes | Display name in level select |
| `world` | string | Yes | Theme key ("grasslands" for World 1) |
| `gridWidth` | number | Yes | Total level width in tiles |
| `gridHeight` | number | Yes | Always 9 (576px fits in 600px viewport) |
| `start.gridX/gridY` | number | Yes | Player spawn (gridY = platform gridY - 1) |
| `goal.gridX/gridY` | number | Yes | Goal flag position |
| `platforms[].gridX` | number | Yes | Left edge in tile coords |
| `platforms[].gridY` | number | Yes | Top edge in tile coords (usually 8) |
| `platforms[].width` | number | Yes | Width in tiles |
| `platforms[].tile` | string | No | Texture key (default: "grass-top") |
| `gaps[].id` | string | Yes | Unique ID: "gap1", "gap2", etc. |
| `gaps[].gridX` | number | Yes | Left edge of gap |
| `gaps[].gridY` | number | Yes | Same Y as adjacent platforms |
| `gaps[].width` | number | Yes | Gap width in tiles = the correct answer |
| `gaps[].correctAnswer` | number | Yes | Must equal `width` |

## Design Rules

1. **`correctAnswer` MUST equal `width`** for every gap — the gap width IS the math problem
2. **`gridHeight` is always 9** — this fits 576px in the 600px viewport
3. **Player spawns one tile above platform** — if platform is at gridY=8, player is at gridY=7
4. **Platforms and gaps must tile seamlessly** — platform end + gap start must be contiguous, no floating sections
5. **Goal must be reachable** — placed on the last platform, one tile above it
6. **Camera scrolls if gridWidth > 12** — viewport is ~12.5 tiles wide
7. **Gap widths 1-10** for age 5-8 target audience

## Difficulty Curve (World 1)

| Tier | Levels | Gaps | Max Width | Concepts |
|------|--------|------|-----------|----------|
| Tutorial | 1-3 | 1 each | 2-4 | Basic counting |
| Multi-gap | 4-6 | 2 each | 2-5 | Multiple challenges, elevation |
| Endurance | 7-9 | 2-3 each | 2-6 | Scrolling, sustained focus |
| Boss | 10 | 1 | 10 | Screen-wide gap |

## Existing Levels

Read existing levels to understand progression. For the full level specifications with ASCII diagrams, see [docs/plans/05-level-design.md](../../docs/plans/05-level-design.md).

## Validation Checklist

When creating or editing a level, verify:

- [ ] JSON parses without errors
- [ ] `correctAnswer` equals `width` for every gap
- [ ] Platforms don't overlap with each other or with gaps
- [ ] Platform edges align with gap edges (no floating terrain)
- [ ] Player start is on solid ground (above a platform)
- [ ] Goal is reachable after all gaps are bridged
- [ ] `gridWidth` is wide enough to contain all platforms and gaps
- [ ] Gap widths are appropriate for age 5-8 (1-10 blocks)
- [ ] Level name is unique and descriptive
- [ ] File is named `levelNN.json` with zero-padded number

## Example: Creating a New Level

To create level 11 with 2 gaps (widths 3 and 4):

1. Calculate layout: platform(6) + gap(3) + platform(5) + gap(4) + platform(7) = 25 tiles wide
2. Place player at gridX=1, gridY=7 (on first platform)
3. Place goal at gridX=23, gridY=7 (on last platform)
4. Write JSON at `public/levels/world1/level11.json`
5. Validate using the checklist above
