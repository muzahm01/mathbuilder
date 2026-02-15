# Preview Game

Build and preview the MathBuilder game locally.

## Instructions

1. Check if `node_modules/` exists. If not, run `npm install` first
2. Check if there are any TypeScript or build errors by running `npm run build`
3. If the build succeeds, start the dev server:

```bash
npm run dev
```

4. If the build fails, analyze the error output and fix issues:
   - Missing imports: check file paths and module exports
   - Phaser API errors: verify against Phaser 3.80+ API
   - Asset loading errors: verify files exist in `public/assets/`
   - Vite config issues: check `vite.config.js`

5. Report the dev server URL (should be http://localhost:8080) and any warnings

## Common Issues
- If port 8080 is in use, Vite will auto-increment to 8081
- Phaser requires `type: "module"` in package.json for ES module imports
- Assets in `public/` are served at root path (e.g., `public/assets/images/foo.png` -> `/assets/images/foo.png`)
- The math input overlay HTML must exist in `index.html` for MathInputUI to work
