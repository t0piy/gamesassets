use std::env;
use std::fs;
use std::path::{Path, PathBuf};

use vpkmanager::source2::texture::encode_vtex_png_rgba8888_from_png;
use vpkmanager::source2::{inspect, TextureFlags};

const TARGET: &str =
    "models/heroes_wip/ratking/materials/ratking_ratannia_flag_color_png_155b4b23.vtex_c";

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 {
        eprintln!("usage: {} <input.png> <output_dir.vpk> <staging_dir>", args[0]);
        std::process::exit(2);
    }

    let png_path = PathBuf::from(&args[1]);
    let output_vpk = PathBuf::from(&args[2]);
    let staging = PathBuf::from(&args[3]);

    if staging.exists() {
        fs::remove_dir_all(&staging)?;
    }
    fs::create_dir_all(&staging)?;

    let png = fs::read(&png_path)?;
    let vtex = encode_vtex_png_rgba8888_from_png(&png, TextureFlags::empty())?;
    let info = inspect(&vtex)?;
    if info.width != 2048 || info.height != 1024 {
        return Err(format!(
            "generated VTEX has unexpected dimensions {}x{}",
            info.width, info.height
        ).into());
    }

    let target = staging.join(Path::new(TARGET));
    fs::create_dir_all(target.parent().expect("target has parent"))?;
    fs::write(&target, vtex)?;

    if let Some(parent) = output_vpk.parent() {
        fs::create_dir_all(parent)?;
    }
    if output_vpk.exists() {
        fs::remove_file(&output_vpk)?;
    }

    let count = vpkmanager::pack_directory(&staging, &output_vpk)?;
    if count != 1 {
        return Err(format!("expected 1 VPK entry, packed {count}").into());
    }

    // Validate with the exact parser used by Deadlock Mod Manager rather than
    // older third-party VPK readers that do not understand DMM's VPK v2 hashes.
    let entries = vpk_parser::VpkParser::parse_directory_from_file(&output_vpk)?;
    if entries.len() != 1 || entries[0].full_path != TARGET {
        return Err(format!(
            "DMM parser saw unexpected VPK entries: {:?}",
            entries.iter().map(|e| e.full_path.as_str()).collect::<Vec<_>>()
        ).into());
    }

    println!(
        "built+validated {} from {} -> {} ({}x{}, {:?}, flags={:?})",
        output_vpk.display(),
        png_path.display(),
        TARGET,
        info.width,
        info.height,
        info.format,
        info.flags
    );
    Ok(())
}
