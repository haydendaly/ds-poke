import math
import time
from datetime import datetime

import pandas as pd
import requests

from src.shared.storage import Database, JSONStorage

# TODO(hayden): need to fix


class PsaAuctionScraper:
    SCRAPE_URL = "https://www.psacard.com/auctionprices/GetItemLots"
    PAGE_MAX = 250

    def __init__(self):
        self.card_storage = JSONStorage("psa/auction", db=Database.SAMSUNG_T7)

    def persist(self, card_id, data):
        self.card_storage.set(card_id, data)

    def get_persisted(self, card_id):
        return self.card_storage.get(card_id, default=None)

    def post_to_url(self, session, form_data):
        response = session.post(self.SCRAPE_URL, data=form_data)
        response.raise_for_status()
        json_data = response.json()
        time.sleep(3)
        return json_data

    def scrape_card(self, card_id):
        existing_data, last_updated = self.card_storage.get_with_metadata(
            card_id, default=None
        )

        if existing_data:
            if (datetime.now() - last_updated).days < 10:
                return None

        sess = requests.Session()
        sess.mount("https://", requests.adapters.HTTPAdapter(max_retries=5))
        form_data = {
            "specID": str(card_id),
            "draw": 1,
            "start": 0,
            "length": self.PAGE_MAX,
        }

        json_data = self.post_to_url(sess, form_data)
        sales = json_data["data"]

        total_sales = json_data["recordsTotal"]
        if total_sales > self.PAGE_MAX:
            additional_pages = math.ceil((total_sales - self.PAGE_MAX) / self.PAGE_MAX)
            for i in range(additional_pages):
                curr_page = i + 1
                form_data = {
                    "specID": str(card_id),
                    "draw": curr_page + 2,
                    "start": self.PAGE_MAX * curr_page,
                    "length": self.PAGE_MAX,
                }

                json_data = self.post_to_url(sess, form_data)
                sales += json_data["data"]

        self.persist(card_id, sales)
        return sales

    def scrape(self, card_ids):
        for card_id in card_ids:
            try:
                self.scrape_card(card_id)
            except Exception as e:
                print(e, card_id)
                time.sleep(10)

    def get_auction_data_df(self, card_id=None):
        if card_id:
            cards = [card_id]
        else:
            cards = self.card_storage.get_all_keys()

        all_auction_data = []

        for card_id in cards:
            existing_data = self.get_persisted(card_id)

            if existing_data:
                all_auction_data.extend(existing_data)

        auction_data_df = pd.DataFrame(all_auction_data)
        return auction_data_df
