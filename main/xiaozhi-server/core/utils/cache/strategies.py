"""
bộ nhớ đệmvàdữ liệuđịnh nghĩa
"""

import time
from enum import Enum
from typing import Any, Optional
from dataclasses import dataclass


class CacheStrategy(Enum):
    """bộ nhớ đệm"""

    TTL = "ttl"  # dựa trênthời gianqua
    LRU = "lru"  # làm chosử dụng
    FIXED_SIZE = "fixed_size"  # 
    TTL_LRU = "ttl_lru"  # TTL + LRU


@dataclass
class CacheEntry:
    """bộ nhớ đệmdữ liệu"""

    value: Any
    timestamp: float
    ttl: Optional[float] = None  # thời gian（）
    access_count: int = 0
    last_access: float = None

    def __post_init__(self):
        if self.last_access is None:
            self.last_access = self.timestamp

    def is_expired(self) -> bool:
        """kiểm tracóqua"""
        if self.ttl is None:
            return False
        return time.time() - self.timestamp > self.ttl

    def touch(self):
        """cập nhậtthời gianvà"""
        self.last_access = time.time()
        self.access_count += 1
