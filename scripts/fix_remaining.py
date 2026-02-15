#!/usr/bin/env python3
"""
Fix remaining issues: walk/jump sprites and hills transparency.

The source images are JPEGs with a "fake" checkerboard pattern that
simulates transparency. We need to detect and remove this pattern.
"""

from PIL import Image, ImageFilter
import os
# numpy not needed

RESOURCES = "/home/user/mathbuilder/resources"
OUTPUT = "/home/user/mathbuilder/public/assets/images"


def analyze_checkerboard(img):
    """Detect the checkerboard pattern colors in a JPEG with fake transparency."""
    pixels = img.load()
    w, h = img.size

    # Sample the corners and edges to find checkerboard colors
    light_samples = []
    dark_samples = []

    for y in range(0, min(20, h)):
        for x in range(0, min(20, w)):
            r, g, b = pixels[x, y][:3]
            brightness = (r + g + b) / 3
            if brightness > 170:
                light_samples.append((r, g, b))
            elif 100 < brightness < 170:
                dark_samples.append((r, g, b))

    if light_samples:
        avg_light = tuple(sum(c) // len(light_samples) for c in zip(*light_samples))
    else:
        avg_light = (204, 204, 204)

    if dark_samples:
        avg_dark = tuple(sum(c) // len(dark_samples) for c in zip(*dark_samples))
    else:
        avg_dark = (153, 153, 153)

    return avg_light, avg_dark


def remove_checkerboard_bg(img, extra_threshold=45):
    """
    Remove the checkerboard transparency pattern from a JPEG image.
    Also removes white/near-white pixels.
    """
    img = img.convert("RGBA")
    pixels = img.load()
    w, h = img.size

    # Detect checkerboard colors
    light, dark = analyze_checkerboard(img)
    print(f"    Checkerboard light={light}, dark={dark}")

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]

            # Check if pixel matches checkerboard light square
            if (abs(r - light[0]) < extra_threshold and
                abs(g - light[1]) < extra_threshold and
                abs(b - light[2]) < extra_threshold):
                pixels[x, y] = (r, g, b, 0)
                continue

            # Check if pixel matches checkerboard dark square
            if (abs(r - dark[0]) < extra_threshold and
                abs(g - dark[1]) < extra_threshold and
                abs(b - dark[2]) < extra_threshold):
                pixels[x, y] = (r, g, b, 0)
                continue

            # Also remove white/near-white
            if r > 235 and g > 235 and b > 235:
                pixels[x, y] = (r, g, b, 0)
                continue

            # Grey pixels that are neutral (not colored)
            if abs(r - g) < 12 and abs(g - b) < 12 and r > 140 and r < 220:
                pixels[x, y] = (r, g, b, 0)

    return img


def find_sprites_in_clean(img, num_sprites):
    """Find sprite bounding boxes in a cleaned (bg removed) image."""
    pixels = img.load()
    w, h = img.size

    # Horizontal content detection
    x_has_content = []
    for x in range(w):
        has = False
        for y in range(h):
            if pixels[x, y][3] > 50:
                has = True
                break
        x_has_content.append(has)

    # Find spans
    spans = []
    in_span = False
    start = 0
    for x in range(w):
        if x_has_content[x] and not in_span:
            start = x
            in_span = True
        elif not x_has_content[x] and in_span:
            spans.append((start, x))
            in_span = False
    if in_span:
        spans.append((start, w))

    # Merge small gaps (< 5px)
    merged = [spans[0]] if spans else []
    for s, e in spans[1:]:
        if s - merged[-1][1] < 5:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))

    # Filter out tiny noise spans (< 15px wide)
    merged = [(s, e) for s, e in merged if e - s > 15]

    print(f"    Found {len(merged)} content spans (need {num_sprites})")

    # Adjust count
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

    # Get vertical bounds per sprite
    bboxes = []
    for sx, ex in merged:
        top = h
        bottom = 0
        for x in range(sx, ex):
            for y in range(h):
                if pixels[x, y][3] > 50:
                    top = min(top, y)
                    bottom = max(bottom, y + 1)
                    break
            for y in range(h - 1, -1, -1):
                if pixels[x, y][3] > 50:
                    bottom = max(bottom, y + 1)
                    break
        bboxes.append((sx, top, ex, bottom))

    return bboxes


def extract_stitch(src_path, num_frames, target_size=64):
    """Extract sprites and create proper sprite sheet."""
    print(f"  Loading {os.path.basename(src_path)}...")
    img = Image.open(src_path)

    # Remove checkerboard background
    clean = remove_checkerboard_bg(img)

    # Find sprites
    bboxes = find_sprites_in_clean(clean, num_frames)
    print(f"    Bounding boxes: {bboxes}")

    frames = []
    for left, top, right, bottom in bboxes:
        # Extract with small padding
        pad = 3
        sprite = clean.crop((
            max(0, left - pad),
            max(0, top - pad),
            min(clean.width, right + pad),
            min(clean.height, bottom + pad)
        ))

        sw, sh = sprite.size
        if sw == 0 or sh == 0:
            frames.append(Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0)))
            continue

        # Scale to fill frame (85% height)
        fill = 0.85
        scale = min(
            (target_size * fill) / sw,
            (target_size * fill) / sh
        )
        new_w = max(1, int(sw * scale))
        new_h = max(1, int(sh * scale))
        sprite = sprite.resize((new_w, new_h), Image.LANCZOS)

        # Center horizontally, align to bottom
        frame = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
        paste_x = (target_size - new_w) // 2
        paste_y = target_size - new_h - 2
        frame.paste(sprite, (paste_x, paste_y), sprite)
        frames.append(frame)

    # Stitch
    sheet = Image.new("RGBA", (target_size * num_frames, target_size), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * target_size, 0), f)

    return sheet


def fix_hills():
    """Fix hills.png transparency."""
    print("\n  Fixing hills.png...")
    img = Image.open(os.path.join(RESOURCES, "backgrounds", "hills.png"))

    # Remove checkerboard/white background
    clean = remove_checkerboard_bg(img, extra_threshold=40)

    # The hills should be in the bottom portion
    # Crop to the content area
    bbox = clean.getbbox()
    if bbox:
        # Keep full width, crop vertically to content
        content = clean.crop((0, bbox[1], clean.width, clean.height))
    else:
        content = clean

    # Resize to 800x200
    result = content.resize((800, 200), Image.LANCZOS)
    result.save(os.path.join(OUTPUT, "backgrounds", "hills.png"), "PNG")
    print(f"    -> Saved 800x200 PNG")


def main():
    print("=" * 50)
    print("Fixing walk/jump sprites and hills")
    print("=" * 50)

    # Fix walk sprite
    print("\n--- botty-walk.png ---")
    sheet = extract_stitch(
        os.path.join(RESOURCES, "player", "botty-walk.png"), 6, 64
    )
    sheet.save(os.path.join(OUTPUT, "player", "botty-walk.png"), "PNG")
    print(f"  -> Final: {sheet.width}x{sheet.height}")

    # Fix jump sprite
    print("\n--- botty-jump.png ---")
    sheet = extract_stitch(
        os.path.join(RESOURCES, "player", "botty-jump.png"), 2, 64
    )
    sheet.save(os.path.join(OUTPUT, "player", "botty-jump.png"), "PNG")
    print(f"  -> Final: {sheet.width}x{sheet.height}")

    # Fix hills
    fix_hills()

    print("\nAll fixes applied!")


if __name__ == "__main__":
    main()
