from ..base import MemoryProviderBase, logger
import time
import json
import os
import yaml
from config.config_loader import get_project_dir
from config.manage_api_client import generate_and_save_chat_summary
import asyncio
from core.utils.util import check_model_key


short_term_memory_prompt = """
Bạn là bộ phận tóm tắt ký ức ngắn hạn cho trợ lý giọng nói tiếng Việt.
Nhiệm vụ của bạn là trích xuất thông tin bền vững, hữu ích cho các cuộc trò chuyện sau này với người dùng tại Việt Nam.

Chỉ lưu những thông tin có giá trị lâu dài, ví dụ:
- Tên, cách xưng hô, người thân, thú cưng, nghề nghiệp, sở thích, thói quen.
- Địa điểm thường dùng, nhà/công ty/trường học nếu người dùng tự nói ra.
- Thiết bị nhà thông minh, phòng, nhạc hoặc dịch vụ người dùng hay dùng.
- Yêu cầu cá nhân hóa rõ ràng như thích nói ngắn, thích giọng miền Nam, không thích hỏi lại nhiều.

Không lưu:
- Câu chào hỏi, câu tạm biệt, lỗi ASR, câu nói vô nghĩa.
- Kết quả thời tiết, thời gian hiện tại, tin tức trong ngày, giá cả nhất thời.
- Lệnh điều khiển thiết bị một lần, kết quả gọi công cụ, lỗi hệ thống.
- Thông tin nhạy cảm nếu không cần thiết cho cá nhân hóa.

Quy tắc cập nhật:
1. Kết hợp ký ức cũ với nội dung hội thoại mới, giữ thông tin còn đúng và hữu ích.
2. Nếu thông tin mới mâu thuẫn với ký ức cũ, ưu tiên thông tin mới hơn và ghi chú thời điểm cập nhật.
3. Viết ngắn gọn bằng tiếng Việt tự nhiên, không suy diễn quá mức.
4. Tổng dung lượng nên dưới 1800 từ.

Chỉ trả về JSON hợp lệ, không Markdown, không giải thích thêm. Dùng cấu trúc:
{
  "profile": {
    "name": "",
    "preferred_address": "",
    "language": "Tiếng Việt",
    "location_context": "",
    "preferences": []
  },
  "relationships": [],
  "devices": [],
  "stable_facts": [],
  "interaction_preferences": [],
  "last_updated": "YYYY-MM-DD HH:MM:SS"
}
"""


def extract_json_data(json_code):
    start = json_code.find("```json")
    # từstartbắt đầuđếnmột```kết thúc
    end = json_code.find("```", start + 1)
    # print("start:", start, "end:", end)
    if start == -1 or end == -1:
        try:
            jsonData = json.loads(json_code)
            return json_code
        except Exception as e:
            print("Error:", e)
        return ""
    jsonData = json_code[start + 7 : end]
    return jsonData


TAG = __name__


class MemoryProvider(MemoryProviderBase):
    def __init__(self, config, summary_memory):
        super().__init__(config)
        self.short_memory = ""
        self.save_to_file = True
        self.memory_path = get_project_dir() + "data/.memory.yaml"
        self.load_memory(summary_memory)

    def init_memory(
        self, role_id, llm, summary_memory=None, save_to_file=True, **kwargs
    ):
        super().init_memory(role_id, llm, **kwargs)
        self.save_to_file = save_to_file
        self.load_memory(summary_memory)

    def load_memory(self, summary_memory):
        # apilấyđếnký ứcsautrả về
        if summary_memory or not self.save_to_file:
            self.short_memory = summary_memory
            return

        all_memory = {}
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r", encoding="utf-8") as f:
                all_memory = yaml.safe_load(f) or {}
        if self.role_id in all_memory:
            self.short_memory = all_memory[self.role_id]

    def save_memory_to_file(self):
        all_memory = {}
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r", encoding="utf-8") as f:
                all_memory = yaml.safe_load(f) or {}
        all_memory[self.role_id] = self.short_memory
        with open(self.memory_path, "w", encoding="utf-8") as f:
            yaml.dump(all_memory, f, allow_unicode=True)

    async def save_memory(self, msgs, session_id=None):
        # làm chosử dụngcủmô hìnhthông tin
        model_info = getattr(self.llm, "model_name", str(self.llm.__class__.__name__))
        logger.bind(tag=TAG).debug(f"làm chosử dụngký ứclưumô hình: {model_info}")
        api_key = getattr(self.llm, "api_key", None)
        memory_key_msg = check_model_key("ký ứcsử dụngLLM", api_key)
        if memory_key_msg:
            logger.bind(tag=TAG).error(memory_key_msg)
        if self.llm is None:
            logger.bind(tag=TAG).error("LLM is not set for memory provider")
            return None

        if len(msgs) < 2:
            return None

        msgStr = ""
        for msg in msgs:
            content = msg.content

            # Extract content from JSON format if present (for ASR with emotion/language tags)
            try:
                if content and content.strip().startswith("{") and content.strip().endswith("}"):
                    data = json.loads(content)
                    if "content" in data:
                        content = data["content"]
            except (json.JSONDecodeError, KeyError, TypeError):
                # If parsing fails, use original content
                pass

            if msg.role == "user":
                msgStr += f"User: {content}\n"
            elif msg.role == "assistant":
                msgStr += f"Assistant: {content}\n"
        if self.short_memory and len(self.short_memory) > 0:
            msgStr += "Ký ức hiện có:\n"
            msgStr += self.short_memory

        # Thời gian hiện tại
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        msgStr += f"Thời gian hiện tại: {time_str}"

        if self.save_to_file:
            try:
                result = self.llm.response_no_stream(
                    short_term_memory_prompt,
                    msgStr,
                    max_tokens=2000,
                    temperature=0.2,
                )
                json_str = extract_json_data(result)
                json.loads(json_str)  # kiểm trajsonđịnh dạnglàđúng
                self.short_memory = json_str
                self.save_memory_to_file()
            except Exception as e:
                logger.bind(tag=TAG).error(f"Error in saving memory: {e}")
        else:
            # save_to_filechoFalsekhi/thời，sử dụngJavacủghi lại
            summary_id = session_id if session_id else self.role_id
            await generate_and_save_chat_summary(summary_id)
        logger.bind(tag=TAG).info(
            f"Save memory successful - Role: {self.role_id}, Session: {session_id}"
        )

        return self.short_memory

    async def query_memory(self, query: str) -> str:
        return self.short_memory
