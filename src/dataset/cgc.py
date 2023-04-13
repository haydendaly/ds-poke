import os

import pandas as pd

from ..image import ImageDatabase, ImageStorage
from ..shared import POKEMON_TITLE


def get_cgc_df():
    storage = ImageStorage("cgc", db=ImageDatabase.SAMSUNG_T7)

    dfs = []
    for file_name in os.listdir("./db/cgc/sub"):
        if file_name.endswith(".json"):
            try:
                df = pd.read_json(f"./db/cgc/sub/{file_name}")
                dfs.append(df)
            except Exception as e:
                print(e)

    cgc_df = pd.concat(dfs, ignore_index=True)
    cgc_df = cgc_df[cgc_df["game"] == POKEMON_TITLE]
    cgc_df["key"] = cgc_df["cert_#"]
    cgc_df = cgc_df.set_index("key")
    cgc_df = cgc_df[~cgc_df.index.duplicated(keep="first")]

    images = set([p[2:-4] for p in os.listdir(storage.base_path)])

    def exists(row):
        return str(row["cert_#"]) in images

    cgc_df["exists"] = cgc_df.apply(exists, axis=1)
    cgc_df = cgc_df[cgc_df["exists"]]
    return cgc_df
