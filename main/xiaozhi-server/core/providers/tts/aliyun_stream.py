import os
import uuid
import json
import hmac
import hashlib
import base64
import time
import queue
import asyncio
import traceback
import websockets

from asyncio import Task
from urllib import parse
from datetime import datetime
from typing import Callable, Any
from config.logger import setup_logging
from core.utils.tts import MarkdownCleaner
from core.providers.tts.base import TTSProviderBase
from core.providers.tts.dto.dto import SentenceType, ContentType, InterfaceType


TAG = __name__
logger = setup_logging()


class AccessToken:
    @staticmethod
    def _encode_text(text):
        encoded_text = parse.quote_plus(text)
        return encoded_text.replace("+", "%20").replace("*", "%2A").replace("%7E", "~")

    @staticmethod
    def _encode_dict(dic):
        keys = dic.keys()
        dic_sorted = [(key, dic[key]) for key in sorted(keys)]
        encoded_text = parse.urlencode(dic_sorted)
        return encoded_text.replace("+", "%20").replace("*", "%2A").replace("%7E", "~")

    @staticmethod
    def create_token(access_key_id, access_key_secret):
        parameters = {
            "AccessKeyId": access_key_id,
            "Action": "CreateToken",
            "Format": "JSON",
            "RegionId": "cn-shanghai",  # Sử dụng khu vực Thượng Hải để lấy Token
            "SignatureMethod": "HMAC-SHA1",
            "SignatureNonce": str(uuid.uuid1()),
            "SignatureVersion": "1.0",
            "Timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "Version": "2019-02-28",
        }

        query_string = AccessToken._encode_dict(parameters)
        string_to_sign = (
            "GET"
            + "&"
            + AccessToken._encode_text("/")
            + "&"
            + AccessToken._encode_text(query_string)
        )

        secreted_string = hmac.new(
            bytes(access_key_secret + "&", encoding="utf-8"),
            bytes(string_to_sign, encoding="utf-8"),
            hashlib.sha1,
        ).digest()
        signature = base64.b64encode(secreted_string)
        signature = AccessToken._encode_text(signature)

        full_url = "http://nls-meta.cn-shanghai.aliyuncs.com/?Signature=%s&%s" % (
            signature,
            query_string,
        )

        import requests

        response = requests.get(full_url)
        if response.ok:
            root_obj = response.json()
            key = "Token"
            if key in root_obj:
                token = root_obj[key]["Id"]
                expire_time = root_obj[key]["ExpireTime"]
                return token, expire_time
        return None, None


class TTSProvider(TTSProviderBase):
    TTS_PARAM_CONFIG = [
        ("ttsVolume", "volume", 0, 100, 50, int),
        ("ttsRate", "speech_rate", -500, 500, 0, int),
        ("ttsPitch", "pitch_rate", -500, 500, 0, int),
    ]

    def __init__(self, config, delete_audio_file):
        super().__init__(config, delete_audio_file)

        # Đặt thành stream interface type
        self.interface_type = InterfaceType.DUAL_STREAM

        # Cấu hình cơ bản
        self.access_key_id = config.get("access_key_id")
        self.access_key_secret = config.get("access_key_secret")
        self.appkey = config.get("appkey")
        self.format = config.get("format", "pcm")
        self.report_on_last = True

        # Cấu hình voice - CosyVoicemô hình
        if config.get("private_voice"):
            self.voice = config.get("private_voice")
        else:
            self.voice = config.get("voice", "longxiaochun")  # CosyVoicemặc định

        # Cấu hình tham số âm thanh
        volume = config.get("volume", "50")
        self.volume = int(volume) if volume else 50

        speech_rate = config.get("speech_rate", "0")
        self.speech_rate = int(speech_rate) if speech_rate else 0

        pitch_rate = config.get("pitch_rate", "0")
        self.pitch_rate = int(pitch_rate) if pitch_rate else 0

        # Áp dụng điều chỉnh phần trăm (nếu có), nếu không thì dùng cấu hình chung
        self._apply_percentage_params(config)

        # Cấu hình WebSocket
        self.host = config.get("host", "nls-gateway-cn-beijing.aliyuncs.com")
        # Nếu cấu hình địa chỉ nội bộ (chứa -internal.aliyuncs.com), sử dụng ws, mặc định là wss
        if "-internal." in self.host:
            self.ws_url = f"ws://{self.host}/ws/v1"
        else:
            # mặc định sử dụng wss
            self.ws_url = f"wss://{self.host}/ws/v1"
        self.ws = None
        self._monitor_task = None
        self.activate_session = False
        self.last_active_time = None

        # cấu hình tts chuyên dụng
        self.task_id = uuid.uuid4().hex

        # quản lý Token
        if self.access_key_id and self.access_key_secret:
            self._refresh_token()
        else:
            self.token = config.get("token")
            self.expire_time = None

    def _refresh_token(self):
        """làm mớiTokenvàghi lạiquakhi/thời"""
        if self.access_key_id and self.access_key_secret:
            self.token, expire_time_str = AccessToken.create_token(
                self.access_key_id, self.access_key_secret
            )
            if not expire_time_str:
                raise ValueError("lấyhiệu quảcủTokenquakhi/thời")

            expire_str = str(expire_time_str).strip()

            try:
                if expire_str.isdigit():
                    expire_time = datetime.fromtimestamp(int(expire_str))
                else:
                    expire_time = datetime.strptime(expire_str, "%Y-%m-%dT%H:%M:%SZ")
                self.expire_time = expire_time.timestamp() - 60
            except Exception as e:
                raise ValueError(f"không hiệu quảcủquakhi/thờiđịnh dạng: {expire_str}") from e
        else:
            self.expire_time = None

        if not self.token:
            raise ValueError("lấyhiệu quảcủToken")

    def _is_token_expired(self):
        """kiểm traTokenlàqua"""
        if not self.expire_time:
            return False
        return time.time() > self.expire_time

    async def _ensure_connection(self):
        """đảm bảoWebSocketkết nốikhả dụng"""
        try:
            if self._is_token_expired():
                logger.bind(tag=TAG).warning("Tokenđãqua，tại/tronglàm mới...")
                self._refresh_token()
            current_time = time.time()
            if self.ws and current_time - self.last_active_time < 10:
                # 10bên trongcó thểsử dụngtiến hànhvới
                self.task_id = uuid.uuid4().hex
                logger.bind(tag=TAG).debug(f"làm chosử dụngđãcó..., task_id: {self.task_id}")
                return self.ws
            logger.bind(tag=TAG).debug("Bắt đầu tạo connection mới...")

            self.ws = await websockets.connect(
                self.ws_url,
                additional_headers={"X-NLS-Token": self.token},
                ping_interval=30,
                ping_timeout=10,
                close_timeout=10,
            )
            self.task_id = uuid.uuid4().hex
            logger.bind(tag=TAG).debug(f"WebSocketkết nốithành công, task_id: {self.task_id}")
            self.last_active_time = time.time()
            return self.ws
        except Exception as e:
            logger.bind(tag=TAG).error(f"Tạo connection thất bại: {str(e)}")
            self.ws = None
            self.last_active_time = None
            raise

    def tts_text_priority_thread(self):
        """luồngvăn bảnxử lýluồng"""
        while not self.conn.stop_event.is_set():
            try:
                message = self.tts_text_queue.get(timeout=1)

                if self.conn.client_abort:
                    logger.bind(tag=TAG).info("Nhận thông tin interrupt, chấm dứt thread xử lý text TTS")
                    asyncio.run_coroutine_threadsafe(
                        self.finish_session(self.conn.sentence_id),
                        loop=self.conn.loop,
                    )
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
                    # khởi tạo tham số
                    try:
                        logger.bind(tag=TAG).debug("bắt đầukhởi độngTTSphiên...")
                        future = asyncio.run_coroutine_threadsafe(
                            self.start_session(self.task_id),
                            loop=self.conn.loop,
                        )
                        future.result(timeout=self.tts_timeout)
                        self.before_stop_play_files.clear()
                        logger.bind(tag=TAG).debug("TTSphiênkhởi độngthành công")

                    except Exception as e:
                        logger.bind(tag=TAG).error(f"khởi độngTTSphiênthất bại: {str(e)}")
                        continue

                elif ContentType.TEXT == message.content_type:
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
                            continue

                elif ContentType.FILE == message.content_type:
                    logger.bind(tag=TAG).info(
                        f"thêmâm thanhtệpđến: {message.content_file}"
                    )
                    if message.content_file and os.path.exists(message.content_file):
                        # xử lý dữ liệu âm thanh tệp trước
                        self._process_audio_file_stream(message.content_file, callback=lambda audio_data: self.handle_audio_file(audio_data, message.content_detail))
                if message.sentence_type == SentenceType.LAST:
                    try:
                        logger.bind(tag=TAG).debug("bắt đầukết thúcTTSphiên...")
                        future = asyncio.run_coroutine_threadsafe(
                            self.finish_session(self.task_id),
                            loop=self.conn.loop,
                        )
                        future.result(timeout=self.tts_timeout)
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
                        run_request = {
                            "header": {
                                "message_id": uuid.uuid4().hex,
                                "task_id": self.task_id,
                                "namespace": "FlowingSpeechSynthesizer",
                                "name": "RunSynthesis",
                                "appkey": self.appkey,
                            },
                            "payload": {"text": txt},
                        }
                        await self.ws.send(json.dumps(run_request))
                        self.last_active_time = time.time()
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

    async def start_session(self, task_id):
        logger.bind(tag=TAG).debug("bắt đầuphiên～～")
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

            start_request = {
                "header": {
                    "message_id": uuid.uuid4().hex,
                    "task_id": self.task_id,
                    "namespace": "FlowingSpeechSynthesizer",
                    "name": "StartSynthesis",
                    "appkey": self.appkey,
                },
                "payload": {
                    "voice": self.voice,
                    "format": self.format,
                    "sample_rate": self.conn.sample_rate,
                    "volume": self.volume,
                    "speech_rate": self.speech_rate,
                    "pitch_rate": self.pitch_rate,
                    "enable_subtitle": True,
                },
            }
            await self.ws.send(json.dumps(start_request))
            self.last_active_time = time.time()
            logger.bind(tag=TAG).debug("phiênkhởi độngyêu cầuđãgửi")
        except Exception as e:
            logger.bind(tag=TAG).error(f"khởi độngphiênthất bại: {str(e)}")
            # đảm bảodọn dẹptài nguyên
            await self.close()
            raise

    async def finish_session(self, task_id):
        logger.bind(tag=TAG).debug(f"đóngphiên～～{task_id}")
        try:
            if self.ws:
                stop_request = {
                    "header": {
                        "message_id": uuid.uuid4().hex,
                        "task_id": self.task_id,
                        "namespace": "FlowingSpeechSynthesizer",
                        "name": "StopSynthesis",
                        "appkey": self.appkey,
                    }
                }
                await self.ws.send(json.dumps(stop_request))
                logger.bind(tag=TAG).debug("phiênkết thúcyêu cầuđãgửi")
                self.last_active_time = time.time()

        except Exception as e:
            logger.bind(tag=TAG).error(f"đóngphiênthất bại: {str(e)}")
            # đảm bảodọn dẹptài nguyên
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
            self.last_active_time = None

    async def _start_monitor_tts_response(self):
        """TTSphản hồi - """
        try:
            while not self.conn.stop_event.is_set():
                try:
                    msg = await self.ws.recv()
                    self.last_active_time = time.time()

                    if isinstance(msg, str):  # văn bảntin nhắn
                        try:
                            data = json.loads(msg)
                            header = data.get("header", {})
                            event_name = header.get("name")
                            task_id = header.get("task_id")

                            # chỉ xử lý phản hồi của phiên đang hoạt động hiện tại
                            if task_id and self.task_id != task_id:
                                if event_name in ["SynthesisCompleted", "TaskFailed"]:
                                    logger.bind(tag=TAG).debug(f"đếnkết thúcphản hồiđặt lạiphiêntrạng thái～～")
                                    self.activate_session = False
                                continue

                            if event_name == "SynthesisStarted":
                                logger.bind(tag=TAG).debug("TTSđãkhởi động")
                                self.tts_audio_queue.put(
                                    (SentenceType.FIRST, [], None)
                                )
                            elif event_name == "SentenceEnd":
                                # gửi dữ liệu đã lưu vào bộ nhớ đệm
                                tts_text = self.get_tts_text(self.conn.sentence_id)
                                if tts_text:
                                    logger.bind(tag=TAG).info(
                                        f"câugiọng nóitạothành công： {tts_text}"
                                    )
                                    self.tts_audio_queue.put(
                                        (SentenceType.FIRST, [], tts_text)
                                    )
                                    self.clear_tts_text(self.conn.sentence_id)
                            elif event_name == "SynthesisCompleted":
                                logger.bind(tag=TAG).debug(f"phiênkết thúc～～")
                                self.activate_session = False
                                self._process_before_stop_play_files()
                        except json.JSONDecodeError:
                            logger.bind(tag=TAG).warning("đếnkhông hiệu quảcủJSONtin nhắn")
                    # tin nhắn（dữ liệu âm thanh）
                    elif isinstance(msg, (bytes, bytearray)):
                        self.opus_encoder.encode_pcm_to_opus_stream(msg, False, self.handle_opus)
                except websockets.ConnectionClosed:
                    logger.bind(tag=TAG).warning("WebSocketkết nốiđãđóng")
                    break
                except Exception as e:
                    logger.bind(tag=TAG).error(
                        f"xử lýTTSphản hồikhi/thờira: {e}\n{traceback.format_exc()}"
                    )
                    break
            # đóng WebSocket khi có ngoại lệ kết nối
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

    def to_tts(self, text: str) -> list:
        """luồngTTSxử lý，sử dụngtạikiểm travà/cũnglưuâm thanhtệpcủ"""
        try:
            # tạocủ
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # lưu trữ dữ liệu âm thanh
            audio_data = []

            async def _generate_audio():
                # làm mớiToken（nhưcần）
                if self._is_token_expired():
                    self._refresh_token()

                # WebSocketkết nối
                ws = await websockets.connect(
                    self.ws_url,
                    additional_headers={"X-NLS-Token": self.token},
                    ping_interval=30,
                    ping_timeout=10,
                    close_timeout=10,
                )
                try:
                    # gửiStartSynthesisyêu cầu
                    start_request = {
                        "header": {
                            "message_id": uuid.uuid4().hex,
                            "task_id": self.task_id,
                            "namespace": "FlowingSpeechSynthesizer",
                            "name": "StartSynthesis",
                            "appkey": self.appkey,
                        },
                        "payload": {
                            "voice": self.voice,
                            "format": self.format,
                            "sample_rate": self.conn.sample_rate,
                            "volume": self.volume,
                            "speech_rate": self.speech_rate,
                            "pitch_rate": self.pitch_rate,
                            "enable_subtitle": True,
                        },
                    }
                    await ws.send(json.dumps(start_request))

                    # chờSynthesisStartedphản hồi
                    synthesis_started = False
                    while not synthesis_started:
                        msg = await ws.recv()
                        if isinstance(msg, str):
                            data = json.loads(msg)
                            header = data.get("header", {})
                            if header.get("name") == "SynthesisStarted":
                                synthesis_started = True
                                logger.bind(tag=TAG).debug("TTSđãkhởi động")
                            elif header.get("name") == "TaskFailed":
                                error_info = data.get("payload", {}).get(
                                    "error_info", {}
                                )
                                error_code = error_info.get("error_code")
                                error_message = error_info.get(
                                    "error_message", "lỗi không xác định"
                                )
                                raise Exception(
                                    f"khởi độngthất bại: {error_code} - {error_message}"
                                )

                    # Gửi request synthesis text
                    filtered_text = MarkdownCleaner.clean_markdown(text)
                    if self._correct_words_pattern:
                        filtered_text = self._correct_words_pattern.sub(lambda m: self.correct_words[m.group(0)], filtered_text)
                    run_request = {
                        "header": {
                            "message_id": uuid.uuid4().hex,
                            "task_id": self.task_id,
                            "namespace": "FlowingSpeechSynthesizer",
                            "name": "RunSynthesis",
                            "appkey": self.appkey,
                        },
                        "payload": {"text": filtered_text},
                    }
                    await ws.send(json.dumps(run_request))

                    # gửidừngyêu cầu
                    stop_request = {
                        "header": {
                            "message_id": uuid.uuid4().hex,
                            "task_id": self.task_id,
                            "namespace": "FlowingSpeechSynthesizer",
                            "name": "StopSynthesis",
                            "appkey": self.appkey,
                        }
                    }
                    await ws.send(json.dumps(stop_request))

                    # Nhận audio data
                    synthesis_completed = False
                    while not synthesis_completed:
                        msg = await ws.recv()
                        if isinstance(msg, (bytes, bytearray)):
                            self.opus_encoder.encode_pcm_to_opus_stream(
                                msg,
                                end_of_stream=False,
                                callback=lambda opus: audio_data.append(opus)
                            )
                        elif isinstance(msg, str):
                            data = json.loads(msg)
                            header = data.get("header", {})
                            event_name = header.get("name")
                            if event_name == "SynthesisCompleted":
                                synthesis_completed = True
                                logger.bind(tag=TAG).debug("TTShoàn thành")
                            elif event_name == "TaskFailed":
                                error_info = data.get("payload", {}).get(
                                    "error_info", {}
                                )
                                error_code = error_info.get("error_code")
                                error_message = error_info.get(
                                    "error_message", "lỗi không xác định"
                                )
                                raise Exception(
                                    f"thất bại: {error_code} - {error_message}"
                                )
                finally:
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