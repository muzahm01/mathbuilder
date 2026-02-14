import struct
import zlib
import os

def write_png(width, height, color_rgb):
    # color_rgb is (r, g, b) tuple
    # simple PNG writer
    
    # Header
    png_sig = b'\x89PNG\r\n\x1a\n'
    
    # IHDR
    # Length, Type, Width, Height, BitDepth, ColorType, Compression, Filter, Interlace
    # ColorType 2 = Truecolor (RGB)
    ihdr_content = struct.pack("!IIBBBBB", width, height, 8, 2, 0, 0, 0)
    ihdr_data = struct.pack("!I4s", 13, b'IHDR') + ihdr_content
    ihdr_crc = struct.pack("!I", zlib.crc32(ihdr_data[4:]) & 0xFFFFFFFF)
    
    # IDAT
    # Create raw data: 1 byte filter (0) + width * 3 bytes RGB per row
    line_data = b'\x00' + struct.pack("BBB", *color_rgb) * width
    raw_data = line_data * height
            
    compressor = zlib.compressobj()
    compressed = compressor.compress(raw_data) + compressor.flush()
    idat_data = struct.pack("!I4s", len(compressed), b'IDAT') + compressed
    idat_crc = struct.pack("!I", zlib.crc32(idat_data[4:]) & 0xFFFFFFFF)
    
    # IEND
    iend_data = struct.pack("!I4s", 0, b'IEND')
    iend_crc = struct.pack("!I", zlib.crc32(iend_data[4:]) & 0xFFFFFFFF)
    
    return png_sig + ihdr_data + ihdr_crc + idat_data + idat_crc + iend_data + iend_crc

# Ensure resources directories exist
dirs = [
    "resources/tiles",
    "resources/player",
    "resources/backgrounds",
    "resources/ui",
    "resources/objects",
    "resources/particles"
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

placeholders = [
    # Tiles
    {"path": "resources/tiles/grass-top.png", "size": (64, 64), "color": "#4CAF50"},
    {"path": "resources/tiles/dirt.png", "size": (64, 64), "color": "#795548"},
    {"path": "resources/tiles/stone.png", "size": (64, 64), "color": "#9E9E9E"},
    
    # Player
    {"path": "resources/player/botty-idle.png", "size": (256, 64), "color": "#2196F3"},
    {"path": "resources/player/botty-walk.png", "size": (384, 64), "color": "#2196F3"},
    {"path": "resources/player/botty-jump.png", "size": (128, 64), "color": "#2196F3"},
    
    # Backgrounds
    {"path": "resources/backgrounds/sky.png", "size": (800, 600), "color": "#87CEEB"},
    {"path": "resources/backgrounds/clouds.png", "size": (800, 200), "color": "#E0F7FA"},
    {"path": "resources/backgrounds/hills.png", "size": (800, 200), "color": "#81C784"},
    
    # UI
    {"path": "resources/ui/btn-play.png", "size": (200, 70), "color": "#4CAF50"},
    {"path": "resources/ui/btn-levels.png", "size": (200, 70), "color": "#2196F3"},
    {"path": "resources/ui/star-filled.png", "size": (32, 32), "color": "#FFD700"},
    {"path": "resources/ui/star-empty.png", "size": (32, 32), "color": "#BDBDBD"},
    {"path": "resources/ui/math-input-bg.png", "size": (400, 250), "color": "#FFFFFF"},
    {"path": "resources/ui/arrow-left.png", "size": (64, 64), "color": "#607D8B"},
    {"path": "resources/ui/arrow-right.png", "size": (64, 64), "color": "#607D8B"},
    {"path": "resources/ui/arrow-jump.png", "size": (64, 64), "color": "#607D8B"},
    
    # Objects
    {"path": "resources/objects/flag.png", "size": (64, 64), "color": "#FFC107"},
    {"path": "resources/objects/bridge-block.png", "size": (64, 64), "color": "#8D6E63"},
    
    # Particles
    {"path": "resources/particles/dust.png", "size": (8, 8), "color": "#EFEBE9"},
    {"path": "resources/particles/confetti.png", "size": (8, 8), "color": "#FFEB3B"}
]

for item in placeholders:
    rgb = hex_to_rgb(item["color"])
    data = write_png(item["size"][0], item["size"][1], rgb)
    with open(item["path"], "wb") as f:
        f.write(data)
    print(f"Generated: {item['path']}")
