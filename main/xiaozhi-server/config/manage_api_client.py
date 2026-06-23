import os
import base64
from typing import Optional, Dict

import httpx

TAG = __name__


class DeviceNotFoundException(Exception):
    pass


class DeviceBindException(Exception):
    def __init__(self, bind_code):
        self.bind_code = bind_code
        super().__init__(f"ngoại lệ，: {bind_code}")


class ManageApiClient:
    _instance = None
    _async_clients = {}  # chomỗilưu trữmáy khách
    _secret = None

    def __new__(cls, config):
        """chế độđảm bảotoàn cục，vàvàocấu hìnhtham số"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._init_client(config)
        return cls._instance

    @classmethod
    def _init_client(cls, config):
        """khởi tạocấu hình（độ trễtạomáy khách）"""
        cls.config = config.get("manager-api")

        if not cls.config:
            raise Exception("manager-apicấu hìnhlỗi")

        if not cls.config.get("url") or not cls.config.get("secret"):
            raise Exception("manager-apiurlhoặcsecretcấu hìnhlỗi")

        if "thay_bang" in cls.config.get("secret") or "your_secret" in cls.config.get("secret"):
            raise Exception("Vui lòng cấu hình manager-api secret thực tế trong file .config.yaml")

        cls._secret = cls.config.get("secret")
        cls.max_retries = cls.config.get("max_retries", 6)  # thử lạilần
        cls.retry_delay = cls.config.get("retry_delay", 10)  # thử lạiđộ trễ()
        # khôngtạinàytrongtạo AsyncClient，độ trễđếnlàm chosử dụngthờitạo
        cls._async_clients = {}

    @classmethod
    async def _ensure_async_client(cls):
        """đảm bảomáy kháchđãtạo（chomỗitạomáy khách）"""
        import asyncio

        try:
            loop = asyncio.get_running_loop()
            loop_id = id(loop)

            # chomỗitạomáy khách
            if loop_id not in cls._async_clients:
                # dịch vụcó thểđóngkết nối，httpx kết nốiđúngvàdọn dẹp
                limits = httpx.Limits(
                    max_keepalive_connections=0,  # vô hiệu hóa keep-alive，lầnkết nối
                )
                cls._async_clients[loop_id] = httpx.AsyncClient(
                    base_url=cls.config.get("url"),
                    headers={
                        "User-Agent": f"PythonClient/2.0 (PID:{os.getpid()})",
                        "Accept": "application/json",
                        "Authorization": "Bearer " + cls._secret,
                    },
                    timeout=cls.config.get("timeout", 30),
                    limits=limits,  # làm chosử dụng
                )
            return cls._async_clients[loop_id]
        except RuntimeError:
            # nhưkhông cótrong，tạomộttạm thời
            raise Exception("tạingữ cảnhtrongsử dụng")

    @classmethod
    async def _async_request(cls, method: str, endpoint: str, **kwargs) -> Dict:
        """gửilầnHTTPyêu cầuvàxử lýphản hồi"""
        # đảm bảomáy kháchđãtạo
        client = await cls._ensure_async_client()
        endpoint = endpoint.lstrip("/")
        response = None
        try:
            response = await client.request(method, endpoint, **kwargs)
            response.raise_for_status()

            result = response.json()

            # xử lýAPItrả vềlỗi
            if result.get("code") == 10041:
                raise DeviceNotFoundException(result.get("msg"))
            elif result.get("code") == 10042:
                raise DeviceBindException(result.get("msg"))
            elif result.get("code") != 0:
                raise Exception(f"APItrả vềlỗi: {result.get('msg', 'lỗi không xác định')}")

            # trả vềthành côngdữ liệu
            return result.get("data") if result.get("code") == 0 else None
        finally:
            # đảm bảophản hồibịđóng（làm chongoại lệsẽ）
            if response is not None:
                await response.aclose()

    @classmethod
    def _should_retry(cls, exception: Exception) -> bool:
        """ngoại lệcóthử lại"""
        # kết nốilỗi
        if isinstance(
            exception, (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError)
        ):
            return True

        # HTTPtrạng tháilỗi
        if isinstance(exception, httpx.HTTPStatusError):
            status_code = exception.response.status_code
            return status_code in [408, 429, 500, 502, 503, 504]

        return False

    @classmethod
    async def _execute_async_request(cls, method: str, endpoint: str, **kwargs) -> Dict:
        """thử lạiyêu cầu"""
        import asyncio

        retry_count = 0

        while retry_count <= cls.max_retries:
            try:
                # yêu cầu
                return await cls._async_request(method, endpoint, **kwargs)
            except Exception as e:
                # cóthử lại
                if retry_count < cls.max_retries and cls._should_retry(e):
                    retry_count += 1
                    print(
                        f"{method} {endpoint} yêu cầuthất bại，sẽtại {cls.retry_delay:.1f} sautiến hành {retry_count} lầnthử lại"
                    )
                    await asyncio.sleep(cls.retry_delay)
                    continue
                else:
                    # khôngthử lại，rangoại lệ
                    raise

    @classmethod
    def safe_close(cls):
        """an toànđóngcókết nối"""
        import asyncio

        for client in list(cls._async_clients.values()):
            try:
                asyncio.run(client.aclose())
            except Exception:
                pass
        cls._async_clients.clear()
        cls._instance = None


async def get_server_config() -> Optional[Dict]:
    """lấymáy chủcấu hình"""
    return await ManageApiClient._instance._execute_async_request(
        "POST", "/config/server-base"
    )


async def get_agent_models(
    mac_address: str, client_id: str, selected_module: Dict
) -> Optional[Dict]:
    """lấymô hìnhcấu hình"""
    return await ManageApiClient._instance._execute_async_request(
        "POST",
        "/config/agent-models",
        json={
            "macAddress": mac_address,
            "clientId": client_id,
            "selectedModule": selected_module,
        },
    )


async def get_correct_words(mac_address: str) -> Optional[Dict]:
    """lấycó thểthay thế"""
    try:
        return await ManageApiClient._instance._execute_async_request(
            "POST", "/config/correct-words",
            json={"macAddress": mac_address}
        )
    except Exception as e:
        print(f"lấythay thếthất bại: {e}")
        return None


async def generate_and_save_chat_summary(session_id: str) -> Optional[Dict]:
    """tạovàlưughi lại"""
    try:
        return await ManageApiClient._instance._execute_async_request(
            "POST",
            f"/agent/chat-summary/{session_id}/save",
        )
    except Exception as e:
        print(f"tạovàlưughi lạithất bại: {e}")
        return None


async def generate_and_save_chat_title(session_id: str) -> Optional[Dict]:
    """tạovàlưu"""
    try:
        return await ManageApiClient._instance._execute_async_request(
            "POST",
            f"/agent/chat-title/{session_id}/generate",
        )
    except Exception as e:
        print(f"tạovàlưuthất bại: {e}")
        return None


async def report(
    mac_address: str, session_id: str, chat_type: int, content: str, audio, report_time
) -> Optional[Dict]:
    """ghi lạibáo cáo"""
    if not content or not ManageApiClient._instance:
        return None
    try:
        return await ManageApiClient._instance._execute_async_request(
            "POST",
            f"/agent/chat-history/report",
            json={
                "macAddress": mac_address,
                "sessionId": session_id,
                "chatType": chat_type,
                "content": content,
                "reportTime": report_time,
                "audioBase64": (
                    base64.b64encode(audio).decode("utf-8") if audio else None
                ),
            },
        )
    except Exception as e:
        print(f"TTSbáo cáothất bại: {e}")
        return None


async def lookup_address_book(caller_mac: str, nickname: str) -> Optional[Dict]:
    """theo"""
    if not ManageApiClient._instance:
        return None
    try:
        return await ManageApiClient._instance._execute_async_request(
            "GET",
            f"/device/address-book/lookup?callerMac={caller_mac}&nickname={nickname}",
        )
    except Exception as e:
        print(f"thất bại: {e}")
        return None


def init_service(config):
    ManageApiClient(config)


def manage_api_http_safe_close():
    ManageApiClient.safe_close()
