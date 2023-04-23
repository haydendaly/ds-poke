import asyncio
import concurrent.futures
import os
import time
from collections import deque

from src.classification import LabelClassifier
from src.scrape.browser import SSRBrowser
from src.shared.constant import POKEMON_TITLE
from src.shared.file import swap_files
from src.shared.storage import Database, DataFrameStorage, ImageStorage, JSONStorage


class CGCScraper:
    CGC_BASE_URL = "https://www.cgccards.com/certlookup/"
    CGC_BASE_SUB_NUM = 1100000
    CGC_TOP_SUB_NUM = 4426544
    # cert seems to be two parts: submission_id `4126544`, card_number in submission `002`
    CGC_BATCH_SIZE = (
        50  # how many submissions to process before persisting to seen.json
    )
    MAX_CONNECTIONS = 58

    def __init__(self, single_threaded=False):
        self.image_storage = ImageStorage("cgc", db=Database.SAMSUNG_T7)
        self.json_storage = JSONStorage("cgc", db=Database.SAMSUNG_T7)
        self.sub_storage = JSONStorage("cgc/sub", db=Database.SAMSUNG_T7)
        self.browser = SSRBrowser()

        self.times = deque()

        cpus = os.cpu_count()
        if cpus is None or single_threaded:
            cpus = 1
        else:
            cpus *= 6
        self.num_threads = cpus
        self.queue = asyncio.Queue()

        self.get_persisted()
        self.semaphore = asyncio.Semaphore(self.MAX_CONNECTIONS)
        self.label_classifier = LabelClassifier()

    def get_images(self, cert_num, image_urls):
        if not self.image_storage.has("0_" + cert_num):
            if len(image_urls) == 2:
                path_0, image_0 = self.image_storage.download_to_id(
                    image_urls[0], "0_" + cert_num
                )
                if not self.label_classifier.is_front(image_0):
                    path_1, image_1 = self.image_storage.download_to_id(
                        image_urls[1], "1_" + cert_num
                    )
                    if self.label_classifier.images_are_inverted(image_0, image_1):
                        swap_files(path_0, path_1)

    async def parse_card_info(self, cert_num: str, data):
        async with self.semaphore:
            if cert_num in self.failed:
                # print(f"Skipping {cert_num} because it already exists")
                return False
            try:
                try:
                    dom = await self.browser.get_async(self.CGC_BASE_URL + cert_num)
                except Exception as e:
                    time.sleep(0.1)
                    self.failed.add(cert_num)
                    print(f"Failed to get {cert_num} because {e}")
                    return False
                card_info = {}
                for dl in dom.select("div.certlookup-intro dl"):
                    key, value = None, None
                    key_elem, value_elem = dl.select_one("dt"), dl.select_one("dd")
                    if key_elem is not None:
                        key = key_elem.text.strip()
                    if value_elem is not None:
                        value = value_elem.text.strip()
                    if key is not None and value is not None:
                        card_info[key] = value
                if len(card_info) == 0:
                    # print(f"Failed to find card info for {cert_num}")
                    self.failed.add(cert_num)
                    return False
                card_data = {}
                for key, value in card_info.items():
                    card_data[key.lower().replace(" ", "_", 3)] = value

                images = dom.select("div.certlookup-images img")
                image_urls = [str(img["src"]) for img in images]
                card_data["image_urls"] = image_urls
                if card_data["game"] == POKEMON_TITLE:
                    self.get_images(cert_num, image_urls)
                data.append(card_data)
                return True
            except Exception as e:
                # print("Error", e)
                self.failed.add(cert_num)
            return False

    def save_submission(self, sub_prefix, data):
        self.sub_storage.set(sub_prefix, data)

    def has_submission(self, sub_prefix):
        return self.sub_storage.has(sub_prefix)

    def persist(self):
        self.json_storage.set("aborted", list(self.aborted))
        self.json_storage.set("failed", list(self.failed))

    def get_persisted(self):
        self.aborted = set(self.json_storage.get("aborted", default=[]))
        self.failed = set(self.json_storage.get("failed", default=[]))

    async def cgc_worker(self, thread_num):
        while True:
            sub_prefix = await self.queue.get()
            l = self.queue.qsize()
            if l % self.CGC_BATCH_SIZE == 0:
                self.times.append(time.time())
                print(f"{thread_num}: Submissions remaining: {l}")
                if len(self.times) > 10:
                    submission_rate = (
                        self.CGC_BATCH_SIZE * 10 / (self.times[-1] - self.times[-9])
                    )
                    print(f"Submissions / second: {submission_rate}")
                    print("Time remaining (hours):", l / submission_rate / 3600)
                self.persist()
            data = []
            for i in range(1, 1000):
                cert_num = sub_prefix + "{:0>3}".format(i)
                if not await self.parse_card_info(cert_num, data):
                    if i == 1:
                        self.aborted.add(sub_prefix)
                    break
                # dip if we hit a non-pokemon card first
                if i == 1 and data and data[-1]["game"] != POKEMON_TITLE:
                    self.aborted.add(sub_prefix)
                    break

            if len(data) != 0:
                self.save_submission(sub_prefix, data)

            self.queue.task_done()

    async def image_worker(self, df, thread_num):
        while True:
            i = await self.queue.get()
            if i % 200 == 0:
                print(f"{thread_num}: Images remaining: {len(df) - i}")
            row = df.iloc[i]
            try:
                self.get_images(str(row["cert_#"]), row["image_urls"])
            except Exception as e:
                print(f"Failed to get images for {row['cert_#']}: {e}")
            self.queue.task_done()

    async def run(self):
        self.seen = set(self.sub_storage.get_all_keys())
        for sub_num in range(self.CGC_TOP_SUB_NUM, self.CGC_BASE_SUB_NUM, -1):
            sub_prefix = "{:0>7}".format(sub_num)
            if sub_prefix not in self.seen and sub_prefix not in self.aborted:
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

    async def run_images(self):
        storage = DataFrameStorage("cgc", db=Database.LOCAL)
        df = storage.get("images")
        for i in range(len(df)):
            await self.queue.put(i)

        print(f"Processing {self.queue.qsize()} images in {self.num_threads} threads")

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.num_threads
        ) as executor:
            workers = [
                asyncio.create_task(self.image_worker(df, thread_num))
                for thread_num in range(self.num_threads)
            ]
            await asyncio.gather(*workers)
            await self.queue.join()
            for w in workers:
                w.cancel()


def scrape_cgc():
    scraper = CGCScraper()
    return scraper.run()


def scrape_images():
    scraper = CGCScraper()
    return scraper.run_images()


def main():
    asyncio.run(scrape_cgc())
