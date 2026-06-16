import os
import json
import time
from typing import Optional, Tuple, List
from .base import ASRProviderBase
from config.logger import setup_logging
from core.providers.asr.dto.dto import InterfaceType
import vosk

TAG = __name__
logger = setup_logging()

class ASRProvider(ASRProviderBase):
    def __init__(self, config: dict, delete_audio_file: bool = True):
        super().__init__()
        self.interface_type = InterfaceType.LOCAL
        self.model_path = config.get("model_path")
        self.output_dir = config.get("output_dir", "tmp/")
        self.delete_audio_file = delete_audio_file
        
        # khởi tạoVOSKmô hình
        self.model = None
        self.recognizer = None
        self._load_model()
        
        # đảm bảorathư mụctại
        os.makedirs(self.output_dir, exist_ok=True)

    def _load_model(self):
        """tảiVOSKmô hình"""
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"VOSKmô hìnhđường dẫnkhông tồn tại: {self.model_path}")
                
            logger.bind(tag=TAG).info(f"tạitảiVOSKmô hình: {self.model_path}")
            self.model = vosk.Model(self.model_path)

            # khởi tạoVOSKnhận dạng（tần số lấy mẫucho16kHz）
            self.recognizer = vosk.KaldiRecognizer(self.model, 16000)

            logger.bind(tag=TAG).info("VOSKmô hìnhtảithành công")
        except Exception as e:
            logger.bind(tag=TAG).error(f"tảiVOSKmô hìnhthất bại: {e}")
            raise

    async def speech_to_text(
        self, opus_data: List[bytes], session_id: str, audio_format="opus", artifacts=None
    ) -> Tuple[Optional[str], Optional[str]]:
        """sẽgiọng nóidữ liệuchuyển đổichovăn bản"""
        try:
            # kiểm tramô hìnhcótảithành công
            if not self.model:
                logger.bind(tag=TAG).error("VOSKmô hìnhtải，tiến hànhnhận dạng")
                return "", None
            
            if artifacts is None:
                return "", None
            if not artifacts.pcm_bytes:
                logger.bind(tag=TAG).warning("vàsauPCMdữ liệucho")
                return "", None

            start_time = time.time()
            
            
            # tiến hànhnhận dạng（VOSKlầnvào2000dữ liệu）
            chunk_size = 2000
            text_result = ""
            
            for i in range(0, len(artifacts.pcm_bytes), chunk_size):
                chunk = artifacts.pcm_bytes[i:i+chunk_size]
                if self.recognizer.AcceptWaveform(chunk):
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '')
                    if text:
                        text_result += text + " "
            
            # lấykết quả
            final_result = json.loads(self.recognizer.FinalResult())
            final_text = final_result.get('text', '')
            if final_text:
                text_result += final_text
            
            logger.bind(tag=TAG).debug(
                f"VOSKgiọng nóinhận dạngthời: {time.time() - start_time:.3f}s | kết quả: {text_result.strip()}"
            )
            
            return text_result.strip(), artifacts.file_path
            
        except Exception as e:
            logger.bind(tag=TAG).error(f"VOSKgiọng nóinhận dạngthất bại: {e}")
            return "", None
