# MathBuilder QA Audit & Remediation Plan

> Audit date: 2026-02-19
> Auditor: Claude (QA Agent)
> Scope: Full codebase — JavaScript (game), Python (scripts), HTML/CSS, config, levels, tests

---

## Executive Summary

The MathBuilder codebase is reasonably well-structured for a Phaser 3 game, with clean
module separation, good save-data sanitization, and graceful FX degradation. However, the
audit uncovered **32 issues** across 6 categories: functional bugs, documentation drift,
Python script quality, test coverage gaps, build/config issues, and accessibility/UX gaps.

| Severity | Count | Description |
|----------|-------|-------------|
| Critical | 4 | Bugs that break gameplay or cause runtime errors |
| High | 9 | Significant quality/reliability issues |
| Medium | 12 | Best-practice violations, maintainability concerns |
| Low | 7 | Minor polish, documentation, style issues |

---

## Category 1: Critical Functional Bugs

### C-01: CLAUDE.md level JSON schema is wrong — out of sync with actual code
- **File:** `CLAUDE.md` (lines showing Level JSON Format)
- **Problem:** CLAUDE.md documents level fields as `x`, `y`, `width`, `answer`, and
  `player: {x, y}` / `goal: {x, y}`. The actual level files and all game code use
  `gridX`, `gridY`, `correctAnswer`, `start: {gridX, gridY}`, `goal: {gridX, gridY}`.
  Any developer following the docs will create broken levels.
- **Impact:** New contributors produce invalid level files; confusion about data model.
- **Fix:** Update CLAUDE.md Level JSON Format section to match the real schema:
  ```json
  {
    "id": 1, "name": "Level Name",
    "world": "grasslands",
    "gridWidth": 25, "gridHeight": 9,
    "start": { "gridX": 1, "gridY": 7 },
    "goal": { "gridX": 23, "gridY": 7 },
    "platforms": [{ "gridX": 0, "gridY": 8, "width": 5, "tile": "grass-top" }],
    "gaps": [{ "id": "gap1", "gridX": 5, "gridY": 8, "width": 3, "correctAnswer": 3 }]
  }
  ```

### C-02: GameScene `shutdown()` is never called by Phaser
- **File:** `src/game/scenes/GameScene.js:247`
- **Problem:** The method is named `shutdown()` but Phaser's scene lifecycle calls
  the `Phaser.Events.Events` event `'shutdown'`. The scene needs to listen via
  `this.events.on('shutdown', this.cleanup, this)` or override the standard Phaser
  method. Currently the `shutdown()` method is **orphaned** — it never runs. This
  causes `MathInputUI` event listeners to accumulate on every level restart/transition,
  leaking DOM listeners.
- **Impact:** Memory leak; after many level restarts, dozens of stacked `keydown` and
  `click` handlers fire simultaneously, causing erratic math-input behavior.
- **Fix:** In `create()`, register:
  ```js
  this.events.on('shutdown', () => {
    if (this.mathUI) { this.mathUI.destroy(); this.mathUI = null; }
  });
  ```

### C-03: Level data field `gridHeight` not present in all level JSONs
- **File:** All level JSON files (`public/levels/world1/level*.json`)
- **Problem:** `GameScene.js:37-38` reads `levelData.gridHeight` to set world bounds.
  All 10 level files do include `gridHeight: 9`, so this works — but the
  `LevelLoader.js` returns raw JSON without any validation. If a level file is missing
  `gridHeight`, the world bounds become `NaN × NaN` and physics break silently.
- **Impact:** Silent failure on malformed levels; no error message to diagnose.
- **Fix:** Add runtime validation in `GameScene.create()` or enhance `LevelLoader` to
  validate essential fields before returning, using `LevelValidator.validateLevel()`.

### C-04: `levelsUnlocked` can exceed 10, allowing ghost level 11
- **File:** `src/game/systems/SaveManager.js:82-84`
- **Problem:** When completing level 10, `save.levelsUnlocked` becomes 11. The
  `loadSave()` validator allows up to 11 (line 29). The `LevelSelectScene` loop runs
  `i < 10` so no visual bug occurs — but the save data is semantically wrong (there
  is no level 11). A stricter validator should cap at 10.
- **Impact:** Save data inconsistency; potential future bug if level count changes.
- **Fix:** Cap `levelsUnlocked` to max level count:
  ```js
  save.levelsUnlocked = Math.min(levelNumber + 1, 10);
  ```

---

## Category 2: High Severity Issues

### H-01: XP awards are cumulative — replaying gives infinite XP
- **File:** `src/game/systems/SaveManager.js:87`
- **Problem:** `save.xp += stars * 10` adds XP on every level completion, even on
  replays. A child replaying level 1 with 3 stars earns 30 XP per run, infinitely.
  This defeats the title progression system.
- **Impact:** Title progression is meaningless; "Legend" rank reachable in minutes.
- **Fix:** Only award XP for improvement:
  ```js
  const previousStars = save.levelStars[levelKey] || 0;
  if (stars > previousStars) {
    save.xp += (stars - previousStars) * 10;
  }
  ```

### H-02: No `@vitest/coverage-v8` dependency — `test:coverage` script fails
- **File:** `package.json`
- **Problem:** `npm run test:coverage` fails with "MISSING DEPENDENCY" because
  `@vitest/coverage-v8` is not in devDependencies, yet `vite.config.js` references
  `provider: 'v8'`.
- **Impact:** Coverage reporting is broken; CI would fail on coverage step.
- **Fix:** `npm install --save-dev @vitest/coverage-v8`

### H-03: Build produces 1.5 MB single chunk — no code splitting
- **File:** `vite.config.js`
- **Problem:** Vite warns: "Some chunks are larger than 500 kB after minification."
  The entire Phaser library (1.5 MB gzipped to 347 KB) ships in one chunk.
- **Impact:** Slow initial load, especially on mobile/tablet (target audience).
- **Fix:** Add `build.rollupOptions.output.manualChunks` to separate Phaser into its
  own chunk so it can be cached independently:
  ```js
  build: {
    rollupOptions: {
      output: {
        manualChunks: { phaser: ['phaser'] }
      }
    }
  }
  ```

### H-04: No error handling for missing audio files
- **File:** `src/game/scenes/GameScene.js` (lines 160, 202, 220)
- **Problem:** `this.sound.play('sfx-wrong')` etc. will throw if audio fails to load
  in PreloadScene (network error, format unsupported). Phaser's `sound.play()` throws
  when the key doesn't exist.
- **Impact:** Uncaught runtime error crashes the game on audio failure.
- **Fix:** Wrap sound calls in a safe helper, or check `this.sound.get(key)` before
  playing. Alternatively, add a load error handler in PreloadScene.

### H-05: MathInputUI — no guard against double-submission race condition
- **File:** `src/game/systems/MathInputUI.js:74-112`
- **Problem:** After a correct answer, there's a 600ms `setTimeout` before `hide()`.
  During this window, the user can press Enter again, triggering `handleSubmit()` a
  second time. `this.currentGap` is still set, so the callback fires twice. This can
  double-count wrong attempts or cause bridge-building to trigger twice.
- **Impact:** Double bridge build, double XP, or double wrong-attempt counting.
- **Fix:** Set `this.currentGap = null` immediately after correct answer:
  ```js
  if (answer === correct) {
    const gap = this.currentGap;
    this.currentGap = null;  // prevent re-submission
    this.feedback.textContent = 'Correct!';
    ...
    this.onResult(gap, true);
  }
  ```

### H-06: `index.html` uses absolute `/src/main.js` — breaks with `base: './'`
- **File:** `index.html:36`
- **Problem:** `<script type="module" src="/src/main.js">` uses an absolute path
  starting with `/`. The Vite config sets `base: './'` for relative asset paths
  (needed for Vercel subdirectory deploys). Vite rewrites this during build, so
  production works, but the inconsistency could cause issues in non-root deployments
  during development.
- **Impact:** May break if served from a subdirectory during dev.
- **Fix:** Change to `src="./src/main.js"` for consistency.

### H-07: Python fix scripts use hardcoded absolute paths
- **Files:** `scripts/fix_sprites_and_bg.py:9-10`, `scripts/fix_remaining.py:13-14`,
  `scripts/fix_final.py:11-12`
- **Problem:** These scripts hardcode `/home/user/mathbuilder/resources` and
  `/home/user/mathbuilder/public/assets/images`. They won't work on any other machine
  or if the repo is cloned to a different path.
- **Impact:** Scripts are non-portable; fail on any other developer's machine.
- **Fix:** Use `__file__`-relative paths like `process_images.py` does:
  ```python
  SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
  PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
  RESOURCES = os.path.join(PROJECT_ROOT, "resources")
  OUTPUT = os.path.join(PROJECT_ROOT, "public", "assets", "images")
  ```

### H-08: No `requirements.txt` or Python dependency specification
- **Files:** N/A (missing file)
- **Problem:** Python scripts require `Pillow` but there's no `requirements.txt`,
  `pyproject.toml`, or any specification of the Python dependency.
- **Impact:** New developers get `ModuleNotFoundError: No module named 'PIL'` with no
  guidance on how to fix it.
- **Fix:** Create `scripts/requirements.txt`:
  ```
  Pillow>=9.0.0
  ```

### H-09: BootScene font loading relies on arbitrary 500ms delay
- **File:** `src/game/scenes/BootScene.js:23`
- **Problem:** The 500ms `delayedCall` is a heuristic to wait for Fredoka One to
  load. On slow connections (mobile/tablet), 500ms may not be enough. The font will
  render as fallback, then pop in later.
- **Impact:** FOUT (flash of unstyled text) on slow connections.
- **Fix:** Use `document.fonts.ready` promise or the CSS Font Loading API:
  ```js
  document.fonts.ready.then(() => this.scene.start('Preload'));
  ```

---

## Category 3: Medium Severity Issues

### M-01: Massive code duplication across Python fix scripts
- **Files:** `scripts/fix_sprites_and_bg.py`, `scripts/fix_remaining.py`,
  `scripts/fix_final.py`
- **Problem:** All three fix scripts reimplement the same sprite-finding, background-
  removal, and sheet-stitching logic with slight variations. There are 3 different
  `find_sprite_*` functions, 3 different `remove_*_bg` functions, and 3 different
  `extract_*_stitch` functions.
- **Impact:** Maintenance nightmare; bug fixes must be applied in 3+ places.
- **Fix:** Consolidate into a single `image_utils.py` module with the best
  implementation of each function. Have fix scripts import from it. Ideally, fold all
  functionality into `process_images.py` with CLI flags for different modes.

### M-02: Python scripts lack `if __name__ == '__main__'` guard usage consistency
- **Files:** All Python scripts
- **Problem:** While all scripts do have the guard, the fix scripts define all logic
  at module level (hardcoded paths as globals). Functions should receive paths as
  parameters for testability.
- **Impact:** Cannot unit-test individual functions; cannot import modules without
  side effects from global path variables.
- **Fix:** Move path resolution inside `main()` or accept as function parameters.

### M-03: No Python linting or formatting configuration
- **Files:** N/A (missing)
- **Problem:** No `ruff.toml`, `pyproject.toml` [tool.ruff], `.flake8`, or `black`
  configuration. Python code style is inconsistent (some functions have docstrings,
  some don't; mixed single/double quotes).
- **Impact:** Code style drift; no automated quality checks for Python code.
- **Fix:** Add `pyproject.toml` with ruff config:
  ```toml
  [tool.ruff]
  line-length = 100
  select = ["E", "F", "W", "I"]
  ```

### M-04: `random.seed(42)` in `create_grass_tile()` affects global RNG state
- **File:** `scripts/process_images.py:735`
- **Problem:** `random.seed(42)` sets the global random state. If any code after this
  call relies on randomness, it gets deterministic results unexpectedly.
- **Impact:** Subtle reproducibility bugs if script is extended.
- **Fix:** Use a local `random.Random(42)` instance instead.

### M-05: No test coverage for LevelLoader (async fetch logic)
- **File:** `src/game/systems/LevelLoader.js`
- **Problem:** Zero test coverage. The URL construction, range validation, and fetch
  error handling are untested.
- **Impact:** Regressions in level loading go undetected.
- **Fix:** Add `tests/LevelLoader.test.js` with mocked `fetch`:
  - Valid level numbers (1-10) produce correct URLs
  - Invalid numbers (0, 11, -1, NaN) throw
  - HTTP errors (404, 500) throw with descriptive messages

### M-06: No test coverage for MathInputUI (answer validation logic)
- **File:** `src/game/systems/MathInputUI.js`
- **Problem:** The core answer-checking logic (correct, too-small, too-big, out-of-
  range, NaN) is untested. DOM dependency makes testing harder.
- **Impact:** Math validation regressions could ship undetected.
- **Fix:** Extract pure validation logic into a testable function:
  ```js
  export function checkAnswer(input, correctAnswer) { ... }
  ```
  Test that function separately from DOM interactions.

### M-07: `GameScene.create()` is async but Phaser doesn't await it
- **File:** `src/game/scenes/GameScene.js:25`
- **Problem:** `async create()` — Phaser calls `create()` synchronously and does not
  await the returned promise. If `loadLevel()` takes time, the `update()` loop starts
  before platforms/player exist, causing `this.player` to be undefined.
- **Impact:** Potential race condition between `create()` completing and `update()` running.
- **Fix:** The `if (!this.player) return` guard in `update()` (line 172) mitigates this,
  but a cleaner approach is to use Phaser's `preload()` to fetch level data, or set a
  `this.ready` flag and check it in `update()`.

### M-08: ESLint warning — FXManager imported but unused in GameScene
- **File:** `src/game/scenes/GameScene.js:12`
- **Problem:** `import { FXManager } from '../systems/FXManager.js'` is imported but
  never used in GameScene.
- **Impact:** Dead import; lint warning.
- **Fix:** Remove the unused import.

### M-09: ESLint warning — `console.error` in GameScene
- **File:** `src/game/scenes/GameScene.js:31`
- **Problem:** `console.error(err)` triggers the `no-console` lint rule.
- **Impact:** Lint warning.
- **Fix:** Either disable the rule for that line with `// eslint-disable-next-line` or
  replace with a user-visible error display.

### M-10: `generate_audio.py` has no type hints or docstrings on helper functions
- **File:** `scripts/generate_audio.py`
- **Problem:** Functions like `write_wav()` take parameters without type annotations.
  The WAV writing logic is non-trivial and lacks inline documentation.
- **Impact:** Reduced maintainability; harder for contributors to modify sound design.
- **Fix:** Add type hints and brief docstrings:
  ```python
  def write_wav(filename: str, samples: list[float], sample_rate: int = SAMPLE_RATE) -> None:
  ```

### M-11: `process_images.py` — `ImageChops` imported but never used
- **File:** `scripts/process_images.py:1` (imports)
- **Problem:** `from PIL import ... ImageChops` is imported but never referenced.
- **Impact:** Dead import.
- **Fix:** Remove `ImageChops` from the import line.

### M-12: No `.env.example` or environment documentation
- **Files:** N/A (missing)
- **Problem:** While the project has no env vars currently, the Vercel deployment may
  need configuration. There's no documentation on deployment setup.
- **Impact:** Deployment friction for new contributors.
- **Fix:** Add deployment instructions to README or a `DEPLOYMENT.md` file.

---

## Category 4: Low Severity Issues

### L-01: `.gitignore` missing common entries
- **File:** `.gitignore`
- **Problem:** Missing entries for `.env`, `.env.local`, `*.pyc`, `__pycache__/`,
  `.vscode/`, `.idea/`, `*.swp`, `*.swo`.
- **Fix:** Add common IDE and Python cache patterns.

### L-02: Level files have extra fields not referenced by code
- **Files:** All `public/levels/world1/level*.json`
- **Problem:** Levels include `"id"` and `"world"` fields that are never read by the
  game code. Not harmful, but creates confusion about what's required.
- **Fix:** Either use these fields in the game (e.g., show world name) or document
  them as optional metadata.

### L-03: CSS `@keyframes shake` is defined but only applied via JS
- **File:** `style.css:151`
- **Problem:** The `shake` animation is applied via `MathInputUI.shakePanel()`. This
  works, but the animation isn't reset properly — the `animation = 'none'` / reflow
  trick may fail in some browsers.
- **Impact:** Minor: shake may not replay on consecutive wrong answers in edge cases.
- **Fix:** Use `element.classList.add/remove` with an animation class instead.

### L-04: `vercel.json` CSP missing `media-src` for audio
- **File:** `vercel.json:14`
- **Problem:** The Content-Security-Policy header doesn't include `media-src 'self'`.
  Audio files (`.wav`) are loaded via Phaser which may use `<audio>` elements.
- **Impact:** Audio may be blocked by CSP in production.
- **Fix:** Add `media-src 'self'` to the CSP header value.

### L-05: `btn-levels` asset is loaded but never used
- **File:** `src/game/scenes/PreloadScene.js:63`
- **Problem:** `btn-levels` image is loaded in PreloadScene but never referenced by
  any scene. `LevelSelectScene` builds buttons with rectangles and text, not images.
- **Impact:** Wasted bandwidth loading an unused asset.
- **Fix:** Remove the `btn-levels` load call, or use it in LevelSelectScene.

### L-06: `math-input-bg` asset is loaded but never used
- **File:** `src/game/scenes/PreloadScene.js` — no load call for `math-input-bg`,
  but the asset exists in `public/assets/images/ui/`.
- **Problem:** The math input panel uses CSS styling, not the generated PNG background.
  The asset was generated by `process_images.py` but is unused.
- **Impact:** Wasted disk space (minor).
- **Fix:** Either integrate the PNG as panel background or stop generating it.

### L-07: `stone` tile is loaded but never used in any level
- **File:** `src/game/scenes/PreloadScene.js:40`
- **Problem:** The `stone` tile texture is loaded but no level file uses
  `"tile": "stone"`. All levels use `grass-top` only.
- **Impact:** Wasted bandwidth.
- **Fix:** Either use stone tiles in later levels or defer loading until needed.

---

## Category 5: Test Coverage Gaps

### T-01: Overall test coverage is ~25% (4 of 16 modules tested)

**Currently tested:**
- GridSystem.js — comprehensive
- SaveManager.js — comprehensive
- TitleSystem.js — comprehensive
- LevelValidator.js — comprehensive

**Untested modules (priority order):**

| Priority | Module | Why It Matters |
|----------|--------|----------------|
| P0 | LevelLoader.js | Core async logic; URL construction, error handling |
| P0 | MathInputUI.js | Core gameplay; answer validation, feedback logic |
| P1 | Bridge.js | Gameplay; block placement math |
| P1 | Player.js | Gameplay; movement physics integration |
| P2 | FXManager.js | Graceful degradation; null safety |
| P2 | ParticleManager.js | Cleanup timing |
| P3 | TouchControls.js | Input state management |
| P3 | FullscreenButton.js | Event listener cleanup |

### T-02: Missing integration tests for level data
- **Problem:** No test validates that all 10 level JSON files pass
  `LevelValidator.validateLevel()`.
- **Fix:** Add a test that reads each level file and runs it through validation.

### T-03: No coverage thresholds configured
- **File:** `vite.config.js`
- **Problem:** No minimum coverage thresholds. Tests can pass with 0% coverage.
- **Fix:** Add to vite.config.js test section:
  ```js
  coverage: {
    thresholds: { statements: 60, branches: 50, functions: 60, lines: 60 }
  }
  ```

---

## Category 6: Accessibility & UX Gaps

### A-01: No ARIA labels on math input overlay
- **File:** `index.html`
- **Problem:** The math input overlay lacks `role="dialog"`, `aria-modal="true"`,
  and `aria-label` attributes. Screen readers won't announce it as a dialog.
- **Fix:** Add ARIA attributes to `#math-input-overlay` and `#math-input-panel`.

### A-02: No keyboard shortcut to dismiss math input
- **File:** `src/game/systems/MathInputUI.js`
- **Problem:** There's no way to close the math panel with Escape key. Children
  (or parents helping) may expect Escape to dismiss.
- **Fix:** Add Escape key handler in `MathInputUI`.

### A-03: No focus trap in math input overlay
- **File:** `src/game/systems/MathInputUI.js`
- **Problem:** When the math overlay is open, Tab can focus elements behind it.
- **Fix:** Implement focus trapping within the overlay when visible.

---

## Remediation Priority & Effort Estimate

### Sprint 1: Critical Fixes (must-fix before release)
| ID | Issue | Effort |
|----|-------|--------|
| C-01 | Fix CLAUDE.md level JSON docs | Small |
| C-02 | Fix GameScene shutdown listener leak | Small |
| C-03 | Add level validation in LevelLoader | Small |
| C-04 | Cap levelsUnlocked at 10 | Small |
| H-05 | Fix MathInputUI double-submission | Small |
| H-06 | Fix index.html script path | Small |
| H-09 | Fix font loading race condition | Small |

### Sprint 2: High Priority (reliability & build)
| ID | Issue | Effort |
|----|-------|--------|
| H-01 | Fix XP replay exploit | Small |
| H-02 | Add @vitest/coverage-v8 dep | Small |
| H-03 | Add code splitting for Phaser | Small |
| H-04 | Add safe audio playback | Medium |
| H-07 | Fix Python hardcoded paths | Small |
| H-08 | Add requirements.txt | Small |
| M-08 | Remove unused FXManager import | Small |
| M-09 | Fix console.error lint warning | Small |
| L-04 | Fix CSP media-src | Small |

### Sprint 3: Test Coverage
| ID | Issue | Effort |
|----|-------|--------|
| T-01 | Add LevelLoader tests | Medium |
| T-01 | Add MathInputUI tests | Medium |
| T-02 | Add level file integration tests | Small |
| T-03 | Configure coverage thresholds | Small |
| M-05 | Extract testable validation from MathInputUI | Medium |
| M-06 | Test remaining modules | Large |

### Sprint 4: Python Quality & Maintenance
| ID | Issue | Effort |
|----|-------|--------|
| M-01 | Consolidate Python scripts | Large |
| M-02 | Fix Python module-level side effects | Medium |
| M-03 | Add ruff/linting config | Small |
| M-04 | Fix global random seed | Small |
| M-10 | Add type hints to generate_audio.py | Small |
| M-11 | Remove unused ImageChops import | Small |

### Sprint 5: Polish & Accessibility
| ID | Issue | Effort |
|----|-------|--------|
| A-01 | Add ARIA labels to math overlay | Small |
| A-02 | Add Escape key dismiss | Small |
| A-03 | Add focus trap | Medium |
| L-01 | Improve .gitignore | Small |
| L-03 | Improve shake animation reset | Small |
| L-05 | Remove unused btn-levels asset load | Small |
| L-07 | Remove/use stone tile | Small |

---

## Automated Checks to Add

1. **Pre-commit hook:** `npm run lint && npm run test`
2. **CI pipeline:** lint -> test -> coverage threshold -> build
3. **Python CI:** `ruff check scripts/` and `python -m py_compile scripts/*.py`
4. **Level validation:** Automated test that validates all JSON level files on every commit
