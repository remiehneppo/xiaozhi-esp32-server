import time
import os
from typing import Optional, Tuple, List
from aip import AipSpeech
from core.providers.asr.base import ASRProviderBase
from config.logger import setup_logging
from core.providers.asr.dto.dto import InterfaceType

TAG = __name__
logger = setup_logging()


class ASRProvider(ASRProviderBase):
    def __init__(self, config: dict, delete_audio_file: bool = True):
        super().__init__()
        self.interface_type = InterfaceType.NON_STREAM
        self.app_id = config.get("app_id")
        self.api_key = config.get("api_key")
        self.secret_key = config.get("secret_key")

        dev_pid = config.get("dev_pid", "1537")
        self.dev_pid = int(dev_pid) if dev_pid else 1537

        self.output_dir = config.get("output_dir")
        self.delete_audio_file = delete_audio_file

        self.client = AipSpeech(str(self.app_id), self.api_key, self.secret_key)

        # đảm bảorathư mụctại
        os.makedirs(self.output_dir, exist_ok=True)

    async def speech_to_text(
        self, opus_data: List[bytes], session_id: str, audio_format="opus", artifacts=None
    ) -> Tuple[Optional[str], Optional[str]]:
        """sẽgiọng nóidữ liệuchuyển đổichovăn bản"""
        if not opus_data:
            logger.bind(tag=TAG).warning("dữ liệu âm thanhcho！")
            return None, None

        try:
            # kiểm tracấu hìnhcóđãđặt
            if not self.app_id or not self.api_key or not self.secret_key:
                logger.bind(tag=TAG).error("giọng nóinhận dạngcấu hìnhđặt，tiến hànhnhận dạng")
                return None, None

            if artifacts is None:
                return "", None

            start_time = time.time()
            # nhận dạngcục bộtệp
            result = self.client.asr(
                artifacts.pcm_bytes,
                "pcm",
                16000,
                {
                    "dev_pid": str(self.dev_pid),
                },
            )

            if result and result["err_no"] == 0:
                logger.bind(tag=TAG).debug(
                    f"giọng nóinhận dạngthời: {time.time() - start_time:.3f}s | kết quả: {result}"
                )
                result = result["result"][0]
                return result, artifacts.file_path
            else:
                raise Exception(
                    f"giọng nóinhận dạngthất bại，lỗi: {result['err_no']}，lỗithông tin: {result['err_msg']}"
                )
                return None, artifacts.file_path

        except Exception as e:
            logger.bind(tag=TAG).error(f"xử lýâm thanhthờilỗi！{e}", exc_info=True)
            return None, None
