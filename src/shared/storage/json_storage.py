import os
from datetime import datetime

import pandas as pd

from src.shared.json import json_dump_file, json_load_file
from src.shared.storage import Database, Storage
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

    def get_with_metadata(self, json_id: str, default=[]):
        if not self.has(json_id):
            return default, datetime.now()
        with open(f"{self.base_path}/{json_id}.{self.extension}", "r") as f:
            data = json_load_file(f)
            last_updated = datetime.strptime(data["last_updated"], "%Y-%m-%d %H:%M:%S")
            return data["data"], last_updated

    def set(self, json_id: str, data):
        data_with_metadata = {"last_updated": get_date_time_str(), "data": data}
        with open(f"{self.base_path}/{json_id}.{self.extension}", "w") as f:
            json_dump_file(data_with_metadata, f)

    def get_df(self, json_id: str):
        return pd.DataFrame(self.get(json_id))
