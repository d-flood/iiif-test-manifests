from iiif_prezi3 import Manifest, AnnotationPage, Annotation
from manifests.helpers import get_image_dimensions, get_thumbnail_url


def load(base_url: str) -> Manifest:
    manifest = Manifest(
        id=f"{base_url}/manifests/basic/multipage.json",
        label={"en": ["Multipage Manifest (Aleppo Codex)"]},
        summary={
            "en": ["A standard multipage manifest using images from the Aleppo Codex."]
        },
        items=[],
    )

    # List of images sorted by filename
    images = sorted(
        [
            "001-r_Deuteronomy",
            "002-v_Deuteronomy",
            "003-r_Deuteronomy",
            "004-v_Deuteronomy",
            "005-r_Deuteronomy",
            "006-v_Deuteronomy",
            "007-r_Deuteronomy",
            "008-v_Deuteronomy",
            "009-r_Deuteronomy",
            "010-v_Deuteronomy",
            "011-r_Deuteronomy",
        ]
    )

    for i, img_name in enumerate(images):
        canvas_num = i + 1

        # Image service ID
        image_service_id = f"{base_url}/images/aleppo/{img_name}"

        # Get actual dimensions from the generated info.json
        width, height = get_image_dimensions(image_service_id)

        # Get thumbnail URL
        thumb_url = get_thumbnail_url(image_service_id, width, height)

        # Determine label (Recto/Verso) based on filename
        label_text = f"Page {canvas_num}"
        if "-r_" in img_name:
            label_text += " (Recto)"
        elif "-v_" in img_name:
            label_text += " (Verso)"

        # Create canvas
        canvas_id = f"{base_url}/manifests/basic/multipage/canvas/{canvas_num}"
        canvas = manifest.make_canvas(
            id=canvas_id,
            height=height,
            width=width,
            label={"en": [label_text]},
        )

        # Annotation Page
        anno_page = AnnotationPage(id=f"{canvas_id}/page/1")
        canvas.items.append(anno_page)

        # Annotation
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
