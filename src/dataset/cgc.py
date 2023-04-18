import pandas as pd

from src.shared.constant import POKEMON_TITLE
from src.shared.storage import Database, ImageStorage, JSONStorage


def get_cgc_df():
    image_storage = ImageStorage("cgc", db=Database.SAMSUNG_T7)
    sub_storage = JSONStorage("cgc/sub", db=Database.SAMSUNG_T7)

    dfs = []
    for key in sub_storage.get_all_keys():
        try:
            df = sub_storage.get_df(key)
            dfs.append(df)
        except Exception as e:
            print(e)
    cgc_df = pd.concat(dfs, ignore_index=True)

    cgc_df = cgc_df[cgc_df["game"] == POKEMON_TITLE]
    cgc_df["key"] = cgc_df["cert_#"]
    cgc_df = cgc_df.set_index("key")
    cgc_df = cgc_df[~cgc_df.index.duplicated(keep="first")]

    images = set(image_storage.get_all_keys())

    def exists(row):
        return "0_" + str(row["cert_#"]) in images

    cgc_df["exists"] = cgc_df.apply(exists, axis=1)
    cgc_df = cgc_df[cgc_df["exists"]]

    return cgc_df
