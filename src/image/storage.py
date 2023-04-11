import asyncio
import os
from enum import Enum

import requests
from PIL import Image

SSD_NAME = "T7"


class ImageDatabase(Enum):
    LOCAL = "db/images"
    SAMSUNG_T7 = f"/Volumes/{SSD_NAME}/db/images"


class ImageStorage:
    def __init__(self, path: str, db: ImageDatabase = ImageDatabase.LOCAL):
        self.base_path = f"{db.value}/{path}"
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def download_image_to_id(self, url: str, image_id: str, return_img=True):
        try:
            path = f"{self.base_path}/{image_id}.jpg"
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

    async def download_image_to_id_async(self, url: str, image_id: str):
        loop = asyncio.get_event_loop()
        path = f"{self.base_path}/{image_id}.jpg"
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

    def get_image(self, image_id: str):
        if not self.has_image(image_id):
            return None
        return Image.open(f"{self.base_path}/{image_id}.jpg")

    def has_image(self, image_id: str):
        return os.path.exists(f"{self.base_path}/{image_id}.jpg")

    def delete_image(self, image_id: str):
        if not self.has_image(image_id):
            raise FileNotFoundError
        return os.remove(f"{self.base_path}/{image_id}.jpg")
