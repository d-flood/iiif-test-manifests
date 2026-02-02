from ..helpers import create_simple_manifest


def load(base_url):
    return create_simple_manifest(
        base_url,
        "viewing/ltr.json",
        "Left-to-Right Viewing",
        "A manifest with viewingDirection set to 'left-to-right'. This is the default.",
        "left-to-right",
        [1, 2, 3],
    )
