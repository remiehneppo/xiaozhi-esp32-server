from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler
from core.handle.textMessageHandlerRegistry import TextMessageHandlerRegistry
from core.handle.textMessageProcessor import TextMessageProcessor

TAG = __name__

# toàn cụcxử lý
message_registry = TextMessageHandlerRegistry()

# tạotoàn cụctin nhắnxử lý
message_processor = TextMessageProcessor(message_registry)


async def handleTextMessage(conn: "ConnectionHandler", message):
    """xử lývăn bảntin nhắn"""
    await message_processor.process_message(conn, message)
