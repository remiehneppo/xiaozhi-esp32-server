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
            "sử dụngphảihoặckhi/thờisử dụng（như'đến''cógì'）。"
            "sử dụngcó thểchỉ định，nhưsẽ、、v.v.。"
            "nhưcóchỉ định，mặc địnhsẽ。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "，nhưsẽ、、。tùy chọntham số，nhưkhônglàm chosử dụngmặc định",
                },
                "detail": {
                    "type": "boolean",
                    "description": "làlấybên trong，mặc địnhchofalse。nhưchotrue，lấytrêncủbên trong",
                },
                "lang": {
                    "type": "string",
                    "description": "Ngôn ngữ code user sử dụng trả về, ví dụ zh_CN/zh_HK/en_US/ja_JP v.v., mặc định zh_CN",
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
                else "không xác địnhkhi/thời"
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
        logger.bind(tag=TAG).error(f"lấythất bại: {e}")
        return "lấybên trong"


def map_category(category_text):
    """sẽsử dụngvàocủtrongđếncấu hìnhtệptrongcủ"""
    if not category_text:
        return None

    # ，sẽ、、，nhưhơnnhiều，cấu hìnhtệp
    category_map = {
        # sẽ
        "sẽ": "society_rss_url",
        "sẽ": "society_rss_url",
        # 
        "": "world_rss_url",
        "": "world_rss_url",
        # 
        "": "finance_rss_url",
        "": "finance_rss_url",
        "": "finance_rss_url",
        "": "finance_rss_url",
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
    lang: str = "zh_CN",
):
    """lấyvàtiến hành，hoặclấytrêncủbên trong"""
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
                    "，cóđếncủ，lấy。",
                    None,
                )

            link = conn.last_news_link.get("link")
            title = conn.last_news_link.get("title", "không xác định")

            if link == "#":
                return ActionResponse(
                    Action.REQLLM, "，cókhả dụngcủlấybên trong。", None
                )

            logger.bind(tag=TAG).debug(f"lấy: {title}, URL={link}")

            # lấy
            detail_content = fetch_news_detail(link)

            if not detail_content or detail_content == "lấybên trong":
                return ActionResponse(
                    Action.REQLLM,
                    f"，lấy《{title}》củbên trong，có thểlàđãhoặc。",
                    None,
                )

            # xây dựngbáo cáo
            detail_report = (
                f"theodữ liệu，sử dụng{lang}sử dụngcủyêu cầu：\n\n"
                f": {title}\n"
                f"bên trong: {detail_content}\n\n"
                f"(vớitrênbên trongtiến hành，thông tin，bằng、củphương thứchướngsử dụng，"
                f"khôngphảivà/cũngnàylà，thìlàtại/trongmộthoàn chỉnhcủ)"
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
                Action.REQLLM, "，có thểlấyđếnthông tin，sau。", None
            )

        # 
        selected_news = random.choice(news_items)

        # lưuhiện tạiđếnkết nốivới，bằngsau
        if not hasattr(conn, "last_news_link"):
            conn.last_news_link = {}
        conn.last_news_link = {
            "link": selected_news.get("link", "#"),
            "title": selected_news.get("title", "không xác định"),
        }

        # xây dựngbáo cáo
        news_report = (
            f"theodữ liệu，sử dụng{lang}sử dụngcủyêu cầu：\n\n"
            f": {selected_news['title']}\n"
            f"khi/thời: {selected_news['pubDate']}\n"
            f"bên trong: {selected_news['description']}\n"
            f"(bằng、củphương thứchướngsử dụngnày，có thểbên trong，"
            f"ra，khôngcầnbên ngoàinhiềucủbên trong。"
            f"nhưsử dụnghơnnhiều，sử dụngcó thểnói'này'lấyhơnnhiềubên trong)"
        )

        return ActionResponse(Action.REQLLM, news_report, None)

    except Exception as e:
        logger.bind(tag=TAG).error(f"lấyra: {e}")
        return ActionResponse(
            Action.REQLLM, "，lấykhi/thờisai，sau。", None
        )
