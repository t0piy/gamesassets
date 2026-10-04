# Art and technical references

The bundled flag artwork is an original vector reconstruction made for this mod. It does **not** redistribute Valve's Rat King texture.

## Flag references

- **Historical / original-inspired:** Wikimedia Commons, *Gadsden Flag (Accurate).svg*, by BlinxTheKitty, CC0 1.0. Commons describes it as a likely accurate depiction based on vintage references.
  https://commons.wikimedia.org/wiki/File:Gadsden_Flag_(Accurate).svg
- **Modern / common reconstruction:** Wikimedia Commons, *Gadsden flag.svg*. The underlying 1775 design is public domain; this particular SVG page lists its vector-file licensing separately.
  https://commons.wikimedia.org/wiki/File:Gadsden_flag.svg

The repository's own SVG paths were redrawn rather than copied from the Commons SVG files, allowing the mod source itself to remain under the repository license below.

## Deadlock / Source 2 references

- Rat King assets are currently under `models/heroes_wip/ratking/` in Deadlock's VPK; the banner texture is in its `materials` subtree. The build script discovers the exact current `.vtex_c` path instead of hard-coding a filename that may change during Deadlock development.
- ValveResourceFormat / Source 2 Viewer CLI is used to list/decompile the VPK locally.
- Reduced CSDK 12 / `resourcecompiler.exe` is used to compile the replacement VTEX locally.

No game asset is committed to this repository. The build process requires your legally installed local Deadlock files.
