# Rat King — Gadsden Banner

Deadlock texture-replacement mod for Rat King's **Rule, Ratannia!** ultimate. The mod now uses a real raster flag image from Wikimedia Commons as its source and only applies high-quality resampling, restrained wear, and the actual Rat King banner's local shading/alpha during build.

> Deadlock is in active development. The Rat King asset path is discovered from your current game files at build time instead of baking in a fragile texture filename.

## Variants

| Variant | Style | Source |
|---|---|---|
| `modern-clean` | Clean modern Gadsden image, upscaled from the exact published raster | Original PNG + 4096px PNG |
| `modern-worn` | Same published raster with restrained wear before the game's own banner shading is applied | Original PNG + 4096px PNG |

`modern-worn` is the recommended default.

The previous historical set was removed because the raster-only historical material I found was not good enough to justify a lower-fidelity result. This follows the project's original fallback rule: when the historical version cannot be made convincingly game-authentic, prefer the stronger modern source.

## Raster source

The source file is the exact published `Gadsden flag large.png` raster from Wikimedia Commons. `tools/fetch_source.py` downloads it and verifies its published SHA-1 before anything is processed.

No artwork is redrawn. `tools/prepare_rasters.py` only:

- resamples the exact source to a 4096px master with Lanczos;
- applies mild sharpening to compensate for enlargement;
- optionally adds restrained cloth/grime variation for `modern-worn`.

The more important game-matching step happens later: `compose_texture.py` uses the banner texture extracted from your own current Deadlock install so the replacement inherits its real alpha silhouette and part of its cloth lighting/wear.

## Why there is no Valve texture in this repo

The project intentionally does not redistribute the original Deadlock texture. `tools/build.ps1` extracts the current Rat King banner from **your own local Deadlock installation**, composes the raster flag into the same canvas, then compiles the replacement back to the same Source 2 virtual path.

## Local build (Windows)

Requirements:

- Deadlock installed locally.
- [Source 2 Viewer / ValveResourceFormat CLI](https://s2v.app/) (`Source2Viewer-CLI.exe`).
- Reduced CSDK 12 with `resourcecompiler.exe`; `vpk.exe` is optional but enables a `.vpk` output.
- Python 3 with Pillow (`py -m pip install pillow`).
- Internet access on the first build if `assets/source/gadsden-original.png` has not already been fetched.

Example:

```powershell
pwsh -File .\tools\build.ps1 `
  -Variant modern-worn `
  -DeadlockDir 'C:\Program Files (x86)\Steam\steamapps\common\Deadlock' `
  -Source2ViewerCli 'C:\Tools\Source2Viewer-CLI.exe' `
  -CsdkDir 'C:\Reduced_CSDK_12'
```

The build script downloads/verifies the original raster when needed, prepares the requested 4K raster, then searches `models/heroes_wip/ratking/` for candidate `.vtex_c` files. If it cannot choose the banner texture unambiguously, it stops and prints candidates instead of guessing.

```powershell
pwsh -File .\tools\build.ps1 ... -TexturePath 'models/heroes_wip/ratking/.../banner.vtex_c'
```

Outputs are written to `dist/`:

- `ratking-gadsden-<variant>.vpk` when the CSDK provides `vpk.exe`;
- `ratking-gadsden-<variant>-loose.zip`;
- `ratking-gadsden-<variant>-target.txt`.

## GitHub build artifacts

The workflow `.github/workflows/deadlock-ratking-gadsden-package.yml` produces one source artifact per current variant. Each artifact contains:

- the exact downloaded source PNG;
- the 4096px processed PNG;
- a preview PNG;
- source/license notes.

The workflow also cleans older Rat King source artifacts before uploading the current raster-only set.

A compiled Deadlock VPK remains a local build because it depends on your installed Deadlock VPK and Source 2 compilation tools.

## Project layout

```text
tools/
  fetch_source.py           # download + SHA-1 verify the exact raster source
  prepare_rasters.py        # source raster → clean/worn 4096px variants
  compose_texture.py        # inherit real Rat King alpha + cloth shading
  build.ps1                 # discover → extract → compose → compile → VPK
  package_sources.py        # CI artifact packager
SOURCES.md
LICENSE
mod.json
```

Generated locally/CI:

```text
assets/
  source/
    gadsden-original.png
    modern-clean-4096.png
    modern-worn-4096.png
  previews/
    modern-clean.png
    modern-worn.png
```

## Disclaimer

Unofficial community mod. Not affiliated with or endorsed by Valve. Deadlock and its assets are property of their respective owners.
