# Process Images

Process raw Gemini-generated images from `resources/` into game-ready assets in `public/assets/images/`.

## Instructions

1. Check if new or modified source images exist in `resources/` subdirectories (tiles/, player/, backgrounds/, ui/, objects/, particles/)
2. Run the main image processing pipeline:

```bash
cd /home/user/mathbuilder && python3 scripts/process_images.py
```

3. If the main script fails or produces incorrect results for specific assets, check and run the fix scripts as needed:
   - `scripts/fix_sprites_and_bg.py` — fixes sprite sheet alignment and background transparency
   - `scripts/fix_remaining.py` — handles edge cases for remaining assets
   - `scripts/fix_final.py` — final tweaks and corrections

4. Verify all 21 output assets exist with correct dimensions:

| Output Path | Expected Size |
|------------|--------------|
| tiles/grass-top.png | 64x64 |
| tiles/dirt.png | 64x64 |
| tiles/stone.png | 64x64 |
| player/botty-idle.png | 256x64 (4 frames) |
| player/botty-walk.png | 384x64 (6 frames) |
| player/botty-jump.png | 128x64 (2 frames) |
| backgrounds/sky.png | 800x600 |
| backgrounds/clouds.png | 800x200 |
| backgrounds/hills.png | 800x200 |
| ui/btn-play.png | 200x70 |
| ui/btn-levels.png | 200x70 |
| ui/star-filled.png | 32x32 |
| ui/star-empty.png | 32x32 |
| ui/math-input-bg.png | 400x250 |
| ui/arrow-left.png | 64x64 |
| ui/arrow-right.png | 64x64 |
| ui/arrow-jump.png | 64x64 |
| objects/flag.png | 64x64 |
| objects/bridge-block.png | 64x64 |
| particles/dust.png | 8x8 |
| particles/confetti.png | 8x8 |

5. Report any assets that are missing or have wrong dimensions.

## Processing Pipeline Details

The scripts handle:
- **Background removal:** Strips white/near-white backgrounds and checkerboard patterns from AI-generated images
- **Sprite extraction:** Finds individual character frames from scattered sprite sheets using alpha-channel gap analysis
- **Tile processing:** Crops rounded edges, resizes to exact 64x64
- **Programmatic generation:** Creates UI elements (stars, buttons, arrows, math panel) when source images aren't suitable
- **Verification:** Validates all output dimensions match game requirements

## Requirements
- Python 3 with Pillow: `pip install Pillow`
