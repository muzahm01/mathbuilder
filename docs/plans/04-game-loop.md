# Phase 4: Game Loop & Progression

## Goal
Transform the single-level prototype into a full game with a menu, level select screen, save system, star ratings, XP accumulation, and a title/rank system. By the end, the player has a complete gameplay loop: Menu → Select Level → Play → Complete → See Stars → Next Level.

**Depends on:** Phase 2 (GameScene), Phase 3 (PreloadScene with assets)

---

## Step 4.1 — Goal Flag

### src/game/objects/GoalFlag.js

A sprite placed at the goal position defined in the level JSON. When the player overlaps it, the level is complete.

```js
import Phaser from 'phaser';
import { TILE_SIZE, gridToPixel } from '../systems/GridSystem.js';

export default class GoalFlag extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, gridX, gridY) {
    const { x, y } = gridToPixel(gridX, gridY);

    super(scene, x + TILE_SIZE / 2, y + TILE_SIZE / 2, 'flag');

    scene.add.existing(this);
    scene.physics.add.existing(this, true); // Static body

    // Gentle floating animation
    scene.tweens.add({
      targets: this,
      y: this.y - 8,
      duration: 1000,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut'
    });
  }
}
```

**Update GameScene.js** to use GoalFlag instead of the placeholder rectangle:

```js
import GoalFlag from '../objects/GoalFlag.js';

// In create(), replace the goal rectangle with:
this.goalFlag = new GoalFlag(this, levelData.goal.gridX, levelData.goal.gridY);
this.physics.add.overlap(this.player, this.goalFlag, () => {
  this.completeLevel();
});
```

---

## Step 4.2 — Star Rating System

Stars are earned based on wrong attempts across the ENTIRE level (all gaps combined):

| Wrong Attempts | Stars | Description |
|---------------|-------|-------------|
| 0 | 3 stars | Perfect — every gap answered correctly first try |
| 1-2 | 2 stars | Good — a couple of mistakes |
| 3+ | 1 star | Keep trying — you still completed it! |

**The player always gets at least 1 star for completing a level.** There is no 0-star state — completing a level is always a win.

**Implementation in GameScene.js:**

`wrongAttempts` is already tracked in Phase 2 (incremented in the `onResult` callback for wrong answers). The star calculation happens in `completeLevel()`:

```js
completeLevel() {
  if (this.levelComplete) return;
  this.levelComplete = true;

  // Calculate stars
  let stars;
  if (this.wrongAttempts === 0) stars = 3;
  else if (this.wrongAttempts <= 2) stars = 2;
  else stars = 1;

  // Calculate XP
  const gapCount = this.levelData.gaps.length;
  const xpEarned = (gapCount * 10) + (stars * 5);

  // Save progress
  const saveData = SaveManager.completeLevel(this.levelNumber, stars, xpEarned);

  // Transition to level complete scene
  this.scene.start('LevelComplete', {
    levelNumber: this.levelNumber,
    stars: stars,
    xpEarned: xpEarned,
    totalXP: saveData.totalXP,
    title: saveData.title
  });
}
```

---

## Step 4.3 — XP System

XP is the currency for progression titles. It accumulates across all level completions.

### XP Formula

```
XP per level completion = (number_of_gaps × 10) + (stars_earned × 5)
```

**Examples:**

| Level | Gaps | Stars | XP Earned | Breakdown |
|-------|------|-------|-----------|-----------|
| Level 1 | 1 gap | 3 stars | 25 XP | (1×10) + (3×5) |
| Level 1 | 1 gap | 1 star | 15 XP | (1×10) + (1×5) |
| Level 5 | 2 gaps | 3 stars | 35 XP | (2×10) + (3×5) |
| Level 7 | 3 gaps | 2 stars | 40 XP | (3×10) + (2×5) |
| Level 10 | 1 gap | 3 stars | 25 XP | (1×10) + (3×5) |

**XP is cumulative** — replaying a level always earns XP, encouraging replay.

**Maximum possible XP from one playthrough of all 10 levels:**
Each level at 3 stars: roughly 25-40 XP per level = ~300 XP total for World 1 (enough to reach "Bridge Builder" title).

---

## Step 4.4 — Save Manager

### src/game/systems/SaveManager.js

Handles all persistence via `localStorage`. One key stores the entire save as JSON.

```js
import { TitleSystem } from './TitleSystem.js';

const SAVE_KEY = 'mathbuilder_save';

const DEFAULT_SAVE = {
  currentLevel: 1,
  maxUnlockedLevel: 1,
  stars: {},       // { "1": 3, "2": 2, "3": 1 }
  totalXP: 0,
  title: 'Newbie'
};

export class SaveManager {
  /**
   * Load save data from LocalStorage.
   * Returns default save if no data exists or data is corrupt.
   */
  static load() {
    const raw = localStorage.getItem(SAVE_KEY);
    if (!raw) return { ...DEFAULT_SAVE };

    try {
      const data = JSON.parse(raw);
      // Basic validation: ensure required fields exist
      return {
        ...DEFAULT_SAVE,
        ...data
      };
    } catch {
      return { ...DEFAULT_SAVE };
    }
  }

  /**
   * Write save data to LocalStorage.
   */
  static save(data) {
    localStorage.setItem(SAVE_KEY, JSON.stringify(data));
  }

  /**
   * Record a level completion.
   * Only updates stars if the new result is better than the previous best.
   * Always adds XP (encourages replay).
   * Unlocks the next level.
   * Returns the updated save data.
   */
  static completeLevel(levelNumber, starsEarned, xpEarned) {
    const data = this.load();

    // Update stars (keep best)
    const prevStars = data.stars[String(levelNumber)] || 0;
    if (starsEarned > prevStars) {
      data.stars[String(levelNumber)] = starsEarned;
    }

    // Add XP
    data.totalXP += xpEarned;

    // Update title
    data.title = TitleSystem.getTitle(data.totalXP);

    // Unlock next level
    if (levelNumber >= data.maxUnlockedLevel && levelNumber < 10) {
      data.maxUnlockedLevel = levelNumber + 1;
    }

    this.save(data);
    return data;
  }

  /**
   * Get stars for a specific level (0 if never completed).
   */
  static getStars(levelNumber) {
    const data = this.load();
    return data.stars[String(levelNumber)] || 0;
  }

  /**
   * Reset all progress (for testing or "New Game").
   */
  static reset() {
    localStorage.removeItem(SAVE_KEY);
  }
}
```

**Design decisions:**
- **Stars: keep best** — Replaying a level with fewer stars doesn't overwrite your best performance
- **XP: always additive** — This encourages replay and prevents "XP loss" anxiety
- **Level unlock: sequential** — Complete level N to unlock N+1. Simple and predictable.
- **Spread operator merge** — `{ ...DEFAULT_SAVE, ...data }` ensures new fields added in updates don't break old saves
- **String keys for stars** — JSON doesn't support numeric object keys natively, so we use strings

---

## Step 4.5 — Title System

### src/game/systems/TitleSystem.js

Maps cumulative XP to fun title/rank strings displayed on the menu.

```js
const TITLES = [
  { xp: 0,    title: 'Newbie' },
  { xp: 50,   title: 'Math Cadet' },
  { xp: 100,  title: 'Number Ninja' },
  { xp: 200,  title: 'Bridge Builder' },
  { xp: 350,  title: 'Team Leader' },
  { xp: 500,  title: 'Math Master' },
  { xp: 750,  title: 'Grand Master' },
  { xp: 1000, title: 'Legend' }
];

export class TitleSystem {
  /**
   * Get the highest title earned for a given XP amount.
   */
  static getTitle(totalXP) {
    let result = TITLES[0].title;
    for (const t of TITLES) {
      if (totalXP >= t.xp) {
        result = t.title;
      } else {
        break;
      }
    }
    return result;
  }

  /**
   * Get progress info toward the next title.
   * Returns { currentTitle, nextTitle, currentXP, xpNeeded, progress (0-1) }
   */
  static getProgress(totalXP) {
    let currentIdx = 0;
    for (let i = 0; i < TITLES.length; i++) {
      if (totalXP >= TITLES[i].xp) {
        currentIdx = i;
      } else {
        break;
      }
    }

    const current = TITLES[currentIdx];
    const next = TITLES[currentIdx + 1] || null;

    if (!next) {
      // Max title reached
      return {
        currentTitle: current.title,
        nextTitle: null,
        currentXP: totalXP,
        xpNeeded: 0,
        progress: 1
      };
    }

    const xpIntoCurrentTier = totalXP - current.xp;
    const xpForNextTier = next.xp - current.xp;

    return {
      currentTitle: current.title,
      nextTitle: next.title,
      currentXP: totalXP,
      xpNeeded: next.xp - totalXP,
      progress: xpIntoCurrentTier / xpForNextTier
    };
  }
}
```

**Title progression feel:**
- First 3 titles (Newbie → Math Cadet → Number Ninja) come quickly to give early dopamine
- Mid-tier titles require more XP (replaying levels or achieving better stars)
- "Legend" at 1000 XP is aspirational — requires replaying many levels at high stars

---

## Step 4.6 — Menu Scene

### src/game/scenes/MenuScene.js

The first screen the player sees. Shows the game title, a Play button, and the player's current rank.

```js
import Phaser from 'phaser';
import { SaveManager } from '../systems/SaveManager.js';

export default class MenuScene extends Phaser.Scene {
  constructor() {
    super('Menu');
  }

  create() {
    const { width, height } = this.scale;

    // ── Background ─────────────────────────────────
    this.add.image(width / 2, height / 2, 'sky');

    // ── Title ──────────────────────────────────────
    const title = this.add.text(width / 2, 140, 'MathBuilder', {
      fontSize: '56px',
      fontFamily: 'Fredoka One',
      color: '#ffffff',
      stroke: '#2c3e50',
      strokeThickness: 8
    }).setOrigin(0.5);

    // Gentle floating animation
    this.tweens.add({
      targets: title,
      y: title.y - 10,
      duration: 2000,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut'
    });

    // ── Botty (idle animation) ─────────────────────
    const botty = this.add.sprite(width / 2, 280, 'botty-idle');
    botty.play('botty-idle');
    botty.setScale(2); // Bigger on menu for visual impact

    // ── Play Button ────────────────────────────────
    const playBtn = this.add.image(width / 2, 420, 'btn-play')
      .setInteractive({ useHandCursor: true });

    playBtn.on('pointerover', () => playBtn.setScale(1.1));
    playBtn.on('pointerout', () => playBtn.setScale(1));
    playBtn.on('pointerdown', () => {
      this.scene.start('LevelSelect');
    });

    // ── Current Rank ───────────────────────────────
    const saveData = SaveManager.load();

    this.add.text(width / 2, 520, `Rank: ${saveData.title}`, {
      fontSize: '22px',
      fontFamily: 'Fredoka One',
      color: '#f39c12'
    }).setOrigin(0.5);

    this.add.text(width / 2, 555, `${saveData.totalXP} XP`, {
      fontSize: '16px',
      fontFamily: 'Fredoka One',
      color: '#bdc3c7'
    }).setOrigin(0.5);
  }
}
```

**UX notes:**
- Play button has hover scale feedback (desktop) and pointer cursor
- Botty at 2x scale serves as the "mascot" focal point
- Rank and XP at the bottom give returning players a reason to keep playing
- The floating title animation adds life without being distracting

---

## Step 4.7 — Level Select Scene

### src/game/scenes/LevelSelectScene.js

Displays 10 level buttons in a 5x2 grid. Shows stars for completed levels and locks for unavailable levels.

```js
import Phaser from 'phaser';
import { SaveManager } from '../systems/SaveManager.js';

export default class LevelSelectScene extends Phaser.Scene {
  constructor() {
    super('LevelSelect');
  }

  create() {
    const { width, height } = this.scale;
    const saveData = SaveManager.load();

    // ── Background ─────────────────────────────────
    this.add.image(width / 2, height / 2, 'sky');

    // ── Header ─────────────────────────────────────
    this.add.text(width / 2, 50, 'World 1: Grasslands', {
      fontSize: '32px',
      fontFamily: 'Fredoka One',
      color: '#ffffff',
      stroke: '#2c3e50',
      strokeThickness: 4
    }).setOrigin(0.5);

    // ── Level Grid (5 columns × 2 rows) ────────────
    const startX = 120;
    const startY = 140;
    const spacingX = 140;
    const spacingY = 200;

    for (let i = 0; i < 10; i++) {
      const col = i % 5;
      const row = Math.floor(i / 5);
      const x = startX + col * spacingX;
      const y = startY + row * spacingY;
      const levelNum = i + 1;
      const isUnlocked = levelNum <= saveData.maxUnlockedLevel;
      const stars = saveData.stars[String(levelNum)] || 0;

      this.createLevelButton(x, y, levelNum, isUnlocked, stars);
    }

    // ── Back Button ────────────────────────────────
    const backText = this.add.text(60, height - 40, '< Back', {
      fontSize: '20px',
      fontFamily: 'Fredoka One',
      color: '#ffffff'
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });

    backText.on('pointerdown', () => this.scene.start('Menu'));
  }

  createLevelButton(x, y, levelNum, isUnlocked, stars) {
    // ── Button Background ────────────────────────
    const bg = this.add.rectangle(x, y, 100, 100, isUnlocked ? 0x3498db : 0x7f8c8d)
      .setStrokeStyle(3, isUnlocked ? 0x2980b9 : 0x636e72);

    if (isUnlocked) {
      bg.setInteractive({ useHandCursor: true });

      bg.on('pointerover', () => bg.setScale(1.1));
      bg.on('pointerout', () => bg.setScale(1));
      bg.on('pointerdown', () => {
        this.scene.start('Game', { levelNumber: levelNum });
      });
    }

    // ── Level Number ─────────────────────────────
    const color = isUnlocked ? '#ffffff' : '#bdc3c7';
    this.add.text(x, y - 10, String(levelNum), {
      fontSize: '36px',
      fontFamily: 'Fredoka One',
      color: color
    }).setOrigin(0.5);

    // ── Stars ────────────────────────────────────
    if (isUnlocked) {
      for (let s = 0; s < 3; s++) {
        const starKey = s < stars ? 'star-filled' : 'star-empty';
        this.add.image(
          x - 24 + s * 24,   // Spread 3 stars across 48px
          y + 30,
          starKey
        ).setScale(0.7);
      }
    } else {
      // Lock icon (text placeholder, could be an image)
      this.add.text(x, y + 25, '🔒', {
        fontSize: '20px'
      }).setOrigin(0.5);
    }
  }
}
```

**Layout:**
```
   1       2       3       4       5
  ★★★     ★★☆     ★☆☆     ☆☆☆     🔒

   6       7       8       9      10
  🔒      🔒      🔒      🔒      🔒
```

**UX notes:**
- Unlocked levels are blue, locked are grey — instantly clear
- Stars below each level show best performance at a glance
- Hover scale provides feedback on desktop; tap works on mobile
- Back button returns to menu

---

## Step 4.8 — Level Complete Scene

### src/game/scenes/LevelCompleteScene.js

The reward screen after completing a level. Stars animate in one by one for dramatic effect.

```js
import Phaser from 'phaser';

export default class LevelCompleteScene extends Phaser.Scene {
  constructor() {
    super('LevelComplete');
  }

  init(data) {
    this.levelNumber = data.levelNumber;
    this.stars = data.stars;
    this.xpEarned = data.xpEarned;
    this.totalXP = data.totalXP;
    this.title = data.title;
  }

  create() {
    const { width, height } = this.scale;

    // ── Background ─────────────────────────────────
    this.add.image(width / 2, height / 2, 'sky');

    // ── Semi-transparent overlay ────────────────────
    this.add.rectangle(width / 2, height / 2, width, height, 0x000000, 0.4);

    // ── Header ─────────────────────────────────────
    const header = this.add.text(width / 2, 100, 'Level Complete!', {
      fontSize: '42px',
      fontFamily: 'Fredoka One',
      color: '#f1c40f',
      stroke: '#2c3e50',
      strokeThickness: 6
    }).setOrigin(0.5).setScale(0);

    // Pop-in animation for header
    this.tweens.add({
      targets: header,
      scale: 1,
      duration: 400,
      ease: 'Back.easeOut'
    });

    // ── Stars (animate in sequentially) ─────────────
    const starY = 220;
    const starSpacing = 80;
    const starStartX = width / 2 - starSpacing;

    for (let i = 0; i < 3; i++) {
      const isFilled = i < this.stars;
      const starKey = isFilled ? 'star-filled' : 'star-empty';

      const star = this.add.image(
        starStartX + i * starSpacing,
        starY,
        starKey
      ).setScale(0);

      // Staggered pop-in: 500ms, 800ms, 1100ms
      this.tweens.add({
        targets: star,
        scale: 2.5,
        duration: 400,
        delay: 500 + i * 300,
        ease: 'Back.easeOut'
      });
    }

    // ── XP Earned ──────────────────────────────────
    const xpText = this.add.text(width / 2, 320, `+${this.xpEarned} XP`, {
      fontSize: '28px',
      fontFamily: 'Fredoka One',
      color: '#27ae60'
    }).setOrigin(0.5).setAlpha(0);

    this.tweens.add({
      targets: xpText,
      alpha: 1,
      y: xpText.y - 10,
      duration: 400,
      delay: 1800
    });

    // ── Title Display ──────────────────────────────
    const titleText = this.add.text(width / 2, 370, `Rank: ${this.title}`, {
      fontSize: '22px',
      fontFamily: 'Fredoka One',
      color: '#f39c12'
    }).setOrigin(0.5).setAlpha(0);

    this.tweens.add({
      targets: titleText,
      alpha: 1,
      duration: 400,
      delay: 2100
    });

    // ── Buttons (appear after animations) ───────────
    const btnDelay = 2500;

    // Next Level button
    if (this.levelNumber < 10) {
      const nextBtn = this.add.text(width / 2, 460, 'Next Level >', {
        fontSize: '26px',
        fontFamily: 'Fredoka One',
        color: '#ffffff',
        backgroundColor: '#27ae60',
        padding: { x: 20, y: 10 }
      }).setOrigin(0.5).setAlpha(0).setInteractive({ useHandCursor: true });

      this.tweens.add({
        targets: nextBtn,
        alpha: 1,
        duration: 300,
        delay: btnDelay
      });

      nextBtn.on('pointerover', () => nextBtn.setScale(1.1));
      nextBtn.on('pointerout', () => nextBtn.setScale(1));
      nextBtn.on('pointerdown', () => {
        this.scene.start('Game', { levelNumber: this.levelNumber + 1 });
      });
    }

    // Level Select button
    const selectBtn = this.add.text(width / 2, 520, 'Level Select', {
      fontSize: '20px',
      fontFamily: 'Fredoka One',
      color: '#bdc3c7'
    }).setOrigin(0.5).setAlpha(0).setInteractive({ useHandCursor: true });

    this.tweens.add({
      targets: selectBtn,
      alpha: 1,
      duration: 300,
      delay: btnDelay + 200
    });

    selectBtn.on('pointerdown', () => {
      this.scene.start('LevelSelect');
    });
  }
}
```

**Animation timeline:**
```
0ms      - Scene starts
0-400ms  - "Level Complete!" pops in (scale 0 → 1)
500ms    - Star 1 pops in
800ms    - Star 2 pops in
1100ms   - Star 3 pops in
1800ms   - "+XP" fades in and slides up
2100ms   - Rank text fades in
2500ms   - "Next Level" button appears
2700ms   - "Level Select" button appears
```

This staggered reveal builds anticipation — especially for children who are excited to see how many stars they earned.

---

## Step 4.9 — Update GameConfig with All Scenes

### src/game/GameConfig.js

```js
import BootScene from './scenes/BootScene.js';
import PreloadScene from './scenes/PreloadScene.js';
import MenuScene from './scenes/MenuScene.js';
import LevelSelectScene from './scenes/LevelSelectScene.js';
import GameScene from './scenes/GameScene.js';
import LevelCompleteScene from './scenes/LevelCompleteScene.js';

// In config:
scene: [BootScene, PreloadScene, MenuScene, LevelSelectScene, GameScene, LevelCompleteScene]
```

The first scene in the array (BootScene) auto-starts. Each subsequent scene is started via `this.scene.start('SceneName')`.

---

## Step 4.10 — Update GameScene for Level Complete Flow

### Modifications to src/game/scenes/GameScene.js

Add the SaveManager import and update `completeLevel()`:

```js
import { SaveManager } from '../systems/SaveManager.js';

// In completeLevel():
completeLevel() {
  if (this.levelComplete) return;
  this.levelComplete = true;

  this.physics.pause();

  // Calculate stars
  let stars;
  if (this.wrongAttempts === 0) stars = 3;
  else if (this.wrongAttempts <= 2) stars = 2;
  else stars = 1;

  // Calculate XP
  const gapCount = this.levelData.gaps.length;
  const xpEarned = (gapCount * 10) + (stars * 5);

  // Save progress
  const saveData = SaveManager.completeLevel(this.levelNumber, stars, xpEarned);

  // Brief celebration delay, then transition
  this.time.delayedCall(500, () => {
    this.scene.start('LevelComplete', {
      levelNumber: this.levelNumber,
      stars: stars,
      xpEarned: xpEarned,
      totalXP: saveData.totalXP,
      title: saveData.title
    });
  });
}
```

---

## Data Flow Diagram

```
┌─────────────┐      levelNumber      ┌─────────────┐
│ LevelSelect  │ ──────────────────> │  GameScene   │
│              │                      │              │
│ reads:       │                      │ tracks:      │
│  SaveManager │                      │  wrongAttempts│
│  .load()     │                      │              │
└─────────────┘                      └──────┬───────┘
                                            │ completeLevel()
                                            │
                                            │ SaveManager.completeLevel(
                                            │   levelNumber, stars, xpEarned
                                            │ )
                                            │
                                            v
                                     ┌─────────────────┐
                                     │ LevelComplete    │
                                     │                  │
                                     │ displays:        │
                                     │  stars, xpEarned │
                                     │  totalXP, title  │
                                     │                  │
                                     │ buttons:         │
                                     │  Next Level ──────────> GameScene (N+1)
                                     │  Level Select ────────> LevelSelect
                                     └─────────────────┘

┌───────────────┐
│  SaveManager   │  (LocalStorage)
│                │
│  {             │
│    maxUnlocked │ <── updated on level complete
│    stars: {}   │ <── best stars per level
│    totalXP     │ <── cumulative, always increases
│    title       │ <── derived from totalXP via TitleSystem
│  }             │
└───────────────┘
```

---

## Files Created/Modified in This Phase

| File | Action | Purpose |
|------|--------|---------|
| `src/game/objects/GoalFlag.js` | Create | Goal flag sprite with floating tween |
| `src/game/systems/SaveManager.js` | Create | LocalStorage persistence |
| `src/game/systems/TitleSystem.js` | Create | XP → title mapping |
| `src/game/scenes/MenuScene.js` | Create | Title screen |
| `src/game/scenes/LevelSelectScene.js` | Create | Level grid with stars |
| `src/game/scenes/LevelCompleteScene.js` | Create | Star rating + XP display |
| `src/game/scenes/GameScene.js` | Modify | Use GoalFlag, SaveManager, proper scene transitions |
| `src/game/GameConfig.js` | Modify | Add all 6 scenes |

---

## Verification Checklist

- [ ] Game boots to MenuScene (not directly to GameScene)
- [ ] Menu shows "MathBuilder" title with floating animation
- [ ] Menu shows current rank ("Newbie" on first run) and "0 XP"
- [ ] Clicking Play goes to LevelSelectScene
- [ ] Level 1 is unlocked (blue), levels 2-10 are locked (grey)
- [ ] Clicking Level 1 starts GameScene with level 1
- [ ] Goal flag has a gentle floating animation
- [ ] Reaching the goal flag pauses the game and transitions to LevelCompleteScene
- [ ] "Level Complete!" header pops in with animation
- [ ] Stars animate in one by one (correct count based on wrong attempts)
- [ ] XP text shows the correct amount earned
- [ ] "Next Level" button starts level 2
- [ ] "Level Select" returns to the grid
- [ ] After completing level 1, level 2 is now unlocked in LevelSelectScene
- [ ] Stars are displayed on the Level 1 button in LevelSelectScene
- [ ] Refreshing the browser preserves all progress (open Application > LocalStorage in dev tools)
- [ ] Clearing LocalStorage resets to "Newbie" with only level 1 unlocked
- [ ] XP accumulates across multiple level completions
- [ ] Title updates when crossing XP thresholds (play several times to reach "Math Cadet" at 50 XP)
- [ ] Falling off-screen still restarts the level without affecting saved progress
