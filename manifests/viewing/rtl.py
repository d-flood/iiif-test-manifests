from ..helpers import create_simple_manifest


def load(base_url):
    return create_simple_manifest(
        base_url,
        "viewing/rtl.json",
        "Right-to-Left Viewing",
        "A manifest with viewingDirection set to 'right-to-left'. Useful for Semitic languages.",
        "right-to-left",
        [1, 2, 3],
    )
