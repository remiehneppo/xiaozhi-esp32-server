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
        "description": "sử dụngkết thúchội thoạihoặccầnthoátthờisử dụng",
        "parameters": {
            "type": "object",
            "properties": {
                "say_goodbye": {
                    "type": "string",
                    "description": "vàsử dụngkết thúchội thoại",
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
    # xử lýthoátý định
    try:
        if say_goodbye is None:
            say_goodbye = "，！"
        if not conn.close_after_chat:
            conn.close_after_chat = True
        logger.bind(tag=TAG).info(f"Ý định thoát đã được xử lý:{say_goodbye}")
        return ActionResponse(
            action=Action.RESPONSE, result="Ý định thoát đã được xử lý", response=say_goodbye
        )
    except Exception as e:
        logger.bind(tag=TAG).error(f"xử lýthoátý địnhlỗi: {e}")
        return ActionResponse(
            action=Action.NONE, result="thoátý địnhxử lý thất bại", response=""
        )
