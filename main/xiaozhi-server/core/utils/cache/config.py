"""
bộ nhớ đệmcấu hình
"""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass
from .strategies import CacheStrategy


class CacheType(Enum):
    """bộ nhớ đệm"""

    LOCATION = "location"
    WEATHER = "weather"
    LUNAR = "lunar"
    INTENT = "intent"
    IP_INFO = "ip_info"
    CONFIG = "config"
    DEVICE_PROMPT = "device_prompt"
    VOICEPRINT_HEALTH = "voiceprint_health"  # nhận dạngkiểm tra
    AUDIO_DATA = "audio_data"  # dữ liệu âm thanhbộ nhớ đệm


@dataclass
class CacheConfig:
    """bộ nhớ đệmcấu hình"""

    strategy: CacheStrategy = CacheStrategy.TTL
    ttl: Optional[float] = 300  # mặc định5
    max_size: Optional[int] = 1000  # mặc định1000
    cleanup_interval: float = 60  # dọn dẹp（）

    @classmethod
    def for_type(cls, cache_type: CacheType) -> "CacheConfig":
        """theobộ nhớ đệmtrả vềcấu hình"""
        configs = {
            CacheType.LOCATION: cls(
                strategy=CacheStrategy.TTL, ttl=None, max_size=1000  # 
            ),
            CacheType.IP_INFO: cls(
                strategy=CacheStrategy.TTL, ttl=86400, max_size=1000  # 24thời
            ),
            CacheType.WEATHER: cls(
                strategy=CacheStrategy.TTL, ttl=28800, max_size=1000  # 8thời
            ),
            CacheType.LUNAR: cls(
                strategy=CacheStrategy.TTL, ttl=2592000, max_size=365  # 30qua
            ),
            CacheType.INTENT: cls(
                strategy=CacheStrategy.TTL_LRU, ttl=600, max_size=1000  # 10
            ),
            CacheType.CONFIG: cls(
                strategy=CacheStrategy.FIXED_SIZE, ttl=None, max_size=20  # 
            ),
            CacheType.DEVICE_PROMPT: cls(
                strategy=CacheStrategy.TTL, ttl=None, max_size=1000  # 
            ),
            CacheType.VOICEPRINT_HEALTH: cls(
                strategy=CacheStrategy.TTL, ttl=600, max_size=100  # 10qua
            ),
            CacheType.AUDIO_DATA: cls(
                strategy=CacheStrategy.TTL, ttl=600, max_size=100  # 10qua
            ),
        }
        return configs.get(cache_type, cls())
