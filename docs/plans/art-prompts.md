# Art Prompts for Google Gemini

All art assets for MathBuilder are generated using Google Gemini's image generation. Each prompt below produces one asset. After generation, crop/resize to the specified dimensions and save as PNG.

**Style keywords to use consistently:** "soft plastic voxel", "vinyl toy", "smooth rounded edges", "vibrant colors", "soft ambient lighting", "kid-friendly", "cartoon"

---

## Tiles (64x64 pixels each)

### Prompt 1 — Grass Top Tile

```
Generate a single 2D game tile, exactly 64x64 pixels, top-down isometric view flattened
for a side-scrolling platformer. The tile shows a grass block: vibrant green grass on
the top surface, cartoon brown dirt on the side.

Style: soft plastic voxel, like a smooth vinyl toy block. Soft ambient lighting, no
harsh shadows. White background. The left and right edges must be seamless (tileable
horizontally).
```

**Save to:** `public/assets/images/tiles/grass-top.png`

---

### Prompt 2 — Dirt Tile

```
Generate a single 2D game tile, exactly 64x64 pixels, for a side-scrolling platformer.
The tile shows a solid dirt/earth block. Warm brown color with subtle horizontal grain
lines suggesting layers of soil.

Style: soft plastic voxel, smooth like a toy building block. Soft ambient lighting.
White background. Seamless on all edges (tileable in all directions).
```

**Save to:** `public/assets/images/tiles/dirt.png`

---

### Prompt 3 — Stone Tile

```
Generate a single 2D game tile, exactly 64x64 pixels, for a side-scrolling platformer.
The tile shows a stone/cobblestone block. Cool grey color with subtle rounded stone
shapes embedded in it, like a cartoon cobblestone wall.

Style: soft plastic voxel, smooth like a toy building block. Soft ambient lighting.
White background. Seamless on all edges (tileable in all directions).
```

**Save to:** `public/assets/images/tiles/stone.png`

---

## Player Character — Botty (64x64 per frame)

### Character Description (use in all Botty prompts)

> Botty is a cute, chunky blue robot. He looks like a high-quality vinyl toy figure.
> He has: a square head with rounded corners, a rectangular body, stubby cylindrical
> legs, small rounded arm stubs (no fingers), a small antenna on top of his head, and
> two friendly glowing dot eyes (like white LEDs). His primary color is a vibrant
> blue, with lighter blue highlights on his chest panel. Simple shapes, bright primary
> colors, smooth surfaces.

---

### Prompt 4 — Botty Idle Sprite Sheet (4 frames)

```
Generate a horizontal sprite sheet for a 2D platformer character. The character is
"Botty", a cute chunky blue robot that looks like a vinyl toy (see character
description below).

Show 4 frames of a gentle idle breathing animation: the body bobs slightly up and
down (about 2-3 pixels of movement), the antenna sways slightly. Side view facing
right.

Each frame is exactly 64x64 pixels. Total image size: 256x64 pixels (4 frames in
a single horizontal row, packed edge-to-edge with no spacing).

Character: Square head, rectangular body, stubby legs, small antenna, dot eyes.
Vibrant blue body with lighter chest panel.

Style: soft plastic voxel, vinyl toy, vibrant colors, soft lighting.
Transparent background (PNG).
```

**Save to:** `public/assets/images/player/botty-idle.png`
**Dimensions:** 256x64 (4 frames of 64x64)

---

### Prompt 5 — Botty Walk Sprite Sheet (6 frames)

```
Generate a horizontal sprite sheet for a 2D platformer character. The character is
"Botty", a cute chunky blue robot vinyl toy.

Show 6 frames of a walk cycle animation: legs alternate stepping forward and back,
slight arm swing, body has a subtle bounce with each step. Side view facing right.

Each frame is exactly 64x64 pixels. Total image size: 384x64 pixels (6 frames in
a single horizontal row, packed edge-to-edge with no spacing).

Character: Square head, rectangular body, stubby legs, small antenna, LED dot eyes.
Vibrant blue body.

Style: soft plastic voxel, vinyl toy, vibrant colors, soft lighting.
Transparent background (PNG).
```

**Save to:** `public/assets/images/player/botty-walk.png`
**Dimensions:** 384x64 (6 frames of 64x64)

---

### Prompt 6 — Botty Jump Sprite Sheet (2 frames)

```
Generate a horizontal sprite sheet for a 2D platformer character. The character is
"Botty", a cute chunky blue robot vinyl toy.

Show 2 frames:
Frame 1 (jump up): Legs tucked up, arms raised slightly, body compact, antenna
stretched up. Excited pose.
Frame 2 (falling): Legs dangling down, arms out to the sides for balance, antenna
drooping slightly. Gentle falling pose.

Side view facing right. Each frame is exactly 64x64 pixels. Total image size:
128x64 pixels (2 frames, horizontal row, no spacing).

Character: Square head, rectangular body, stubby legs, antenna, LED dot eyes.
Vibrant blue body.

Style: soft plastic voxel, vinyl toy, vibrant colors, soft lighting.
Transparent background (PNG).
```

**Save to:** `public/assets/images/player/botty-jump.png`
**Dimensions:** 128x64 (2 frames of 64x64)

---

## Backgrounds

### Prompt 7 — Sky Gradient

```
Generate a 2D game background, exactly 800x600 pixels. A smooth vertical gradient
sky: bright cerulean blue (#87CEEB) at the top, gradually transitioning to a warm
pale blue-white (#E0F0FF) at the bottom.

No clouds, no sun, no objects — just the clean smooth gradient. This will serve as
the base background layer for a kids' platformer game.

Style: soft, warm, kid-friendly color palette. No noise or texture, just smooth color.
```

**Save to:** `public/assets/images/backgrounds/sky.png`
**Dimensions:** 800x600

---

### Prompt 8 — Clouds Parallax Layer

```
Generate a 2D parallax layer for a platformer game, exactly 800x200 pixels.

Several fluffy, rounded white cartoon clouds scattered across the image at various
heights. The clouds look like soft cotton balls or marshmallow shapes with very
gentle grey shadows on the bottom. 3-5 clouds of different sizes.

The image must be seamless when tiled horizontally (the left edge connects to the
right edge). Transparent background (PNG) — only the clouds are visible.

Style: soft plastic, kid-friendly, gentle lighting, cartoon clouds.
```

**Save to:** `public/assets/images/backgrounds/clouds.png`
**Dimensions:** 800x200, transparent background

---

### Prompt 9 — Hills Parallax Layer

```
Generate a 2D parallax layer for a platformer game, exactly 800x200 pixels.

Rolling green hills filling the bottom portion of the image. The hills have gentle,
smooth curves like a toy landscape. Multiple overlapping hill shapes in slightly
different shades of green (lighter in front, darker behind) to create depth.

The image must be seamless when tiled horizontally. Transparent background (PNG)
above the hills — only the hills are visible.

Style: soft plastic voxel, like a vinyl toy playset landscape. Vibrant greens with
soft lighting. Kid-friendly.
```

**Save to:** `public/assets/images/backgrounds/hills.png`
**Dimensions:** 800x200, transparent background

---

## UI Elements

### Prompt 10 — Play Button

```
Generate a single 2D game UI button, approximately 200x70 pixels.

A glossy green button with the text "PLAY" in bold white letters. The button has:
- Rounded corners (pill shape)
- Subtle 3D bevel/gradient (lighter on top, darker on bottom)
- Slight drop shadow underneath
- The "PLAY" text has a small text shadow for depth

Style: candy-like, glossy, bubbly, kid-friendly game UI. Think "Candy Crush" or
"Cut the Rope" button style. White background (or transparent PNG).
```

**Save to:** `public/assets/images/ui/btn-play.png`
**Dimensions:** ~200x70

---

### Prompt 11 — Levels Button

```
Generate a single 2D game UI button, approximately 200x70 pixels.

A glossy blue button with the text "LEVELS" in bold white letters. Same style as:
- Rounded corners (pill shape)
- 3D bevel/gradient
- Drop shadow
- Text shadow

Style: candy-like, glossy, kid-friendly. Matches the green Play button but in blue.
White background (or transparent PNG).
```

**Save to:** `public/assets/images/ui/btn-levels.png`
**Dimensions:** ~200x70

---

### Prompt 12 — Star Icons (Filled and Empty)

```
Generate two 2D game UI icons side by side on the same image:

Left star: A filled, glossy GOLD star (like a reward/achievement star).
Has a bright highlight/shine spot in the upper left. Rich gold/yellow color.
Size: 32x32 pixels.

Right star: An EMPTY grey star outline with the same shape and size.
Grey/silver color, slightly 3D with a subtle shadow.
Size: 32x32 pixels.

Spacing: Leave a few pixels gap between the two stars.
Total image: approximately 72x32 pixels.

Style: candy-like, rounded corners on star points (not sharp), glossy, kid-friendly.
White background.
```

**Save to:** Crop into two separate files:
- `public/assets/images/ui/star-filled.png` (32x32)
- `public/assets/images/ui/star-empty.png` (32x32)

---

### Prompt 13 — Math Input Panel Background

```
Generate a 2D UI panel for a kids' math game, approximately 400x250 pixels.

A rounded rectangle panel that looks like a toy tablet or clipboard:
- Soft blue-grey background (#E8F0FE or similar)
- Thick rounded border in a darker blue (#4A90D9)
- Rounded corners (20px radius feel)
- Gentle drop shadow
- A white rectangular area in the center (where the number input will go)
- Space at the top for a question text
- Space at the bottom for a button

Style: soft plastic, toy-like, kid-friendly, candy UI. Like a popup dialog from a
children's educational app. White background around the panel (or transparent PNG).
```

**Save to:** `public/assets/images/ui/math-input-bg.png`
**Dimensions:** ~400x250

---

### Prompt 14 — Touch Control Arrows

```
Generate three 2D game UI buttons for mobile/tablet touch screen controls, arranged
in a horizontal row:

Button 1 (LEFT): A circular button (64x64 pixels) with a left-pointing arrow (◀).
Button 2 (RIGHT): A circular button (64x64 pixels) with a right-pointing arrow (▶).
Button 3 (JUMP): A circular button (64x64 pixels) with an up-pointing arrow (▲).

Each button has:
- Dark semi-transparent background (like frosted glass)
- White arrow icon, bold and thick
- Subtle border ring
- Looks like a modern mobile game D-pad button

Transparent background (PNG). Style: clean, minimal, semi-transparent, professional
mobile game controls.
```

**Save to:** Crop into three separate files:
- `public/assets/images/ui/arrow-left.png` (64x64)
- `public/assets/images/ui/arrow-right.png` (64x64)
- `public/assets/images/ui/arrow-jump.png` (64x64)

---

## Game Objects

### Prompt 15 — Goal Flag

```
Generate a 2D game sprite, exactly 64x64 pixels.

A checkered race/finish flag on a thin pole:
- The flag is a small rectangle with a red and white checkered pattern
- It's waving slightly (not stiff, has a gentle curve)
- The pole is thin, dark grey/brown, goes from bottom to top of the sprite
- The flag is attached at the top of the pole

Style: soft plastic voxel, toy-like, vibrant red and white colors.
Transparent background (PNG). The pole base should be at the bottom of the 64x64
frame.
```

**Save to:** `public/assets/images/objects/flag.png`
**Dimensions:** 64x64, transparent background

---

### Prompt 16 — Bridge Block

```
Generate a single 2D game tile, exactly 64x64 pixels, for a side-scrolling platformer.

The tile shows a wooden plank/bridge block:
- Warm wood brown color (#8B6914 or similar)
- Visible horizontal plank lines (2-3 planks stacked)
- Slightly different style from ground/earth tiles — this looks BUILT, not natural
- Like wooden planks nailed together

Style: soft plastic voxel, smooth like a toy building block. Soft lighting.
White background. Seamless on left and right edges (tileable horizontally).
```

**Save to:** `public/assets/images/objects/bridge-block.png`
**Dimensions:** 64x64

---

## Particles (8x8 pixels each)

### Prompt 17 — Dust Particle

```
Generate a tiny 2D particle sprite, exactly 8x8 pixels (you may generate it larger
and I will resize).

A small, soft dust puff:
- Tan/beige/light brown color
- Circular shape with soft/fuzzy edges fading to transparency
- Looks like a tiny cloud of dust

Simple, minimal. Transparent background (PNG).
```

**Save to:** `public/assets/images/particles/dust.png`
**Dimensions:** 8x8, transparent background

---

### Prompt 18 — Confetti Particle

```
Generate a tiny 2D particle sprite, exactly 8x8 pixels (you may generate it larger
and I will resize).

A small square confetti piece:
- Bright white or light yellow color
- Simple flat square/rectangle shape with slightly rounded corners
- Minimal detail

Note: This will be tinted different colors at runtime by the game engine, so a
neutral white/yellow base works best.

Simple, minimal. Transparent background (PNG).
```

**Save to:** `public/assets/images/particles/confetti.png`
**Dimensions:** 8x8, transparent background

---

## Tips for Better Gemini Results

1. **If results are too realistic:** Add "cartoon style, flat shading, no photorealism" to the prompt
2. **If results have wrong dimensions:** Generate at any size and manually resize in an image editor. The exact pixel dimensions matter for Phaser's spritesheet parser.
3. **If sprite sheets have inconsistent frames:** Generate each frame separately and stitch them together horizontally in an image editor
4. **If tiles aren't seamless:** Generate a 2x1 tile version and crop the center 64x64 — the seam will be in the middle where it's seamless
5. **If backgrounds have unwanted objects:** Specify "no objects, no characters, no text" in the prompt
6. **For transparency:** Always request "transparent background (PNG)". If Gemini returns a white background, use an image editor's magic wand/background removal tool.
7. **Batch processing:** Generate all tiles in one session, all Botty sprites in another, etc. This helps maintain style consistency within each category.
8. **Regenerate variations:** For each prompt, generate 3-4 variations and pick the best one. Gemini outputs vary significantly between runs.

---

## Asset Checklist

| # | Asset | Dimensions | Transparent | Generated | Processed | In Place |
|---|-------|-----------|-------------|-----------|-----------|----------|
| 1 | grass-top.png | 64x64 | No | [ ] | [ ] | [ ] |
| 2 | dirt.png | 64x64 | No | [ ] | [ ] | [ ] |
| 3 | stone.png | 64x64 | No | [ ] | [ ] | [ ] |
| 4 | botty-idle.png | 256x64 | Yes | [ ] | [ ] | [ ] |
| 5 | botty-walk.png | 384x64 | Yes | [ ] | [ ] | [ ] |
| 6 | botty-jump.png | 128x64 | Yes | [ ] | [ ] | [ ] |
| 7 | sky.png | 800x600 | No | [ ] | [ ] | [ ] |
| 8 | clouds.png | 800x200 | Yes | [ ] | [ ] | [ ] |
| 9 | hills.png | 800x200 | Yes | [ ] | [ ] | [ ] |
| 10 | btn-play.png | ~200x70 | Yes | [ ] | [ ] | [ ] |
| 11 | btn-levels.png | ~200x70 | Yes | [ ] | [ ] | [ ] |
| 12 | star-filled.png | 32x32 | Yes | [ ] | [ ] | [ ] |
| 13 | star-empty.png | 32x32 | Yes | [ ] | [ ] | [ ] |
| 14 | math-input-bg.png | ~400x250 | Yes | [ ] | [ ] | [ ] |
| 15 | arrow-left.png | 64x64 | Yes | [ ] | [ ] | [ ] |
| 16 | arrow-right.png | 64x64 | Yes | [ ] | [ ] | [ ] |
| 17 | arrow-jump.png | 64x64 | Yes | [ ] | [ ] | [ ] |
| 18 | flag.png | 64x64 | Yes | [ ] | [ ] | [ ] |
| 19 | bridge-block.png | 64x64 | No | [ ] | [ ] | [ ] |
| 20 | dust.png | 8x8 | Yes | [ ] | [ ] | [ ] |
| 21 | confetti.png | 8x8 | Yes | [ ] | [ ] | [ ] |
