# Add Game Level

Create a new level JSON file for MathBuilder.

## Arguments

$ARGUMENTS - Provide level details: level number, name, gap count, gap widths, and any special features (elevation changes, etc). Example: "level 11, name 'Bridge Master', 3 gaps of widths 4 3 5, grid width 40"

## Instructions

1. Read the level design spec at `docs/plans/05-level-design.md` to understand the JSON schema and design principles
2. Review existing levels in `public/levels/world1/` to understand the progression and avoid duplicating patterns
3. Create the level JSON at `public/levels/world1/levelNN.json` using this schema:

```json
{
  "id": <level_number>,
  "name": "<level_name>",
  "world": "grasslands",
  "gridWidth": <total_width_in_tiles>,
  "gridHeight": 9,
  "start": { "gridX": 1, "gridY": 7 },
  "goal": { "gridX": <near_right_edge>, "gridY": <on_last_platform_minus_1> },
  "platforms": [
    { "gridX": 0, "gridY": 8, "width": <tiles>, "tile": "grass-top" }
  ],
  "gaps": [
    { "id": "gap1", "gridX": <x>, "gridY": 8, "width": <gap_tiles>, "correctAnswer": <same_as_width> }
  ]
}
```

4. Follow these design rules:
   - `gridHeight` is always 9 (576px fits in 600px viewport with HUD room)
   - Player spawns at gridY = platformGridY - 1 (standing on the platform)
   - `correctAnswer` MUST always equal `width` for each gap
   - Each gap's `id` is "gap1", "gap2", etc. sequentially
   - Platforms must not overlap with gaps
   - Platform `gridX + width` should equal the next gap's `gridX` (no floating platforms)
   - Goal must be reachable after all gaps are bridged
   - For levels with `gridWidth` > 12, the camera will scroll horizontally
   - Gap widths for 5-8 year olds: typically 1-10 blocks

5. Validate that:
   - The JSON is valid (no trailing commas, proper structure)
   - All platforms and gaps tile perfectly (no overlaps or floating sections)
   - The player start position is on solid ground
   - The goal is reachable
   - Gap widths match their correctAnswer values
