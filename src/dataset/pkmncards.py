import os

import pandas as pd

from src.shared.storage import Database, ImageStorage


def get_pkmncards_df():
    image_storage = ImageStorage("pkmncards/sets-eng", db=Database.SHARED)

    result = []
    for root, _, files in os.walk(image_storage.base_path):
        for file in files:
            if file.endswith(image_storage.extension) and not file.startswith("._"):
                relative_path = os.path.relpath(root, image_storage.base_path)
                key = os.path.join(
                    relative_path, file[: -(len(image_storage.extension) + 1)]
                )
                full_path = os.path.join(root, file)
                result.append((key, full_path))
    pkmncards_df = pd.DataFrame(result, columns=["id", "image_path"])
    pkmncards_df = pkmncards_df.set_index("id")
    return pkmncards_df
