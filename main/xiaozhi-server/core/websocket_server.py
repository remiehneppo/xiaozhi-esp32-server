import asyncio
import logging

import websockets
from config.logger import setup_logging


class SuppressInvalidHandshakeFilter(logging.Filter):
    """Lọc log lỗi bắt tay không hợp lệ (ví dụ truy cập HTTPS vào cổng WS)"""

    def filter(self, record):
        msg = record.getMessage()
        suppress_keywords = [
            "opening handshake failed",
            "did not receive a valid HTTP request",
            "connection closed while reading HTTP request",
            "line without CRLF",
        ]
        return not any(keyword in msg for keyword in suppress_keywords)


def _setup_websockets_logger():
    """Cấu hình toàn bộ logger liên quan đến websockets, lọc lỗi bắt tay không hợp lệ"""
    filter_instance = SuppressInvalidHandshakeFilter()
    for logger_name in ["websockets", "websockets.server", "websockets.client"]:
        logger = logging.getLogger(logger_name)
        logger.addFilter(filter_instance)


_setup_websockets_logger()


from core.connection import ConnectionHandler
from config.config_loader import get_config_from_api_async
from core.auth import AuthManager, AuthenticationError
from core.utils.modules_initialize import initialize_modules
from core.utils.util import check_vad_update, check_asr_update

TAG = __name__


class WebSocketServer:
    def __init__(self, config: dict):
        self.config = config
        self.logger = setup_logging()
        self.config_lock = asyncio.Lock()
        modules = initialize_modules(
            self.logger,
            self.config,
            "VAD" in self.config["selected_module"],
            "ASR" in self.config["selected_module"],
            "LLM" in self.config["selected_module"],
            False,
            "Memory" in self.config["selected_module"],
            "Intent" in self.config["selected_module"],
        )
        self._vad = modules["vad"] if "vad" in modules else None
        self._asr = modules["asr"] if "asr" in modules else None
        self._llm = modules["llm"] if "llm" in modules else None
        self._intent = modules["intent"] if "intent" in modules else None
        self._memory = modules["memory"] if "memory" in modules else None

        auth_config = self.config["server"].get("auth", {})
        self.auth_enable = auth_config.get("enabled", False)
        # 
        self.allowed_devices = set(auth_config.get("allowed_devices", []))
        secret_key = self.config["server"]["auth_key"]
        expire_seconds = auth_config.get("expire_seconds", None)
        self.auth = AuthManager(secret_key=secret_key, expire_seconds=expire_seconds)

    async def start(self):
        server_config = self.config["server"]
        host = server_config.get("ip", "0.0.0.0")
        port = int(server_config.get("port", 8000))

        async with websockets.serve(
            self._handle_connection, host, port, process_request=self._http_response
        ):
            await asyncio.Future()

    async def _handle_connection(self, websocket: websockets.ServerConnection):
        headers = dict(websocket.request.headers)
        if headers.get("device-id", None) is None:
            # thử URL tham sốtronglấy device-id
            from urllib.parse import parse_qs, urlparse

            #  WebSocket yêu cầutronglấyđường dẫn
            request_path = websocket.request.path
            if not request_path:
                self.logger.bind(tag=TAG).error("Không thể lấy đường dẫn yêu cầu")
                await websocket.close()
                return
            parsed_url = urlparse(request_path)
            query_params = parse_qs(parsed_url.query)
            if "device-id" not in query_params:
                await websocket.send("Cổng hoạt động bình thường, nếu muốn kiểm tra kết nối hãy khởi động digital-human")
                await websocket.close()
                return
            else:
                websocket.request.headers["device-id"] = query_params["device-id"][0]
            if "client-id" in query_params:
                websocket.request.headers["client-id"] = query_params["client-id"][0]
            if "authorization" in query_params:
                websocket.request.headers["authorization"] = query_params[
                    "authorization"
                ][0]

        """xử lýkết nối，lầntạoConnectionHandler"""
        # xác thực，saukết nối
        try:
            await self._handle_auth(websocket)
        except AuthenticationError:
            await websocket.send("Xác thực thất bại")
            await websocket.close()
            return
        # tạoConnectionHandlerthờivàohiện tạiserver
        handler = ConnectionHandler(
            self.config,
            self._vad,
            self._asr,
            self._llm,
            self._memory,
            self._intent,
            self,  # vàoserver
        )
        try:
            await handler.handle_connection(websocket)
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Lỗi khi xử lý kết nối: {e}")
        finally:
            # đóngkết nối（nhưcũngkhông cóđóng）
            try:
                # Kiểm tra an toàn trạng thái WebSocket rồi đóng
                if hasattr(websocket, "closed") and not websocket.closed:
                    await websocket.close()
                elif hasattr(websocket, "state") and websocket.state.name != "CLOSED":
                    await websocket.close()
                else:
                    # Nếu không có thuộc tính closed thì thử đóng trực tiếp
                    await websocket.close()
            except Exception as close_error:
                self.logger.bind(tag=TAG).error(
                    f"Lỗi khi máy chủ buộc đóng kết nối: {close_error}"
                )

    async def _http_response(self, websocket, request_headers):
        # kiểm tracócho WebSocket yêu cầu
        if request_headers.headers.get("connection", "").lower() == "upgrade":
            # như WebSocket yêu cầu，trả về None tiếp tục
            return None
        else:
            # Nếu là yêu cầu HTTP bình thường, trả về "máy chủ đang chạy"
            return websocket.respond(200, "Máy chủ đang chạy\n")

    async def update_config(self) -> bool:
        """cập nhậtmáy chủcấu hìnhvàkhởi tạo

        Returns:
            bool: cập nhậtcóthành công
        """
        try:
            async with self.config_lock:
                # lấycấu hình（làm chosử dụng）
                new_config = await get_config_from_api_async(self.config)
                if new_config is None:
                    self.logger.bind(tag=TAG).error("Không lấy được cấu hình mới")
                    return False
                self.logger.bind(tag=TAG).info("Lấy cấu hình mới thành công")
                # kiểm tra VAD và ASR cócầncập nhật
                update_vad = check_vad_update(self.config, new_config)
                update_asr = check_asr_update(self.config, new_config)
                self.logger.bind(tag=TAG).info(
                    f"Kiểm tra VAD và ASR có cần cập nhật không: {update_vad} {update_asr}"
                )
                # cập nhậtcấu hình
                self.config = new_config
                # khởi tạo
                modules = initialize_modules(
                    self.logger,
                    new_config,
                    update_vad,
                    update_asr,
                    "LLM" in new_config["selected_module"],
                    False,
                    "Memory" in new_config["selected_module"],
                    "Intent" in new_config["selected_module"],
                )

                # cập nhật
                if "vad" in modules:
                    self._vad = modules["vad"]
                if "asr" in modules:
                    self._asr = modules["asr"]
                if "llm" in modules:
                    self._llm = modules["llm"]
                if "intent" in modules:
                    self._intent = modules["intent"]
                if "memory" in modules:
                    self._memory = modules["memory"]
                self.logger.bind(tag=TAG).info("Tác vụ cập nhật cấu hình đã hoàn tất")
                return True
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Cập nhật cấu hình máy chủ thất bại: {str(e)}")
            return False

    async def _handle_auth(self, websocket: websockets.ServerConnection):
        # xác thực，saukết nối
        if self.auth_enable:
            headers = dict(websocket.request.headers)
            device_id = headers.get("device-id", None)
            client_id = headers.get("client-id", None)
            if self.allowed_devices and device_id in self.allowed_devices:
                # nhưtạitrong，khôngkiểm tratoken，
                return
            else:
                # kiểm tratoken
                token = headers.get("authorization", "")
                if token.startswith("Bearer "):
                    token = token[7:]  # loại bỏ'Bearer 'tiền tố
                else:
                    raise AuthenticationError("Thiếu hoặc không hợp lệ header Authorization")
                # tiến hànhxác thực
                auth_success = self.auth.verify_token(
                    token, client_id=client_id, username=device_id
                )
                if not auth_success:
                    raise AuthenticationError("Token không hợp lệ")
