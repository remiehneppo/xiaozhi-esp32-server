import os
import uuid
import json
import time
import queue
import asyncio
import traceback
import websockets

from asyncio import Task
from typing import Callable, Any
from config.logger import setup_logging
from core.utils.tts import MarkdownCleaner
from core.providers.tts.base import TTSProviderBase
from core.providers.tts.dto.dto import SentenceType, ContentType, InterfaceType

TAG = __name__
logger = setup_logging()


class TTSProvider(TTSProviderBase):
    TTS_PARAM_CONFIG = [
        ("ttsVolume", "volume", 0, 100, 50, int),
        ("ttsRate", "rate", 0.5, 2.0, 1.0, lambda v: round(v, 1)),
        ("ttsPitch", "pitch", 0.5, 2.0, 1.0, lambda v: round(v, 1)),
    ]

    def __init__(self, config, delete_audio_file):
        super().__init__(config, delete_audio_file)

        self.interface_type = InterfaceType.DUAL_STREAM
        # Cấu hình cơ bản
        self.api_key = config.get("api_key")
        if not self.api_key:
            raise ValueError("api_key is required for CosyVoice TTS")
        self.report_on_last = True

        # Cấu hình WebSocket
        self.ws_url = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/"
        self.ws = None
        self._monitor_task = None
        self.activate_session = False
        self.last_active_time = None

        # Cấu hình mô hình và giọng nói
        self.model = config.get("model", "cosyvoice-v2")
        self.voice = config.get("voice", "longxiaochun_v2")  # giọng nói mặc định
        if config.get("private_voice"):
            self.voice = config.get("private_voice")

        # Cấu hình tham số âm thanh
        self.format = config.get("format", "pcm")

        volume = config.get("volume", "50")
        self.volume = int(volume) if volume else 50

        rate = config.get("rate", "1.0")
        self.rate = float(rate) if rate else 1.0

        pitch = config.get("pitch", "1.0")
        self.pitch = float(pitch) if pitch else 1.0

        # Áp dụng điều chỉnh phần trăm (nếu có), nếu không thì dùng cấu hình chung
        self._apply_percentage_params(config)

        self.header = {
            "Authorization": f"Bearer {self.api_key}",
            # "user-agent": "your_platform_info", // tùy chọn
            # "X-DashScope-WorkSpace": workspace, // tùy chọn, ID không gian làm việc Bailian của Alibaba Cloud
            "X-DashScope-DataInspection": "enable",
        }

    async def _ensure_connection(self):
        """đảm bảoWebSocketkết nốikhả dụng，60bên trongkết nốisử dụng"""
        try:
            current_time = time.time()
            if self.ws and current_time - self.last_active_time < 60:
                # chỉ có thể tái sử dụng kết nối trong vòng 1 phút để hội thoại liên tục
                logger.bind(tag=TAG).debug(f"Đang dùng link có sẵn...")
                return self.ws
            logger.bind(tag=TAG).debug("Bắt đầu tạo connection mới...")

            self.ws = await websockets.connect(
                self.ws_url,
                additional_headers=self.header,
                ping_interval=30,
                ping_timeout=10,
                close_timeout=10,
            )

            logger.bind(tag=TAG).debug("WebSocket connection tạo thành công")
            self.last_active_time = current_time
            return self.ws
        except Exception as e:
            logger.bind(tag=TAG).error(f"Tạo connection thất bại: {str(e)}")
            self.ws = None
            self.last_active_time = None
            raise

    def tts_text_priority_thread(self):
        """luồngTTSvăn bảnxử lýluồng"""
        while not self.conn.stop_event.is_set():
            try:
                message = self.tts_text_queue.get(timeout=1)

                if self.conn.client_abort:
                    try:
                        logger.bind(tag=TAG).info("Nhận thông tin interrupt, chấm dứt thread xử lý text TTS")
                        asyncio.run_coroutine_threadsafe(
                            self.finish_session(self.conn.sentence_id),
                            loop=self.conn.loop,
                        )
                        continue
                    except Exception as e:
                        logger.bind(tag=TAG).error(f"Hủy session TTS thất bại: {str(e)}")
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
                    # khởi tạo phiên
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
                            self.finish_session(self.conn.sentence_id),
                            loop=self.conn.loop,
                        )
                        future.result()
                    except Exception as e:
                        logger.bind(tag=TAG).error(f"kết thúcTTSphiênthất bại: {str(e)}")
                        continue

            except queue.Empty:
                continue
            except Exception as e:
                logger.bind(tag=TAG).error(
                    f"xử lýTTSvăn bảnthất bại: {str(e)}, : {type(e).__name__}, stack: {traceback.format_exc()}"
                )
                continue

    async def text_to_speak(self, text, _):
        """gửivăn bảnđếnTTSdịch vụtiến hành"""
        try:
            if self.ws is None:
                logger.bind(tag=TAG).warning("WebSocketkết nốikhôngtại/trong，dừnggửivăn bản")
                return

            # lọc Markdown
            filtered_text = MarkdownCleaner.clean_markdown(text)

            if filtered_text:
                # sử dụng cửa sổ trượt để khớp xử lý từ thay thế qua các phân đoạn
                confirmed_texts, self._pending_prefix = self._match_stream_text(filtered_text)

                # gửi mỗi đoạn văn bản đã xác định
                for txt in confirmed_texts:
                    if txt and self.ws:
                        continue_task_message = {
                            "header": {
                                "action": "continue-task",
                                "task_id": self.conn.sentence_id,
                                "streaming": "duplex",
                            },
                            "payload": {"input": {"text": txt}},
                        }
                        await self.ws.send(json.dumps(continue_task_message))
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

    async def start_session(self, session_id):
        """khởi độngTTSphiên"""
        logger.bind(tag=TAG).debug(f"bắt đầuphiên～～{session_id}")
        try:
            # đóng kết nối cũ và tạo kết nối mới khi phiên trước đang ở trạng thái hoạt động
            if self.activate_session:
                await self.close()

            # đặt cờ kích hoạt phiên
            self.activate_session = True

            # đảm bảo kết nối khả dụng
            await self._ensure_connection()

            # bắt đầu nhiệm vụ nghe
            if self._monitor_task is None or self._monitor_task.done():
                logger.bind(tag=TAG).debug("Khởi động listen task...")
                self._monitor_task = asyncio.create_task(self._start_monitor_tts_response())

            # gửi tin nhắn run-task để khởi động phiên
            run_task_message = {
                "header": {
                    "action": "run-task",
                    "task_id": session_id,
                    "streaming": "duplex",
                },
                "payload": {
                    "task_group": "audio",
                    "task": "tts",
                    "function": "SpeechSynthesizer",
                    "model": self.model,
                    "parameters": {
                        "text_type": "PlainText",
                        "voice": self.voice,
                        "format": self.format,
                        "sample_rate": self.conn.sample_rate,
                        "volume": self.volume,
                        "rate": self.rate,
                        "pitch": self.pitch,
                    },
                    "input": {}
                },
            }

            await self.ws.send(json.dumps(run_task_message))
            self.last_active_time = time.time()
            logger.bind(tag=TAG).debug("phiênkhởi độngyêu cầuđãgửi")
        except Exception as e:
            logger.bind(tag=TAG).error(f"khởi độngphiênthất bại: {str(e)}")
            await self.close()
            raise

    async def finish_session(self, session_id):
        """kết thúcTTSphiên"""
        logger.bind(tag=TAG).debug(f"đóngphiên～～{session_id}")
        try:
            if self.ws and session_id:
                # gửi tin nhắn finish-task
                finish_task_message = {
                    "header": {
                        "action": "finish-task",
                        "task_id": session_id,
                        "streaming": "duplex",
                    },
                    "payload": {
                        "input": {}
                    }
                }

                await self.ws.send(json.dumps(finish_task_message))
                self.last_active_time = time.time()

        except Exception as e:
            logger.bind(tag=TAG).error(f"đóngphiênthất bại: {str(e)}")
            await self.close()
            raise

    async def close(self):
        """dọn dẹptài nguyên"""
        await super().close()
        self.activate_session = False
        # hủy nhiệm vụ nghe
        if self._monitor_task:
            try:
                self._monitor_task.cancel()
                await self._monitor_task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logger.bind(tag=TAG).warning(f"đóngkhi/thờihủynhiệm vụsai: {e}")
            self._monitor_task = None

        # Đóng kết nối WebSocket
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

                    if isinstance(msg, str):  # JSONtin nhắn
                        try:
                            data = json.loads(msg)
                            header = data.get("header", {})
                            event = header.get("event")
                            task_id = header.get("task_id")

                            # chỉ xử lý phản hồi của phiên đang hoạt động hiện tại
                            if task_id and self.conn.sentence_id != task_id:
                                if event in ["task-finished", "task-failed"]:
                                    logger.bind(tag=TAG).debug(f"đếnkết thúcphản hồiđặt lạiphiêntrạng thái～～")
                                    self.activate_session = False
                                continue

                            if event == "task-started":
                                logger.bind(tag=TAG).debug("TTSnhiệm vụkhởi độngthành công~")
                                self.tts_audio_queue.put((SentenceType.FIRST, [], None))
                            elif event == "result-generated":
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
                            elif event == "task-finished":
                                logger.bind(tag=TAG).debug("TTSnhiệm vụhoàn thành~")
                                self.activate_session = False
                                self._process_before_stop_play_files()
                            elif event == "task-failed":
                                error_code = header.get("error_code", "unknown")
                                error_message = header.get("error_message", "lỗi không xác định")
                                logger.bind(tag=TAG).error(
                                    f"TTSnhiệm vụthất bại: {error_code} - {error_message}"
                                )
                                break
                        except json.JSONDecodeError:
                            logger.bind(tag=TAG).warning("đếnkhông hiệu quảcủJSONtin nhắn")
                    elif isinstance(msg, (bytes, bytearray)):
                        self.opus_encoder.encode_pcm_to_opus_stream(
                            msg, False, callback=self.handle_opus
                        )
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
        """luồngtạodữ liệu âm thanh，sử dụngtạitạoâm thanhvà/cũngkiểm tra"""
        try:
            # tạo vòng lặp sự kiện
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # tạo ID phiên
            session_id = uuid.uuid4().hex
            # lưu trữ dữ liệu âm thanh
            audio_data = []

            async def _generate_audio():
                ws = await websockets.connect(
                    self.ws_url,
                    additional_headers=self.header,
                    ping_interval=30,
                    ping_timeout=10,
                    close_timeout=10,
                    max_size=10 * 1024 * 1024,
                )

                try:
                    # gửi tin nhắn run-task để khởi động phiên
                    run_task_message = {
                        "header": {
                            "action": "run-task",
                            "task_id": session_id,
                            "streaming": "duplex",
                        },
                        "payload": {
                            "task_group": "audio",
                            "task": "tts",
                            "function": "SpeechSynthesizer",
                            "model": self.model,
                            "parameters": {
                                "text_type": "PlainText",
                                "voice": self.voice,
                                "format": self.format,
                                "sample_rate": self.conn.sample_rate,
                                "volume": self.volume,
                                "rate": self.rate,
                                "pitch": self.pitch,
                            },
                            "input": {}
                        },
                    }
                    await ws.send(json.dumps(run_task_message))

                    # chờ khởi động nhiệm vụ
                    task_started = False
                    while not task_started:
                        msg = await ws.recv()
                        if isinstance(msg, str):
                            data = json.loads(msg)
                            header = data.get("header", {})
                            if header.get("event") == "task-started":
                                task_started = True
                                logger.bind(tag=TAG).debug("TTSnhiệm vụđãkhởi động")
                            elif header.get("event") == "task-failed":
                                error_code = header.get("error_code", "unknown")
                                error_message = header.get("error_message", "lỗi không xác định")
                                raise Exception(
                                    f"khởi độngnhiệm vụthất bại: {error_code} - {error_message}"
                                )

                    # gửi văn bản
                    filtered_text = MarkdownCleaner.clean_markdown(text)
                    if self._correct_words_pattern:
                        filtered_text = self._correct_words_pattern.sub(lambda m: self.correct_words[m.group(0)], filtered_text)
                    # gửi tin nhắn continue-task
                    continue_task_message = {
                        "header": {
                            "action": "continue-task",
                            "task_id": session_id,
                            "streaming": "duplex",
                        },
                        "payload": {"input": {"text": filtered_text}},
                    }
                    await ws.send(json.dumps(continue_task_message))

                    # gửi tin nhắn finish-task
                    finish_task_message = {
                        "header": {
                            "action": "finish-task",
                            "task_id": session_id,
                            "streaming": "duplex",
                        },
                        "payload": {
                            "input": {}
                        }
                    }
                    await ws.send(json.dumps(finish_task_message))

                    # Nhận audio data
                    task_finished = False
                    while not task_finished:
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
                            if header.get("event") == "task-finished":
                                task_finished = True
                                logger.bind(tag=TAG).debug("TTSnhiệm vụhoàn thành")
                            elif header.get("event") == "task-failed":
                                error_code = header.get("error_code", "unknown")
                                error_message = header.get("error_message", "lỗi không xác định")
                                raise Exception(
                                    f"thất bại: {error_code} - {error_message}"
                                )

                finally:
                    # dọn dẹp tài nguyên
                    try:
                        await ws.close()
                    except:
                        pass

            # chạy nhiệm vụ bất đồng bộ
            loop.run_until_complete(_generate_audio())
            loop.close()

            return audio_data

        except Exception as e:
            logger.bind(tag=TAG).error(f"tạodữ liệu âm thanhthất bại: {str(e)}")
            return []