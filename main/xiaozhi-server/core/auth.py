import hmac
import base64
import hashlib
import time


class AuthenticationError(Exception):
    """xác thựcngoại lệ"""

    pass


class AuthManager:
    """
    thống nhấtủy quyềnxác thực
    tạovớixác thực client_id device_id token（HMAC-SHA256）xác thực
    token trongkhông client_id/device_id，chỉchữ ký + thời gian; client_id/device_idtạikết nốithời
    tại MQTT trong client_id: client_id, username: device_id, password: token
    tại Websocket trong，header:{Device-ID: device_id, Client-ID: client_id, Authorization: Bearer token, ......}
    """

    def __init__(self, secret_key: str, expire_seconds: int = 60 * 60 * 24 * 30):
        if not expire_seconds or expire_seconds < 0:
            self.expire_seconds = 60 * 60 * 24 * 30
        else:
            self.expire_seconds = expire_seconds
        self.secret_key = secret_key

    def _sign(self, content: str) -> str:
        """HMAC-SHA256chữ kývàBase64mã hóa"""
        sig = hmac.new(
            self.secret_key.encode("utf-8"), content.encode("utf-8"), hashlib.sha256
        ).digest()
        return base64.urlsafe_b64encode(sig).decode("utf-8").rstrip("=")

    def generate_token(self, client_id: str, username: str) -> str:
        """
        tạo token
        Args:
            client_id: kết nốiID
            username: sử dụng（chodeviceId）
        Returns:
            str: tokenký tự
        """
        ts = int(time.time())
        content = f"{client_id}|{username}|{ts}"
        signature = self._sign(content)
        # tokenchỉchữ kývớithời gian，khôngthông tin
        token = f"{signature}.{ts}"
        return token

    def verify_token(self, token: str, client_id: str, username: str) -> bool:
        """
        xác thựctokenhiệu quả
        Args:
            token: máy kháchvàotoken
            client_id: kết nốilàm chosử dụngclient_id
            username: kết nốilàm chosử dụngusername
        """
        try:
            sig_part, ts_str = token.split(".")
            ts = int(ts_str)
            if int(time.time()) - ts > self.expire_seconds:
                return False  # qua

            expected_sig = self._sign(f"{client_id}|{username}|{ts}")
            if not hmac.compare_digest(sig_part, expected_sig):
                return False

            return True
        except Exception:
            return False
