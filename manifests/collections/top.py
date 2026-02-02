from iiif_prezi3 import Collection, ManifestRef


def load(base_url: str, manifests_list: list = None) -> Collection:
    # Create the top-level collection
    collection = Collection(
        id=f"{base_url}/collections/top.json",
        label={"en": ["IIIF Test Manifests Collection"]},
        summary={"en": ["A collection of all test manifests in this repository."]},
        items=[],
    )

    if manifests_list:
        for m in manifests_list:
            # Add to collection using ManifestRef
            # We construct the ID based on the known output path
            manifest_id = f"{base_url}/{m['path']}"

            collection.items.append(
                ManifestRef(
                    id=manifest_id,
                    type="Manifest",
                    label=m["label_obj"],  # We will pass the raw label object
                )
            )

    return collection
