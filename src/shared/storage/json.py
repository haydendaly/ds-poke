import os

import pandas as pd

from src.shared.json import json_dump_file, json_load_file
from src.shared.storage.base import Database, Storage
from src.shared.time import get_date_time_str


class JSONStorage(Storage):
    def __init__(self, path: str, db: Database = Database.LOCAL):
        super().__init__(path, db.value, "json")

    def get(self, json_id: str, default=[]):
        if not self.has(json_id):
            return default
        with open(f"{self.base_path}/{json_id}.{self.extension}", "r") as f:
            data = json_load_file(f)
            return data["data"]

    def set(self, json_id: str, data):
        data_with_metadata = {"last_updated": get_date_time_str(), "data": data}
        with open(f"{self.base_path}/{json_id}.{self.extension}", "w") as f:
            json_dump_file(data_with_metadata, f)

    def get_df(self, json_id: str):
        return pd.DataFrame(self.get(json_id))

    def get_all_keys(self):
        return [
            p[: -(len(self.extension) + 1)]
            for p in os.listdir(self.base_path)
            if p.endswith(self.extension) and p[0:2] != "._"
        ]

    def get_all_keys_recursive(self):
        result = []
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(self.extension) and not file.startswith("._"):
                    relative_path = os.path.relpath(root, self.base_path)
                    key = os.path.join(
                        relative_path, file[: -(len(self.extension) + 1)]
                    )
                    result.append(key)
        return result
