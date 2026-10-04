# Art and technical references

This project is raster-only. It does not redraw any flag and contains no SVG asset pipeline.

## Original / historical Gadsden raster

The `original-*` variants use **Gadsden Flag.png**, a raster reproduction sourced from *The Evening Tribune*, 11 February 1898, hosted by Wikimedia Commons.

- File page: https://commons.wikimedia.org/wiki/File:Gadsden_Flag.png
- Commons title: `File:Gadsden Flag.png`
- Published dimensions: 1,140 × 1,466
- Source date: 11 February 1898
- Source publication: *The Evening Tribune*
- Licensing on Commons: public domain in the United States (pre-1931 publication).

The build fetcher queries Wikimedia Commons' image-info API for the current original-file URL, dimensions and SHA-1, then verifies the downloaded raster byte-for-byte against that SHA-1.

Because the historical raster is an archival reproduction rather than a modern rectangular flag render, the clean treatment preserves all source detail but color-maps the paper and ink into ochre cloth/brown ink before placing it on the 3:2 banner canvas. No vector reconstruction is involved.

## Modern Gadsden raster

The `modern-*` variants use the exact raster image published as **Gadsden flag large.png** on Wikimedia Commons.

- File page: https://commons.wikimedia.org/wiki/File:Gadsden_flag_large.png
- Published dimensions: 900 × 600
- Pinned SHA-1: `ad1c2fa16219d59b975c29a8e290bc9c1587ab68`
- Original upload: Vikrum~commonswiki; later raster revision by Ptkfgs
- Licensing shown on the file page: GFDL and CC BY-SA 2.0 / 3.0.

## Join, or Die raster

The `join-or-die-*` variants use the archival lossless restoration **Benjamin Franklin - Join or Die.png** from Wikimedia Commons.

- File page: https://commons.wikimedia.org/wiki/File:Benjamin_Franklin_-_Join_or_Die.png
- Published dimensions: 3,740 × 2,696
- Pinned SHA-1: `7a79e6e41841667436d1ec2174b9caaa277248ad`
- Date of original political cartoon: 9 May 1754
- Attribution on Commons: Benjamin Franklin / restoration uploaded by Adam Cuerden
- Licensing: public domain / Public Domain Mark on the Commons file page.

The Join, or Die image is kept whole when mapped to the 3:2 source canvas. The pipeline pads it using a color sampled from the archival paper rather than cropping the snake, labels, or title.

## Raster treatment

`tools/fetch_source.py` verifies each raster against Wikimedia Commons metadata before it is accepted.

`tools/prepare_rasters.py` only performs raster operations:

- high-quality Lanczos resampling;
- archival paper/ink color mapping for the original Gadsden reproduction;
- mild sharpening appropriate to each source;
- optional restrained cloth/grime treatment for every `*-worn` variant.

No flag artwork is reconstructed as vector art.

## Deadlock / Source 2 references

- Rat King assets are under `models/heroes_wip/ratking/` in Deadlock's VPK; the build script discovers the current banner texture instead of hard-coding a filename that may change during development.
- ValveResourceFormat / Source 2 Viewer CLI is used to list and extract the current local asset.
- Reduced CSDK 12 / `resourcecompiler.exe` is used to compile the replacement.

No Valve texture is committed to this repository. The build process requires the user's own installed Deadlock files.
