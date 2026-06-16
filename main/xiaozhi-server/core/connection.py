import os
import sys
import copy
import json
import re
import uuid
import time
import queue
import asyncio
import threading
import traceback
import subprocess
import websockets

from core.utils.util import (
    extract_json_from_string,
    check_vad_update,
    check_asr_update,
    filter_sensitive_info,
)
from typing import Dict, Any
from collections import deque
from core.utils.modules_initialize import (
    initialize_modules,
    initialize_tts,
    initialize_asr,
)
from core.handle.reportHandle import report, enqueue_tool_report
from core.providers.tts.default import DefaultTTS
from concurrent.futures import ThreadPoolExecutor
from core.utils.dialogue import Message, Dialogue
from core.providers.asr.dto.dto import InterfaceType
from core.handle.textHandle import handleTextMessage
from core.providers.tools.unified_tool_handler import UnifiedToolHandler
from plugins_func.loadplugins import auto_import_modules
from plugins_func.register import Action, ActionResponse
from core.auth import AuthenticationError
from config.config_loader import get_private_config_from_api
from core.providers.tts.dto.dto import ContentType, TTSMessageDTO, SentenceType
from config.logger import setup_logging, build_module_string, create_connection_logger
from config.manage_api_client import DeviceNotFoundException, DeviceBindException, generate_and_save_chat_title
from core.utils.prompt_manager import PromptManager
from core.utils.voiceprint_provider import VoiceprintProvider
from core.utils.util import get_system_error_response
from core.utils import textUtils


TAG = __name__

auto_import_modules("plugins_func.functions")


class TTSException(RuntimeError):
    pass

# direct_answer - Định nghĩa công cụ ảo
# Không phải công cụ thật, là cơ chế định tuyến: chuyển lựa chọn "có/không gọi công cụ" thành "gọi công cụ nào", ngăn mô hình nhỏ kích hoạt nhầm công cụ thật
DIRECT_ANSWER_TOOL = {
    "type": "function",
    "function": {
        "name": "direct_answer",
        "description": "Khi yêu cầu người dùng không khớp với bất kỳ công cụ nào, hãy dùng tùy chọn này để trả lời trực tiếp. Viết nội dung trả lời trong tham số response.",
        "parameters": {
            "type": "object",
            "properties": {
                "response": {
                    "type": "string",
                    "description": "Nội dung đầy đủ bạn trả lời người dùng",
                },
            },
            "required": ["response"],
        },
    },
}


class ConnectionHandler:
    def __init__(
            self,
            config: Dict[str, Any],
            _vad,
            _asr,
            _llm,
            _memory,
            _intent,
            server=None,
    ):
        self.common_config = config
        self.config = copy.deepcopy(config)
        self.session_id = str(uuid.uuid4())
        self.logger = setup_logging()
        self.server = server  # Giữ tham chiếu đến instance server

        self.need_bind = False  # Có cần ràng buộc thiết bị không
        self.bind_completed_event = asyncio.Event()
        self.bind_code = None  # Mã xác thực ràng buộc thiết bị
        self.last_bind_prompt_time = 0  # Nhãn thời gian nhắc ràng buộc lần cuối (giây)
        self.bind_prompt_interval = 60  # Khoảng phát nhắc ràng buộc (giây)

        self.read_config_from_api = self.config.get("read_config_from_api", False)

        self.websocket: websockets.ServerConnection | None = None
        self.headers = None
        self.device_id = None
        self.client_ip = None
        self.prompt = None
        self.welcome_msg = None
        self.max_output_size = 0
        self.chat_history_conf = 0
        self.audio_format = "opus"
        self.sample_rate = 24000  # Tốc độ lấy mẫu mặc định, cập nhật động từ tin nhắn hello của client

        # Liên quan trạng thái client
        self.client_abort = False
        self.client_is_speaking = False
        self.client_listen_mode = "auto"

        # Liên quan tác vụ luồng
        self.loop = None  # Lấy event loop đang chạy trong handle_connection
        self.stop_event = threading.Event()
        self.executor = ThreadPoolExecutor(max_workers=5)

        # Thêm thread pool báo cáo
        self.report_queue = queue.Queue()
        self.report_thread = None
        # Tương lai có thể chỉnh sửa ở đây để điều chỉnh báo cáo ASR và TTS, hiện tại mặc định đều bật
        self.report_asr_enable = self.read_config_from_api
        self.report_tts_enable = self.read_config_from_api

        # Thành phần phụ thuộc
        self.vad = None
        self.asr = None
        self.tts = None
        self._asr = _asr
        self._vad = _vad
        self.llm = _llm
        self.memory = _memory
        self.intent = _intent

        # Quản lý nhận dạng giọng nói riêng cho mỗi kết nối
        self.voiceprint_provider = None

        # Biến liên quan VAD
        self.client_audio_buffer = bytearray()
        self.client_have_voice = False
        self.client_voice_window = deque(maxlen=5)
        self.first_activity_time = 0.0  # Ghi lại thời điểm hoạt động đầu tiên (ms)
        self.last_activity_time = 0.0  # Nhãn thời gian hoạt động thống nhất (ms)
        self.vad_last_voice_time = 0.0  # Ghi lại thời điểm người dùng nói lần cuối (ms)
        self.client_voice_stop = False
        self.last_is_voice = False

        # Biến liên quan ASR
        # Vì khi triển khai thực tế có thể dùng ASR nội bộ dùng chung, không thể expose biến cho ASR chung
        # Vì vậy biến liên quan ASR cần định nghĩa ở đây, thuộc về biến private của connection
        self.asr_audio = []
        self.asr_audio_queue = queue.Queue()
        self.current_speaker = None  # Lưu người nói hiện tại

        # Biến liên quan LLM
        self.dialogue = Dialogue()

        # Biến liên quan TTS
        self.sentence_id = None
        # Xử lý khi TTS không trả về văn bản
        self.tts_MessageText = ""

        # Biến liên quan IoT
        self.iot_descriptors = {}
        self.func_handler = None

        self.cmd_exit = self.config["exit_commands"]

        # Có đóng kết nối sau khi kết thúc cuộc trò chuyện không
        self.close_after_chat = False
        self.load_function_plugin = False
        self.intent_type = "nointent"

        self.timeout_seconds = (
                int(self.config.get("close_connection_no_voice_time", 120)) + 60
        )  # Thêm 60 giây dựa trên lần đóng đầu tiên để thực hiện lần đóng thứ hai
        self.timeout_task = None

        # {"mcp":true} biểu thị kích hoạt chức năng MCP
        self.features = None

        # Đánh dấu kết nối có đến từ MQTT không
        self.conn_from_mqtt_gateway = False

        # Khởi tạo prompt manager
        self.prompt_manager = PromptManager(self.config, self.logger)

        # Khởi tạo trạng thái cuộc gọi
        self.calling = False

    async def handle_connection(self, ws: websockets.ServerConnection):
        try:
            # Lấy event loop đang chạy (phải trong ngữ cảnh bất đồng bộ)
            self.loop = asyncio.get_running_loop()

            # Lấy và xác thực headers
            self.headers = dict(ws.request.headers)
            real_ip = self.headers.get("x-real-ip") or self.headers.get(
                "x-forwarded-for"
            )
            if real_ip:
                self.client_ip = real_ip.split(",")[0].strip()
            else:
                self.client_ip = ws.remote_address[0]
            self.logger.bind(tag=TAG).info(
                f"{self.client_ip} conn - Headers: {self.headers}"
            )

            self.device_id = self.headers.get("device-id", None)

            # Xác thực thành công, tiếp tục xử lý
            self.websocket = ws

            # Kiểm tra có đến từ kết nối MQTT không
            request_path = ws.request.path
            self.conn_from_mqtt_gateway = request_path.endswith("?from=mqtt_gateway")
            if self.conn_from_mqtt_gateway:
                self.logger.bind(tag=TAG).info("Kết nối đến từ MQTT gateway")

            # Khởi tạo nhãn thời gian hoạt động
            self.first_activity_time = time.time() * 1000
            self.last_activity_time = time.time() * 1000

            # Khởi động tác vụ kiểm tra quá hạn
            self.timeout_task = asyncio.create_task(self._check_timeout())

            self.welcome_msg = self.config["xiaozhi"]
            self.welcome_msg["session_id"] = self.session_id

            # Đọc tốc độ lấy mẫu từ cấu hình
            self.sample_rate = self.welcome_msg["audio_params"]["sample_rate"]
            self.logger.bind(tag=TAG).info(f"Tần số lấy mẫu âm thanh đầu ra được cấu hình là: {self.sample_rate}")

            # Khởi tạo cấu hình và thành phần ở background (không block main loop)
            asyncio.create_task(self._background_initialize())

            try:
                async for message in self.websocket:
                    await self._route_message(message)
            except websockets.exceptions.ConnectionClosed:
                self.logger.bind(tag=TAG).info("Client đã ngắt kết nối")

        except AuthenticationError as e:
            self.logger.bind(tag=TAG).error(f"Xác thực thất bại: {str(e)}")
            return
        except Exception as e:
            stack_trace = traceback.format_exc()
            self.logger.bind(tag=TAG).error(f"Lỗi kết nối: {str(e)}-{stack_trace}")
            return
        finally:
            try:
                await self._save_and_close(ws)
            except Exception as final_error:
                self.logger.bind(tag=TAG).error(f"Lỗi khi dọn dẹp cuối cùng: {final_error}")
                # Đảm bảo dù lưu ký ức thất bại vẫn đóng kết nối
                try:
                    await self.close(ws)
                except Exception as close_error:
                    self.logger.bind(tag=TAG).error(
                        f"Lỗi khi buộc đóng kết nối: {close_error}"
                    )

    async def _save_and_close(self, ws):
        """Lưu ký ức và đóng kết nối"""
        try:
            # Daemon thread 1: tạo tiêu đề độc lập (không phụ thuộc memory model)
            if self.read_config_from_api and self.session_id:
                def generate_title_task():
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(
                            generate_and_save_chat_title(self.session_id)
                        )
                    except Exception as e:
                        self.logger.bind(tag=TAG).error(f"Tạo tiêu đề thất bại: {e}")
                    finally:
                        try:
                            loop.close()
                        except Exception:
                            pass

                threading.Thread(target=generate_title_task, daemon=True).start()

            # Daemon thread 2: lưu ký ức theo quy trình cũ (chỉ ký ức, không có tiêu đề)
            if self.memory:
                # Dùng thread pool lưu ký ức bất đồng bộ
                def save_memory_task():
                    try:
                        # Tạo event loop mới (tránh xung đột với main loop)
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(
                            self.memory.save_memory(
                                self.dialogue.dialogue, self.session_id
                            )
                        )
                    except Exception as e:
                        self.logger.bind(tag=TAG).error(f"Lưu bộ nhớ thất bại: {e}")
                    finally:
                        try:
                            loop.close()
                        except Exception:
                            pass

                # Khởi động luồng lưu ký ức, không chờ hoàn thành
                threading.Thread(target=save_memory_task, daemon=True).start()
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Lưu bộ nhớ thất bại: {e}")
        finally:
            # Đóng kết nối ngay, không chờ lưu ký ức xong
            try:
                await self.close(ws)
            except Exception as close_error:
                self.logger.bind(tag=TAG).error(
                    f"Đóng kết nối sau khi lưu bộ nhớ thất bại: {close_error}"
                )

    async def _discard_message_with_bind_prompt(self):
        """Bỏ tin nhắn và kiểm tra có cần phát nhắc ràng buộc không"""
        current_time = time.time()
        # Kiểm tra có cần phát nhắc ràng buộc không
        if current_time - self.last_bind_prompt_time >= self.bind_prompt_interval:
            self.last_bind_prompt_time = current_time
            # Tái sử dụng logic nhắc ràng buộc hiện có
            from core.handle.receiveAudioHandle import check_bind_device

            asyncio.create_task(check_bind_device(self))

    async def _route_message(self, message):
        """Định tuyến tin nhắn"""
        # Kiểm tra đã lấy được trạng thái ràng buộc thật chưa
        if not self.bind_completed_event.is_set():
            # Chưa lấy được trạng thái thật, đợi đến khi lấy được hoặc hết thời gian
            try:
                await asyncio.wait_for(self.bind_completed_event.wait(), timeout=1)
            except asyncio.TimeoutError:
                # Hết thời gian vẫn chưa lấy được trạng thái thật, bỏ tin nhắn
                await self._discard_message_with_bind_prompt()
                return

        # Đã lấy được trạng thái thật, kiểm tra có cần ràng buộc không
        if self.need_bind:
            # Cần ràng buộc, bỏ tin nhắn
            await self._discard_message_with_bind_prompt()
            return

        # Không cần ràng buộc, tiếp tục xử lý tin nhắn

        if isinstance(message, str):
            await handleTextMessage(self, message)
        elif isinstance(message, bytes):
            if self.vad is None or self.asr is None:
                return

            # Xử lý gói âm thanh từ gateway MQTT
            if self.conn_from_mqtt_gateway and len(message) >= 16:
                handled = await self._process_mqtt_audio_message(message)
                if handled:
                    return

            # Không cần xử lý header hoặc không có header thì xử lý trực tiếp tin nhắn gốc
            self.asr_audio_queue.put(message)

    async def _process_mqtt_audio_message(self, message):
        """
        Xử lý tin nhắn âm thanh từ gateway MQTT, giải tích 16 byte header và trích xuất dữ liệu âm thanh

        Args:
            message: tin nhắn âm thanh chứa header

        Returns:
            bool: có xử lý thành công tin nhắn không
        """
        try:
            # Trích xuất thông tin header
            timestamp = int.from_bytes(message[8:12], "big")
            audio_length = int.from_bytes(message[12:16], "big")

            # Trích xuất dữ liệu âm thanh
            if audio_length > 0 and len(message) >= 16 + audio_length:
                # Có độ dài chỉ định, trích xuất dữ liệu âm thanh chính xác
                audio_data = message[16 : 16 + audio_length]
                # Sắp xếp xử lý dựa trên nhãn thời gian
                self._process_websocket_audio(audio_data, timestamp)
                return True
            elif len(message) > 16:
                # Không có độ dài chỉ định hoặc độ dài không hợp lệ, bỏ header rồi xử lý dữ liệu còn lại
                audio_data = message[16:]
                self.asr_audio_queue.put(audio_data)
                return True
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Phân tích gói âm thanh WebSocket thất bại: {e}")

        # Xử lý thất bại, trả về False biểu thị cần tiếp tục xử lý
        return False

    def _process_websocket_audio(self, audio_data, timestamp):
        """Xử lý gói âm thanh định dạng WebSocket"""
        # Khởi tạo quản lý chuỗi nhãn thời gian
        if not hasattr(self, "audio_timestamp_buffer"):
            self.audio_timestamp_buffer = {}
            self.last_processed_timestamp = 0
            self.max_timestamp_buffer_size = 20

        # Nếu nhãn thời gian tăng dần thì xử lý trực tiếp
        if timestamp >= self.last_processed_timestamp:
            self.asr_audio_queue.put(audio_data)
            self.last_processed_timestamp = timestamp

            # Xử lý các gói tiếp theo trong buffer
            processed_any = True
            while processed_any:
                processed_any = False
                for ts in sorted(self.audio_timestamp_buffer.keys()):
                    if ts > self.last_processed_timestamp:
                        buffered_audio = self.audio_timestamp_buffer.pop(ts)
                        self.asr_audio_queue.put(buffered_audio)
                        self.last_processed_timestamp = ts
                        processed_any = True
                        break
        else:
            # Gói rối thứ tự, lưu tạm
            if len(self.audio_timestamp_buffer) < self.max_timestamp_buffer_size:
                self.audio_timestamp_buffer[timestamp] = audio_data
            else:
                self.asr_audio_queue.put(audio_data)

    async def handle_restart(self, message):
        """Xử lý yêu cầu khởi động lại máy chủ"""
        try:

            self.logger.bind(tag=TAG).info("Đã nhận lệnh khởi động lại máy chủ, chuẩn bị thực thi...")

            # Gửi phản hồi xác nhận
            await self.websocket.send(
                json.dumps(
                    {
                        "type": "server",
                        "status": "success",
                        "message": "Máy chủ đang khởi động lại...",
                        "content": {"action": "restart"},
                    }
                )
            )

            # Thực thi bất đồng bộ thao tác khởi động lại
            def restart_server():
                """Phương thức thực thi khởi động lại"""
                time.sleep(1)
                self.logger.bind(tag=TAG).info("Đang thực thi khởi động lại máy chủ...")
                subprocess.Popen(
                    [sys.executable, "app.py"],
                    stdin=sys.stdin,
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                    start_new_session=True,
                )
                os._exit(0)

            # Dùng luồng thực thi khởi động lại để không block event loop
            threading.Thread(target=restart_server, daemon=True).start()

        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Khởi động lại thất bại: {str(e)}")
            await self.websocket.send(
                json.dumps(
                    {
                        "type": "server",
                        "status": "error",
                        "message": f"Khởi động lại thất bại: {str(e)}",
                        "content": {"action": "restart"},
                    }
                )
            )

    def _initialize_components(self):
        try:
            if self.tts is None:
                self.tts = self._initialize_tts()
            # Mở kênh tổng hợp giọng nói
            asyncio.run_coroutine_threadsafe(
                self.tts.open_audio_channels(self), self.loop
            )
            if self.need_bind:
                self.bind_completed_event.set()
                return
            self.selected_module_str = build_module_string(
                self.config.get("selected_module", {})
            )
            self.logger = create_connection_logger(self.selected_module_str)

            """Khởi tạo các thành phần"""
            if self.config.get("prompt") is not None:
                user_prompt = self.config["prompt"]
                # Khởi tạo bằng prompt nhanh
                prompt = self.prompt_manager.get_quick_prompt(user_prompt)
                self.change_system_prompt(prompt)
                self.logger.bind(tag=TAG).info(
                    f"Khởi tạo nhanh thành phần: prompt thành công {prompt[:50]}..."
                )

            """Khởi tạo các thành phần cục bộ"""
            if self.vad is None:
                self.vad = self._vad
            if self.asr is None:
                self.asr = self._initialize_asr()

            # Khởi tạo nhận dạng giọng nói
            self._initialize_voiceprint()
            # Mở kênh nhận dạng giọng nói
            asyncio.run_coroutine_threadsafe(
                self.asr.open_audio_channels(self), self.loop
            )

            """Tải bộ nhớ"""
            self._initialize_memory()
            """Tải nhận diện ý định"""
            self._initialize_intent()
            """Khởi tạo luồng báo cáo"""
            self._init_report_threads()
            """Cập nhật system prompt"""
            self._init_prompt_enhancement()
            """Chèn ví dụ few-shot gọi công cụ (chỉ chế độ function_call)"""
            self._inject_tool_call_fewshot()

        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Khởi tạo thành phần thất bại: {e}")

    def _init_prompt_enhancement(self):

        # Cập nhật thông tin ngữ cảnh
        self.prompt_manager.update_context_info(self, self.client_ip)
        enhanced_prompt = self.prompt_manager.build_enhanced_prompt(
            self.config["prompt"],
            self.device_id,
            self.client_ip,
            emoji_enabled=(self.features or {}).get("emoji", True),
        )
        if enhanced_prompt:
            self.change_system_prompt(enhanced_prompt)
            self.logger.bind(tag=TAG).debug("System prompt đã được tăng cường và cập nhật")

    def _inject_tool_call_fewshot(self):
        """Chèn ví dụ few-shot gọi công cụ vào lịch sử hội thoại.
        Cấu trúc: mẫu dương (ví dụ gọi công cụ) đặt trước system động để tận dụng prefix cache;
        mẫu âm (ví dụ trả lời trực tiếp) đặt sau system động, sát với tin nhắn người dùng thật,
        để mô hình nhìn thấy hành vi "không gọi công cụ" ngay trước khi xử lý tin nhắn người dùng.
        """
        if self.intent_type != "function_call":
            return
        if not hasattr(self, "func_handler") or self.func_handler is None:
            return

        tools = self.func_handler.get_functions()
        if not tools:
            return

        tool_names = {t.get("function", {}).get("name") for t in tools}

        # === Ví dụ few-shot (is_temporary) ===
        # Hiển thị cách dùng direct_answer với tham số response, hoàn thành phản hồi trong một lần gọi

        # Ví dụ 1: direct_answer (nội dung phản hồi viết trong tham số response, không cần đệ quy)
        da_tc_id = "fewshot_da_001"
        self.dialogue.put(Message(role="user", content="Hãy kể cho tôi nghe một câu chuyện", is_temporary=True))
        self.dialogue.put(Message(
            role="assistant",
            tool_calls=[{
                "id": da_tc_id,
                "function": {"arguments": '{"response": "Tuyệt, bạn muốn nghe loại nào? Cổ tích, phiêu lưu hay hài hước? Chọn một tôi sẽ kể~"}', "name": "direct_answer"},
                "type": "function", "index": 0,
            }],
            is_temporary=True,
        ))
        self.dialogue.put(Message(
            role="tool", tool_call_id=da_tc_id,
            content="Đã phản hồi trực tiếp", is_temporary=True,
        ))

        # Ví dụ 2: Gọi công cụ thật (handle_exit_intent)
        if "handle_exit_intent" in tool_names:
            tc_id = "fewshot_exit_001"
            self.dialogue.put(Message(role="user", content="Tạm biệt", is_temporary=True))
            self.dialogue.put(Message(
                role="assistant",
                tool_calls=[{
                    "id": tc_id,
                    "function": {"arguments": '{"say_goodbye": "Hẹn gặp lại lần sau~"}', "name": "handle_exit_intent"},
                    "type": "function", "index": 0,
                }],
                is_temporary=True,
            ))
            self.dialogue.put(Message(
                role="tool", tool_call_id=tc_id,
                content="Ý định thoát đã được xử lý", is_temporary=True,
            ))
            self.dialogue.put(Message(
                role="assistant", content="Hẹn gặp lại lần sau~", is_temporary=True,
            ))

        self.logger.bind(tag=TAG).debug("Đã tiêm ví dụ few-shot gọi công cụ")

    def _init_report_threads(self):
        """Khởi tạo luồng báo cáo ASR và TTS"""
        if not self.read_config_from_api or self.need_bind:
            return
        if self.chat_history_conf == 0:
            return
        if self.report_thread is None or not self.report_thread.is_alive():
            self.report_thread = threading.Thread(
                target=self._report_worker, daemon=True
            )
            self.report_thread.start()
            self.logger.bind(tag=TAG).info("Luồng báo cáo TTS đã khởi động")

    def _initialize_tts(self):
        """Khởi tạo TTS"""
        tts = None
        if not self.need_bind:
            tts = initialize_tts(self.config)

        if tts is None:
            tts = DefaultTTS(self.config, delete_audio_file=True)

        return tts

    def _initialize_asr(self):
        """Khởi tạo ASR"""
        if (
                self._asr is not None
                and hasattr(self._asr, "interface_type")
                and self._asr.interface_type == InterfaceType.LOCAL
        ):
            # Nếu ASR chung là dịch vụ local thì trả về ngay
            # Vì ASR local một instance có thể được chia sẻ bởi nhiều kết nối
            asr = self._asr
        else:
            # Nếu ASR chung là dịch vụ remote thì khởi tạo instance mới
            # Vì ASR remote, liên quan đến kết nối websocket và luồng nhận, cần mỗi kết nối một instance
            asr = initialize_asr(self.config)

        return asr

    def _initialize_voiceprint(self):
        """Khởi tạo nhận diện giọng nói cho kết nối hiện tại"""
        try:
            voiceprint_config = self.config.get("voiceprint", {})
            if voiceprint_config:
                voiceprint_provider = VoiceprintProvider(voiceprint_config)
                if voiceprint_provider is not None and voiceprint_provider.enabled:
                    self.voiceprint_provider = voiceprint_provider
                    self.logger.bind(tag=TAG).info("Chức năng nhận diện giọng nói đã được bật động khi kết nối")
                else:
                    self.logger.bind(tag=TAG).warning("Chức năng nhận diện giọng nói đã bật nhưng cấu hình chưa đầy đủ")
            else:
                self.logger.bind(tag=TAG).info("Chức năng nhận diện giọng nói chưa được bật")
        except Exception as e:
            self.logger.bind(tag=TAG).warning(f"Khởi tạo nhận diện giọng nói thất bại: {str(e)}")

    async def _background_initialize(self):
        """Khởi tạo cấu hình và thành phần ở nền (không chặn vòng lặp chính)"""
        try:
            # Lấy cấu hình cá thể hóa bất đồng bộ
            await self._initialize_private_config_async()
            # Khởi tạo thành phần trong thread pool
            self.executor.submit(self._initialize_components)
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Khởi tạo nền thất bại: {e}")

    async def _initialize_private_config_async(self):
        """Lấy cấu hình cá thể hóa bất đồng bộ từ API (phiên bản bất đồng bộ, không block main loop)"""
        if not self.read_config_from_api:
            self.need_bind = False
            self.bind_completed_event.set()
            return
        try:
            begin_time = time.time()
            private_config = await get_private_config_from_api(
                self.config,
                self.headers.get("device-id"),
                self.headers.get("client-id", self.headers.get("device-id")),
            )
            private_config["delete_audio"] = bool(self.config.get("delete_audio", True))
            self.logger.bind(tag=TAG).info(
                f"{time.time() - begin_time} giây,Lấy cấu hình cá thể hóa bất đồng bộ thành công: {json.dumps(filter_sensitive_info(private_config), ensure_ascii=False)}"
            )
            self.need_bind = False
            self.bind_completed_event.set()
        except DeviceNotFoundException as e:
            self.need_bind = True
            private_config = {}
        except DeviceBindException as e:
            self.need_bind = True
            self.bind_code = e.bind_code
            private_config = {}
        except Exception as e:
            self.need_bind = True
            self.logger.bind(tag=TAG).error(f"Lấy cấu hình cá thể hóa bất đồng bộ thất bại: {e}")
            private_config = {}

        init_llm, init_tts, init_memory, init_intent = (
            False,
            False,
            False,
            False,
        )

        init_vad = check_vad_update(self.common_config, private_config)
        init_asr = check_asr_update(self.common_config, private_config)

        if init_vad:
            self.config["VAD"] = private_config["VAD"]
            self.config["selected_module"]["VAD"] = private_config["selected_module"][
                "VAD"
            ]
        if init_asr:
            self.config["ASR"] = private_config["ASR"]
            self.config["selected_module"]["ASR"] = private_config["selected_module"][
                "ASR"
            ]
        if private_config.get("TTS", None) is not None:
            init_tts = True
            self.config["TTS"] = private_config["TTS"]
            self.config["selected_module"]["TTS"] = private_config["selected_module"][
                "TTS"
            ]
        if private_config.get("LLM", None) is not None:
            init_llm = True
            self.config["LLM"] = private_config["LLM"]
            self.config["selected_module"]["LLM"] = private_config["selected_module"][
                "LLM"
            ]
        if private_config.get("VLLM", None) is not None:
            self.config["VLLM"] = private_config["VLLM"]
            self.config["selected_module"]["VLLM"] = private_config["selected_module"][
                "VLLM"
            ]
        if private_config.get("Memory", None) is not None:
            init_memory = True
            self.config["Memory"] = private_config["Memory"]
            self.config["selected_module"]["Memory"] = private_config[
                "selected_module"
            ]["Memory"]
        if private_config.get("Intent", None) is not None:
            init_intent = True
            self.config["Intent"] = private_config["Intent"]
            model_intent = private_config.get("selected_module", {}).get("Intent", {})
            self.config["selected_module"]["Intent"] = model_intent
            # Tải cấu hình plugin
            if model_intent != "Intent_nointent":
                plugin_from_server = private_config.get("plugins", {})
                for plugin, config_str in plugin_from_server.items():
                    plugin_from_server[plugin] = json.loads(config_str)
                self.config["plugins"] = plugin_from_server
                self.config["Intent"][self.config["selected_module"]["Intent"]][
                    "functions"
                ] = plugin_from_server.keys()
        if private_config.get("prompt", None) is not None:
            self.config["prompt"] = private_config["prompt"]
        # Lấy thông tin giọng nói
        if private_config.get("voiceprint", None) is not None:
            self.config["voiceprint"] = private_config["voiceprint"]
        if private_config.get("summaryMemory", None) is not None:
            self.config["summaryMemory"] = private_config["summaryMemory"]
        if private_config.get("device_max_output_size", None) is not None:
            self.max_output_size = int(private_config["device_max_output_size"])
        if private_config.get("chat_history_conf", None) is not None:
            self.chat_history_conf = int(private_config["chat_history_conf"])
        if private_config.get("mcp_endpoint", None) is not None:
            self.config["mcp_endpoint"] = private_config["mcp_endpoint"]
        if private_config.get("context_providers", None) is not None:
            self.config["context_providers"] = private_config["context_providers"]

        # Gỡ từ thay thế vào cấu hình module TTS
        if private_config.get("correct_words", None) is not None:
            select_tts_module = self.config["selected_module"]["TTS"]
            self.config["TTS"][select_tts_module]["correct_words"] = private_config[
                "correct_words"
            ]

        # Dùng run_in_executor trong thread pool để chạy initialize_modules, tránh block main loop
        try:
            modules = await self.loop.run_in_executor(
                None,  # Dùng thread pool mặc định
                initialize_modules,
                self.logger,
                private_config,
                init_vad,
                init_asr,
                init_llm,
                init_tts,
                init_memory,
                init_intent,
            )
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Khởi tạo thành phần thất bại: {e}")
            modules = {}
        if modules.get("tts", None) is not None:
            self.tts = modules["tts"]
        if modules.get("vad", None) is not None:
            self.vad = modules["vad"]
        if modules.get("asr", None) is not None:
            self.asr = modules["asr"]
        if modules.get("llm", None) is not None:
            self.llm = modules["llm"]
        if modules.get("intent", None) is not None:
            self.intent = modules["intent"]
        if modules.get("memory", None) is not None:
            self.memory = modules["memory"]

    def _initialize_memory(self):
        if self.memory is None:
            return
        """Khởi tạo module bộ nhớ"""
        self.memory.init_memory(
            role_id=self.device_id,
            llm=self.llm,
            summary_memory=self.config.get("summaryMemory", None),
            save_to_file=not self.read_config_from_api,
        )

        # Lấy cấu hình tóm tắt ký ức
        memory_config = self.config["Memory"]
        memory_type = self.config["Memory"][self.config["selected_module"]["Memory"]][
            "type"
        ]
        # Nếu dùng nomen hoặc mem_report_only thì trả về ngay
        if memory_type == "nomem" or memory_type == "mem_report_only":
            return
        # Dùng chế độ mem_local_short
        elif memory_type == "mem_local_short":
            memory_llm_name = memory_config[self.config["selected_module"]["Memory"]][
                "llm"
            ]
            if memory_llm_name and memory_llm_name in self.config["LLM"]:
                # Nếu cấu hình LLM chuyên dụng thì tạo instance LLM độc lập
                from core.utils import llm as llm_utils

                memory_llm_config = self.config["LLM"][memory_llm_name]
                memory_llm_type = memory_llm_config.get("type", memory_llm_name)
                memory_llm = llm_utils.create_instance(
                    memory_llm_type, memory_llm_config
                )
                self.logger.bind(tag=TAG).info(
                    f"Đã tạo LLM chuyên dụng cho tóm tắt bộ nhớ: {memory_llm_name}, loại: {memory_llm_type}"
                )
                self.memory.set_llm(memory_llm)
            else:
                # Ngược lại dùng LLM chính
                self.memory.set_llm(self.llm)
                self.logger.bind(tag=TAG).info("Dùng LLM chính làm mô hình nhận diện ý định")

    def _initialize_intent(self):
        if self.intent is None:
            return
        self.intent_type = self.config["Intent"][
            self.config["selected_module"]["Intent"]
        ]["type"]
        if self.intent_type == "function_call" or self.intent_type == "intent_llm":
            self.load_function_plugin = True
        """Khởi tạo module nhận diện ý định"""
        # Lấy cấu hình nhận diện ý định
        intent_config = self.config["Intent"]
        intent_type = self.config["Intent"][self.config["selected_module"]["Intent"]][
            "type"
        ]

        # Nếu dùng nointent thì trả về ngay
        if intent_type == "nointent":
            return
        # Dùng chế độ intent_llm
        elif intent_type == "intent_llm":
            intent_llm_name = intent_config[self.config["selected_module"]["Intent"]][
                "llm"
            ]

            if intent_llm_name and intent_llm_name in self.config["LLM"]:
                # Nếu cấu hình LLM chuyên dụng thì tạo instance LLM độc lập
                from core.utils import llm as llm_utils

                intent_llm_config = self.config["LLM"][intent_llm_name]
                intent_llm_type = intent_llm_config.get("type", intent_llm_name)
                intent_llm = llm_utils.create_instance(
                    intent_llm_type, intent_llm_config
                )
                self.logger.bind(tag=TAG).info(
                    f"Đã tạo LLM chuyên dụng cho nhận diện ý định: {intent_llm_name}, loại: {intent_llm_type}"
                )
                self.intent.set_llm(intent_llm)
            else:
                # Ngược lại dùng LLM chính
                self.intent.set_llm(self.llm)
                self.logger.bind(tag=TAG).info("Dùng LLM chính làm mô hình nhận diện ý định")

        """Tải bộ xử lý công cụ thống nhất"""
        self.func_handler = UnifiedToolHandler(self)

        # Khởi tạo bất đồng bộ bộ xử lý công cụ
        if hasattr(self, "loop") and self.loop:
            asyncio.run_coroutine_threadsafe(self.func_handler._initialize(), self.loop)

    def change_system_prompt(self, prompt):
        self.prompt = prompt
        # Cập nhật prompt hệ thống vào ngữ cảnh
        self.dialogue.update_system_message(self.prompt)

    def chat(self, query, depth=0):
        # Lưu sentence_id của tác vụ hiện tại vào biến cục bộ, tránh bị tác vụ mới ghi đè
        current_sentence_id = None

        if query is not None:
            self.logger.bind(tag=TAG).info(f"Mô hình lớn nhận được tin nhắn người dùng: {query}")

        # Tạo mới session ID và gửi yêu cầu FIRST ở tầng cao nhất
        if depth == 0:
            current_sentence_id = str(uuid.uuid4().hex)
            self.sentence_id = current_sentence_id  # Cập nhật thuộc tính chung
            self.dialogue.put(Message(role="user", content=query))
            self.tts.tts_text_queue.put(
                TTSMessageDTO(
                    sentence_id=current_sentence_id,
                    sentence_type=SentenceType.FIRST,
                    content_type=ContentType.ACTION,
                )
            )
        else:
            # Khi gọi đệ quy, sử dụng sentence_id hiện tại
            current_sentence_id = self.sentence_id

        # Đặt độ sâu đệ quy tối đa, tránh vòng lặp vô hạn, có thể điều chỉnh theo nhu cầu thực tế
        MAX_DEPTH = 5
        force_final_answer = False  # Đánh dấu có bắt buộc trả lời cuối cùng không

        if depth >= MAX_DEPTH:
            self.logger.bind(tag=TAG).debug(
                f"Đã đạt độ sâu gọi công cụ tối đa {MAX_DEPTH}, sẽ buộc trả lời dựa trên thông tin hiện có"
            )
            force_final_answer = True
            # Thêm chỉ thị hệ thống, yêu cầu LLM dựa trên thông tin hiện có để trả lời
            self.dialogue.put(
                Message(
                    role="user",
                    content="[Thông báo hệ thống] Đã đạt giới hạn số lần gọi công cụ tối đa, hãy dựa trên toàn bộ thông tin hiện có để trả lời trực tiếp đáp án cuối cùng. Đừng thử gọi thêm bất kỳ công cụ nào nữa.",
                )
            )

        # Define intent functions
        functions = None
        # Khi đạt độ sâu tối đa, vô hiệu hóa gọi công cụ, bắt LLM trả lời trực tiếp
        if (
                self.intent_type == "function_call"
                and hasattr(self, "func_handler")
                and not force_final_answer
        ):
            functions = list(self.func_handler.get_functions())
            # Chỉ tiêm công cụ ảo direct_answer ở tầng gọi đầu tiên
            # Gọi đệ quy (depth>0) không tiêm, tránh mô hình gọi lại direct_answer khi sinh phản hồi văn bản gây vòng lặp
            if functions is not None and depth == 0:
                functions.append(DIRECT_ANSWER_TOOL)

        response_message = []

        try:
            # Dùng hội thoại có ký ức
            memory_str = None
            # Chỉ truy vấn ký ức khi query không rỗng (biểu thị người dùng hỏi)
            if self.memory is not None and query:
                future = asyncio.run_coroutine_threadsafe(
                    self.memory.query_memory(query), self.loop
                )
                memory_str = future.result()

            if self.intent_type == "function_call" and functions is not None:
                # Dùng streaming interface hỗ trợ functions
                llm_responses = self.llm.response_with_functions(
                    self.session_id,
                    self.dialogue.get_llm_dialogue_with_memory(
                        memory_str, self.config.get("voiceprint", {})
                    ),
                    functions=functions,
                )
            else:
                llm_responses = self.llm.response(
                    self.session_id,
                    self.dialogue.get_llm_dialogue_with_memory(
                        memory_str, self.config.get("voiceprint", {})
                    ),
                )
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"LLM xử lý lỗi {query}: {e}")
            return None

        # Xử lý phản hồi streaming
        tool_call_flag = False
        # Hỗ trợ nhiều lần gọi công cụ song song - dùng list lưu trữ
        tool_calls_list = []  # Định dạng: [{"id": "", "name": "", "arguments": ""}]
        content_arguments = ""
        emotion_flag = True
        try:
            for response in llm_responses:
                if self.client_abort:
                    break
                if self.intent_type == "function_call" and functions is not None:
                    content, tools_call = response
                    if "content" in response:
                        content = response["content"]
                        tools_call = None
                    if content is not None and len(content) > 0:
                        content_arguments += content

                    if not tool_call_flag and content_arguments.startswith("<tool_call>"):
                        # print("content_arguments", content_arguments)
                        tool_call_flag = True

                    if tools_call is not None and len(tools_call) > 0:
                        tool_call_flag = True
                        self._merge_tool_calls(tool_calls_list, tools_call)

                    # Streaming trích xuất tham số response của direct_answer, gửi TTS theo thời gian thực
                    # Dùng buffer an toàn, ngăn ký hiệu đóng JSON rò rỉ sang TTS
                    _DA_STREAM_BUFFER = 5
                    for tc in tool_calls_list:
                        if tc["name"] == "direct_answer" and tc.get("arguments"):
                            da_text = self._extract_direct_answer_response(tc["arguments"])
                            sent_len = tc.get("_da_sent", 0)
                            if da_text and len(da_text) > sent_len:
                                safe_end = max(sent_len, len(da_text) - _DA_STREAM_BUFFER)
                                if safe_end > sent_len:
                                    new_part = da_text[sent_len:safe_end]
                                    # Dọn dẹp ký hiệu đóng JSON rò rỉ trong delta
                                    new_part = self._clean_response_garbage(new_part)
                                    if new_part:
                                        tc["_da_sent"] = safe_end
                                        self.tts.tts_text_queue.put(
                                            TTSMessageDTO(
                                                sentence_id=current_sentence_id,
                                                sentence_type=SentenceType.MIDDLE,
                                                content_type=ContentType.TEXT,
                                                content_detail=new_part,
                                            )
                                        )
                else:
                    content = response

                # Lấy emoji cảm xúc từ phản hồi LLM, mỗi vòng hội thoại chỉ lấy một lần ở đầu
                if emotion_flag and content is not None and content.strip():
                    if (self.features or {}).get("emoji", True):
                        asyncio.run_coroutine_threadsafe(
                            textUtils.get_emotion(self, content),
                            self.loop,
                        )
                    emotion_flag = False

                if content is not None and len(content) > 0:
                    if not tool_call_flag:
                        response_message.append(content)
                        self.tts.tts_text_queue.put(
                            TTSMessageDTO(
                                sentence_id=current_sentence_id,
                                sentence_type=SentenceType.MIDDLE,
                                content_type=ContentType.TEXT,
                                content_detail=content,
                            )
                        )
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"LLM stream processing error: {e}")
            self.tts.tts_text_queue.put(
                TTSMessageDTO(
                    sentence_id=current_sentence_id,
                    sentence_type=SentenceType.MIDDLE,
                    content_type=ContentType.TEXT,
                    content_detail=get_system_error_response(self.config),
                )
            )
            if depth == 0:
                self.tts.tts_text_queue.put(
                    TTSMessageDTO(
                        sentence_id=current_sentence_id,
                        sentence_type=SentenceType.LAST,
                        content_type=ContentType.ACTION,
                    )
                )
            return
        # Xử lý function call
        if tool_call_flag:
            bHasError = False
            # Xử lý định dạng gọi công cụ dựa trên văn bản
            if len(tool_calls_list) == 0 and content_arguments:
                a = extract_json_from_string(content_arguments)
                if a is not None:
                    try:
                        content_arguments_json = json.loads(a)
                        tool_calls_list.append(
                            {
                                "id": str(uuid.uuid4().hex),
                                "name": content_arguments_json["name"],
                                "arguments": json.dumps(
                                    content_arguments_json["arguments"],
                                    ensure_ascii=False,
                                ),
                            }
                        )
                    except Exception as e:
                        bHasError = True
                        response_message.append(a)
                else:
                    bHasError = True
                    response_message.append(content_arguments)
                if bHasError:
                    self.logger.bind(tag=TAG).error(
                        f"Lỗi function call: {content_arguments}"
                    )

            if not bHasError and len(tool_calls_list) > 0:
                # Xử lý công cụ ảo direct_answer
                direct_answer_calls = [tc for tc in tool_calls_list if tc["name"] == "direct_answer"]
                real_tool_calls = [tc for tc in tool_calls_list if tc["name"] != "direct_answer"]

                if direct_answer_calls:
                    self.logger.bind(tag=TAG).debug(
                        f"Mô hình chọn direct_answer, đã phát luồng và ghi vào lịch sử hội thoại"
                    )
                    for tc in direct_answer_calls:
                        da_response = self._extract_direct_answer_response(tc.get("arguments", "{}"))
                        if da_response:
                            # Làm mới phần chưa gửi trong buffer streaming
                            sent_len = tc.get("_da_sent", 0)
                            remaining = da_response[sent_len:]
                            if remaining:
                                remaining = self._clean_response_garbage(remaining)
                                if remaining:
                                    self.tts.tts_text_queue.put(
                                        TTSMessageDTO(
                                            sentence_id=current_sentence_id,
                                            sentence_type=SentenceType.MIDDLE,
                                            content_type=ContentType.TEXT,
                                            content_detail=remaining,
                                        )
                                    )
                            # Ghi vào lịch sử hội thoại
                            da_response = self._clean_response_garbage(da_response)
                            self.tts.store_tts_text(current_sentence_id, da_response)
                            self.dialogue.put(Message(role="assistant", content=da_response))

                    if not real_tool_calls:
                        if depth == 0:
                            self.tts.tts_text_queue.put(
                                TTSMessageDTO(
                                    sentence_id=current_sentence_id,
                                    sentence_type=SentenceType.LAST,
                                    content_type=ContentType.ACTION,
                                )
                            )
                        return

                    tool_calls_list = real_tool_calls

            if not bHasError and len(tool_calls_list) > 0:
                self.logger.bind(tag=TAG).debug(
                    f"Phát hiện {len(tool_calls_list)} lần gọi công cụ"
                )

                # Văn bản đã phát trong giai đoạn streaming của LLM
                streamed_text = ""
                if len(response_message) > 0:
                    streamed_text = "".join(response_message)
                    self.tts.store_tts_text(current_sentence_id, streamed_text)
                    self.dialogue.put(Message(role="assistant", content=streamed_text))
                response_message.clear()

                # Thu thập Future của tất cả lời gọi công cụ
                futures_with_data = []
                for tool_call_data in tool_calls_list:
                    self.logger.bind(tag=TAG).debug(
                        f"function_name={tool_call_data['name']}, function_id={tool_call_data['id']}, function_arguments={tool_call_data['arguments']}"
                    )

                    # Dùng phương pháp chung báo cáo lời gọi công cụ
                    tool_input = json.loads(tool_call_data.get("arguments") or "{}")
                    enqueue_tool_report(self, tool_call_data['name'], tool_input)

                    future = asyncio.run_coroutine_threadsafe(
                        self.func_handler.handle_llm_function_call(
                            self, tool_call_data
                        ),
                        self.loop,
                    )
                    futures_with_data.append((future, tool_call_data, tool_input))

                # Thời gian quá hạn gọi công cụ, có thể cấu hình, mặc định 30 giây
                tool_call_timeout = int(self.config.get("tool_call_timeout", 30))
                # Đợi coroutine kết thúc (thời gian chờ thực tế là cái chậm nhất)
                tool_results = []

                for future, tool_call_data, tool_input in futures_with_data:
                    try:
                        result = future.result(timeout=tool_call_timeout)
                        tool_results.append((result, tool_call_data))
                        # Dùng phương pháp chung báo cáo kết quả gọi công cụ
                        enqueue_tool_report(self, tool_call_data['name'], tool_input, str(result.result) if result.result else None, report_tool_call=False)

                    except Exception as e:
                        self.logger.bind(tag=TAG).error(
                            f"Gọi công cụ bị quá thời gian hoặc lỗi: {tool_call_data['name']}, lỗi: {e}"
                        )
                        # Khi quá hạn thì trả về phản hồi lỗi, tránh block toàn bộ quy trình
                        tool_results.append((
                            ActionResponse(action=Action.ERROR, result="Ồ, mạng đang gặp chút vấn đề, vui lòng thử lại sau!"),
                            tool_call_data
                        ))
                        # Báo cáo lỗi gọi công cụ
                        enqueue_tool_report(self, tool_call_data['name'], tool_input, str(e), report_tool_call=False)

                # Xử lý thống nhất kết quả gọi công cụ
                if tool_results:
                    self._handle_function_result(tool_results, depth=depth, streamed_text=streamed_text)

        # Lưu trữ nội dung hội thoại
        if len(response_message) > 0:
            text_buff = "".join(response_message)
            self.tts.store_tts_text(current_sentence_id, text_buff)
            self.dialogue.put(Message(role="assistant", content=text_buff))

        if depth == 0:
            self.tts.tts_text_queue.put(
                TTSMessageDTO(
                    sentence_id=current_sentence_id,
                    sentence_type=SentenceType.LAST,
                    content_type=ContentType.ACTION,
                )
            )
            # Dùng lambda tính toán trễ, chỉ thực thi get_llm_dialogue() khi level DEBUG
            self.logger.bind(tag=TAG).debug(
                lambda: json.dumps(
                    self.dialogue.get_llm_dialogue(), indent=4, ensure_ascii=False
                )
            )

        return True

    def _handle_function_result(self, tool_results, depth, streamed_text=""):
        need_llm_tools = []
        record_tools = []

        for result, tool_call_data in tool_results:
            if result.action in [
                Action.RESPONSE,
                Action.NOTFOUND,
                Action.ERROR,
            ]:
                text = result.response if result.response else result.result
                if streamed_text and text in streamed_text:
                    self.logger.bind(tag=TAG).debug(
                        f"Bỏ qua TTS trùng lặp cho công cụ {tool_call_data['name']}, đã phát luồng rồi"
                    )
                else:
                    self.tts.tts_one_sentence(self, ContentType.TEXT, content_detail=text)
                    self.tts.store_tts_text(self.sentence_id, text)
                self.dialogue.put(Message(role="assistant", content=text))
            elif result.action == Action.REQLLM:
                need_llm_tools.append((result, tool_call_data))
            elif result.action == Action.RECORD:
                record_tools.append((result, tool_call_data))
            else:
                pass

        # Action.RECORD: ghi chuỗi gọi công cụ đầy đủ (assistant(tool_calls) → tool(result) → assistant(response))
        # Mô hình học từ lịch sử pattern gọi công cụ, không gọi thêm LLM
        if record_tools:
            # Tạo tin nhắn assistant (chứa tool_calls), ghi lại "mô hình gọi các công cụ"
            all_tool_calls = [
                {
                    "id": tool_call_data["id"],
                    "function": {
                        "arguments": (
                            "{}"
                            if tool_call_data["arguments"] == ""
                            else tool_call_data["arguments"]
                        ),
                        "name": tool_call_data["name"],
                    },
                    "type": "function",
                    "index": idx,
                }
                for idx, (_, tool_call_data) in enumerate(record_tools)
            ]
            self.dialogue.put(Message(role="assistant", tool_calls=all_tool_calls))

            # Ghi kết quả thực thi mỗi công cụ, ghi lại "công cụ trả về gì"
            for result, tool_call_data in record_tools:
                text = result.result or ""
                self.dialogue.put(
                    Message(
                        role="tool",
                        tool_call_id=(
                            str(uuid.uuid4())
                            if tool_call_data["id"] is None
                            else tool_call_data["id"]
                        ),
                        content=text,
                    )
                )

            # Dùng văn bản cố định làm phản hồi cuối, bổ sung dạng 3 phần chuẩn, đảm bảo tin nhắn tiếp theo là user chứ không phải tool
            response_parts = []
            for result, _ in record_tools:
                resp = result.response or result.result
                if resp:
                    response_parts.append(resp)
            if response_parts:
                self.dialogue.put(Message(role="assistant", content="，".join(response_parts)))

        if need_llm_tools:
            all_tool_calls = [
                {
                    "id": tool_call_data["id"],
                    "function": {
                        "arguments": (
                            "{}"
                            if tool_call_data["arguments"] == ""
                            else tool_call_data["arguments"]
                        ),
                        "name": tool_call_data["name"],
                    },
                    "type": "function",
                    "index": idx,
                }
                for idx, (_, tool_call_data) in enumerate(need_llm_tools)
            ]
            self.dialogue.put(Message(role="assistant", tool_calls=all_tool_calls))

            for result, tool_call_data in need_llm_tools:
                text = result.result
                if text is not None and len(text) > 0:
                    self.dialogue.put(
                        Message(
                            role="tool",
                            tool_call_id=(
                                str(uuid.uuid4())
                                if tool_call_data["id"] is None
                                else tool_call_data["id"]
                            ),
                            content=text,
                        )
                    )

            self.chat(None, depth=depth + 1)

    def _report_worker(self):
        """Luồng làm việc báo cáo lịch sử trò chuyện"""
        while not self.stop_event.is_set():
            try:
                # Lấy dữ liệu từ queue, đặt timeout để kiểm tra stop event định kỳ
                item = self.report_queue.get(timeout=1)
                if item is None:  # Kiểm tra đối tượng poison pill
                    break
                try:
                    # Kiểm tra trạng thái thread pool
                    if self.executor is None:
                        continue
                    # Gửi task đến thread pool
                    self.executor.submit(self._process_report, *item)
                except Exception as e:
                    self.logger.bind(tag=TAG).error(f"Luồng báo cáo lịch sử trò chuyện gặp lỗi: {e}")
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.bind(tag=TAG).error(f"Luồng làm việc báo cáo lịch sử trò chuyện gặp lỗi: {e}")

        self.logger.bind(tag=TAG).info("Luồng báo cáo lịch sử trò chuyện đã thoát")

    def _process_report(self, type, text, audio_data, report_time):
        """Xử lý tác vụ báo cáo"""
        try:
            # Thực thi báo cáo bất đồng bộ (chạy trong event loop)
            asyncio.run(report(self, type, text, audio_data, report_time))
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Xử lý báo cáo gặp lỗi: {e}")
        finally:
            # Đánh dấu task hoàn thành
            self.report_queue.task_done()

    def clearSpeakStatus(self):
        self.client_is_speaking = False
        self.logger.bind(tag=TAG).debug("Xóa trạng thái nói của máy chủ")

    async def close(self, ws=None):
        """Phương thức dọn dẹp tài nguyên"""
        try:
            # Dọn dẹp tài nguyên kết nối VAD
            if (
                    hasattr(self, "vad")
                    and self.vad
                    and hasattr(self.vad, "release_conn_resources")
            ):
                self.vad.release_conn_resources(self)

            # Dọn dẹp buffer âm thanh
            if hasattr(self, "audio_buffer"):
                self.audio_buffer.clear()

            # Hủy task timeout
            if self.timeout_task and not self.timeout_task.done():
                self.timeout_task.cancel()
                try:
                    await self.timeout_task
                except asyncio.CancelledError:
                    pass
                self.timeout_task = None

            # Dọn dẹp tài nguyên bộ xử lý công cụ
            if hasattr(self, "func_handler") and self.func_handler:
                try:
                    await self.func_handler.cleanup()
                except Exception as cleanup_error:
                    self.logger.bind(tag=TAG).error(
                        f"Lỗi khi dọn dẹp bộ xử lý công cụ: {cleanup_error}"
                    )

            # Kích hoạt stop event
            if self.stop_event:
                self.stop_event.set()

            # Xóa queue task
            self.clear_queues()

            # Đóng kết nối WebSocket
            try:
                if ws:
                    # Kiểm tra an toàn trạng thái WebSocket rồi đóng
                    try:
                        if hasattr(ws, "closed") and not ws.closed:
                            await ws.close()
                        elif hasattr(ws, "state") and ws.state.name != "CLOSED":
                            await ws.close()
                        else:
                            # Nếu không có thuộc tính closed thì thử đóng trực tiếp
                            await ws.close()
                    except Exception:
                        # Nếu đóng thất bại thì bỏ qua lỗi
                        pass
                elif self.websocket:
                    try:
                        if (
                                hasattr(self.websocket, "closed")
                                and not self.websocket.closed
                        ):
                            await self.websocket.close()
                        elif (
                                hasattr(self.websocket, "state")
                                and self.websocket.state.name != "CLOSED"
                        ):
                            await self.websocket.close()
                        else:
                            # Nếu không có thuộc tính closed thì thử đóng trực tiếp
                            await self.websocket.close()
                    except Exception:
                        # Nếu đóng thất bại thì bỏ qua lỗi
                        pass
            except Exception as ws_error:
                self.logger.bind(tag=TAG).error(f"Lỗi khi đóng kết nối WebSocket: {ws_error}")

            if self.tts:
                await self.tts.close()
            if self.asr:
                await self.asr.close()

            # Đóng thread pool cuối cùng (tránh block)
            if self.executor:
                try:
                    self.executor.shutdown(wait=False)
                except Exception as executor_error:
                    self.logger.bind(tag=TAG).error(
                        f"Lỗi khi đóng thread pool: {executor_error}"
                    )
                self.executor = None
            self.logger.bind(tag=TAG).info("Tài nguyên kết nối đã được giải phóng")
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Lỗi khi đóng kết nối: {e}")
        finally:
            # Đảm bảo stop event được đặt
            if self.stop_event:
                self.stop_event.set()

    def clear_queues(self):
        """Xóa toàn bộ hàng đợi tác vụ"""
        if self.tts:
            self.logger.bind(tag=TAG).debug(
                f"Bắt đầu dọn dẹp: kích thước hàng đợi TTS={self.tts.tts_text_queue.qsize()}, kích thước hàng đợi âm thanh={self.tts.tts_audio_queue.qsize()}"
            )

            # Sử dụng cách không block để xóa queue
            for q in [
                self.tts.tts_text_queue,
                self.tts.tts_audio_queue,
                self.report_queue,
            ]:
                if not q:
                    continue
                while True:
                    try:
                        q.get_nowait()
                    except queue.Empty:
                        break

            # Đặt lại bộ điều khiển luồng âm thanh (hủy task background và xóa queue)
            if hasattr(self, "audio_rate_controller") and self.audio_rate_controller:
                self.audio_rate_controller.reset()
                self.logger.bind(tag=TAG).debug("Đã đặt lại bộ điều tiết luồng âm thanh")

            self.logger.bind(tag=TAG).debug(
                f"Kết thúc dọn dẹp: kích thước hàng đợi TTS={self.tts.tts_text_queue.qsize()}, kích thước hàng đợi âm thanh={self.tts.tts_audio_queue.qsize()}"
            )

    def reset_audio_states(self):
        """
        Đặt lại toàn bộ trạng thái liên quan đến âm thanh (VAD + ASR)
        """
        # Reset VAD states
        self.client_audio_buffer.clear()
        self.client_have_voice = False
        self.client_voice_stop = False
        self.client_voice_window.clear()
        self.last_is_voice = False
        self.vad_last_voice_time = 0.0

        # Clear ASR buffers
        self.asr_audio.clear()

        self.logger.bind(tag=TAG).debug("Đã đặt lại toàn bộ trạng thái âm thanh.")

    def chat_and_close(self, text):
        """Trò chuyện với người dùng rồi đóng kết nối"""
        try:
            # Use the existing chat method
            self.chat(text)

            # After chat is complete, close the connection
            self.close_after_chat = True
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Lỗi chat và đóng: {str(e)}")

    async def _check_timeout(self):
        """Kiểm tra hết thời gian kết nối"""
        try:
            while not self.stop_event.is_set():
                last_activity_time = self.last_activity_time
                if self.need_bind:
                    last_activity_time = self.first_activity_time

                # Kiểm tra quá hạn (chỉ khi nhãn thời gian đã khởi tạo)
                if last_activity_time > 0.0:
                    current_time = time.time() * 1000
                    if current_time - last_activity_time > self.timeout_seconds * 1000:
                        if not self.stop_event.is_set():
                            self.logger.bind(tag=TAG).info("Kết nối đã hết thời gian, chuẩn bị đóng")
                            # Đặt stop event, ngăn xử lý trùng
                            self.stop_event.set()
                            # Dùng try-except bao quanh thao tác đóng, đảm bảo không block vì exception
                            try:
                                await self.close(self.websocket)
                            except Exception as close_error:
                                self.logger.bind(tag=TAG).error(
                                    f"Lỗi khi đóng kết nối do hết thời gian: {close_error}"
                                )
                        break
                # Kiểm tra mỗi 10 giây, tránh quá thường xuyên
                await asyncio.sleep(10)
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Tác vụ kiểm tra hết thời gian gặp lỗi: {e}")
        finally:
            self.logger.bind(tag=TAG).info("Tác vụ kiểm tra hết thời gian đã thoát")

    @staticmethod
    def _extract_direct_answer_response(arguments_str):
        """Trích xuất giá trị response từ tham số của direct_answer.
        Ưu tiên dùng json.loads tiêu chuẩn, giai đoạn streaming thì fallback sang trích xuất chuỗi.
        """
        if not arguments_str:
            return ""
        # Ưu tiên thử phân tích JSON tiêu chuẩn (áp dụng cho JSON đầy đủ và đúng định dạng)
        try:
            data = json.loads(arguments_str)
            if isinstance(data, dict) and "response" in data:
                return data["response"]
        except (json.JSONDecodeError, TypeError):
            pass
        # Fallback: giai đoạn streaming JSON có thể không đầy đủ, dùng trích xuất chuỗi
        marker = '"response": "'
        idx = arguments_str.find(marker)
        if idx < 0:
            marker = '"response":"'
            idx = arguments_str.find(marker)
        if idx < 0:
            return ""
        start = idx + len(marker)
        raw = arguments_str[start:]
        # Bỏ ký hiệu đóng JSON ở cuối (nếu đã đầy đủ)
        if raw.endswith('"}'):
            raw = raw[:-2]
        elif raw.endswith('"'):
            raw = raw[:-1]
        # Xử lý escape JSON
        raw = raw.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')
        return raw

    @staticmethod
    def _clean_response_garbage(text):
        """Dọn dẹp ký hiệu đóng JSON có thể rò rỉ trong response.
        Mô hình đôi khi sinh ký hiệu đóng JSON trong nội dung response (như "))}}" hoặc "\'}}"),
        Đây không phải phần nội dung câu chuyện, cần loại bỏ.
        """
        if not text:
            return text
        # Dọn dẹp ký hiệu đóng JSON dòng riêng (như "))}}" "\'}}" "}}" }}" } )
        _garbage_chars = frozenset('")\'}）')
        lines = text.split('\n')
        cleaned = []
        for line in lines:
            stripped = line.strip()
            if stripped and len(stripped) <= 8 and all(c in _garbage_chars for c in stripped):
                continue
            cleaned.append(line)
        result = '\n'.join(cleaned)
        # Dọn dẹp ký hiệu đóng JSON còn sót ở cuối
        result = re.sub(r'["\'}\]]+$', '', result.rstrip()).rstrip()
        return result

    def _merge_tool_calls(self, tool_calls_list, tools_call):
        """Hợp nhất danh sách gọi công cụ

        Args:
            tool_calls_list: danh sách gọi công cụ đã thu thập
            tools_call: lời gọi công cụ mới
        """
        for tool_call in tools_call:
            tool_index = getattr(tool_call, "index", None)
            if tool_index is None:
                if tool_call.function.name:
                    # Có function_name, biểu thị là lời gọi công cụ mới
                    tool_index = len(tool_calls_list)
                else:
                    tool_index = len(tool_calls_list) - 1 if tool_calls_list else 0

            # Đảm bảo danh sách có đủ vị trí
            if tool_index >= len(tool_calls_list):
                tool_calls_list.append({"id": "", "name": "", "arguments": ""})

            # Cập nhật thông tin gọi công cụ
            if tool_call.id:
                tool_calls_list[tool_index]["id"] = tool_call.id
            if tool_call.function.name:
                tool_calls_list[tool_index]["name"] = tool_call.function.name
            if tool_call.function.arguments:
                tool_calls_list[tool_index]["arguments"] += tool_call.function.arguments
