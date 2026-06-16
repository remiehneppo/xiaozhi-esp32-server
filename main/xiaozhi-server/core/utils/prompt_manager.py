"""
gợi ý
vàcập nhậtgợi ý，bao gồmnhanhkhởi tạovàcó thể
"""

import os
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler
from config.logger import setup_logging
from jinja2 import Template

TAG = __name__

WEEKDAY_MAP = {
    "Monday": "",
    "Tuesday": "",
    "Wednesday": "",
    "Thursday": "",
    "Friday": "",
    "Saturday": "",
    "Sunday": "",
}

EMOJI_List = [
    "😶",
    "🙂",
    "😆",
    "😂",
    "😔",
    "😠",
    "😭",
    "😍",
    "😳",
    "😲",
    "😱",
    "🤔",
    "😉",
    "😎",
    "😌",
    "🤤",
    "😘",
    "😏",
    "😴",
    "😜",
    "🙄",
]


class PromptManager:
    """gợi ý，vàcập nhậtgợi ý"""

    def __init__(self, config: Dict[str, Any], logger=None):
        self.config = config
        self.logger = logger or setup_logging()
        self.base_prompt_template = None
        self.last_update_time = 0

        # Nhập trình quản lý bộ nhớ cache toàn cục
        from core.utils.cache.manager import cache_manager, CacheType

        self.cache_manager = cache_manager
        self.CacheType = CacheType

        # khởi tạotrên
        from core.utils.context_provider import ContextDataProvider

        self.context_provider = ContextDataProvider(config, self.logger)
        self.context_data = {}

        self._load_base_template()

    def _load_base_template(self):
        """tảigợi ý"""
        try:
            template_path = self.config.get("prompt_template", None)
            if not template_path:
                template_path = "agent-base-prompt.txt"
            cache_key = f"prompt_template:{template_path}"

            # Lấy từ cache trước
            cached_template = self.cache_manager.get(self.CacheType.CONFIG, cache_key)
            if cached_template is not None:
                self.base_prompt_template = cached_template
                self.logger.bind(tag=TAG).debug("từbộ nhớ đệmtảigợi ý")
                return

            # bộ nhớ đệmtrong，từtệpđọc
            if os.path.exists(template_path):
                with open(template_path, "r", encoding="utf-8") as f:
                    template_content = f.read()

                # Lưu vào cache（CONFIGmặc địnhkhôngqua，cần）
                self.cache_manager.set(
                    self.CacheType.CONFIG, cache_key, template_content
                )
                self.base_prompt_template = template_content
                self.logger.bind(tag=TAG).debug("thành côngtảigợi ývàbộ nhớ đệm")
            else:
                self.logger.bind(tag=TAG).warning(f"đến{template_path}tệp")
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"tảigợi ýthất bại: {e}")

    def get_quick_prompt(self, user_prompt: str, device_id: str = None) -> str:
        """nhanhlấygợi ý（làm chosử dụngsử dụngcấu hình）"""
        device_cache_key = f"device_prompt:{device_id}"
        cached_device_prompt = self.cache_manager.get(
            self.CacheType.DEVICE_PROMPT, device_cache_key
        )
        if cached_device_prompt is not None:
            self.logger.bind(tag=TAG).debug(f"làm chosử dụng {device_id} củbộ nhớ đệmgợi ý")
            return cached_device_prompt
        else:
            self.logger.bind(tag=TAG).debug(
                f" {device_id} bộ nhớ đệmgợi ý，làm chosử dụngvàocủgợi ý"
            )

        # sử dụngvàocủgợi ývàbộ nhớ đệm（nhưcóID）
        if device_id:
            device_cache_key = f"device_prompt:{device_id}"
            self.cache_manager.set(self.CacheType.DEVICE_PROMPT, device_cache_key, user_prompt)
            self.logger.bind(tag=TAG).debug(f" {device_id} củgợi ýđãbộ nhớ đệm")

        self.logger.bind(tag=TAG).info(f"làm chosử dụngnhanhgợi ý: {user_prompt[:50]}...")
        return user_prompt

    def _get_current_time_info(self) -> tuple:
        """lấyhiện tạikhi/thờithông tin"""
        from .current_time import (
            get_current_date,
            get_current_weekday,
            get_current_lunar_date,
        )

        today_date = get_current_date()
        today_weekday = get_current_weekday()
        lunar_date = get_current_lunar_date() + "\n"

        return today_date, today_weekday, lunar_date

    def _get_location_info(self, client_ip: str) -> str:
        """lấyvị tríthông tin"""
        try:
            # Lấy từ cache trước
            cached_location = self.cache_manager.get(self.CacheType.LOCATION, client_ip)
            if cached_location is not None:
                return cached_location

            # Cache miss, gọi APIlấy
            from core.utils.util import get_ip_info

            ip_info = get_ip_info(client_ip, self.logger)
            city = ip_info.get("city", "không xác địnhvị trí")
            location = f"{city}"

            # Lưu vào cache
            self.cache_manager.set(self.CacheType.LOCATION, client_ip, location)
            return location
        except Exception as e:
            self.logger.bind(tag=TAG).error(f"lấyvị tríthông tinthất bại: {e}")
            return "không xác địnhvị trí"

    def _get_weather_info(self, conn: "ConnectionHandler", location: str) -> str:
        """lấythông tin"""
        try:
            # Lấy từ cache trước
            cached_weather = self.cache_manager.get(self.CacheType.WEATHER, location)
            if cached_weather is not None:
                return cached_weather

            # bộ nhớ đệmtrong，sử dụngget_weatherhàmlấy
            from plugins_func.functions.get_weather import get_weather
            from plugins_func.register import ActionResponse

            # sử dụngget_weatherhàm
            result = get_weather(conn, location=location, lang="zh_CN")
            if isinstance(result, ActionResponse):
                weather_report = result.result
                self.cache_manager.set(self.CacheType.WEATHER, location, weather_report)
                return weather_report
            return "thông tinlấythất bại"

        except Exception as e:
            self.logger.bind(tag=TAG).error(f"lấythông tinthất bại: {e}")
            return "thông tinlấythất bại"

    def update_context_info(self, conn, client_ip: str):
        """cập nhậttrênthông tin"""
        try:
            local_address = ""
            if (
                client_ip
                and self.base_prompt_template
                and (
                    "local_address" in self.base_prompt_template
                    or "weather_info" in self.base_prompt_template
                )
            ):
                # lấyvị tríthông tin（làm chosử dụngtoàn cụcbộ nhớ đệm）
                local_address = self._get_location_info(client_ip)

            if (
                self.base_prompt_template
                and "weather_info" in self.base_prompt_template
                and local_address
            ):
                # lấythông tin（làm chosử dụngtoàn cụcbộ nhớ đệm）
                self._get_weather_info(conn, local_address)

            # lấycấu hìnhcủtrêndữ liệu
            if hasattr(conn, "device_id") and conn.device_id:
                if (
                    self.base_prompt_template
                    and "dynamic_context" in self.base_prompt_template
                ):
                    self.context_data = self.context_provider.fetch_all(conn.device_id)
                else:
                    self.context_data = ""

            self.logger.bind(tag=TAG).debug(f"trênthông tincập nhậthoàn thành")

        except Exception as e:
            self.logger.bind(tag=TAG).error(f"cập nhậttrênthông tinthất bại: {e}")

    def build_enhanced_prompt(
        self, user_prompt: str, device_id: str, client_ip: str = None, *args, **kwargs
    ) -> str:
        """xây dựngcủgợi ý"""
        if not self.base_prompt_template:
            return user_prompt

        try:
            # lấycủkhi/thờithông tin（khôngbộ nhớ đệm）
            today_date, today_weekday, lunar_date = self._get_current_time_info()

            # lấybộ nhớ đệmcủtrênthông tin
            local_address = ""
            weather_info = ""

            if client_ip:
                # lấyvị tríthông tin（từtoàn cụcbộ nhớ đệm）
                local_address = (
                    self.cache_manager.get(self.CacheType.LOCATION, client_ip) or ""
                )

                # lấythông tin（từtoàn cụcbộ nhớ đệm）
                if local_address:
                    weather_info = (
                        self.cache_manager.get(self.CacheType.WEATHER, local_address)
                        or ""
                    )

            # lấyTTScủ，mặc địnhchotrong
            language = (
                self.config.get("TTS", {})
                .get(self.config.get("selected_module", {}).get("TTS", ""), {})
                .get("language")
                or "trong"
            )
            self.logger.bind(tag=TAG).debug(f"lấyđếncủ: {language}")

            # thay thế
            template = Template(self.base_prompt_template)
            enhanced_prompt = template.render(
                base_prompt=user_prompt,
                current_time="{{current_time}}",
                today_date=today_date,
                today_weekday=today_weekday,
                lunar_date=lunar_date,
                local_address=local_address,
                weather_info=weather_info,
                emojiList=EMOJI_List,
                device_id=device_id,
                client_ip=client_ip,
                dynamic_context=self.context_data,
                language=language,
                *args,
                **kwargs,
            )
            device_cache_key = f"device_prompt:{device_id}"
            self.cache_manager.set(
                self.CacheType.DEVICE_PROMPT, device_cache_key, enhanced_prompt
            )
            self.logger.bind(tag=TAG).info(
                f"xây dựnggợi ýthành công，: {len(enhanced_prompt)}"
            )
            return enhanced_prompt

        except Exception as e:
            self.logger.bind(tag=TAG).error(f"xây dựnggợi ýthất bại: {e}")
            return user_prompt
