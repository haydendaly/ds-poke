import os

import pandas as pd

from src.shared.storage import Database, JSONStorage


def get_eng_checklists():
    pokemontcg_storage = JSONStorage("pokemontcg", db=Database.SAMSUNG_T7)
    sets_eng = pokemontcg_storage.get("sets-eng", default=[])

    dfs = []
    id_to_set = dict()

    for set_obj in sets_eng:
        id_to_set[set_obj["id"]] = set_obj
        set_data = pokemontcg_storage.get("sets-eng/" + set_obj["id"], default=None)
        if set_data:
            df = pd.DataFrame(set_data)
            dfs.append(df)

    sets_eng_df = pd.concat(dfs)
    print_map = {
        "FirstEdition": "fe",
        "Shadowless": "s",
        "Unlimited": "",
        "UK_1999": "",
        "NoSetSymbol": "",
    }

    def get_path(row):
        set_id = row["setReference"]["connect"]["id"]
        name = id_to_set[set_id]["name"].lower().replace(" ", "-")
        num = "{:0>3}".format(row["number"])
        print_run = ""
        if row["print"]:
            print_run = print_map[row["print"]]
        return f"{pokemontcg_storage.base_path}/sets-eng/{name}/{num}{print_run}.jpg"

    def path_exists(row):
        return os.path.exists(row["path"])

    sets_eng_df["path"] = sets_eng_df.apply(get_path, axis=1)
    sets_eng_df["image_exists"] = sets_eng_df.apply(path_exists, axis=1)
    return sets_eng_df


def get_pokemontcg_df():
    pokemontcg_storage = JSONStorage("pokemontcg/sets-eng", db=Database.SAMSUNG_T7)
    image_files = pokemontcg_storage.get_all_keys_recursive()

    return pd.DataFrame(image_files, columns=["file_path"])
