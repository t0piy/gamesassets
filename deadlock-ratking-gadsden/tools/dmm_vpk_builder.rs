use std::env;
use std::fs;
use std::io::Cursor;
use std::path::{Path, PathBuf};

use image::{DynamicImage, ImageFormat, RgbaImage};
use vpkmanager::source2::{ImageData, TextureFormat, inspect};

const MATERIAL_ENTRY: &str =
    "models/heroes_wip/ratking/materials/ratking_ratannia_flag.vmat_c";
const MATERIAL_SOURCE_NAME: &str =
    "models/heroes_wip/ratking/materials/ratking_ratannia_flag.vmat";

const DEFAULT_NORMAL: &str = "materials/default/default_normal_tga_7be61377.vtex";
const DEFAULT_BLACK_MASK: &str = "materials/default/default_black_mask_tga_e7be3cc.vtex";
const DEFAULT_TINT_RIM_MASK: &str = "materials/default/default_mask_tga_8d0774e6.vtex";

fn safe_variant(value: &str) -> String {
    value
        .chars()
        .map(|c| if c.is_ascii_alphanumeric() { c } else { '_' })
        .collect()
}

fn png_with_template_alpha(
    input_png: &[u8],
    template_vtex: &[u8],
) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
    let template = vpkmanager::source2::decode(template_vtex)?;
    if template.width != 2048 || template.height != 1024 {
        return Err(format!(
            "donor texture is {}x{}, expected 2048x1024",
            template.width, template.height
        ).into());
    }

    let mut source = image::load_from_memory(input_png)?.to_rgba8();
    if source.dimensions() != (2048, 1024) {
        return Err(format!(
            "prepared raster is {:?}, expected 2048x1024",
            source.dimensions()
        ).into());
    }

    if let ImageData::Rgba8(template_rgba) = template.data {
        for (dst, src) in source.as_mut().chunks_exact_mut(4).zip(template_rgba.chunks_exact(4)) {
            dst[3] = src[3];
        }
    } else {
        return Err("donor flag texture unexpectedly uses HDR pixels".into());
    }

    let mut encoded = Cursor::new(Vec::new());
    DynamicImage::ImageRgba8(RgbaImage::from_raw(2048, 1024, source.into_raw())
        .ok_or("failed to construct RGBA image")?)
        .write_to(&mut encoded, ImageFormat::Png)?;
    Ok(encoded.into_inner())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 7 {
        eprintln!(
            "usage: {} <variant> <input.png> <template-color.vtex_c> <donor.vmat_c> <output_dir.vpk> <staging_dir>",
            args[0]
        );
        std::process::exit(2);
    }

    let variant = safe_variant(&args[1]);
    let png_path = PathBuf::from(&args[2]);
    let template_vtex_path = PathBuf::from(&args[3]);
    let donor_vmat_path = PathBuf::from(&args[4]);
    let output_vpk = PathBuf::from(&args[5]);
    let staging = PathBuf::from(&args[6]);

    if staging.exists() {
        fs::remove_dir_all(&staging)?;
    }
    fs::create_dir_all(&staging)?;

    let input_png = fs::read(&png_path)?;
    let template_vtex = fs::read(&template_vtex_path)?;
    let donor_vmat = fs::read(&donor_vmat_path)?;

    // Rebuild color pixels inside the same BC7/9-mip texture container used by
    // a known-working Rat King flag replacement. The donor alpha is preserved.
    let composed_png = png_with_template_alpha(&input_png, &template_vtex)?;
    let edited = vpkmanager::replace_texture_image(&template_vtex, &composed_png)?;
    let color_info = inspect(&edited.bytes)?;
    if color_info.width != 2048
        || color_info.height != 1024
        || color_info.mip_count != 9
        || color_info.flags.bits() != 0
        || color_info.format != TextureFormat::Bc7
    {
        return Err(format!(
            "unexpected output VTEX: {}x{}, {:?}, mips={}, flags={}",
            color_info.width,
            color_info.height,
            color_info.format,
            color_info.mip_count,
            color_info.flags.bits()
        ).into());
    }

    // Give each variant its own resource path. The material override makes this
    // binding explicit instead of relying on the stock material's generated name.
    let color_source = format!(
        "models/heroes_wip/ratking/materials/ratking_revolutionary_{}_color.vtex",
        variant
    );
    let color_entry = format!("{}_c", color_source);

    // Keep the exact engine-accepted material layout/flags from the working
    // Rat King flag donor, while redirecting authored texture slots to our color
    // and stable global defaults. compile_pbr_vmat patches the v5 DATA block
    // byte-faithfully and preserves the donor's non-DATA shader blocks.
    let donor_mat = morphic::material::parse(&donor_vmat)?;
    if donor_mat.shader_name != "pbr.vfx" {
        return Err(format!("unexpected donor shader: {}", donor_mat.shader_name).into());
    }

    let patched_vmat = morphic::compile_pbr_vmat(
        &donor_vmat,
        MATERIAL_SOURCE_NAME,
        &[
            ("g_tColor", color_source.as_str()),
            ("g_tNormalRoughness", DEFAULT_NORMAL),
            ("g_tNprTransmissiveColor", DEFAULT_BLACK_MASK),
            ("g_tTintMaskRimLightMask", DEFAULT_TINT_RIM_MASK),
        ],
    )?;

    let check_mat = morphic::material::parse(&patched_vmat)?;
    if check_mat.texture("g_tColor") != Some(color_source.as_str()) {
        return Err("patched material does not reference generated color texture".into());
    }

    let material_target = staging.join(Path::new(MATERIAL_ENTRY));
    fs::create_dir_all(material_target.parent().expect("material parent"))?;
    fs::write(&material_target, patched_vmat)?;

    let color_target = staging.join(Path::new(&color_entry));
    fs::create_dir_all(color_target.parent().expect("color parent"))?;
    fs::write(&color_target, edited.bytes)?;

    if let Some(parent) = output_vpk.parent() {
        fs::create_dir_all(parent)?;
    }
    if output_vpk.exists() {
        fs::remove_file(&output_vpk)?;
    }

    let count = vpkmanager::pack_directory(&staging, &output_vpk)?;
    if count != 2 {
        return Err(format!("expected 2 VPK entries, packed {count}").into());
    }

    // Validate with the exact directory parser used by Deadlock Mod Manager.
    let mut entries = vpk_parser::VpkParser::parse_directory_from_file(&output_vpk)?;
    entries.sort_by(|a, b| a.full_path.cmp(&b.full_path));
    let paths: Vec<&str> = entries.iter().map(|e| e.full_path.as_str()).collect();
    if paths.len() != 2
        || !paths.contains(&MATERIAL_ENTRY)
        || !paths.contains(&color_entry.as_str())
    {
        return Err(format!("DMM parser saw unexpected VPK entries: {:?}", paths).into());
    }

    println!(
        "built+validated {}: material={} color={} (BC7 2048x1024, 9 mips, donor alpha)",
        output_vpk.display(),
        MATERIAL_ENTRY,
        color_entry
    );
    Ok(())
}
