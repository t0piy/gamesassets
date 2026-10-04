# Rat King — Gadsden Banner

Deadlock texture-replacement mod for Rat King's **Rule, Ratannia!** ultimate. It replaces the banner art with a Gadsden-inspired flag while preserving the real in-game banner's dimensions, alpha mask, and part of its cloth/wear shading during the local build.

> Deadlock is in active development. The Rat King asset path is discovered from your current game files at build time instead of baking in a fragile texture filename.

## Variants

| Variant | Style | Source files |
|---|---|---|
| `historical-original` | Original/historical-inspired, warmer ochre and brown snake | SVG + 4096px PNG |
| `historical-worn` | Historical-inspired with heavier age/wear | SVG + 4096px PNG |
| `modern-clean` | Modern/common high-contrast Gadsden treatment | SVG + 4096px PNG |
| `modern-worn` | Modern treatment with in-world wear; **recommended default** | SVG + 4096px PNG |

Previews live in [`assets/previews`](assets/previews). Master artwork lives in [`assets/source`](assets/source). The SVGs are the canonical sources so the art can be rasterized at the exact texture resolution without quality loss.

## Why there is no Valve texture in this repo

The project intentionally does not redistribute the original Deadlock texture. `tools/build.ps1` extracts the current Rat King banner from **your own local Deadlock installation**, uses its exact canvas/alpha and a small amount of its wear shading, then compiles the replacement back to the same Source 2 virtual path.

This also makes the mod more resilient to pre-release asset changes.

## Local build (Windows)

Requirements:

- Deadlock installed locally.
- [Source 2 Viewer / ValveResourceFormat CLI](https://s2v.app/) (`Source2Viewer-CLI.exe`).
- Reduced CSDK 12 with `resourcecompiler.exe`; `vpk.exe` is optional but enables a `.vpk` output.
- Python 3 with Pillow (`py -m pip install pillow`).

Example:

```powershell
pwsh -File .\tools\build.ps1 `
  -Variant modern-worn `
  -DeadlockDir 'C:\Program Files (x86)\Steam\steamapps\common\Deadlock' `
  -Source2ViewerCli 'C:\Tools\Source2Viewer-CLI.exe' `
  -CsdkDir 'C:\Reduced_CSDK_12'
```

The script searches `models/heroes_wip/ratking/` for candidate `.vtex_c` files. If it cannot choose the banner texture unambiguously, it stops and prints the candidates instead of guessing. Re-run with the exact path:

```powershell
pwsh -File .\tools\build.ps1 ... -TexturePath 'models/heroes_wip/ratking/.../banner.vtex_c'
```

Outputs are written to `dist/`:

- `ratking-gadsden-<variant>.vpk` when the CSDK provides `vpk.exe`;
- `ratking-gadsden-<variant>-loose.zip` as a loose compiled fallback/inspection package;
- `ratking-gadsden-<variant>-target.txt` recording the exact current game asset overridden.

## Installation

Use the `.vpk` with your normal Deadlock mod workflow/mod manager. Because the packed resource keeps the game's original virtual asset path, Source 2 resolves it as an override rather than requiring gameplay/script edits.

If a Deadlock update changes the Rat King banner asset, rebuild: the discovery step is designed specifically for that case.

## GitHub build artifacts

The GitHub Actions workflow creates one artifact per variant containing the high-quality SVG, 4096px PNG, preview, license and source notes. A fully compiled Deadlock VPK is intentionally a **local** build because it depends on your installed Deadlock VPK and Reduced CSDK toolchain; the workflow does not fake or redistribute those proprietary inputs.

## Artwork / fidelity

The source art was redrawn as scalable vector artwork for this mod, using public historical/common Gadsden references. The local composition step is what makes it feel closer to the actual Rat King banner: it keeps the base texture's alpha and gently reuses its cloth luminance/wear instead of simply dropping a flat yellow rectangle onto the mesh.

See [`SOURCES.md`](SOURCES.md) for references and licensing notes.

## Project layout

```text
assets/
  previews/                 # lightweight previews
  source/                   # canonical SVG + 4096px raster variants
tools/
  build.ps1                 # discover → extract → compose → compile → VPK
  compose_texture.py        # preserves alpha + cloth/wear shading
  make_assets.py            # reproducible source-art generator
  package_sources.py        # CI artifact packager
.github/workflows/
  package.yml               # one source artifact per variant
SOURCES.md
LICENSE
```

## Disclaimer

Unofficial community mod. Not affiliated with or endorsed by Valve. Deadlock and its assets are property of their respective owners.
