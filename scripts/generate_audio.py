#!/usr/bin/env python3
"""Generate simple chiptune-style WAV sound effects for MathBuilder."""

import struct
import math
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'public', 'assets', 'audio')
SAMPLE_RATE = 22050

def write_wav(filename, samples, sample_rate=SAMPLE_RATE):
    """Write 16-bit mono WAV file."""
    path = os.path.join(OUTPUT_DIR, filename)
    num_samples = len(samples)
    data_size = num_samples * 2  # 16-bit = 2 bytes per sample

    with open(path, 'wb') as f:
        # RIFF header
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + data_size))
        f.write(b'WAVE')
        # fmt chunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))          # chunk size
        f.write(struct.pack('<H', 1))           # PCM format
        f.write(struct.pack('<H', 1))           # mono
        f.write(struct.pack('<I', sample_rate)) # sample rate
        f.write(struct.pack('<I', sample_rate * 2))  # byte rate
        f.write(struct.pack('<H', 2))           # block align
        f.write(struct.pack('<H', 16))          # bits per sample
        # data chunk
        f.write(b'data')
        f.write(struct.pack('<I', data_size))
        for s in samples:
            clamped = max(-1.0, min(1.0, s))
            f.write(struct.pack('<h', int(clamped * 32767)))

    print(f"  Written: {path} ({num_samples} samples, {num_samples/sample_rate:.2f}s)")


def generate_jump():
    """Quick ascending chirp - bright and short."""
    duration = 0.12
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        progress = i / n
        # Frequency sweeps up from 400 to 900 Hz
        freq = 400 + 500 * progress
        # Square wave (softer via mixing with sine)
        sine = math.sin(2 * math.pi * freq * t)
        square = 1.0 if sine > 0 else -1.0
        val = 0.6 * sine + 0.3 * square
        # Envelope: quick attack, quick decay
        env = 1.0 - progress
        samples.append(val * env * 0.5)
    return samples


def generate_correct():
    """Bright ascending two-tone ding - positive feedback."""
    duration = 0.3
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        progress = i / n
        # Two ascending notes
        if progress < 0.4:
            freq = 660  # E5
        else:
            freq = 880  # A5
        val = math.sin(2 * math.pi * freq * t)
        # Add harmonic
        val += 0.3 * math.sin(2 * math.pi * freq * 2 * t)
        # Envelope
        env = 1.0 - progress * 0.7
        samples.append(val * env * 0.45)
    return samples


def generate_wrong():
    """Soft low buzz - gentle 'oops', not scary."""
    duration = 0.2
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        progress = i / n
        # Low frequency descending
        freq = 300 - 100 * progress
        val = math.sin(2 * math.pi * freq * t)
        # Add slight wobble
        val += 0.2 * math.sin(2 * math.pi * (freq * 1.5) * t)
        # Soft envelope
        env = (1.0 - progress) * 0.6
        samples.append(val * env * 0.35)
    return samples


def generate_build():
    """Chunky stacking sound - satisfying construction feel."""
    duration = 0.35
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        progress = i / n
        # Low thud + higher click
        freq1 = 150 + 50 * progress
        freq2 = 500 - 200 * progress
        val = 0.6 * math.sin(2 * math.pi * freq1 * t)
        val += 0.4 * math.sin(2 * math.pi * freq2 * t)
        # Noise-like crunch at start
        if progress < 0.15:
            noise = math.sin(2 * math.pi * 1200 * t) * (1 - progress / 0.15)
            val += 0.3 * noise
        # Envelope: sharp attack, medium decay
        if progress < 0.05:
            env = progress / 0.05
        else:
            env = 1.0 - (progress - 0.05) / 0.95
        samples.append(val * env * 0.5)
    return samples


def generate_win():
    """Triumphant ascending sweep - celebration moment."""
    duration = 0.6
    n = int(SAMPLE_RATE * duration)
    samples = []
    # Three ascending notes with overlap
    notes = [
        (0.0, 0.25, 523),   # C5
        (0.15, 0.4, 659),   # E5
        (0.3, 0.6, 784),    # G5
    ]
    for i in range(n):
        t = i / SAMPLE_RATE
        val = 0
        for start, end, freq in notes:
            if start <= t <= end:
                local_t = (t - start) / (end - start)
                env = math.sin(math.pi * local_t)  # Smooth bell envelope
                tone = math.sin(2 * math.pi * freq * t)
                tone += 0.3 * math.sin(2 * math.pi * freq * 2 * t)  # Harmonic
                val += tone * env * 0.35
        samples.append(max(-1.0, min(1.0, val)))
    return samples


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating MathBuilder sound effects...")

    write_wav('jump.wav', generate_jump())
    write_wav('correct.wav', generate_correct())
    write_wav('wrong.wav', generate_wrong())
    write_wav('build.wav', generate_build())
    write_wav('win.wav', generate_win())

    print("Done! All audio files generated.")
