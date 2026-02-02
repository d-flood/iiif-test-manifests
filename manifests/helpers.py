import json
from pathlib import Path

from iiif_prezi3 import Manifest, Canvas, AnnotationPage, Annotation

# Must match THUMBNAIL_SIZE in build_images.py
THUMBNAIL_SIZE = 400


def get_image_dimensions(image_id: str, site_dir: str = "_site") -> tuple[int, int]:
    """Get image dimensions from the info.json file.

    Args:
        image_id: The image service ID (e.g., "{base_url}/images/super-res/webb-helix-nebula")
        site_dir: The site directory where images are stored

    Returns:
        Tuple of (width, height). Falls back to (1000, 1000) if info.json not found.
    """
    try:
        if "/images/" in image_id:
            image_path = image_id.split("/images/", 1)[1]
            info_path = Path(site_dir) / "images" / image_path / "info.json"

            if info_path.exists():
                with open(info_path, "r") as f:
                    info_data = json.load(f)
                return info_data.get("width", 1000), info_data.get("height", 1000)
    except Exception:
        pass

    # Fallback dimensions
    return 1000, 1000


def get_thumbnail_url(image_service_id: str, width: int, height: int) -> str:
    """Get the thumbnail URL for an image.

    Returns the URL to the generated thumbnail in format:
    {image_service_id}/full/{thumb_w},{thumb_h}/0/default.jpg
    """
    # Calculate thumbnail dimensions maintaining aspect ratio
    if width >= height:
        thumb_width = THUMBNAIL_SIZE
        thumb_height = round(height * (THUMBNAIL_SIZE / width))
    else:
        thumb_height = THUMBNAIL_SIZE
        thumb_width = round(width * (THUMBNAIL_SIZE / height))

    return f"{image_service_id}/full/{thumb_width},{thumb_height}/0/default.jpg"


def create_simple_manifest(
    base_url, rel_path, label, summary, viewing_direction, image_indices
):
    manifest = Manifest(
        id=f"{base_url}/manifests/{rel_path}",
        label={"en": [label]},
        summary={"en": [summary]},
        viewingDirection=viewing_direction,
        items=[],
    )

    for i in image_indices:
        # Image service ID
        image_service_id = f"{base_url}/images/numbers/{i}"

        # Get actual dimensions from the generated info.json
        width, height = get_image_dimensions(image_service_id)

        # Get thumbnail URL
        thumb_url = get_thumbnail_url(image_service_id, width, height)

        # Create a canvas
        canvas_id = f"{base_url}/manifests/{rel_path}/canvas/{i}"
        canvas = manifest.make_canvas(
            id=canvas_id, height=height, width=width, label={"en": [f"Page {i}"]}
        )

        # Create the annotation page
        anno_page = AnnotationPage(id=f"{canvas_id}/page/1")
        canvas.items.append(anno_page)

        # Create the annotation
        anno = Annotation(
            id=f"{canvas_id}/page/1/annotation/1",
            motivation="painting",
            target=canvas_id,
            body={
                "id": thumb_url,
                "type": "Image",
                "format": "image/jpeg",
                "height": height,
                "width": width,
                "service": [
                    {
                        "id": image_service_id,
                        "type": "ImageService3",
                        "profile": "level0",
                    }
                ],
            },
        )
        anno_page.items.append(anno)

    return manifest
