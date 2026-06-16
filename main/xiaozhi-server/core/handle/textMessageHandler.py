from abc import abstractmethod, ABC
from typing import Dict, Any

from core.handle.textMessageType import TextMessageType

TAG = __name__


class TextMessageHandler(ABC):
    """tin nhắnxử lý"""

    @abstractmethod
    async def handle(self, conn, msg_json: Dict[str, Any]) -> None:
        """xử lýtin nhắnphương pháp"""
        pass

    @property
    @abstractmethod
    def message_type(self) -> TextMessageType:
        """trả vềxử lýtin nhắn"""
        pass
