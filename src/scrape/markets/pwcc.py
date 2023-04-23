import math
import re

from selenium.webdriver.common.keys import Keys

from src.scrape.browser import CSRBrowser

from .market import Market

PWCC_ITEMS_PER_PAGE = 96
PWCC_TIMEOUT = 1


class PWCC(Market):
    def __init__(self):
        super().__init__("pwcc", "https://www.pwccmarketplace.com/")
        self.browser = CSRBrowser(headless=False)

    def _get_search_url(self, query, page_num=None):
        q = query.replace(" ", "+")
        base_url = f"https://www.pwccmarketplace.com/weekly-auction?q={q}&items_per_page={PWCC_ITEMS_PER_PAGE}"
        if page_num:
            base_url += f"&page={page_num}"
        return base_url

    def search(self, query):
        url = self._get_search_url(query)
        self.browser.get(url, PWCC_TIMEOUT + 5)
        self.browser.press(Keys.ESCAPE)
        self.browser.scroll_down_page()
        dom = self.browser.get_dom()

        num_items_raw = list(
            list(dom.find_all("span", class_="headerStatsContainer")[0].children)[
                0
            ].children
        )[0]
        num_items = re.sub("[^0-9]", "", num_items_raw)
        num_pages = math.ceil(int(num_items) / PWCC_ITEMS_PER_PAGE)

        for page in range(1, num_pages + 1):
            print(f"Page {page} of {num_pages}")
            raw_items = list(dom.find_all("div", class_="gridItemList")[0].children)
            items = []
            for raw_item in raw_items:
                title_a = raw_item.find("a", attrs={"data-testid": "item-title"})
                front_image_url = list(
                    raw_item.find("a", attrs={"data-testid": "item-image"}).children
                )[0]["src"]
                # TODO: find out how to infer back image url
                # - Potentially bucket storage is {id}_1, {id}_2
                # - Potentially can look at DOM for hover and see if image pops up (potentially emulate mouse too)
                # - Worst case, query the specific item URL (would need to do over a long period of time to circumvent rate limitting)

                price = None
                try:
                    price_item = raw_item.find(
                        "span", attrs={"data-testid": "price-label-current-bid-value"}
                    )
                    price = list(price_item.children)[2].text[1:]
                except Exception as e_curr:
                    try:
                        price_item = raw_item.find(
                            "span",
                            attrs={"data-testid": "price-label-starting-bid-value"},
                        )
                        price = list(price_item.children)[2].text[1:]
                    except Exception as e_start:
                        print("Failed to grab price", e_curr, e_start)

                try:
                    price = float(re.sub("[^0-9|.]", "", price))
                except Exception as e:
                    print("Failed to convert price to float", e)
                    price = None

                name = title_a["title"]
                url = title_a["href"]

                items.append(
                    {
                        "name": name,
                        "url": url,
                        "front_image_url": front_image_url,
                        "price": price,
                        "source": "PWCC",
                        # "end_date": "TBD",
                        # "id": f"pwcc-{uuid.uuidv4()}" # TODO: pull actual pwcc id, potentially f"{auction}-{lot#}"
                    }
                )
            yield page, items

            if page != num_pages:
                next_url = self._get_search_url(query, page + 1)
                self.browser.get(next_url, PWCC_TIMEOUT)
                self.browser.press(Keys.ESCAPE)
                self.browser.scroll_down_page()
                dom = self.browser.get_dom()

    def search_historical(self):
        historical_url = "https://sales-history.pwccmarketplace.com/?title=pokemon"
        self.browser.get(historical_url, PWCC_TIMEOUT + 5)
        self.browser.press(Keys.ESCAPE)
        self.browser.scroll_down_page()

        return self.browser.get_dom()

        loop = True
        seen = set()

        for i in range(3):
            self.browser.scroll()
            dom = self.browser.get_dom()

            raw_items = list(dom.find_all("div", class_="gridItemList")[0].children)
            items = []
            for raw_item in raw_items:
                title_a = raw_item.find("a", attrs={"data-testid": "item-title"})
                front_image_url = list(
                    raw_item.find("a", attrs={"data-testid": "item-image"}).children
                )[0]["src"]
                price = None
                try:
                    price_item = raw_item.find(
                        "span", attrs={"data-testid": "price-label-current-bid-value"}
                    )
                    price = list(price_item.children)[2].text[1:]
                except Exception as e_curr:
                    try:
                        price_item = raw_item.find(
                            "span",
                            attrs={"data-testid": "price-label-starting-bid-value"},
                        )
                        price = list(price_item.children)[2].text[1:]
                    except Exception as e_start:
                        print("Failed to grab price", e_curr, e_start)

                try:
                    price = float(re.sub("[^0-9|.]", "", price))
                except Exception as e:
                    print("Failed to convert price to float", e)
                    price = None

                name = title_a["title"]
                url = title_a["href"]

                items.append(
                    {
                        "name": name,
                        "url": url,
                        "front_image_url": front_image_url,
                        "price": price,
                        "source": "PWCC",
                        "active": False,
                    }
                )
            yield items

            loop = False
