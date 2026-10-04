# Art and technical references

This project is raster-only. It does not redraw either flag and contains no SVG asset pipeline.

## Gadsden raster

The Gadsden variants use the exact raster image published as **Gadsden flag large.png** on Wikimedia Commons.

- File page: https://commons.wikimedia.org/wiki/File:Gadsden_flag_large.png
- Direct raster: https://upload.wikimedia.org/wikipedia/commons/a/a1/Gadsden_flag_large.png
- Published dimensions: 900 × 600
- Published SHA-1: `ad1c2fa16219d59b975c29a8e290bc9c1587ab68`
- Original upload: Vikrum~commonswiki; later raster revision by Ptkfgs
- Licensing shown on the file page: GFDL and CC BY-SA 2.0 / 3.0; the underlying historical design is also marked public domain.

## Join, or Die raster

The Join, or Die variants use the archival lossless restoration **Benjamin Franklin - Join or Die.png** from Wikimedia Commons.

- File page: https://commons.wikimedia.org/wiki/File:Benjamin_Franklin_-_Join_or_Die.png
- Download endpoint: https://commons.wikimedia.org/wiki/Special:Redirect/file/Benjamin%20Franklin%20-%20Join%20or%20Die.png
- Published dimensions: 3,740 × 2,696
- Published SHA-1: `7a79e6e41841667436d1ec2174b9caaa277248ad`
- Date of original political cartoon: 9 May 1754
- Attribution on Commons: Benjamin Franklin / restoration uploaded by Adam Cuerden
- Licensing: public domain / Public Domain Mark on the Commons file page.

The Join, or Die image is kept whole when mapped to the 3:2 source canvas. The pipeline pads it using a color sampled from the archival paper rather than cropping the snake, labels, or title.

## Raster treatment

`tools/fetch_source.py` verifies the published SHA-1 before accepting either source.

`tools/prepare_rasters.py` only performs raster operations:

- high-quality Lanczos resampling;
- mild sharpening appropriate to each source;
- optional restrained cloth/grime treatment for the `*-worn` variants.

No flag artwork is reconstructed.

## Deadlock / Source 2 references

- Rat King assets are under `models/heroes_wip/ratking/` in Deadlock's VPK; the build script discovers the current banner texture instead of hard-coding a filename that may change during development.
- ValveResourceFormat / Source 2 Viewer CLI is used to list and extract the current local asset.
- Reduced CSDK 12 / `resourcecompiler.exe` is used to compile the replacement.

No Valve texture is committed to this repository. The build process requires the user's own installed Deadlock files.
