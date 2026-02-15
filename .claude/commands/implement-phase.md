# Implement Phase

Implement a specific development phase of MathBuilder based on the detailed plan docs.

## Arguments

$ARGUMENTS - The phase number to implement (1-6). Example: "1" or "phase 2"

## Instructions

1. Read the corresponding plan document from `docs/plans/`:
   - Phase 1: `01-foundation.md` — Project setup (package.json, Vite, Phaser bootstrap, BootScene)
   - Phase 2: `02-core-mechanics.md` — Player, grid system, gaps, bridges, math input
   - Phase 3: `03-visuals-and-art.md` — Asset loading, PreloadScene, sprite integration
   - Phase 4: `04-game-loop.md` — GoalFlag, star rating, SaveManager, TitleSystem, menus
   - Phase 5: `05-level-design.md` — 10 level JSON files
   - Phase 6: `06-polish-and-launch.md` — SFX, particles, touch controls, deployment

2. Also read `docs/plans/00-overview.md` for the overall architecture and conventions

3. Check which phases have already been implemented by examining existing files in `src/`, `public/`, and root config files

4. Implement the phase following the plan document closely:
   - Use the exact file paths specified in the plan
   - Follow the code templates provided in the plan docs
   - Respect the project conventions (ES6 modules, Phaser 3 patterns, 800x600 canvas, 64px tiles)
   - Do NOT skip any files listed in the phase

5. After creating/modifying files, verify the implementation:
   - Phase 1: Run `npm install` and `npm run dev`, check for build errors
   - Phase 2+: Run `npm run dev` and check browser console for errors
   - All phases: Ensure no import errors, no missing dependencies

6. Run the verification checklist from the bottom of the plan document

## Key Conventions
- Game canvas: 800x600, Phaser.Scale.FIT
- Tile size: 64x64 (TILE_SIZE constant)
- Physics: Arcade, gravity y=800
- Scene naming: PascalCase (e.g., BootScene, GameScene)
- All scenes in `src/game/scenes/`
- All game objects in `src/game/objects/`
- All systems in `src/game/systems/`
- Math input uses HTML overlay, not Phaser DOM
- Font: Fredoka One from Google Fonts
