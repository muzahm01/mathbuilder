# Phase 1: The Foundation

## Goal
Get a blank Phaser 3 game running locally with Vite, deployable to Vercel. By the end of this phase, you should see a sky-blue 800x600 canvas with "MathBuilder" text that scales responsively on any screen.

---

## Step 1.1 — Initialize the Project

### package.json

Create the project manifest with Vite as the build tool and Phaser 3 as the game engine:

```json
{
  "name": "mathbuilder",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "phaser": "^3.80.0"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}
```

**Why these versions:**
- Phaser 3.80+ includes the new particle emitter API we'll use in Phase 6
- Vite 5 provides fast HMR and clean ESM support

**Action:** Run `npm install` to generate `node_modules/` and `package-lock.json`.

---

## Step 1.2 — Vite Configuration

### vite.config.js

```js
import { defineConfig } from 'vite';

export default defineConfig({
  base: './',
  build: {
    outDir: 'dist',
    assetsInlineLimit: 0
  },
  server: {
    port: 8080
  }
});
```

**Key settings explained:**
- `base: './'` — Uses relative paths in the production build so assets load correctly on Vercel regardless of the deployment URL path
- `assetsInlineLimit: 0` — Prevents Vite from inlining small images as base64 data URIs; we want all assets as separate files for Phaser's loader
- `port: 8080` — Consistent dev server port

---

## Step 1.3 — HTML Entry Point

### index.html

This is the single HTML file that Vite serves. It contains:

1. **The Phaser game container** — a div where Phaser mounts its canvas
2. **The math input overlay** — an HTML form that floats over the game canvas (hidden by default, shown when the player encounters a gap)
3. **Google Font** — "Fredoka One" for kid-friendly text
4. **Responsive viewport meta tag** — ensures proper scaling on mobile

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>MathBuilder</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <div id="game-wrapper">
    <div id="game-container"></div>

    <!-- Math Input Overlay (hidden by default) -->
    <div id="math-input-overlay" style="display: none;">
      <div id="math-input-panel">
        <p id="math-question">How wide is the gap?</p>
        <input
          id="math-answer-input"
          type="number"
          min="1"
          max="20"
          placeholder="?"
          inputmode="numeric"
        />
        <button id="math-submit-btn">Build!</button>
        <p id="math-feedback"></p>
      </div>
    </div>
  </div>

  <script type="module" src="/src/main.js"></script>
</body>
</html>
```

**Why HTML overlay instead of Phaser DOM?**
- The `<input type="number">` with `inputmode="numeric"` triggers the numeric keyboard on tablets and phones — critical for the target audience (7-year-olds on iPads)
- Standard CSS styling is simpler and more consistent than Phaser's DOM element API
- Focus/blur handling works natively without Phaser workarounds

---

## Step 1.4 — Styles

### style.css

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: #1a1a2e;
  overflow: hidden;
  font-family: 'Fredoka One', cursive;
}

#game-wrapper {
  position: relative;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

#game-container canvas {
  display: block;
}

/* ── Math Input Overlay ────────────────────────────── */

#math-input-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5);
  z-index: 10;
}

#math-input-panel {
  background: #e8f0fe;
  border: 4px solid #4a90d9;
  border-radius: 20px;
  padding: 30px 40px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  max-width: 350px;
  width: 90%;
}

#math-question {
  font-size: 1.4rem;
  color: #2c3e50;
  margin-bottom: 16px;
}

#math-answer-input {
  font-family: 'Fredoka One', cursive;
  font-size: 2.5rem;
  text-align: center;
  width: 120px;
  padding: 10px;
  border: 3px solid #4a90d9;
  border-radius: 12px;
  outline: none;
  background: white;
  color: #2c3e50;
  -moz-appearance: textfield;  /* Hide spin buttons on Firefox */
}

#math-answer-input::-webkit-outer-spin-button,
#math-answer-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

#math-submit-btn {
  font-family: 'Fredoka One', cursive;
  font-size: 1.3rem;
  display: block;
  margin: 16px auto 0;
  padding: 10px 40px;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  box-shadow: 0 4px 0 #1e8449;
  transition: transform 0.1s, box-shadow 0.1s;
}

#math-submit-btn:active {
  transform: translateY(2px);
  box-shadow: 0 2px 0 #1e8449;
}

#math-feedback {
  font-size: 1.2rem;
  margin-top: 12px;
  min-height: 1.5em;
  font-weight: bold;
}
```

**Design notes:**
- The dark overlay (`rgba(0,0,0,0.5)`) dims the game behind the input panel, focusing attention on the math question
- The input hides number spinner buttons for a cleaner look
- The "Build!" button has a `box-shadow` based pressed effect (translateY on :active) that feels tactile
- All fonts use Fredoka One for consistency with the kid-friendly theme

---

## Step 1.5 — Phaser Game Configuration

### src/game/GameConfig.js

```js
import Phaser from 'phaser';
import BootScene from './scenes/BootScene.js';

export const GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: 'game-container',
  backgroundColor: '#87CEEB',
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 800 },
      debug: false
    }
  },
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  scene: [BootScene]
};
```

**Configuration explained:**

| Setting | Value | Why |
|---------|-------|-----|
| `type: Phaser.AUTO` | WebGL with Canvas fallback | Maximum device compatibility |
| `width/height: 800x600` | 4:3 aspect ratio | Fits tablets well, plenty of room for platforming |
| `parent: 'game-container'` | Mounts canvas into our div | Keeps it within the wrapper for overlay positioning |
| `backgroundColor: '#87CEEB'` | Sky blue | Matches the grasslands theme before backgrounds load |
| `gravity.y: 800` | Moderate gravity | Feels responsive for a kids' platformer (not too floaty, not too fast) |
| `debug: false` | No physics debug | Toggle to `true` during development to see hitboxes |
| `Scale.FIT` | Scales canvas to fit viewport | Maintains 800x600 ratio, letterboxes if needed |
| `CENTER_BOTH` | Centers canvas in viewport | Looks correct on all screen sizes |

---

## Step 1.6 — Bootstrap

### src/main.js

```js
import Phaser from 'phaser';
import { GameConfig } from './game/GameConfig.js';

const game = new Phaser.Game(GameConfig);
```

This is intentionally minimal — just imports the config and starts Phaser. All game logic lives in scenes.

---

## Step 1.7 — Boot Scene (Stub)

### src/game/scenes/BootScene.js

```js
import Phaser from 'phaser';

export default class BootScene extends Phaser.Scene {
  constructor() {
    super('Boot');
  }

  create() {
    this.add.text(
      this.scale.width / 2,
      this.scale.height / 2,
      'MathBuilder',
      {
        fontSize: '48px',
        fontFamily: 'Fredoka One',
        color: '#ffffff',
        stroke: '#2c3e50',
        strokeThickness: 6
      }
    ).setOrigin(0.5);
  }
}
```

This is a temporary scene to confirm the game boots. It will be expanded in Phase 3 to load assets and transition to PreloadScene.

---

## Step 1.8 — Vercel Configuration

### vercel.json

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist"
}
```

Vercel auto-detects Vite projects, but this explicit config ensures the correct build command and output directory are used.

---

## Step 1.9 — Git Ignore

### .gitignore

```
node_modules/
dist/
.DS_Store
*.log
```

---

## Step 1.10 — Create Directory Structure

Create all empty directories that will be populated in later phases:

```
public/assets/images/tiles/
public/assets/images/player/
public/assets/images/backgrounds/
public/assets/images/ui/
public/assets/images/objects/
public/assets/images/particles/
public/assets/audio/
public/levels/world1/
src/game/scenes/
src/game/objects/
src/game/systems/
docs/plans/
```

**Note:** Level files live under `public/levels/` so Vite serves them as static files accessible via `fetch()` at runtime.

---

## Files Created in This Phase

| File | Purpose |
|------|---------|
| `package.json` | Project dependencies and scripts |
| `vite.config.js` | Build tool configuration |
| `index.html` | HTML entry with game container + math overlay |
| `style.css` | Styling for overlay and page layout |
| `src/main.js` | Phaser bootstrap |
| `src/game/GameConfig.js` | Game engine configuration |
| `src/game/scenes/BootScene.js` | Stub scene to confirm boot |
| `vercel.json` | Deployment configuration |
| `.gitignore` | Git exclusions |

---

## Verification Checklist

- [ ] `npm install` completes without errors
- [ ] `npm run dev` starts Vite dev server on `http://localhost:8080`
- [ ] Browser shows a sky-blue 800x600 canvas with "MathBuilder" text centered
- [ ] Resizing the browser window causes the canvas to scale proportionally (no stretching)
- [ ] The math input overlay div exists in the DOM (inspect with dev tools) but is hidden
- [ ] `npm run build` produces a `dist/` folder with `index.html` and bundled JS
- [ ] `npx vite preview` serves the production build correctly
- [ ] No console errors in the browser dev tools
- [ ] Pushing to GitHub and connecting to Vercel deploys the live site
