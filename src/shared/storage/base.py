import os
from enum import Enum

SSD_NAME = "T7"


class Database(Enum):
    LOCAL = "db/local"
    SAMSUNG_T7 = f"/Volumes/{SSD_NAME}/db"
    SHARED = "db/shared"


class Storage:
    def __init__(self, path: str, db: str, extension: str):
        self.base_path = f"{db}/{extension}/{path}"
        self.extension = extension
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def has(self, data_id: str):
        return os.path.exists(f"{self.base_path}/{data_id}.{self.extension}")

    def delete(self, data_id: str):
        if not self.has(data_id):
            raise FileNotFoundError
        return os.remove(f"{self.base_path}/{data_id}.{self.extension}")

    def get_all_keys(self):
        return [
            p[: -(len(self.extension) + 1)]
            for p in os.listdir(self.base_path)
            if p.endswith(self.extension)
        ]

    def size(self):
        return len(os.listdir(self.base_path))
