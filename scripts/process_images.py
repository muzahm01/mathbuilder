#!/usr/bin/env python3
"""
MathBuilder Image Processing Script — Modern 3D Style
=====================================================
Processes raw Gemini-generated images in resources/ into game-ready assets
in public/assets/images/ with correct dimensions, format, and transparency.

All programmatic assets use modern 3D rendering techniques:
- Multi-layer gradients for depth
- Ambient occlusion simulation
- Specular highlights and rim lighting
- Glass-morphism and PBR-inspired materials
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import os
import math
import random

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


def draw_star_points(cx, cy, outer_r, inner_r, rotation=0):
    """Generate 5-pointed star polygon points centered at (cx, cy)."""
    points = []
    for i in range(10):
        angle = math.radians(i * 36 - 90 + rotation)
        r = outer_r if i % 2 == 0 else inner_r
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return points


def create_star_filled(size=32):
    """Create a modern 3D metallic gold star with specular highlights and depth."""
    # Work at 4x for smooth anti-aliasing
    s = size * 4
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = s // 2, s // 2 + 2
    outer_r = s // 2 - 6
    inner_r = outer_r * 0.38

    # Drop shadow
    shadow_pts = draw_star_points(cx + 3, cy + 4, outer_r, inner_r)
    draw.polygon(shadow_pts, fill=(80, 50, 0, 80))

    # Apply blur to shadow
    shadow_layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)
    sd.polygon(shadow_pts, fill=(80, 50, 0, 70))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(4))
    img = Image.alpha_composite(img, shadow_layer)
    draw = ImageDraw.Draw(img)

    # Dark base (bottom/shadow side of 3D star)
    base_pts = draw_star_points(cx + 1, cy + 2, outer_r, inner_r)
    draw.polygon(base_pts, fill=(180, 120, 0, 255))

    # Main gold body
    main_pts = draw_star_points(cx, cy, outer_r, inner_r)
    draw.polygon(main_pts, fill=(255, 200, 20, 255), outline=(200, 145, 0, 255))

    # Upper gradient overlay (lighter gold, simulating light from top-left)
    upper_pts = draw_star_points(cx - 1, cy - 1, outer_r - 3, inner_r - 1)
    draw.polygon(upper_pts, fill=(255, 225, 60, 200))

    # Specular highlight band (bright streak across upper portion)
    highlight_pts = draw_star_points(cx - 2, cy - 3, outer_r - 6, inner_r - 2)
    draw.polygon(highlight_pts, fill=(255, 245, 140, 150))

    # Hot specular spot (bright white-gold point)
    spot_r = int(outer_r * 0.2)
    draw.ellipse((cx - spot_r - 6, cy - spot_r - 8,
                  cx + spot_r - 6, cy + spot_r - 8),
                 fill=(255, 255, 220, 200))

    # Tiny sparkle/lens flare on top point
    sparkle_y = cy - outer_r + 2
    draw.line([(cx - 4, sparkle_y), (cx + 4, sparkle_y)], fill=(255, 255, 255, 200), width=1)
    draw.line([(cx, sparkle_y - 4), (cx, sparkle_y + 4)], fill=(255, 255, 255, 200), width=1)

    # Rim light on right edge
    rim_pts = draw_star_points(cx + 2, cy, outer_r - 1, inner_r)
    rim_img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rim_img)
    rd.polygon(rim_pts, fill=(255, 240, 180, 60))
    img = Image.alpha_composite(img, rim_img)

    img = img.resize((size, size), Image.LANCZOS)
    return img


def create_star_empty(size=32):
    """Create a modern 3D brushed silver empty star with subtle depth."""
    s = size * 4
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = s // 2, s // 2 + 2
    outer_r = s // 2 - 6
    inner_r = outer_r * 0.38

    # Soft shadow
    shadow_layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)
    shadow_pts = draw_star_points(cx + 2, cy + 3, outer_r, inner_r)
    sd.polygon(shadow_pts, fill=(0, 0, 0, 40))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(3))
    img = Image.alpha_composite(img, shadow_layer)
    draw = ImageDraw.Draw(img)

    # Dark edge (3D thickness)
    base_pts = draw_star_points(cx + 1, cy + 2, outer_r, inner_r)
    draw.polygon(base_pts, fill=(100, 105, 115, 255))

    # Main silver body
    main_pts = draw_star_points(cx, cy, outer_r, inner_r)
    draw.polygon(main_pts, fill=(155, 160, 175, 255), outline=(115, 120, 135, 255))

    # Upper highlight (brushed metal feel)
    upper_pts = draw_star_points(cx - 1, cy - 1, outer_r - 3, inner_r - 1)
    draw.polygon(upper_pts, fill=(180, 185, 200, 160))

    # Subtle specular
    spec_pts = draw_star_points(cx - 2, cy - 3, outer_r - 8, inner_r - 3)
    draw.polygon(spec_pts, fill=(200, 205, 215, 100))

    # Inner bevel (recessed center)
    inner_pts = draw_star_points(cx, cy + 1, outer_r - 10, inner_r - 3)
    draw.polygon(inner_pts, fill=(130, 135, 150, 100))

    img = img.resize((size, size), Image.LANCZOS)
    return img


def create_button(text, base_color, width=200, height=70):
    """
    Create a modern 3D-style glossy button with PBR-inspired materials.
    Features: 3D extrusion, specular highlights, environment reflection,
    soft drop shadow, and beveled text.
    """
    # Work at 2x for anti-aliasing
    w, h = width * 2, height * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    r, g, b = base_color
    radius = h // 2

    # ── Soft blurred drop shadow ──
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        (8, 14, w - 4, h - 2),
        radius=radius,
        fill=(int(r * 0.15), int(g * 0.15), int(b * 0.15), 120)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)

    # ── 3D extrusion (visible thickness on bottom and right) ──
    for offset in range(6, 0, -1):
        darkness = 0.4 + (6 - offset) * 0.05
        draw.rounded_rectangle(
            (4 + offset, 4 + offset + 2, w - 4 + offset // 2, h - 6 + offset),
            radius=radius,
            fill=(int(r * darkness), int(g * darkness), int(b * darkness), 255)
        )

    # ── Main button body ──
    # Bottom half (darker)
    draw.rounded_rectangle(
        (4, 4, w - 4, h - 8),
        radius=radius,
        fill=(int(r * 0.8), int(g * 0.8), int(b * 0.8), 255)
    )

    # Upper half gradient (brighter, main color)
    draw.rounded_rectangle(
        (4, 4, w - 4, h // 2 + 10),
        radius=radius,
        fill=(r, g, b, 255)
    )

    # ── Specular highlight streak (glossy top surface) ──
    draw.rounded_rectangle(
        (12, 6, w - 12, h // 3 + 4),
        radius=radius - 6,
        fill=(min(255, r + 50), min(255, g + 50), min(255, b + 50), 180)
    )

    # Hot specular line (sharp bright edge near top)
    draw.rounded_rectangle(
        (20, 8, w - 20, 18),
        radius=6,
        fill=(min(255, r + 100), min(255, g + 100), min(255, b + 100), 120)
    )

    # ── Environment reflection (subtle bright band in lower third) ──
    draw.rounded_rectangle(
        (16, h // 2 + 4, w - 16, h // 2 + 14),
        radius=4,
        fill=(min(255, r + 30), min(255, g + 30), min(255, b + 30), 50)
    )

    # ── Border with subtle inner glow ──
    draw.rounded_rectangle(
        (4, 4, w - 4, h - 8),
        radius=radius,
        outline=(int(r * 0.4), int(g * 0.4), int(b * 0.4), 255),
        width=3
    )
    # Inner highlight border
    draw.rounded_rectangle(
        (7, 7, w - 7, h - 11),
        radius=radius - 3,
        outline=(min(255, r + 40), min(255, g + 40), min(255, b + 40), 60),
        width=1
    )

    # ── Text with 3D bevel effect ──
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (w - tw) // 2
    ty = (h - th) // 2 - 6

    # Text extrusion shadow (3D depth)
    for offset in range(4, 0, -1):
        alpha = int(60 + (4 - offset) * 20)
        draw.text((tx + offset, ty + offset + 2), text,
                  fill=(0, 0, 0, alpha), font=font)

    # Text body (white)
    draw.text((tx, ty), text, fill=(255, 255, 255, 255), font=font)

    # Text specular highlight (bright top edge)
    draw.text((tx, ty - 1), text, fill=(255, 255, 255, 60), font=font)

    # Downscale
    img = img.resize((width, height), Image.LANCZOS)
    return img


def create_arrow_button(direction, size=64):
    """
    Create a modern glass-morphism touch control button with 3D depth,
    soft glow ring, frosted glass effect, and beveled arrow icon.
    """
    # Work at 4x for smooth anti-aliasing
    s = size * 4
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = s // 2, s // 2
    pad = 8

    # ── Outer glow ring (subtle neon-like) ──
    glow = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((pad - 4, pad - 4, s - pad + 4, s - pad + 4),
               fill=(120, 160, 220, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # ── Glass body (frosted dark background) ──
    # Outer ring
    draw.ellipse((pad, pad, s - pad, s - pad),
                 fill=(25, 35, 55, 180),
                 outline=(80, 110, 160, 200), width=3)

    # Inner gradient (lighter at top for 3D dome effect)
    inner_pad = pad + 6
    draw.ellipse((inner_pad, inner_pad, s - inner_pad, s - inner_pad),
                 fill=(40, 55, 80, 140))

    # Upper specular highlight (glass reflection)
    highlight = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    hd = ImageDraw.Draw(highlight)
    # Create an elliptical highlight in the upper portion
    hx1, hy1 = int(s * 0.25), int(s * 0.12)
    hx2, hy2 = int(s * 0.75), int(s * 0.45)
    hd.ellipse((hx1, hy1, hx2, hy2), fill=(140, 170, 220, 50))
    highlight = highlight.filter(ImageFilter.GaussianBlur(6))
    img = Image.alpha_composite(img, highlight)
    draw = ImageDraw.Draw(img)

    # ── Arrow icon with 3D bevel ──
    arrow_s = s // 5  # Arrow size

    if direction == "left":
        points = [(cx + arrow_s, cy - arrow_s), (cx - arrow_s, cy), (cx + arrow_s, cy + arrow_s)]
    elif direction == "right":
        points = [(cx - arrow_s, cy - arrow_s), (cx + arrow_s, cy), (cx - arrow_s, cy + arrow_s)]
    elif direction == "jump":
        points = [(cx - arrow_s, cy + arrow_s // 2), (cx, cy - arrow_s), (cx + arrow_s, cy + arrow_s // 2)]

    # Arrow shadow (depth)
    shadow_pts = [(x + 2, y + 3) for x, y in points]
    draw.polygon(shadow_pts, fill=(0, 0, 0, 80))

    # Arrow body (bright white)
    draw.polygon(points, fill=(235, 240, 255, 240))

    # Arrow highlight (top edge brighter)
    highlight_pts = [(x - 1, y - 1) for x, y in points]
    draw.polygon(highlight_pts, fill=(255, 255, 255, 60))

    # ── Bottom rim light (subtle edge glow) ──
    rim = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rim)
    rd.arc((pad + 2, pad + 2, s - pad - 2, s - pad - 2),
           start=30, end=150, fill=(100, 140, 200, 60), width=2)
    img = Image.alpha_composite(img, rim)

    img = img.resize((size, size), Image.LANCZOS)
    return img


def create_math_input_bg(width=400, height=250):
    """
    Create a modern 3D glass-morphism math input panel with PBR-inspired materials.
    Features: frosted glass effect, 3D depth/extrusion, recessed input area,
    soft ambient occlusion, and warm inner glow.
    """
    # Work at 2x for anti-aliasing
    w, h = width * 2, height * 2
    result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    radius = 40

    # ── Soft blurred drop shadow ──
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        (20, 26, w - 8, h - 4),
        radius=radius,
        fill=(20, 40, 80, 60)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    result = Image.alpha_composite(result, shadow)

    # ── 3D extrusion (visible thickness at bottom and right) ──
    panel = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    for offset in range(8, 0, -1):
        darkness = int(50 + offset * 8)
        pd.rounded_rectangle(
            (16 + offset, 16 + offset + 2, w - 16 + offset // 2, h - 16 + offset),
            radius=radius,
            fill=(darkness, int(darkness * 1.2), int(darkness * 1.6), 200)
        )
    result = Image.alpha_composite(result, panel)

    # ── Main panel body (glass-morphism gradient) ──
    body = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)

    # Base panel color
    bd.rounded_rectangle(
        (16, 16, w - 16, h - 16),
        radius=radius,
        fill=(210, 225, 250, 235)
    )

    # Upper gradient (lighter, simulating light from above)
    bd.rounded_rectangle(
        (16, 16, w - 16, h // 2 + 20),
        radius=radius,
        fill=(230, 240, 255, 240)
    )

    # Specular highlight streak at top
    bd.rounded_rectangle(
        (30, 20, w - 30, 50),
        radius=15,
        fill=(255, 255, 255, 60)
    )

    result = Image.alpha_composite(result, body)

    # ── Border with 3D depth ──
    border = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    brd = ImageDraw.Draw(border)
    # Outer border (darker)
    brd.rounded_rectangle(
        (16, 16, w - 16, h - 16),
        radius=radius,
        outline=(60, 120, 200, 255),
        width=5
    )
    # Inner highlight border
    brd.rounded_rectangle(
        (22, 22, w - 22, h - 22),
        radius=radius - 4,
        outline=(140, 190, 255, 80),
        width=2
    )
    result = Image.alpha_composite(result, border)

    # ── Recessed input area (sunken 3D effect) ──
    input_area = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ia = ImageDraw.Draw(input_area)
    inner_y = h // 2 - 50
    inner_h = 100

    # Inset shadow (top and left darker = recessed)
    ia.rounded_rectangle(
        (76, inner_y - 2, w - 76, inner_y + inner_h + 2),
        radius=18,
        fill=(40, 70, 120, 40)
    )
    # White input background
    ia.rounded_rectangle(
        (80, inner_y, w - 80, inner_y + inner_h),
        radius=16,
        fill=(255, 255, 255, 250)
    )
    # Bottom highlight of inset (light coming from below = recessed)
    ia.rounded_rectangle(
        (82, inner_y + inner_h - 6, w - 82, inner_y + inner_h - 2),
        radius=4,
        fill=(220, 235, 255, 60)
    )
    # Inset border
    ia.rounded_rectangle(
        (80, inner_y, w - 80, inner_y + inner_h),
        radius=16,
        outline=(70, 130, 210, 160),
        width=2
    )
    result = Image.alpha_composite(result, input_area)

    # ── Subtle inner glow around edges ──
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle(
        (20, 20, w - 20, h - 20),
        radius=radius - 2,
        outline=(100, 160, 255, 30),
        width=6
    )
    glow = glow.filter(ImageFilter.GaussianBlur(4))
    result = Image.alpha_composite(result, glow)

    # ── Ambient occlusion at bottom edge ──
    ao = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    aod = ImageDraw.Draw(ao)
    aod.rounded_rectangle(
        (20, h - 50, w - 20, h - 16),
        radius=20,
        fill=(30, 50, 90, 25)
    )
    ao = ao.filter(ImageFilter.GaussianBlur(6))
    result = Image.alpha_composite(result, ao)

    result = result.resize((width, height), Image.LANCZOS)
    return result


def create_grass_tile(size=64):
    """
    Create a modern 3D-style grass tile with depth, ambient occlusion,
    volumetric grass blades, and layered dirt with embedded stones.
    """
    # Work at 2x resolution for anti-aliasing, then downscale
    s = size * 2
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ── DIRT BODY with layered depth ──
    # Base warm dirt color
    for y in range(s):
        # Vertical gradient: lighter near top (near grass), darker at bottom
        t = y / s
        r = int(155 - t * 30 + math.sin(y * 0.3) * 8)
        g = int(110 - t * 25 + math.sin(y * 0.4 + 1) * 6)
        b = int(65 - t * 15 + math.sin(y * 0.5 + 2) * 4)
        draw.line([(0, y), (s, y)], fill=(r, g, b, 255))

    # Horizontal sediment layers with ambient occlusion
    layer_positions = [30, 48, 65, 82, 100, 115]
    for ly in layer_positions:
        ly2 = int(ly * s / 128)
        # Dark line (crack/shadow between layers)
        draw.line([(0, ly2), (s, ly2)], fill=(90, 60, 35, 140), width=2)
        # Ambient occlusion below crack
        draw.line([(0, ly2 + 2), (s, ly2 + 2)], fill=(80, 55, 30, 60), width=1)
        # Light edge above crack (rim light)
        draw.line([(0, ly2 - 1), (s, ly2 - 1)], fill=(175, 130, 85, 80), width=1)

    # Embedded stones with 3D shading
    random.seed(42)  # Deterministic for reproducibility
    stones = [(20, 55, 14), (70, 45, 10), (16, 90, 12), (90, 80, 11),
              (55, 70, 9), (100, 105, 13), (35, 110, 8)]
    for sx, sy, sr in stones:
        sx2, sy2, sr2 = int(sx * s / 128), int(sy * s / 128), int(sr * s / 128)
        # Stone shadow (ambient occlusion)
        draw.ellipse((sx2 - sr2 + 2, sy2 - sr2 + 2, sx2 + sr2 + 2, sy2 + sr2 + 2),
                     fill=(70, 45, 25, 80))
        # Stone body
        draw.ellipse((sx2 - sr2, sy2 - sr2, sx2 + sr2, sy2 + sr2),
                     fill=(120, 95, 65, 255))
        # Stone highlight (specular)
        draw.ellipse((sx2 - sr2 + 2, sy2 - sr2 + 1, sx2 - sr2 + sr2, sy2 - sr2 + sr2 // 2 + 1),
                     fill=(150, 120, 85, 100))

    # Small root-like details
    draw.line([(15 * s // 64, 42 * s // 64), (22 * s // 64, 48 * s // 64)],
             fill=(100, 75, 40, 100), width=1)
    draw.line([(50 * s // 64, 55 * s // 64), (58 * s // 64, 52 * s // 64)],
             fill=(100, 75, 40, 100), width=1)

    # ── GRASS LAYER with 3D depth ──
    grass_h = int(22 * s / 64)

    # Grass base layer (dark green at bottom of grass zone)
    for y in range(grass_h + 8):
        t = y / (grass_h + 8)
        r = int(55 + t * 35)
        g = int(140 + t * 55)
        b = int(35 + t * 30)
        draw.line([(0, y), (s, y)], fill=(r, g, b, 255))

    # Wavy transition edge (grass meets dirt) with ambient occlusion
    for x in range(0, s, 2):
        wave = int(4 * math.sin(x * 0.15) + 2 * math.sin(x * 0.3 + 1))
        base_y = grass_h + wave

        # Ambient occlusion shadow below grass edge
        for dy in range(6):
            alpha = int(120 * (1 - dy / 6))
            draw.point((x, base_y + dy), fill=(40, 60, 20, alpha))
            if x + 1 < s:
                draw.point((x + 1, base_y + dy), fill=(40, 60, 20, alpha))

        # Grass drip (irregular edge)
        drip_len = int(3 + 2 * math.sin(x * 0.4 + 0.7))
        for dy in range(drip_len):
            alpha = int(255 * (1 - dy / drip_len))
            draw.point((x, base_y - dy), fill=(70, 160, 45, alpha))

    # Individual grass blades (3D tufts)
    blade_positions = list(range(0, s, 3))
    for bx in blade_positions:
        blade_h = int(6 + 4 * math.sin(bx * 0.2 + 0.5))
        lean = int(2 * math.sin(bx * 0.3))
        # Dark blade (shadow side)
        for dy in range(blade_h):
            t = dy / blade_h
            px = bx + int(lean * t)
            py = int(4 + (1 - t) * blade_h)
            if 0 <= px < s and 0 <= py < s:
                g_val = int(130 + t * 80)
                draw.point((px, py), fill=(50, g_val, 30, int(200 + t * 55)))
        # Light blade (highlight side)
        if bx + 1 < s:
            for dy in range(blade_h - 1):
                t = dy / blade_h
                px = bx + 1 + int(lean * t)
                py = int(4 + (1 - t) * blade_h)
                if 0 <= px < s and 0 <= py < s:
                    g_val = int(170 + t * 60)
                    draw.point((px, py), fill=(80, g_val, 45, int(160 + t * 55)))

    # Top specular highlight (light hitting the grass canopy)
    highlight = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    hd = ImageDraw.Draw(highlight)
    for y in range(8):
        alpha = int(80 * (1 - y / 8))
        hd.line([(0, y + 2), (s, y + 2)], fill=(180, 255, 140, alpha))
    img = Image.alpha_composite(img, highlight)

    # ── LEFT EDGE ambient occlusion (subtle) ──
    ao = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    aod = ImageDraw.Draw(ao)
    for x in range(6):
        alpha = int(30 * (1 - x / 6))
        aod.line([(x, 0), (x, s)], fill=(0, 0, 0, alpha))
    img = Image.alpha_composite(img, ao)

    # Downscale to target size with high-quality resampling
    img = img.resize((size, size), Image.LANCZOS)
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
