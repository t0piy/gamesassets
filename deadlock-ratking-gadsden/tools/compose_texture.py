#!/usr/bin/env python3
"""Compose the verified raster flag into Rat King's real banner texture.

The base texture is exported from the user's own Deadlock VPK. The replacement keeps
the game's exact alpha silhouette and reuses controlled luminance/wear from that real
banner so the flag reads like part of the asset instead of a flat pasted image.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps, ImageStat

def corner_fill(src: Image.Image) -> tuple[int, int, int, int]:
    rgba = src.convert("RGBA")
    w, h = rgba.size
    s = max(1, min(w, h) // 12)
    patches = [
        rgba.crop((0, 0, s, s)),
        rgba.crop((w-s, 0, w, s)),
        rgba.crop((0, h-s, s, h)),
        rgba.crop((w-s, h-s, w, h)),
    ]
    means = [ImageStat.Stat(p.convert("RGB")).mean for p in patches]
    rgb = tuple(int(sum(v[i] for v in means) / len(means)) for i in range(3))
    return (*rgb, 255)

def place_full_flag(src: Image.Image, size: tuple[int, int], margin: float) -> Image.Image:
    w, h = size
    inset_w = max(1, int(w * (1 - 2 * margin)))
    inset_h = max(1, int(h * (1 - 2 * margin)))
    art = src.convert("RGBA").copy()
    art.thumbnail((inset_w, inset_h), Image.Resampling.LANCZOS)

    out = Image.new("RGBA", size, corner_fill(src))
    x = (w - art.width) // 2
    y = (h - art.height) // 2
    out.alpha_composite(art, (x, y))
    return out

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--base", required=True, type=Path)
    p.add_argument("--art", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--margin", type=float, default=0.0)
    p.add_argument("--wear", type=float, default=0.26,
                   help="0..1 strength of real base-texture luminance modulation")
    args = p.parse_args()

    base = Image.open(args.base).convert("RGBA")
    art = place_full_flag(Image.open(args.art), base.size, args.margin)

    # The mesh/banner silhouette comes from the actual Deadlock texture, not the source image.
    base_alpha = base.getchannel("A")

    base_l = ImageOps.grayscale(base)
    base_l = ImageEnhance.Contrast(base_l).enhance(0.74).filter(ImageFilter.GaussianBlur(0.45))
    neutral = Image.new("L", base.size, 128)
    shade = Image.blend(neutral, base_l, max(0.0, min(1.0, args.wear)))
    shade_rgb = Image.merge("RGB", (shade, shade, shade))
    shade_rgb = ImageEnhance.Brightness(shade_rgb).enhance(2.0)

    rgb = ImageChops.multiply(art.convert("RGB"), shade_rgb)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.035)
    rgb = ImageEnhance.Color(rgb).enhance(0.985)

    out = rgb.convert("RGBA")
    out.putalpha(base_alpha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.save(args.output, optimize=True)
    print(f"wrote {args.output} ({out.width}x{out.height})")

if __name__ == "__main__":
    main()
