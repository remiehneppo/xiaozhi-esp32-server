from config.logger import setup_logging
from openai import OpenAI
import json
from core.providers.llm.base import LLMProviderBase

TAG = __name__
logger = setup_logging()


class LLMProvider(LLMProviderBase):
    def __init__(self, config):
        self.model_name = config.get("model_name")
        self.base_url = config.get("base_url", "http://localhost:11434")
        # Khởi tạo OpenAI client với base URL Ollama
        # nhưkhông cóv1，v1
        if not self.base_url.endswith("/v1"):
            self.base_url = f"{self.base_url}/v1"

        self.client = OpenAI(
            base_url=self.base_url,
            api_key="ollama",  # Ollama doesn't need an API key but OpenAI client requires one
        )

        # Kiểm tra xem có phải model qwen3 không
        self.is_qwen3 = self.model_name and self.model_name.lower().startswith("qwen3")

    def response(self, session_id, dialogue, **kwargs):
        # Nếu là model qwen3, thêm lệnh /no_think vào tin nhắn người dùng cuối cùng
        if self.is_qwen3:
            # Sao chép danh sách hội thoại để tránh sửa dữ liệu gốc
            dialogue_copy = dialogue.copy()

            # Tìm tin nhắn người dùng cuối cùng
            for i in range(len(dialogue_copy) - 1, -1, -1):
                if dialogue_copy[i]["role"] == "user":
                    # Thêm lệnh /no_think trước nội dung người dùng
                    dialogue_copy[i]["content"] = (
                        "/no_think " + dialogue_copy[i]["content"]
                    )
                    logger.bind(tag=TAG).debug("Đã thêm chỉ dẫn /no_think cho model qwen3")
                    break

            # Dùng hội thoại đã chỉnh sửa
            dialogue = dialogue_copy

        responses = self.client.chat.completions.create(
            model=self.model_name, messages=dialogue, stream=True
        )
        is_active = True
        # dùng choxử lýchunk
        buffer = ""

        try:
            for chunk in responses:
                try:
                    delta = (
                        chunk.choices[0].delta
                        if getattr(chunk, "choices", None)
                        else None
                    )
                    content = delta.content if hasattr(delta, "content") else ""

                    if content:
                        # Thêm nội dung vào bộ đệm
                        buffer += content

                        # Xử lý thẻ trong bộ đệm
                        while "<think>" in buffer and "</think>" in buffer:
                            # Tìm thẻ <think></think> đầy đủ và loại bỏ
                            pre = buffer.split("<think>", 1)[0]
                            post = buffer.split("</think>", 1)[1]
                            buffer = pre + post

                        # Xử lý trường hợp chỉ có thẻ mở
                        if "<think>" in buffer:
                            is_active = False
                            buffer = buffer.split("<think>", 1)[0]

                        # Xử lý trường hợp chỉ có thẻ đóng
                        if "</think>" in buffer:
                            is_active = True
                            buffer = buffer.split("</think>", 1)[1]

                        # Nếu đang ở trạng thái hoạt động và bộ đệm có nội dung thì xuất ra
                        if is_active and buffer:
                            yield buffer
                            buffer = ""  # Xóa bộ đệm

                except Exception as e:
                    logger.bind(tag=TAG).error(f"Lỗi khi xử lý chunk: {e}")
        finally:
            responses.close()

    def response_with_functions(self, session_id, dialogue, functions=None):
        # Nếu là model qwen3, thêm lệnh /no_think vào tin nhắn người dùng cuối cùng
        if self.is_qwen3:
            # Sao chép danh sách hội thoại để tránh sửa dữ liệu gốc
            dialogue_copy = dialogue.copy()

            # Tìm tin nhắn người dùng cuối cùng
            for i in range(len(dialogue_copy) - 1, -1, -1):
                if dialogue_copy[i]["role"] == "user":
                    # Thêm lệnh /no_think trước nội dung người dùng
                    dialogue_copy[i]["content"] = (
                        "/no_think " + dialogue_copy[i]["content"]
                    )
                    logger.bind(tag=TAG).debug("Đã thêm chỉ dẫn /no_think cho model qwen3")
                    break

            # Dùng hội thoại đã chỉnh sửa
            dialogue = dialogue_copy

        stream = self.client.chat.completions.create(
            model=self.model_name,
            messages=dialogue,
            stream=True,
            tools=functions,
        )

        is_active = True
        buffer = ""

        try:
            for chunk in stream:
                try:
                    delta = (
                        chunk.choices[0].delta
                        if getattr(chunk, "choices", None)
                        else None
                    )
                    content = delta.content if hasattr(delta, "content") else None
                    tool_calls = (
                        delta.tool_calls if hasattr(delta, "tool_calls") else None
                    )

                    # nhưcông cụsử dụng，
                    if tool_calls:
                        yield None, tool_calls
                        continue

                    # xử lývăn bảnnội dung
                    if content:
                        # sẽnội dungthêmđến
                        buffer += content

                        # xử lýtrong
                        while "<think>" in buffer and "</think>" in buffer:
                            # đếnhoàn chỉnh<think></think>vàloại bỏ
                            pre = buffer.split("<think>", 1)[0]
                            post = buffer.split("</think>", 1)[1]
                            buffer = pre + post

                        # xử lýchỉcóbắt đầu
                        if "<think>" in buffer:
                            is_active = False
                            buffer = buffer.split("<think>", 1)[0]

                        # xử lýchỉcókết thúc
                        if "</think>" in buffer:
                            is_active = True
                            buffer = buffer.split("</think>", 1)[1]

                        # nhưhiện tạitạitrạng tháivàcónội dung，ra
                        if is_active and buffer:
                            yield buffer, None
                            buffer = ""  # 
                except Exception as e:
                    logger.bind(tag=TAG).error(f"Lỗi khi xử lý function chunk: {e}")
                    continue
        finally:
            stream.close()
