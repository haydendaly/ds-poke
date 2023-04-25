import time
from datetime import datetime

import pandas as pd
import requests

from src.shared.browser import SSRBrowser
from src.shared.storage import Database, JSONStorage


class PSAPopScraper:
    GET_SETS_URL = "https://www.psacard.com/pop/essearch"
    GET_SET_URL = "https://www.psacard.com/Pop/GetSetItems"

    def __init__(self):
        self.ssr_browser = SSRBrowser()
        self.sets = dict()
        self.set_list_storage = JSONStorage("psa/pop", db=Database.SAMSUNG_T7)
        self.sets_storage = JSONStorage("psa/pop/sets", db=Database.SAMSUNG_T7)

    def persist(self):
        self.set_list_storage.set("sets", self.sets)

    def get_persisted(self):
        self.sets = self.set_list_storage.get("sets", default={})

    def scrape_set_search(self):
        payload = {
            "draw": 2,
            "filterCategoryID": 0,
            "categoryName": "",
            "pageNumber": 1,
            "pageSize": 2000,
            "search": "pokemon",
            "searchSequence": 1,
        }
        response = requests.post(self.GET_SETS_URL, data=payload).json()

        if response.get("Success") and "data" in response:
            for set_info in response["data"]:
                self.sets[set_info["HeadingID"]] = set_info

    def scrape_set(self, set_number):
        existing_data, last_updated = self.sets_storage.get_with_metadata(
            set_number, default=None
        )

        if existing_data:
            if (datetime.now() - last_updated).days < 10:
                return

        payload = {
            "draw": 1,
            "start": 0,
            "length": 1000,
            "search": "",
            "headingID": set_number,
            "categoryID": 156940,
            "isPSADNA": False,
        }
        response = requests.post(self.GET_SET_URL, json=payload).json()

        if response.get("recordsFiltered") > 0 and "data" in response:
            set_data = {}

            for item in response["data"]:
                if item["SpecID"] == 0:
                    continue

                set_data[item["SpecID"]] = item

            self.sets_storage.set(set_number, set_data)
            return True

    def scrape(self):
        self.get_persisted()

        if not self.sets:
            self.scrape_set_search()
            self.persist()

        for i, set_number in enumerate(self.sets):
            try:
                if self.scrape_set(set_number):
                    time.sleep(5)
            except Exception as e:
                print(e, set_number)
                time.sleep(10)
            if i % 10 == 0:
                print(f"Scraped {i}/{len(self.sets)} sets")

    def get_sets_df(self):
        sets_data = list(self.sets.values())
        sets_df = pd.DataFrame(sets_data)
        sets_df["set_id"] = sets_df["HeadingID"]
        sets_df = sets_df.set_index("HeadingID")
        sets_df = sets_df[~sets_df.index.duplicated(keep="first")]
        return sets_df

    def get_cards_df(self, set_id=None):
        all_cards = []

        if set_id:
            sets = [set_id]
        else:
            if not self.sets:
                self.get_persisted()
            sets = self.sets.keys()

        for set_number in list(sets):
            existing_data = self.sets_storage.get(set_number, default=None)

            try:
                if existing_data:
                    for card in existing_data.values():
                        card["set_id"] = set_number
                        all_cards.append(card)
            except Exception as e:
                print(e, set_number, existing_data)
                break

        cards_df = pd.DataFrame(all_cards)
        cards_df = cards_df.set_index("SpecID")
        cards_df = cards_df[~cards_df.index.duplicated(keep="first")]

        sets_df = self.get_sets_df()
        cards_df["set_id"] = cards_df["set_id"].astype(str)
        sets_df["set_id"] = sets_df["set_id"].astype(str)

        merged_df = cards_df.merge(sets_df, on="set_id", how="left")

        return merged_df
