# Phase 6: Polish & Launch

## Goal
Add sound effects, particle effects, touch controls for tablets, and deploy to Vercel. By the end, MathBuilder is a polished, publicly accessible game that works on desktops and tablets.

**Depends on:** Phase 4 (full game loop) and Phase 5 (all levels)

---

## Step 6.1 — Sound Effects

### Generating Sounds with sfxr.me

Visit [sfxr.me](https://sfxr.me) — a free browser-based chiptune sound generator. Use the preset buttons and tweak parameters to get the right feel.

| Sound | sfxr.me Preset | Tweaks | Save As |
|-------|---------------|--------|---------|
| **Jump** | Click "Jump" preset | Shorten duration to ~0.15s, raise pitch slightly | `public/assets/audio/jump.wav` |
| **Correct** | Click "Pickup/Coin" preset | Bright, ascending tone. Keep short (~0.3s) | `public/assets/audio/correct.wav` |
| **Wrong** | Click "Hit/Hurt" preset | Low buzzer tone. Make it soft, not scary (~0.2s) | `public/assets/audio/wrong.wav` |
| **Build** | Click "Explosion" preset | Lower volume, increase sustain — should sound like blocks stacking. Detune to sound chunky (~0.4s) | `public/assets/audio/build.wav` |
| **Win** | Click "Powerup" preset | Ascending triumphant sweep. Slightly longer (~0.6s) | `public/assets/audio/win.wav` |

**Important for kids' game:** All sounds should be bright, soft, and non-threatening. Avoid harsh or startling sounds. The "wrong" buzzer should be gentle — like a friendly "oops", not a punishment.

### Integrating Sound into GameScene

Add sound playback calls at the appropriate moments:

```js
// In Player.js — jump:
if (doJump && this.body.blocked.down) {
  this.setVelocityY(this.JUMP_VELOCITY);
  this.scene.sound.play('sfx-jump', { volume: 0.5 });
}

// In MathInputUI.js — correct answer (called from GameScene callback):
// GameScene.onCorrectAnswer():
this.sound.play('sfx-correct', { volume: 0.7 });

// In MathInputUI.js — wrong answer (called from GameScene callback):
// GameScene (in the onResult callback when correct === false):
this.sound.play('sfx-wrong', { volume: 0.4 });

// In Bridge.js — bridge building (called from GameScene):
scene.sound.play('sfx-build', { volume: 0.6 });

// In GameScene.completeLevel():
this.sound.play('sfx-win', { volume: 0.8 });
```

**Volume levels are intentionally varied:**
- Jump: quiet (0.5) — it fires frequently, shouldn't be annoying
- Correct: clear (0.7) — positive reinforcement should be noticeable
- Wrong: soft (0.4) — gentle feedback, not punishing
- Build: medium (0.6) — satisfying construction sound
- Win: prominent (0.8) — celebration moment

### Optional: Mute Button

Add a small mute toggle in the corner of MenuScene:

```js
// In MenuScene.create():
let muted = false;
const muteBtn = this.add.text(760, 30, '🔊', { fontSize: '24px' })
  .setOrigin(0.5)
  .setInteractive({ useHandCursor: true });

muteBtn.on('pointerdown', () => {
  muted = !muted;
  this.sound.mute = muted;
  muteBtn.setText(muted ? '🔇' : '🔊');
});
```

---

## Step 6.2 — Particle Effects

### src/game/systems/ParticleManager.js

Uses Phaser 3.60+ particle emitter API for two effects: dust burst (bridge building) and confetti (level complete).

```js
export class ParticleManager {
  /**
   * Dust burst at a specific position.
   * Used when bridge blocks are placed.
   */
  static dustBurst(scene, x, y) {
    const emitter = scene.add.particles(x, y, 'dust', {
      speed: { min: 50, max: 150 },
      angle: { min: 200, max: 340 },
      lifespan: 400,
      quantity: 8,
      scale: { start: 1, end: 0 },
      alpha: { start: 0.8, end: 0 },
      gravityY: 100,
      emitting: false
    });

    emitter.explode();

    // Auto-cleanup after particles expire
    scene.time.delayedCall(500, () => emitter.destroy());
  }

  /**
   * Confetti rain across the screen.
   * Used on level complete scene.
   */
  static confetti(scene) {
    const emitter = scene.add.particles(400, -20, 'confetti', {
      x: { min: 0, max: 800 },
      speed: { min: 80, max: 250 },
      angle: { min: 75, max: 105 },
      lifespan: 3000,
      quantity: 3,
      frequency: 60,
      scale: { start: 1.5, end: 0.5 },
      rotate: { min: 0, max: 360 },
      tint: [0xff4444, 0x44ff44, 0x4444ff, 0xffff44, 0xff44ff, 0x44ffff],
      gravityY: 150
    });

    // Stop spawning after 2.5 seconds
    scene.time.delayedCall(2500, () => emitter.stop());

    // Destroy after all particles expire
    scene.time.delayedCall(6000, () => emitter.destroy());
  }

  /**
   * Small sparkle at a position.
   * Optional: used when a star fills in on the level complete screen.
   */
  static sparkle(scene, x, y) {
    const emitter = scene.add.particles(x, y, 'confetti', {
      speed: { min: 30, max: 100 },
      angle: { min: 0, max: 360 },
      lifespan: 300,
      quantity: 6,
      scale: { start: 0.8, end: 0 },
      tint: 0xf1c40f,  // Gold
      emitting: false
    });

    emitter.explode();
    scene.time.delayedCall(400, () => emitter.destroy());
  }
}
```

### Integrating Particles

**Bridge building dust** — Modify `Bridge.js` or the GameScene bridge callback:

```js
import { ParticleManager } from '../systems/ParticleManager.js';

// In buildBridge(), after creating each block:
for (let i = 0; i < gapData.width; i++) {
  // ... create block ...

  // Staggered dust burst per block
  scene.time.delayedCall(i * 100, () => {
    ParticleManager.dustBurst(
      scene,
      baseX + i * TILE_SIZE + TILE_SIZE / 2,
      baseY + TILE_SIZE / 2
    );
  });
}
```

The staggered delay (100ms per block) creates a cascade effect — dust poofs from left to right as each block appears.

**Level complete confetti** — In `LevelCompleteScene.create()`:

```js
import { ParticleManager } from '../systems/ParticleManager.js';

// After the stars finish animating (delay ~1500ms):
this.time.delayedCall(1500, () => {
  ParticleManager.confetti(this);
});
```

**Star sparkle** — Optional enhancement in LevelCompleteScene when each star pops in:

```js
// In the star animation tween onComplete:
this.tweens.add({
  targets: star,
  scale: 2.5,
  duration: 400,
  delay: 500 + i * 300,
  ease: 'Back.easeOut',
  onComplete: () => {
    if (isFilled) {
      ParticleManager.sparkle(this, star.x, star.y);
    }
  }
});
```

---

## Step 6.3 — Touch Controls

### src/game/systems/TouchControls.js

Detects if the device supports touch input and creates semi-transparent on-screen buttons for left, right, and jump.

```js
export class TouchControls {
  constructor(scene) {
    this.left = false;
    this.right = false;
    this.jump = false;

    // Only show on touch devices
    if (!scene.sys.game.device.input.touch) return;

    this.createButton(scene, 80, 520, 'arrow-left', 'left');
    this.createButton(scene, 180, 520, 'arrow-right', 'right');
    this.createButton(scene, 720, 520, 'arrow-jump', 'jump');
  }

  createButton(scene, x, y, textureKey, direction) {
    const btn = scene.add.image(x, y, textureKey)
      .setScrollFactor(0)      // Stay fixed on screen
      .setAlpha(0.4)           // Semi-transparent
      .setInteractive()
      .setDepth(1000);         // Always on top

    // Handle multi-touch correctly
    btn.on('pointerdown', () => {
      this[direction] = true;
      btn.setAlpha(0.7);       // Visual press feedback
    });
    btn.on('pointerup', () => {
      this[direction] = false;
      btn.setAlpha(0.4);
    });
    btn.on('pointerout', () => {
      this[direction] = false;
      btn.setAlpha(0.4);
    });
  }
}
```

### Integrating Touch Controls into GameScene

```js
import { TouchControls } from '../systems/TouchControls.js';

// In GameScene.create(), after creating the player:
this.touchControls = new TouchControls(this);
this.player.touchControls = this.touchControls;
```

Player.js already reads `this.touchControls` in its `update()` method (set up in Phase 2).

### Touch Control Layout

```
┌──────────────────────────────────────────┐
│                                          │
│              GAME AREA                   │
│                                          │
│                                          │
│  [←]  [→]                        [↑]    │
│  (80,520) (180,520)           (720,520)  │
└──────────────────────────────────────────┘
```

- Left/Right arrows are in the bottom-left (thumb position for left hand)
- Jump button is in the bottom-right (thumb position for right hand)
- Buttons are semi-transparent (alpha 0.4) so they don't obstruct gameplay
- Buttons become more opaque (alpha 0.7) when pressed for tactile feedback
- `setScrollFactor(0)` keeps them fixed on screen even when the camera scrolls

### Important: Prevent Default Touch Behavior

Add to `index.html` or `style.css` to prevent accidental browser gestures:

```css
#game-container canvas {
  touch-action: none;  /* Prevents pinch-zoom and scroll on canvas */
}
```

And in `GameConfig.js`, add input configuration:

```js
input: {
  activePointers: 3  // Support 3 simultaneous touches (left + right + jump)
}
```

---

## Step 6.4 — Final Polish Touches

### Loading Screen Enhancement

Update `BootScene.js` to show a simple loading spinner or "MathBuilder" logo while the web font loads:

```js
// In BootScene.create():
// Wait for Fredoka One font to be available
document.fonts.ready.then(() => {
  this.scene.start('Preload');
});
```

### Smooth Scene Transitions

Add a simple fade transition between scenes:

```js
// When starting a new scene:
this.cameras.main.fadeOut(300, 0, 0, 0);
this.cameras.main.once('camerafadeoutcomplete', () => {
  this.scene.start('NextScene', data);
});

// At the start of each scene's create():
this.cameras.main.fadeIn(300, 0, 0, 0);
```

### Error Handling for Level Loading

Update `LevelLoader.js` to handle missing levels gracefully:

```js
export async function loadLevel(levelNumber) {
  try {
    const paddedNum = String(levelNumber).padStart(2, '0');
    const response = await fetch(`./levels/world1/level${paddedNum}.json`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  } catch (error) {
    console.error(`Failed to load level ${levelNumber}:`, error);
    // Return to level select on error
    return null;
  }
}
```

---

## Step 6.5 — Vercel Deployment

### Pre-Deployment Checklist

1. **Verify build works:**
   ```bash
   npm run build
   ```
   Confirm `dist/` contains:
   - `index.html`
   - `assets/` folder with all images and audio
   - JavaScript bundle(s)
   - `levels/` folder with all JSON files

2. **Test production build locally:**
   ```bash
   npx vite preview
   ```
   Play through the entire game in the preview build.

3. **Verify `vercel.json`:**
   ```json
   {
     "buildCommand": "npm run build",
     "outputDirectory": "dist"
   }
   ```

4. **Verify `.gitignore`** includes `node_modules/` and `dist/`

5. **Verify `vite.config.js`** has `base: './'` for relative paths

### Deployment Steps

1. Push all code to GitHub:
   ```bash
   git add -A
   git commit -m "MathBuilder v1.0 - World 1 complete"
   git push origin main
   ```

2. Connect GitHub repo to Vercel:
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import the `mathbuilder` repository
   - Vercel auto-detects Vite and configures the build
   - Click "Deploy"

3. Verify the live URL works

### Post-Deployment Testing

Test on each of these platforms:

| Platform | What to Test |
|----------|-------------|
| **Desktop Chrome** | Keyboard controls, all 10 levels, save persistence |
| **Desktop Firefox** | Same as Chrome — verify cross-browser compatibility |
| **iPad Safari** | Touch controls appear, virtual keyboard works for math input, responsive scaling |
| **Android Tablet Chrome** | Same as iPad |
| **iPhone Safari** | Screen fits, touch controls work in portrait and landscape |
| **Android Phone Chrome** | Same as iPhone |

**Critical tablet tests:**
- [ ] Touch control buttons appear automatically
- [ ] Left/right buttons move the player correctly
- [ ] Jump button works while holding a direction (simultaneous multi-touch)
- [ ] Math input overlay shows the numeric keyboard
- [ ] Typing a number and pressing "Build!" works
- [ ] Game scales correctly in both portrait and landscape
- [ ] No pinch-zoom or accidental scrolling on the canvas

---

## Step 6.6 — Performance Audit

Run Chrome Lighthouse on the deployed URL:

**Target scores:**
- Performance: > 80
- Accessibility: > 70
- Best Practices: > 90

**Common issues and fixes:**

| Issue | Fix |
|-------|-----|
| Large images | Compress PNGs with TinyPNG or Squoosh |
| Uncompressed audio | Convert WAV to MP3 (smaller) or use OGG with WAV fallback |
| No meta description | Add `<meta name="description" content="...">` to index.html |
| Missing favicon | Add a favicon (Botty's face, 32x32) |
| Layout shift | Set explicit width/height on the canvas container |

---

## Files Created/Modified in This Phase

| File | Action | Purpose |
|------|--------|---------|
| `src/game/systems/ParticleManager.js` | Create | Dust burst + confetti emitters |
| `src/game/systems/TouchControls.js` | Create | On-screen buttons for tablet |
| `public/assets/audio/*.wav` | Create | 5 sound effect files from sfxr.me |
| `src/game/objects/Player.js` | Modify | Add jump sound |
| `src/game/objects/Bridge.js` | Modify | Add build sound + dust particles |
| `src/game/scenes/GameScene.js` | Modify | Add sounds, touch controls, fade transitions |
| `src/game/scenes/LevelCompleteScene.js` | Modify | Add confetti, star sparkles, win sound |
| `src/game/scenes/MenuScene.js` | Modify | Add mute button, fade transition |
| `src/game/GameConfig.js` | Modify | Add `input.activePointers: 3` |
| `style.css` | Modify | Add `touch-action: none` |
| `index.html` | Modify | Add meta description, favicon |

---

## Verification Checklist — Final

### Sound
- [ ] Jump sound plays on every jump (not too loud, not annoying)
- [ ] Correct answer sound plays — bright and satisfying
- [ ] Wrong answer sound plays — gentle, not scary
- [ ] Bridge build sound plays — chunky construction feel
- [ ] Win sound plays on level completion — triumphant
- [ ] Mute button works and persists visually

### Particles
- [ ] Dust bursts from each bridge block during construction (staggered left to right)
- [ ] Confetti rains on LevelCompleteScene after stars animate
- [ ] Gold sparkles appear when filled stars pop in (optional)
- [ ] No particle-related performance issues (particles self-cleanup)

### Touch Controls
- [ ] Touch buttons appear ONLY on touch-capable devices
- [ ] Touch buttons do NOT appear on desktop
- [ ] Left/right arrows control movement correctly
- [ ] Jump button works while holding a direction
- [ ] Buttons have visual press feedback (opacity change)
- [ ] Buttons stay fixed on screen during camera scroll
- [ ] No accidental pinch-zoom or scroll on the game canvas

### Deployment
- [ ] `npm run build` succeeds without errors
- [ ] Production build plays identically to dev build
- [ ] Vercel deployment is live and accessible
- [ ] Game works on desktop Chrome, Firefox, Safari
- [ ] Game works on iPad Safari with touch controls
- [ ] Game works on Android Chrome with touch controls
- [ ] LocalStorage saves persist across browser sessions on the deployed URL
- [ ] Lighthouse Performance score > 80

### Full Game Playthrough
- [ ] Boot → Preload (progress bar) → Menu → Level Select → Game works
- [ ] All 10 levels are completable
- [ ] Stars accumulate correctly across levels
- [ ] XP accumulates and title updates
- [ ] Level 10 boss gap is solvable and feels like a climactic challenge
- [ ] "Next Level" on level complete correctly advances to the next level
- [ ] After completing level 10, only "Level Select" button appears (no "Next Level")
- [ ] All progress persists after page refresh
