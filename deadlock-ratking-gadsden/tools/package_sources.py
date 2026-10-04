#!/usr/bin/env python3
from pathlib import Path
import argparse
import zipfile

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument("variant", choices=["modern-clean", "modern-worn"])
a = p.parse_args()
v = a.variant

out = ROOT / "dist" / f"ratking-gadsden-{v}-sources.zip"
out.parent.mkdir(exist_ok=True)

files = [
    ROOT / "assets" / "source" / "gadsden-original.png",
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
