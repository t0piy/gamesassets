#!/usr/bin/env python3
"""Fetch exact raster sources used by the mod and verify them byte-for-byte."""
from __future__ import annotations

import argparse
import hashlib
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "assets" / "source"

SOURCES = {
    "gadsden": {
        "dest": SRC_DIR / "gadsden-original.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/a1/Gadsden_flag_large.png",
        "sha1": "ad1c2fa16219d59b975c29a8e290bc9c1587ab68",
    },
    "join-or-die": {
        "dest": SRC_DIR / "join-or-die-original.png",
        "url": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Benjamin%20Franklin%20-%20Join%20or%20Die.png",
        "sha1": "7a79e6e41841667436d1ec2174b9caaa277248ad",
    },
}


def file_sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(name: str, force: bool = False) -> None:
    spec = SOURCES[name]
    dest: Path = spec["dest"]
    expected = spec["sha1"]

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not force:
        digest = file_sha1(dest)
        if digest == expected:
            print(f"{name}: using verified raster source: {dest}")
            return
        raise SystemExit(
            f"{dest} exists but SHA-1 is {digest}; expected {expected}. "
            "Use --force to replace it."
        )

    req = urllib.request.Request(
        spec["url"],
        headers={"User-Agent": "RatKing-Revolutionary-Banners/2.0 (+GitHub Actions)"},
    )
    with urllib.request.urlopen(req, timeout=120) as response, dest.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)

    digest = file_sha1(dest)
    if digest != expected:
        dest.unlink(missing_ok=True)
        raise SystemExit(
            f"{name}: source checksum mismatch: got {digest}, expected {expected}"
        )
    print(f"{name}: downloaded and verified {dest}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "sources",
        nargs="*",
        choices=sorted(SOURCES),
        help="Source(s) to fetch. Omit to fetch all.",
    )
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    selected = args.sources or list(SOURCES)
    for name in selected:
        fetch(name, force=args.force)


if __name__ == "__main__":
    main()
