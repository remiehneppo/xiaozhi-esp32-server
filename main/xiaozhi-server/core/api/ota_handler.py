import json
import time
import base64
import hashlib
import hmac
import os
import re
import glob
from typing import Dict, List, Tuple
from aiohttp import web

from core.auth import AuthManager
from core.utils.util import get_local_ip, get_vision_url
from core.api.base_handler import BaseHandler

TAG = __name__


def _safe_basename(filename: str) -> str:
    # Prevent directory traversal
    return os.path.basename(filename)


def _parse_version(ver: str) -> Tuple[int, ...]:
    # conservative parser: split by non-digit, keep numeric parts
    parts = re.findall(r"\d+", ver)
    return tuple(int(p) for p in parts) if parts else (0,)


def _is_higher_version(a: str, b: str) -> bool:
    """Return True if version string a > b (semver-like numeric compare)."""
    ta = _parse_version(a)
    tb = _parse_version(b)
    # compare tuple lexicographically, but allow different lengths
    maxlen = max(len(ta), len(tb))
    for i in range(maxlen):
        ai = ta[i] if i < len(ta) else 0
        bi = tb[i] if i < len(tb) else 0
        if ai > bi:
            return True
        if ai < bi:
            return False
    return False


class OTAHandler(BaseHandler):
    def __init__(self, config: dict):
        super().__init__(config)
        auth_config = config["server"].get("auth", {})
        self.auth_enable = auth_config.get("enabled", False)
        # 
        self.allowed_devices = set(auth_config.get("allowed_devices", []))
        secret_key = config["server"]["auth_key"]
        expire_seconds = auth_config.get("expire_seconds")
        self.auth = AuthManager(secret_key=secret_key, expire_seconds=expire_seconds)

        # firmware storage
        self.bin_dir = os.path.join(os.getcwd(), "data", "bin")
        # cache structure: { 'updated_at': timestamp, 'ttl': seconds, 'files_by_model': { model: [(version, filename), ...] } }
        self._bin_cache: Dict = {
            "updated_at": 0,
            "ttl": config.get("firmware_cache_ttl", 30),
            "files_by_model": {},
        }

    def _refresh_bin_cache_if_needed(self):
        now = int(time.time())
        ttl = int(self._bin_cache.get("ttl", 30))
        if now - int(
            self._bin_cache.get("updated_at", 0)
        ) < ttl and self._bin_cache.get("files_by_model"):
            return

        files_by_model: Dict[str, List[Tuple[str, str]]] = {}
        try:
            if not os.path.isdir(self.bin_dir):
                os.makedirs(self.bin_dir, exist_ok=True)

            # match files like model_1.2.3.bin (allow dots, dashes, underscores in model and version)
            pattern = os.path.join(self.bin_dir, "*.bin")
            for path in glob.glob(pattern):
                fname = os.path.basename(path)
                # filename format: {model}_{version}.bin
                m = re.match(r"^(.+?)_([0-9][A-Za-z0-9\.\-_]*)\.bin$", fname)
                if not m:
                    # skip files not conforming to naming rule
                    continue
                model = m.group(1)
                version = m.group(2)
                files_by_model.setdefault(model, []).append((version, fname))

            # sort versions for each model descending
            for model, items in files_by_model.items():
                items.sort(key=lambda it: _parse_version(it[0]), reverse=True)

            self._bin_cache["files_by_model"] = files_by_model
            self._bin_cache["updated_at"] = now
            self.logger.bind(tag=TAG).info(
                f"Firmware cache refreshed: {len(files_by_model)} models"
            )
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"làm mớibộ nhớ đệmthất bại: {e}")
            # keep previous cache if any

    def generate_password_signature(self, content: str, secret_key: str) -> str:
        """tạoMQTTchữ ký

        Args:
            content: chữ kýnội dung (clientId + '|' + username)
            secret_key: 

        Returns:
            str: Base64mã hóaHMAC-SHA256chữ ký
        """
        try:
            hmac_obj = hmac.new(
                secret_key.encode("utf-8"), content.encode("utf-8"), hashlib.sha256
            )
            signature = hmac_obj.digest()
            return base64.b64encode(signature).decode("utf-8")
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Tạo chữ ký mật khẩu MQTT thất bại: {e}")
            return ""

    def _get_websocket_url(self, local_ip: str, port: int) -> str:
        """Lấy địa chỉ WebSocket

        Args:
            local_ip: Địa chỉ IP cục bộ
            port: Số cổng

        Returns:
            str: Địa chỉ WebSocket
        """
        server_config = self.config["server"]
        websocket_config = server_config.get("websocket", "")

        if "" not in websocket_config:
            return websocket_config
        else:
            return f"ws://{local_ip}:{port}/xiaozhi/v1/"

    async def handle_post(self, request):
        """Xử lý yêu cầu OTA POST

        Trình xử lý này sẽ:
        - đọc device id/client id như trước
        - cố xác định model thiết bị và firmware hiện tại (ưu tiên header, fallback sang body)
        - kiểm tra `data/bin` xem có firmware mới cho model đó không
        - nếu có firmware mới thì đặt `firmware.url` sang endpoint tải xuống
        """
        try:
            data = await request.text()
            self.logger.bind(tag=TAG).debug(f"Phương thức yêu cầu OTA: {request.method}")
            self.logger.bind(tag=TAG).debug(f"Header yêu cầu OTA: {request.headers}")
            self.logger.bind(tag=TAG).debug(f"Dữ liệu yêu cầu OTA: {data}")

            device_id = request.headers.get("device-id", "")
            if device_id:
                self.logger.bind(tag=TAG).info(f"Device ID yêu cầu OTA: {device_id}")
            else:
                raise Exception("Device ID của yêu cầu OTA trống")

            client_id = request.headers.get("client-id", "")
            if client_id:
                self.logger.bind(tag=TAG).info(f"Client ID yêu cầu OTA: {client_id}")
            else:
                raise Exception("Client ID của yêu cầu OTA trống")

            data_json = {}
            try:
                data_json = json.loads(data) if data else {}
            except Exception:
                data_json = {}

            server_config = self.config["server"]
            # Phân biệt cổng:
            # - websocket_port dùng để dựng URL WebSocket (server["port"])
            # - http_port dùng để dựng URL tải firmware OTA (server["http_port"])
            websocket_port = int(server_config.get("port", 8000))
            http_port = int(server_config.get("http_port", 8003))
            local_ip = get_local_ip()

            # Xác định model thiết bị (ưu tiên header)
            device_model = ""
            # Các header có thể chứa model
            for h in ("device-model", "device_model", "model"):
                if h in request.headers:
                    device_model = request.headers.get(h, "").strip()
                    break
            # Fallback sang body
            if not device_model:
                try:
                    if "board" in data_json and isinstance(data_json["board"], dict):
                        device_model = data_json["board"].get("type", "")
                    elif "model" in data_json:
                        device_model = data_json.get("model", "")
                except Exception:
                    device_model = ""
            if not device_model:
                device_model = "default"

            # Xác định phiên bản hiện tại của thiết bị (ưu tiên header)
            device_version = ""
            for h in (
                "device-version",
                "device_version",
                "firmware-version",
                "app-version",
                "application-version",
            ):
                if h in request.headers:
                    device_version = request.headers.get(h, "").strip()
                    break
            if not device_version:
                try:
                    device_version = data_json.get("application", {}).get("version", "")
                except Exception:
                    device_version = ""
            if not device_version:
                device_version = "0.0.0"

            return_json = {
                "server_time": {
                    "timestamp": int(round(time.time() * 1000)),
                    "timezone_offset": server_config.get("timezone_offset", 8) * 60,
                },
                "firmware": {
                    "version": device_version,
                    "url": "",
                },
            }

            # existing mqtt/websocket logic (unchanged)
            mqtt_gateway_endpoint = server_config.get("mqtt_gateway")

            if mqtt_gateway_endpoint:  # Nếu cấu hình một chuỗi không rỗng
                # Cố lấy model thiết bị từ dữ liệu yêu cầu (đã phân tích ở trên)
                try:
                    group_id = f"GID_{device_model}".replace(":", "_").replace(" ", "_")
                except Exception as e:
                    self.logger.bind(tag=TAG).error(f"Lấy model thiết bị thất bại: {e}")
                    group_id = "GID_default"

                mac_address_safe = device_id.replace(":", "_")
                mqtt_client_id = f"{group_id}@@@{mac_address_safe}@@@{mac_address_safe}"

                # xây dựngsử dụngdữ liệu
                user_data = {"ip": "unknown"}
                try:
                    user_data_json = json.dumps(user_data)
                    username = base64.b64encode(user_data_json.encode("utf-8")).decode(
                        "utf-8"
                    )
                except Exception as e:
                    self.logger.bind(tag=TAG).error(f"Tạo username thất bại: {e}")
                    username = ""

                # tạo
                password = ""
                signature_key = server_config.get("mqtt_signature_key", "")
                if signature_key:
                    password = self.generate_password_signature(
                        mqtt_client_id + "|" + username, signature_key
                    )
                    if not password:
                        password = ""  # Nếu ký thất bại thì để trống, do thiết bị quyết định có cho phép không mật khẩu hay không
                else:
                    self.logger.bind(tag=TAG).warning("Thiếu khóa ký MQTT, mật khẩu sẽ để trống")

                # xây dựngMQTTcấu hình（làm chosử dụng mqtt_gateway ký tự）
                return_json["mqtt"] = {
                    "endpoint": mqtt_gateway_endpoint,
                    "client_id": mqtt_client_id,
                    "username": username,
                    "password": password,
                    "publish_topic": "device-server",
                    "subscribe_topic": f"devices/p2p/{mac_address_safe}",
                }
                self.logger.bind(tag=TAG).info(f"Cấp cấu hình MQTT gateway cho thiết bị {device_id}")

            else:  # Chưa cấu hình mqtt_gateway, cấp WebSocket
                # Nếu bật xác thực thì kiểm tra token
                token = ""
                if self.auth_enable:
                    if self.allowed_devices:
                        if device_id not in self.allowed_devices:
                            token = self.auth.generate_token(client_id, device_id)
                    else:
                        token = self.auth.generate_token(client_id, device_id)
                # NOTE: use websocket_port here
                return_json["websocket"] = {
                    "url": self._get_websocket_url(local_ip, websocket_port),
                    "token": token,
                }
                self.logger.bind(tag=TAG).info(
                    f"Chưa cấu hình MQTT gateway, cấp cấu hình WebSocket cho thiết bị {device_id}"
                )

            # Now check firmware files for updates
            try:
                self._refresh_bin_cache_if_needed()
                files_by_model = self._bin_cache.get("files_by_model", {})
                candidates = files_by_model.get(device_model, [])

                self.logger.bind(tag=TAG).info(
                    f"Tìm firmware cho model {device_model}, tìm thấy {len(candidates)} bản ứng viên"
                )

                chosen_url = ""
                chosen_version = device_version

                # candidates are sorted descending by version
                for ver, fname in candidates:
                    if _is_higher_version(ver, device_version):
                        # build download url (only allow download via our download endpoint)
                        chosen_version = ver
                        # Use get_vision_url to get the base URL and replace the path
                        vision_url = get_vision_url(self.config)
                        # Replace the path from "/mcp/vision/explain" to "/xiaozhi/ota/download/{fname}"
                        chosen_url = vision_url.replace(
                            "/mcp/vision/explain", f"/xiaozhi/ota/download/{fname}"
                        )
                        break

                if chosen_url:
                    return_json["firmware"]["version"] = chosen_version
                    return_json["firmware"]["url"] = chosen_url
                    self.logger.bind(tag=TAG).info(
                        f"Cấp firmware {chosen_version} cho thiết bị {device_id} [nếu tiền tố địa chỉ sai, hãy kiểm tra server.vision_explain trong file cấu hình] -> {chosen_url} "
                    )
                else:
                    self.logger.bind(tag=TAG).info(
                        f"Firmware của thiết bị {device_id} đã là mới nhất: {device_version}"
                    )

            except Exception as e:
                self.logger.bind(tag=TAG).error(f"Lỗi khi kiểm tra phiên bản firmware: {e}")

            response = web.Response(
                text=json.dumps(return_json, separators=(",", ":")),
                content_type="application/json",
            )
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Xử lý OTA POST gặp lỗi: {e}")
            return_json = {"success": False, "message": "lỗi yêu cầu."}
            response = web.Response(
                text=json.dumps(return_json, separators=(",", ":")),
                content_type="application/json",
            )
        finally:
            self._add_cors_headers(response)
            return response

    async def handle_get(self, request):
        """Xử lý yêu cầu OTA GET"""
        try:
            server_config = self.config["server"]
            local_ip = get_local_ip()
            # use websocket port for websocket URL
            websocket_port = int(server_config.get("port", 8000))
            websocket_url = self._get_websocket_url(local_ip, websocket_port)
            message = f"Giao diện OTA đang hoạt động bình thường, địa chỉ WebSocket gửi cho thiết bị là: {websocket_url}"
            response = web.Response(text=message, content_type="text/plain")
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Yêu cầu GET OTA gặp lỗi: {e}")
            response = web.Response(text="Giao diện OTA gặp lỗi", content_type="text/plain")
        finally:
            self._add_cors_headers(response)
            return response

    async def handle_download(self, request):
        """
        Giao diện tải firmware
        URL: /xiaozhi/ota/download/{filename}
        - Chỉ cho phép tải file .bin trong thư mục `data/bin`
        - filename phải là basename và khớp mẫu an toàn
        """
        try:
            fname = request.match_info.get("filename", "")
            if not fname:
                raise web.HTTPBadRequest(text="cần filename")

            # sanitize
            fname = _safe_basename(fname)
            # pattern: allow letters, numbers, dot, underscore, dash
            if not re.match(r"^[A-Za-z0-9\.\-_]+\.bin$", fname):
                raise web.HTTPBadRequest(text="filename không hợp lệ")

            file_path = os.path.join(self.bin_dir, fname)
            # ensure realpath is under bin_dir
            file_real = os.path.realpath(file_path)
            bin_dir_real = os.path.realpath(self.bin_dir)
            if (
                not file_real.startswith(bin_dir_real + os.sep)
                and file_real != bin_dir_real
            ):
                raise web.HTTPForbidden(text="bị từ chối")

            if not os.path.isfile(file_real):
                raise web.HTTPNotFound(text="không tìm thấy file")

            # use FileResponse to stream file
            resp = web.FileResponse(path=file_real)
        except web.HTTPError as e:
            resp = e
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Lỗi tải firmware: {e}")
            resp = web.Response(text="lỗi tải xuống", status=500)
        finally:
            try:
                self._add_cors_headers(resp)
            except Exception:
                pass
            return resp
