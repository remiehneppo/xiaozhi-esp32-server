import importlib
import logging
import os
import sys
import time
import wave
import uuid
from abc import ABC, abstractmethod
from typing import Optional, Tuple, List
from core.providers.asr.base import ASRProviderBase
from config.logger import setup_logging

TAG = __name__
logger = setup_logging()

def create_instance(class_name: str, *args, **kwargs) -> ASRProviderBase:
    """Tạo instance ASR bằng factory method"""
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'providers', 'asr', f'{class_name}.py')):
        lib_name = f'core.providers.asr.{class_name}'
        if lib_name not in sys.modules:
            sys.modules[lib_name] = importlib.import_module(f'{lib_name}')
        return sys.modules[lib_name].ASRProvider(*args, **kwargs)

    raise ValueError(f"Kiểu ASR không được hỗ trợ: {class_name}, hãy kiểm tra cấu hình `type` có đúng không")
