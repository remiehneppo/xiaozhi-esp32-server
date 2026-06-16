from enum import Enum
from typing import Union, Optional


class SentenceType(Enum):
    # nói
    FIRST = "FIRST"  # 
    MIDDLE = "MIDDLE"  # nóitrong
    LAST = "LAST"  # sau


class ContentType(Enum):
    # nội dung
    TEXT = "TEXT"  # văn bảnnội dung
    FILE = "FILE"  # tệpnội dung
    ACTION = "ACTION"  # nội dung


class InterfaceType(Enum):
    # 
    DUAL_STREAM = "DUAL_STREAM"  # luồng
    SINGLE_STREAM = "SINGLE_STREAM"  # luồng
    NON_STREAM = "NON_STREAM"  # luồng


class TTSMessageDTO:
    def __init__(
        self,
        sentence_id: str,
        # nói
        sentence_type: SentenceType,
        # nội dung
        content_type: ContentType,
        # nội dung，cầnchuyển đổivăn bảnhoặcâm thanh
        content_detail: Optional[str] = None,
        # nhưnội dungchotệp，cầnvàotệpđường dẫn
        content_file: Optional[str] = None,
    ):
        self.sentence_id = sentence_id
        self.sentence_type = sentence_type
        self.content_type = content_type
        self.content_detail = content_detail
        self.content_file = content_file
