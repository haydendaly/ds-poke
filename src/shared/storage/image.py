import asyncio
import os

import requests
from PIL import Image

from src.shared.storage.base import Database, Storage


class ImageStorage(Storage):
    def __init__(self, path: str, db: Database = Database.LOCAL):
        super().__init__(path, db.value, "jpg")

    def download_to_id(self, url: str, image_id: str, return_img=True):
        try:
            path = f"{self.base_path}/{image_id}.{self.extension}"
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to download {url}")
            with open(path, "wb") as f:
                f.write(response.content)
            if return_img:
                return path, Image.open(path)
        except Exception as e:
            print(e)
        return "", None

    async def download_to_id_async(self, url: str, image_id: str):
        loop = asyncio.get_event_loop()
        path = f"{self.base_path}/{image_id}.{self.extension}"
        if not os.path.exists(path):
            response = await loop.run_in_executor(None, requests.get, url)
            if response.status_code == 200:
                with open(path, "wb") as f:
                    f.write(response.content)
                return True
            else:
                print(
                    f"Failed to download {url} with status code {response.status_code}"
                )
        return False

    def get(self, image_id: str):
        if not self.has(image_id):
            return None
        return Image.open(f"{self.base_path}/{image_id}.{self.extension}")

    # def get_cv2(self, image_id: str):
    #     if not self.has(image_id):
    #         return None
    #     return cv2.imread(f"{self.base_path}/{image_id}.{self.extension}")
