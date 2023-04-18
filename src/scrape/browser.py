import aiohttp
import requests
from bs4 import BeautifulSoup

from src.shared.error import NotImplementedError

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.action_chains import ActionChains
# import undetected_chromedriver as uc


# PROXY_KEY = ""


class SSRBrowser:
    def __init__(self, has_proxy=False):
        # self.session = aiohttp.ClientSession()
        self.has_proxy = has_proxy

    def get(self, url):
        res = None
        if self.has_proxy:
            raise NotImplementedError("Proxy not yet supported.")
            # res = self.session.get(
            #     url='https://proxy.scrapeops.io/v1/',
            #     params={
            #         'api_key': PROXY_KEY,
            #         'url': url,
            #         'bypass': 'perimeterx',
            #     }
            # )
        else:
            res = requests.get(url)

        return BeautifulSoup(res.text, "html.parser")

    # async def get_async(self, url):
    #     loop = asyncio.get_event_loop()
    #     # TODO merge implementations
    #     res = await loop.run_in_executor(None, requests.get, url)
    #     return BeautifulSoup(res.text, "html.parser")

    async def get_async(self, url):
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                content = await response.read()
                dom = BeautifulSoup(content, "html.parser")
            return dom


# class CSRBrowser:
#     def __init__(self, headless=True):
#         CHROME_PATH = ChromeDriverManager().install()

#         options = Options()
#         if headless:
#             options.add_argument("--headless")

#         self.service = Service(CHROME_PATH)
#         self.driver = uc.Chrome(service=self.service, options=options)

#         # self.driver = webdriver.Chrome(service=self.service, options=options)
#         # self.driver.maximize_window()

#         # self.request_interceptors = []
#         # self.response_interceptors = []
#         # self.driver.request_interceptor = self.intercept_request
#         # self.driver.response_interceptor = self.intercept_response

#     # def intercept_request(self, request):
#     #     for interceptor in self.request_interceptors:
#     #         interceptor(request)

#     # def intercept_response(self, request, response):
#     #     for interceptor in self.response_interceptors:
#     #         interceptor(request, response)

#     def get(self, url, timeout=0):
#         self.driver.get(url)
#         time.sleep(timeout)

#     def get_dom(self):
#         return BeautifulSoup(self.driver.page_source, "html.parser")

#     def press(self, key):
#         return ActionChains(self.driver).send_keys(key).perform()

#     def scroll_down_page(self, speed=24):
#         current_scroll_position, new_height = 0, 1
#         while current_scroll_position <= new_height:
#             current_scroll_position += speed
#             self.driver.execute_script(
#                 "window.scrollTo(0, {});".format(current_scroll_position)
#             )
#             new_height = self.driver.execute_script("return document.body.scrollHeight")

#     def scroll(self, pixels=2000):
#         c.driver.execute_script(
#             "window.scrollBy({ top: " + pixels + ", behavior: 'smooth' })"
#         )

#     # def add_request_interceptor(self, interceptor):
#     #     self.request_interceptors.append(interceptor)

#     # def add_response_interceptor(self, interceptor):
#     #     self.response_interceptors.append(interceptor)
