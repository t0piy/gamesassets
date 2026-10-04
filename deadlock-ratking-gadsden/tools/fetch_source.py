#!/usr/bin/env python3
"""Fetch the exact raster source used by the mod and verify it byte-for-byte."""
from __future__ import annotations
import argparse
import hashlib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "assets" / "source" / "gadsden-original.png"
URL = "https://upload.wikimedia.org/wikipedia/commons/a/a1/Gadsden_flag_large.png"
EXPECTED_SHA1 = "ad1c2fa16219d59b975c29a8e290bc9c1587ab68"

def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.exists() and not args.force:
        digest = sha1(DEST)
        if digest == EXPECTED_SHA1:
            print(f"using verified raster source: {DEST}")
            return
        raise SystemExit(f"{DEST} exists but SHA-1 is {digest}; expected {EXPECTED_SHA1}. Use --force to replace it.")

    req = urllib.request.Request(URL, headers={"User-Agent": "RatKing-Gadsden-Mod/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response, DEST.open("wb") as out:
        out.write(response.read())

    digest = sha1(DEST)
    if digest != EXPECTED_SHA1:
        DEST.unlink(missing_ok=True)
        raise SystemExit(f"source checksum mismatch: got {digest}, expected {EXPECTED_SHA1}")
    print(f"downloaded and verified {DEST}")

if __name__ == "__main__":
    main()
