# Phase 5: Level Design

## Goal
Create 10 complete levels for World 1 "Grasslands" with progressive difficulty. Each level is a JSON file that defines platforms, gaps, and start/goal positions. By the end, the player has a full 10-level experience from tutorial to boss.

**Depends on:** Phase 2 (level format confirmed and loading works)

---

## JSON Level Format Specification

Every level is stored as a JSON file at `public/levels/world1/levelNN.json`.

### Schema

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
    {
      "gridX": 0,
      "gridY": 8,
      "width": 8,
      "tile": "grass-top"
    }
  ],
  "gaps": [
    {
      "id": "gap1",
      "gridX": 8,
      "gridY": 8,
      "width": 3,
      "correctAnswer": 3
    }
  ]
}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | number | Yes | Sequential level number (1-10) |
| `name` | string | Yes | Display name shown in level select |
| `world` | string | Yes | Theme key ("grasslands" for World 1) |
| `gridWidth` | number | Yes | Total level width in grid units |
| `gridHeight` | number | Yes | Total level height in grid units (9 = 576px, fits in 600 with HUD room) |
| `start` | object | Yes | Player spawn position `{ gridX, gridY }` |
| `goal` | object | Yes | Goal flag position `{ gridX, gridY }` |
| `platforms` | array | Yes | Platform rectangles |
| `platforms[].gridX` | number | Yes | Left edge of platform in grid coords |
| `platforms[].gridY` | number | Yes | Top edge of platform in grid coords |
| `platforms[].width` | number | Yes | Platform width in tiles |
| `platforms[].tile` | string | No | Tile texture key (default: "grass-top") |
| `gaps` | array | Yes | Gap definitions |
| `gaps[].id` | string | Yes | Unique ID for the gap within the level |
| `gaps[].gridX` | number | Yes | Left edge of gap in grid coords |
| `gaps[].gridY` | number | Yes | Y position (same as adjacent platform gridY) |
| `gaps[].width` | number | Yes | Gap width in tiles (THIS IS the correct answer) |
| `gaps[].correctAnswer` | number | Yes | Expected player input (always equals `width`) |

### Key Design Rule

**The `width` field on each gap IS the correct answer.** A gap with `width: 3` means 3 empty tiles, and the player must type `3` to build a 3-block bridge. The `correctAnswer` field is redundant by design — it exists for clarity and to make the intent explicit in the JSON.

### Camera Behavior

- Game viewport: 800x600 pixels = 12.5 × 9.375 grid tiles
- If `gridWidth` ≤ 12: entire level fits on screen, camera is static
- If `gridWidth` > 12: camera follows the player horizontally with smooth lerp
- Camera world bounds are set to `gridWidth × 64` by `gridHeight × 64`

---

## Level Progression Design

### Difficulty Curve

```
Level:  1    2    3    4    5    6    7    8    9    10
Gaps:   1    1    1    2    2    2    3    2    3    1
Max:    3    4    2    3+2  4+2  3+5  2+3+4 5+3  4+6+3  10
Width:  25   25   25   30   30   30   40   35   45   50

        ╔═══════════╗  ╔══════════════╗  ╔══════════════╗
        ║  TUTORIAL  ║  ║  MULTI-GAP   ║  ║  ENDURANCE   ║
        ║  (1-3)     ║  ║  (4-6)       ║  ║  (7-9) + BOSS║
        ╚═══════════╝  ╚══════════════╝  ╚══════════════╝
```

### Design Principles

1. **Levels 1-3 (Tutorial)**: Single gap each. Teaches the core mechanic. Increasing/decreasing gap sizes to show that answers vary.
2. **Levels 4-6 (Multi-gap)**: Two gaps per level. Introduces the idea that one level can have multiple math challenges. Level 6 adds elevation changes.
3. **Levels 7-9 (Endurance)**: Two or three gaps with camera scrolling. Tests retention and counting accuracy under sustained play.
4. **Level 10 (Boss)**: One enormous gap of 10 blocks. The camera must scroll to see the full gap, making counting a real challenge.

---

## Level Layouts

### Level 1 — "First Steps"

**Purpose:** Teach the basic mechanic. Walk right, encounter a gap, type the number, build a bridge.

```
Grid (25 wide × 9 tall):

Y=7:  P                                    F
Y=8:  ████████   ___GAP(3)___   ██████████████
      0       7  8    9    10  11            24

P = Player (1, 7)    F = Goal (23, 7)
```

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
    { "gridX": 0, "gridY": 8, "width": 8, "tile": "grass-top" },
    { "gridX": 11, "gridY": 8, "width": 14, "tile": "grass-top" }
  ],
  "gaps": [
    { "id": "gap1", "gridX": 8, "gridY": 8, "width": 3, "correctAnswer": 3 }
  ]
}
```

---

### Level 2 — "One More"

**Purpose:** Slightly larger gap (4 blocks). Reinforces counting.

```
Grid (25 wide × 9 tall):

Y=7:  P                                       F
Y=8:  ██████   ____GAP(4)____   ███████████████
      0     5  6   7   8   9   10             24

P = Player (1, 7)    F = Goal (23, 7)
```

```json
{
  "id": 2,
  "name": "One More",
  "world": "grasslands",
  "gridWidth": 25,
  "gridHeight": 9,
  "start": { "gridX": 1, "gridY": 7 },
  "goal": { "gridX": 23, "gridY": 7 },
  "platforms": [
    { "gridX": 0, "gridY": 8, "width": 6, "tile": "grass-top" },
    { "gridX": 10, "gridY": 8, "width": 15, "tile": "grass-top" }
  ],
  "gaps": [
    { "id": "gap1", "gridX": 6, "gridY": 8, "width": 4, "correctAnswer": 4 }
  ]
}
```

---

### Level 3 — "Small Step"

**Purpose:** Smaller gap (2 blocks). Shows that answers vary — bigger isn't always the answer.

```
Grid (25 wide × 9 tall):

Y=7:  P                                 F
Y=8:  ██████████   _GAP(2)_   ████████████████
      0         9  10    11   12              24

P = Player (1, 7)    F = Goal (23, 7)
```

```json
{
  "id": 3,
  "name": "Small Step",
  "world": "grasslands",
  "gridWidth": 25,
  "gridHeight": 9,
  "start": { "gridX": 1, "gridY": 7 },
  "goal": { "gridX": 23, "gridY": 7 },
  "platforms": [
    { "gridX": 0, "gridY": 8, "width": 10, "tile": "grass-top" },
    { "gridX": 12, "gridY": 8, "width": 13, "tile": "grass-top" }
  ],
  "gaps": [
    { "id": "gap1", "gridX": 10, "gridY": 8, "width": 2, "correctAnswer": 2 }
  ]
}
```

---

### Level 4 — "Double Trouble"

**Purpose:** First level with TWO gaps. Teaches that levels can have multiple math challenges.

```
Grid (30 wide × 9 tall):

Y=7:  P                                              F
Y=8:  ██████   ___GAP(3)___   ████████   __GAP(2)__   █████████
      0     5  6   7   8     9       16  17    18    19       29

P = Player (1, 7)    F = Goal (28, 7)
```

```json
{
  "id": 4,
  "name": "Double Trouble",
  "world": "grasslands",
  "gridWidth": 30,
  "gridHeight": 9,
  "start": { "gridX": 1, "gridY": 7 },
  "goal": { "gridX": 28, "gridY": 7 },
  "platforms": [
    { "gridX": 0, "gridY": 8, "width": 6, "tile": "grass-top" },
    { "gridX": 9, "gridY": 8, "width": 8, "tile": "grass-top" },
    { "gridX": 19, "gridY": 8, "width": 11, "tile": "grass-top" }
  ],
  "gaps": [
    { "id": "gap1", "gridX": 6, "gridY": 8, "width": 3, "correctAnswer": 3 },
    { "id": "gap2", "gridX": 17, "gridY": 8, "width": 2, "correctAnswer": 2 }
  ]
}
```

---

### Level 5 — "Think Twice"

**Purpose:** Two gaps with different sizes. Requires the player to count each gap independently.

```
Grid (30 wide × 9 tall):

Y=7:  P                                                  F
Y=8:  ████████   ____GAP(4)____   ██████   __GAP(2)__   ██████
      0       7  8  9  10  11    12    17  18    19    20    29

P = Player (1, 7)    F = Goal (28, 7)
```

```json
{
  "id": 5,
  "name": "Think Twice",
  "world": "grasslands",
  "gridWidth": 30,
  "gridHeight": 9,
  "start": { "gridX": 1, "gridY": 7 },
  "goal": { "gridX": 28, "gridY": 7 },
  "platforms": [
    { "gridX": 0, "gridY": 8, "width": 8, "tile": "grass-top" },
    { "gridX": 12, "gridY": 8, "width": 6, "tile": "grass-top" },
    { "gridX": 20, "gridY": 8, "width": 10, "tile": "grass-top" }
  ],
  "gaps": [
    { "id": "gap1", "gridX": 8, "gridY": 8, "width": 4, "correctAnswer": 4 },
    { "id": "gap2", "gridX": 18, "gridY": 8, "width": 2, "correctAnswer": 2 }
  ]
}
```

---

### Level 6 — "Rising Up"

**Purpose:** Introduces elevation changes. The second platform is one tile higher, requiring a jump after the bridge.

```
Grid (30 wide × 9 tall):

Y=6:                                            F
Y=7:                           ████████████████████
Y=8:  ██████████   ___GAP(3)___   _GAP(5)_
      0         9  10  11  12    13         17  18           29

P = Player (1, 7) on first platform
F = Goal (28, 6) on elevated platform
```

```json
{
  "id": 6,
  "name": "Rising Up",
  "world": "grasslands",
  "gridWidth": 30,
  "gridHeight": 9,
  "start": { "gridX": 1, "gridY": 7 },
  "goal": { "gridX": 28, "gridY": 6 },
  "platforms": [
    { "gridX": 0, "gridY": 8, "width": 10, "tile": "grass-top" },
    { "gridX": 13, "gridY": 8, "width": 5, "tile": "grass-top" },
    { "gridX": 23, "gridY": 7, "width": 7, "tile": "grass-top" }
  ],
  "gaps": [
    { "id": "gap1", "gridX": 10, "gridY": 8, "width": 3, "correctAnswer": 3 },
    { "id": "gap2", "gridX": 18, "gridY": 8, "width": 5, "correctAnswer": 5 }
  ]
}
```

---

### Level 7 — "Triple Play"

**Purpose:** Three gaps in one level. Tests endurance and sustained focus. First level with camera scrolling.

```
Grid (40 wide × 9 tall):

Y=7:  P                                                                         F
Y=8:  ██████   __GAP(2)__   ████████████   ___GAP(3)___   ██████   ____GAP(4)____   ████████
      0     5  6     7     8           17  18  19  20    21    26  27 28 29 30    31       39

P = Player (1, 7)    F = Goal (38, 7)
```

```json
{
  "id": 7,
  "name": "Triple Play",
  "world": "grasslands",
  "gridWidth": 40,
  "gridHeight": 9,
  "start": { "gridX": 1, "gridY": 7 },
  "goal": { "gridX": 38, "gridY": 7 },
  "platforms": [
    { "gridX": 0, "gridY": 8, "width": 6, "tile": "grass-top" },
    { "gridX": 8, "gridY": 8, "width": 10, "tile": "grass-top" },
    { "gridX": 21, "gridY": 8, "width": 6, "tile": "grass-top" },
    { "gridX": 31, "gridY": 8, "width": 9, "tile": "grass-top" }
  ],
  "gaps": [
    { "id": "gap1", "gridX": 6, "gridY": 8, "width": 2, "correctAnswer": 2 },
    { "id": "gap2", "gridX": 18, "gridY": 8, "width": 3, "correctAnswer": 3 },
    { "id": "gap3", "gridX": 27, "gridY": 8, "width": 4, "correctAnswer": 4 }
  ]
}
```

---

### Level 8 — "High Bridge"

**Purpose:** Two gaps with platforms at different heights. The larger gap (5) is visually imposing.

```
Grid (35 wide × 9 tall):

Y=6:                                              F
Y=7:                          ███████████████████████
Y=8:  ████████████   _____GAP(5)_____   ___GAP(3)___
      0          11  12  13  14  15  16  17       22  23          34

P = Player (1, 7)    F = Goal (33, 6) on elevated platform
```

```json
{
  "id": 8,
  "name": "High Bridge",
  "world": "grasslands",
  "gridWidth": 35,
  "gridHeight": 9,
  "start": { "gridX": 1, "gridY": 7 },
  "goal": { "gridX": 33, "gridY": 6 },
  "platforms": [
    { "gridX": 0, "gridY": 8, "width": 12, "tile": "grass-top" },
    { "gridX": 17, "gridY": 8, "width": 6, "tile": "grass-top" },
    { "gridX": 26, "gridY": 7, "width": 9, "tile": "grass-top" }
  ],
  "gaps": [
    { "id": "gap1", "gridX": 12, "gridY": 8, "width": 5, "correctAnswer": 5 },
    { "id": "gap2", "gridX": 23, "gridY": 8, "width": 3, "correctAnswer": 3 }
  ]
}
```

---

### Level 9 — "The Gauntlet"

**Purpose:** Three gaps with the largest gap yet (6 blocks). The pre-boss challenge. Long level requiring sustained attention.

```
Grid (45 wide × 9 tall):

Y=7:  P                                                                                         F
Y=8:  ████████   ____GAP(4)____   ████████████   ______GAP(6)______   ██████   ___GAP(3)___   ███████
      0       7  8  9  10  11    12          21  22 23 24 25 26 27   28    33  34  35  36    37     44

P = Player (1, 7)    F = Goal (43, 7)
```

```json
{
  "id": 9,
  "name": "The Gauntlet",
  "world": "grasslands",
  "gridWidth": 45,
  "gridHeight": 9,
  "start": { "gridX": 1, "gridY": 7 },
  "goal": { "gridX": 43, "gridY": 7 },
  "platforms": [
    { "gridX": 0, "gridY": 8, "width": 8, "tile": "grass-top" },
    { "gridX": 12, "gridY": 8, "width": 10, "tile": "grass-top" },
    { "gridX": 28, "gridY": 8, "width": 6, "tile": "grass-top" },
    { "gridX": 37, "gridY": 8, "width": 8, "tile": "grass-top" }
  ],
  "gaps": [
    { "id": "gap1", "gridX": 8, "gridY": 8, "width": 4, "correctAnswer": 4 },
    { "id": "gap2", "gridX": 22, "gridY": 8, "width": 6, "correctAnswer": 6 },
    { "id": "gap3", "gridX": 34, "gridY": 8, "width": 3, "correctAnswer": 3 }
  ]
}
```

---

### Level 10 — "Mega Bridge" (Boss Level)

**Purpose:** The capstone challenge. One enormous gap of 10 blocks. The player must carefully count across a gap that's wider than the screen — the camera must scroll to see the entire gap. This is the climactic moment of World 1.

```
Grid (50 wide × 9 tall):

Y=7:  P                                                                                                     F
Y=8:  ██████████████████   __________GAP(10)__________   ███████████████████████████████████████████████████████
      0               17  18 19 20 21 22 23 24 25 26 27  28                                                  49

P = Player (1, 7)    F = Goal (48, 7)
```

```json
{
  "id": 10,
  "name": "Mega Bridge",
  "world": "grasslands",
  "gridWidth": 50,
  "gridHeight": 9,
  "start": { "gridX": 1, "gridY": 7 },
  "goal": { "gridX": 48, "gridY": 7 },
  "platforms": [
    { "gridX": 0, "gridY": 8, "width": 18, "tile": "grass-top" },
    { "gridX": 28, "gridY": 8, "width": 22, "tile": "grass-top" }
  ],
  "gaps": [
    { "id": "gap1", "gridX": 18, "gridY": 8, "width": 10, "correctAnswer": 10 }
  ]
}
```

**Boss level design notes:**
- The long approach platform (18 blocks) gives the player time to build anticipation
- The gap is 640px wide (10 × 64) — wider than the 800px viewport
- The player must walk to the gap edge, and the camera will show it extending off-screen
- The child needs to count carefully: 1, 2, 3... up to 10
- The long platform after the gap (22 blocks) gives a satisfying victory run to the flag
- Only ONE gap — this is a focus challenge, not an endurance challenge

---

## Level Summary Table

| Level | Name | Gaps | Answers | Grid Width | Scrolling | New Concept |
|-------|------|------|---------|------------|-----------|-------------|
| 1 | First Steps | 1 | 3 | 25 | No | Basic mechanic |
| 2 | One More | 1 | 4 | 25 | No | Larger gap |
| 3 | Small Step | 1 | 2 | 25 | No | Smaller gap |
| 4 | Double Trouble | 2 | 3, 2 | 30 | Slight | Multiple gaps |
| 5 | Think Twice | 2 | 4, 2 | 30 | Slight | Mixed sizes |
| 6 | Rising Up | 2 | 3, 5 | 30 | Slight | Elevation change |
| 7 | Triple Play | 3 | 2, 3, 4 | 40 | Yes | Three gaps |
| 8 | High Bridge | 2 | 5, 3 | 35 | Yes | Multi-height |
| 9 | The Gauntlet | 3 | 4, 6, 3 | 45 | Yes | Largest variety |
| 10 | Mega Bridge | 1 | 10 | 50 | Yes | Boss gap |

---

## Counting Aid Design

For the target audience (7-year-olds), counting gaps wider than 5-6 blocks can be tricky. Consider these visual aids built into the gap area:

### Option A: Tile markers (recommended)
Add faint vertical dotted lines or tile-width markers at the bottom of each gap to help children count individual tile spaces. These can be drawn in GameScene using light graphics:

```js
// In GameScene, after creating gap zones:
for (const g of levelData.gaps) {
  const { x: gapX, y: gapY } = gridToPixel(g.gridX, g.gridY);
  const graphics = this.add.graphics();
  graphics.lineStyle(1, 0xffffff, 0.2);

  for (let i = 1; i < g.width; i++) {
    const lineX = gapX + i * TILE_SIZE;
    graphics.moveTo(lineX, gapY);
    graphics.lineTo(lineX, gapY + TILE_SIZE);
  }
  graphics.strokePath();
}
```

### Option B: No markers (harder)
Leave gaps as pure empty space — the child must estimate the width by looking at the surrounding platform edges. Suitable for a "hard mode" or World 2.

**Recommendation:** Use Option A for World 1 to support learning. The faint lines help without giving away the answer.

---

## Files Created in This Phase

| File | Action | Purpose |
|------|--------|---------|
| `public/levels/world1/level01.json` | Create (or update from Phase 2) | Tutorial level |
| `public/levels/world1/level02.json` | Create | Single gap, size 4 |
| `public/levels/world1/level03.json` | Create | Single gap, size 2 |
| `public/levels/world1/level04.json` | Create | Two gaps: 3, 2 |
| `public/levels/world1/level05.json` | Create | Two gaps: 4, 2 |
| `public/levels/world1/level06.json` | Create | Two gaps: 3, 5 + elevation |
| `public/levels/world1/level07.json` | Create | Three gaps: 2, 3, 4 |
| `public/levels/world1/level08.json` | Create | Two gaps: 5, 3 + elevation |
| `public/levels/world1/level09.json` | Create | Three gaps: 4, 6, 3 |
| `public/levels/world1/level10.json` | Create | Boss: one gap of 10 |

---

## Verification Checklist

- [ ] All 10 level JSON files parse without errors (`JSON.parse` in console)
- [ ] Each level loads correctly in GameScene (no missing fields, no NaN positions)
- [ ] Level 1: single gap of 3 — answer 3 builds a perfect bridge
- [ ] Level 4: both gaps must be solved to reach the goal
- [ ] Level 6: elevated platform requires a jump after the second bridge
- [ ] Level 7+: camera scrolls horizontally to follow the player
- [ ] Level 10: the 10-block gap extends beyond the visible screen
- [ ] Level 10: answering 10 builds a 10-block bridge that fills the gap exactly
- [ ] Gap counting aids (faint lines) are visible and help count tiles
- [ ] All gap `width` values match the visible gap size (count tiles on screen)
- [ ] All `correctAnswer` values match their corresponding `width` values
- [ ] Player start positions are on solid ground (not floating or inside a platform)
- [ ] Goal flag positions are reachable after all gaps are solved
- [ ] No overlapping platforms or gaps in any level
- [ ] Difficulty feels progressive: a 7-year-old should breeze through levels 1-3 and be challenged by levels 8-10
