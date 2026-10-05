# Art and technical references

This project is raster-only. It does not redraw any flag and contains no SVG asset pipeline.

## Original / accurate Gadsden raster

The `original-*` variants use the same **Gadsden Flag (Accurate)** appearance used as the project's first historical reference.

- File page: https://commons.wikimedia.org/wiki/File:Gadsden_Flag_(Accurate).svg
- Commons source dimensions: 1,614 × 1,014
- Source SHA-1: `5ee2386154327e7be90b7ff48134fd4a0e5ad092`
- Author: BlinxTheKitty
- Licensing: CC0 1.0 / public-domain dedication.
- Raster downloaded by this project: the large PNG preview rendered by Wikimedia Commons (3840px wide; the served PNG decodes as 3840×2413).

The project does not download, store, convert, or process the SVG file. `tools/fetch_source.py` asks the Commons API for its PNG preview and validates the source metadata and raster dimensions.

## Modern Gadsden raster

The `modern-*` variants use **Gadsden flag large.png** from Wikimedia Commons.

- File page: https://commons.wikimedia.org/wiki/File:Gadsden_flag_large.png
- Published dimensions: 900 × 600
- Pinned SHA-1: `ad1c2fa16219d59b975c29a8e290bc9c1587ab68`

## Join, or Die raster

The `join-or-die-*` variants use **Benjamin Franklin - Join or Die.png** from Wikimedia Commons.

- File page: https://commons.wikimedia.org/wiki/File:Benjamin_Franklin_-_Join_or_Die.png
- Published dimensions: 3,740 × 2,696
- Pinned SHA-1: `7a79e6e41841667436d1ec2174b9caaa277248ad`
- Licensing: public domain / Public Domain Mark.

## Rat King VPK target

For interoperability testing, the project inspected the file structure of the public **Turkish Flag for Ratking** mod:

- GameBanana: https://gamebanana.com/mods/723299
- Inspection purpose: determine the resource path and texture parameters used by a working Rat King banner replacement.
- No image, material, VTEX, VPK payload, or other compiled bytes from that mod are included in this project.

The working mod confirmed this color-texture target:

```text
models/heroes_wip/ratking/materials/ratking_ratannia_flag_color_png_155b4b23.vtex_c
```

Technical observations from the working replacement texture:

- stored/actual dimensions: 2048 × 1024
- format: BC7
- mip levels: 9
- texture flags: 0

The DMM-ready artifacts in this project create a **new** VTEX from this project's raster artwork at the same 2048×1024 canvas and pack only that replacement path into a fresh VPK. No reference-mod or Valve asset is redistributed.

## Deadlock Mod Manager compatibility

Deadlock Mod Manager's local-import code accepts a raw `.vpk` or an archive containing at least one `.vpk`. A source-only ZIP is intentionally not an installable mod.

The GitHub workflow therefore publishes six `*-DMM` artifacts, each containing a generated `*_dir.vpk`.

The VPK/Source 2 writing step uses a pinned revision of the open-source `vpkmanager` package from Deadlock Mod Manager during CI. The dependency is fetched at build time; the generated artifact contains only this project's one-file VPK.

## Raster treatment

`tools/prepare_rasters.py` performs only raster operations:

- high-quality Lanczos resampling;
- mild sharpening appropriate to each source;
- optional restrained cloth/grime treatment for `*-worn` variants.

`tools/prepare_dmm_payloads.py` then resizes the selected prepared art to the real Rat King flag texture canvas, 2048×1024.

## Local Source 2 build

The optional local build uses:

- ValveResourceFormat / Source 2 Viewer CLI to inspect the user's installed game;
- Reduced CSDK 12 / `resourcecompiler.exe` to compile replacements locally.

No Valve texture is committed to this repository.
