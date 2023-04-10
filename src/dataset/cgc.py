import pandas as pd
import os


def get_cgc_df():
    dfs = []
    for file_name in os.listdir("./db/cgc/sub"):
        if file_name.endswith(".json"):
            try:
                df = pd.read_json(f"./db/cgc/sub/{file_name}")
                dfs.append(df)
            except Exception as e:
                print(e)

    cgc = pd.concat(dfs, ignore_index=True)
    new_cgc = cgc[cgc["game"] == "Pokémon"]
    new_cgc["key"] = new_cgc["cert_#"]
    return new_cgc
