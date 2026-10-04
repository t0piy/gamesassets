#!/usr/bin/env python3
"""Prepare high-resolution raster variants from exact downloaded source images."""
from __future__ import annotations

from pathlib import Path
import random
from PIL import (
    Image,
    ImageChops,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageOps,
    ImageStat,
)

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "assets" / "source"
PRE_DIR = ROOT / "assets" / "previews"

GADSDEN_SOURCE = SRC_DIR / "gadsden-original.png"
JOIN_SOURCE = SRC_DIR / "join-or-die-original.png"

MASTER_SIZE = (4096, 2731)   # near-exact 3:2 flag canvas
PREVIEW_SIZE = (1600, 1067)


def border_color(img: Image.Image) -> tuple[int, int, int]:
    rgb = img.convert("RGB")
    w, h = rgb.size
    s = max(8, min(w, h) // 24)
    patches = [
        rgb.crop((0, 0, s, s)),
        rgb.crop((w - s, 0, w, s)),
        rgb.crop((0, h - s, s, h)),
        rgb.crop((w - s, h - s, w, h)),
    ]
    means = [ImageStat.Stat(p).mean for p in patches]
    return tuple(int(sum(m[i] for m in means) / len(means)) for i in range(3))


def prepare_gadsden(img: Image.Image) -> Image.Image:
    out = ImageOps.fit(
        img.convert("RGB"),
        MASTER_SIZE,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )
    return out.filter(ImageFilter.UnsharpMask(radius=1.15, percent=115, threshold=2))


def prepare_join_or_die(img: Image.Image) -> Image.Image:
    """Preserve the complete archival print; pad to 3:2 instead of cropping it."""
    src = img.convert("RGB")
    contained = ImageOps.contain(src, MASTER_SIZE, method=Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", MASTER_SIZE, border_color(src))
    x = (MASTER_SIZE[0] - contained.width) // 2
    y = (MASTER_SIZE[1] - contained.height) // 2
    canvas.paste(contained, (x, y))
    return canvas.filter(ImageFilter.UnsharpMask(radius=0.7, percent=60, threshold=2))


def add_game_wear(
    img: Image.Image,
    *,
    seed: int,
    grime: tuple[int, int, int],
    fiber: tuple[int, int, int],
    color_strength: float,
) -> Image.Image:
    rng = random.Random(seed)
    base = img.convert("RGB")

    # Broad low-frequency cloth lighting. Final build also inherits the actual
    # Deadlock banner luminance, so this pass deliberately stays restrained.
    noise_small = Image.new("L", (128, 86))
    px = noise_small.load()
    for y in range(noise_small.height):
        for x in range(noise_small.width):
            px[x, y] = rng.randint(96, 162)

    noise = noise_small.resize(base.size, Image.Resampling.BICUBIC)
    noise = noise.filter(ImageFilter.GaussianBlur(13))
    neutral = Image.new("L", base.size, 128)
    shade = Image.blend(neutral, noise, 0.24)
    shade_rgb = Image.merge("RGB", (shade, shade, shade))
    shade_rgb = ImageEnhance.Brightness(shade_rgb).enhance(2.0)
    worn = ImageChops.multiply(base, shade_rgb)

    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay, "RGBA")
    w, h = base.size

    for _ in range(95):
        x = rng.randint(-80, w)
        y = rng.randint(-40, h)
        rx = rng.randint(16, 170)
        ry = rng.randint(4, 40)
        d.ellipse(
            (x - rx, y - ry, x + rx, y + ry),
            fill=(*grime, rng.randint(4, 20)),
        )

    for _ in range(32):
        x = rng.randint(0, w)
        y = rng.randint(0, h)
        length = rng.randint(40, 220)
        d.line(
            (x, y, min(w, x + length), min(h, y + rng.randint(-10, 10))),
            fill=(*fiber, rng.randint(8, 24)),
            width=rng.randint(1, 4),
        )

    worn = Image.alpha_composite(worn.convert("RGBA"), overlay).convert("RGB")
    worn = ImageEnhance.Color(worn).enhance(color_strength)
    worn = ImageEnhance.Contrast(worn).enhance(0.975)
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
    missing = [p for p in (GADSDEN_SOURCE, JOIN_SOURCE) if not p.exists()]
    if missing:
        raise SystemExit(
            "missing raster source(s):\n"
            + "\n".join(str(p) for p in missing)
            + "\nrun tools/fetch_source.py first"
        )

    gadsden_clean = prepare_gadsden(Image.open(GADSDEN_SOURCE))
    gadsden_worn = add_game_wear(
        gadsden_clean,
        seed=1775,
        grime=(74, 48, 21),
        fiber=(246, 224, 132),
        color_strength=0.94,
    )

    join_clean = prepare_join_or_die(Image.open(JOIN_SOURCE))
    join_worn = add_game_wear(
        join_clean,
        seed=1754,
        grime=(58, 45, 32),
        fiber=(235, 226, 198),
        color_strength=0.965,
    )

    save_variant("modern-clean", gadsden_clean)
    save_variant("modern-worn", gadsden_worn)
    save_variant("join-or-die-clean", join_clean)
    save_variant("join-or-die-worn", join_worn)


if __name__ == "__main__":
    main()
