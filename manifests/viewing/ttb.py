from ..helpers import create_simple_manifest


def load(base_url):
    return create_simple_manifest(
        base_url,
        "viewing/ttb.json",
        "Top-to-Bottom Viewing",
        "A manifest with viewingDirection set to 'top-to-bottom'. Useful for scrolls.",
        "top-to-bottom",
        [1, 2, 3],
    )
