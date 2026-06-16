import json
import hmac
import base64
import hashlib
import asyncio
import websockets
import opuslib_next
import gc
from time import mktime
from datetime import datetime
from urllib.parse import urlencode
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler
from config.logger import setup_logging
from wsgiref.handlers import format_date_time
from core.providers.asr.base import ASRProviderBase
from core.providers.asr.dto.dto import InterfaceType

TAG = __name__
logger = setup_logging()

# Trạng thái frame constant
STATUS_FIRST_FRAME = 0  # Nhãn frame đầu tiên
STATUS_CONTINUE_FRAME = 1  # Nhãn frame giữa
STATUS_LAST_FRAME = 2  # Nhãn frame cuối cùng


class ASRProvider(ASRProviderBase):
    def __init__(self, config, delete_audio_file):
        super().__init__()
        self.interface_type = InterfaceType.STREAM
        self.config = config
        self.text = ""
        self.decoder = opuslib_next.Decoder(16000, 1)
        self.asr_ws = None
        self.forward_task = None
        self.is_processing = False
        self.server_ready = False

        # Cấu hình
        self.app_id = config.get("app_id")
        self.api_key = config.get("api_key")
        self.api_secret = config.get("api_secret")

        if not all([self.app_id, self.api_key, self.api_secret]):
            raise ValueError("Cần cung cấp app_id, api_key và api_secret")

        # Tham số recognition
        self.iat_params = {
            "domain": config.get("domain", "slm"),
            "language": config.get("language", "zh_cn"),
            "accent": config.get("accent", "mandarin"),
            "result": {"encoding": "utf8", "compress": "raw", "format": "plain"},
        }

        self.output_dir = config.get("output_dir", "tmp/")
        self.delete_audio_file = delete_audio_file

    def create_url(self) -> str:
        """Sinhxác thựcURL"""
        url = "ws://iat.cn-huabei-1.xf-yun.com/v1"
        # Sinh timestamp định dạng RFC1123
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # Nối chuỗi
        signature_origin = "host: " + "iat.cn-huabei-1.xf-yun.com" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v1 " + "HTTP/1.1"

        # Thực hiện hmac-sha256 để encrypt
        signature_sha = hmac.new(
            self.api_secret.encode("utf-8"),
            signature_origin.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding="utf-8")

        authorization_origin = (
            'api_key="%s", algorithm="%s", headers="%s", signature="%s"'
            % (self.api_key, "hmac-sha256", "host date request-line", signature_sha)
        )
        authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode(
            encoding="utf-8"
        )

        # Kết hợp số xác thực request thành dict
        v = {
            "authorization": authorization,
            "date": date,
            "host": "iat.cn-huabei-1.xf-yun.com",
        }

        # Nối số xác thực, sinh url
        url = url + "?" + urlencode(v)
        return url

    async def open_audio_channels(self, conn: "ConnectionHandler"):
        await super().open_audio_channels(conn)

    async def receive_audio(self, conn: "ConnectionHandler", audio, audio_have_voice):
        # Gọi trước method parent class xử lý logic cơ bản
        await super().receive_audio(conn, audio, audio_have_voice)

        # Nếu lần này có, và trước đó chưakết nối
        if audio_have_voice and self.asr_ws is None and not self.is_processing:
            try:
                await self._start_recognition(conn)
            except Exception as e:
                logger.bind(tag=TAG).error(f"ASRkết nốithất bại: {str(e)}")
                await self._cleanup()
                return

        # gửihiện tạidữ liệu âm thanh
        if self.asr_ws and self.is_processing and self.server_ready:
            try:
                pcm_frame = self.decoder.decode(audio, 960)
                await self._send_audio_frame(pcm_frame, STATUS_CONTINUE_FRAME)
            except Exception as e:
                logger.bind(tag=TAG).warning(f"gửidữ liệu âm thanhkhi/thờisai: {e}")
                await self._cleanup()

    async def _start_recognition(self, conn: "ConnectionHandler"):
        """bắt đầunhận dạngphiên"""
        try:
            self.is_processing = True
            # WebSocketkết nối
            ws_url = self.create_url()
            logger.bind(tag=TAG).info(f"tại/trongkết nốiASRdịch vụ: {ws_url[:50]}...")

            # nhưchochế độ,đặtquá thời giankhi/thờicho
            if conn.client_listen_mode == "manual":
                self.iat_params["eos"] = 60000

            self.asr_ws = await websockets.connect(
                ws_url,
                max_size=1000000000,
                ping_interval=None,
                ping_timeout=None,
                close_timeout=10,
            )

            logger.bind(tag=TAG).info("ASR WebSocketkết nốiđã")
            self.server_ready = False
            self.forward_task = asyncio.create_task(self._forward_results(conn))

            # gửikhungâm thanh
            if conn.asr_audio and len(conn.asr_audio) > 0:
                first_audio = conn.asr_audio[-1] if conn.asr_audio else b""
                pcm_frame = (
                    self.decoder.decode(first_audio, 960) if first_audio else b""
                )
                await self._send_audio_frame(pcm_frame, STATUS_FIRST_FRAME)
                self.server_ready = True
                logger.bind(tag=TAG).info("đãgửikhung，bắt đầunhận dạng")

                # gửibộ nhớ đệmcủdữ liệu âm thanh
                for cached_audio in conn.asr_audio[-10:]:
                    try:
                        pcm_frame = self.decoder.decode(cached_audio, 960)
                        await self._send_audio_frame(pcm_frame, STATUS_CONTINUE_FRAME)
                    except Exception as e:
                        logger.bind(tag=TAG).info(f"gửibộ nhớ đệmdữ liệu âm thanhkhi/thờisai: {e}")
                        break

        except Exception as e:
            logger.bind(tag=TAG).error(f"ASRkết nốithất bại: {str(e)}")
            if hasattr(e, "__cause__") and e.__cause__:
                logger.bind(tag=TAG).error(f"saido: {str(e.__cause__)}")
            if self.asr_ws:
                await self.asr_ws.close()
                self.asr_ws = None
            self.is_processing = False
            raise

    async def _send_audio_frame(self, audio_data: bytes, status: int):
        """gửiâm thanhkhung"""
        if not self.asr_ws:
            return

        audio_b64 = base64.b64encode(audio_data).decode("utf-8")

        frame_data = {
            "header": {"status": status, "app_id": self.app_id},
            "parameter": {"iat": self.iat_params},
            "payload": {
                "audio": {"audio": audio_b64, "sample_rate": 16000, "encoding": "raw"}
            },
        }

        await self.asr_ws.send(json.dumps(frame_data, ensure_ascii=False))

    async def _forward_results(self, conn: "ConnectionHandler"):
        """nhận dạngkết quả"""
        try:
            while not conn.stop_event.is_set():
                try:
                    response = await asyncio.wait_for(self.asr_ws.recv(), timeout=60)
                    result = json.loads(response)
                    logger.bind(tag=TAG).debug(f"đếnASRkết quả: {result}")

                    header = result.get("header", {})
                    payload = result.get("payload", {})
                    code = header.get("code", 0)
                    status = header.get("status", 0)

                    if code != 0:
                        logger.bind(tag=TAG).error(
                            f"nhận dạngsai，sai: {code}, tin nhắn: {header.get('message', '')}"
                        )
                        if code in [10114, 10160]:  # kết nối
                            break
                        continue

                    # Xử lý kết quả recognition
                    if payload and "result" in payload:
                        text_data = payload["result"]["text"]
                        if text_data:
                            # giải mãbase64văn bản
                            decoded_text = base64.b64decode(text_data).decode("utf-8")
                            text_json = json.loads(decoded_text)
                            # văn bảnbên trong
                            text_ws = text_json.get("ws", [])
                            for i in text_ws:
                                for j in i.get("cw", []):
                                    w = j.get("w", "")
                                    self.text += w

                    if status == 2:
                        logger.bind(tag=TAG).debug("đếnnhận dạngkết quả，xử lý")
                        await self.handle_voice_stop(conn, conn.asr_audio)
                        break

                except asyncio.TimeoutError:
                    logger.bind(tag=TAG).error("nhậnkết quảquá thời gian")
                    break
                except websockets.ConnectionClosed:
                    logger.bind(tag=TAG).info("ASRdịch vụkết nốiđãđóng")
                    self.is_processing = False
                    break
                except Exception as e:
                    logger.bind(tag=TAG).error(f"xử lýASRkết quảkhi/thờisai: {str(e)}")
                    if hasattr(e, "__cause__") and e.__cause__:
                        logger.bind(tag=TAG).error(f"saido: {str(e.__cause__)}")
                    self.is_processing = False
                    break

        except Exception as e:
            logger.bind(tag=TAG).error(f"ASRkết quảnhiệm vụsai: {str(e)}")
            if hasattr(e, "__cause__") and e.__cause__:
                logger.bind(tag=TAG).error(f"saido: {str(e.__cause__)}")
        finally:
            # dọn dẹpkết nốitài nguyên
            await self._cleanup()
            conn.reset_audio_states()

    async def handle_voice_stop(
        self, conn: "ConnectionHandler", asr_audio_task: List[bytes]
    ):
        """xử lýgiọng nóidừng，gửisaukhungvàxử lýnhận dạngkết quả"""
        try:
            # gửisaukhungâm thanhkết thúc
            if self.asr_ws and self.is_processing:
                try:
                    await self._send_audio_frame(b"", STATUS_LAST_FRAME)
                    logger.bind(tag=TAG).debug(f"đãgửidừngyêu cầu")

                    await asyncio.sleep(0.25)
                except Exception as e:
                    logger.bind(tag=TAG).error(f"gửidừngyêu cầuthất bại: {e}")

            await super().handle_voice_stop(conn, asr_audio_task)
        except Exception as e:
            logger.bind(tag=TAG).error(f"xử lýgiọng nóidừngthất bại: {e}")
            import traceback

            logger.bind(tag=TAG).debug(f"ngoại lệ: {traceback.format_exc()}")

    def stop_ws_connection(self):
        if self.asr_ws:
            asyncio.create_task(self.asr_ws.close())
            self.asr_ws = None
        self.is_processing = False

    async def _send_stop_request(self):
        """gửidừngnhận dạngyêu cầu（khôngđóngkết nối）"""
        if self.asr_ws:
            try:
                # dừngâm thanhgửi
                self.is_processing = False
                await self._send_audio_frame(b"", STATUS_LAST_FRAME)
                logger.bind(tag=TAG).debug("đãgửidừngyêu cầu")
            except Exception as e:
                logger.bind(tag=TAG).error(f"gửidừngyêu cầuthất bại: {e}")

    async def _cleanup(self):
        """dọn dẹptài nguyên（đóngkết nối）"""
        logger.bind(tag=TAG).debug(
            f"bắt đầuASRphiêndọn dẹp | hiện tạitrạng thái: processing={self.is_processing}, server_ready={self.server_ready}"
        )

        # trạng tháiđặt lại
        self.is_processing = False
        self.server_ready = False
        logger.bind(tag=TAG).debug("ASRtrạng tháiđãđặt lại")

        # đóngkết nối
        if self.asr_ws:
            try:
                logger.bind(tag=TAG).debug("tại/trongđóngWebSocketkết nối")
                await asyncio.wait_for(self.asr_ws.close(), timeout=2.0)
                logger.bind(tag=TAG).debug("WebSocketkết nốiđãđóng")
            except Exception as e:
                logger.bind(tag=TAG).error(f"đóngWebSocketkết nốithất bại: {e}")
            finally:
                self.asr_ws = None

        # dọn dẹpnhiệm vụsử dụng
        self.forward_task = None

        logger.bind(tag=TAG).debug("ASRphiêndọn dẹphoàn thành")

    async def speech_to_text(self, opus_data, session_id, audio_format, artifacts=None):
        """lấynhận dạngkết quả"""
        result = self.text
        self.text = ""
        return result, None

    async def close(self):
        """tài nguyêndọn dẹpphương pháp"""
        if self.asr_ws:
            await self.asr_ws.close()
            self.asr_ws = None
        if self.forward_task:
            self.forward_task.cancel()
            try:
                await self.forward_task
            except asyncio.CancelledError:
                pass
            self.forward_task = None
        self.is_processing = False

        # giải phóngdecodertài nguyên
        if hasattr(self, "decoder") and self.decoder is not None:
            try:
                del self.decoder
                self.decoder = None
                logger.bind(tag=TAG).debug("Xunfei decoder resources released")
            except Exception as e:
                logger.bind(tag=TAG).debug(f"giải phóngXunfei decodertài nguyênkhi/thờira: {e}")

