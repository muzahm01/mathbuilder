#!/usr/bin/env python3
"""
Final fix: Use color-based extraction for Botty sprites.
Botty is a blue robot, so we keep blue-dominant pixels and
remove the grey checkerboard pattern.
"""

from PIL import Image, ImageFilter
import os

RESOURCES = "/home/user/mathbuilder/resources"
OUTPUT = "/home/user/mathbuilder/public/assets/images"


def extract_blue_character(img):
    """
    Extract the blue character from a JPEG with fake checkerboard bg.
    Botty is blue, so we keep pixels where blue is dominant or
    the pixel has significant color saturation (not grey).
    """
    img = img.convert("RGBA")
    pixels = img.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]

            # Calculate color properties
            max_c = max(r, g, b)
            min_c = min(r, g, b)
            saturation = max_c - min_c  # How "colorful" the pixel is
            brightness = (r + g + b) / 3

            # Keep pixel if it's colorful (saturated) -- this is the character
            if saturation > 25:
                # It's a colored pixel, keep it
                continue

            # Grey/white/neutral pixel -- make transparent
            pixels[x, y] = (r, g, b, 0)

    return img


def find_sprites_by_columns(img, num_sprites, min_span_width=20):
    """Find sprite bounding boxes by scanning columns for opaque pixels."""
    pixels = img.load()
    w, h = img.size

    # Build column alpha profile
    col_content = []
    for x in range(w):
        has = any(pixels[x, y][3] > 50 for y in range(h))
        col_content.append(has)

    # Find content spans
    spans = []
    in_span = False
    start = 0
    for x in range(w):
        if col_content[x] and not in_span:
            start = x
            in_span = True
        elif not col_content[x] and in_span:
            if x - start >= min_span_width:
                spans.append((start, x))
            in_span = False
    if in_span and w - start >= min_span_width:
        spans.append((start, w))

    # Merge spans with small gaps (< 10px)
    merged = [spans[0]] if spans else []
    for s, e in spans[1:]:
        if s - merged[-1][1] < 10:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))

    print(f"    Found {len(merged)} content spans: {merged}")

    # Adjust to desired count
    while len(merged) > num_sprites:
        min_gap = float('inf')
        min_idx = 0
        for i in range(len(merged) - 1):
            gap = merged[i + 1][0] - merged[i][1]
            if gap < min_gap:
                min_gap = gap
                min_idx = i
        merged[min_idx] = (merged[min_idx][0], merged[min_idx + 1][1])
        merged.pop(min_idx + 1)

    while len(merged) < num_sprites:
        widths = [(e - s, i) for i, (s, e) in enumerate(merged)]
        widths.sort(reverse=True)
        idx = widths[0][1]
        s, e = merged[idx]
        mid = (s + e) // 2
        merged[idx] = (s, mid)
        merged.insert(idx + 1, (mid, e))

    # Get vertical bounds
    bboxes = []
    for sx, ex in merged:
        top = h
        bottom = 0
        for x in range(sx, ex):
            for y in range(h):
                if pixels[x, y][3] > 50:
                    top = min(top, y)
                    break
            for y in range(h - 1, -1, -1):
                if pixels[x, y][3] > 50:
                    bottom = max(bottom, y + 1)
                    break
        bboxes.append((sx, top, ex, bottom))

    return bboxes


def make_sheet(src_path, num_frames, target_size=64):
    """Create a proper sprite sheet from a source image."""
    print(f"  Processing {os.path.basename(src_path)} ({num_frames} frames)...")
    img = Image.open(src_path)

    # Extract blue character
    clean = extract_blue_character(img)

    # Find sprites
    bboxes = find_sprites_by_columns(clean, num_frames)
    print(f"    Bounding boxes: {bboxes}")

    frames = []
    for left, top, right, bottom in bboxes:
        pad = 2
        sprite = clean.crop((
            max(0, left - pad),
            max(0, top - pad),
            min(clean.width, right + pad),
            min(clean.height, bottom + pad)
        ))

        sw, sh = sprite.size
        if sw < 5 or sh < 5:
            frames.append(Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0)))
            continue

        # Scale to fill 85% of frame
        scale = min(
            (target_size * 0.85) / sw,
            (target_size * 0.85) / sh
        )
        new_w = max(1, int(sw * scale))
        new_h = max(1, int(sh * scale))
        sprite = sprite.resize((new_w, new_h), Image.LANCZOS)

        # Center in frame, bottom-aligned
        frame = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
        px = (target_size - new_w) // 2
        py = target_size - new_h - 2
        frame.paste(sprite, (px, py), sprite)
        frames.append(frame)

    # Stitch into horizontal strip
    sheet = Image.new("RGBA", (target_size * num_frames, target_size), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * target_size, 0), f)

    return sheet


def fix_hills():
    """Fix hills: use color extraction (keep green, remove grey)."""
    print("\n  Fixing hills.png...")
    img = Image.open(os.path.join(RESOURCES, "backgrounds", "hills.png")).convert("RGBA")
    pixels = img.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            max_c = max(r, g, b)
            min_c = min(r, g, b)
            saturation = max_c - min_c

            # Keep colored (green) pixels, remove grey/neutral
            if saturation < 20:
                pixels[x, y] = (r, g, b, 0)
            # Also handle transition pixels: apply partial transparency
            # for softer edges
            elif saturation < 35:
                alpha = int(255 * (saturation - 20) / 15)
                pixels[x, y] = (r, g, b, alpha)

    # Crop to content and resize
    bbox = img.getbbox()
    if bbox:
        content = img.crop((0, bbox[1], w, h))
    else:
        content = img

    result = content.resize((800, 200), Image.LANCZOS)
    result.save(os.path.join(OUTPUT, "backgrounds", "hills.png"), "PNG")
    print(f"    -> Saved 800x200 PNG with transparency")


def main():
    print("=" * 50)
    print("Final fixes: color-based sprite extraction")
    print("=" * 50)

    # Walk sprite
    sheet = make_sheet(os.path.join(RESOURCES, "player", "botty-walk.png"), 6, 64)
    sheet.save(os.path.join(OUTPUT, "player", "botty-walk.png"), "PNG")
    print(f"  -> Saved {sheet.width}x{sheet.height}")

    # Jump sprite
    sheet = make_sheet(os.path.join(RESOURCES, "player", "botty-jump.png"), 2, 64)
    sheet.save(os.path.join(OUTPUT, "player", "botty-jump.png"), "PNG")
    print(f"  -> Saved {sheet.width}x{sheet.height}")

    # Hills
    fix_hills()

    # Verify all final outputs
    print("\n--- Final Verification ---")
    checks = {
        "player/botty-idle.png": (256, 64),
        "player/botty-walk.png": (384, 64),
        "player/botty-jump.png": (128, 64),
        "backgrounds/hills.png": (800, 200),
    }
    for path, (ew, eh) in checks.items():
        full = os.path.join(OUTPUT, path)
        img = Image.open(full)
        status = "OK" if img.size == (ew, eh) else f"WRONG {img.size}"
        has_alpha = img.mode == "RGBA"
        # Check if there are actually transparent pixels
        if has_alpha:
            alpha_vals = list(img.getdata(band=3))
            transparent_pct = sum(1 for a in alpha_vals if a < 128) / len(alpha_vals) * 100
        else:
            transparent_pct = 0
        print(f"  {status}: {path} ({img.size[0]}x{img.size[1]}, {transparent_pct:.0f}% transparent)")

    print("\nDone!")


if __name__ == "__main__":
    main()
