import random
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from config.logger import setup_logging
from plugins_func.register import register_function, ToolType, ActionResponse, Action
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler


TAG = __name__
logger = setup_logging()

GET_NEWS_FROM_CHINANEWS_FUNCTION_DESC = {
    "type": "function",
    "function": {
        "name": "get_news_from_chinanews",
        "description": (
            "Lấy một tin tức từ nguồn RSS cấu hình sẵn. Dùng khi người dùng hỏi tin mới, tin xã hội, thế giới hoặc tài chính. "
            "Nên ưu tiên nguồn tin phù hợp với Việt Nam trong cấu hình triển khai."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Chuyên mục tin tức, ví dụ xã hội, thế giới, tài chính. Nếu không truyền thì dùng chuyên mục mặc định.",
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


def fetch_news_from_rss(rss_url):
    """từRSSlấy"""
    try:
        response = requests.get(rss_url)
        response.raise_for_status()

        # phân tíchXML
        root = ET.fromstring(response.content)

        # cóitem（）
        news_items = []
        for item in root.findall(".//item"):
            title = (
                item.find("title").text if item.find("title") is not None else ""
            )
            link = item.find("link").text if item.find("link") is not None else "#"
            description = (
                item.find("description").text
                if item.find("description") is not None
                else ""
            )
            pubDate = (
                item.find("pubDate").text
                if item.find("pubDate") is not None
                else "không rõ thời gian"
            )

            news_items.append(
                {
                    "title": title,
                    "link": link,
                    "description": description,
                    "pubDate": pubDate,
                }
            )

        return news_items
    except Exception as e:
        logger.bind(tag=TAG).error(f"lấyRSSthất bại: {e}")
        return []


def fetch_news_detail(url):
    """lấybên trongvà"""
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # cố gắngbên trong (nàytrongcủcầntheo)
        content_div = soup.select_one(
            ".content_desc, .content, article, .article-content"
        )
        if content_div:
            paragraphs = content_div.find_all("p")
            content = "\n".join(
                [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
            )
            return content
        else:
            # nhưkhôngđếncủbên trong，thửlấycó
            paragraphs = soup.find_all("p")
            content = "\n".join(
                [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
            )
            return content[:2000]  # 
    except Exception as e:
        logger.bind(tag=TAG).error(f"Lấy nội dung tin thất bại: {e}")
        return "không lấy được nội dung"


def map_category(category_text):
    """Ánh xạ tên chuyên mục tiếng Việt sang key cấu hình RSS."""
    if not category_text:
        return None

    # ，sẽ、、，nhưhơnnhiều，cấu hìnhtệp
    category_map = {
        "xã hội": "society_rss_url",
        "xa hoi": "society_rss_url",
        "thế giới": "world_rss_url",
        "the gioi": "world_rss_url",
        "quốc tế": "world_rss_url",
        "quoc te": "world_rss_url",
        "tài chính": "finance_rss_url",
        "tai chinh": "finance_rss_url",
        "kinh tế": "finance_rss_url",
        "kinh te": "finance_rss_url",
    }

    # chuyển đổichovàđi
    normalized_category = category_text.lower().strip()

    # trả vềkết quả，nhưcókhớptrả vềban đầuvào
    return category_map.get(normalized_category, category_text)


@register_function(
    "get_news_from_chinanews",
    GET_NEWS_FROM_CHINANEWS_FUNCTION_DESC,
    ToolType.SYSTEM_CTL,
)
def get_news_from_chinanews(
    conn: "ConnectionHandler",
    category: str = None,
    detail: bool = False,
    lang: str = "vi_VN",
):
    """Lấy tin tức RSS hoặc nội dung chi tiết của tin vừa chọn."""
    try:
        # nhưdetailchoTrue，lấytrêncủbên trong
        if detail:
            if (
                not hasattr(conn, "last_news_link")
                or not conn.last_news_link
                or "link" not in conn.last_news_link
            ):
                return ActionResponse(
                    Action.REQLLM,
                    "Chưa có tin nào trước đó để lấy nội dung chi tiết.",
                    None,
                )

            link = conn.last_news_link.get("link")
            title = conn.last_news_link.get("title", "không rõ tiêu đề")

            if link == "#":
                return ActionResponse(
                    Action.REQLLM, "Tin trước đó không có liên kết chi tiết khả dụng.", None
                )

            logger.bind(tag=TAG).debug(f"lấy: {title}, URL={link}")

            # lấy
            detail_content = fetch_news_detail(link)

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
                f"Nội dung: {detail_content}\n\n"
                "Trả lời ngắn gọn, nêu ý chính và tránh khẳng định vượt quá nội dung nguồn."
            )

            return ActionResponse(Action.REQLLM, detail_report, None)

        # ，lấyvà
        # từcấu hìnhtronglấyRSS URL
        rss_config = conn.config.get("plugins", {}).get("get_news_from_chinanews", {})
        default_rss_url = rss_config.get(
            "default_rss_url", "https://www.chinanews.com.cn/rss/society.xml"
        )

        # sẽsử dụngvàocủđếncấu hìnhtrongcủ
        mapped_category = map_category(category)

        # như，thửtừcấu hìnhtronglấyvớicủURL
        rss_url = default_rss_url
        if mapped_category and mapped_category in rss_config:
            rss_url = rss_config[mapped_category]

        logger.bind(tag=TAG).info(
            f"lấy: ban đầu={category}, ={mapped_category}, URL={rss_url}"
        )

        # lấy
        news_items = fetch_news_from_rss(rss_url)

        if not news_items:
            return ActionResponse(
                Action.REQLLM, "Mình chưa lấy được tin tức từ nguồn cấu hình, bạn thử lại sau nhé.", None
            )

        # 
        selected_news = random.choice(news_items)

        # lưuhiện tạiđếnkết nốivới，bằngsau
        if not hasattr(conn, "last_news_link"):
            conn.last_news_link = {}
        conn.last_news_link = {
            "link": selected_news.get("link", "#"),
            "title": selected_news.get("title", "không rõ tiêu đề"),
        }

        # xây dựngbáo cáo
        news_report = (
            f"Hãy dùng ngôn ngữ {lang} để đọc tin này cho người dùng Việt Nam:\n\n"
            f"Tiêu đề: {selected_news['title']}\n"
            f"Thời gian: {selected_news['pubDate']}\n"
            f"Tóm tắt nguồn: {selected_news['description']}\n"
            "Trả lời ngắn gọn. Nếu người dùng muốn biết thêm, họ có thể hỏi chi tiết tin này."
        )

        return ActionResponse(Action.REQLLM, news_report, None)

    except Exception as e:
        logger.bind(tag=TAG).error(f"lấyra: {e}")
        return ActionResponse(
            Action.REQLLM, "Mình gặp lỗi khi lấy tin tức, bạn thử lại sau nhé.", None
        )
