---
name: implement-phase
description: Implement a specific development phase of MathBuilder from the detailed plan docs. Use when the user wants to build out Phase 1 (foundation), Phase 2 (core mechanics), Phase 3 (visuals), Phase 4 (game loop), Phase 5 (levels), or Phase 6 (polish). Also use when the user asks to set up the project, implement gameplay, add menus, or deploy.
---

# Implement Phase

Implement a specific phase of the MathBuilder project by following the detailed plan documents in `docs/plans/`.

## When to Use

- User asks to "implement phase N" or "build phase N"
- User asks to "set up the project" (Phase 1)
- User asks to "add player movement" or "implement gameplay" (Phase 2)
- User asks to "integrate art" or "add asset loading" (Phase 3)
- User asks to "add menus", "save system", or "progression" (Phase 4)
- User asks to "create levels" (Phase 5)
- User asks to "add sound", "particles", "touch controls", or "deploy" (Phase 6)

## Phase Map

| Phase | Plan Doc | What It Builds |
|-------|----------|---------------|
| 1 | `docs/plans/01-foundation.md` | package.json, Vite config, index.html, style.css, GameConfig, main.js, BootScene |
| 2 | `docs/plans/02-core-mechanics.md` | GridSystem, Player, Bridge, MathInputUI, LevelLoader, gap zones |
| 3 | `docs/plans/03-visuals-and-art.md` | PreloadScene, sprite integration, background parallax, animations |
| 4 | `docs/plans/04-game-loop.md` | GoalFlag, star rating, SaveManager, TitleSystem, MenuScene, LevelSelectScene, LevelCompleteScene |
| 5 | `docs/plans/05-level-design.md` | 10 level JSON files in public/levels/world1/ |
| 6 | `docs/plans/06-polish-and-launch.md` | Sound effects, ParticleManager, TouchControls, Vercel deployment |

## Workflow

1. **Read the plan doc** for the requested phase — it contains detailed instructions, code templates, and file paths
2. **Read `docs/plans/00-overview.md`** for architecture context and conventions
3. **Check existing implementation** — examine `src/`, `public/`, and root config files to see what's already done
4. **Check dependencies** — ensure prerequisite phases are complete:
   - Phase 2 requires Phase 1
   - Phase 3 can start in parallel with Phase 2 (art assets exist)
   - Phase 4 requires Phase 2
   - Phase 5 requires Phase 2 (level format must work)
   - Phase 6 requires Phases 1-5
5. **Implement** following the plan doc closely:
   - Use exact file paths from the plan
   - Follow code templates provided
   - Respect conventions: ES6 modules, Phaser 3 patterns, 800x600 canvas, 64px tiles
   - Do NOT skip files listed in the phase
6. **Verify** using the checklist at the bottom of each plan doc

## Key Conventions

- **Canvas:** 800x600 pixels, `Phaser.Scale.FIT`, `CENTER_BOTH`
- **Tiles:** 64x64 pixels (`TILE_SIZE` constant in GridSystem)
- **Physics:** Arcade, gravity `y: 800`
- **Scenes:** PascalCase, extend `Phaser.Scene`, call `super('SceneName')`
- **Objects:** extend `Phaser.Physics.Arcade.Sprite`
- **Systems:** plain ES6 classes, no DI
- **Math input:** HTML overlay `#math-input-overlay`, not Phaser DOM
- **Font:** Fredoka One (Google Fonts)
- **Level data:** `fetch()` from `/levels/world1/levelNN.json`
- **Coordinates:** pixels everywhere; use GridSystem for tile ↔ pixel conversion

## File Structure Reference

```
src/
  main.js                      # Phaser bootstrap
  game/
    GameConfig.js              # Phaser config
    scenes/
      BootScene.js             # Phase 1
      PreloadScene.js          # Phase 3
      MenuScene.js             # Phase 4
      LevelSelectScene.js      # Phase 4
      GameScene.js             # Phase 2
      LevelCompleteScene.js    # Phase 4
    objects/
      Player.js                # Phase 2
      Bridge.js                # Phase 2
      GoalFlag.js              # Phase 4
    systems/
      GridSystem.js            # Phase 2
      LevelLoader.js           # Phase 2
      MathInputUI.js           # Phase 2
      SaveManager.js           # Phase 4
      TitleSystem.js           # Phase 4
      TouchControls.js         # Phase 6
      ParticleManager.js       # Phase 6
```

## Post-Implementation

After implementing a phase:
1. Run `npm run dev` and check browser console for errors
2. Run `npm run build` to verify production build works
3. Test the specific features added in that phase
4. Walk through the verification checklist in the plan doc
