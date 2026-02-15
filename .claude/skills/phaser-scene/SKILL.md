---
name: phaser-scene
description: Create new Phaser 3 scenes for MathBuilder following project conventions. Use when the user wants to add a new game scene, screen, or menu to the platformer game.
---

# Phaser Scene

Create new Phaser 3 scenes for MathBuilder following the project's established patterns and conventions.

## When to Use

- User wants to add a new scene (settings screen, credits, tutorial overlay, etc.)
- User mentions "new scene", "add screen", "create menu"

## Scene Template

Create scenes at `src/game/scenes/<SceneName>.js`:

```js
import Phaser from 'phaser';

export default class SceneName extends Phaser.Scene {
  constructor() {
    super('SceneName');
  }

  init(data) {
    // Data passed via this.scene.start('SceneName', { key: value })
  }

  create() {
    // Add background
    this.add.image(
      this.scale.width / 2,
      this.scale.height / 2,
      'sky'
    );

    // Add title text
    this.add.text(
      this.scale.width / 2,
      80,
      'Scene Title',
      {
        fontSize: '36px',
        fontFamily: 'Fredoka One',
        color: '#ffffff',
        stroke: '#2c3e50',
        strokeThickness: 4
      }
    ).setOrigin(0.5);
  }

  update(time, delta) {
    // Per-frame logic (only if needed)
  }
}
```

## Registration

After creating the scene file, register it in `src/game/GameConfig.js`:

```js
import NewScene from './scenes/NewScene.js';

export const GameConfig = {
  // ...existing config...
  scene: [BootScene, PreloadScene, MenuScene, /* add here */, NewScene]
};
```

## Conventions

| Convention | Details |
|-----------|---------|
| Class naming | PascalCase ending with `Scene` (e.g., `SettingsScene`) |
| Super key | Match class name: `super('SettingsScene')` |
| Positioning | Use `this.scale.width` / `this.scale.height`, not hardcoded 800/600 |
| Font | `fontFamily: 'Fredoka One'` with stroke for readability |
| Colors | Background: sky blue `#87CEEB`, text: `#ffffff` with `#2c3e50` stroke |
| Transitions | `this.scene.start('NextScene', optionalData)` |
| Buttons | Interactive sprites with `setInteractive()` and `pointerdown` events |
| Text buttons | Use `this.add.text(...).setInteractive()` with hover effects |

## Scene Flow

```
BootScene → PreloadScene → MenuScene → LevelSelectScene → GameScene → LevelCompleteScene
```

New scenes should fit logically into this flow. Common insertion points:
- **After MenuScene**: Settings, credits, how-to-play
- **From LevelCompleteScene**: Achievement details, statistics
- **Parallel to GameScene**: Pause overlay (use `this.scene.launch` + `this.scene.pause`)

## Interactive Button Pattern

```js
const button = this.add.image(x, y, 'btn-play')
  .setInteractive({ useHandCursor: true })
  .on('pointerover', () => button.setScale(1.05))
  .on('pointerout', () => button.setScale(1.0))
  .on('pointerdown', () => {
    this.scene.start('TargetScene');
  });
```

## Text Button Pattern

```js
const btn = this.add.text(x, y, 'Button Text', {
  fontSize: '28px',
  fontFamily: 'Fredoka One',
  color: '#ffffff',
  backgroundColor: '#27ae60',
  padding: { x: 20, y: 10 }
}).setOrigin(0.5).setInteractive({ useHandCursor: true });

btn.on('pointerover', () => btn.setStyle({ backgroundColor: '#2ecc71' }));
btn.on('pointerout', () => btn.setStyle({ backgroundColor: '#27ae60' }));
btn.on('pointerdown', () => this.scene.start('TargetScene'));
```
