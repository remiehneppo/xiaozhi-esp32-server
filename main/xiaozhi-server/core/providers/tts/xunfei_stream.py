import os
import time
import uuid
import json
import hmac
import queue
import base64
import hashlib
import asyncio
import traceback
import websockets

from asyncio import Task
from typing import Callable, Any
from config.logger import setup_logging
from core.utils.tts import MarkdownCleaner
from urllib.parse import urlencode, urlparse
from core.providers.tts.base import TTSProviderBase
from core.providers.tts.dto.dto import SentenceType, ContentType, InterfaceType

TAG = __name__
logger = setup_logging()


class XunfeiWSAuth:
    @staticmethod
    def create_auth_url(api_key, api_secret, api_url):
        """SinhWebSocketxác thựcURL"""
        parsed_url = urlparse(api_url)
        host = parsed_url.netloc
        path = parsed_url.path

        # Lấy UTC time, yêu cầu dùng RFC1123 format
        now = time.gmtime()
        date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', now)

        # Xây dựng signed string
        signature_origin = f"host: {host}\ndate: {date}\nGET {path} HTTP/1.1"

        # Tính signature
        signature_sha = hmac.new(
            api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        # Xây dựng authorization
        authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # Xây dựng final WebSocket URL
        v = {
            "authorization": authorization,
            "date": date,
            "host": host
        }
        url = api_url + '?' + urlencode(v)
        return url


class TTSProvider(TTSProviderBase):
    TTS_PARAM_CONFIG = [
        ("ttsVolume", "volume", 0, 100, 50, int),
        ("ttsRate", "speed", 0, 100, 50, int),
        ("ttsPitch", "pitch", 0, 100, 50, int),
    ]

    def __init__(self, config, delete_audio_file):
        super().__init__(config, delete_audio_file)

        # Đặt thành stream interface type
        self.interface_type = InterfaceType.DUAL_STREAM

        # Cấu hình cơ bản
        self.app_id = config.get("app_id")
        self.api_key = config.get("api_key")
        self.api_secret = config.get("api_secret")
        self.report_on_last = True

        # Địa chỉ interface
        self.api_url = config.get("api_url", "wss://cbm01.cn-huabei-1.xf-yun.com/v1/private/mcd9m97e6")

        # Cấu hình voice
        self.voice = config.get("voice", "x5_lingxiaoxuan_flow")
        if config.get("private_voice"):
            self.voice = config.get("private_voice")

        # Cấu hình tham số âm thanh
        speed = config.get("speed", "50")
        self.speed = int(speed) if speed else 50

        volume = config.get("volume", "50")
        self.volume = int(volume) if volume else 50

        pitch = config.get("pitch", "50")
        self.pitch = int(pitch) if pitch else 50

        # Áp dụng điều chỉnh phần trăm (nếu có), nếu không thì dùng cấu hình chung
        self._apply_percentage_params(config)

        # cấu hình mã hóa âm thanh
        self.format = config.get("format", "raw")

        # cấu hình nói chuyện tự nhiên
        self.oral_level = config.get("oral_level", "mid")

        spark_assist = config.get("spark_assist", "1")
        self.spark_assist = int(spark_assist) if spark_assist else 1

        stop_split = config.get("stop_split", "0")
        self.stop_split = int(stop_split) if stop_split else 0
    
        remain = config.get("remain", "0")
        self.remain = int(remain) if remain else 0

        # Cấu hình WebSocket
        self.ws = None
        self._monitor_task = None
        self.activate_session = False

        # quản lý số thứ tự
        self.text_seq = 0

        # xác thực tham số bắt buộc
        if not all([self.app_id, self.api_key, self.api_secret]):
            raise ValueError("TTScầncấu hìnhapp_id、api_keyvàapi_secret")

    async def _ensure_connection(self):
        """đảm bảoWebSocketkết nốikhả dụng"""
        try:
            logger.bind(tag=TAG).debug("Bắt đầu tạo connection mới...")

            # tạo URL xác thực
            auth_url = XunfeiWSAuth.create_auth_url(
                self.api_key, self.api_secret, self.api_url
            )

            self.ws = await websockets.connect(
                auth_url,
                ping_interval=30,
                ping_timeout=10,
                close_timeout=10,
            )
            logger.bind(tag=TAG).debug("WebSocket connection tạo thành công")
            return self.ws
        except Exception as e:
            logger.bind(tag=TAG).error(f"Tạo connection thất bại: {str(e)}")
            self.ws = None
            raise

    def tts_text_priority_thread(self):
        """luồngvăn bảnxử lýluồng"""
        while not self.conn.stop_event.is_set():
            try:
                message = self.tts_text_queue.get(timeout=1)

                if self.conn.client_abort:
                    logger.bind(tag=TAG).info("Nhận thông tin interrupt, chấm dứt thread xử lý text TTS")
                    continue

                # Lọc message cũ: kiểm tra sentence_id có match không
                if message.sentence_id != self.conn.sentence_id:
                    continue

                logger.bind(tag=TAG).debug(
                    f"Nhận task TTS｜{message.sentence_type.name} ｜ {message.content_type.name} | Session ID: {message.sentence_id}"
                )

                if message.sentence_type == SentenceType.FIRST:
                    # Đặt lại trạng thái stream processing
                    self.reset_stream_state()
                    # đặt lại số thứ tự
                    self.text_seq = 0
                # tăng số thứ tự
                self.text_seq += 1

                if message.sentence_type == SentenceType.FIRST:
                    # khởi tạo tham số
                    try:
                        if not getattr(self.conn, "sentence_id", None):
                            self.conn.sentence_id = uuid.uuid4().hex
                            logger.bind(tag=TAG).debug(f"tạocủ phiênID: {self.conn.sentence_id}")

                        logger.bind(tag=TAG).debug("bắt đầukhởi độngTTSphiên...")
                        future = asyncio.run_coroutine_threadsafe(
                            self.start_session(self.conn.sentence_id),
                            loop=self.conn.loop,
                        )
                        future.result(timeout=self.tts_timeout)
                        self.before_stop_play_files.clear()
                        logger.bind(tag=TAG).debug("TTSphiênkhởi độngthành công")

                    except Exception as e:
                        logger.bind(tag=TAG).error(f"khởi độngTTSphiênthất bại: {str(e)}")
                        continue

                # xử lý nội dung văn bản
                if ContentType.TEXT == message.content_type:
                    if message.content_detail:
                        try:
                            logger.bind(tag=TAG).debug(
                                f"bắt đầugửiTTSvăn bản: {message.content_detail}"
                            )
                            future = asyncio.run_coroutine_threadsafe(
                                self.text_to_speak(message.content_detail, None),
                                loop=self.conn.loop,
                            )
                            future.result(timeout=self.tts_timeout)
                        except Exception as e:
                            logger.bind(tag=TAG).error(f"gửiTTSvăn bảnthất bại: {str(e)}")
                            # khônglàm chosử dụngcontinue，đảm bảosauxử lýkhôngbịtrong

                # xử lýtệpbên trong
                if ContentType.FILE == message.content_type:
                    logger.bind(tag=TAG).info(
                        f"thêmâm thanhtệpđến: {message.content_file}"
                    )
                    if message.content_file and os.path.exists(message.content_file):
                        # xử lý dữ liệu âm thanh tệp trước
                        self._process_audio_file_stream(message.content_file, callback=lambda audio_data: self.handle_audio_file(audio_data, message.content_detail))

                # xử lýphiênkết thúc
                if message.sentence_type == SentenceType.LAST:
                    try:
                        logger.bind(tag=TAG).debug("bắt đầukết thúcTTSphiên...")
                        asyncio.run_coroutine_threadsafe(
                            self.finish_session(self.conn.sentence_id),
                            loop=self.conn.loop,
                        )
                    except Exception as e:
                        logger.bind(tag=TAG).error(f"kết thúcTTSphiênthất bại: {str(e)}")
                        continue

            except queue.Empty:
                continue
            except Exception as e:
                logger.bind(tag=TAG).error(
                    f"xử lýTTSvăn bảnthất bại: {str(e)}, : {type(e).__name__}, stack: {traceback.format_exc()}"
                )

    async def text_to_speak(self, text, _):
        """gửivăn bảnđếnTTSdịch vụtiến hành"""
        try:
            if self.ws is None:
                logger.bind(tag=TAG).warning(f"WebSocketkết nốikhôngtại/trong，dừnggửivăn bản")
                return

            filtered_text = MarkdownCleaner.clean_markdown(text)

            if filtered_text:
                # sử dụng cửa sổ trượt để khớp xử lý từ thay thế qua các phân đoạn
                confirmed_texts, self._pending_prefix = self._match_stream_text(filtered_text)

                # gửi mỗi đoạn văn bản đã xác định
                for txt in confirmed_texts:
                    if txt and self.ws:
                        # Gửi request synthesis text
                        run_request = self._build_base_request(status=1, text=txt)
                        await self.ws.send(json.dumps(run_request))
            return

        except Exception as e:
            logger.bind(tag=TAG).error(f"gửiTTSvăn bảnthất bại: {str(e)}")
            if self.ws:
                try:
                    await self.ws.close()
                except:
                    pass
                self.ws = None
            raise

    async def start_session(self, session_id):
        logger.bind(tag=TAG).debug(f"bắt đầuphiên～～{session_id}")
        try:
            # đóng kết nối cũ và tạo kết nối mới khi phiên trước đang ở trạng thái hoạt động
            if self.activate_session:
                await self.close()

            # đặt cờ kích hoạt phiên
            self.activate_session = True

            # kết nối
            await self._ensure_connection()

            # bắt đầu nhiệm vụ nghe
            if self._monitor_task is None or self._monitor_task.done():
                logger.bind(tag=TAG).debug("Khởi động listen task...")
                self._monitor_task = asyncio.create_task(self._start_monitor_tts_response())

            # gửi yêu cầu khởi động phiên
            start_request = self._build_base_request(status=0)

            await self.ws.send(json.dumps(start_request))
            logger.bind(tag=TAG).debug("phiênkhởi độngyêu cầuđãgửi")
        except Exception as e:
            logger.bind(tag=TAG).error(f"khởi độngphiênthất bại: {str(e)}")
            # đảm bảodọn dẹptài nguyên
            await self.close()
            raise

    async def finish_session(self, session_id):
        logger.bind(tag=TAG).debug(f"đóngphiên～～{session_id}")
        try:
            if self.ws:
                # gửiphiênkết thúcyêu cầu
                stop_request = self._build_base_request(status=2)
                await self.ws.send(json.dumps(stop_request))
                logger.bind(tag=TAG).debug("phiênkết thúcyêu cầuđãgửi")

                if self._monitor_task:
                    try:
                        await self._monitor_task
                    except Exception as e:
                        logger.bind(tag=TAG).error(f"chờnhiệm vụhoàn thànhkhi/thờisai: {str(e)}")
                    finally:
                        self._monitor_task = None
        except Exception as e:
            logger.bind(tag=TAG).error(f"đóngphiênthất bại: {str(e)}")
            await self.close()
            raise

    async def close(self):
        """tài nguyêndọn dẹp"""
        await super().close()
        self.activate_session = False
        if self._monitor_task:
            try:
                self._monitor_task.cancel()
                await self._monitor_task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logger.bind(tag=TAG).warning(f"đóngkhi/thờihủynhiệm vụsai: {e}")
            self._monitor_task = None

        if self.ws:
            try:
                await self.ws.close()
            except:
                pass
            self.ws = None

    async def _start_monitor_tts_response(self):
        """TTSphản hồi"""
        try:
            while not self.conn.stop_event.is_set():
                try:
                    msg = await self.ws.recv()

                    # kiểm tramáy kháchlàtrong
                    if self.conn.client_abort:
                        logger.bind(tag=TAG).info("đếnngắtthông tin，dừngTTSphản hồi")
                        break

                    try:
                        data = json.loads(msg)
                        header = data.get("header", {})
                        code = header.get("code")

                        if code == 0:
                            payload = data.get("payload", {})
                            audio_payload = payload.get("audio", {})

                            if audio_payload:
                                status = audio_payload.get("status", 0)
                                audio_data = audio_payload.get("audio", "")
                                if status == 0:
                                    logger.bind(tag=TAG).debug("TTSđãkhởi động")
                                    self.tts_audio_queue.put(
                                        (SentenceType.FIRST, [], None)
                                    )
                                elif status == 2:
                                    logger.bind(tag=TAG).debug("đếnkết thúctrạng tháicủdữ liệu âm thanh，TTShoàn thành")
                                    self.activate_session = False
                                    self._process_before_stop_play_files()
                                    break
                                else:
                                    tts_text = self.get_tts_text(self.conn.sentence_id)
                                    if tts_text:
                                        logger.bind(tag=TAG).info(
                                            f"câugiọng nóitạothành công： {tts_text}"
                                        )
                                        self.tts_audio_queue.put(
                                            (SentenceType.FIRST, [], tts_text)
                                        )
                                        self.clear_tts_text(self.conn.sentence_id)
                                    try:
                                        audio_bytes = base64.b64decode(audio_data)
                                        self.opus_encoder.encode_pcm_to_opus_stream(
                                            audio_bytes, False, self.handle_opus
                                        )

                                    except Exception as e:
                                        logger.bind(tag=TAG).error(f"xử lýdữ liệu âm thanhthất bại: {e}")

                        else:
                            message = header.get("message", "lỗi không xác định")
                            logger.bind(tag=TAG).error(f"TTSsai: {code} - {message}")
                            break

                    except json.JSONDecodeError:
                        logger.bind(tag=TAG).warning("đếnkhông hiệu quảcủJSONtin nhắn")

                except websockets.ConnectionClosed:
                    logger.bind(tag=TAG).warning("WebSocketkết nốiđãđóng")
                    break

                except Exception as e:
                    logger.bind(tag=TAG).error(
                        f"xử lýTTSphản hồikhi/thờira: {e}\n{traceback.format_exc()}"
                    )
                    break

            # khôngsử dụng
            if self.ws:
                try:
                    await self.ws.close()
                except:
                    pass
                self.ws = None
        # dọn dẹp tham chiếu khi nhiệm vụ nghe thoát
        finally:
            self.activate_session = False
            self._monitor_task = None

    def to_tts(self, text: str) -> list:
        """luồngTTSxử lý，sử dụngtạikiểm travà/cũnglưuâm thanhtệpcủ"""
        try:
            # tạocủ
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # lưu trữ dữ liệu âm thanh
            audio_data = []

            async def _generate_audio():
                # tạo URL xác thực
                auth_url = XunfeiWSAuth.create_auth_url(
                    self.api_key, self.api_secret, self.api_url
                )

                # WebSocketkết nối
                ws = await websockets.connect(
                    auth_url,
                    ping_interval=30,
                    ping_timeout=10,
                    close_timeout=10,
                )

                try:
                    filtered_text = MarkdownCleaner.clean_markdown(text)
                    if self._correct_words_pattern:
                        filtered_text = self._correct_words_pattern.sub(lambda m: self.correct_words[m.group(0)], filtered_text)

                    text_request = self._build_base_request(status=2,text=filtered_text)

                    await ws.send(json.dumps(text_request))

                    task_finished = False
                    while not task_finished:
                        msg = await ws.recv()

                        data = json.loads(msg)
                        header = data.get("header", {})
                        code = header.get("code")

                        if code == 0:
                            payload = data.get("payload", {})
                            audio_payload = payload.get("audio", {})
                            if audio_payload:
                                status = audio_payload.get("status", 0)
                                audio_base64 = audio_payload.get("audio", "")
                                if status == 1:
                                    try:
                                        audio_bytes = base64.b64decode(audio_base64)
                                        self.opus_encoder.encode_pcm_to_opus_stream(
                                            audio_bytes,
                                            end_of_stream=False,
                                            callback=lambda opus: audio_data.append(opus)
                                        )
                                    except Exception as e:
                                        logger.bind(tag=TAG).error(f"xử lýdữ liệu âm thanhthất bại: {e}")
                                elif status == 2:
                                    task_finished = True
                                    logger.bind(tag=TAG).debug("TTSnhiệm vụhoàn thành")

                        else:
                            message = header.get("message", "lỗi không xác định")
                            raise Exception(f"thất bại: {code} - {message}")

                finally:
                    # dọn dẹp tài nguyên
                    try:
                        await ws.close()
                    except:
                        pass

            loop.run_until_complete(_generate_audio())
            loop.close()

            return audio_data
        except Exception as e:
            logger.bind(tag=TAG).error(f"tạodữ liệu âm thanhthất bại: {str(e)}")
            return []

    def audio_to_opus_data_stream(
        self, audio_file_path, callback: Callable[[Any], Any] = None
    ):
        """ghi đèphương pháp：làm chosử dụngcủtạm thờimã hóaxử lýâm thanhtệp，vớiTTSluồngmã hóavà。
        luồngTTStrong，monitornhiệm vụtại/trongevent loopluồngnhậnTTSâm thanhvàlàm chosử dụngself.opus_encodermã hóa，
        khi/thờitts_text_priority_threadxử lýtệplàm chosử dụngself.opus_encoder，
        củencoder.bufferluồngan toàn，vàsẽSILK resamplerthất bại。
        """
        from core.utils.util import audio_to_data_stream

        return audio_to_data_stream(
            audio_file_path,
            is_opus=True,
            callback=callback,
            sample_rate=self.conn.sample_rate,
            opus_encoder=None,
        )

    def _build_base_request(self, status, text=" "):
        """xây dựngyêu cầu"""
        return {
            "header": {
                "app_id": self.app_id,
                "status": status,
            },
            "parameter": {
                "oral": {
                    "oral_level": self.oral_level,
                    "spark_assist": self.spark_assist,
                    "stop_split": self.stop_split,
                    "remain": self.remain
                },
                "tts": {
                    "vcn": self.voice,
                    "speed": self.speed,
                    "volume": self.volume,
                    "pitch": self.pitch,
                    "bgs": 0,
                    "reg": 0,
                    "rdn": 0,
                    "rhy": 0,
                    "audio": {
                        "encoding": self.format,
                        "sample_rate": self.conn.sample_rate,
                        "channels": 1,
                        "bit_depth": 16,
                        "frame_size": 0
                    }
                }
            },
            "payload": {
                "text": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "plain",
                    "status": status,
                    "seq": self.text_seq,
                    "text": base64.b64encode(text.encode('utf-8')).decode('utf-8')
                }
            }
        }
