#!/usr/bin/env python3
"""Compose one of the vector/raster Gadsden variants into Rat King's real banner texture.

The base texture is exported from the user's own Deadlock VPK. We preserve its exact
canvas, alpha, and a controlled amount of its luminance/wear so the replacement keeps
some of the in-game cloth character instead of looking like a flat sticker.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps


def contain(src: Image.Image, size: tuple[int, int], margin: float) -> Image.Image:
    w, h = size
    box = (max(1, int(w * (1 - 2 * margin))), max(1, int(h * (1 - 2 * margin))))
    src = src.copy()
    src.thumbnail(box, Image.Resampling.LANCZOS)
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    x = (w - src.width) // 2
    y = (h - src.height) // 2
    out.alpha_composite(src, (x, y))
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--base", required=True, type=Path)
    p.add_argument("--art", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--margin", type=float, default=0.015)
    p.add_argument("--wear", type=float, default=0.22,
                   help="0..1 strength of base-texture luminance modulation")
    args = p.parse_args()

    base = Image.open(args.base).convert("RGBA")
    art = Image.open(args.art).convert("RGBA")
    art = contain(art, base.size, args.margin)

    base_alpha = base.getchannel("A")
    art_alpha = art.getchannel("A")
    alpha = ImageChops.multiply(art_alpha, base_alpha)

    base_l = ImageOps.grayscale(base)
    base_l = ImageEnhance.Contrast(base_l).enhance(0.70).filter(ImageFilter.GaussianBlur(0.45))
    neutral = Image.new("L", base.size, 128)
    shade = Image.blend(neutral, base_l, max(0.0, min(1.0, args.wear)))
    shade_rgb = Image.merge("RGB", (shade, shade, shade))

    rgb = art.convert("RGB")
    shade_rgb = ImageEnhance.Brightness(shade_rgb).enhance(2.0)
    rgb = ImageChops.multiply(rgb, shade_rgb)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.04)

    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.save(args.output, optimize=True)
    print(f"wrote {args.output} ({out.width}x{out.height})")

if __name__ == "__main__":
    main()
