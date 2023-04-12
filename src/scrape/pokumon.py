import asyncio
import concurrent.futures
import os

from ..image import ImageDatabase, ImageStorage
from ..shared import json_dump_file, json_load_file
from .browser import SSRBrowser


class PokumonScraper:
    PAGE_URL = "https://pokumon.com/cards/?sf_data=all&sf_paged="
    POKUMON_BATCH_SIZE = 50

    def __init__(self, single_threaded=False):
        self.storage = ImageStorage("pokumon", db=ImageDatabase.SAMSUNG_T7)
        self.browser = SSRBrowser()

        cpus = os.cpu_count()
        if cpus is None or single_threaded:
            cpus = 1
        # else:
        #     cpus *= 2
        self.num_threads = cpus
        self.queue = asyncio.Queue()

        self.get_persisted()

    def persist(self):
        os.makedirs("./db/pokumon", exist_ok=True)

        with open(f"./db/pokumon/card_links.json", "w") as f:
            json_dump_file(list(self.card_links), f)
        with open(f"./db/pokumon/pages.json", "w") as f:
            json_dump_file(list(self.pages), f)
        with open(f"./db/pokumon/cards.json", "w") as f:
            json_dump_file(self.cards, f)

    def get_persisted(self):
        os.makedirs("./db/pokumon", exist_ok=True)

        self.card_links = set()
        self.pages = set()
        self.cards = dict()

        os.makedirs("./db/pokumon", exist_ok=True)
        try:
            with open(f"./db/pokumon/card_links.json", "r") as f:
                self.card_links = set(json_load_file(f))
        except:
            pass
        try:
            with open(f"./db/pokumon/pages.json", "r") as f:
                self.pages = set(json_load_file(f))
        except:
            pass
        try:
            with open(f"./db/pokumon/cards.json", "r") as f:
                self.cards = dict(json_load_file(f))
        except:
            pass

    async def get_page_links(self, page_num):
        self.pages.add(page_num)
        dom = await self.browser.get_async(self.PAGE_URL + str(page_num))
        for link in dom.select("a.cl-element-featured_media__anchor"):
            self.card_links.add(link["href"])
        self.persist()

    async def get_all_card_links(self):
        print(len(self.pages))
        for i in range(0, 243):
            if i in self.pages:
                continue
            if (i % 10) == 0:
                print(f"Processing page {i}")
            await self.get_page_links(i)

    async def get_card_info(self, card_link):
        dom = await self.browser.get_async(card_link)
        card_info = dict()
        try:
            title_elem = dom.find("h3", class_="elementor-heading-title")
            desc_elem = dom.find("div", class_="elementor-widget-theme-post-content")
            img_elem = dom.find("img", class_="attachment-large")
            if not title_elem or not desc_elem or not img_elem:
                return
            card_info["title"] = title_elem.text.strip()
            card_info["desc"] = desc_elem.text.strip()
            card_info["image_url"] = img_elem["src"]
            card_info["id"] = card_link.split("/")[-2]
            fields = dom.find_all("a", class_="elementor-post-info__terms-list-item")
            for ul in fields:
                href = ul["href"]
                key = href.split("/")[3]
                text = ul.text.strip()
                card_info[key] = text
            return card_info

        except Exception as e:
            print(e)

    async def pokumon_worker(self, thread_num):
        while True:
            url = await self.queue.get()
            l = self.queue.qsize()
            if l % self.POKUMON_BATCH_SIZE == 0:
                print(f"Cards remaining: {l}")
                self.persist()
            card_info = await self.get_card_info(url)
            if card_info is not None:
                self.cards[url] = card_info
                await self.storage.download_image_to_id_async(
                    card_info["image_url"], card_info["id"]
                )
            self.queue.task_done()

    async def run(self):
        for url in self.card_links:
            if url not in self.cards:
                await self.queue.put(url)

        print(
            f"Processing {self.queue.qsize()} submissions in {self.num_threads} threads"
        )

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.num_threads
        ) as executor:
            workers = [
                asyncio.create_task(self.pokumon_worker(thread_num))
                for thread_num in range(self.num_threads)
            ]
            await asyncio.gather(*workers)
            await self.queue.join()
            for w in workers:
                w.cancel()


def main():
    scraper = PokumonScraper()
    # asyncio.run(scraper.get_all_card_links())
    asyncio.run(scraper.run())
