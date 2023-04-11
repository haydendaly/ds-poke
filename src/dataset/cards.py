import glob
import json
import os

import pandas as pd


def get_eng_checklists():
    json_folder = "./db/cards/sets-eng/"
    # open json_folder / sets-eng.json
    sets_eng = None
    with open("./db/cards/sets-eng.json") as f:
        sets_eng = json.load(f)

    dfs = []
    id_to_set = dict()

    for set_obj in sets_eng:
        set_path = json_folder + set_obj["id"] + ".json"
        id_to_set[set_obj["id"]] = set_obj
        if os.path.exists(set_path):
            with open(set_path) as f:
                df = pd.read_json(f)
                dfs.append(df)
    sets_eng_df = pd.concat(dfs)

    # variant = {

    # }
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
        return f"./db/pokemontcg.io/sets-eng/{name}/{num}{print_run}.jpg"

    def path_exists(row):
        return os.path.exists(row["path"])

    sets_eng_df["path"] = sets_eng_df.apply(get_path, axis=1)
    sets_eng_df["image_exists"] = sets_eng_df.apply(path_exists, axis=1)
    return sets_eng_df


def get_eng_df():
    image_folder = "../db/pokemontcg.io/sets-eng/"
    image_files = glob.glob(image_folder + "**/*.jpg", recursive=True)
    return pd.DataFrame(image_files, columns=["file_path"])
