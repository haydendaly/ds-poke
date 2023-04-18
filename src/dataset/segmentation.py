from src.shared.storage import Database, ImageStorage, JSONStorage


def get_segmentation_df():
    json_storage = JSONStorage("segmentation", db=Database.SHARED)
    image_storage = ImageStorage("segmentation/front_scans", db=Database.SHARED)

    front_scans_df = json_storage.get_df("front_scans")
    front_scans_df["file_path"] = front_scans_df["file_name"].apply(
        lambda p: f"{image_storage.base_path}/{p}"
    )
    return front_scans_df
