from enum import Enum

import redis


class CacheDatabase(Enum):
    AUCTION = "auction"


class Cache:
    def __init__(self):
        self.cache = redis.Redis(host="localhost", port=6379, db=0)

    def get(self, database: CacheDatabase, key: str):
        return self.cache.get(f"{database.value}:{key}")

    def set(self, database: CacheDatabase, key: str, value, expiry=None):
        return self.cache.set(f"{database.value}:{key}", value)

    def delete(self, database: CacheDatabase, key: str):
        return self.cache.delete(f"{database.value}:{key}")

    def exists(self, database: CacheDatabase, key: str):
        return self.cache.exists(f"{database.value}:{key}")

    def keys(self, database: CacheDatabase, pattern: str):
        return [
            key.decode("utf-8").split(":", 1)[1]
            for key in self.cache.keys(f"{database.value}:{pattern}")
        ]

    def flush(self, database: CacheDatabase):
        return self.cache.delete(f"{database.value}:*")
