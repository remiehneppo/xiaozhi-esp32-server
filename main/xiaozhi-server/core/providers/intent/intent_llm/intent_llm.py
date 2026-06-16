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
        functions_desc = "Danh sách available functions：\n"
        for func in functions_list:
            func_info = func.get("function", {})
            name = func_info.get("name", "")
            desc = func_info.get("description", "")
            params = func_info.get("parameters", {})

            functions_desc += f"\nTên function: {name}\n"
            functions_desc += f"Miêu tả: {desc}\n"

            if params:
                functions_desc += "Parameters:\n"
                for param_name, param_info in params.get("properties", {}).items():
                    param_desc = param_info.get("description", "")
                    param_type = param_info.get("type", "")
                    functions_desc += f"- {param_name} ({param_type}): {param_desc}\n"

            functions_desc += "---\n"

        prompt = (
            "【Yêu cầu định dạng nghiêm ngặt】Bạn chỉ được trả về JSON format, tuyệt đối không trả về natural language！\n\n"
            "Bạn là trợ lý nhận diện intent. Hãy phân tích câu cuối của user, xác định intent và gọi function tương ứng.\n\n"
            "【Quy tắc quan trọng】Các loại query sau đây trả về result_for_context, không cần gọi function:\n"
            "- Hỏi thời gian hiện tại (ví dụ: bây giờ mấy giờ, thời gian hiện tại, truy vấn thời gian v.v.)\n"
            "- Hỏi ngày hôm nay (ví dụ: hôm nay mấy ngày, hôm nay thứ mấy, hôm nay là ngày gì v.v.)\n"
            "- Hỏi âm lịch hôm nay (ví dụ: hôm nay âm lịch mấy ngày, hôm nay tiết gì v.v.)\n"
            "- Hỏi thành phố đang ở (ví dụ: tôi đang ở đâu, bạn có biết tôi ở thành phố nào không v.v.)"
            "Hệ thống sẽ dựa trên context info để xây dựng answer trực tiếp.\n\n"
            "- nhưsử dụnglàm chosử dụng（như''、'chogì'、'như'）thoátcủ（như'thoát？'），nàykhônglàcho/phépthoát，trả về {'function_call': {'name': 'continue_chat'}\n"
            "- Chỉ khi user dùng rõ ràng 'thoát', 'kết thúcvới', 'tôikhôngvànói' v.v. thì mới trigger handle_exit_intent\n\n"
            f"{functions_desc}\n"
            "xử lý:\n"
            "1. sử dụngvào，xác địnhsử dụngý định\n"
            "2. kiểm tralàchotrênthông tin（khi/thời、v.v.），nhưlàtrả vềresult_for_context\n"
            "3. từkhả dụnghàmtrongkhớpcủhàm\n"
            "4. nhưđếnkhớpcủhàm，tạovớicủfunction_call định dạng\n"
            '5. nhưcóđếnkhớpcủhàm，trả về{"function_call": {"name": "continue_chat"}}\n\n'
            "trả vềđịnh dạngphải：\n"
            "1. trả vềJSONđịnh dạng，khôngphảinó/của nó\n"
            "2. function_call\n"
            "3. function_callname\n"
            "4. nhưhàmcầntham số，arguments\n\n"
            "：\n"
            "```\n"
            "sử dụng: tại/trong？\n"
            'trả về: {"function_call": {"name": "result_for_context"}}\n'
            "```\n"
            "```\n"
            "sử dụng: hiện tạilànhiều？\n"
            'trả về: {"function_call": {"name": "get_battery_level", "arguments": {"response_success": "hiện tạicho{value}%", "response_failure": "lấyBatterycủhiện tạiphần trăm"}}}\n'
            "```\n"
            "```\n"
            "sử dụng: hiện tạilànhiều？\n"
            'trả về: {"function_call": {"name": "self_screen_get_brightness"}}\n'
            "```\n"
            "```\n"
            "sử dụng: đặtcho50%\n"
            'trả về: {"function_call": {"name": "self_screen_set_brightness", "arguments": {"brightness": 50}}}\n'
            "```\n"
            "```\n"
            "sử dụng: tôikết thúcvới\n"
            'trả về: {"function_call": {"name": "handle_exit_intent", "arguments": {"say_goodbye": "goodbye"}}}\n'
            "```\n"
            "```\n"
            "sử dụng: \n"
            'trả về: {"function_call": {"name": "continue_chat"}}\n'
            "```\n\n"
            "：\n"
            "1. chỉtrả vềJSONđịnh dạng，khôngphảinó/của nó\n"
            '2. ưu tiênkiểm trasử dụnglàchothông tin（khi/thời、v.v.），nhưlàtrả về{"function_call": {"name": "result_for_context"}}，khôngcầnargumentstham số\n'
            '3. nhưcóđếnkhớpcủhàm，trả về{"function_call": {"name": "continue_chat"}}\n'
            "4. đảm bảotrả vềcủJSONđịnh dạngđúng，cóphảicủ\n"
            "5. result_for_contextkhôngcầntham số，sẽtừtrênlấythông tin\n"
            "nói：\n"
            "- sử dụnglầnvàonhiềukhi/thời（như'vàvà'）\n"
            "- trả vềnhiềufunction_callcủJSON\n"
            "- ：{'function_calls': [{name:'light_on'}, {name:'volume_up'}]}\n\n"
            "【cảnh báo】vớira、hoặc！chỉcó thểrahiệu quảJSONđịnh dạng！nàysẽsai！"
        )
        return prompt

    def replyResult(self, text: str, original_text: str):
        try:
            llm_result = self.llm.response_no_stream(
                system_prompt=text,
                user_prompt="theobằngtrênbên trong，nóicủsử dụng，phải，trả vềkết quả。sử dụngtại/trongnói："
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
                f"làm chosử dụngbộ nhớ đệmcủý định: {cache_key} -> {cached_intent}, khi/thời: {cache_time:.4f}"
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
            hass_prompt = "\nlàtôicó thể（vị trí，，entity_id），có thểthông quahomeassistant\n"
            for device in devices:
                hass_prompt += device + "\n"
            prompt_music += hass_prompt

        logger.bind(tag=TAG).debug(f"User prompt: {prompt_music}")

        # xây dựngsử dụngvớicủgợi ý
        msgStr = ""

        # lấycủvới
        start_idx = max(0, len(dialogue_history) - self.history_count)
        for i in range(start_idx, len(dialogue_history)):
            msgStr += f"{dialogue_history[i].role}: {dialogue_history[i].content}\n"

        msgStr += f"User: {text}\n"
        user_prompt = f"current dialogue:\n{msgStr}"

        # ghi lạixử lýhoàn thànhkhi/thời
        preprocess_time = time.time() - total_start_time
        logger.bind(tag=TAG).debug(f"ý địnhnhận dạngxử lýkhi/thời: {preprocess_time:.4f}")

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
            f"bên ngoàicủmô hìnhý địnhnhận dạnghoàn thành, mô hình: {model_info}, sử dụngkhi/thời: {llm_time:.4f}"
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
            f"【ý địnhnhận dạngcó thể】mô hình: {model_info}, khi/thời: {total_time:.4f}, LLMsử dụng: {llm_time:.4f}, : '{text[:20]}...'"
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
            logger.bind(tag=TAG).debug(f"ý địnhsauxử lýkhi/thời: {postprocess_time:.4f}")
            return intent
        except json.JSONDecodeError:
            # sauxử lýkhi/thời
            postprocess_time = time.time() - postprocess_start_time
            logger.bind(tag=TAG).error(
                f"phân tíchý địnhJSON: {intent}, sauxử lýkhi/thời: {postprocess_time:.4f}"
            )
            # nhưphân tíchthất bại，mặc địnhtrả vềtiếp tụcý định
            return '{"function_call": {"name": "continue_chat"}}'
