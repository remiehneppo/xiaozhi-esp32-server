import base64
import hashlib
import hmac
import json
import time
from datetime import datetime, timezone
import os
from typing import Optional, Tuple, List
from core.providers.asr.dto.dto import InterfaceType
import requests
from core.providers.asr.base import ASRProviderBase
from config.logger import setup_logging

TAG = __name__
logger = setup_logging()


class ASRProvider(ASRProviderBase):
    API_URL = "https://asr.tencentcloudapi.com"
    API_VERSION = "2019-06-14"
    FORMAT = "pcm"  # củâm thanhđịnh dạng：pcm, wav, mp3

    def __init__(self, config: dict, delete_audio_file: bool = True):
        super().__init__()
        self.interface_type = InterfaceType.NON_STREAM
        self.secret_id = config.get("secret_id")
        self.secret_key = config.get("secret_key")
        self.output_dir = config.get("output_dir")
        self.delete_audio_file = delete_audio_file

        # đảm bảorathư mụctại/trong
        os.makedirs(self.output_dir, exist_ok=True)

    async def speech_to_text(
        self, opus_data: List[bytes], session_id: str, audio_format="opus", artifacts=None
    ) -> Tuple[Optional[str], Optional[str]]:
        """sẽgiọng nóidữ liệuchuyển đổichovăn bản"""
        if not opus_data:
            logger.bind(tag=TAG).warning("dữ liệu âm thanhcho！")
            return None, None

        try:
            # kiểm tracấu hìnhlàđãđặt
            if not self.secret_id or not self.secret_key:
                logger.bind(tag=TAG).error("giọng nóinhận dạngcấu hìnhđặt，tiến hànhnhận dạng")
                return None, None

            if artifacts is None:
                return "", None

            # sẽdữ liệu âm thanhchuyển đổichoBase64mã hóa
            base64_audio = base64.b64encode(artifacts.pcm_bytes).decode("utf-8")

            # xây dựngyêu cầu
            request_body = self._build_request_body(base64_audio)

            # lấyxác thực
            timestamp, authorization = self._get_auth_headers(request_body)

            # gửiyêu cầu
            start_time = time.time()
            result = self._send_request(request_body, timestamp, authorization)

            if result:
                logger.bind(tag=TAG).debug(
                    f"giọng nóinhận dạngkhi/thời: {time.time() - start_time:.3f}s | kết quả: {result}"
                )

            return result, artifacts.file_path

        except Exception as e:
            logger.bind(tag=TAG).error(f"xử lýâm thanhkhi/thờisai！{e}", exc_info=True)
            return None, None

    def _build_request_body(self, base64_audio: str) -> str:
        """xây dựngyêu cầu"""
        request_map = {
            "ProjectId": 0,
            "SubServiceType": 2,  # nhận dạng
            "EngSerViceType": "16k_zh",  # trongsử dụng
            "SourceType": 1,  # dữ liệu âm thanhđếnchogiọng nóitệp
            "VoiceFormat": self.FORMAT,  # âm thanhđịnh dạng
            "Data": base64_audio,  # Base64mã hóacủdữ liệu âm thanh
            "DataLen": len(base64_audio),  # dữ liệu
        }
        return json.dumps(request_map)

    def _get_auth_headers(self, request_body: str) -> Tuple[str, str]:
        """lấyxác thực"""
        try:
            # lấyhiện tạiUTCkhi/thời
            now = datetime.now(timezone.utc)
            timestamp = str(int(now.timestamp()))
            date = now.strftime("%Y-%m-%d")

            # dịch vụlà "asr"
            service = "asr"

            # nối
            credential_scope = f"{date}/{service}/tc3_request"

            # sử dụngTC3-HMAC-SHA256chữ kýphương pháp
            algorithm = "TC3-HMAC-SHA256"

            # xây dựngyêu cầuký tự
            http_request_method = "POST"
            canonical_uri = "/"
            canonical_query_string = ""

            # ：thông tincầntheoASCII，vàkeyvàvaluecho
            # content-typevàhost
            content_type = "application/json; charset=utf-8"
            host = "asr.tencentcloudapi.com"
            action = "SentenceRecognition"  # 

            # xây dựngthông tin，vàđịnh dạng
            canonical_headers = (
                f"content-type:{content_type.lower()}\n"
                + f"host:{host.lower()}\n"
                + f"x-tc-action:{action.lower()}\n"
            )

            signed_headers = "content-type;host;x-tc-action"

            # yêu cầubăm
            payload_hash = self._sha256_hex(request_body)

            # xây dựngyêu cầuký tự
            canonical_request = (
                f"{http_request_method}\n"
                + f"{canonical_uri}\n"
                + f"{canonical_query_string}\n"
                + f"{canonical_headers}\n"
                + f"{signed_headers}\n"
                + f"{payload_hash}"
            )

            # tính toányêu cầucủbăm
            hashed_canonical_request = self._sha256_hex(canonical_request)

            # xây dựngchữ kýký tự
            string_to_sign = (
                f"{algorithm}\n"
                + f"{timestamp}\n"
                + f"{credential_scope}\n"
                + f"{hashed_canonical_request}"
            )

            # tính toán chữ ký
            secret_date = self._hmac_sha256(f"TC3{self.secret_key}", date)
            secret_service = self._hmac_sha256(secret_date, service)
            secret_signing = self._hmac_sha256(secret_service, "tc3_request")

            # tính toán chữ ký
            signature = self._bytes_to_hex(
                self._hmac_sha256(secret_signing, string_to_sign)
            )

            # xây dựngủy quyền
            authorization = (
                f"{algorithm} "
                + f"Credential={self.secret_id}/{credential_scope}, "
                + f"SignedHeaders={signed_headers}, "
                + f"Signature={signature}"
            )

            return timestamp, authorization

        except Exception as e:
            logger.bind(tag=TAG).error(f"tạoxác thựcthất bại: {e}", exc_info=True)
            raise RuntimeError(f"tạoxác thựcthất bại: {e}")

    def _send_request(
        self, request_body: str, timestamp: str, authorization: str
    ) -> Optional[str]:
        """gửiyêu cầuđếnAPI"""
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Host": "asr.tencentcloudapi.com",
            "Authorization": authorization,
            "X-TC-Action": "SentenceRecognition",
            "X-TC-Version": self.API_VERSION,
            "X-TC-Timestamp": timestamp,
            "X-TC-Region": "ap-shanghai",
        }

        try:
            response = requests.post(self.API_URL, headers=headers, data=request_body)

            if not response.ok:
                raise IOError(f"yêu cầuthất bại: {response.status_code} {response.reason}")

            response_json = response.json()

            # kiểm tralàcósai
            if "Response" in response_json and "Error" in response_json["Response"]:
                error = response_json["Response"]["Error"]
                error_code = error["Code"]
                error_message = error["Message"]
                raise IOError(f"APItrả vềsai: {error_code}: {error_message}")

            # nhận dạngkết quả
            if "Response" in response_json and "Result" in response_json["Response"]:
                return response_json["Response"]["Result"]
            else:
                logger.bind(tag=TAG).warning(f"phản hồitrongcónhận dạngkết quả: {response_json}")
                return ""

        except Exception as e:
            logger.bind(tag=TAG).error(f"gửiyêu cầuthất bại: {e}", exc_info=True)
            return None

    def _sha256_hex(self, data: str) -> str:
        """tính toánký tựcủSHA256băm"""
        digest = hashlib.sha256(data.encode("utf-8")).digest()
        return self._bytes_to_hex(digest)

    def _hmac_sha256(self, key, data: str) -> bytes:
        """tính toánHMAC-SHA256"""
        if isinstance(key, str):
            key = key.encode("utf-8")

        return hmac.new(key, data.encode("utf-8"), hashlib.sha256).digest()

    def _bytes_to_hex(self, bytes_data: bytes) -> str:
        """ký tự"""
        return "".join(f"{b:02x}" for b in bytes_data)
