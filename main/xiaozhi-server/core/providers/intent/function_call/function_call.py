from ..base import IntentProviderBase
from typing import List, Dict
from config.logger import setup_logging

TAG = __name__
logger = setup_logging()


class IntentProvider(IntentProviderBase):
    async def detect_intent(self, conn, dialogue_history: List[Dict], text: str) -> str:
        """
        mặc địnhý địnhnhận dạng，trả vềtiếp tục
        Args:
            dialogue_history: hội thoạighi lại
            text: lầnhội thoạighi lại
        Returns:
            trả về"tiếp tục"
        """
        logger.bind(tag=TAG).debug(
            "Using functionCallProvider, always returning continue chat"
        )
        return '{"function_call": {"name": "continue_chat"}}'
