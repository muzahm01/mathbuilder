#!/usr/bin/env python3
"""
MathBuilder Image Processing Script
====================================
Processes raw Gemini-generated images in resources/ into game-ready assets
in public/assets/images/ with correct dimensions, format, and transparency.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math

RESOURCES = "/home/user/mathbuilder/resources"
OUTPUT = "/home/user/mathbuilder/public/assets/images"


def ensure_dirs():
    """Create all output directories."""
    for subdir in ["tiles", "player", "backgrounds", "ui", "objects", "particles"]:
        os.makedirs(os.path.join(OUTPUT, subdir), exist_ok=True)


def remove_background(img, threshold=240):
    """
    Remove white/near-white background and checkerboard patterns.
    Returns RGBA image with transparent background.
    """
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for pixel in data:
        r, g, b, a = pixel
        # Remove white and near-white pixels
        if r > threshold and g > threshold and b > threshold:
            new_data.append((r, g, b, 0))
        # Remove checkerboard grey pixels (common in AI-generated "transparency")
        elif abs(r - g) < 10 and abs(g - b) < 10 and 180 < r < 220:
            new_data.append((r, g, b, 0))
        else:
            new_data.append(pixel)
    img.putdata(new_data)
    return img


def remove_bg_smart(img, tolerance=30):
    """
    Remove background by sampling corner colors and removing similar pixels.
    Better for images where the background isn't pure white.
    """
    img = img.convert("RGBA")
    w, h = img.size
    # Sample corners to determine background color
    corners = [
        img.getpixel((2, 2)),
        img.getpixel((w - 3, 2)),
        img.getpixel((2, h - 3)),
        img.getpixel((w - 3, h - 3)),
    ]
    # Average corner color
    avg_r = sum(c[0] for c in corners) // 4
    avg_g = sum(c[1] for c in corners) // 4
    avg_b = sum(c[2] for c in corners) // 4

    data = img.getdata()
    new_data = []
    for pixel in data:
        r, g, b, a = pixel
        if (abs(r - avg_r) < tolerance and
            abs(g - avg_g) < tolerance and
            abs(b - avg_b) < tolerance):
            new_data.append((r, g, b, 0))
        else:
            new_data.append(pixel)
    img.putdata(new_data)
    return img


def crop_to_content(img, padding=2):
    """Crop an RGBA image to its non-transparent content with optional padding."""
    bbox = img.getbbox()
    if bbox is None:
        return img
    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(img.width, right + padding)
    bottom = min(img.height, bottom + padding)
    return img.crop((left, top, right, bottom))


def find_sprite_columns(img, num_sprites, scan_row=None):
    """
    Find individual sprites in a horizontal arrangement by analyzing
    alpha channel gaps. Returns list of (left, right) x-coordinates.
    """
    if scan_row is None:
        # Scan at the vertical center
        scan_row = img.height // 2

    w = img.width
    data = img.load()

    # Build a horizontal alpha profile
    alpha_profile = []
    for x in range(w):
        col_has_content = False
        for y_offset in range(-30, 31, 5):
            y = max(0, min(img.height - 1, scan_row + y_offset))
            if data[x, y][3] > 30:  # non-transparent
                col_has_content = True
                break
        alpha_profile.append(col_has_content)

    # Find runs of content
    spans = []
    in_span = False
    start = 0
    for x, has_content in enumerate(alpha_profile):
        if has_content and not in_span:
            start = x
            in_span = True
        elif not has_content and in_span:
            spans.append((start, x))
            in_span = False
    if in_span:
        spans.append((start, w))

    # Merge spans that are very close together (< 5px gap)
    merged = [spans[0]] if spans else []
    for s, e in spans[1:]:
        if s - merged[-1][1] < 5:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))

    # If we found more spans than expected, merge closest ones
    while len(merged) > num_sprites:
        # Find smallest gap and merge
        min_gap = float('inf')
        min_idx = 0
        for i in range(len(merged) - 1):
            gap = merged[i + 1][0] - merged[i][1]
            if gap < min_gap:
                min_gap = gap
                min_idx = i
        merged[min_idx] = (merged[min_idx][0], merged[min_idx + 1][1])
        merged.pop(min_idx + 1)

    # If we found fewer spans than expected, split the largest ones
    while len(merged) < num_sprites:
        # Find widest span and split it
        max_w = 0
        max_idx = 0
        for i, (s, e) in enumerate(merged):
            if e - s > max_w:
                max_w = e - s
                max_idx = i
        s, e = merged[max_idx]
        mid = (s + e) // 2
        merged[max_idx] = (s, mid)
        merged.insert(max_idx + 1, (mid, e))

    return merged


def extract_sprites(img, num_sprites, target_size=64):
    """
    Extract individual sprite frames from a sheet with scattered poses.
    Returns a properly formatted horizontal sprite sheet.
    """
    img = img.convert("RGBA")

    # Try to remove background first
    clean = remove_background(img)

    # Find vertical content bounds
    bbox = clean.getbbox()
    if bbox is None:
        # Fallback: just divide evenly
        frame_w = img.width // num_sprites
        frames = []
        for i in range(num_sprites):
            frame = img.crop((i * frame_w, 0, (i + 1) * frame_w, img.height))
            frame = frame.resize((target_size, target_size), Image.LANCZOS)
            frames.append(frame)
    else:
        # Crop to vertical content area
        content = clean.crop((0, bbox[1], clean.width, bbox[3]))

        # Find sprite columns
        columns = find_sprite_columns(content, num_sprites)

        frames = []
        for left, right in columns:
            # Extract this sprite with some vertical padding
            sprite = content.crop((left, 0, right, content.height))
            sprite = crop_to_content(sprite, padding=1)

            # Resize to fit in target_size x target_size, maintaining aspect ratio
            sw, sh = sprite.size
            scale = min(target_size / sw, target_size / sh) * 0.9  # 90% fill
            new_w = max(1, int(sw * scale))
            new_h = max(1, int(sh * scale))
            sprite = sprite.resize((new_w, new_h), Image.LANCZOS)

            # Center in target_size x target_size frame
            frame = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
            paste_x = (target_size - new_w) // 2
            paste_y = target_size - new_h - 2  # Align to bottom with 2px margin
            frame.paste(sprite, (paste_x, paste_y), sprite)
            frames.append(frame)

    # Stitch into horizontal strip
    sheet = Image.new("RGBA", (target_size * num_sprites, target_size), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        sheet.paste(frame, (i * target_size, 0), frame)

    return sheet


def draw_star(draw, cx, cy, outer_r, inner_r, color, outline=None):
    """Draw a 5-pointed star centered at (cx, cy)."""
    points = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        r = outer_r if i % 2 == 0 else inner_r
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=color, outline=outline)


def create_star_filled(size=32):
    """Create a glossy gold filled star icon."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2 + 1
    outer_r = size // 2 - 2
    inner_r = outer_r * 0.38

    # Main star
    draw_star(draw, cx, cy, outer_r, inner_r, (255, 200, 0, 255), outline=(200, 150, 0, 255))
    # Highlight overlay (lighter star offset up-left)
    draw_star(draw, cx - 1, cy - 1, outer_r - 2, inner_r - 1, (255, 230, 80, 180))
    # Bright spot
    draw.ellipse((cx - 4, cy - 6, cx + 1, cy - 2), fill=(255, 255, 200, 160))

    return img


def create_star_empty(size=32):
    """Create a grey empty star icon."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2 + 1
    outer_r = size // 2 - 2
    inner_r = outer_r * 0.38

    # Grey star
    draw_star(draw, cx, cy, outer_r, inner_r, (160, 165, 175, 255), outline=(120, 125, 135, 255))
    # Subtle highlight
    draw_star(draw, cx - 1, cy - 1, outer_r - 2, inner_r - 1, (180, 185, 195, 120))

    return img


def create_button(text, base_color, width=200, height=70):
    """Create a glossy candy-style button with text."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    r, g, b = base_color
    radius = height // 2

    # Shadow
    draw.rounded_rectangle(
        (4, 6, width - 4, height - 2),
        radius=radius,
        fill=(r // 3, g // 3, b // 3, 120)
    )

    # Main body (darker bottom half)
    draw.rounded_rectangle(
        (2, 2, width - 2, height - 4),
        radius=radius,
        fill=(int(r * 0.75), int(g * 0.75), int(b * 0.75), 255)
    )

    # Upper gradient (lighter)
    draw.rounded_rectangle(
        (2, 2, width - 2, height // 2 + 8),
        radius=radius,
        fill=(r, g, b, 255)
    )

    # Gloss highlight
    draw.rounded_rectangle(
        (8, 4, width - 8, height // 3),
        radius=radius - 4,
        fill=(min(255, r + 60), min(255, g + 60), min(255, b + 60), 100)
    )

    # Border
    draw.rounded_rectangle(
        (2, 2, width - 2, height - 4),
        radius=radius,
        outline=(int(r * 0.5), int(g * 0.5), int(b * 0.5), 255),
        width=2
    )

    # Text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (width - tw) // 2
    ty = (height - th) // 2 - 3

    # Text shadow
    draw.text((tx + 1, ty + 2), text, fill=(0, 0, 0, 80), font=font)
    # White text
    draw.text((tx, ty), text, fill=(255, 255, 255, 255), font=font)

    return img


def create_arrow_button(direction, size=64):
    """Create a semi-transparent touch control button with arrow."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Circle background
    draw.ellipse((2, 2, size - 2, size - 2), fill=(40, 50, 65, 160))
    draw.ellipse((2, 2, size - 2, size - 2), outline=(100, 115, 135, 200), width=2)

    cx, cy = size // 2, size // 2
    s = size // 5  # Arrow size

    if direction == "left":
        points = [(cx + s, cy - s), (cx - s, cy), (cx + s, cy + s)]
    elif direction == "right":
        points = [(cx - s, cy - s), (cx + s, cy), (cx - s, cy + s)]
    elif direction == "jump":
        points = [(cx - s, cy + s // 2), (cx, cy - s), (cx + s, cy + s // 2)]

    draw.polygon(points, fill=(240, 245, 255, 220))

    return img


def create_math_input_bg(width=400, height=250):
    """Create a kid-friendly math input panel background."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Panel body
    draw.rounded_rectangle(
        (8, 8, width - 8, height - 8),
        radius=20,
        fill=(232, 240, 254, 245)
    )

    # Border
    draw.rounded_rectangle(
        (8, 8, width - 8, height - 8),
        radius=20,
        outline=(74, 144, 217, 255),
        width=4
    )

    # Inner white area for input
    inner_y = height // 2 - 25
    draw.rounded_rectangle(
        (40, inner_y, width - 40, inner_y + 50),
        radius=12,
        fill=(255, 255, 255, 255),
        outline=(74, 144, 217, 180),
        width=2
    )

    # Drop shadow
    shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        (12, 14, width - 4, height - 2),
        radius=20,
        fill=(0, 0, 0, 40)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(4))

    # Composite shadow behind panel
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    result.paste(shadow, (0, 0), shadow)
    result.paste(img, (0, 0), img)

    return result


def create_grass_tile(size=64):
    """
    Create a front-facing grass tile suitable for side-scrolling.
    Green grass on top, brown dirt below.
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Dirt body (lower portion)
    draw.rectangle((0, 0, size, size), fill=(139, 100, 60))

    # Dirt variation stripes
    for y in range(0, size, 8):
        shade = 130 + (y * 3) % 20 - 10
        draw.rectangle((0, y, size, y + 4), fill=(shade, int(shade * 0.72), int(shade * 0.43)))

    # Small embedded stones
    stones = [(12, 35, 18, 40), (40, 25, 48, 31), (8, 50, 14, 55), (50, 45, 58, 50)]
    for sx, sy, ex, ey in stones:
        draw.rounded_rectangle((sx, sy, ex, ey), radius=2, fill=(120, 90, 55))

    # Grass top layer (top ~20 pixels)
    grass_h = 18
    # Base grass
    draw.rectangle((0, 0, size, grass_h), fill=(80, 185, 60))
    # Lighter top
    draw.rectangle((0, 0, size, grass_h // 2), fill=(100, 210, 75))
    # Grass edge (wavy-ish bottom)
    for x in range(0, size, 4):
        offset = int(2 * math.sin(x * 0.5))
        draw.rectangle((x, grass_h + offset - 2, x + 4, grass_h + offset + 3), fill=(80, 185, 60))

    # Highlight on grass
    draw.rectangle((0, 2, size, 6), fill=(120, 230, 95, 100))

    return img


def process_tile(name, target_size=64, needs_transparency=False):
    """Process a tile image: resize and convert to proper PNG."""
    src = os.path.join(RESOURCES, "tiles", name)
    dst = os.path.join(OUTPUT, "tiles", name)
    print(f"  Processing tile: {name}")

    img = Image.open(src)
    if needs_transparency:
        img = remove_bg_smart(img)
    else:
        img = img.convert("RGBA")

    # Crop out any white border first
    if not needs_transparency:
        # For tiles, take the center portion avoiding rounded edges
        w, h = img.size
        margin = int(w * 0.08)  # 8% margin to cut rounded edges
        img = img.crop((margin, margin, w - margin, h - margin))

    img = img.resize((target_size, target_size), Image.LANCZOS)
    img.save(dst, "PNG")
    print(f"    -> Saved {target_size}x{target_size} PNG")


def process_background(name, target_w, target_h, needs_transparency=False):
    """Process a background image."""
    src = os.path.join(RESOURCES, "backgrounds", name)
    dst = os.path.join(OUTPUT, "backgrounds", name)
    print(f"  Processing background: {name}")

    img = Image.open(src)

    if needs_transparency:
        img = remove_background(img, threshold=235)
    else:
        img = img.convert("RGBA")

    img = img.resize((target_w, target_h), Image.LANCZOS)
    img.save(dst, "PNG")
    print(f"    -> Saved {target_w}x{target_h} PNG")


def process_object(name, target_size=64, needs_transparency=True):
    """Process an object image."""
    src = os.path.join(RESOURCES, "objects", name)
    dst = os.path.join(OUTPUT, "objects", name)
    print(f"  Processing object: {name}")

    img = Image.open(src)

    if needs_transparency:
        img = remove_bg_smart(img, tolerance=35)
        img = crop_to_content(img, padding=4)

    # Resize maintaining aspect ratio, center in target
    w, h = img.size
    scale = min(target_size / w, target_size / h) * 0.95
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))
    img = img.resize((new_w, new_h), Image.LANCZOS)

    result = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
    paste_x = (target_size - new_w) // 2
    paste_y = (target_size - new_h) // 2
    result.paste(img, (paste_x, paste_y), img if img.mode == "RGBA" else None)

    result.save(dst, "PNG")
    print(f"    -> Saved {target_size}x{target_size} PNG")


def process_particle(name, target_size=8):
    """Process a particle image."""
    src = os.path.join(RESOURCES, "particles", name)
    dst = os.path.join(OUTPUT, "particles", name)
    print(f"  Processing particle: {name}")

    img = Image.open(src)
    img = remove_background(img, threshold=230)
    img = crop_to_content(img, padding=0)

    if img.size[0] > 0 and img.size[1] > 0:
        img = img.resize((target_size, target_size), Image.LANCZOS)

    img.save(dst, "PNG")
    print(f"    -> Saved {target_size}x{target_size} PNG")


def main():
    print("=" * 60)
    print("MathBuilder Image Processing")
    print("=" * 60)

    ensure_dirs()

    # ── TILES ──────────────────────────────────────────────
    print("\n[1/8] Processing tiles...")

    # grass-top: The original is isometric 3D, create a proper side-scrolling tile
    print("  Creating grass-top tile (programmatic - original is isometric 3D)")
    grass = create_grass_tile(64)
    grass.save(os.path.join(OUTPUT, "tiles", "grass-top.png"), "PNG")
    print("    -> Saved 64x64 PNG")

    # dirt and stone: resize from originals (they look fine for side-scrolling)
    process_tile("dirt.png", 64)
    process_tile("stone.png", 64)

    # ── PLAYER SPRITES ─────────────────────────────────────
    print("\n[2/8] Processing player sprites...")

    # botty-idle: 4 frames -> 256x64
    print("  Processing botty-idle.png (4 frames)")
    src = Image.open(os.path.join(RESOURCES, "player", "botty-idle.png"))
    sheet = extract_sprites(src, 4, 64)
    sheet.save(os.path.join(OUTPUT, "player", "botty-idle.png"), "PNG")
    print(f"    -> Saved {sheet.width}x{sheet.height} PNG sprite sheet")

    # botty-walk: 6 frames -> 384x64
    print("  Processing botty-walk.png (6 frames)")
    src = Image.open(os.path.join(RESOURCES, "player", "botty-walk.png"))
    sheet = extract_sprites(src, 6, 64)
    sheet.save(os.path.join(OUTPUT, "player", "botty-walk.png"), "PNG")
    print(f"    -> Saved {sheet.width}x{sheet.height} PNG sprite sheet")

    # botty-jump: 2 frames -> 128x64
    print("  Processing botty-jump.png (2 frames)")
    src = Image.open(os.path.join(RESOURCES, "player", "botty-jump.png"))
    sheet = extract_sprites(src, 2, 64)
    sheet.save(os.path.join(OUTPUT, "player", "botty-jump.png"), "PNG")
    print(f"    -> Saved {sheet.width}x{sheet.height} PNG sprite sheet")

    # ── BACKGROUNDS ────────────────────────────────────────
    print("\n[3/8] Processing backgrounds...")
    process_background("sky.png", 800, 600, needs_transparency=False)
    process_background("clouds.png", 800, 200, needs_transparency=True)
    process_background("hills.png", 800, 200, needs_transparency=True)

    # ── UI ELEMENTS ────────────────────────────────────────
    print("\n[4/8] Processing UI elements...")

    # Buttons - create proper glossy buttons with text
    print("  Creating btn-play.png (glossy with text)")
    btn_play = create_button("PLAY", (76, 175, 80))  # Green
    btn_play.save(os.path.join(OUTPUT, "ui", "btn-play.png"), "PNG")
    print("    -> Saved 200x70 PNG")

    print("  Creating btn-levels.png (glossy with text)")
    btn_levels = create_button("LEVELS", (52, 152, 219))  # Blue
    btn_levels.save(os.path.join(OUTPUT, "ui", "btn-levels.png"), "PNG")
    print("    -> Saved 200x70 PNG")

    # Stars - create proper star shapes
    print("  Creating star-filled.png")
    star_f = create_star_filled(32)
    star_f.save(os.path.join(OUTPUT, "ui", "star-filled.png"), "PNG")
    print("    -> Saved 32x32 PNG")

    print("  Creating star-empty.png")
    star_e = create_star_empty(32)
    star_e.save(os.path.join(OUTPUT, "ui", "star-empty.png"), "PNG")
    print("    -> Saved 32x32 PNG")

    # Math input background
    print("  Creating math-input-bg.png")
    math_bg = create_math_input_bg(400, 250)
    math_bg.save(os.path.join(OUTPUT, "ui", "math-input-bg.png"), "PNG")
    print("    -> Saved 400x250 PNG")

    # Arrow buttons - create proper ones with visible arrows
    for direction in ["left", "right", "jump"]:
        name = f"arrow-{direction}.png"
        print(f"  Creating {name}")
        arrow = create_arrow_button(direction, 64)
        arrow.save(os.path.join(OUTPUT, "ui", name), "PNG")
        print(f"    -> Saved 64x64 PNG")

    # ── OBJECTS ────────────────────────────────────────────
    print("\n[5/8] Processing objects...")
    process_object("flag.png", 64, needs_transparency=True)
    process_object("bridge-block.png", 64, needs_transparency=False)

    # ── PARTICLES ──────────────────────────────────────────
    print("\n[6/8] Processing particles...")
    process_particle("dust.png", 8)
    process_particle("confetti.png", 8)

    # ── VERIFICATION ───────────────────────────────────────
    print("\n[7/8] Verifying outputs...")
    expected = {
        "tiles/grass-top.png": (64, 64),
        "tiles/dirt.png": (64, 64),
        "tiles/stone.png": (64, 64),
        "player/botty-idle.png": (256, 64),
        "player/botty-walk.png": (384, 64),
        "player/botty-jump.png": (128, 64),
        "backgrounds/sky.png": (800, 600),
        "backgrounds/clouds.png": (800, 200),
        "backgrounds/hills.png": (800, 200),
        "ui/btn-play.png": (200, 70),
        "ui/btn-levels.png": (200, 70),
        "ui/star-filled.png": (32, 32),
        "ui/star-empty.png": (32, 32),
        "ui/math-input-bg.png": (400, 250),
        "ui/arrow-left.png": (64, 64),
        "ui/arrow-right.png": (64, 64),
        "ui/arrow-jump.png": (64, 64),
        "objects/flag.png": (64, 64),
        "objects/bridge-block.png": (64, 64),
        "particles/dust.png": (8, 8),
        "particles/confetti.png": (8, 8),
    }

    all_ok = True
    for path, (exp_w, exp_h) in expected.items():
        full_path = os.path.join(OUTPUT, path)
        if not os.path.exists(full_path):
            print(f"  MISSING: {path}")
            all_ok = False
            continue
        img = Image.open(full_path)
        w, h = img.size
        fmt = img.format
        status = "OK" if (w == exp_w and h == exp_h) else f"WRONG SIZE ({w}x{h})"
        if w != exp_w or h != exp_h:
            all_ok = False
        print(f"  {status}: {path} ({w}x{h}, {fmt})")

    print(f"\n[8/8] Summary")
    print(f"  Total assets: {len(expected)}")
    if all_ok:
        print("  All assets processed correctly!")
    else:
        print("  Some assets need attention (see above)")

    print(f"\n  Output directory: {OUTPUT}")
    print("  Done!")


if __name__ == "__main__":
    main()
