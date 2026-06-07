import sys
import uuid
import signal
import asyncio
from aioconsole import ainput
from config.settings import load_config
from config.logger import setup_logging
from core.utils.util import get_local_ip, validate_mcp_endpoint
from core.http_server import SimpleHttpServer
from core.websocket_server import WebSocketServer
from core.utils.util import check_ffmpeg_installed
from core.utils.gc_manager import get_gc_manager

TAG = __name__
logger = setup_logging()


async def wait_for_exit() -> None:
    """
    Chặn đến khi nhận Ctrl-C / SIGTERM.
    - Unix: dùng `add_signal_handler`
    - Windows: dựa vào `KeyboardInterrupt`
    """
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    if sys.platform != "win32":  # Unix / macOS
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop_event.set)
        await stop_event.wait()
    else:
        # Windows: chờ một Future luôn pending,
        # để KeyboardInterrupt nổi lên tới asyncio.run và tránh tiến trình bị chặn khi còn thread thường tồn tại
        try:
            await asyncio.Future()
        except KeyboardInterrupt:  # Ctrl‑C
            pass


async def monitor_stdin():
    """Theo dõi stdin, chỉ để tiêu thụ phím Enter"""
    while True:
        await ainput()  # Chờ input bất đồng bộ, chỉ để tiêu thụ Enter


async def main():
    check_ffmpeg_installed()
    config = load_config()

    # Độ ưu tiên của auth_key: server.auth_key trong config > manager-api.secret > tự sinh
    # auth_key dùng cho xác thực JWT, ví dụ JWT cho API phân tích ảnh, token OTA và xác thực WebSocket
    # Lấy auth_key từ file config
    auth_key = config["server"].get("auth_key", "")
    
    # Kiểm tra auth_key, nếu không hợp lệ thì thử dùng manager-api.secret
    if not auth_key or len(auth_key) == 0 or "giá_trị_server.secret_của_bạn" in auth_key:
        auth_key = config.get("manager-api", {}).get("secret", "")
        # Kiểm tra secret, nếu không hợp lệ thì sinh khóa ngẫu nhiên
        if not auth_key or len(auth_key) == 0 or "giá_trị_server.secret_của_bạn" in auth_key:
            auth_key = str(uuid.uuid4().hex)
    
    config["server"]["auth_key"] = auth_key

    # Thêm tác vụ theo dõi stdin
    stdin_task = asyncio.create_task(monitor_stdin())

    # Khởi động trình quản lý GC toàn cục (dọn dẹp mỗi 5 phút)
    gc_manager = get_gc_manager(interval_seconds=300)
    await gc_manager.start()

    # Khởi động server WebSocket
    ws_server = WebSocketServer(config)
    ws_task = asyncio.create_task(ws_server.start())
    # Khởi động server HTTP đơn giản
    ota_server = SimpleHttpServer(config)
    ota_task = asyncio.create_task(ota_server.start())

    read_config_from_api = config.get("read_config_from_api", False)
    port = int(config["server"].get("http_port", 8003))
    if not read_config_from_api:
        logger.bind(tag=TAG).info(
            "Địa chỉ OTA là\t\thttp://{}:{}/xiaozhi/ota/",
            get_local_ip(),
            port,
        )
    logger.bind(tag=TAG).info(
        "Địa chỉ phân tích ảnh là\thttp://{}:{}/mcp/vision/explain",
        get_local_ip(),
        port,
    )
    mcp_endpoint = config.get("mcp_endpoint", None)
    if mcp_endpoint is not None and "Địa chỉ WebSocket của điểm truy cập MCP" not in mcp_endpoint:
        # Kiểm tra định dạng điểm truy cập MCP
        if validate_mcp_endpoint(mcp_endpoint):
            logger.bind(tag=TAG).info("Điểm truy cập MCP là\t{}", mcp_endpoint)
            # Chuyển địa chỉ MCP từ điểm truy cập sang điểm gọi
            mcp_endpoint = mcp_endpoint.replace("/mcp/", "/call/")
            config["mcp_endpoint"] = mcp_endpoint
        else:
            logger.bind(tag=TAG).error("Điểm truy cập MCP không đúng định dạng")
            config["mcp_endpoint"] = "Địa chỉ WebSocket của điểm truy cập MCP"

    # Lấy cấu hình WebSocket, dùng giá trị mặc định an toàn
    websocket_port = 8000
    server_config = config.get("server", {})
    if isinstance(server_config, dict):
        websocket_port = int(server_config.get("port", 8000))

    logger.bind(tag=TAG).info(
        "Địa chỉ WebSocket là\tws://{}:{}/xiaozhi/v1/",
        get_local_ip(),
        websocket_port,
    )

    logger.bind(tag=TAG).info(
        "=======Địa chỉ trên là địa chỉ giao thức WebSocket, không mở bằng trình duyệt======="
    )
    logger.bind(tag=TAG).info(
        "Nếu muốn kiểm tra WebSocket, hãy khởi động module digital-human và mở trình duyệt để thử tương tác"
    )
    logger.bind(tag=TAG).info(
        "=============================================================\n"
    )

    try:
        await wait_for_exit()  # Chặn đến khi nhận tín hiệu thoát
    except asyncio.CancelledError:
        print("Tác vụ đã bị hủy, đang dọn dẹp tài nguyên...")
    finally:
        # Dừng trình quản lý GC toàn cục
        await gc_manager.stop()

        # Hủy tất cả tác vụ (điểm sửa quan trọng)
        stdin_task.cancel()
        ws_task.cancel()
        if ota_task:
            ota_task.cancel()

        # Chờ tác vụ kết thúc (phải có timeout)
        await asyncio.wait(
            [stdin_task, ws_task, ota_task] if ota_task else [stdin_task, ws_task],
            timeout=3.0,
            return_when=asyncio.ALL_COMPLETED,
        )
        print("Máy chủ đã tắt, chương trình thoát.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Đã ngắt thủ công, chương trình dừng.")
