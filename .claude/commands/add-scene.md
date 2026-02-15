# Add Phaser Scene

Create a new Phaser scene for MathBuilder.

## Arguments

$ARGUMENTS - The scene name and purpose. Example: "SettingsScene - allows players to toggle sound and reset progress"

## Instructions

1. Read `docs/plans/00-overview.md` for the scene flow and architecture conventions
2. Check existing scenes in `src/game/scenes/` to understand the current patterns and imports
3. Create the new scene at `src/game/scenes/<SceneName>.js` following this template:

```js
import Phaser from 'phaser';

export default class SceneName extends Phaser.Scene {
  constructor() {
    super('SceneName');  // Scene key matches class name without "Scene" suffix where appropriate
  }

  init(data) {
    // Receive data passed from previous scene via this.scene.start('SceneName', data)
  }

  preload() {
    // Only if this scene needs to load additional assets not handled by PreloadScene
  }

  create() {
    // Scene setup: add sprites, text, input handlers, physics
  }

  update(time, delta) {
    // Per-frame game logic (movement, collision checks, etc.)
  }
}
```

4. Follow these conventions:
   - Scene class names use PascalCase and end with "Scene" (e.g., `SettingsScene`)
   - The `super()` key should match the class name (e.g., `super('Settings')` or `super('SettingsScene')` — match existing convention)
   - Use `this.scale.width` and `this.scale.height` for positioning (not hardcoded 800/600)
   - Text uses `fontFamily: 'Fredoka One'` with appropriate stroke for readability
   - Colors: background sky blue (#87CEEB), text dark (#2c3e50), accents match the "Soft Plastic Voxel" theme
   - Scene transitions use `this.scene.start('NextScene', optionalData)`

5. Register the new scene in `src/game/GameConfig.js` by:
   - Adding an import statement
   - Adding it to the `scene` array in the correct position in the flow

6. If the scene needs to be accessible from other scenes, update those scenes to add navigation (buttons, transitions)
