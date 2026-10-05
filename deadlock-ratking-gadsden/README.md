# Rat King — Revolutionary Banners

Texture-replacement mod for Rat King's **Rule, Ratannia!** ultimate in Deadlock. It provides six variants across three designs: the original/accurate Gadsden treatment, a modern Gadsden, and **Join, or Die**.

## Install with Deadlock Mod Manager

**Use only artifacts whose names end in `-DMM` from the latest successful workflow run.**

1. Disable/remove any older version of this mod from Deadlock Mod Manager.
2. Open the latest successful **Rat King Revolutionary Banner DMM artifacts** workflow run.
3. Download exactly one variant, for example `ratking-banner-modern-worn-DMM`.
4. GitHub downloads the artifact as a ZIP. **Do not extract it.**
5. In Deadlock Mod Manager, open **Mods Library → Add Local Mod**.
6. Drop the ZIP into the upload area, finish adding it, and enable it.
7. Restart Deadlock.

Install only one banner variant at a time because all six override the same Rat King material.

### Important: old DMM artifacts are obsolete

The first DMM-compatible build contained only a color `.vtex_c`. Deadlock Mod Manager accepted that VPK, but in-game Rat King could keep using the original material binding, so the flag did not visibly change.

The current build fixes this by overriding the **material and its color texture together**.

## Six variants

| Variant | Design | Treatment | Raster source |
|---|---|---|---|
| `original-clean` | original/accurate Gadsden | clean | Commons-rendered PNG of **Gadsden Flag (Accurate)** |
| `original-worn` | original/accurate Gadsden | restrained game-like wear | same Accurate raster |
| `modern-clean` | modern Gadsden | clean | `Gadsden flag large.png` |
| `modern-worn` | modern Gadsden | restrained game-like wear | same modern raster |
| `join-or-die-clean` | Join, or Die | clean archival print | 3740×2696 lossless PNG |
| `join-or-die-worn` | Join, or Die | restrained game-like wear | same archival PNG |

`modern-worn` remains the default recommendation.

## What is inside the fixed installable VPK

Each VPK now contains exactly two resources:

```text
models/heroes_wip/ratking/materials/
  ratking_ratannia_flag.vmat_c
  ratking_revolutionary_<variant>_color.vtex_c
```

The material override explicitly points `g_tColor` at the variant texture. This removes the previous assumption that the stock material would resolve a generated texture filename on its own.

The generated color texture is validated as:

- **2048 × 1024**
- **BC7**
- **9 mip levels**
- texture flags **0**
- alpha silhouette preserved from a known-working Rat King flag texture

The material is the actual Rat King `pbr.vfx` layout used by a working banner replacement. Its compiled DATA binding is patched to this project's texture, while the auxiliary authored slots are redirected to stable game default textures. The resulting VPK is validated with the same VPK parser used by Deadlock Mod Manager before it is uploaded.

## Technical reference

A public working Rat King flag mod was inspected only to establish the actual material structure, texture parameters, and working resource paths. Its flag artwork is not included in this project.

The working material confirmed:

- material path: `models/heroes_wip/ratking/materials/ratking_ratannia_flag.vmat_c`
- shader: `pbr.vfx`
- `F_ALPHA_TEST = 1`
- `F_RENDER_BACKFACES = 1`
- `F_USE_NPR_LIGHTING = 1`
- working color texture: BC7 2048×1024, 9 mips, flags 0

This is why the current build overrides the material instead of shipping only a texture.

## Raster-only artwork

The project does not store or process an SVG asset.

- **Original Gadsden:** Wikimedia Commons' rendered 3840px PNG preview of `Gadsden Flag (Accurate)`.
- **Modern Gadsden:** `Gadsden flag large.png`.
- **Join, or Die:** archival lossless `Benjamin Franklin - Join or Die.png`.

`tools/fetch_source.py` validates the source metadata. `tools/prepare_rasters.py` performs raster resampling, sharpening, and optional wear.

## GitHub Actions artifacts

The current workflow publishes six installable artifacts:

- `ratking-banner-original-clean-DMM`
- `ratking-banner-original-worn-DMM`
- `ratking-banner-modern-clean-DMM`
- `ratking-banner-modern-worn-DMM`
- `ratking-banner-join-or-die-clean-DMM`
- `ratking-banner-join-or-die-worn-DMM`

Each downloaded artifact ZIP contains one `*_dir.vpk` and can be passed directly to **Add Local Mod**.

## Optional local build

The older local CSDK build pipeline remains available for people who specifically want to compile against their own installed Deadlock resources.

Requirements:

- Deadlock installed locally.
- Source 2 Viewer / ValveResourceFormat CLI.
- Reduced CSDK 12 with `resourcecompiler.exe`; `vpk.exe` is optional.
- Python 3 with Pillow.

Example:

```powershell
pwsh -File .\tools\build.ps1 `
  -Variant modern-worn `
  -DeadlockDir 'C:\Program Files (x86)\Steam\steamapps\common\Deadlock' `
  -Source2ViewerCli 'C:\Tools\Source2Viewer-CLI.exe' `
  -CsdkDir 'C:\Reduced_CSDK_12'
```

Supported values:

```text
original-clean
original-worn
modern-clean
modern-worn
join-or-die-clean
join-or-die-worn
```

## Project layout

```text
tools/
  fetch_source.py
  prepare_rasters.py
  prepare_dmm_payloads.py
  dmm_vpk_builder.rs
  compose_texture.py
  build.ps1
  package_sources.py
SOURCES.md
LICENSE
mod.json
```

## Disclaimer

Unofficial community mod. Not affiliated with or endorsed by Valve. Deadlock and its assets are property of their respective owners.
