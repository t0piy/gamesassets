#!/usr/bin/env python3
"""Fetch exact raster sources used by the mod and verify them against Wikimedia Commons metadata."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "assets" / "source"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"

SOURCES = {
    # This intentionally downloads ONLY the large PNG preview rendered by Commons.
    # No SVG file is stored or processed by this project.
    "original-gadsden": {
        "title": "File:Gadsden Flag (Accurate).svg",
        "dest": SRC_DIR / "gadsden-accurate-original.png",
        "source_dimensions": (1614, 1014),
        "source_sha1": "5ee2386154327e7be90b7ff48134fd4a0e5ad092",
        "thumb_width": 3840,
        "raster_dimensions": (3840, 2413),
        # raster_sha1 is pinned after the rendered PNG has been validated in CI.
    },
    "modern-gadsden": {
        "title": "File:Gadsden flag large.png",
        "dest": SRC_DIR / "gadsden-original.png",
        "source_dimensions": (900, 600),
        "source_sha1": "ad1c2fa16219d59b975c29a8e290bc9c1587ab68",
        "raster_dimensions": (900, 600),
        "raster_sha1": "ad1c2fa16219d59b975c29a8e290bc9c1587ab68",
    },
    "join-or-die": {
        "title": "File:Benjamin Franklin - Join or Die.png",
        "dest": SRC_DIR / "join-or-die-original.png",
        "source_dimensions": (3740, 2696),
        "source_sha1": "7a79e6e41841667436d1ec2174b9caaa277248ad",
        "raster_dimensions": (3740, 2696),
        "raster_sha1": "7a79e6e41841667436d1ec2174b9caaa277248ad",
    },
}


def file_sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def urlopen_with_retry(req: urllib.request.Request, timeout: int):
    last_error = None
    for attempt in range(5):
        try:
            return urllib.request.urlopen(req, timeout=timeout)
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code != 429 or attempt == 4:
                raise
            retry_after = exc.headers.get("Retry-After")
            delay = int(retry_after) if retry_after and retry_after.isdigit() else (2 ** attempt)
            print(f"HTTP 429 from Wikimedia; retrying in {delay}s...")
            time.sleep(delay)
    raise last_error


def commons_metadata(title: str, thumb_width: int | None = None) -> dict:
    query = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "imageinfo",
        "iiprop": "url|sha1|size",
        "titles": title,
    }
    if thumb_width:
        query["iiurlwidth"] = str(thumb_width)

    params = urllib.parse.urlencode(query)
    req = urllib.request.Request(
        f"{COMMONS_API}?{params}",
        headers={"User-Agent": "RatKing-Revolutionary-Banners/3.1 (+GitHub Actions)"},
    )
    with urlopen_with_retry(req, timeout=120) as response:
        data = json.load(response)

    pages = data.get("query", {}).get("pages", [])
    if not pages or "imageinfo" not in pages[0]:
        raise SystemExit(f"Commons did not return image metadata for {title}")

    info = pages[0]["imageinfo"][0]
    result = {
        "url": info["url"],
        "sha1": info["sha1"],
        "width": int(info["width"]),
        "height": int(info["height"]),
    }
    if thumb_width:
        result.update(
            {
                "thumburl": info["thumburl"],
                "thumbwidth": int(info["thumbwidth"]),
                "thumbheight": int(info["thumbheight"]),
            }
        )
    return result


def verify_png(path: Path, expected_dims: tuple[int, int]) -> None:
    with Image.open(path) as img:
        if img.format != "PNG":
            raise SystemExit(f"{path} is {img.format}, expected PNG")
        if img.size != expected_dims:
            raise SystemExit(f"{path} is {img.size}, expected {expected_dims}")


def fetch(name: str, force: bool = False) -> None:
    spec = SOURCES[name]
    dest: Path = spec["dest"]
    thumb_width = spec.get("thumb_width")
    meta = commons_metadata(spec["title"], thumb_width=thumb_width)

    source_dims = (meta["width"], meta["height"])
    if source_dims != tuple(spec["source_dimensions"]):
        raise SystemExit(
            f"{name}: Commons source dimensions changed: got {source_dims}, "
            f"expected {tuple(spec['source_dimensions'])}"
        )
    if meta["sha1"] != spec["source_sha1"]:
        raise SystemExit(
            f"{name}: Commons source SHA-1 changed: got {meta['sha1']}, "
            f"expected {spec['source_sha1']}"
        )

    if thumb_width:
        download_url = meta["thumburl"]
        actual_raster_dims = (meta["thumbwidth"], meta["thumbheight"])
    else:
        download_url = meta["url"]
        actual_raster_dims = source_dims

    expected_raster_dims = tuple(spec["raster_dimensions"])
    if actual_raster_dims != expected_raster_dims:
        raise SystemExit(
            f"{name}: Commons raster dimensions changed: got {actual_raster_dims}, "
            f"expected {expected_raster_dims}"
        )

    pinned_raster_sha1 = spec.get("raster_sha1")
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists() and not force:
        verify_png(dest, expected_raster_dims)
        digest = file_sha1(dest)
        if pinned_raster_sha1 and digest != pinned_raster_sha1:
            raise SystemExit(
                f"{name}: local PNG SHA-1 is {digest}; expected {pinned_raster_sha1}. "
                "Use --force to replace it."
            )
        print(
            f"{name}: using verified raster source: {dest} "
            f"({expected_raster_dims[0]}x{expected_raster_dims[1]}, sha1={digest})"
        )
        return

    req = urllib.request.Request(
        download_url,
        headers={"User-Agent": "RatKing-Revolutionary-Banners/3.1 (+GitHub Actions)"},
    )
    with urlopen_with_retry(req, timeout=180) as response, dest.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)

    verify_png(dest, expected_raster_dims)
    digest = file_sha1(dest)
    if pinned_raster_sha1 and digest != pinned_raster_sha1:
        dest.unlink(missing_ok=True)
        raise SystemExit(
            f"{name}: raster checksum mismatch: got {digest}, expected {pinned_raster_sha1}"
        )

    print(
        f"{name}: downloaded and verified {dest} "
        f"({expected_raster_dims[0]}x{expected_raster_dims[1]}, sha1={digest})"
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
