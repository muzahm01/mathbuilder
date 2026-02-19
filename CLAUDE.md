# MathBuilder

## Project Overview

MathBuilder is a web-based 2D platformer game for children aged 5-8 where math builds the world. A robot character "Botty" runs through platformer levels with gaps in the ground. Players count the gap width in tile units and type the answer to build a bridge.

- **Engine:** Phaser 3.80+ with Arcade Physics
- **Build Tool:** Vite 5 (ES modules)
- **Language:** JavaScript (ES6 modules, no TypeScript)
- **Hosting:** Vercel (static site)
- **Persistence:** LocalStorage only (no backend, no accounts)
- **Art Style:** "Modern 3D Clay Render" — Fall Guys meets Yoshi's Crafted World with PBR materials, ambient occlusion, and volumetric lighting

## Project Structure

```
mathbuilder/
  index.html              # Phaser mount + math-input HTML overlay
  style.css               # Overlay and layout styles
  package.json            # Vite + Phaser 3 dependencies
  vite.config.js          # Vite config (port 8080, base './')
  vercel.json             # Deployment config

  src/
    main.js               # Bootstrap: creates Phaser.Game
    game/
      GameConfig.js       # Phaser config (800x600, Arcade, Scale.FIT)
      scenes/             # BootScene, PreloadScene, MenuScene, LevelSelectScene, GameScene, LevelCompleteScene
      objects/            # Player.js, Bridge.js, GoalFlag.js
      systems/            # GridSystem, LevelLoader, MathInputUI, SaveManager, TitleSystem, TouchControls, ParticleManager

  public/
    assets/
      images/             # All game art (tiles/, player/, backgrounds/, ui/, objects/, particles/)
      audio/              # Sound effects (jump.wav, correct.wav, wrong.wav, build.wav, win.wav)
    levels/
      world1/             # 10 JSON level files (level01.json - level10.json)

  scripts/                # Python image processing pipeline
    process_images.py     # Main processor: background removal, sprite extraction, resizing
    fix_sprites_and_bg.py
    fix_remaining.py
    fix_final.py

  resources/              # Raw source images from Gemini (input to processing scripts)

  docs/plans/             # Detailed phase-by-phase implementation docs
    00-overview.md        # Architecture, tech stack, scene flow
    01-foundation.md      # Phase 1: Project setup (Vite + Phaser)
    02-core-mechanics.md  # Phase 2: Player, gaps, bridges, math input
    03-visuals-and-art.md # Phase 3: Asset integration, PreloadScene
    04-game-loop.md       # Phase 4: Progression, save system, menus
    05-level-design.md    # Phase 5: Level JSON format, 10 levels
    06-polish-and-launch.md # Phase 6: SFX, particles, touch, deploy
    art-prompts.md        # Gemini image generation prompts
```

## Key Commands

```bash
npm install          # Install dependencies
npm run dev          # Start Vite dev server on http://localhost:8080
npm run build        # Production build to dist/
npm run preview      # Preview production build locally
```

## Image Processing

```bash
cd /home/user/mathbuilder
python3 scripts/process_images.py    # Process resources/ -> public/assets/images/
```

Requires Python 3 with Pillow (`pip install Pillow`). Source images go in `resources/`, processed output goes to `public/assets/images/`.

## Architecture Conventions

### Game Config
- Canvas: 800x600 pixels, 4:3 aspect ratio
- Tile size: 64x64 pixels (TILE_SIZE constant in GridSystem)
- Gravity: 800 pixels/s² (Arcade Physics)
- Scale mode: Phaser.Scale.FIT with CENTER_BOTH

### Scene Flow
```
BootScene -> PreloadScene -> MenuScene -> LevelSelectScene -> GameScene -> LevelCompleteScene
                                                                  |
                                                                  v (fall off screen = restart)
```

### Code Patterns
- Each scene extends `Phaser.Scene` and calls `super('SceneName')` in the constructor
- Game objects extend `Phaser.GameObjects.Sprite` or use `Phaser.Physics.Arcade.Sprite`
- Systems are plain ES6 classes instantiated in scenes (no dependency injection)
- Level data is loaded via `fetch()` from `/levels/world1/levelNN.json`
- Math input uses an HTML overlay (`#math-input-overlay`) controlled by `MathInputUI.js`, not Phaser DOM elements
- All coordinates use pixel values; use `GridSystem.tileToPixel()` / `GridSystem.pixelToTile()` for conversions

### Level JSON Format
```json
{
  "name": "Level Name",
  "width": 15,
  "platforms": [
    { "x": 0, "y": 8, "width": 5, "tile": "grass-top" }
  ],
  "gaps": [
    { "x": 5, "y": 8, "width": 3, "answer": 3 }
  ],
  "player": { "x": 1, "y": 7 },
  "goal": { "x": 14, "y": 7 }
}
```
All positions are in tile coordinates (multiply by 64 for pixels).

### Asset Specifications
| Category | Dimensions | Notes |
|----------|-----------|-------|
| Tiles | 64x64 | Seamless, tileable |
| Player sprites | 64x64 per frame | Horizontal sprite sheets (idle=4fr, walk=6fr, jump=2fr) |
| Backgrounds | 800x600 (sky), 800x200 (clouds, hills) | clouds/hills are tileable for parallax |
| UI buttons | 200x70 | Glossy candy-style |
| Stars | 32x32 | filled and empty variants |
| Math panel BG | 400x250 | Kid-friendly blue panel |
| Touch arrows | 64x64 | Semi-transparent circles |
| Objects | 64x64 | flag, bridge-block (transparent BG) |
| Particles | 8x8 | dust, confetti |

### Star Rating
- 0 wrong answers = 3 stars
- 1-2 wrong answers = 2 stars
- 3+ wrong answers = 1 star (never 0 — always positive reinforcement)

### Title/XP System
Titles progress: Newbie -> Math Cadet -> Number Ninja -> Bridge Builder -> Team Leader -> Math Hero -> Grand Master -> Legend

## Implementation Status

Phase 3 (art assets) is partially complete — all 21 game images are processed and ready in `public/assets/images/`. The game code (Phases 1-2, 4-6) has not been implemented yet. Refer to `docs/plans/` for detailed phase-by-phase instructions with complete code templates.

## Design Philosophy

- **Target audience is children aged 5-8** — keep UX simple, colors bright, feedback positive
- **No backend, no accounts, no ads** — pure client-side game
- **Touch-first** — must work well on tablets with on-screen controls
- **Positive reinforcement** — wrong answers get "Try again!" not punishment; minimum 1 star always
- **Font:** Fredoka One (Google Fonts) for all text — chunky, kid-friendly
