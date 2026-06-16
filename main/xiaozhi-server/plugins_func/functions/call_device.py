"""công cụ"""
import requests
from typing import TYPE_CHECKING

from config.logger import setup_logging
from plugins_func.register import register_function, ToolType, ActionResponse, Action

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

TAG = __name__
logger = setup_logging()

call_device_function_desc = {
    "type": "function",
    "function": {
        "name": "call_device",
        "description": (
            "dùng chogiọng nóikết nối。"
            "sử dụngnóirabằngý địnhthờisử dụngnàycông cụ：\n"
            "1. ：sử dụngnói”XX/choXX/XX/choXX/tôiXX”thờisử dụng，nicknameXX。"
            "như：””→nickname=””、”tôi”→nickname=””；\n"
            "2. đến：gợi ý”nhận đượcđếnXXđến，có？”sau，sử dụngnói”////hội thoại”thờisử dụng，"
            "nicknamegợi ýtrongXX。\n"
            "nhưsử dụngđầu vàokhông，không，khôngsử dụngcall_device，lần"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "nickname": {"type": "string", "description": "，như：、"},
            },
            "required": ["nickname"],
        },
    },
}


def _request_api(url: str, params: dict, headers: dict) -> requests.Response:
    return requests.get(url, params=params, headers=headers, timeout=10)


def _failed_reply(msg: str) -> ActionResponse:
    return ActionResponse(action=Action.RESPONSE, response=msg)


@register_function("call_device", call_device_function_desc, ToolType.SYSTEM_CTL)
def call_device(conn: "ConnectionHandler", nickname: str):
    caller_mac = conn.headers.get("device-id")
    if not caller_mac:
        return _failed_reply("lấyMACđịa chỉ")

    api_config = conn.config.get("manager-api", {})
    api_url = api_config.get("url")
    api_secret = api_config.get("secret")
    if not api_url or not api_secret:
        logger.bind(tag=TAG).error("manager-apicấu hình")
        return _failed_reply("cấu hìnhlỗi，sau")

    headers = {"Authorization": f"Bearer {api_secret}"}

    # 
    try:
        resp = _request_api(
            f"{api_url}/device/address-book/lookup",
            params={"callerMac": caller_mac, "nickname": nickname},
            headers=headers,
        )
        result = resp.json()
    except requests.RequestException as e:
        logger.bind(tag=TAG).error(f"yêu cầuthất bại: {e}")
        return _failed_reply("thất bại，sau")

    if result.get("code") != 0 or not result.get("data"):
        return _failed_reply(f"đếncho'{nickname}'")

    data = result["data"]
    target_mac = data.get("targetMac")
    caller_nickname = data.get("callerNickname")
    has_permission = data.get("hasPermission")

    if not target_mac:
        return _failed_reply(f"đếncho'{nickname}'")
    if not caller_nickname:
        return _failed_reply("thất bại，khôngvới")
    if not has_permission:
        return _failed_reply("thất bại，không có")

    # thông quaJavatrongsử dụng
    try:
        resp = _request_api(
            f"{api_url}/device/call/forward",
            params={"callerMac": caller_mac, "targetMac": target_mac, "callerNickname": caller_nickname},
            headers=headers,
        )
        result = resp.json()
    except requests.RequestException as e:
        logger.bind(tag=TAG).error(f"yêu cầuthất bại: {e}")
        return _failed_reply("thất bại，sau")

    if result.get("code") != 0:
        return _failed_reply(result.get("msg", "thất bại"))

    call_data = result.get("data", {})
    if call_data.get("status") == "offline":
        return _failed_reply(call_data.get("message"))

    conn.calling = True
    return ActionResponse(action=Action.NONE, response=f"tại{nickname}，chờvới")