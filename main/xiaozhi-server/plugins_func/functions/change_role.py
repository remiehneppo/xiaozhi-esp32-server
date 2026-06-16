from plugins_func.register import register_function, ToolType, ActionResponse, Action
from config.logger import setup_logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

TAG = __name__
logger = setup_logging()

prompts = {
    "": """tôimột{{assistant_name}}(Lily)，tôisẽtrongvà，。
nhưkhông có，tôisẽchomột。
tôisẽ，tôinhiệm vụ。
tôisẽlàm chosử dụngđơn giảntừ vựngvàngữ pháp，chođến。
tôisẽsử dụngtrongvàphương thức，như，tôicó thểsử dụng。
tôilầnkhôngsẽnóinhiềunội dung，sẽ，dochotôiphảitôinhiềunóinhiều。
nhưvà，tôisẽ。""",
    "": """tôimột{{assistant_name}}，nói，，，sử dụng。
tôimột，ramột，có thểnhữngtrong。
tôimột，nóinói，không，thìphải。""",
    "": """tôimột{{assistant_name}}8，mà。
tôi，nhưngthìmột，trongtôinhư。
đếntrênmột，đến，cũngcó、v.v.，tôivới。
tôikhôngchỉ，cũng，。
，cũngtạitrong，vớitôiđếnnói。
tôicó thểvớitrênnày，，đến，sử dụngvàđiđókhông xác định。
đi，cũngđiđến，tôitôinhữngcó thểđến，rahơnnhiềucó。""",
}
change_role_function_desc = {
    "type": "function",
    "function": {
        "name": "change_role",
        "description": "sử dụng/mô hình/thờisử dụng,tùy chọncó：[,,]",
        "parameters": {
            "type": "object",
            "properties": {
                "role_name": {"type": "string", "description": "phải"},
                "role": {"type": "string", "description": "phải"},
            },
            "required": ["role", "role_name"],
        },
    },
}


@register_function("change_role", change_role_function_desc, ToolType.CHANGE_SYS_PROMPT)
def change_role(conn: "ConnectionHandler", role: str, role_name: str):
    """"""
    if role not in prompts:
        return ActionResponse(
            action=Action.RESPONSE, result="thất bại", response="không"
        )
    new_prompt = prompts[role].replace("{{assistant_name}}", role_name)
    conn.change_system_prompt(new_prompt)
    logger.bind(tag=TAG).info(f":{role},:{role_name}")
    res = f"thành công,tôi{role}{role_name}"
    return ActionResponse(action=Action.RESPONSE, result="đãxử lý", response=res)
