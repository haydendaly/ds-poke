import pandas as pd

from src.shared.storage import Database, JSONStorage


def get_pokemontcg_df():
    json_storage = JSONStorage("pokemontcg", db=Database.LOCAL)
    image_storage = JSONStorage("pokemontcg/sets-eng", db=Database.LOCAL)
    sets_eng = json_storage.get("sets-eng", default=[])

    dfs = []
    id_to_set = dict()

    for set_obj in sets_eng:
        id_to_set[set_obj["id"]] = set_obj
        set_data = json_storage.get("sets-eng/" + set_obj["id"], default=None)
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

    # TODO: Figure out key/image mapping
    def get_key(row):
        set_id = row["setReference"]["connect"]["id"]
        name = id_to_set[set_id]["name"].lower().replace(" ", "-")
        num = "{:0>3}".format(row["number"])
        print_run = ""
        if row["print"]:
            print_run = print_map[row["print"]]
        return f"{name}/{num}{print_run}"

    keys = set(image_storage.get_all_keys_recursive())

    def path_exists(row):
        return row["key"] in keys

    sets_eng_df["key"] = sets_eng_df.apply(get_key, axis=1)
    sets_eng_df["image_exists"] = sets_eng_df.apply(path_exists, axis=1)
    return sets_eng_df
