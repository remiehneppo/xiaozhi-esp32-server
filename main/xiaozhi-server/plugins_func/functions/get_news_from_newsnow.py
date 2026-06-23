import random
import requests
import json
from config.logger import setup_logging
from plugins_func.register import register_function, ToolType, ActionResponse, Action
from markitdown import MarkItDown
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler


TAG = __name__
logger = setup_logging()

CHANNEL_MAP = {
    "V2EX": "v2ex-share",
    "Zhihu": "zhihu",
    "Weibo": "weibo",
    "Zaobao": "zaobao",
    "Coolapk": "coolapk",
    "MKTNews": "mktnews-flash",
    "WallstreetCN": "wallstreetcn-quick",
    "36": "36kr-quick",
    "Douyin": "douyin",
    "Hupu": "hupu",
    "Tieba": "tieba",
    "Toutiao": "toutiao",
    "IT": "ithome",
    "The Paper": "thepaper",
    "Sputnik CN": "sputniknewscn",
    "Tin tham khảo": "cankaoxiaoxi",
    "Windows 11": "pcbeta-windows11",
    "CLS": "cls-depth",
    "Xueqiu": "xueqiu-hotstock",
    "Gelonghui": "gelonghui",
    "FastBull": "fastbull-express",
    "Solidot": "solidot",
    "Hacker News": "hackernews",
    "Product Hunt": "producthunt",
    "Github": "github-trending-today",
    "Bilibili": "bilibili-hot-search",
    "Kuaishou": "kuaishou",
    "Kaopu": "kaopu",
    "Jin10": "jin10",
    "Baidu": "baidu",
    "Nowcoder": "nowcoder",
    "SSPai": "sspai",
    "Juejin": "juejin",
    "Ifeng": "ifeng",
    "Chongbuluo": "chongbuluo-latest",
}

# Nguồn mặc định; có thể ghi đè bằng cấu hình plugins.get_news_from_newsnow.news_sources.
DEFAULT_NEWS_SOURCES = "Hacker News;Product Hunt;Github;IT"

def _get_newsnow_config(conn):
    # từkết nốicấu hìnhlấy
    plugins = conn.config.get("plugins", {})
    newsnow = plugins.get("get_news_from_newsnow", {})
    sources = newsnow.get("news_sources", "")
    if isinstance(sources, str) and sources.strip():
        return sources

    return ""

def get_news_sources_from_config(conn):
    """Lấy danh sách nguồn tin từ cấu hình."""
    try:
        result = _get_newsnow_config(conn)
        if result:
            logger.bind(tag=TAG).debug(f"Dùng nguồn tin từ cấu hình: {result}")
            return result

        logger.bind(tag=TAG).debug("Không có cấu hình nguồn tin, dùng mặc định")
        return DEFAULT_NEWS_SOURCES

    except Exception as e:
        logger.bind(tag=TAG).error(f"Lấy cấu hình nguồn tin thất bại: {e}, dùng mặc định")
        return DEFAULT_NEWS_SOURCES


# từmặc địnhcấu hìnhlấykhả dụngcủ（khi/thờiget_news_sources_from_configlấy）
example_sources_str = DEFAULT_NEWS_SOURCES.replace(";","、")

GET_NEWS_FROM_NEWSNOW_FUNCTION_DESC = {
    "type": "function",
    "function": {
        "name": "get_news_from_newsnow",
        "description": "Lấy một tin mới từ NewsNow theo nguồn cấu hình sẵn. Dùng khi người dùng hỏi tin mới, xu hướng công nghệ, tin GitHub hoặc nguồn cụ thể.",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": f"Tên nguồn tin, ví dụ {example_sources_str}. Nếu không truyền thì dùng nguồn mặc định.",
                },
                "detail": {
                    "type": "boolean",
                    "description": "Có lấy nội dung chi tiết của tin vừa đọc không. Mặc định false.",
                },
                "lang": {
                    "type": "string",
                    "description": "Mã ngôn ngữ trả lời, ví dụ vi_VN hoặc en_US. Mặc định vi_VN.",
                },
            },
            "required": ["lang"],
        },
    },
}


def fetch_news_from_api(conn: "ConnectionHandler", source="thepaper"):
    """Lấy tin từ NewsNow API."""
    try:
        api_url = f"https://newsnow.busiyi.world/api/s?id={source}"

        news_config = conn.config.get("plugins", {}).get("get_news_from_newsnow", {})
        if news_config.get("url"):
            api_url = news_config["url"] + source

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "items" in data:
            return data["items"]
        else:
            logger.bind(tag=TAG).error(f"Phản hồi API tin tức sai định dạng: {data}")
            return []

    except Exception as e:
        logger.bind(tag=TAG).error(f"Lấy API tin tức thất bại: {e}")
        return []


def fetch_news_detail(url):
    """Lấy nội dung chi tiết và dùng MarkItDown để dọn HTML."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # sử dụngMarkItDowndọn dẹpHTMLbên trong
        md = MarkItDown(enable_plugins=False)
        result = md.convert(response)

        # lấydọn dẹpsaucủvăn bảnbên trong
        clean_text = result.text_content

        # nhưdọn dẹpsaucủbên trongcho，trả vềgợi ýthông tin
        if not clean_text or len(clean_text.strip()) == 0:
            logger.bind(tag=TAG).warning(f"Nội dung sau khi dọn rỗng: {url}")
            return "Không phân tích được nội dung chi tiết."

        return clean_text
    except Exception as e:
        logger.bind(tag=TAG).error(f"Lấy nội dung tin thất bại: {e}")
        return "không lấy được nội dung"


@register_function(
    "get_news_from_newsnow",
    GET_NEWS_FROM_NEWSNOW_FUNCTION_DESC,
    ToolType.SYSTEM_CTL,
)
def get_news_from_newsnow(
    conn: "ConnectionHandler",
    source: str = "",
    detail: bool = False,
    lang: str = "vi_VN",
):
    """Lấy tin NewsNow hoặc nội dung chi tiết của tin vừa chọn."""
    try:
        # lấyhiện tạicấu hìnhcủ
        news_sources = get_news_sources_from_config(conn)

        # nhưdetailchoTrue，lấytrêncủbên trong
        detail = str(detail).lower() == "true"
        if detail:
            if (
                not hasattr(conn, "last_newsnow_link")
                or not conn.last_newsnow_link
                or "url" not in conn.last_newsnow_link
            ):
                return ActionResponse(
                    Action.REQLLM,
                    "Chưa có tin nào trước đó để lấy nội dung chi tiết.",
                    None,
                )

            url = conn.last_newsnow_link.get("url")
            title = conn.last_newsnow_link.get("title", "không rõ tiêu đề")
            source_id = conn.last_newsnow_link.get("source_id", "thepaper")
            source_name = CHANNEL_MAP.get(source_id, "không rõ nguồn")

            if not url or url == "#":
                return ActionResponse(
                    Action.REQLLM, "Tin trước đó không có liên kết chi tiết khả dụng.", None
                )

            logger.bind(tag=TAG).debug(
                f"lấy: {title}, đến: {source_name}, URL={url}"
            )

            # lấy
            detail_content = fetch_news_detail(url)

            if not detail_content or detail_content == "không lấy được nội dung":
                return ActionResponse(
                    Action.REQLLM,
                    f"Mình chưa lấy được nội dung chi tiết của tin \"{title}\".",
                    None,
                )

            # xây dựngbáo cáo
            detail_report = (
                f"Hãy dùng ngôn ngữ {lang} để tóm tắt tin sau cho người dùng Việt Nam:\n\n"
                f"Tiêu đề: {title}\n"
                # f"đến: {source_name}\n"
                f"Nội dung: {detail_content}\n\n"
                "Trả lời ngắn gọn, nêu ý chính và tránh khẳng định vượt quá nội dung nguồn."
            )

            return ActionResponse(Action.REQLLM, detail_report, None)

        # ，lấyvà
        # sẽtrongchuyển đổichoID
        english_source_id = None

        # Kiểm tra nguồn người dùng yêu cầu có nằm trong cấu hình không.
        news_sources_list = [
            name.strip() for name in news_sources.split(";") if name.strip()
        ]
        if source in news_sources_list:
            # Nếu nguồn nằm trong cấu hình thì ánh xạ sang ID NewsNow.
            english_source_id = CHANNEL_MAP.get(source)

        # Nếu không khớp nguồn, dùng mặc định.
        if not english_source_id:
            logger.bind(tag=TAG).warning(f"Nguồn tin không hợp lệ: {source}, dùng mặc định")
            english_source_id = "thepaper"
            source = ""

        logger.bind(tag=TAG).info(f"Lấy tin: source={source}({english_source_id})")

        # lấy
        news_items = fetch_news_from_api(conn, english_source_id)

        if not news_items:
            return ActionResponse(
                Action.REQLLM,
                f"Mình chưa lấy được tin từ nguồn {source or english_source_id}, bạn thử lại sau hoặc chọn nguồn khác nhé.",
                None,
            )

        # 
        selected_news = random.choice(news_items)

        # lưuhiện tạiđếnkết nốivới，bằngsau
        if not hasattr(conn, "last_newsnow_link"):
            conn.last_newsnow_link = {}
        conn.last_newsnow_link = {
            "url": selected_news.get("url", "#"),
            "title": selected_news.get("title", "không rõ tiêu đề"),
            "source_id": english_source_id,
        }

        # xây dựngbáo cáo
        news_report = (
            f"Hãy dùng ngôn ngữ {lang} để đọc tin này cho người dùng Việt Nam:\n\n"
            f"Tiêu đề: {selected_news['title']}\n"
            # f"đến: {source}\n"
            "Trả lời ngắn gọn. Nếu người dùng muốn biết thêm, họ có thể hỏi chi tiết tin này."
        )

        return ActionResponse(Action.REQLLM, news_report, None)

    except Exception as e:
        logger.bind(tag=TAG).error(f"Lấy tin NewsNow lỗi: {e}")
        return ActionResponse(
            Action.REQLLM, "Mình gặp lỗi khi lấy tin tức, bạn thử lại sau nhé.", None
        )
