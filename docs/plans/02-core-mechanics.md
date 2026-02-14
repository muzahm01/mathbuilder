# Phase 2: Core Mechanics

## Goal
A placeholder player (red square) can move, jump, encounter gaps, solve math problems via the HTML overlay, and build bridges. Falling off screen restarts the level. This phase uses NO art assets — everything is colored rectangles and debug graphics.

**Depends on:** Phase 1 (project structure running)

---

## Step 2.1 — Grid System

### src/game/systems/GridSystem.js

The entire game world is built on a 64x64 pixel grid. Every platform, gap, player position, and goal flag is defined in grid coordinates and converted to pixel positions at runtime.

```js
export const TILE_SIZE = 64;

/**
 * Convert grid coordinates to pixel coordinates (top-left of the tile).
 */
export function gridToPixel(gridX, gridY) {
  return {
    x: gridX * TILE_SIZE,
    y: gridY * TILE_SIZE
  };
}

/**
 * Convert pixel coordinates to grid coordinates.
 */
export function pixelToGrid(x, y) {
  return {
    gridX: Math.floor(x / TILE_SIZE),
    gridY: Math.floor(y / TILE_SIZE)
  };
}

/**
 * Draw a debug grid overlay. Call this in GameScene's create()
 * and toggle with a constant during development.
 */
export function drawDebugGrid(scene, widthInTiles, heightInTiles) {
  const graphics = scene.add.graphics();
  graphics.lineStyle(1, 0xffffff, 0.15);

  for (let x = 0; x <= widthInTiles; x++) {
    graphics.moveTo(x * TILE_SIZE, 0);
    graphics.lineTo(x * TILE_SIZE, heightInTiles * TILE_SIZE);
  }
  for (let y = 0; y <= heightInTiles; y++) {
    graphics.moveTo(0, y * TILE_SIZE);
    graphics.lineTo(widthInTiles * TILE_SIZE, y * TILE_SIZE);
  }

  graphics.strokePath();
  graphics.setDepth(1000); // Always on top during debug
  return graphics;
}
```

**Why 64x64?**
- Divides evenly into 800x600 (12.5 x 9.375 tiles) — close enough for clean layouts
- Large enough for a 7-year-old to visually count tiles in a gap
- Standard power-of-two size that works well with texture atlases later

---

## Step 2.2 — Player

### src/game/objects/Player.js

The Player class handles movement, jumping, and input reading. In this phase it renders as a red square placeholder.

```js
import Phaser from 'phaser';
import { TILE_SIZE, gridToPixel } from '../systems/GridSystem.js';

export default class Player extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, gridX, gridY) {
    // Create a placeholder red square texture (replaced with Botty in Phase 3)
    if (!scene.textures.exists('player-placeholder')) {
      const canvas = scene.textures.createCanvas('player-placeholder', TILE_SIZE, TILE_SIZE);
      const ctx = canvas.getContext();
      ctx.fillStyle = '#e74c3c';
      ctx.fillRect(0, 0, TILE_SIZE, TILE_SIZE);
      canvas.refresh();
    }

    const { x, y } = gridToPixel(gridX, gridY);
    super(scene, x + TILE_SIZE / 2, y + TILE_SIZE / 2, 'player-placeholder');

    scene.add.existing(this);
    scene.physics.add.existing(this);

    // Physics body setup
    this.setCollideWorldBounds(false); // Allow falling off-screen (death)
    this.setBounce(0.1);
    this.body.setSize(TILE_SIZE - 8, TILE_SIZE - 4); // Slightly smaller hitbox for forgiving collisions
    this.body.setOffset(4, 4);

    // Movement constants
    this.MOVE_SPEED = 200;
    this.JUMP_VELOCITY = -450;

    // Input
    this.cursors = scene.input.keyboard.createCursorKeys();

    // Reference to touch controls (set from GameScene if available)
    this.touchControls = null;
  }

  update() {
    // Skip movement when game is paused (math input visible)
    if (!this.scene || !this.scene.physics.world.isPaused === false) {
      // Physics is paused, don't process input
    }

    const moveLeft = this.cursors.left.isDown ||
      (this.touchControls && this.touchControls.left);
    const moveRight = this.cursors.right.isDown ||
      (this.touchControls && this.touchControls.right);
    const doJump = this.cursors.up.isDown ||
      (this.touchControls && this.touchControls.jump);

    // Horizontal movement
    if (moveLeft) {
      this.setVelocityX(-this.MOVE_SPEED);
      this.setFlipX(true);
    } else if (moveRight) {
      this.setVelocityX(this.MOVE_SPEED);
      this.setFlipX(false);
    } else {
      this.setVelocityX(0);
    }

    // Jumping (only when on the ground)
    if (doJump && this.body.blocked.down) {
      this.setVelocityY(this.JUMP_VELOCITY);
    }
  }
}
```

**Movement tuning:**
- `MOVE_SPEED: 200` — Moderate speed suitable for a child player. Not too fast to lose control.
- `JUMP_VELOCITY: -450` — With gravity of 800, this produces a jump height of roughly 2 tiles (128px), enough to jump onto elevated platforms.
- `bounce: 0.1` — Tiny bounce on landing feels more alive than a dead stop.
- Hitbox is 4px smaller on each side for "forgiving" collision — prevents frustrating pixel-perfect edge catches.

---

## Step 2.3 — Level Loader

### src/game/systems/LevelLoader.js

Fetches level JSON files from the `public/levels/` directory at runtime.

```js
/**
 * Load a level JSON file by number.
 * Files are stored at /levels/world1/level01.json, etc.
 */
export async function loadLevel(levelNumber) {
  const paddedNum = String(levelNumber).padStart(2, '0');
  const url = `./levels/world1/level${paddedNum}.json`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to load level ${levelNumber}: ${response.status}`);
  }

  return response.json();
}
```

**Why `fetch()` instead of Phaser's loader?**
- Level data is pure JSON, not a game asset — no need for Phaser's preload pipeline
- `fetch()` gives us `async/await` for cleaner code in scene `create()`
- Levels can be loaded on-demand rather than all upfront

---

## Step 2.4 — Game Scene (Core Orchestrator)

### src/game/scenes/GameScene.js

This is the most complex file in the project. It orchestrates level loading, platform creation, gap detection, math input triggers, bridge building, fall detection, and goal completion.

```js
import Phaser from 'phaser';
import { TILE_SIZE, gridToPixel, drawDebugGrid } from '../systems/GridSystem.js';
import { loadLevel } from '../systems/LevelLoader.js';
import { MathInputUI } from '../systems/MathInputUI.js';
import { buildBridge } from '../objects/Bridge.js';
import Player from '../objects/Player.js';

const DEBUG_GRID = true; // Set to false to hide grid lines

export default class GameScene extends Phaser.Scene {
  constructor() {
    super('Game');
  }

  init(data) {
    // Receive level number from previous scene (default to 1)
    this.levelNumber = data.levelNumber || 1;
    this.wrongAttempts = 0; // Track wrong answers for star rating
  }

  async create() {
    // ── Load Level Data ──────────────────────────────
    const levelData = await loadLevel(this.levelNumber);

    // ── Set World Bounds ─────────────────────────────
    const worldWidth = levelData.gridWidth * TILE_SIZE;
    const worldHeight = levelData.gridHeight * TILE_SIZE;
    this.physics.world.setBounds(0, 0, worldWidth, worldHeight);

    // ── Debug Grid (toggle with DEBUG_GRID constant) ─
    if (DEBUG_GRID) {
      drawDebugGrid(this, levelData.gridWidth, levelData.gridHeight);
    }

    // ── Build Platforms ──────────────────────────────
    this.platforms = this.physics.add.staticGroup();

    for (const p of levelData.platforms) {
      const { x: baseX, y: baseY } = gridToPixel(p.gridX, p.gridY);

      for (let i = 0; i < p.width; i++) {
        // Create placeholder green rectangles (replaced with tiles in Phase 3)
        if (!this.textures.exists('tile-placeholder')) {
          const canvas = this.textures.createCanvas('tile-placeholder', TILE_SIZE, TILE_SIZE);
          const ctx = canvas.getContext();
          ctx.fillStyle = '#27ae60';
          ctx.fillRect(0, 0, TILE_SIZE, TILE_SIZE);
          ctx.strokeStyle = '#1e8449';
          ctx.lineWidth = 2;
          ctx.strokeRect(0, 0, TILE_SIZE, TILE_SIZE);
          canvas.refresh();
        }

        const block = this.platforms.create(
          baseX + i * TILE_SIZE + TILE_SIZE / 2,
          baseY + TILE_SIZE / 2,
          'tile-placeholder'
        );
        block.setSize(TILE_SIZE, TILE_SIZE);
        block.refreshBody();
      }
    }

    // ── Build Gap Trigger Zones ──────────────────────
    this.gapZones = [];

    for (const g of levelData.gaps) {
      const { x, y } = gridToPixel(g.gridX, g.gridY);

      // The zone sits IN the gap area, one tile tall
      // When the player overlaps it (falls into the gap area), trigger math input
      const zone = this.add.zone(
        x + (g.width * TILE_SIZE) / 2,   // Center of the gap horizontally
        y - TILE_SIZE / 2,                // One tile above the gap floor
        g.width * TILE_SIZE,              // Full gap width
        TILE_SIZE                          // One tile tall
      );
      this.physics.add.existing(zone, true); // Static physics body

      // Attach gap metadata directly to the zone
      zone.gapData = g;
      zone.solved = false;

      this.gapZones.push(zone);

      // Debug: visualize the gap zone
      if (DEBUG_GRID) {
        this.add.rectangle(
          x + (g.width * TILE_SIZE) / 2,
          y - TILE_SIZE / 2,
          g.width * TILE_SIZE,
          TILE_SIZE,
          0xff0000, 0.2
        );
      }
    }

    // ── Create Player ────────────────────────────────
    this.player = new Player(
      this,
      levelData.start.gridX,
      levelData.start.gridY
    );

    // ── Collisions ───────────────────────────────────
    this.physics.add.collider(this.player, this.platforms);

    // Gap overlap detection
    for (const zone of this.gapZones) {
      this.physics.add.overlap(this.player, zone, () => {
        if (!zone.solved && !this.mathInputActive) {
          this.openMathInput(zone);
        }
      });
    }

    // ── Goal Flag (placeholder) ──────────────────────
    const goalPos = gridToPixel(levelData.goal.gridX, levelData.goal.gridY);
    this.goalFlag = this.add.rectangle(
      goalPos.x + TILE_SIZE / 2,
      goalPos.y + TILE_SIZE / 2,
      TILE_SIZE,
      TILE_SIZE * 1.5,
      0xf1c40f  // Yellow placeholder
    );
    this.physics.add.existing(this.goalFlag, true);
    this.physics.add.overlap(this.player, this.goalFlag, () => {
      this.completeLevel();
    });

    // ── Camera ───────────────────────────────────────
    this.cameras.main.setBounds(0, 0, worldWidth, worldHeight);
    this.cameras.main.startFollow(this.player, true, 0.1, 0.1);

    // ── Math Input UI ────────────────────────────────
    this.mathInputActive = false;
    this.mathUI = new MathInputUI((gapData, correct) => {
      if (correct) {
        this.onCorrectAnswer(gapData);
      } else {
        this.wrongAttempts++;
      }
    });

    // ── Store level data for later reference ─────────
    this.levelData = levelData;
  }

  update() {
    if (!this.player) return;

    // Player movement
    this.player.update();

    // Fall death detection
    if (this.player.y > this.levelData.gridHeight * TILE_SIZE + 100) {
      this.restartLevel();
    }
  }

  // ── Math Input ───────────────────────────────────────

  openMathInput(zone) {
    this.mathInputActive = true;
    this.physics.pause();
    this.mathUI.show(zone.gapData);
  }

  onCorrectAnswer(gapData) {
    // Find and mark the zone as solved
    const zone = this.gapZones.find(z => z.gapData === gapData);
    if (zone) zone.solved = true;

    // Build the bridge
    buildBridge(this, gapData, this.platforms);

    // Resume gameplay
    this.mathInputActive = false;
    this.physics.resume();
  }

  // ── Level Flow ───────────────────────────────────────

  completeLevel() {
    // Prevent double-triggering
    if (this.levelComplete) return;
    this.levelComplete = true;

    // Calculate star rating
    let stars;
    if (this.wrongAttempts === 0) stars = 3;
    else if (this.wrongAttempts <= 2) stars = 2;
    else stars = 1;

    // Transition to level complete scene (Phase 4)
    // For now, just restart
    this.scene.start('Game', { levelNumber: this.levelNumber });
  }

  restartLevel() {
    this.mathUI.hide();
    this.scene.restart({ levelNumber: this.levelNumber });
  }
}
```

**Architecture notes:**

- **`init(data)`** receives the level number from the previous scene (LevelSelectScene or LevelCompleteScene). This is how we pass data between Phaser scenes.
- **`async create()`** — Phaser supports async create methods. We use this to `await loadLevel()` before building the scene.
- **`mathInputActive` flag** — Prevents re-triggering the math input while it's already open. Without this, continuous overlap detection would fire repeatedly.
- **`wrongAttempts` counter** — Tracks total wrong answers across ALL gaps in the level (not per gap). Used for star rating in Phase 4.
- **Camera follow** — `startFollow` with lerp values (0.1, 0.1) creates smooth camera movement rather than rigid tracking. For levels that fit within 800px, the camera stays stationary.

---

## Step 2.5 — Math Input UI

### src/game/systems/MathInputUI.js

Controls the HTML overlay defined in `index.html`. This is the bridge between the DOM world and the Phaser world.

```js
export class MathInputUI {
  /**
   * @param {Function} onResult - Called with (gapData, isCorrect) on each submission
   */
  constructor(onResult) {
    this.overlay = document.getElementById('math-input-overlay');
    this.input = document.getElementById('math-answer-input');
    this.feedback = document.getElementById('math-feedback');
    this.submitBtn = document.getElementById('math-submit-btn');
    this.onResult = onResult;
    this.currentGap = null;

    // Bind event listeners
    this.submitBtn.addEventListener('click', () => this.handleSubmit());
    this.input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') this.handleSubmit();
    });
  }

  /**
   * Show the math input overlay for a specific gap.
   */
  show(gapData) {
    this.currentGap = gapData;
    this.input.value = '';
    this.feedback.textContent = '';
    this.feedback.style.color = '';
    this.overlay.style.display = 'flex';

    // Focus the input after a short delay (allows overlay to render)
    setTimeout(() => this.input.focus(), 100);
  }

  /**
   * Hide the math input overlay.
   */
  hide() {
    this.overlay.style.display = 'none';
    this.currentGap = null;
  }

  /**
   * Process the player's answer.
   */
  handleSubmit() {
    const answer = parseInt(this.input.value, 10);

    // Ignore empty or non-numeric input
    if (isNaN(answer) || answer < 1) {
      this.input.value = '';
      return;
    }

    const correct = this.currentGap.correctAnswer;

    if (answer === correct) {
      // ── Correct! ──────────────────────────
      this.feedback.textContent = 'Correct!';
      this.feedback.style.color = '#27ae60';
      this.onResult(this.currentGap, true);

      // Brief pause to show "Correct!" then hide
      setTimeout(() => this.hide(), 600);

    } else if (answer < correct) {
      // ── Too small ─────────────────────────
      this.feedback.textContent = 'Too Short! Try again.';
      this.feedback.style.color = '#e74c3c';
      this.input.value = '';
      this.input.focus();
      this.onResult(this.currentGap, false);

    } else {
      // ── Too large ─────────────────────────
      this.feedback.textContent = 'Too Long! Try again.';
      this.feedback.style.color = '#e74c3c';
      this.input.value = '';
      this.input.focus();
      this.onResult(this.currentGap, false);
    }
  }
}
```

**Feedback design:**
- "Too Short!" and "Too Long!" are more intuitive for a child than "Wrong!" — they give directional hints that connect the number to the physical gap
- The input clears on wrong answer so the child can try again immediately
- 600ms delay on correct answer lets the child see "Correct!" before the overlay disappears
- `onResult` fires on EVERY submission (correct or wrong) so GameScene can track wrong attempts

---

## Step 2.6 — Bridge Builder

### src/game/objects/Bridge.js

Spawns bridge blocks when the player answers correctly. Each block is added to the existing platform physics group so the player can immediately walk on them.

```js
import { TILE_SIZE, gridToPixel } from '../systems/GridSystem.js';

/**
 * Build a bridge of N blocks at the gap position.
 * Blocks are added to the existing platform static group.
 */
export function buildBridge(scene, gapData, platformGroup) {
  const { x: baseX, y: baseY } = gridToPixel(gapData.gridX, gapData.gridY);

  // Create placeholder brown bridge texture
  if (!scene.textures.exists('bridge-placeholder')) {
    const canvas = scene.textures.createCanvas('bridge-placeholder', TILE_SIZE, TILE_SIZE);
    const ctx = canvas.getContext();
    ctx.fillStyle = '#8B4513';
    ctx.fillRect(0, 0, TILE_SIZE, TILE_SIZE);
    ctx.strokeStyle = '#654321';
    ctx.lineWidth = 2;
    ctx.strokeRect(2, 2, TILE_SIZE - 4, TILE_SIZE - 4);
    // Horizontal plank lines
    ctx.strokeStyle = '#654321';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, TILE_SIZE / 3);
    ctx.lineTo(TILE_SIZE, TILE_SIZE / 3);
    ctx.moveTo(0, (TILE_SIZE / 3) * 2);
    ctx.lineTo(TILE_SIZE, (TILE_SIZE / 3) * 2);
    ctx.stroke();
    canvas.refresh();
  }

  for (let i = 0; i < gapData.width; i++) {
    const block = platformGroup.create(
      baseX + i * TILE_SIZE + TILE_SIZE / 2,
      baseY + TILE_SIZE / 2,
      'bridge-placeholder'
    );
    block.setSize(TILE_SIZE, TILE_SIZE);
    block.refreshBody();
  }
}
```

**Why add to the existing `platformGroup`?**
- The collider between `player` and `platforms` is already set up — new blocks automatically participate
- No need to create a separate collider or physics group for bridges
- The bridge visually and physically becomes part of the level

---

## Step 2.7 — Test Level

### public/levels/world1/level01.json

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
    },
    {
      "gridX": 11,
      "gridY": 8,
      "width": 14,
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

**Visual layout (grid view):**

```
Grid Y:  0  1  2  3  4  5  6  7  8

Col 0-7:                     [P]  ████████   <- Left platform (8 blocks)
Col 8-10:                         ___GAP___  <- 3-block gap (answer: 3)
Col 11-24:                   [F]  ██████████████  <- Right platform (14 blocks)

P = Player start (1, 7)
F = Goal flag (23, 7)
```

**How the gap works visually:**
- Left platform ends at gridX=7 (8 blocks from 0-7)
- Gap starts at gridX=8 and is 3 tiles wide (gridX 8, 9, 10)
- Right platform starts at gridX=11
- The player can see 3 empty tiles and must count them: the answer is 3

---

## Step 2.8 — Update GameConfig Scenes

Update `src/game/GameConfig.js` to include GameScene:

```js
import BootScene from './scenes/BootScene.js';
import GameScene from './scenes/GameScene.js';

// In the config:
scene: [BootScene, GameScene]
```

Update `BootScene.js` to transition to GameScene after a brief delay:

```js
create() {
  // ... existing title text ...

  // Auto-transition to game after 1 second
  this.time.delayedCall(1000, () => {
    this.scene.start('Game', { levelNumber: 1 });
  });
}
```

---

## Gap Detection — How It Works

The gap detection system deserves extra explanation since it's the core mechanic:

```
1. Level JSON defines gaps with position + width + correctAnswer
2. GameScene creates invisible Phaser Zones at each gap location
3. Each Zone has a static physics body for overlap detection
4. When the player's physics body overlaps a Zone:
   a. Check if zone.solved === false (hasn't been answered yet)
   b. Check if mathInputActive === false (overlay not already open)
   c. If both true: pause physics, show HTML overlay
5. Player types a number and clicks "Build!" (or presses Enter)
6. MathInputUI compares answer to correctAnswer:
   - Wrong: show feedback, increment wrongAttempts, clear input
   - Correct: show "Correct!", call onResult callback
7. GameScene receives correct callback:
   a. Mark zone.solved = true
   b. Call buildBridge() to spawn platform blocks
   c. Resume physics
   d. Hide overlay
8. Player can now walk across the bridge
```

**Edge case handling:**
- Zone trigger area is positioned one tile ABOVE the gap floor — this means the player triggers it by walking to the edge, not by falling in
- `mathInputActive` flag prevents re-triggering if the player's physics body still overlaps after resuming
- `zone.solved` flag prevents re-triggering on subsequent overlaps after building the bridge

---

## Files Created/Modified in This Phase

| File | Action | Purpose |
|------|--------|---------|
| `src/game/systems/GridSystem.js` | Create | Grid constants and coordinate helpers |
| `src/game/objects/Player.js` | Create | Player movement and input handling |
| `src/game/systems/LevelLoader.js` | Create | Level JSON fetcher |
| `src/game/scenes/GameScene.js` | Create | Core gameplay orchestration |
| `src/game/systems/MathInputUI.js` | Create | HTML overlay controller |
| `src/game/objects/Bridge.js` | Create | Bridge block spawner |
| `public/levels/world1/level01.json` | Create | Test level |
| `src/game/GameConfig.js` | Modify | Add GameScene to scene list |
| `src/game/scenes/BootScene.js` | Modify | Add transition to GameScene |

---

## Verification Checklist

- [ ] Red square (player) spawns on the left platform at grid position (1, 7)
- [ ] Arrow keys move the player left and right smoothly
- [ ] Up arrow makes the player jump ONLY when touching the ground (no double-jump)
- [ ] Walking to the right edge of the left platform and approaching the gap triggers the math input overlay
- [ ] Game physics pause while the overlay is visible (player freezes in place)
- [ ] Typing a number smaller than 3 shows "Too Short! Try again." in red
- [ ] Typing a number larger than 3 shows "Too Long! Try again." in red
- [ ] Input clears after a wrong answer and re-focuses for immediate retry
- [ ] Typing 3 shows "Correct!" in green, then the overlay closes after ~600ms
- [ ] 3 brown bridge blocks appear filling the gap
- [ ] Player can walk across the bridge blocks seamlessly (no falling through)
- [ ] Approaching the gap zone again does NOT re-trigger the overlay (zone is solved)
- [ ] Reaching the yellow goal flag rectangle triggers level completion (restart for now)
- [ ] Walking off the bottom of the screen restarts the level
- [ ] The debug grid is visible and lines up with platforms and gap edges
- [ ] No console errors in browser dev tools
- [ ] Camera follows player horizontally (test by making a wider level temporarily)
