#!/usr/bin/env python3
"""Verify all MathBuilder game assets exist with correct dimensions."""

from PIL import Image
import os
import sys

OUTPUT = "/home/user/mathbuilder/public/assets/images"

EXPECTED = {
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


def main():
    ok = 0
    missing = 0
    wrong = 0

    for path, (exp_w, exp_h) in EXPECTED.items():
        full_path = os.path.join(OUTPUT, path)
        if not os.path.exists(full_path):
            print(f"  MISSING: {path}")
            missing += 1
            continue
        img = Image.open(full_path)
        w, h = img.size
        if (w, h) == (exp_w, exp_h):
            print(f"  OK: {path} ({w}x{h})")
            ok += 1
        else:
            print(f"  WRONG SIZE: {path} is {w}x{h}, expected {exp_w}x{exp_h}")
            wrong += 1

    total = len(EXPECTED)
    print(f"\nResults: {ok}/{total} OK, {missing} missing, {wrong} wrong size")

    if ok == total:
        print("All assets verified successfully!")
        return 0
    else:
        print("Some assets need attention.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
