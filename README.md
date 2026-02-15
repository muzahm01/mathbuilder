# MathBuilder

A web-based 2D platformer where math builds the world. Designed for children aged 5-8.

A robot character named **Botty** runs through platformer levels with gaps in the ground. Players count the gap width in tile units and type the correct answer to build a bridge and keep moving.

## Screenshots

**Art Style:** "Soft Plastic Voxel" — Minecraft meets Mario made of smooth vinyl toys.

## Tech Stack

- **Engine:** [Phaser 3.80+](https://phaser.io/) with Arcade Physics
- **Build Tool:** [Vite 5](https://vitejs.dev/)
- **Language:** JavaScript (ES6 modules)
- **Hosting:** [Vercel](https://vercel.com/) (static site)
- **Persistence:** LocalStorage (no backend, no accounts)

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) 18+
- npm

### Install & Run

```bash
# Install dependencies
npm install

# Start dev server at http://localhost:8080
npm run dev
```

### Other Commands

```bash
npm run build        # Production build to dist/
npm run preview      # Preview production build locally
npm test             # Run tests
npm run test:watch   # Run tests in watch mode
npm run test:coverage # Run tests with coverage
npm run lint         # Lint with ESLint
npm run validate     # Lint + test + build
```

## How to Play

1. Use **arrow keys** (or on-screen touch controls) to move Botty left and right
2. Press **Up** to jump
3. When Botty reaches a gap, a math prompt appears
4. **Count the gap width** and type the number
5. Get it right and a bridge is built — cross and keep going!
6. Reach the **goal flag** to complete the level

### Star Rating

- 0 wrong answers = 3 stars
- 1-2 wrong answers = 2 stars
- 3+ wrong answers = 1 star (always positive reinforcement — never 0)

### Progression

Earn XP by completing levels and collecting stars. Your title progresses through:

**Newbie** > Math Cadet > Number Ninja > Bridge Builder > Team Leader > Math Hero > Grand Master > **Legend**

## Project Structure

```
mathbuilder/
├── src/
│   ├── main.js                  # Phaser bootstrap
│   └── game/
│       ├── GameConfig.js        # 800x600, Arcade physics, Scale.FIT
│       ├── scenes/
│       │   ├── BootScene.js     # Font loading, splash
│       │   ├── PreloadScene.js  # Asset loading with progress bar
│       │   ├── MenuScene.js     # Main menu
│       │   ├── LevelSelectScene.js
│       │   ├── GameScene.js     # Core gameplay
│       │   └── LevelCompleteScene.js
│       ├── objects/
│       │   ├── Player.js        # Physics sprite with movement
│       │   ├── Bridge.js        # Animated bridge building
│       │   └── GoalFlag.js      # Level end flag
│       └── systems/
│           ├── GridSystem.js    # Tile/pixel coordinate conversion
│           ├── LevelLoader.js   # JSON level loader
│           ├── MathInputUI.js   # HTML overlay for math prompts
│           ├── SaveManager.js   # LocalStorage persistence
│           ├── TitleSystem.js   # XP and rank progression
│           ├── TouchControls.js # On-screen mobile controls
│           └── ParticleManager.js
├── public/
│   ├── assets/
│   │   ├── images/              # Tiles, sprites, backgrounds, UI
│   │   └── audio/               # Sound effects
│   └── levels/
│       └── world1/              # 10 level JSON files
├── tests/                       # Vitest unit tests
├── scripts/                     # Python image processing pipeline
└── docs/plans/                  # Phase-by-phase design docs
```

## Game Architecture

### Scene Flow

```
BootScene → PreloadScene → MenuScene → LevelSelectScene → GameScene → LevelCompleteScene
                                                              ↓
                                                        (fall = restart)
```

### Key Constants

| Setting | Value |
|---------|-------|
| Canvas | 800 x 600 px (4:3) |
| Tile size | 64 x 64 px |
| Gravity | 800 px/s² |
| Scale mode | `Phaser.Scale.FIT` |

### Level Format

Levels are JSON files with tile-coordinate positions:

```json
{
  "name": "First Steps",
  "width": 15,
  "platforms": [
    { "x": 0, "y": 8, "width": 5, "tile": "grass-top" }
  ],
  "gaps": [
    { "x": 5, "y": 8, "width": 3, "answer": 3 }
  ],
  "player": { "x": 1, "y": 7 },
  "goal": { "x": 14, "y": 7 }
}
```

## Image Processing

Raw source images (in `resources/`) are processed into game-ready assets using Python scripts:

```bash
pip install Pillow
python3 scripts/process_images.py
```

## Deployment

The project is configured for Vercel. Build output goes to `dist/`.

```bash
npm run build
```

## License

All rights reserved.
