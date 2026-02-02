from .basic import simple, multipage
from .viewing import ltr, rtl, ttb, btt

# Registry mapping: relative output path -> loader function
# The key determines where the JSON file will be written inside _site/manifests/
MANIFESTS = {
    "basic/simple.json": simple.load,
    "basic/multipage.json": multipage.load,
    "viewing/ltr.json": ltr.load,
    "viewing/rtl.json": rtl.load,
    "viewing/ttb.json": ttb.load,
    "viewing/btt.json": btt.load,
}
