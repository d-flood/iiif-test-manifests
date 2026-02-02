"""Image processing script for IIIF Test Manifests.

This script handles tiling source images into IIIF Image API format using vips.
Can be run standalone or imported by the main build script.
"""

import argparse
import json
import shutil
import subprocess
from pathlib import Path

# Thumbnail size for viewer previews
THUMBNAIL_SIZE = 400


def check_vips_installed():
    """Check if vips is available in the system path."""
    return shutil.which("vips") is not None


def get_image_dimensions(img_path):
    """Get the width and height of an image using vips."""
    try:
        result = subprocess.run(
            ["vipsheader", "-f", "width", str(img_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        width = int(result.stdout.strip())

        result = subprocess.run(
            ["vipsheader", "-f", "height", str(img_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        height = int(result.stdout.strip())

        return width, height
    except subprocess.CalledProcessError:
        return None, None


def generate_thumbnail(img_file, img_out_dir, orig_width, orig_height):
    """Generate a single thumbnail for viewer previews.

    Creates: full/{width},{height}/0/default.jpg
    """
    # Calculate thumbnail dimensions maintaining aspect ratio
    if orig_width >= orig_height:
        thumb_width = THUMBNAIL_SIZE
        thumb_height = round(orig_height * (THUMBNAIL_SIZE / orig_width))
    else:
        thumb_height = THUMBNAIL_SIZE
        thumb_width = round(orig_width * (THUMBNAIL_SIZE / orig_height))

    # Create directory structure: full/{width},{height}/0/default.jpg
    thumb_dir = img_out_dir / "full" / f"{thumb_width},{thumb_height}" / "0"
    thumb_dir.mkdir(parents=True, exist_ok=True)
    thumb_output = thumb_dir / "default.jpg"

    try:
        subprocess.run(
            [
                "vips",
                "thumbnail",
                str(img_file),
                str(thumb_output),
                str(THUMBNAIL_SIZE),
            ],
            check=True,
            capture_output=True,
        )
        print(f"  Generated thumbnail {thumb_width}x{thumb_height}")
        return {"width": thumb_width, "height": thumb_height}
    except subprocess.CalledProcessError as e:
        print(f"  Warning: Failed to generate thumbnail: {e}")
        return None


def ensure_images_dir(site_dir):
    """Ensure the images directory exists in the site directory."""
    site_path = Path(site_dir)
    images_path = site_path / "images"
    if not site_path.exists():
        site_path.mkdir(parents=True)
    if not images_path.exists():
        images_path.mkdir()
    return images_path


def process_images(src_dir, dest_dir, base_url):
    """Process source images into IIIF tiles.

    Args:
        src_dir: Directory containing source images
        dest_dir: Site directory to output tiles to
        base_url: Base URL for the deployment
    """
    print("Processing images...")

    if not check_vips_installed():
        print("Warning: 'vips' is not installed. Skipping image tiling.")
        print("   (This is expected if running locally outside Docker)")
        return

    src_path = Path(src_dir)
    if not src_path.exists():
        print("No source images directory found.")
        return

    dest_path = Path(dest_dir)
    ensure_images_dir(dest_dir)

    # Recursively find images
    image_extensions = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

    # We walk the directory
    for img_file in src_path.rglob("*"):
        if not img_file.is_file():
            continue

        if img_file.name.startswith("."):
            continue

        if img_file.suffix.lower() not in image_extensions:
            continue

        # Determine relative path from src_dir
        rel_path = img_file.relative_to(src_path)

        # Get path without suffix for the ID/Folder
        id_path = rel_path.parent / rel_path.stem

        print(f"Tiling {rel_path}...")
        img_out_dir = dest_path / "images" / id_path
        img_out_dir.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "vips",
            "dzsave",
            str(img_file),
            str(img_out_dir),
            "--layout",
            "iiif3",
            "--id",
            f"{base_url}/images/{id_path}",
        ]

        try:
            subprocess.run(cmd, check=True)
            print(f"Created tiles for {id_path}")

            # Get original image dimensions
            orig_width, orig_height = get_image_dimensions(img_file)
            if orig_width is None:
                print(f"  Warning: Could not get dimensions for {img_file}")
                orig_width, orig_height = 1000, 1000  # fallback

            # Generate a thumbnail for viewer previews
            thumb = generate_thumbnail(img_file, img_out_dir, orig_width, orig_height)

            # Fix the id in info.json
            info_json_path = img_out_dir / "info.json"
            if info_json_path.exists():
                with open(info_json_path, "r") as f:
                    info_data = json.load(f)
                # Set correct id without duplicated path segment
                info_data["id"] = f"{base_url}/images/{id_path}"

                with open(info_json_path, "w") as f:
                    json.dump(info_data, f, indent=2)

        except subprocess.CalledProcessError as e:
            print(f"Error tiling {id_path}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Process images for IIIF Test Manifests"
    )
    parser.add_argument("--url", required=True, help="Base URL for the deployment")
    parser.add_argument("--src", default="src_images", help="Source images directory")
    parser.add_argument("--dest", default="_site", help="Destination site directory")
    args = parser.parse_args()

    base_url = args.url.rstrip("/")
    process_images(args.src, args.dest, base_url)
    print("Image processing complete.")


if __name__ == "__main__":
    main()
