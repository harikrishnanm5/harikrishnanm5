"""
Pixel Art Video & GIF Converter
Generates high-quality retro pixel art GIF and MP4 from video.
"""

import subprocess
import sys
import shutil

INPUT = "video.mp4"
OUTPUT_GIF = "pixel_art.gif"
OUTPUT_MP4 = "pixel_art.mp4"

# Settings
PIX_W = 90          # Pixel grid width (90x160 matches 9:16 aspect ratio)
PIX_H = 160         # Pixel grid height
SCALE_GIF = 3       # Upscale factor for GIF -> 270x480
SCALE_MP4 = 6       # Upscale factor for MP4 -> 540x960
MAX_SEC = 9.08      # Cuts off dead black screen at the end
GIF_FPS = 12        # Optimized framerate for smooth loop & <3MB file size
COLORS = 64         # Palette size (keeps eye color & ribbon vibrant)

def convert():
    if not shutil.which("ffmpeg"):
        print("FFmpeg not found in PATH!")
        sys.exit(1)

    print(f"Generating optimized Pixel Art GIF ({OUTPUT_GIF})...")
    # Area downscale gives clean anime lines, neighbor upscale gives crisp pixel blocks
    gif_vf = (
        f"fps={GIF_FPS},"
        f"scale={PIX_W}:{PIX_H}:flags=area,"
        f"scale={PIX_W * SCALE_GIF}:{PIX_H * SCALE_GIF}:flags=neighbor,"
        f"split[s0][s1];"
        f"[s0]palettegen=max_colors={COLORS}:stats_mode=diff[p];"
        f"[s1][p]paletteuse=dither=none"
    )
    subprocess.run([
        "ffmpeg", "-t", str(MAX_SEC), "-i", INPUT,
        "-vf", gif_vf, "-y", OUTPUT_GIF
    ], check=True)
    print(f"✓ Saved {OUTPUT_GIF}")

    print(f"Generating Pixel Art MP4 video with audio ({OUTPUT_MP4})...")
    mp4_vf = (
        f"scale={PIX_W}:{PIX_H}:flags=area,"
        f"scale={PIX_W * SCALE_MP4}:{PIX_H * SCALE_MP4}:flags=neighbor"
    )
    subprocess.run([
        "ffmpeg", "-t", str(MAX_SEC), "-i", INPUT,
        "-vf", mp4_vf,
        "-c:v", "libx264", "-crf", "20", "-preset", "fast",
        "-c:a", "aac", "-threads", "2", "-y", OUTPUT_MP4
    ], check=True)
    print(f"✓ Saved {OUTPUT_MP4}")

if __name__ == "__main__":
    convert()
