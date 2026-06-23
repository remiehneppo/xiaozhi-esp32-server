from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler
from ..base import IntentProviderBase
from plugins_func.functions.play_music import initialize_music_handler
from config.logger import setup_logging
from core.utils.util import get_system_error_response
import re
import json
import hashlib
import time



TAG = __name__
logger = setup_logging()


class IntentProvider(IntentProviderBase):
    def __init__(self, config):
        super().__init__(config)
        self.llm = None
        self.promot = ""
        # Nhập trình quản lý bộ nhớ cache toàn cục
        from core.utils.cache.manager import cache_manager, CacheType

        self.cache_manager = cache_manager
        self.CacheType = CacheType
        self.history_count = 4  # Mặc định dùng 4 đoạn hội thoại gần nhất

    def get_intent_system_prompt(self, functions_list: str) -> str:
        """
        Tạo dynamic system prompt dựa trên intent options và available functions đã cấu hình
        Args:
            functions: Danh sách available functions, JSON format string
        Returns:
            System prompt sau khi format
        """

        # Xây dựng phần function description
        functions_desc = "Danh sách function khả dụng:\n"
        for func in functions_list:
            func_info = func.get("function", {})
            name = func_info.get("name", "")
            desc = func_info.get("description", "")
            params = func_info.get("parameters", {})

            functions_desc += f"\nTên function: {name}\n"
            functions_desc += f"Mô tả: {desc}\n"

            if params:
                functions_desc += "Parameters:\n"
                for param_name, param_info in params.get("properties", {}).items():
                    param_desc = param_info.get("description", "")
                    param_type = param_info.get("type", "")
                    functions_desc += f"- {param_name} ({param_type}): {param_desc}\n"

            functions_desc += "---\n"

        prompt = (
            "Bạn là bộ phân loại ý định cho trợ lý giọng nói tiếng Việt.\n"
            "Nhiệm vụ: đọc câu cuối của người dùng trong hội thoại hiện tại và trả về đúng một JSON hợp lệ.\n"
            "Không giải thích, không Markdown, không thêm văn bản ngoài JSON.\n\n"
            "Các intent dùng ngữ cảnh sẵn có, trả về result_for_context, không gọi công cụ khác:\n"
            "- Hỏi giờ hiện tại: 'mấy giờ rồi', 'bây giờ là mấy giờ'.\n"
            "- Hỏi ngày/thứ hôm nay: 'hôm nay ngày mấy', 'hôm nay thứ mấy'.\n"
            "- Hỏi âm lịch hôm nay: 'hôm nay âm lịch ngày bao nhiêu'.\n"
            "- Hỏi vị trí thiết bị/ngữ cảnh địa phương: 'tôi đang ở đâu'.\n\n"
            "Quy tắc thoát hội thoại:\n"
            "- Chỉ gọi handle_exit_intent khi người dùng nói rõ muốn dừng: 'thoát', 'tạm biệt', 'dừng lại', 'ngủ đi', 'hẹn gặp lại', 'không nói nữa'.\n"
            "- Nếu người dùng chỉ hỏi nghĩa của từ thoát, ví dụ 'thoát là gì', 'nút thoát ở đâu', thì trả về continue_chat.\n\n"
            f"{functions_desc}\n"
            "Quy trình phân loại:\n"
            "1. Xác định ý định chính của câu cuối, có xét vài lượt hội thoại gần nhất.\n"
            "2. Nếu câu hỏi thuộc nhóm dùng ngữ cảnh sẵn có, trả về result_for_context.\n"
            "3. Nếu có function khớp rõ ràng, trả về function_call với name và arguments cần thiết.\n"
            "4. Nếu không chắc hoặc không cần công cụ, trả về continue_chat.\n"
            "5. Với nhiều lệnh trong một câu, chỉ chọn lệnh quan trọng/rõ nhất vì hệ thống chỉ xử lý một function_call.\n\n"
            "Định dạng trả về bắt buộc:\n"
            '{"function_call": {"name": "ten_function", "arguments": {}}}\n'
            "Nếu không có arguments thì có thể bỏ trường arguments.\n\n"
            "Ví dụ:\n"
            'User: "mấy giờ rồi" -> {"function_call": {"name": "result_for_context"}}\n'
            'User: "pin còn bao nhiêu phần trăm" -> {"function_call": {"name": "get_battery_level", "arguments": {"response_success": "Pin hiện còn {value}%.", "response_failure": "Mình chưa lấy được mức pin hiện tại."}}}\n'
            'User: "độ sáng màn hình hiện tại bao nhiêu" -> {"function_call": {"name": "self_screen_get_brightness"}}\n'
            'User: "đặt độ sáng màn hình 50 phần trăm" -> {"function_call": {"name": "self_screen_set_brightness", "arguments": {"brightness": 50}}}\n'
            'User: "tạm biệt nhé" -> {"function_call": {"name": "handle_exit_intent", "arguments": {"say_goodbye": "Tạm biệt, hẹn gặp lại bạn nhé."}}}\n'
            'User: "kể tôi nghe một chuyện vui" -> {"function_call": {"name": "continue_chat"}}\n\n'
            "Nhắc lại: chỉ trả về JSON hợp lệ."
        )
        return prompt

    def replyResult(self, text: str, original_text: str):
        try:
            llm_result = self.llm.response_no_stream(
                system_prompt=text,
                user_prompt="Dựa vào ngữ cảnh phía trên, hãy trả lời ngắn gọn bằng tiếng Việt cho câu người dùng: "
                + original_text,
            )
            return llm_result
        except Exception as e:
            logger.bind(tag=TAG).error(f"Error in generating reply result: {e}")
            return get_system_error_response(self.config)

    async def detect_intent(
        self, conn: "ConnectionHandler", dialogue_history: List[Dict], text: str
    ) -> str:
        if not self.llm:
            raise ValueError("LLM provider not set")
        if conn.func_handler is None:
            return '{"function_call": {"name": "continue_chat"}}'

        # ghi lạibắt đầukhi/thời
        total_start_time = time.time()

        # làm chosử dụngcủmô hìnhthông tin
        model_info = getattr(self.llm, "model_name", str(self.llm.__class__.__name__))
        logger.bind(tag=TAG).debug(f"làm chosử dụngý địnhnhận dạngmô hình: {model_info}")

        # tính toánbộ nhớ đệm
        cache_key = hashlib.md5((conn.device_id + text).encode()).hexdigest()

        # kiểm trabộ nhớ đệm
        cached_intent = self.cache_manager.get(self.CacheType.INTENT, cache_key)
        if cached_intent is not None:
            cache_time = time.time() - total_start_time
            logger.bind(tag=TAG).debug(
                f"Dùng intent cache: {cache_key} -> {cached_intent}, thời gian: {cache_time:.4f}"
            )
            return cached_intent

        if self.promot == "":
            functions = conn.func_handler.get_functions()
            if hasattr(conn, "mcp_client"):
                mcp_tools = conn.mcp_client.get_available_tools()
                if mcp_tools is not None and len(mcp_tools) > 0:
                    if functions is None:
                        functions = []
                    functions.extend(mcp_tools)

            self.promot = self.get_intent_system_prompt(functions)

        music_config = initialize_music_handler(conn)
        music_file_names = music_config["music_file_names"]
        prompt_music = f"{self.promot}\n<musicNames>{music_file_names}\n</musicNames>"

        home_assistant_cfg = conn.config["plugins"].get("home_assistant")
        if home_assistant_cfg:
            devices = home_assistant_cfg.get("devices", [])
        else:
            devices = []
        if len(devices) > 0:
            hass_prompt = "\nDanh sách thiết bị Home Assistant có thể điều khiển (phòng, tên thiết bị, entity_id):\n"
            for device in devices:
                hass_prompt += device + "\n"
            prompt_music += hass_prompt

        logger.bind(tag=TAG).debug(f"User prompt: {prompt_music}")

        # Xây dựng hội thoại gần nhất cho prompt phân loại intent.
        msgStr = ""

        # lấycủvới
        start_idx = max(0, len(dialogue_history) - self.history_count)
        for i in range(start_idx, len(dialogue_history)):
            msgStr += f"{dialogue_history[i].role}: {dialogue_history[i].content}\n"

        msgStr += f"User: {text}\n"
        user_prompt = f"Hội thoại hiện tại:\n{msgStr}"

        # ghi lạixử lýhoàn thànhkhi/thời
        preprocess_time = time.time() - total_start_time
        logger.bind(tag=TAG).debug(f"Tiền xử lý nhận diện intent: {preprocess_time:.4f}")

        # Dùng LLM để nhận diện intent
        llm_start_time = time.time()
        logger.bind(tag=TAG).debug(f"bắt đầuLLMý địnhnhận dạngsử dụng, mô hình: {model_info}")

        try:
            intent = self.llm.response_no_stream(
                system_prompt=prompt_music, user_prompt=user_prompt
            )
        except Exception as e:
            logger.bind(tag=TAG).error(f"Error in intent detection LLM call: {e}")
            return '{"function_call": {"name": "continue_chat"}}'

        # ghi lạiLLMsử dụnghoàn thànhkhi/thời
        llm_time = time.time() - llm_start_time
        logger.bind(tag=TAG).debug(
            f"LLM nhận diện intent hoàn thành, mô hình: {model_info}, thời gian: {llm_time:.4f}"
        )

        # ghi lạisauxử lýbắt đầukhi/thời
        postprocess_start_time = time.time()

        # dọn dẹpvàphân tíchphản hồi
        intent = intent.strip()
        # cố gắngJSONphần
        match = re.search(r"\{.*\}", intent, re.DOTALL)
        if match:
            intent = match.group(0)

        # ghi lạixử lýkhi/thời
        total_time = time.time() - total_start_time
        logger.bind(tag=TAG).debug(
            f"Nhận diện intent: mô hình={model_info}, tổng thời gian={total_time:.4f}, LLM={llm_time:.4f}, text='{text[:20]}...'"
        )

        # cố gắngphân tíchchoJSON
        try:
            intent_data = json.loads(intent)
            # nhưfunction_call，định dạngchophù hợpxử lýcủđịnh dạng
            if "function_call" in intent_data:
                function_data = intent_data["function_call"]
                function_name = function_data.get("name")
                function_args = function_data.get("arguments", {})

                # ghi lạinhận dạngđếncủfunction call
                logger.bind(tag=TAG).info(
                    f"llm nhận dạngđếný định: {function_name}, tham số: {function_args}"
                )

                # xử lýkhôngcủý định
                if function_name == "result_for_context":
                    # xử lýthông tin，từcontextxây dựngkết quả
                    logger.bind(tag=TAG).info(
                        "đếnresult_for_contextý định，sẽlàm chosử dụngtrênthông tin"
                    )

                elif function_name == "continue_chat":
                    # xử lývới
                    # giữ lạicông cụcủtin nhắn
                    clean_history = [
                        msg
                        for msg in conn.dialogue.dialogue
                        if msg.role not in ["tool", "function"]
                    ]
                    conn.dialogue.dialogue = clean_history

                else:
                    # xử lýhàmsử dụng
                    logger.bind(tag=TAG).info(f"đếnhàmsử dụngý định: {function_name}")

            # thống nhấtbộ nhớ đệmxử lývàtrả về
            self.cache_manager.set(self.CacheType.INTENT, cache_key, intent)
            postprocess_time = time.time() - postprocess_start_time
            logger.bind(tag=TAG).debug(f"Hậu xử lý intent: {postprocess_time:.4f}")
            return intent
        except json.JSONDecodeError:
            # sauxử lýkhi/thời
            postprocess_time = time.time() - postprocess_start_time
            logger.bind(tag=TAG).error(
                f"Đã phân tích JSON intent: {intent}, hậu xử lý: {postprocess_time:.4f}"
            )
            # nhưphân tíchthất bại，mặc địnhtrả vềtiếp tụcý định
            return '{"function_call": {"name": "continue_chat"}}'
