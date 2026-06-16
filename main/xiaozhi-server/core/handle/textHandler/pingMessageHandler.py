import json
import time
from typing import Dict, Any

from core.handle.textMessageHandler import TextMessageHandler
from core.handle.textMessageType import TextMessageType

TAG = __name__


class PingMessageHandler(TextMessageHandler):
    """Pingtin nhắnxử lý，dùng choWebSocketkết nối"""

    @property
    def message_type(self) -> TextMessageType:
        return TextMessageType.PING

    async def handle(self, conn, msg_json: Dict[str, Any]) -> None:
        """
        xử lýPINGtin nhắn，gửiPONGphản hồi
        tin nhắnđịnh dạng：{"type": "ping"}
        Args:
            conn: WebSocketkết nốivới
            msg_json: PINGtin nhắnJSONdữ liệu
        """
        # kiểm tracókích hoạtWebSocketcó thể
        enable_websocket_ping = conn.config.get("enable_websocket_ping", False)
        if not enable_websocket_ping:
            conn.logger.debug(f"WebSocketcó thểkích hoạt，PINGtin nhắn")
            return

        try:
            conn.logger.debug(f"nhận đượcPINGtin nhắn，gửiPONGphản hồi")
            conn.last_activity_time = time.time() * 1000
            # PONGphản hồitin nhắn
            pong_message = {
                "type": "pong",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            }

            # gửiPONGphản hồi
            await conn.websocket.send(json.dumps(pong_message))

        except Exception as e:
            conn.logger.error(f"xử lýPINGtin nhắnthờilỗi: {e}")
