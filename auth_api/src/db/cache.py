"""Implement Cache."""
import datetime
import logging
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any, Union


class CacheStorage(ABC):
    @abstractmethod
    def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    def set(self, key: str, value: str, ex: Union[int, datetime.timedelta], **kwargs):
        pass

    @abstractmethod
    def delete(self, key: str):
        pass


class BaseCache(ABC):
    @abstractmethod
    def gen_cache_key(self, **kwargs):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def delete(self, key):
        pass


class Cache(BaseCache):
    """Implement cache storage interface."""

    def __init__(self, cache: CacheStorage, ttl: int, prefix: str):
        """Generate a name for key.
        Args:
            ttl: Time to live of a key.
            Cache: AsyncCacheStorage.
            prefix: Prefix for key of the object.
        """
        self.cache = cache
        self.ttl = ttl
        self.prefix = prefix

    @lru_cache()
    def gen_cache_key(self, **kwargs) -> str:
        """Generate a name for key.
        Args:
            kwargs: Uses key/value to generate key string.
        Returs:
            str: Cache key name.
        """
        kwargs = dict(sorted(kwargs.items()))
        id = kwargs.pop('id', None)
        if id:
            key_strings = [f"{id}_{self.prefix}"]
        else:
            key_strings = [self.prefix]

        for key, value in kwargs.items():
            key_strings.append(f"{key}::{value}")
        return '::'.join(key_strings)

    def get(self, key) -> Any:
        """Get data from Cache.
        Args:
            key: Key to retrieve data.
        Returns:
            Any: Any data from cache gotten by key name.
        """
        data = self.cache.get(key)
        return data

    def set(self, key, value) -> None:
        """Save data to Cache.
        Args:
            key: A key for the saving value
            value: The value will be saved to Cache.
        """
        self.cache.set(key, value, ex=self.ttl)
        logging.debug('Success to Put data to cache')

    def delete(self, key):
        self.cache.delete(key)
        logging.debug('Key %s deleted.', key)
