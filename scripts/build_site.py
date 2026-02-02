"""Site generation script for IIIF Test Manifests.

This script handles generating manifests, collections, and the index page.
Can be run standalone or imported by the main build script.
"""

import argparse
import shutil
import sys
from pathlib import Path

# Ensure the root directory is in the path so we can import manifests
sys.path.append(str(Path.cwd()))

from jinja2 import Environment, FileSystemLoader
from manifests.registry import MANIFESTS
from manifests.collections import top


def ensure_site_dirs(site_dir):
    """Ensure the site directory structure exists."""
    site_path = Path(site_dir)
    if not site_path.exists():
        site_path.mkdir(parents=True)
    manifests_path = site_path / "manifests"
    if not manifests_path.exists():
        manifests_path.mkdir()
    return site_path


def process_manifests(dest_dir, base_url):
    """Generate all manifests from the registry.

    Args:
        dest_dir: Site directory to output manifests to
        base_url: Base URL for the deployment

    Returns:
        List of manifest metadata for index generation
    """
    print("Generating manifests from registry...")
    manifests_list = []

    dest_path = Path(dest_dir)
    ensure_site_dirs(dest_dir)

    for rel_path, loader_func in MANIFESTS.items():
        try:
            # 1. Generate Manifest Object
            manifest = loader_func(base_url)

            # 2. Serialize to JSON
            # ensure_ascii=False ensures proper unicode characters
            json_output = manifest.json(indent=2, ensure_ascii=False)

            # 3. Write to file
            output_path = dest_path / "manifests" / rel_path
            output_path.parent.mkdir(parents=True, exist_ok=True)

            output_path.write_text(json_output, encoding="utf-8")

            print(f"Generated {rel_path}")

            # 4. Extract metadata for Index
            label = "Untitled"
            if manifest.label:
                # Handle LanguageMap
                if isinstance(manifest.label, dict):
                    # Try English, then first available
                    label = manifest.label.get(
                        "en", [list(manifest.label.values())[0]]
                    )[0]
                else:
                    label = str(manifest.label)

            summary = ""
            if manifest.summary:
                if isinstance(manifest.summary, dict):
                    summary = manifest.summary.get(
                        "en", [list(manifest.summary.values())[0]]
                    )[0]
                else:
                    summary = str(manifest.summary)

            manifests_list.append(
                {
                    "path": f"manifests/{rel_path}",
                    "label": label,
                    "label_obj": manifest.label,  # Store raw label for the collection
                    "summary": summary,
                    "category": str(Path(rel_path).parent),
                }
            )

        except Exception as e:
            print(f"Error generating {rel_path}: {e}")
            # We don't stop the build, but we log the error

    # Generate Top Collection
    print("Generating collections/top.json...")
    try:
        top_col = top.load(base_url, manifests_list)
        col_json = top_col.json(indent=2, ensure_ascii=False)
        col_path = dest_path / "collections" / "top.json"
        col_path.parent.mkdir(parents=True, exist_ok=True)
        col_path.write_text(col_json, encoding="utf-8")
        print("Generated collections/top.json")
    except Exception as e:
        print(f"Error generating collection: {e}")

    return manifests_list


def generate_index(manifests, dest_dir, template_dir, base_url):
    """Generate the index.html and copy static files.

    Args:
        manifests: List of manifest metadata
        dest_dir: Site directory to output to
        template_dir: Directory containing templates
        base_url: Base URL for the deployment
    """
    print("Generating index.html...")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("index.html")

    # Group by category
    categories = {}
    for m in manifests:
        cat = m["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(m)

    output = template.render(categories=categories, BASE_URL=base_url)

    (Path(dest_dir) / "index.html").write_text(output, encoding="utf-8")

    # Copy viewer.html to dest_dir
    shutil.copy(Path(template_dir) / "viewer.html", Path(dest_dir) / "viewer.html")

    # Copy triiiceratops.html to dest_dir
    shutil.copy(
        Path(template_dir) / "triiiceratops.html", Path(dest_dir) / "triiiceratops.html"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Build IIIF Test Manifests Site (manifests and index)"
    )
    parser.add_argument("--url", required=True, help="Base URL for the deployment")
    parser.add_argument("--dest", default="_site", help="Destination site directory")
    parser.add_argument("--templates", default="templates", help="Templates directory")
    args = parser.parse_args()

    base_url = args.url.rstrip("/")

    ensure_site_dirs(args.dest)
    manifests = process_manifests(args.dest, base_url)
    generate_index(manifests, args.dest, args.templates, base_url)

    print("Site generation complete.")


if __name__ == "__main__":
    main()
