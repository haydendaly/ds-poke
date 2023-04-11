import os
import json
import time
import concurrent.futures
import pandas as pd
import threading
import asyncio
from PIL import Image

from ....shared import json_dump_file, json_load_file, json_loads, POKEMON_TITLE
from ....image import ImageDatabase, ImageStorage, display_image
from ...browser import SSRBrowser
from .label_classifier import LabelClassifier

CGC_BASE_URL = "https://www.cgccards.com/certlookup/"
CGC_BASE_SUB_NUM = 3526544
CGC_TOP_SUB_NUM = 4126544
# cert seems to be two parts: submission_id `4126544`, card_number in submission `002`
CGC_BATCH_SIZE = 50  # how many submissions to process before persisting to seen.json


def swap_files(path_0, path_1):
    os.rename(path_0, path_0 + '.temp')
    os.rename(path_1, path_0)
    os.rename(path_0 + '.temp', path_1)


class CGCScraper:
    def __init__(self):
        self.storage = ImageStorage("cgc", db=ImageDatabase.SAMSUNG_T7)
        self.browser = SSRBrowser()

        self.num_threads = os.cpu_count() // 2
        # self.num_threads = 1
        self.queue = asyncio.Queue()

        self.get_persisted()
        self.label_classifier = LabelClassifier()

    async def parse_card_info(self, cert_num: str, data):
        if self.storage.has_image("0_" + cert_num):
            print(f"Skipping {cert_num} because it already exists")
            return False
        dom = await self.browser.get_async(CGC_BASE_URL + cert_num)
        card_info = {}
        for dl in dom.select("div.certlookup-intro dl"):
            key = dl.select_one("dt").text.strip()
            value = dl.select_one("dd").text.strip()
            card_info[key] = value
        if len(card_info) == 0:
            print(f"Failed to find card info for {cert_num}")
            return False
        card_data = {}
        for key, value in card_info.items():
            card_data[key.lower().replace(" ", "_", 3)] = value

        if card_data["game"] != POKEMON_TITLE:
            return True

        image_url = ""
        images = dom.select("div.certlookup-images img")
        image_urls = [img["src"] for img in images]
        if len(image_urls) == 2:
            path_0, image_0 = self.storage.download_image_to_id(
                image_urls[0], "0_" + cert_num)
            path_1, image_1 = self.storage.download_image_to_id(
                image_urls[1], "1_" + cert_num)
            if self.label_classifier.images_are_inverted(image_0, image_1):
                swap_files(path_0, path_1)
            return True
        print(card_data, f"Failed to find images for {cert_num}")
        return False

    def save_submission(self, sub_prefix, data):
        os.makedirs("./db/cgc/sub", exist_ok=True)

        with open(f"./db/cgc/sub/{sub_prefix}.json", "w") as f:
            json_dump_file(data, f)

    def persist(self):
        os.makedirs("./db/cgc", exist_ok=True)

        with open(f"./db/cgc/seen.json", "w") as f:
            json_dump_file(list(self.seen), f)
        with open(f"./db/cgc/aborted.json", "w") as f:
            json_dump_file(list(self.aborted), f)
        with open(f"./db/cgc/failed.json", "w") as f:
            json_dump_file(list(self.failed), f)

    def get_persisted(self):
        os.makedirs("./db/cgc", exist_ok=True)

        self.seen = set()
        self.aborted = set()
        self.failed = set()

        if os.path.exists("./db/cgc/seen.json"):
            with open("./db/cgc/seen.json", "r") as f:
                self.seen = set(json_load_file(f))
        if os.path.exists("./db/cgc/aborted.json"):
            with open("./db/cgc/aborted.json", "r") as f:
                self.aborted = set(json_load_file(f))
        if os.path.exists("./db/cgc/failed.json"):
            with open("./db/cgc/failed.json", "r") as f:
                self.failed = set(json_load_file(f))

    async def cgc_worker(self, thread_num):
        while True:
            sub_prefix = await self.queue.get()
            l = self.queue.qsize()
            if l % CGC_BATCH_SIZE == 0:
                print(f"Submissions remaining: {l}")
                self.persist()
            if sub_prefix in self.seen:
                self.queue.task_done()
                continue
            if (
                os.path.exists(f"./db/cgc/sub/{sub_prefix}.json")
                or sub_prefix in self.aborted
            ):
                self.seen.add(sub_prefix)
                self.queue.task_done()
                continue
            self.seen.add(sub_prefix)
            data = []
            for i in range(1, 1000):
                cert_num = sub_prefix + "{:0>3}".format(i)
                if not await self.parse_card_info(cert_num, data):
                    break
                # dip if we hit a non-pokemon card first
                if i == 1 and data and data[-1]["game"] != POKEMON_TITLE:
                    self.aborted.add(sub_prefix)
                    break

            if len(data) != 0:
                self.save_submission(sub_prefix, data)

            self.queue.task_done()

    async def run(self):
        for sub_num in range(CGC_TOP_SUB_NUM, CGC_BASE_SUB_NUM, -1):
            sub_prefix = "{:0>7}".format(sub_num)
            if sub_prefix not in self.seen:
                await self.queue.put(sub_prefix)

        print(
            f"Processing {self.queue.qsize()} submissions in {self.num_threads} threads"
        )

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.num_threads
        ) as executor:
            workers = [
                asyncio.create_task(self.cgc_worker(thread_num))
                for thread_num in range(self.num_threads)
            ]
            await asyncio.gather(*workers)
            await self.queue.join()
            for w in workers:
                w.cancel()


def scrape_cgc():
    scraper = CGCScraper()
    return scraper.run()


def main():
    asyncio.run(scrape_cgc())
    # l = LabelClassifier()
    # path_a, path_b = "/Volumes/T7/db/images/cgc/0_4126524003.jpg", "/Volumes/T7/db/images/cgc/1_4126524003.jpg"
    # image_a, image_b = Image.open(
    #     path_a), Image.open(path_b)
    # display_image(l._preprocess_crop(image_a))
    # display_image(l._preprocess_crop(image_b))
    # print(l.images_are_inverted(image_a, image_b))
