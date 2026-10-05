#!/usr/bin/env python3
"""Prepare game-sized 2048x1024 raster payloads for DMM-installable VPKs."""
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "source"
OUT = ROOT / "dist" / "dmm-textures"
TARGET = (2048, 1024)

VARIANTS = (
    "original-clean",
    "original-worn",
    "modern-clean",
    "modern-worn",
    "join-or-die-clean",
    "join-or-die-worn",
)

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for variant in VARIANTS:
        src = SRC / f"{variant}-4096.png"
        if not src.exists():
            raise SystemExit(f"missing prepared master: {src}")
        # The real Rat King color VTEX is 2048x1024. Resize to that exact
        # on-wire canvas so the mesh/material sees the same aspect and dimensions
        # as a known-working Rat King flag mod.
        img = Image.open(src).convert("RGBA")
        img = img.resize(TARGET, Image.Resampling.LANCZOS)
        img = img.filter(ImageFilter.UnsharpMask(radius=0.45, percent=45, threshold=2))
        out = OUT / f"{variant}.png"
        img.save(out, optimize=True)
        print(f"{variant}: {out} {img.size}")

if __name__ == "__main__":
    main()
