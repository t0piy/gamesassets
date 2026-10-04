# Art and technical references

This project is raster-only. It does not redraw any flag and contains no SVG asset pipeline.

## Original / accurate Gadsden raster

The `original-*` variants use the same **Gadsden Flag (Accurate)** appearance that the project used as its first historical reference.

- File page: https://commons.wikimedia.org/wiki/File:Gadsden_Flag_(Accurate).svg
- Commons source dimensions: 1,614 × 1,014
- Source SHA-1: `5ee2386154327e7be90b7ff48134fd4a0e5ad092`
- Author: BlinxTheKitty
- Licensing: CC0 1.0 / public-domain dedication.
- Raster actually downloaded by this project: the **3,840 × 2,412 PNG preview rendered by Wikimedia Commons**.

The project does not download, store, convert, or process the SVG file. `tools/fetch_source.py` asks the Commons API for its official 3,840-pixel PNG preview and validates the source metadata plus the downloaded PNG dimensions/checksum.

This restores the earlier original/accurate visual while keeping the entire mod pipeline raster-only.

## Modern Gadsden raster

The `modern-*` variants use the exact raster image published as **Gadsden flag large.png** on Wikimedia Commons.

- File page: https://commons.wikimedia.org/wiki/File:Gadsden_flag_large.png
- Published dimensions: 900 × 600
- Pinned SHA-1: `ad1c2fa16219d59b975c29a8e290bc9c1587ab68`

## Join, or Die raster

The `join-or-die-*` variants use the archival lossless restoration **Benjamin Franklin - Join or Die.png** from Wikimedia Commons.

- File page: https://commons.wikimedia.org/wiki/File:Benjamin_Franklin_-_Join_or_Die.png
- Published dimensions: 3,740 × 2,696
- Pinned SHA-1: `7a79e6e41841667436d1ec2174b9caaa277248ad`
- Licensing: public domain / Public Domain Mark.

## Raster treatment

`tools/fetch_source.py` validates each source against Wikimedia Commons metadata before it is accepted.

`tools/prepare_rasters.py` only performs raster operations:

- high-quality Lanczos resampling;
- mild sharpening appropriate to each source;
- optional restrained cloth/grime treatment for every `*-worn` variant.

No flag artwork is reconstructed as vector art.

## Deadlock / Source 2 references

- Rat King assets are under `models/heroes_wip/ratking/` in Deadlock's VPK; the build script discovers the current banner texture instead of hard-coding a filename that may change during development.
- ValveResourceFormat / Source 2 Viewer CLI is used to list and extract the current local asset.
- Reduced CSDK 12 / `resourcecompiler.exe` is used to compile the replacement.

No Valve texture is committed to this repository. The build process requires the user's own installed Deadlock files.
