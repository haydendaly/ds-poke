import pandas as pd

from src.shared.storage import Database, ImageStorage, JSONStorage


def get_pokumon_df():
    pokumon_storage = JSONStorage("pokumon", db=Database.LOCAL)
    image_storage = ImageStorage("pokumon", db=Database.SHARED)

    pokumon_data = pokumon_storage.get("cards", default={}).values()
    pokumon_df = pd.DataFrame(pokumon_data)
    pokumon_df = pokumon_df[~pokumon_df["id"].duplicated(keep="first")]

    def get_path(row):
        return f"{image_storage.base_path}/{row['id']}.{image_storage.extension}"

    pokumon_df["image_path"] = pokumon_df.apply(get_path, axis=1)

    pokumon_df = pokumon_df.set_index("id")
    return pokumon_df
