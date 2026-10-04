# Rat King — Revolutionary Banners

Deadlock texture-replacement mod for Rat King's **Rule, Ratannia!** ultimate. It currently provides Gadsden and **Join, or Die** banner treatments using verified raster originals and the real Rat King banner's local alpha/lighting during build.

> Deadlock is in active development. The Rat King asset path is discovered from your current game files at build time instead of baking in a fragile texture filename.

## Variants

| Variant | Design | Treatment | Source |
|---|---|---|---|
| `modern-clean` | Gadsden | clean | original raster + 4096px master |
| `modern-worn` | Gadsden | restrained game-like wear | original raster + 4096px master |
| `join-or-die-clean` | Join, or Die | clean archival print | original 3740×2696 PNG + 4096px master |
| `join-or-die-worn` | Join, or Die | restrained game-like wear | original 3740×2696 PNG + 4096px master |

`modern-worn` remains the default; `join-or-die-worn` is the recommended Join, or Die version.

## Raster sources

The project deliberately uses raster originals instead of SVG reconstruction.

- Gadsden: `Gadsden flag large.png`, verified by its published SHA-1.
- Join, or Die: `Benjamin Franklin - Join or Die.png`, a 3740×2696 archival lossless restoration, also verified by its published SHA-1.

`tools/fetch_source.py` downloads and checks both source images before processing. `tools/prepare_rasters.py` creates the 4096px clean/worn masters.

For Join, or Die, the complete historical print is preserved: the pipeline pads it to the flag canvas using the archival paper color instead of cropping the snake, colony labels, or title.

The final game-matching step happens in `compose_texture.py`: it uses the Rat King banner texture extracted from your own current Deadlock install so the replacement inherits the game's actual alpha silhouette and part of its cloth lighting/wear.

## Why there is no Valve texture in this repo

The project intentionally does not redistribute the original Deadlock texture. `tools/build.ps1` extracts the current Rat King banner from **your own local Deadlock installation**, composes the selected raster into the same canvas, then compiles the replacement back to the same Source 2 virtual path.

## Local build (Windows)

Requirements:

- Deadlock installed locally.
- [Source 2 Viewer / ValveResourceFormat CLI](https://s2v.app/) (`Source2Viewer-CLI.exe`).
- Reduced CSDK 12 with `resourcecompiler.exe`; `vpk.exe` is optional but enables a `.vpk` output.
- Python 3 with Pillow (`py -m pip install pillow`).
- Internet access on the first build if the verified raster sources have not already been fetched.

Example:

```powershell
pwsh -File .\tools\build.ps1 `
  -Variant join-or-die-worn `
  -DeadlockDir 'C:\Program Files (x86)\Steam\steamapps\common\Deadlock' `
  -Source2ViewerCli 'C:\Tools\Source2Viewer-CLI.exe' `
  -CsdkDir 'C:\Reduced_CSDK_12'
```

Supported values for `-Variant`:

```text
modern-clean
modern-worn
join-or-die-clean
join-or-die-worn
```

The build script downloads/verifies the raster originals when needed, prepares the requested 4K raster, then searches `models/heroes_wip/ratking/` for candidate `.vtex_c` files. If it cannot choose the banner texture unambiguously, it stops and prints candidates instead of guessing.

```powershell
pwsh -File .\tools\build.ps1 ... -TexturePath 'models/heroes_wip/ratking/.../banner.vtex_c'
```

Outputs are written to `dist/`:

- `ratking-banner-<variant>.vpk` when the CSDK provides `vpk.exe`;
- `ratking-banner-<variant>-loose.zip`;
- `ratking-banner-<variant>-target.txt`.

## GitHub build artifacts

The workflow `.github/workflows/deadlock-ratking-gadsden-package.yml` has a four-entry matrix and publishes exactly one source artifact for each current variant:

- `ratking-banner-modern-clean-sources`
- `ratking-banner-modern-worn-sources`
- `ratking-banner-join-or-die-clean-sources`
- `ratking-banner-join-or-die-worn-sources`

Each package contains the exact source raster used by that family, the processed 4096px PNG, preview PNG and source/license notes.

A compiled Deadlock VPK remains a local build because it depends on your installed Deadlock VPK and Source 2 compilation tools.

## Project layout

```text
tools/
  fetch_source.py           # download + SHA-1 verify both raster originals
  prepare_rasters.py        # originals → four clean/worn 4096px variants
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
    join-or-die-original.png
    modern-clean-4096.png
    modern-worn-4096.png
    join-or-die-clean-4096.png
    join-or-die-worn-4096.png
  previews/
    modern-clean.png
    modern-worn.png
    join-or-die-clean.png
    join-or-die-worn.png
```

## Disclaimer

Unofficial community mod. Not affiliated with or endorsed by Valve. Deadlock and its assets are property of their respective owners.
