import requests
from requests.exceptions import RequestException
from config.logger import setup_logging
from core.providers.llm.base import LLMProviderBase

TAG = __name__
logger = setup_logging()


class LLMProvider(LLMProviderBase):
    def __init__(self, config):
        self.agent_id = config.get("agent_id")  # tương ứng agent_id
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", config.get("url"))  # mặc địnhlàm chosử dụng base_url
        self.api_url = f"{self.base_url}/api/conversation/process"  # nốihoàn chỉnh API URL

    def response(self, session_id, dialogue, **kwargs):
        # home assistantgiọng nóiý định，làm chosử dụngxiaozhi ai，chỉcầnsử dụngnóichohome assistant

        # saumột role cho 'user'  content
        input_text = None
        if isinstance(dialogue, list):  # đảm bảo dialogue một
            # duyệt，đếnsaumột role cho 'user' tin nhắn
            for message in reversed(dialogue):
                if message.get("role") == "user":  # đến role cho 'user' tin nhắn
                    input_text = message.get("content", "")
                    break  # đếnsauthoát

        # yêu cầudữ liệu
        payload = {
            "text": input_text,
            "agent_id": self.agent_id,
            "conversation_id": session_id,  # làm chosử dụng session_id cho conversation_id
        }
        # đặtyêu cầu
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        #  POST yêu cầu
        with requests.post(self.api_url, json=payload, headers=headers) as response:
            # kiểm trayêu cầucóthành công
            response.raise_for_status()

            # phân tíchtrả vềdữ liệu
            data = response.json()
        speech = (
            data.get("response", {})
            .get("speech", {})
            .get("plain", {})
            .get("speech", "")
        )

        # trả vềtạonội dung
        if speech:
            yield speech
        else:
            logger.bind(tag=TAG).warning("API trả vềdữ liệutrongkhông có speech nội dung")

    def response_with_functions(self, session_id, dialogue, functions=None):
        logger.bind(tag=TAG).error(
            f"homeassistantkhông（function call），làm chosử dụngnóý địnhnhận dạng"
        )
