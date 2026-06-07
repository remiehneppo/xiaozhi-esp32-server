import json
import copy
from aiohttp import web
from config.logger import setup_logging
from core.api.base_handler import BaseHandler
from core.utils.util import get_vision_url, is_valid_image_file
from core.utils.vllm import create_instance
from config.config_loader import get_private_config_from_api
from core.utils.auth import AuthToken
import base64
from typing import Tuple, Optional
from plugins_func.register import Action

TAG = __name__

# 设置最大文件大小为5MB
MAX_FILE_SIZE = 5 * 1024 * 1024


class VisionHandler(BaseHandler):
    def __init__(self, config: dict):
        super().__init__(config)
        # 初始化认证工具
        self.auth = AuthToken(config["server"]["auth_key"])

    def _create_error_response(self, message: str) -> dict:
        """Tạo định dạng phản hồi lỗi thống nhất"""
        return {"success": False, "message": message}

    def _verify_auth_token(self, request) -> Tuple[bool, Optional[str]]:
        """Xác thực token"""
        # Chế độ kiểm thử: cho phép token thử nghiệm hoặc bỏ qua kiểm tra
        auth_header = request.headers.get("Authorization", "")
        client_id = request.headers.get("Client-Id", "")

        # Cho phép client thử nghiệm bỏ qua xác thực
        if client_id == "web_test_client":
            device_id = request.headers.get("Device-Id", "test_device")
            return True, device_id

        if not auth_header.startswith("Bearer "):
            return False, None

        token = auth_header[7:]  # 移除"Bearer "前缀
        return self.auth.verify_token(token)

    async def handle_post(self, request):
        """Xử lý yêu cầu POST của MCP Vision"""
        response = None  # 初始化response变量
        try:
            # 验证token
            is_valid, token_device_id = self._verify_auth_token(request)
            if not is_valid:
                response = web.Response(
                    text=json.dumps(
                        self._create_error_response("Token xác thực không hợp lệ hoặc đã hết hạn")
                    ),
                    content_type="application/json",
                    status=401,
                )
                return response

            # 获取请求头信息
            device_id = request.headers.get("Device-Id", "")
            client_id = request.headers.get("Client-Id", "")
            if device_id != token_device_id:
                raise ValueError("Device ID không khớp với token")
            # Phân tích yêu cầu multipart/form-data
            reader = await request.multipart()

            # Đọc trường question
            question_field = await reader.next()
            if question_field is None:
                raise ValueError("Thiếu trường câu hỏi")
            question = await question_field.text()
            self.logger.bind(tag=TAG).debug(f"Câu hỏi: {question}")

            # Đọc file ảnh
            image_field = await reader.next()
            if image_field is None:
                raise ValueError("Thiếu file ảnh")

            # Đọc dữ liệu ảnh
            image_data = await image_field.read()
            if not image_data:
                raise ValueError("Dữ liệu ảnh trống")

            # Kiểm tra kích thước file
            if len(image_data) > MAX_FILE_SIZE:
                raise ValueError(
                    f"Kích thước ảnh vượt giới hạn, tối đa cho phép {MAX_FILE_SIZE/1024/1024}MB"
                )

            # Kiểm tra định dạng file
            if not is_valid_image_file(image_data):
                raise ValueError(
                    "Định dạng file không được hỗ trợ, hãy tải lên ảnh hợp lệ (hỗ trợ JPEG, PNG, GIF, BMP, TIFF, WEBP)"
                )

            # Chuyển ảnh sang base64
            image_base64 = base64.b64encode(image_data).decode("utf-8")

            # Nếu bật chế độ đọc cấu hình từ API thì lấy cấu hình mô hình từ đó
            current_config = copy.deepcopy(self.config)
            read_config_from_api = current_config.get("read_config_from_api", False)
            if read_config_from_api:
                current_config = await get_private_config_from_api(
                    current_config,
                    device_id,
                    client_id,
                )

            select_vllm_module = current_config["selected_module"].get("VLLM")
            if not select_vllm_module:
                raise ValueError("Bạn chưa cấu hình module phân tích ảnh mặc định")

            vllm_type = (
                select_vllm_module
                if "type" not in current_config["VLLM"][select_vllm_module]
                else current_config["VLLM"][select_vllm_module]["type"]
            )

            if not vllm_type:
                raise ValueError(f"Không tìm thấy provider tương ứng của module VLLM {vllm_type}")

            vllm = create_instance(
                vllm_type, current_config["VLLM"][select_vllm_module]
            )

            result = vllm.response(question, image_base64)

            return_json = {
                "success": True,
                "action": Action.RESPONSE.name,
                "response": result,
            }

            response = web.Response(
                text=json.dumps(return_json, separators=(",", ":")),
                content_type="application/json",
            )
        except ValueError as e:
            self.logger.bind(tag=TAG).error(f"Yêu cầu POST MCP Vision gặp lỗi: {e}")
            return_json = self._create_error_response(str(e))
            response = web.Response(
                text=json.dumps(return_json, separators=(",", ":")),
                content_type="application/json",
            )
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Yêu cầu POST MCP Vision gặp lỗi: {e}")
            return_json = self._create_error_response("Đã xảy ra lỗi khi xử lý yêu cầu")
            response = web.Response(
                text=json.dumps(return_json, separators=(",", ":")),
                content_type="application/json",
            )
        finally:
            if response:
                self._add_cors_headers(response)
            return response

    async def handle_get(self, request):
        """Xử lý yêu cầu GET của MCP Vision"""
        try:
            vision_explain = get_vision_url(self.config)
            if vision_explain and len(vision_explain) > 0 and "null" != vision_explain:
                message = (
                    f"Giao diện MCP Vision đang hoạt động bình thường, địa chỉ giải thích ảnh là: {vision_explain}"
                )
            else:
                message = "Giao diện MCP Vision chưa hoạt động đúng, hãy mở file `.config.yaml` trong thư mục `data` và đặt `server.vision_explain` cho đúng"

            response = web.Response(text=message, content_type="text/plain")
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Yêu cầu GET MCP Vision gặp lỗi: {e}")
            return_json = self._create_error_response("Lỗi nội bộ máy chủ")
            response = web.Response(
                text=json.dumps(return_json, separators=(",", ":")),
                content_type="application/json",
            )
        finally:
            self._add_cors_headers(response)
            return response
