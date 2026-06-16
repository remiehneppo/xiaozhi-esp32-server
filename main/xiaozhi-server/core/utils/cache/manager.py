"""
toàn cụcbộ nhớ đệm
"""

import time
import threading
from typing import Any, Optional, Dict
from collections import OrderedDict
from .strategies import CacheStrategy, CacheEntry
from .config import CacheConfig, CacheType


class GlobalCacheManager:
    """toàn cụcbộ nhớ đệm"""

    def __init__(self):
        self._logger = None
        self._caches: Dict[str, Dict[str, CacheEntry]] = {}
        self._configs: Dict[str, CacheConfig] = {}
        self._locks: Dict[str, threading.RLock] = {}
        self._global_lock = threading.RLock()
        self._last_cleanup = time.time()
        self._stats = {"hits": 0, "misses": 0, "evictions": 0, "cleanups": 0}

    @property
    def logger(self):
        """độ trễkhởi tạo logger bằngvào"""
        if self._logger is None:
            from config.logger import setup_logging

            self._logger = setup_logging()
        return self._logger

    def _get_cache_name(self, cache_type: CacheType, namespace: str = "") -> str:
        """tạobộ nhớ đệm"""
        if namespace:
            return f"{cache_type.value}:{namespace}"
        return cache_type.value

    def _get_or_create_cache(
        self, cache_name: str, config: CacheConfig
    ) -> Dict[str, CacheEntry]:
        """lấyhoặctạobộ nhớ đệm"""
        with self._global_lock:
            if cache_name not in self._caches:
                self._caches[cache_name] = (
                    OrderedDict()
                    if config.strategy in [CacheStrategy.LRU, CacheStrategy.TTL_LRU]
                    else {}
                )
                self._configs[cache_name] = config
                self._locks[cache_name] = threading.RLock()
            return self._caches[cache_name]

    def set(
        self,
        cache_type: CacheType,
        key: str,
        value: Any,
        ttl: Optional[float] = None,
        namespace: str = "",
    ) -> None:
        """đặtbộ nhớ đệm"""
        cache_name = self._get_cache_name(cache_type, namespace)
        config = self._configs.get(cache_name) or CacheConfig.for_type(cache_type)
        cache = self._get_or_create_cache(cache_name, config)

        # làm chosử dụngcấu hìnhTTLhoặcvàoTTL
        effective_ttl = ttl if ttl is not None else config.ttl

        with self._locks[cache_name]:
            # tạobộ nhớ đệm
            entry = CacheEntry(value=value, timestamp=time.time(), ttl=effective_ttl)

            # xử lýkhông
            if config.strategy in [CacheStrategy.LRU, CacheStrategy.TTL_LRU]:
                # LRU：nhưđãtạiđến
                if key in cache:
                    del cache[key]
                cache[key] = entry

                # kiểm tra
                if config.max_size and len(cache) > config.max_size:
                    # loại bỏcũ
                    oldest_key = next(iter(cache))
                    del cache[oldest_key]
                    self._stats["evictions"] += 1

            else:
                cache[key] = entry

                # kiểm tra
                if config.max_size and len(cache) > config.max_size:
                    # đơn giản：loại bỏmột
                    victim_key = next(iter(cache))
                    del cache[victim_key]
                    self._stats["evictions"] += 1

        # dọn dẹpqua
        self._maybe_cleanup(cache_name)

    def get(
        self, cache_type: CacheType, key: str, namespace: str = ""
    ) -> Optional[Any]:
        """lấybộ nhớ đệm"""
        cache_name = self._get_cache_name(cache_type, namespace)

        if cache_name not in self._caches:
            self._stats["misses"] += 1
            return None

        cache = self._caches[cache_name]
        config = self._configs[cache_name]

        with self._locks[cache_name]:
            if key not in cache:
                self._stats["misses"] += 1
                return None

            entry = cache[key]

            # kiểm traqua
            if entry.is_expired():
                del cache[key]
                self._stats["misses"] += 1
                return None

            # cập nhậtthông tin
            entry.touch()

            # LRU：đến
            if config.strategy in [CacheStrategy.LRU, CacheStrategy.TTL_LRU]:
                del cache[key]
                cache[key] = entry

            self._stats["hits"] += 1
            return entry.value

    def delete(self, cache_type: CacheType, key: str, namespace: str = "") -> bool:
        """xóabộ nhớ đệm"""
        cache_name = self._get_cache_name(cache_type, namespace)

        if cache_name not in self._caches:
            return False

        cache = self._caches[cache_name]

        with self._locks[cache_name]:
            if key in cache:
                del cache[key]
                return True
            return False

    def clear(self, cache_type: CacheType, namespace: str = "") -> None:
        """chỉ địnhbộ nhớ đệm"""
        cache_name = self._get_cache_name(cache_type, namespace)

        if cache_name not in self._caches:
            return

        with self._locks[cache_name]:
            self._caches[cache_name].clear()

    def invalidate_pattern(
        self, cache_type: CacheType, pattern: str, namespace: str = ""
    ) -> int:
        """chế độbộ nhớ đệm"""
        cache_name = self._get_cache_name(cache_type, namespace)

        if cache_name not in self._caches:
            return 0

        cache = self._caches[cache_name]
        deleted_count = 0

        with self._locks[cache_name]:
            keys_to_delete = [key for key in cache.keys() if pattern in key]
            for key in keys_to_delete:
                del cache[key]
                deleted_count += 1

        return deleted_count

    def _cleanup_expired(self, cache_name: str) -> int:
        """dọn dẹpqua"""
        if cache_name not in self._caches:
            return 0

        cache = self._caches[cache_name]
        deleted_count = 0

        with self._locks[cache_name]:
            expired_keys = [key for key, entry in cache.items() if entry.is_expired()]
            for key in expired_keys:
                del cache[key]
                deleted_count += 1

        return deleted_count

    def _maybe_cleanup(self, cache_name: str):
        """dọn dẹpkiểm tra"""
        config = self._configs.get(cache_name)
        if not config:
            return

        now = time.time()
        if now - self._last_cleanup > config.cleanup_interval:
            self._last_cleanup = now
            deleted = self._cleanup_expired(cache_name)
            if deleted > 0:
                self._stats["cleanups"] += 1
                self.logger.debug(f"dọn dẹpbộ nhớ đệm {cache_name}: xóa {deleted} qua")


# tạotoàn cụcbộ nhớ đệm
cache_manager = GlobalCacheManager()
