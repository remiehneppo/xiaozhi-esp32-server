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
    "": "zhihu",
    "": "weibo",
    "": "zaobao",
    "": "coolapk",
    "MKTNews": "mktnews-flash",
    "": "wallstreetcn-quick",
    "36": "36kr-quick",
    "": "douyin",
    "": "hupu",
    "": "tieba",
    "": "toutiao",
    "IT": "ithome",
    "": "thepaper",
    "": "sputniknewscn",
    "tin nhắn": "cankaoxiaoxi",
    "": "pcbeta-windows11",
    "": "cls-depth",
    "": "xueqiu-hotstock",
    "": "gelonghui",
    "": "fastbull-express",
    "Solidot": "solidot",
    "Hacker News": "hackernews",
    "Product Hunt": "producthunt",
    "Github": "github-trending-today",
    "": "bilibili-hot-search",
    "": "kuaishou",
    "": "kaopu",
    "dữ liệu": "jin10",
    "": "baidu",
    "": "nowcoder",
    "": "sspai",
    "": "juejin",
    "": "ifeng",
    "": "chongbuluo-latest",
}

# mặc địnhđến，cấu hìnhtrongcóchỉ địnhkhi/thờilàm chosử dụng
DEFAULT_NEWS_SOURCES = ";;"

def _get_newsnow_config(conn):
    # từkết nốicấu hìnhlấy
    plugins = conn.config.get("plugins", {})
    newsnow = plugins.get("get_news_from_newsnow", {})
    sources = newsnow.get("news_sources", "")
    if isinstance(sources, str) and sources.strip():
        return sources

    return ""

def get_news_sources_from_config(conn):
    """từcấu hìnhtronglấyký tự"""
    try:
        result = _get_newsnow_config(conn)
        if result:
            logger.bind(tag=TAG).debug(f"làm chosử dụngcấu hìnhcủ: {result}")
            return result

        logger.bind(tag=TAG).debug("đếncấu hình，làm chosử dụngmặc địnhcấu hình")
        return DEFAULT_NEWS_SOURCES

    except Exception as e:
        logger.bind(tag=TAG).error(f"lấycấu hìnhthất bại: {e}，làm chosử dụngmặc địnhcấu hình")
        return DEFAULT_NEWS_SOURCES


# từmặc địnhcấu hìnhlấykhả dụngcủ（khi/thờiget_news_sources_from_configlấy）
example_sources_str = DEFAULT_NEWS_SOURCES.replace(";","、")

GET_NEWS_FROM_NEWSNOW_FUNCTION_DESC = {
    "type": "function",
    "function": {
        "name": "get_news_from_newsnow",
        "description": "sử dụngphảihoặckhi/thờisử dụng（như'đến''cógì'）。",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": f"củtrong，như{example_sources_str}v.v.。tùy chọntham số，nhưkhônglàm chosử dụngmặc định",
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


def fetch_news_from_api(conn: "ConnectionHandler", source="thepaper"):
    """từAPIlấy"""
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
            logger.bind(tag=TAG).error(f"lấyAPIphản hồiđịnh dạngsai: {data}")
            return []

    except Exception as e:
        logger.bind(tag=TAG).error(f"lấyAPIthất bại: {e}")
        return []


def fetch_news_detail(url):
    """lấybên trongvàlàm chosử dụngMarkItDowndọn dẹpHTML"""
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
            logger.bind(tag=TAG).warning(f"dọn dẹpsaucủbên trongcho: {url}")
            return "phân tíchbên trong，có thểlàhoặcbên trong。"

        return clean_text
    except Exception as e:
        logger.bind(tag=TAG).error(f"lấythất bại: {e}")
        return "lấybên trong"


@register_function(
    "get_news_from_newsnow",
    GET_NEWS_FROM_NEWSNOW_FUNCTION_DESC,
    ToolType.SYSTEM_CTL,
)
def get_news_from_newsnow(
    conn: "ConnectionHandler",
    source: str = "",
    detail: bool = False,
    lang: str = "zh_CN",
):
    """lấyvàtiến hành，hoặclấytrêncủbên trong"""
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
                    "，cóđếncủ，lấy。",
                    None,
                )

            url = conn.last_newsnow_link.get("url")
            title = conn.last_newsnow_link.get("title", "không xác định")
            source_id = conn.last_newsnow_link.get("source_id", "thepaper")
            source_name = CHANNEL_MAP.get(source_id, "không xác địnhđến")

            if not url or url == "#":
                return ActionResponse(
                    Action.REQLLM, "，cókhả dụngcủlấybên trong。", None
                )

            logger.bind(tag=TAG).debug(
                f"lấy: {title}, đến: {source_name}, URL={url}"
            )

            # lấy
            detail_content = fetch_news_detail(url)

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
                # f"đến: {source_name}\n"
                f"bên trong: {detail_content}\n\n"
                f"(vớitrênbên trongtiến hành，thông tin，bằng、củphương thứchướngsử dụng，"
                f"khôngphảivà/cũngnàylà，thìlàtại/trongmộthoàn chỉnhcủ)"
            )

            return ActionResponse(Action.REQLLM, detail_report, None)

        # ，lấyvà
        # sẽtrongchuyển đổichoID
        english_source_id = None

        # kiểm travàocủtronglàtại/trongcấu hìnhcủtrong
        news_sources_list = [
            name.strip() for name in news_sources.split(";") if name.strip()
        ]
        if source in news_sources_list:
            # nhưvàocủtrongtại/trongcấu hìnhcủtrong，tại/trong CHANNEL_MAP trongvớicủID
            english_source_id = CHANNEL_MAP.get(source)

        # nhưkhôngđếnvớicủID，làm chosử dụngmặc định
        if not english_source_id:
            logger.bind(tag=TAG).warning(f"không hiệu quảcủ: {source}，làm chosử dụngmặc định")
            english_source_id = "thepaper"
            source = ""

        logger.bind(tag=TAG).info(f"lấy: ={source}({english_source_id})")

        # lấy
        news_items = fetch_news_from_api(conn, english_source_id)

        if not news_items:
            return ActionResponse(
                Action.REQLLM,
                f"，có thểtừ{source}lấyđếnthông tin，sauhoặcthửnó/của nó。",
                None,
            )

        # 
        selected_news = random.choice(news_items)

        # lưuhiện tạiđếnkết nốivới，bằngsau
        if not hasattr(conn, "last_newsnow_link"):
            conn.last_newsnow_link = {}
        conn.last_newsnow_link = {
            "url": selected_news.get("url", "#"),
            "title": selected_news.get("title", "không xác định"),
            "source_id": english_source_id,
        }

        # xây dựngbáo cáo
        news_report = (
            f"theodữ liệu，sử dụng{lang}sử dụngcủyêu cầu：\n\n"
            f": {selected_news['title']}\n"
            # f"đến: {source}\n"
            f"(bằng、củphương thứchướngsử dụngnày，"
            f"gợi ýsử dụngcó thểphảilấybên trong，nàykhi/thờisẽlấycủbên trong。)"
        )

        return ActionResponse(Action.REQLLM, news_report, None)

    except Exception as e:
        logger.bind(tag=TAG).error(f"lấyra: {e}")
        return ActionResponse(
            Action.REQLLM, "，lấykhi/thờisai，sau。", None
        )
