from plugins_func.register import register_function, ToolType, ActionResponse, Action
from config.logger import setup_logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

TAG = __name__
logger = setup_logging()

handle_exit_intent_function_desc = {
    "type": "function",
    "function": {
        "name": "handle_exit_intent",
        "description": "Gọi khi người dùng nói rõ muốn kết thúc hội thoại, tạm biệt, dừng lại hoặc cho thiết bị nghỉ.",
        "parameters": {
            "type": "object",
            "properties": {
                "say_goodbye": {
                    "type": "string",
                    "description": "Câu tạm biệt ngắn gọn, thân thiện để đọc cho người dùng trước khi kết thúc hội thoại.",
                }
            },
            "required": ["say_goodbye"],
        },
    },
}


@register_function(
    "handle_exit_intent", handle_exit_intent_function_desc, ToolType.SYSTEM_CTL
)
def handle_exit_intent(conn: "ConnectionHandler", say_goodbye: str | None = None):
    # Xử lý ý định thoát hội thoại.
    try:
        if say_goodbye is None:
            say_goodbye = "Tạm biệt, hẹn gặp lại bạn nhé."
        if not conn.close_after_chat:
            conn.close_after_chat = True
        logger.bind(tag=TAG).info(f"Ý định thoát đã được xử lý:{say_goodbye}")
        return ActionResponse(
            action=Action.RESPONSE, result="Ý định thoát đã được xử lý", response=say_goodbye
        )
    except Exception as e:
        logger.bind(tag=TAG).error(f"Xử lý ý định thoát lỗi: {e}")
        return ActionResponse(
            action=Action.NONE, result="Xử lý ý định thoát thất bại", response=""
        )
