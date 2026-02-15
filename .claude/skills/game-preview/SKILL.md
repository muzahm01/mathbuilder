---
name: game-preview
description: Build and preview the MathBuilder game locally with Vite. Use when the user wants to run the dev server, test the build, check for errors, or preview the game in a browser. Also use when troubleshooting build failures or Phaser loading issues.
---

# Game Preview

Build and run the MathBuilder game locally using Vite.

## When to Use

- User asks to "run the game", "start dev server", "preview", or "test the build"
- User encounters build errors or Phaser loading issues
- After implementing changes that need visual verification

## Quick Start

```bash
cd /home/user/mathbuilder

# Install dependencies (if node_modules/ doesn't exist)
npm install

# Start dev server with hot reload
npm run dev
```

Dev server runs at **http://localhost:8080** (configured in `vite.config.js`).

## Commands

| Command | Purpose |
|---------|---------|
| `npm install` | Install Phaser 3 + Vite dependencies |
| `npm run dev` | Start Vite dev server on port 8080 with HMR |
| `npm run build` | Production build to `dist/` |
| `npm run preview` | Preview production build locally |

## Build Verification

Run a full build check:

```bash
cd /home/user/mathbuilder && npm run build 2>&1
```

If the build succeeds, `dist/` will contain the production-ready static files.

## Common Issues

### Port 8080 in use
Vite auto-increments to 8081, 8082, etc. Check terminal output for the actual URL.

### Module import errors
- Ensure `"type": "module"` exists in `package.json`
- All imports must use `.js` extension: `import Foo from './Foo.js'`
- Phaser imports: `import Phaser from 'phaser'`

### Asset loading failures
- Assets in `public/` are served at root: `public/assets/images/foo.png` → `/assets/images/foo.png`
- In Phaser preload: `this.load.image('key', 'assets/images/tiles/grass-top.png')`
- No leading slash needed for Phaser asset paths when `base: './'` is set

### Phaser canvas not appearing
- Check that `<div id="game-container"></div>` exists in `index.html`
- GameConfig must have `parent: 'game-container'`
- Check browser console for WebGL/Canvas errors

### Math input overlay not working
- The HTML overlay `#math-input-overlay` must exist in `index.html`
- It's hidden by default (`display: none`), shown by MathInputUI.js
- Check that `style.css` is linked in `index.html`

### Font not loading
- Fredoka One loads from Google Fonts CDN
- Check the `<link>` tag in `index.html` head
- Font may flash on first load — this is normal

## Project Dependencies

```json
{
  "dependencies": {
    "phaser": "^3.80.0"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}
```

## Vercel Deployment

For production deployment:

```bash
# Build first
npm run build

# Deploy (requires Vercel CLI)
npx vercel --prod
```

Or push to GitHub — Vercel auto-deploys from the connected repo. Config is in `vercel.json`:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist"
}
```
