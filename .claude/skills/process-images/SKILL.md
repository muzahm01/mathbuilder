---
name: process-images
description: Process raw Gemini-generated images into game-ready assets. Use when the user mentions image processing, asset pipeline, sprite sheets, background removal, processing resources, or regenerating game art from source images in the resources/ directory.
---

# Process Images

Process raw AI-generated images from `resources/` into game-ready assets in `public/assets/images/` with correct dimensions, transparency, and sprite sheet formatting.

## When to Use

- User adds new source images to `resources/`
- User wants to reprocess or fix existing game assets
- User mentions "process images", "sprite sheets", "background removal", or "asset pipeline"
- User regenerates art with Gemini and needs to convert it

## Quick Start

Run the main processing pipeline:

```bash
cd /home/user/mathbuilder && python3 scripts/process_images.py
```

## Processing Pipeline

The pipeline handles these transformations:

### 1. Tiles (64x64)
- Crops rounded edges from AI output (8% margin)
- Resizes to exact 64x64
- `grass-top.png` is generated programmatically (original was isometric 3D)

### 2. Player Sprites (horizontal sheets)
- Removes white/near-white backgrounds (threshold: 240)
- Removes checkerboard "fake transparency" patterns
- Detects individual frames via alpha-channel gap analysis
- Extracts frames, normalizes to 64x64 each, bottom-aligned
- Stitches into horizontal sprite sheets:
  - `botty-idle.png`: 4 frames → 256x64
  - `botty-walk.png`: 6 frames → 384x64
  - `botty-jump.png`: 2 frames → 128x64

### 3. Backgrounds
- `sky.png`: Resize to 800x600 (no transparency)
- `clouds.png`: 800x200, background removed (threshold: 235) for parallax layering
- `hills.png`: 800x200, background removed for parallax layering

### 4. UI Elements (programmatically generated)
These are created by the script, not processed from source images:
- `btn-play.png`: 200x70 glossy green button with "PLAY" text
- `btn-levels.png`: 200x70 glossy blue button with "LEVELS" text
- `star-filled.png`: 32x32 gold star
- `star-empty.png`: 32x32 grey star
- `math-input-bg.png`: 400x250 blue panel with input field area
- `arrow-left.png`, `arrow-right.png`, `arrow-jump.png`: 64x64 semi-transparent touch controls

### 5. Objects
- `flag.png`: 64x64 with smart background removal (corner-sampling, tolerance: 35)
- `bridge-block.png`: 64x64 resized without transparency

### 6. Particles
- `dust.png`: 8x8 with background removal (threshold: 230)
- `confetti.png`: 8x8 with background removal

## Background Removal Methods

The script has two removal strategies:

**`remove_background(threshold=240)`** — For images with white/near-white backgrounds. Also strips checkerboard grey patterns (RGB 180-220 where R≈G≈B).

**`remove_bg_smart(tolerance=30)`** — For images with non-white backgrounds. Samples the 4 corners to detect background color, then removes pixels within tolerance of that average.

## Fix Scripts

If the main script produces incorrect results for specific assets:

```bash
python3 scripts/fix_sprites_and_bg.py   # Fix sprite sheet alignment and background transparency
python3 scripts/fix_remaining.py         # Handle edge cases
python3 scripts/fix_final.py             # Final tweaks
```

## Verification

After processing, verify all 21 assets match expected dimensions:

| Output Path | Expected Size |
|------------|--------------|
| `tiles/grass-top.png` | 64x64 |
| `tiles/dirt.png` | 64x64 |
| `tiles/stone.png` | 64x64 |
| `player/botty-idle.png` | 256x64 (4 frames) |
| `player/botty-walk.png` | 384x64 (6 frames) |
| `player/botty-jump.png` | 128x64 (2 frames) |
| `backgrounds/sky.png` | 800x600 |
| `backgrounds/clouds.png` | 800x200 |
| `backgrounds/hills.png` | 800x200 |
| `ui/btn-play.png` | 200x70 |
| `ui/btn-levels.png` | 200x70 |
| `ui/star-filled.png` | 32x32 |
| `ui/star-empty.png` | 32x32 |
| `ui/math-input-bg.png` | 400x250 |
| `ui/arrow-left.png` | 64x64 |
| `ui/arrow-right.png` | 64x64 |
| `ui/arrow-jump.png` | 64x64 |
| `objects/flag.png` | 64x64 |
| `objects/bridge-block.png` | 64x64 |
| `particles/dust.png` | 8x8 |
| `particles/confetti.png` | 8x8 |

Run this quick verification:

```bash
cd /home/user/mathbuilder && python3 -c "
from PIL import Image; import os
out = 'public/assets/images'
expected = {
    'tiles/grass-top.png': (64,64), 'tiles/dirt.png': (64,64), 'tiles/stone.png': (64,64),
    'player/botty-idle.png': (256,64), 'player/botty-walk.png': (384,64), 'player/botty-jump.png': (128,64),
    'backgrounds/sky.png': (800,600), 'backgrounds/clouds.png': (800,200), 'backgrounds/hills.png': (800,200),
    'ui/btn-play.png': (200,70), 'ui/btn-levels.png': (200,70), 'ui/star-filled.png': (32,32),
    'ui/star-empty.png': (32,32), 'ui/math-input-bg.png': (400,250), 'ui/arrow-left.png': (64,64),
    'ui/arrow-right.png': (64,64), 'ui/arrow-jump.png': (64,64), 'objects/flag.png': (64,64),
    'objects/bridge-block.png': (64,64), 'particles/dust.png': (8,8), 'particles/confetti.png': (8,8),
}
ok = 0
for p, (ew, eh) in expected.items():
    fp = os.path.join(out, p)
    if not os.path.exists(fp): print(f'MISSING: {p}'); continue
    w, h = Image.open(fp).size
    if (w,h) == (ew,eh): ok += 1
    else: print(f'WRONG: {p} is {w}x{h}, expected {ew}x{eh}')
print(f'{ok}/{len(expected)} assets OK')
"
```

## Requirements

- Python 3 with Pillow: `pip install Pillow`
- Source images in `resources/` subdirectories (tiles/, player/, backgrounds/, objects/, particles/)

## Troubleshooting

- **Sprite frames misaligned**: The frame detection uses alpha-channel gap analysis. If sprites overlap or have inconsistent spacing, frames may be split wrong. Try adjusting the `find_sprite_columns` gap merge threshold.
- **Background not fully removed**: Increase threshold for `remove_background()` or tolerance for `remove_bg_smart()`. Some AI-generated images have gradient backgrounds that need higher values.
- **Grass tile looks wrong**: The grass-top is generated programmatically because the Gemini output was isometric 3D. Edit `create_grass_tile()` in `process_images.py` to adjust colors or shape.
