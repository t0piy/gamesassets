#!/usr/bin/env python3
from pathlib import Path
import argparse, zipfile
ROOT = Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(); p.add_argument('variant'); a=p.parse_args()
v=a.variant
out=ROOT/'dist'/f'ratking-gadsden-{v}-sources.zip'; out.parent.mkdir(exist_ok=True)
files=[ROOT/'assets/source'/f'{v}.svg',ROOT/'assets/source'/f'{v}-4096.png',ROOT/'assets/previews'/f'{v}.png',ROOT/'SOURCES.md',ROOT/'LICENSE']
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for f in files: z.write(f,f.relative_to(ROOT))
print(out)
