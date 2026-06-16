from config.logger import setup_logging
from http import HTTPStatus
import dashscope
from dashscope import Application
from core.providers.llm.base import LLMProviderBase
from core.utils.util import check_model_key
import time

TAG = __name__
logger = setup_logging()


class LLMProvider(LLMProviderBase):
    def __init__(self, config):
        self.api_key = config["api_key"]
        self.app_id = config["app_id"]
        self.base_url = config.get("base_url")
        self.is_No_prompt = config.get("is_no_prompt")
        self.memory_id = config.get("ali_memory_id")
        self.streaming_chunk_size = config.get("streaming_chunk_size", 3)  # lầnluồngtrả vềký tự
        check_model_key("AliBLLLM", self.api_key)

    def response(self, session_id, dialogue):
        # xử lýdialogue
        if self.is_No_prompt:
            dialogue.pop(0)
            logger.bind(tag=TAG).debug(
                f"【trongAPIdịch vụ】xử lýsaudialogue: {dialogue}"
            )

        # sử dụngtham số
        call_params = {
            "api_key": self.api_key,
            "app_id": self.app_id,
            "session_id": session_id,
            "messages": dialogue,
            # SDKluồng
            "stream": True,
        }
        if self.memory_id != False:
            # memorycầnprompttham số
            prompt = dialogue[-1].get("content")
            call_params["memory_id"] = self.memory_id
            call_params["prompt"] = prompt
            logger.bind(tag=TAG).debug(
                f"【trongAPIdịch vụ】xử lýsauprompt: {prompt}"
            )

        # tùy chọnđặtđịnh nghĩaAPIđịa chỉ（cấu hìnhchochế độURL）
        if self.base_url and ("/api/" in self.base_url):
            dashscope.base_http_api_url = self.base_url

        responses = Application.call(**call_params)

        # luồngxử lý（SDKtạistream=Truethờitrả vềvới；trả vềlầnphản hồivới）
        logger.bind(tag=TAG).debug(
            f"【trongAPIdịch vụ】tham số: {dict(call_params, api_key='***')}"
        )

        last_text = ""
        try:
            for resp in responses:
                if resp.status_code != HTTPStatus.OK:
                    logger.bind(tag=TAG).error(
                        f"code={resp.status_code}, message={resp.message}, ：https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
                    )
                    continue
                current_text = getattr(getattr(resp, "output", None), "text", None)
                if current_text is None:
                    continue
                # SDKluồngcho，tính toánra
                if len(current_text) >= len(last_text):
                    delta = current_text[len(last_text):]
                else:
                    # 
                    delta = current_text
                if delta:
                    yield delta
                last_text = current_text
        except TypeError:
            # luồng（lầntrả về）
            if responses.status_code != HTTPStatus.OK:
                logger.bind(tag=TAG).error(
                    f"code={responses.status_code}, message={responses.message}, ：https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
                )
                yield "【trongAPIdịch vụphản hồingoại lệ】"
            else:
                full_text = getattr(getattr(responses, "output", None), "text", "")
                logger.bind(tag=TAG).info(
                    f"【trongAPIdịch vụ】hoàn chỉnhphản hồi: {len(full_text)}"
                )
                for i in range(0, len(full_text), self.streaming_chunk_size):
                    chunk = full_text[i:i + self.streaming_chunk_size]
                    if chunk:
                        yield chunk

    def response_with_functions(self, session_id, dialogue, functions=None):
        # tronghiện tại function call。cho，nàytrongđếnvăn bảnluồngra。
        # trênsẽ (content, tool_calls) ，nàytrongtrả về (token, None)
        logger.bind(tag=TAG).warning(
            "trong function call，đãchovăn bảnluồngra"
        )
        for token in self.response(session_id, dialogue):
            yield token, None
