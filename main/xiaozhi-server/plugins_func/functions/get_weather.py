import requests
from bs4 import BeautifulSoup
from config.logger import setup_logging
from plugins_func.register import register_function, ToolType, ActionResponse, Action
from core.utils.util import get_ip_info
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

TAG = __name__
logger = setup_logging()

GET_WEATHER_FUNCTION_DESC = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": (
            "Lấy thời tiết cho một địa điểm cụ thể. Người dùng nên cung cấp vị trí, ví dụ: thời tiết Hà Nội, thời tiết Đà Nẵng, thời tiết TP.HCM. "
            "Nếu người dùng chỉ nói tên tỉnh hoặc địa danh chưa rõ, hãy truyền đúng cụm địa điểm họ nói. "
            "Quan trọng: thời tiết 7 ngày tới tại địa phương đã có trong context; nếu người dùng không chỉ định thành phố khác thì không gọi tool này."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Tên địa điểm, ví dụ Hà Nội hoặc Thành phố Hồ Chí Minh. Nếu không có địa điểm thì không truyền.",
                },
                "lang": {
                    "type": "string",
                    "description": "Mã ngôn ngữ trả về, ví dụ vi_VN hoặc en_US. Mặc định vi_VN.",
                },
            },
            "required": ["lang"],
        },
    },
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    )
}

# Mã thời tiết https://dev.qweather.com/docs/resource/icons/#weather-icons
WEATHER_CODE_MAP = {
    "100": "Nắng",
    "101": "Nhiều mây",
    "102": "Ít mây",
    "103": "Nắng xen mây",
    "104": "Âm",
    "150": "Nắng",
    "151": "Nhiều mây",
    "152": "Ít mây",
    "153": "Nắng xen mây",
    "300": "Mưa rào",
    "301": "Mưa rào mạnh",
    "302": "Mưa dông",
    "303": "Mưa dông mạnh",
    "304": "Mưa dông có mưa đá",
    "305": "Mưa nhỏ",
    "306": "Mưa vừa",
    "307": "Mưa to",
    "308": "Mưa cực đoan",
    "309": "Mưa phùn/Mưa nhỏ",
    "310": "",
    "311": "",
    "312": "",
    "313": "",
    "314": "đếntrong",
    "315": "trongđến",
    "316": "đến",
    "317": "đến",
    "318": "đến",
    "350": "",
    "351": "",
    "399": "Mưa",
    "400": "Tuyết nhỏ",
    "401": "Tuyết vừa",
    "402": "Tuyết to",
    "403": "Tuyết lớn",
    "404": "Mưa tuyết",
    "405": "",
    "406": "",
    "407": "",
    "408": "đếntrong",
    "409": "trongđến",
    "410": "đến",
    "456": "",
    "457": "",
    "499": "Tuyết",
    "500": "Sương mỏng",
    "501": "Sương",
    "502": "Sương mù khô",
    "503": "Bụi bay",
    "504": "Bụi nổi",
    "507": "Bão bụi",
    "508": "Bão bụi mạnh",
    "509": "",
    "510": "",
    "511": "trong",
    "512": "",
    "513": "",
    "514": "",
    "515": "",
    "900": "",
    "901": "",
    "999": "không xác định",
}


def fetch_city_info(location, api_key, api_host):
    url = f"https://{api_host}/geo/v2/city/lookup?key={api_key}&location={location}&lang=zh"
    response = requests.get(url, headers=HEADERS).json()
    if response.get("error") is not None:
        logger.bind(tag=TAG).error(
            f"Lấy thông tin thành phố thất bại: {response.get('error', {}).get('detail')}"
        )
        return None
    return response.get("location", [])[0] if response.get("location") else None


def fetch_weather_page(url):
    response = requests.get(url, headers=HEADERS)
    return BeautifulSoup(response.text, "html.parser") if response.ok else None


def parse_weather_info(soup):
    city_name = soup.select_one("h1.c-submenu__location").get_text(strip=True)

    current_abstract = soup.select_one(".c-city-weather-current .current-abstract")
    current_abstract = (
        current_abstract.get_text(strip=True) if current_abstract else "không xác định"
    )

    current_basic = {}
    for item in soup.select(
        ".c-city-weather-current .current-basic .current-basic___item"
    ):
        parts = item.get_text(strip=True, separator=" ").split(" ")
        if len(parts) == 2:
            key, value = parts[1], parts[0]
            current_basic[key] = value

    temps_list = []
    for row in soup.select(".city-forecast-tabs__row")[:7]:  # 7củdữ liệu
        date = row.select_one(".date-bg .date").get_text(strip=True)
        weather_code = (
            row.select_one(".date-bg .icon")["src"].split("/")[-1].split(".")[0]
        )
        weather = WEATHER_CODE_MAP.get(weather_code, "không xác định")
        temps = [span.get_text(strip=True) for span in row.select(".tmp-cont .temp")]
        high_temp, low_temp = (temps[0], temps[-1]) if len(temps) >= 2 else (None, None)
        temps_list.append((date, weather, high_temp, low_temp))

    return city_name, current_abstract, current_basic, temps_list


@register_function("get_weather", GET_WEATHER_FUNCTION_DESC, ToolType.SYSTEM_CTL)
def get_weather(conn: "ConnectionHandler", location: str = None, lang: str = "vi_VN"):
    from core.utils.cache.manager import cache_manager, CacheType

    weather_config = conn.config.get("plugins", {}).get("get_weather", {})
    api_host = weather_config.get("api_host", "mj7p3y7naa.re.qweatherapi.com")
    api_key = weather_config.get("api_key", "a861d0d5e7bf4ee1a83d9a9e4f96d4da")
    default_location = weather_config.get("default_location", "")
    client_ip = conn.client_ip

    # ưu tiênlàm chosử dụngsử dụngcủlocationtham số
    if not location:
        # thông quamáy kháchIPphân tích
        if client_ip:
            # Lấy từ cache trướcIPvớicủthông tin
            cached_ip_info = cache_manager.get(CacheType.IP_INFO, client_ip)
            if cached_ip_info:
                location = cached_ip_info.get("city")
            else:
                # Cache miss, gọi API lấy vị trí theo IP.
                ip_info = get_ip_info(client_ip, logger)
                if ip_info:
                    cache_manager.set(CacheType.IP_INFO, client_ip, ip_info)
                    location = ip_info.get("city")

            if not location:
                location = default_location
        else:
            # Không có IP thì dùng vị trí mặc định.
            location = default_location
    # Cố gắng lấy báo cáo hoàn chỉnh từ cache.
    weather_cache_key = f"full_weather_{location}_{lang}"
    cached_weather_report = cache_manager.get(CacheType.WEATHER, weather_cache_key)
    if cached_weather_report:
        return ActionResponse(Action.REQLLM, cached_weather_report, None)

    # Không có cache thì lấy dữ liệu thời tiết mới.
    city_info = fetch_city_info(location, api_key, api_host)
    if not city_info:
        return ActionResponse(
            Action.REQLLM, f"Mình chưa tìm được thời tiết cho địa điểm: {location}. Bạn kiểm tra lại tên địa điểm nhé.", None
        )
    soup = fetch_weather_page(city_info["fxLink"])
    if not soup:
        return ActionResponse(Action.REQLLM, None, "Không lấy được dữ liệu thời tiết.")
    city_name, current_abstract, current_basic, temps_list = parse_weather_info(soup)

    weather_report = f"Địa điểm: {city_name}\n\nHiện tại: {current_abstract}\n"

    # Thêm các chỉ số hiện tại nếu có.
    if current_basic:
        weather_report += "Thông số:\n"
        for key, value in current_basic.items():
            if value != "0":
                weather_report += f"  · {key}: {value}\n"

    # Thêm dự báo 7 ngày.
    weather_report += "\nDự báo 7 ngày tới:\n"
    for date, weather, high, low in temps_list:
        weather_report += f"{date}: {weather}, {low}~{high}\n"

    weather_report += "\nHãy trả lời người dùng bằng tiếng Việt ngắn gọn, tự nhiên; không đọc toàn bộ bảng nếu họ chỉ hỏi nhanh."

    # Lưu báo cáo hoàn chỉnh vào cache.
    cache_manager.set(CacheType.WEATHER, weather_cache_key, weather_report)

    return ActionResponse(Action.REQLLM, weather_report, None)
