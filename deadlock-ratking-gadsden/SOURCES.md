# Art and technical references

This project is raster-only. It does not redraw any flag and contains no SVG asset pipeline.

## Original / accurate Gadsden raster

The `original-*` variants use the same **Gadsden Flag (Accurate)** appearance used as the project's first historical reference.

- File page: https://commons.wikimedia.org/wiki/File:Gadsden_Flag_(Accurate).svg
- Commons source dimensions: 1,614 × 1,014
- Source SHA-1: `5ee2386154327e7be90b7ff48134fd4a0e5ad092`
- Author: BlinxTheKitty
- Licensing: CC0 1.0 / public-domain dedication.
- Raster downloaded by this project: the large PNG preview rendered by Wikimedia Commons (3840px wide; served PNG decodes as 3840×2413).

The project does not download, store, convert, or process the SVG file. `tools/fetch_source.py` requests the PNG rendition and validates source metadata and raster dimensions.

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

## Rat King material and texture compatibility

For interoperability testing, the project inspected the public **Turkish Flag for Ratking** mod:

- GameBanana: https://gamebanana.com/mods/723299
- Purpose: establish the resource layout and on-wire texture parameters of a banner replacement known to work in Deadlock.
- The mod's flag artwork is not redistributed.

The working VPK contains the Rat King material and generated texture resources. Inspection of its material established:

```text
models/heroes_wip/ratking/materials/ratking_ratannia_flag.vmat_c
```

Material properties relevant to this project:

- shader: `pbr.vfx`
- `F_ALPHA_TEST = 1`
- `F_DISABLE_NPR_OUTLINE = 1`
- `F_RENDER_BACKFACES = 1`
- `F_USE_NPR_LIGHTING = 1`
- `F_USE_STATUS_EFFECTS_PROXY = 1`
- alpha-test reference: 0.5

Its color texture is:

- 2048 × 1024
- BC7
- 9 mip levels
- flags 0

### Current DMM build strategy

The first version of this repository's DMM artifact only replaced a color VTEX. That VPK was structurally valid but was not sufficient in the user's in-game test.

The current builder therefore:

1. prepares this project's raster artwork;
2. uses the working color resource only as a **technical container template** so output retains BC7, the full 9-mip chain, and the banner alpha;
3. fully replaces the template's color pixels with this project's artwork;
4. byte-faithfully patches the working Rat King `pbr.vfx` material's DATA texture binding so `g_tColor` points to a new per-variant texture path;
5. redirects the donor material's generated auxiliary texture slots to stable game defaults:
   - `g_tNormalRoughness` → `materials/default/default_normal_tga_7be61377.vtex`
   - `g_tNprTransmissiveColor` → `materials/default/default_black_mask_tga_e7be3cc.vtex`
   - `g_tTintMaskRimLightMask` → `materials/default/default_mask_tga_8d0774e6.vtex`
6. packs exactly two entries into the final VPK: the patched Rat King material and the generated color VTEX;
7. validates the result with Deadlock Mod Manager's own VPK parser before publishing.

The material patch uses the pinned open-source `morphic` material tooling from `Slush97/vpkmerge`, whose compiled-material path preserves the engine-accepted v5 layout/non-DATA shader blocks rather than generating a simplified material that can fall back to an error shader.

## Deadlock Mod Manager compatibility

Deadlock Mod Manager accepts a raw `.vpk` or an archive containing at least one `.vpk`. The current workflow publishes six `*-DMM` artifacts, each containing one generated `*_dir.vpk`.

Older `*-sources` artifacts are not installable mods. Older one-texture `*-DMM` artifacts are also superseded by the current material-bound build.

## Raster treatment

`tools/prepare_rasters.py` performs only raster operations:

- high-quality Lanczos resampling;
- mild sharpening appropriate to each source;
- optional restrained cloth/grime treatment for `*-worn` variants.

`tools/prepare_dmm_payloads.py` then prepares a 2048×1024 raster for the game texture slot.

## Local Source 2 build

The optional local build uses:

- ValveResourceFormat / Source 2 Viewer CLI to inspect the user's installed game;
- Reduced CSDK 12 / `resourcecompiler.exe` to compile replacements locally.

No Valve texture is committed to this repository.
