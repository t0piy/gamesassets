#!/usr/bin/env python3
from pathlib import Path
import argparse
import zipfile

ROOT = Path(__file__).resolve().parents[1]

VARIANT_SOURCE = {
    "original-clean": "gadsden-historical-original.png",
    "original-worn": "gadsden-historical-original.png",
    "modern-clean": "gadsden-original.png",
    "modern-worn": "gadsden-original.png",
    "join-or-die-clean": "join-or-die-original.png",
    "join-or-die-worn": "join-or-die-original.png",
}

p = argparse.ArgumentParser()
p.add_argument("variant", choices=sorted(VARIANT_SOURCE))
a = p.parse_args()
v = a.variant

out = ROOT / "dist" / f"ratking-banner-{v}-sources.zip"
out.parent.mkdir(exist_ok=True)

files = [
    ROOT / "assets" / "source" / VARIANT_SOURCE[v],
    ROOT / "assets" / "source" / f"{v}-4096.png",
    ROOT / "assets" / "previews" / f"{v}.png",
    ROOT / "SOURCES.md",
    ROOT / "LICENSE",
    ROOT / "mod.json",
]

missing = [str(f) for f in files if not f.exists()]
if missing:
    raise SystemExit("missing package files:\n" + "\n".join(missing))

with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for f in files:
        z.write(f, f.relative_to(ROOT))

print(out)
