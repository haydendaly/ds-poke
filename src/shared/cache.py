from enum import Enum

import redis

from src.shared.json import jsonify


class CacheDatabase(Enum):
    AUCTION = "auction"


class Cache:
    def __init__(self, db: CacheDatabase = CacheDatabase.AUCTION):
        self.cache = redis.Redis(host="localhost", port=6379, db=0)
        self.database = db.value

    def get(self, key: str):
        return self.cache.get(f"{self.database}:{key}")

    def set(self, key: str, value, expiry=None):
        return self.cache.set(f"{self.database}:{key}", jsonify(value))

    def delete(self, key: str):
        return self.cache.delete(f"{self.database}:{key}")

    def exists(self, key: str):
        return self.cache.exists(f"{self.database}:{key}")

    def keys(self, pattern: str):
        return [
            key.decode("utf-8").split(":", 1)[1]
            for key in self.cache.keys(f"{self.database}:{pattern}")
        ]

    def flush(self):
        return self.cache.delete(f"{self.database}:*")
