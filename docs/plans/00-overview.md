# MathBuilder - Project Overview

## What is MathBuilder?

MathBuilder is a web-based 2D platformer game designed for 7-year-olds where **math builds the world**. A cute robot named "Botty" runs through colorful platformer levels that have gaps in the ground. To cross each gap, the player must count how many blocks wide it is and type the correct number — this builds a bridge and lets Botty continue.

The game teaches basic counting and number recognition through hands-on gameplay rather than flash cards or drills.

---

## Target Audience

- **Primary player:** Children aged 5-8
- **Secondary user:** Parents (supervising, helping, or watching)
- **Platform:** Web browser on tablets, laptops, and phones
- **No accounts, no servers, no ads** — purely client-side with LocalStorage saves

---

## Tech Stack

| Technology | Purpose | Why |
|-----------|---------|-----|
| **Phaser 3.80+** | Game engine | Industry-standard HTML5 game framework, Arcade Physics built-in |
| **Vite 5** | Build tool | Fast dev server with HMR, simple config, excellent Phaser compatibility |
| **HTML/CSS** | Math input overlay | Better virtual keyboard support on tablets than Phaser DOM elements |
| **LocalStorage** | Save system | Zero-config persistence, no backend needed |
| **Vercel** | Hosting | Free tier, auto-deploys from GitHub, global CDN |
| **Google Gemini** | Art generation | Generate all "Soft Plastic Voxel" art assets |
| **sfxr.me** | Sound generation | Free chiptune sound effects generator |

---

## Visual Style: "Soft Plastic Voxel"

The art direction is **Minecraft meets Mario, made of smooth vinyl toys**:
- Chunky, rounded shapes (no sharp edges)
- Vibrant primary colors (blue robot, green grass, warm browns)
- Soft ambient lighting with gentle shadows
- Everything looks like it could be a real plastic toy you'd find in a store
- Isometric-inspired tiles flattened for side-scrolling

---

## Project Structure

```
mathbuilder/
  index.html                     # Phaser mount + math-input HTML overlay
  package.json                   # Vite + Phaser 3 dependencies
  vite.config.js                 # Vite configuration
  vercel.json                    # Vercel deployment config
  .gitignore                     # node_modules, dist, .DS_Store
  plan.md                        # Original project plan (existing)

  docs/
    plans/
      00-overview.md             # This file
      01-foundation.md           # Phase 1: Setup
      02-core-mechanics.md       # Phase 2: Gameplay
      03-visuals-and-art.md      # Phase 3: Art assets
      04-game-loop.md            # Phase 4: Progression
      05-level-design.md         # Phase 5: Levels
      06-polish-and-launch.md    # Phase 6: Polish
      art-prompts.md             # All Gemini art prompts

  public/
    assets/
      images/
        tiles/                   # Ground tiles (64x64 each)
          grass-top.png
          dirt.png
          stone.png
        player/                  # Botty sprite sheets
          botty-idle.png         # 4 frames, 256x64
          botty-walk.png         # 6 frames, 384x64
          botty-jump.png         # 2 frames, 128x64
        backgrounds/             # Parallax layers
          sky.png                # 800x600
          clouds.png             # 800x200, tileable
          hills.png              # 800x200, tileable
        ui/                      # Interface elements
          btn-play.png
          btn-levels.png
          star-filled.png        # 32x32
          star-empty.png         # 32x32
          math-input-bg.png
          arrow-left.png         # 64x64 touch control
          arrow-right.png        # 64x64 touch control
          arrow-jump.png         # 64x64 touch control
        objects/
          flag.png               # 64x64 goal flag
          bridge-block.png       # 64x64 bridge tile
        particles/
          dust.png               # 8x8
          confetti.png           # 8x8
      audio/
        jump.wav
        correct.wav
        wrong.wav
        build.wav
        win.wav
    levels/
      world1/                    # 10 JSON level files
        level01.json
        level02.json
        ...
        level10.json

  src/
    main.js                      # Bootstrap: create Phaser.Game
    game/
      GameConfig.js              # Phaser config (800x600, Arcade, Scale.FIT)
      scenes/
        BootScene.js             # Loads minimal assets, transitions to Preload
        PreloadScene.js          # Loads ALL assets with progress bar
        MenuScene.js             # Title screen with Play button
        LevelSelectScene.js      # 10-level grid with star ratings
        GameScene.js             # Core platformer gameplay
        LevelCompleteScene.js    # Star rating, XP, next level
      objects/
        Player.js                # Player sprite with movement + animations
        Bridge.js                # Bridge block spawner
        GoalFlag.js              # Level completion trigger
      systems/
        GridSystem.js            # TILE_SIZE=64, coordinate helpers
        LevelLoader.js           # Fetches + parses level JSON
        MathInputUI.js           # HTML overlay controller
        SaveManager.js           # LocalStorage read/write
        TitleSystem.js           # XP -> title lookup
        TouchControls.js         # On-screen arrow buttons
        ParticleManager.js       # Dust + confetti emitters
```

---

## Scene Flow

```
┌────────────┐
│  BootScene  │  Loads loading-bar assets
└─────┬──────┘
      v
┌──────────────┐
│ PreloadScene  │  Loads ALL game assets, shows progress bar
└─────┬────────┘
      v
┌────────────┐
│  MenuScene  │  "MathBuilder" title, Play button, rank display
└─────┬──────┘
      v
┌──────────────────┐
│ LevelSelectScene  │  10 level buttons (5x2 grid), stars, locked levels
└─────┬────────────┘
      v
┌─────────────┐     fall off screen
│  GameScene   │ ──────────────────> restart same level
│  (gameplay)  │
└─────┬───────┘
      │ reach goal flag
      v
┌─────────────────────┐
│ LevelCompleteScene   │  Stars, XP earned, title update
│                      │
│  [Next Level]  ──────────> GameScene (level N+1)
│  [Level Select] ─────────> LevelSelectScene
└─────────────────────┘
```

---

## Key Technical Decisions

### HTML Overlay for Math Input (not Phaser DOM)
Phaser's DOM element support is limited and inconsistent across devices. A plain HTML `<input type="number">` positioned over the canvas via CSS provides:
- Better virtual keyboard behavior on tablets and phones
- Native input validation and accessibility
- Simpler styling with standard CSS
- Reliable focus/blur handling

### Custom JSON Level Format (not Tiled)
The levels are simple enough (rectangular platforms + gap positions) that a custom JSON schema is clearer and avoids the complexity of learning Tiled, installing plugins, or parsing TMX/TSJ formats. If the game later needs slopes, moving platforms, or decoration layers, migrating to Tiled would make sense.

### Arcade Physics (not Matter.js)
Arcade Physics handles axis-aligned bounding box (AABB) collisions, which is all a basic platformer needs. Matter.js adds rotation, slopes, and complex shapes — none of which this game requires. Arcade is simpler to configure and performs better.

### Explicit Gap Zones (not Tile Absence Detection)
Rather than scanning the tilemap for missing tiles to detect gaps, each gap is explicitly defined in the level JSON with an invisible Phaser Zone placed above it. This approach:
- Is more reliable (no edge cases with tile boundaries)
- Allows gap metadata (correct answer) to be attached directly to the zone
- Makes level authoring easier (just list gaps in JSON)

### Vite (not Webpack or plain script tags)
Vite provides hot module replacement for fast iteration, handles asset imports cleanly, and produces optimized production builds. The Phaser community actively maintains Vite templates. Using a CDN script tag would work for Phase 1 but becomes painful as the codebase grows.

---

## Development Phases & Dependencies

```
Phase 1 (Foundation)
  |
  v
Phase 2 (Core Mechanics) ------> Phase 3 (Visuals) can START in parallel
  |                                  |
  v                                  v
Phase 4 (Game Loop) <------------- Art integration requires Phase 2 scenes
  |
  v
Phase 5 (Level Design) --- JSON authoring can start after Phase 2
  |
  v
Phase 6 (Polish & Launch)
```

**What can be parallelized:**
- Gemini art generation can begin during Phase 1 (prompts are ready)
- Sound effect generation (sfxr.me) can happen anytime
- Level JSON files can be drafted after Phase 2 confirms the format
- SaveManager and TitleSystem are independent modules

---

## Game Mechanics Summary

### Core Loop
1. Player selects a level from the level select screen
2. Botty spawns on the starting platform
3. Player moves Botty right using arrow keys (or touch buttons)
4. Botty reaches a gap — an overlay appears asking "How wide is the gap?"
5. Player counts the gap width in tile units and types the number
6. **Correct answer:** Bridge blocks spawn, Botty can cross. "Correct!" feedback.
7. **Wrong answer:** "Too Short!" or "Too Long!" feedback. Try again.
8. Botty reaches the goal flag — level complete!
9. Star rating based on wrong attempts (0 wrong = 3 stars, 1-2 = 2 stars, 3+ = 1 star)
10. XP earned, title potentially upgraded, next level unlocked

### Progression
- 10 levels in World 1 "Grasslands"
- Stars earned per level (best score saved)
- XP accumulates across all levels
- Titles unlock at XP thresholds (Newbie -> Math Cadet -> ... -> Legend)
- Levels unlock sequentially (complete level N to unlock level N+1)
