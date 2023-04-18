import pandas as pd

from src.shared.storage import Database, JSONStorage


def get_pokumon_df():
    pokumon_storage = JSONStorage("pokumon", db=Database.SAMSUNG_T7)
    pokumon_data = pokumon_storage.get("cards", default={}).values()
    pokumon_df = pd.DataFrame(pokumon_data)
    pokumon_df = pokumon_df.set_index("id")
    pokumon_df = pokumon_df[~pokumon_df.index.duplicated(keep="first")]
    return pokumon_df
