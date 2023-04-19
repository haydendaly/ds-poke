import pandas as pd

from src.shared.storage.base import Database, Storage


class DataFrameStorage(Storage):
    def __init__(self, path: str, db: Database = Database.LOCAL):
        super().__init__(path, db.value, "csv")

    def get(self, df_id: str):
        if not self.has(df_id):
            raise FileNotFoundError
        return pd.read_csv(f"{self.base_path}/{df_id}.{self.extension}")

    def set(self, df_id: str, df: pd.DataFrame):
        df.to_csv(f"{self.base_path}/{df_id}.{self.extension}")

    def append(self, df_id: str, df: pd.DataFrame):
        if not self.has(df_id):
            self.set(df_id, df)
        else:
            existing_df = self.get(df_id)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            self.set(df_id, combined_df)
