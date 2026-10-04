#!/usr/bin/env python3
"""Prepare high-resolution raster variants from the exact downloaded flag image."""
from __future__ import annotations
from pathlib import Path
import random
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "source" / "gadsden-original.png"
SRC_DIR = ROOT / "assets" / "source"
PRE_DIR = ROOT / "assets" / "previews"
MASTER_SIZE = (4096, 2731)
PREVIEW_SIZE = (1600, 1067)

def upscale_original(img: Image.Image) -> Image.Image:
    img = img.convert("RGB")
    img = ImageOps.fit(img, MASTER_SIZE, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    img = img.filter(ImageFilter.UnsharpMask(radius=1.15, percent=115, threshold=2))
    return img

def add_game_wear(img: Image.Image) -> Image.Image:
    rng = random.Random(1775)
    base = img.convert("RGB")

    # Broad cloth-like lighting variation.
    noise_small = Image.new("L", (128, 86))
    px = noise_small.load()
    for y in range(noise_small.height):
        for x in range(noise_small.width):
            px[x, y] = rng.randint(92, 166)
    noise = noise_small.resize(base.size, Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(13))
    neutral = Image.new("L", base.size, 128)
    shade = Image.blend(neutral, noise, 0.28)
    shade_rgb = Image.merge("RGB", (shade, shade, shade))
    shade_rgb = ImageEnhance.Brightness(shade_rgb).enhance(2.0)
    worn = ImageChops.multiply(base, shade_rgb)

    # Subtle warm grime and faded fibers; deliberately restrained because the
    # real Deadlock banner shading is applied again during the final composition.
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay, "RGBA")
    w, h = base.size
    for _ in range(110):
        x = rng.randint(-80, w)
        y = rng.randint(-40, h)
        rx = rng.randint(16, 180)
        ry = rng.randint(4, 46)
        d.ellipse((x-rx, y-ry, x+rx, y+ry), fill=(74, 48, 21, rng.randint(5, 24)))
    for _ in range(36):
        x = rng.randint(0, w)
        y = rng.randint(0, h)
        length = rng.randint(40, 240)
        d.line((x, y, min(w, x+length), min(h, y+rng.randint(-12, 12))), fill=(246, 224, 132, rng.randint(10, 28)), width=rng.randint(1, 4))

    worn = Image.alpha_composite(worn.convert("RGBA"), overlay).convert("RGB")
    worn = ImageEnhance.Color(worn).enhance(0.94)
    worn = ImageEnhance.Contrast(worn).enhance(0.97)
    return worn

def save_variant(name: str, image: Image.Image) -> None:
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    PRE_DIR.mkdir(parents=True, exist_ok=True)
    master = SRC_DIR / f"{name}-4096.png"
    preview = PRE_DIR / f"{name}.png"
    image.save(master, optimize=True)
    image.resize(PREVIEW_SIZE, Image.Resampling.LANCZOS).save(preview, optimize=True)
    print(master)
    print(preview)

def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"missing raster source: {SOURCE}; run tools/fetch_source.py first")
    original = Image.open(SOURCE)
    clean = upscale_original(original)
    worn = add_game_wear(clean)
    save_variant("modern-clean", clean)
    save_variant("modern-worn", worn)

if __name__ == "__main__":
    main()
