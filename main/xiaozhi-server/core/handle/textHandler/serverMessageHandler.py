import asyncio
import json
from typing import Dict, Any

from core.handle.textMessageHandler import TextMessageHandler
from core.handle.textMessageType import TextMessageType
from core.providers.tools.device_mcp import handle_mcp_message

TAG = __name__

class ServerTextMessageHandler(TextMessageHandler):
    """MCPtin nhắnxử lý"""

    @property
    def message_type(self) -> TextMessageType:
        return TextMessageType.SERVER

    async def handle(self, conn, msg_json: Dict[str, Any]) -> None:
        # nhưcấu hìnhAPIđọc，cầnxác thựcsecret
        if not conn.read_config_from_api:
            return
        # lấypostyêu cầusecret
        post_secret = msg_json.get("content", {}).get("secret", "")
        secret = conn.config["manager-api"].get("secret", "")
        # nhưsecretkhôngkhớp，trả về
        if post_secret != secret:
            await conn.websocket.send(
                json.dumps(
                    {
                        "type": "server",
                        "status": "error",
                        "message": "máy chủxác thựcthất bại",
                    }
                )
            )
            return
        # cập nhậtcấu hình
        if msg_json["action"] == "update_config":
            try:
                # cập nhậtWebSocketServercấu hình
                if not conn.server:
                    await conn.websocket.send(
                        json.dumps(
                            {
                                "type": "server",
                                "status": "error",
                                "message": "lấymáy chủ",
                                "content": {"action": "update_config"},
                            }
                        )
                    )
                    return

                if not await conn.server.update_config():
                    await conn.websocket.send(
                        json.dumps(
                            {
                                "type": "server",
                                "status": "error",
                                "message": "cập nhậtmáy chủcấu hìnhthất bại",
                                "content": {"action": "update_config"},
                            }
                        )
                    )
                    return

                # gửi thành côngphản hồi
                await conn.websocket.send(
                    json.dumps(
                        {
                            "type": "server",
                            "status": "success",
                            "message": "cấu hìnhcập nhậtthành công",
                            "content": {"action": "update_config"},
                        }
                    )
                )
            except Exception as e:
                conn.logger.bind(tag=TAG).error(f"cập nhậtcấu hìnhthất bại: {str(e)}")
                await conn.websocket.send(
                    json.dumps(
                        {
                            "type": "server",
                            "status": "error",
                            "message": f"cập nhậtcấu hìnhthất bại: {str(e)}",
                            "content": {"action": "update_config"},
                        }
                    )
                )
        # khởi động lạimáy chủ
        elif msg_json["action"] == "restart":
            await conn.handle_restart(msg_json)