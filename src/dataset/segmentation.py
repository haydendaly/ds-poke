import pandas as pd

from src.shared.storage import Database, ImageStorage, JSONStorage


def get_segmentation_df():
    json_storage = JSONStorage("segmentation", db=Database.SHARED)
    image_storage = ImageStorage("segmentation/front_scans", db=Database.SHARED)

    def get_path(s):
        return f"{image_storage.base_path}/{s.split('-')[1]}"

    front_scans = json_storage.get("front_scans_tight")

    processed_data = []

    for item in front_scans:
        file_upload = item["file_upload"]
        result = item["annotations"][0]["result"][0]["value"]

        processed_data.append(
            {
                "image_path": get_path(file_upload),
                "x": result["x"],
                "y": result["y"],
                "width": result["width"],
                "height": result["height"],
                "rotation": result["rotation"],
            }
        )

    front_scans_df = pd.DataFrame(processed_data)
    return front_scans_df
