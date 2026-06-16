from enum import Enum
from typing import Union, Optional


class InterfaceType(Enum):
    # 
    STREAM = "STREAM"  # luồng
    NON_STREAM = "NON_STREAM"  # luồng
    LOCAL = "LOCAL"  # cục bộdịch vụ
