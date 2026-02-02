"""Main build script for IIIF Test Manifests Site.

This script orchestrates both image processing and site generation.
For individual operations, use build_images.py or build_site.py directly.
"""

import argparse
import shutil
from pathlib import Path

from build_images import process_images
from build_site import process_manifests, generate_index


def clean_site_dir(site_dir):
    """Clean and recreate the site directory structure."""
    site_path = Path(site_dir)
    if site_path.exists():
        shutil.rmtree(site_path)
    site_path.mkdir()
    (site_path / "images").mkdir()
    (site_path / "manifests").mkdir()


def main():
    parser = argparse.ArgumentParser(description="Build IIIF Test Manifests Site")
    parser.add_argument("--url", required=True, help="Base URL for the deployment")
    parser.add_argument("--dest", default="_site", help="Destination site directory")
    parser.add_argument(
        "--src-images", default="src_images", help="Source images directory"
    )
    parser.add_argument("--templates", default="templates", help="Templates directory")
    args = parser.parse_args()

    base_url = args.url.rstrip("/")

    clean_site_dir(args.dest)
    process_images(args.src_images, args.dest, base_url)
    manifests = process_manifests(args.dest, base_url)
    generate_index(manifests, args.dest, args.templates, base_url)

    print("Build complete.")


if __name__ == "__main__":
    main()
