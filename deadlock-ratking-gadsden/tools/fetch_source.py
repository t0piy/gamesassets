#!/usr/bin/env python3
"""Fetch exact raster sources used by the mod and verify them against Wikimedia Commons metadata."""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "assets" / "source"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"

SOURCES = {
    "original-gadsden": {
        "title": "File:Gadsden Flag.png",
        "dest": SRC_DIR / "gadsden-historical-original.png",
        "dimensions": (1140, 1466),
    },
    "modern-gadsden": {
        "title": "File:Gadsden flag large.png",
        "dest": SRC_DIR / "gadsden-original.png",
        "dimensions": (900, 600),
        "sha1": "ad1c2fa16219d59b975c29a8e290bc9c1587ab68",
    },
    "join-or-die": {
        "title": "File:Benjamin Franklin - Join or Die.png",
        "dest": SRC_DIR / "join-or-die-original.png",
        "dimensions": (3740, 2696),
        "sha1": "7a79e6e41841667436d1ec2174b9caaa277248ad",
    },
}


def file_sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def commons_metadata(title: str) -> dict:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "prop": "imageinfo",
            "iiprop": "url|sha1|size",
            "titles": title,
        }
    )
    req = urllib.request.Request(
        f"{COMMONS_API}?{params}",
        headers={"User-Agent": "RatKing-Revolutionary-Banners/3.0 (+GitHub Actions)"},
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        data = json.load(response)

    pages = data.get("query", {}).get("pages", [])
    if not pages or "imageinfo" not in pages[0]:
        raise SystemExit(f"Commons did not return image metadata for {title}")

    info = pages[0]["imageinfo"][0]
    return {
        "url": info["url"],
        "sha1": info["sha1"],
        "width": int(info["width"]),
        "height": int(info["height"]),
    }


def fetch(name: str, force: bool = False) -> None:
    spec = SOURCES[name]
    dest: Path = spec["dest"]
    meta = commons_metadata(spec["title"])

    expected_dims = tuple(spec["dimensions"])
    actual_dims = (meta["width"], meta["height"])
    if actual_dims != expected_dims:
        raise SystemExit(
            f"{name}: Commons dimensions changed: got {actual_dims}, expected {expected_dims}"
        )

    pinned_sha1 = spec.get("sha1")
    if pinned_sha1 and meta["sha1"] != pinned_sha1:
        raise SystemExit(
            f"{name}: Commons SHA-1 changed: got {meta['sha1']}, expected {pinned_sha1}"
        )

    expected_sha1 = meta["sha1"]
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists() and not force:
        digest = file_sha1(dest)
        if digest == expected_sha1:
            print(
                f"{name}: using verified raster source: {dest} "
                f"({actual_dims[0]}x{actual_dims[1]}, sha1={expected_sha1})"
            )
            return
        raise SystemExit(
            f"{dest} exists but SHA-1 is {digest}; Commons currently reports "
            f"{expected_sha1}. Use --force to replace it."
        )

    req = urllib.request.Request(
        meta["url"],
        headers={"User-Agent": "RatKing-Revolutionary-Banners/3.0 (+GitHub Actions)"},
    )
    with urllib.request.urlopen(req, timeout=180) as response, dest.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)

    digest = file_sha1(dest)
    if digest != expected_sha1:
        dest.unlink(missing_ok=True)
        raise SystemExit(
            f"{name}: source checksum mismatch: got {digest}, expected {expected_sha1}"
        )

    print(
        f"{name}: downloaded and verified {dest} "
        f"({actual_dims[0]}x{actual_dims[1]}, sha1={expected_sha1})"
    )


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
