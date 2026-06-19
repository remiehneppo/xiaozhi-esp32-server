import time
import os
from config.logger import setup_logging
from typing import Optional, Tuple, List
from core.providers.asr.dto.dto import InterfaceType
from core.providers.asr.base import ASRProviderBase

import requests

TAG = __name__
logger = setup_logging()

class ASRProvider(ASRProviderBase):
    def __init__(self, config: dict, delete_audio_file: bool):
        self.interface_type = InterfaceType.NON_STREAM
        self.api_key = config.get("api_key")
        self.api_url = config.get("base_url")
        self.output_dir = config.get("output_dir")
        self.delete_audio_file = delete_audio_file

        # Hỗ trợ nhiều model phân tách bởi dấu ";" hoặc qua khóa fallback_model_name
        model_name = config.get("model_name", "")
        self.models = [m.strip() for m in model_name.split(";") if m.strip()]
        fallback = config.get("fallback_model_name")
        if fallback and fallback not in self.models:
            self.models.append(fallback.strip())

        if not self.models:
            self.models = ["whisper-1"]

        os.makedirs(self.output_dir, exist_ok=True)

    def requires_file(self) -> bool:
        return True

    async def speech_to_text(self, opus_data: List[bytes], session_id: str, audio_format="opus", artifacts=None) -> Tuple[Optional[str], Optional[str]]:
        file_path = None
        if artifacts is None:
            return "", None
        file_path = artifacts.file_path
            
        logger.bind(tag=TAG).info(f"file path: {file_path}")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        last_error = None
        for model in self.models:
            try:
                data = {
                    "model": model
                }

                with open(file_path, "rb") as audio_file:
                    files = {
                        "file": audio_file
                    }

                    start_time = time.time()
                    response = requests.post(
                        self.api_url,
                        files=files,
                        data=data,
                        headers=headers,
                        timeout=15
                    )
                    logger.bind(tag=TAG).debug(
                        f"Nhận dạng giọng nói (model={model}) thời gian: {time.time() - start_time:.3f}s | kết quả: {response.text}"
                    )

                if response.status_code == 200:
                    text = response.json().get("text", "")
                    return text, file_path
                else:
                    logger.bind(tag=TAG).warning(
                        f"Yêu cầu ASR với model {model} thất bại: {response.status_code} - {response.text}"
                    )
                    last_error = f"API request failed with status {response.status_code}"
            except Exception as e:
                logger.bind(tag=TAG).error(f"Lỗi nhận dạng giọng nói với model {model}: {e}")
                last_error = str(e)
                
        logger.bind(tag=TAG).error(f"Tất cả các model ASR đều thất bại. Lỗi cuối: {last_error}")
        return "", None
        
