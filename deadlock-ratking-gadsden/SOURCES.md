# Art and technical references

## Flag raster

The mod uses the exact raster image published as **Gadsden flag large.png** on Wikimedia Commons.

- File page: https://commons.wikimedia.org/wiki/File:Gadsden_flag_large.png
- Direct raster: https://upload.wikimedia.org/wikipedia/commons/a/a1/Gadsden_flag_large.png
- Published dimensions: 900 × 600
- Published SHA-1: `ad1c2fa16219d59b975c29a8e290bc9c1587ab68`
- Original upload: Vikrum~commonswiki; later raster revision by Ptkfgs
- Licensing shown on the file page: GFDL and CC BY-SA 2.0 / 3.0; the underlying historical design is also marked public domain.

`tools/fetch_source.py` verifies the SHA-1 before the image is accepted. The project does not redraw the flag. The 4096px clean and worn files are raster treatments derived from this exact source.

The historical variants were intentionally dropped because the raster-only historical references available for this pass were not strong enough to match the game's texture quality.

## Deadlock / Source 2 references

- Rat King assets are under `models/heroes_wip/ratking/` in Deadlock's VPK; the build script discovers the current banner texture instead of hard-coding a filename that may change during development.
- ValveResourceFormat / Source 2 Viewer CLI is used to list and extract the current local asset.
- Reduced CSDK 12 / `resourcecompiler.exe` is used to compile the replacement.

No Valve texture is committed to this repository. The build process requires the user's own installed Deadlock files.
