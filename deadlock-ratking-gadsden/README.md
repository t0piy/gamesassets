# Rat King — Revolutionary Banners

Deadlock texture-replacement mod for Rat King's **Rule, Ratannia!** ultimate. It provides **six** raster-based variants across three designs: original/historical Gadsden, modern Gadsden, and **Join, or Die**.

> Deadlock is in active development. The Rat King asset path is discovered from your current game files at build time instead of baking in a fragile texture filename.

## Six variants

| Variant | Design | Treatment | Raster source |
|---|---|---|---|
| `original-clean` | historical Gadsden | archival/ochre clean | 1898 public-domain raster reproduction |
| `original-worn` | historical Gadsden | archival/ochre + restrained game wear | same 1898 raster |
| `modern-clean` | modern Gadsden | clean | `Gadsden flag large.png` |
| `modern-worn` | modern Gadsden | restrained game wear | same modern raster |
| `join-or-die-clean` | Join, or Die | clean archival print | 3740×2696 lossless PNG |
| `join-or-die-worn` | Join, or Die | restrained game wear | same archival PNG |

`modern-worn` remains the default.

## Raster-only sources

The project deliberately uses raster originals instead of SVG reconstruction.

- **Original Gadsden:** `Gadsden Flag.png`, a public-domain 1898 newspaper reproduction.
- **Modern Gadsden:** `Gadsden flag large.png`, the existing modern/common raster.
- **Join, or Die:** `Benjamin Franklin - Join or Die.png`, a 3740×2696 archival lossless restoration.

`tools/fetch_source.py` queries Wikimedia Commons metadata, verifies source dimensions and SHA-1, then downloads the exact original raster. The modern Gadsden and Join, or Die hashes are also pinned in the repository.

`tools/prepare_rasters.py` creates all six 4096px masters. The historical Gadsden reproduction is color-mapped from archival paper/ink into ochre cloth/brown ink so it reads as a banner while preserving the raster detail; no vector redraw occurs.

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
  -Variant original-worn `
  -DeadlockDir 'C:\Program Files (x86)\Steam\steamapps\common\Deadlock' `
  -Source2ViewerCli 'C:\Tools\Source2Viewer-CLI.exe' `
  -CsdkDir 'C:\Reduced_CSDK_12'
```

Supported values for `-Variant`:

```text
original-clean
original-worn
modern-clean
modern-worn
join-or-die-clean
join-or-die-worn
```

The build script downloads/verifies the raster originals when needed, prepares the requested 4K raster, then searches `models/heroes_wip/ratking/` for candidate `.vtex_c` files. If it cannot choose the banner texture unambiguously, it stops and prints candidates instead of guessing.

## GitHub build artifacts

The workflow `.github/workflows/deadlock-ratking-gadsden-package.yml` downloads and prepares the three source rasters once, then publishes **six separate source artifacts**, one per variant:

- `ratking-banner-original-clean-sources`
- `ratking-banner-original-worn-sources`
- `ratking-banner-modern-clean-sources`
- `ratking-banner-modern-worn-sources`
- `ratking-banner-join-or-die-clean-sources`
- `ratking-banner-join-or-die-worn-sources`

Each package contains the exact source raster used by that family, the processed 4096px PNG, preview PNG and source/license notes.

A compiled Deadlock VPK remains a local build because it depends on your installed Deadlock VPK and Source 2 compilation tools.

## Project layout

```text
tools/
  fetch_source.py           # fetch + metadata/SHA-1 verification for 3 raster sources
  prepare_rasters.py        # 3 originals → 6 clean/worn 4096px variants
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
    gadsden-historical-original.png
    gadsden-original.png
    join-or-die-original.png
    original-clean-4096.png
    original-worn-4096.png
    modern-clean-4096.png
    modern-worn-4096.png
    join-or-die-clean-4096.png
    join-or-die-worn-4096.png
  previews/
    original-clean.png
    original-worn.png
    modern-clean.png
    modern-worn.png
    join-or-die-clean.png
    join-or-die-worn.png
```

## Disclaimer

Unofficial community mod. Not affiliated with or endorsed by Valve. Deadlock and its assets are property of their respective owners.
