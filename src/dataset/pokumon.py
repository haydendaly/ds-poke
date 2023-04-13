import json

import pandas as pd


def get_pokumon_df():
    cards = []
    with open("./db/pokumon/cards.json") as f:
        cards = json.load(f).values()
    pokumon_df = pd.DataFrame(cards)
    pokumon_df = pokumon_df.set_index("id")
    pokumon_df = pokumon_df[~pokumon_df.index.duplicated(keep="first")]
    return pokumon_df
