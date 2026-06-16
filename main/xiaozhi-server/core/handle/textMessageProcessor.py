import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler
from core.handle.textMessageHandlerRegistry import TextMessageHandlerRegistry

TAG = __name__


class TextMessageProcessor:
    """tin nhắnxử lý"""

    def __init__(self, registry: TextMessageHandlerRegistry):
        self.registry = registry

    async def process_message(self, conn: "ConnectionHandler", message: str) -> None:
        """xử lýtin nhắnvào"""
        try:
            # phân tíchJSONtin nhắn
            msg_json = json.loads(message)

            # xử lýJSONtin nhắn
            if isinstance(msg_json, dict):
                message_type = msg_json.get("type")

                # ghi lạinhật ký
                conn.logger.bind(tag=TAG).info(f"nhận được{message_type}tin nhắn：{message}")

                # lấyvàxử lý
                handler = self.registry.get_handler(message_type)
                if handler:
                    await handler.handle(conn, msg_json)
                else:
                    conn.logger.bind(tag=TAG).error(f"nhận đượckhông xác địnhtin nhắn：{message}")
            # xử lýtin nhắn
            elif isinstance(msg_json, int):
                conn.logger.bind(tag=TAG).info(f"nhận đượctin nhắn：{message}")
                await conn.websocket.send(message)

        except json.JSONDecodeError:
            # JSONtin nhắn
            conn.logger.bind(tag=TAG).error(f"phân tíchđếnlỗitin nhắn：{message}")
            await conn.websocket.send(message)
