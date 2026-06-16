from abc import ABC, abstractmethod
from typing import List, Dict
from config.logger import setup_logging

TAG = __name__
logger = setup_logging()


class IntentProviderBase(ABC):
    def __init__(self, config):
        self.config = config

    def set_llm(self, llm):
        self.llm = llm
        # lấymô hìnhvàthông tin
        model_name = getattr(llm, "model_name", str(llm.__class__.__name__))
        # ghi lạihơnnhật ký
        logger.bind(tag=TAG).info(f"ý địnhnhận dạngđặtLLM: {model_name}")

    @abstractmethod
    async def detect_intent(self, conn, dialogue_history: List[Dict], text: str) -> str:
        """
        sử dụngsauý định
        Args:
            dialogue_history: hội thoạighi lại，ghi lạirolevàcontent
        Returns:
            trả vềnhận dạngraý định，định dạngcho:
            - "tiếp tục"
            - "kết thúc"
            - " " hoặc ""
            - " " hoặc " [hiện tạivị trí]"
        """
        pass
