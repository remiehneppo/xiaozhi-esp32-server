from aiohttp import web
from config.logger import setup_logging


class BaseHandler:
    def __init__(self, config: dict):
        self.config = config
        self.logger = setup_logging()

    def _add_cors_headers(self, response):
        """thêmCORSthông tin"""
        response.headers["Access-Control-Allow-Headers"] = (
            "client-id, content-type, device-id, authorization"
        )
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Origin"] = "*"

    async def handle_options(self, request):
        """xử lýOPTIONSyêu cầu，thêmCORSthông tin"""
        response = web.Response(body=b"", content_type="text/plain")
        self._add_cors_headers(response)
        # thêmphương pháp
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response
