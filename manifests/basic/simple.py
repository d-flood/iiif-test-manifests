from iiif_prezi3 import Manifest, AnnotationPage, Annotation
from manifests.helpers import get_image_dimensions, get_thumbnail_url


def load(base_url: str) -> Manifest:
    # Image service ID
    image_service_id = f"{base_url}/images/super-res/webb-helix-nebula"

    # Get actual dimensions from the generated info.json
    width, height = get_image_dimensions(image_service_id)

    # Get thumbnail URL
    thumb_url = get_thumbnail_url(image_service_id, width, height)

    # Programmatically build the manifest
    manifest = Manifest(
        id=f"{base_url}/manifests/basic/simple.json",
        label={"en": ["Simple Manifest"]},
        summary={
            "en": [
                "A basic single-canvas manifest demonstrating the minimum required properties."
            ]
        },
        items=[],
    )

    # Create a canvas using helper methods
    canvas = manifest.make_canvas(
        id=f"{base_url}/manifests/basic/simple/canvas/1", height=height, width=width
    )

    # Create the annotation page
    anno_page = AnnotationPage(id=f"{base_url}/manifests/basic/simple/canvas/1/page/1")
    canvas.items.append(anno_page)

    # Create the annotation
    anno = Annotation(
        id=f"{base_url}/manifests/basic/simple/canvas/1/page/1/annotation/1",
        motivation="painting",
        target=canvas.id,
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
