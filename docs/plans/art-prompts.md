# Art Prompts for Google Gemini — Modern 3D Style

All art assets for MathBuilder are generated using Google Gemini's image generation. Each prompt below produces one asset. After generation, crop/resize to the specified dimensions and save as PNG.

**Style keywords to use consistently:** "3D rendered", "clay render", "smooth subsurface scattering", "ambient occlusion", "volumetric lighting", "soft global illumination", "physically-based materials", "modern mobile game art", "Blender 3D render", "kid-friendly", "vibrant saturated colors"

**Art Direction:** Think modern clay/Claymation 3D renders — like *Fall Guys*, *Yoshi's Crafted World*, or *Captain Toad*. Objects should look like high-quality 3D-printed figures with smooth surfaces, soft shadows, subtle ambient occlusion in crevices, and a warm global illumination feel. Materials should feel tactile — matte clay, glossy plastic, brushed wood — not flat or cartoony.

---

## Tiles (64x64 pixels each)

### Prompt 1 — Grass Top Tile

```
Generate a single 2D game tile for a side-scrolling platformer, rendered in a modern
3D clay style. The tile shows a grass block: lush green grass on the top surface with
individual blades of grass that have depth and volume, cartoon brown dirt/earth on the
side with visible layered sediment and small embedded pebbles.

The grass should look like sculpted clay or felt — thick, dimensional, with subtle
ambient occlusion where the blades meet the dirt. The dirt should have a warm, baked-
clay appearance with soft internal shadows showing depth between soil layers.

Style: 3D rendered, clay/Claymation aesthetic, smooth subsurface scattering on the
grass, ambient occlusion in crevices, soft global illumination, warm lighting from
upper left. Vibrant saturated colors. White background.
Left and right edges must be seamless (tileable horizontally).
```

**Save to:** `public/assets/images/tiles/grass-top.png`

---

### Prompt 2 — Dirt Tile

```
Generate a single 2D game tile for a side-scrolling platformer, rendered in a modern
3D clay style. The tile shows a solid dirt/earth block with visible layers of compacted
soil, small embedded stones, and subtle root-like details.

The dirt should look like sculpted clay with warm brown tones, subtle depth between
layers, and ambient occlusion in the crevices. Multiple shades of brown with slight
color variation for visual interest.

Style: 3D rendered, clay/Claymation aesthetic, ambient occlusion, soft global
illumination, warm directional lighting. Physically-based materials — matte clay
surface. White background.
Seamless on all edges (tileable in all directions).
```

**Save to:** `public/assets/images/tiles/dirt.png`

---

### Prompt 3 — Stone Tile

```
Generate a single 2D game tile for a side-scrolling platformer, rendered in a modern
3D clay style. The tile shows a stone/cobblestone block with rounded, individually
sculpted stones fitted together with dark mortar gaps between them.

Each stone should have subtle surface detail — slight glossy highlights, soft ambient
occlusion in the gaps between stones, and gentle color variation (cool greys with
hints of blue and warm undertones). The mortar lines should have deep shadows.

Style: 3D rendered, clay/Claymation aesthetic, physically-based stone material with
subtle specular highlights, ambient occlusion in crevices, soft global illumination.
White background.
Seamless on all edges (tileable in all directions).
```

**Save to:** `public/assets/images/tiles/stone.png`

---

## Player Character — Botty (64x64 per frame)

### Character Description (use in all Botty prompts)

> Botty is a cute, chunky blue robot rendered in a modern 3D clay/Claymation style.
> He looks like a high-end 3D-printed collectible figure. He has: a square head with
> smooth rounded corners, a rectangular body with a recessed chest panel, stubby
> cylindrical legs with ball-joint connections, small rounded arm stubs, a small
> antenna on top with a glowing orb tip, and two friendly glowing LED eyes (soft
> white glow with slight bloom). His primary color is a rich metallic blue with
> subtle specular highlights and soft ambient occlusion in joints and recesses.
> Lighter sky-blue on his chest panel. Materials: glossy plastic body, matte rubber
> joints, emissive LED eyes and antenna tip. Warm rim lighting from behind.

---

### Prompt 4 — Botty Idle Sprite Sheet (4 frames)

```
Generate a horizontal sprite sheet for a 2D platformer character, rendered in a modern
3D clay/Claymation style. The character is "Botty", a cute chunky blue robot (see
character description).

Show 4 frames of a gentle idle breathing animation: the body bobs slightly up and down
(2-3 pixels), the antenna sways gently, the LED eyes have a subtle pulse glow. Side
view facing right.

Each frame is exactly 64x64 pixels. Total image: 256x64 pixels (4 frames in a single
horizontal row, packed edge-to-edge with no spacing).

Style: 3D rendered with ambient occlusion at joints, soft subsurface scattering on
the blue plastic, warm rim lighting from behind-right, subtle specular highlights on
the glossy body. Physically-based materials.
Transparent background (PNG).
```

**Save to:** `public/assets/images/player/botty-idle.png`
**Dimensions:** 256x64 (4 frames of 64x64)

---

### Prompt 5 — Botty Walk Sprite Sheet (6 frames)

```
Generate a horizontal sprite sheet for a 2D platformer character, rendered in a modern
3D clay/Claymation style. The character is "Botty", a cute chunky blue robot.

Show 6 frames of a walk cycle animation: legs alternate stepping forward and back with
ball-joint articulation, slight arm swing, body has a bouncy bob with each step, antenna
bounces. Side view facing right.

Each frame is exactly 64x64 pixels. Total image: 384x64 pixels (6 frames in a single
horizontal row, packed edge-to-edge with no spacing).

Style: 3D rendered with ambient occlusion at joints, soft subsurface scattering,
warm rim lighting, specular highlights on glossy blue plastic body. Physically-based
materials.
Transparent background (PNG).
```

**Save to:** `public/assets/images/player/botty-walk.png`
**Dimensions:** 384x64 (6 frames of 64x64)

---

### Prompt 6 — Botty Jump Sprite Sheet (2 frames)

```
Generate a horizontal sprite sheet for a 2D platformer character, rendered in a modern
3D clay/Claymation style. The character is "Botty", a cute chunky blue robot.

Show 2 frames:
Frame 1 (jump up): Legs tucked up, arms raised, body compact, antenna stretched up
with glowing tip. Excited energetic pose with motion lines implied.
Frame 2 (falling): Legs dangling, arms out for balance, antenna drooping. Gentle
falling pose with slight tilt.

Side view facing right. Each frame is exactly 64x64 pixels. Total image: 128x64 pixels
(2 frames, horizontal row, no spacing).

Style: 3D rendered with ambient occlusion, subsurface scattering, warm rim lighting,
specular highlights. Physically-based glossy plastic materials.
Transparent background (PNG).
```

**Save to:** `public/assets/images/player/botty-jump.png`
**Dimensions:** 128x64 (2 frames of 64x64)

---

## Backgrounds

### Prompt 7 — Sky Gradient

```
Generate a 2D game background, exactly 800x600 pixels. A rich atmospheric sky with
depth and dimension: deep cerulean blue (#2E86C1) at the top gradually transitioning
through warm sky blue to a soft peachy-golden horizon (#FDEBD0) at the bottom.

Add very subtle atmospheric haze layers and gentle volumetric light rays coming from
the upper-right corner for a warm, magical feeling. No clouds, no sun, no objects —
just the atmospheric gradient with subtle light effects.

Style: 3D rendered sky dome, volumetric atmosphere, warm global illumination, modern
mobile game background quality. Smooth gradients with subtle noise for richness.
Kid-friendly, inviting, warm palette.
```

**Save to:** `public/assets/images/backgrounds/sky.png`
**Dimensions:** 800x600

---

### Prompt 8 — Clouds Parallax Layer

```
Generate a 2D parallax layer for a platformer game, exactly 800x200 pixels.

Several fluffy, volumetric 3D clouds with realistic depth: soft rounded shapes with
subtle self-shadowing on the bottom, bright highlights on top where the sun hits,
and gentle translucent edges. 3-5 clouds of different sizes scattered at various
heights. The clouds should look like sculpted cotton or soft clay.

The image must be seamless when tiled horizontally. Transparent background (PNG).

Style: 3D rendered clouds with subsurface scattering, volumetric lighting from upper
right, ambient occlusion on undersides. Modern mobile game quality, soft and dreamy.
Kid-friendly.
```

**Save to:** `public/assets/images/backgrounds/clouds.png`
**Dimensions:** 800x200, transparent background

---

### Prompt 9 — Hills Parallax Layer

```
Generate a 2D parallax layer for a platformer game, exactly 800x200 pixels.

Rolling green hills with depth and dimension, filling the bottom portion. Multiple
overlapping hill layers with parallax depth: lighter vibrant green hills in front,
deeper green hills behind. Each hill has gentle 3D shading — soft highlight on top
where the light hits, ambient occlusion at the base where hills overlap.

Small details: subtle grass tufts on hilltops, tiny wildflowers dots of color (yellow,
pink). The hills should look like a sculpted clay landscape diorama.

Seamless when tiled horizontally. Transparent background (PNG) above the hills.

Style: 3D rendered, clay/diorama aesthetic, soft global illumination, warm afternoon
light, ambient occlusion. Vibrant greens with warm undertones. Kid-friendly.
```

**Save to:** `public/assets/images/backgrounds/hills.png`
**Dimensions:** 800x200, transparent background

---

## UI Elements

### Prompt 10 — Play Button

```
Generate a single 2D game UI button, approximately 200x70 pixels, rendered in a modern
3D style.

A glossy green button with the text "PLAY" in bold white 3D-extruded letters. The button
has:
- Pill/capsule shape with smooth rounded edges
- Full 3D depth: visible thickness/extrusion on the bottom and right edges
- Glossy top surface with a bright specular highlight streak
- Subtle environment reflection on the glossy surface
- Soft drop shadow with slight blur underneath
- The text has 3D extrusion/bevel and a subtle inner glow

Style: modern mobile game UI, 3D rendered button like a physical candy or jelly piece.
Glossy PBR materials, warm lighting. Looks like you could pick it up and press it.
White background (or transparent PNG).
```

**Save to:** `public/assets/images/ui/btn-play.png`
**Dimensions:** ~200x70

---

### Prompt 11 — Levels Button

```
Generate a single 2D game UI button, approximately 200x70 pixels, rendered in a modern
3D style.

A glossy blue button with the text "LEVELS" in bold white 3D-extruded letters. Same
3D style as the Play button:
- Pill shape with visible 3D thickness/extrusion
- Glossy surface with specular highlight
- Environment reflection
- Drop shadow
- 3D text with bevel

Style: modern mobile game UI, 3D rendered, PBR glossy materials. Matches the green
Play button but in vibrant blue. White background (or transparent PNG).
```

**Save to:** `public/assets/images/ui/btn-levels.png`
**Dimensions:** ~200x70

---

### Prompt 12 — Star Icons (Filled and Empty)

```
Generate two 2D game UI star icons side by side:

Left star: A filled, glossy GOLD 3D star (reward/achievement star). Rendered as a
3D object with visible thickness, bright specular highlights, warm golden reflections,
and a small lens flare/sparkle on one point. Rich gold metallic PBR material.
Size: 32x32 pixels.

Right star: An EMPTY grey 3D star outline with the same 3D shape. Brushed silver/grey
metallic material with subtle specular highlights but more muted than the gold star.
Slight inner bevel. Size: 32x32 pixels.

Leave a few pixels gap between them. Total: ~72x32 pixels.

Style: 3D rendered, metallic PBR materials, warm lighting from upper-left, soft ambient
occlusion. Modern mobile game quality. White background.
```

**Save to:** Crop into two files:
- `public/assets/images/ui/star-filled.png` (32x32)
- `public/assets/images/ui/star-empty.png` (32x32)

---

### Prompt 13 — Math Input Panel Background

```
Generate a 2D UI panel for a kids' math game, approximately 400x250 pixels, rendered
in a modern 3D style.

A rounded rectangle panel that looks like a 3D tablet or clipboard floating in space:
- Soft blue-gradient background with glass-morphism effect (frosted glass feel)
- Thick rounded border with 3D depth/thickness visible on bottom and right edges
- Smooth rounded corners (20px radius)
- Realistic soft drop shadow with subtle blur
- A white recessed input area in the center (sunken/inset 3D effect)
- Subtle inner glow around the panel edges
- Space at top for question text, space at bottom for button

Style: modern mobile game UI, 3D rendered panel, glass-morphism with PBR materials.
Warm lighting, soft ambient occlusion at edges. Like a physical toy tablet.
Transparent background (PNG).
```

**Save to:** `public/assets/images/ui/math-input-bg.png`
**Dimensions:** ~400x250

---

### Prompt 14 — Touch Control Arrows

```
Generate three 2D game UI buttons for mobile touch controls, arranged horizontally:

Button 1 (LEFT): A circular button (64x64) with a left-pointing arrow (◀).
Button 2 (RIGHT): A circular button (64x64) with a right-pointing arrow (▶).
Button 3 (JUMP): A circular button (64x64) with an up-pointing arrow (▲).

Each button has:
- Glass-morphism/frosted glass appearance with depth
- Semi-transparent dark background with subtle blur effect
- Bright white arrow icon with 3D bevel/extrusion
- Soft glowing ring around the edge (subtle neon-like)
- Subtle specular highlight on the glass surface
- Looks like a modern mobile game's virtual joystick buttons

Transparent background (PNG).
Style: modern mobile game UI, glass-morphism, 3D rendered controls with depth,
soft glow effects, clean and professional.
```

**Save to:** Crop into three files:
- `public/assets/images/ui/arrow-left.png` (64x64)
- `public/assets/images/ui/arrow-right.png` (64x64)
- `public/assets/images/ui/arrow-jump.png` (64x64)

---

## Game Objects

### Prompt 15 — Goal Flag

```
Generate a 2D game sprite, exactly 64x64 pixels, rendered in modern 3D clay style.

A checkered race/finish flag on a thin metallic pole:
- The flag is a small rectangle with red and white checkered pattern, 3D cloth
  simulation look with gentle waving folds and self-shadowing
- The pole is thin brushed metal (chrome/silver), goes from bottom to top
- The flag is attached at the top, waving to the right
- Small circular metal base at the bottom

Style: 3D rendered, clay/Claymation aesthetic. PBR materials: glossy fabric for the
flag with subsurface scattering, brushed metal for the pole. Ambient occlusion,
soft global illumination, warm lighting.
Transparent background (PNG). Pole base at bottom of 64x64 frame.
```

**Save to:** `public/assets/images/objects/flag.png`
**Dimensions:** 64x64, transparent background

---

### Prompt 16 — Bridge Block

```
Generate a single 2D game tile, exactly 64x64 pixels, for a side-scrolling platformer,
rendered in modern 3D clay style.

The tile shows a wooden plank/bridge block:
- Warm honey-oak wood with visible 3D wood grain texture
- 2-3 planks stacked horizontally with visible gaps between them
- Iron/metal nail heads or bolts at the corners (small shiny details)
- Subtle ambient occlusion between the planks
- Slight worn/weathered edges for character

Style: 3D rendered, clay/Claymation aesthetic, PBR wood material with subtle specular
highlights, ambient occlusion in plank gaps, warm directional lighting. Looks built
and crafted, distinctly different from natural ground tiles.
White background. Seamless on left and right edges.
```

**Save to:** `public/assets/images/objects/bridge-block.png`
**Dimensions:** 64x64

---

## Particles (8x8 pixels each)

### Prompt 17 — Dust Particle

```
Generate a small 2D particle sprite (generate at 64x64, will be resized to 8x8).

A soft dust puff with 3D volume:
- Warm tan/beige color with subtle internal color variation
- Soft, volumetric shape — like a tiny 3D-rendered smoke puff
- Smooth falloff edges fading to full transparency
- Subtle internal highlight suggesting light passing through

Style: 3D rendered particle with subsurface scattering, soft volumetric look.
Transparent background (PNG).
```

**Save to:** `public/assets/images/particles/dust.png`
**Dimensions:** 8x8, transparent background

---

### Prompt 18 — Confetti Particle

```
Generate a small 2D particle sprite (generate at 64x64, will be resized to 8x8).

A single confetti piece with 3D depth:
- White/light yellow base color (will be tinted at runtime)
- Small square/rectangle shape with slightly rounded corners
- Subtle 3D thickness visible (like a tiny piece of paper in perspective)
- Tiny specular highlight on one face

Style: 3D rendered with physically-based material, soft lighting. Simple and minimal.
Transparent background (PNG).
```

**Save to:** `public/assets/images/particles/confetti.png`
**Dimensions:** 8x8, transparent background

---

## Tips for Better Gemini Results (Modern 3D Style)

1. **Key style anchor phrase:** Always include "3D rendered, clay/Claymation style, ambient occlusion, PBR materials" in every prompt for consistency
2. **If results look too flat:** Add "volumetric lighting, subsurface scattering, specular highlights, depth of field"
3. **If results are too realistic/scary:** Add "kid-friendly, soft colors, rounded edges, cute proportions, warm lighting"
4. **If results have wrong dimensions:** Generate at any size and resize. Consider generating at 2x resolution and downscaling for crispness.
5. **For sprite sheets:** Generate each frame separately with identical camera angle and lighting, then stitch horizontally
6. **For tiles:** Add "seamless, tileable" and generate a 2x2 grid, then crop one tile from the center
7. **For transparency:** Always request "transparent background (PNG)". Use background removal if Gemini returns solid backgrounds.
8. **Batch by category:** Generate all tiles in one session for style consistency, then all Botty sprites, etc.
9. **Lighting consistency:** All assets should use warm directional lighting from the upper-left for cohesive look
10. **Reference images:** Include references to games like Fall Guys, Yoshi's Crafted World, or Captain Toad for the desired 3D aesthetic

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
