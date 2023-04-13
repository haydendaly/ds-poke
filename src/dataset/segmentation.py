import pandas as pd


def get_segmentation_df():
    with open("./db/shared/front_scans.json", "r") as f:
        front_scans_df = pd.read_json(f)
    front_scans_df["file_path"] = front_scans_df["file_name"].apply(
        lambda p: f"./db/shared/front_scans/{p}"
    )
    return front_scans_df
