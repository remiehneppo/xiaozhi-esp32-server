import asyncio
from aiohttp import web
from config.logger import setup_logging
from core.api.ota_handler import OTAHandler
from core.api.vision_handler import VisionHandler

TAG = __name__


class SimpleHttpServer:
    def __init__(self, config: dict):
        self.config = config
        self.logger = setup_logging()
        self.ota_handler = OTAHandler(config)
        self.vision_handler = VisionHandler(config)

    def _get_websocket_url(self, local_ip: str, port: int) -> str:
        """Lấy địa chỉ WebSocket

        Args:
            local_ip: Địa chỉ IP cục bộ
            port: Số cổng

        Returns:
            str: Địa chỉ WebSocket
        """
        server_config = self.config["server"]
        websocket_config = server_config.get("websocket")

        if websocket_config and "địa_chỉ_ip_hoặc_domain" not in websocket_config and "cổng" not in websocket_config:
            return websocket_config
        else:
            return f"ws://{local_ip}:{port}/xiaozhi/v1/"

    async def start(self):
        try:
            server_config = self.config["server"]
            read_config_from_api = self.config.get("read_config_from_api", False)
            host = server_config.get("ip", "0.0.0.0")
            port = int(server_config.get("http_port", 8003))

            if port:
                app = web.Application()

                if not read_config_from_api:
                    # Nếu chưa bật manager console và chỉ chạy đơn module, cần thêm OTA đơn giản để đẩy địa chỉ WebSocket
                    app.add_routes(
                        [
                            web.get("/xiaozhi/ota/", self.ota_handler.handle_get),
                            web.post("/xiaozhi/ota/", self.ota_handler.handle_post),
                            web.options(
                                "/xiaozhi/ota/", self.ota_handler.handle_options
                            ),
                            # Endpoint tải xuống, chỉ cung cấp tải `data/bin/*.bin`
                            web.get(
                                "/xiaozhi/ota/download/{filename}",
                                self.ota_handler.handle_download,
                            ),
                            web.options(
                                "/xiaozhi/ota/download/{filename}",
                                self.ota_handler.handle_options,
                            ),
                        ]
                    )
                # Thêm route
                app.add_routes(
                    [
                        web.get("/mcp/vision/explain", self.vision_handler.handle_get),
                        web.post(
                            "/mcp/vision/explain", self.vision_handler.handle_post
                        ),
                        web.options(
                            "/mcp/vision/explain", self.vision_handler.handle_options
                        ),
                    ]
                )

                # Chạy dịch vụ
                runner = web.AppRunner(app)
                await runner.setup()
                site = web.TCPSite(runner, host, port)
                await site.start()

                # Giữ dịch vụ chạy
                while True:
                    await asyncio.sleep(3600)  # Kiểm tra mỗi 1 giờ
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"Khởi động máy chủ HTTP thất bại: {e}")
            import traceback

            self.logger.bind(tag=TAG).error(f"Stack lỗi: {traceback.format_exc()}")
            raise
