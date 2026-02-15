#!/usr/bin/env python3
"""
Fix script for player sprites (too small) and background transparency.
"""

from PIL import Image, ImageDraw
import os

RESOURCES = "/home/user/mathbuilder/resources"
OUTPUT = "/home/user/mathbuilder/public/assets/images"


def remove_background_generous(img, threshold=235):
    """Remove white/near-white background aggressively."""
    img = img.convert("RGBA")
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            # White and near-white
            if r > threshold and g > threshold and b > threshold:
                pixels[x, y] = (r, g, b, 0)
            # Grey checkerboard pattern
            elif abs(r - g) < 15 and abs(g - b) < 15 and r > 175:
                pixels[x, y] = (r, g, b, 0)
    return img


def find_sprite_bboxes(img, num_sprites):
    """
    Find individual sprite bounding boxes by scanning for connected
    non-transparent regions horizontally.
    """
    w, h = img.size
    pixels = img.load()

    # Build vertical projection: for each x, is there any non-transparent pixel?
    x_has_content = []
    for x in range(w):
        has = False
        for y in range(h):
            if pixels[x, y][3] > 30:
                has = True
                break
        x_has_content.append(has)

    # Find contiguous horizontal spans of content
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

    # Merge spans with small gaps (< 8px)
    merged = [spans[0]] if spans else []
    for s, e in spans[1:]:
        if s - merged[-1][1] < 8:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))

    # If too many spans, merge the closest ones
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

    # If too few, split the widest
    while len(merged) < num_sprites:
        widths = [(e - s, i) for i, (s, e) in enumerate(merged)]
        widths.sort(reverse=True)
        idx = widths[0][1]
        s, e = merged[idx]
        mid = (s + e) // 2
        merged[idx] = (s, mid)
        merged.insert(idx + 1, (mid, e))

    # Now find vertical bounds for each sprite
    bboxes = []
    for sx, ex in merged:
        top = h
        bottom = 0
        for x in range(sx, ex):
            for y in range(h):
                if pixels[x, y][3] > 30:
                    top = min(top, y)
                    bottom = max(bottom, y)
        bboxes.append((sx, top, ex, bottom + 1))

    return bboxes


def extract_and_stitch(src_path, num_frames, target_size=64):
    """
    Extract sprite frames and stitch into a proper horizontal sheet.
    Characters fill ~85% of each frame height.
    """
    img = Image.open(src_path).convert("RGBA")

    # Remove background
    clean = remove_background_generous(img)

    # Find sprite bounding boxes
    bboxes = find_sprite_bboxes(clean, num_frames)

    print(f"  Found {len(bboxes)} sprites: {bboxes}")

    frames = []
    for left, top, right, bottom in bboxes:
        # Extract sprite with padding
        pad = 2
        sprite = clean.crop((
            max(0, left - pad),
            max(0, top - pad),
            min(clean.width, right + pad),
            min(clean.height, bottom + pad)
        ))

        sw, sh = sprite.size
        if sw == 0 or sh == 0:
            # Empty frame fallback
            frames.append(Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0)))
            continue

        # Scale to fill ~85% of the target frame
        fill_ratio = 0.88
        scale = min(
            (target_size * fill_ratio) / sw,
            (target_size * fill_ratio) / sh
        )
        new_w = max(1, int(sw * scale))
        new_h = max(1, int(sh * scale))
        sprite = sprite.resize((new_w, new_h), Image.LANCZOS)

        # Place in frame, bottom-aligned with small margin
        frame = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
        paste_x = (target_size - new_w) // 2
        paste_y = target_size - new_h - 2  # Bottom-aligned
        frame.paste(sprite, (paste_x, paste_y), sprite)
        frames.append(frame)

    # Stitch
    sheet_w = target_size * num_frames
    sheet = Image.new("RGBA", (sheet_w, target_size), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        sheet.paste(frame, (i * target_size, 0), frame)

    return sheet


def fix_hills():
    """
    Fix hills.png: resize properly and ensure transparency above the hills.
    The original is 640x640 square -- we need to extract just the bottom portion
    where the hills are and resize to 800x200.
    """
    print("\nFixing hills.png...")
    src = Image.open(os.path.join(RESOURCES, "backgrounds", "hills.png")).convert("RGBA")

    # The hills are in the bottom portion of the 640x640 image
    # Crop to the bottom ~45% where the hills actually are
    w, h = src.size
    # Find where content starts vertically
    pixels = src.load()
    content_top = h
    for y in range(h):
        for x in range(0, w, 10):  # Sample every 10px for speed
            r, g, b, a = pixels[x, y]
            # Hills are green - look for green content
            if g > 80 and g > r and g > b * 0.8 and not (r > 230 and g > 230 and b > 230):
                content_top = min(content_top, y)
                break

    print(f"  Hills content starts at y={content_top} of {h}")

    # Add some padding above the content
    crop_top = max(0, content_top - 20)
    hills_crop = src.crop((0, crop_top, w, h))

    # Now remove white/near-white background above the hills
    hills_clean = remove_background_generous(hills_crop, threshold=232)

    # Resize to target
    hills_final = hills_clean.resize((800, 200), Image.LANCZOS)
    hills_final.save(os.path.join(OUTPUT, "backgrounds", "hills.png"), "PNG")
    print(f"  -> Saved 800x200 PNG with transparency")


def fix_clouds():
    """
    Fix clouds.png: extract just the cloud region and resize properly.
    The original 640x640 -> 800x200 squished the clouds too much.
    Instead, take a horizontal strip from the middle of the image.
    """
    print("\nFixing clouds.png...")
    src = Image.open(os.path.join(RESOURCES, "backgrounds", "clouds.png")).convert("RGBA")

    w, h = src.size
    # Take a horizontal strip from the middle (where most clouds are)
    strip_h = int(h * 0.45)  # Take ~45% of the height
    strip_top = (h - strip_h) // 2
    strip = src.crop((0, strip_top, w, strip_top + strip_h))

    # Remove background
    strip_clean = remove_background_generous(strip, threshold=230)

    # Resize to 800x200 (less extreme aspect ratio change now)
    clouds_final = strip_clean.resize((800, 200), Image.LANCZOS)
    clouds_final.save(os.path.join(OUTPUT, "backgrounds", "clouds.png"), "PNG")
    print(f"  -> Saved 800x200 PNG with transparency")


def main():
    print("=" * 50)
    print("Fixing player sprites and backgrounds")
    print("=" * 50)

    # Fix player sprites
    print("\nFixing botty-idle.png (4 frames)...")
    sheet = extract_and_stitch(
        os.path.join(RESOURCES, "player", "botty-idle.png"), 4, 64
    )
    sheet.save(os.path.join(OUTPUT, "player", "botty-idle.png"), "PNG")
    print(f"  -> Saved {sheet.width}x{sheet.height} PNG")

    print("\nFixing botty-walk.png (6 frames)...")
    sheet = extract_and_stitch(
        os.path.join(RESOURCES, "player", "botty-walk.png"), 6, 64
    )
    sheet.save(os.path.join(OUTPUT, "player", "botty-walk.png"), "PNG")
    print(f"  -> Saved {sheet.width}x{sheet.height} PNG")

    print("\nFixing botty-jump.png (2 frames)...")
    sheet = extract_and_stitch(
        os.path.join(RESOURCES, "player", "botty-jump.png"), 2, 64
    )
    sheet.save(os.path.join(OUTPUT, "player", "botty-jump.png"), "PNG")
    print(f"  -> Saved {sheet.width}x{sheet.height} PNG")

    # Fix backgrounds
    fix_hills()
    fix_clouds()

    print("\nDone! All fixes applied.")


if __name__ == "__main__":
    main()
