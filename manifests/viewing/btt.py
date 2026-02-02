from ..helpers import create_simple_manifest


def load(base_url):
    return create_simple_manifest(
        base_url,
        "viewing/btt.json",
        "Bottom-to-Top Viewing",
        "A manifest with viewingDirection set to 'bottom-to-top'. Less common.",
        "bottom-to-top",
        [1, 2, 3],
    )
