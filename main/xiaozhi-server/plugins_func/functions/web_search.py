import requests
from config.logger import setup_logging
from plugins_func.register import (
    register_function,
    ToolType,
    ActionResponse,
    Action,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

TAG = __name__
logger = setup_logging()

_DEFAULT_DESCRIPTION = (
    "Công cụ tìm kiếm trực tuyến. Sử dụng khi cần tìm kiếm thông tin mới nhất trên mạng."
)

WEB_SEARCH_FUNCTION_DESC = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": _DEFAULT_DESCRIPTION,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Câu truy vấn tìm kiếm hoặc từ khóa cần tìm",
                }
            },
            "required": ["query"],
        },
    },
}


def _search_metaso(config: dict, query: str, max_results: int) -> str:
    """Sử dụng API tìm kiếm Metaso"""
    api_key = config.get("api_key", "")
    if not api_key:
        raise ValueError("Công cụ tìm kiếm Metaso chưa được cấu hình API Key. Vui lòng kiểm tra file cấu hình.")

    url = "https://metaso.cn/api/v1/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "q": query,
        "size": max_results,
        "stream": False,
        "scope": "webpage",
        "includeSummary": True,
        "includeRawContent": False,
        "conciseSnippet": False,
    }
    logger.bind(tag=TAG).debug(f"Yêu cầu tìm kiếm Metaso | URL: {url} | payload: {payload}")
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    logger.bind(tag=TAG).debug(f"Phản hồi tìm kiếm Metaso | status: {response.status_code}")

    webpages = data.get("webpages", [])
    if not webpages:
        return "Không tìm thấy kết quả tìm kiếm."

    lines = ["【Kết quả tìm kiếm】"]
    for i, item in enumerate(webpages, 1):
        title = item.get("title", "")
        snippet = item.get("summary", "")
        date = item.get("date", "")
        lines.append(f"{i}. Tiêu đề: {title}")
        if date:
            lines.append(f"   Ngày: {date}")
        if snippet:
            lines.append(f"   Tóm tắt: {snippet}")

    return "\n".join(lines)


def _search_tavily(config: dict, query: str, max_results: int) -> str:
    """Sử dụng API tìm kiếm Tavily"""
    api_key = config.get("api_key", "")
    if not api_key:
        raise ValueError("Công cụ tìm kiếm Tavily chưa được cấu hình API Key. Vui lòng kiểm tra file cấu hình.")

    url = "https://api.tavily.com/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": query,
        "max_results": max_results,
        "search_depth": "advanced",
        "include_answer": "advanced",
    }
    logger.bind(tag=TAG).debug(f"Yêu cầu tìm kiếm Tavily | URL: {url} | payload: {payload}")
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    logger.bind(tag=TAG).debug(f"Phản hồi tìm kiếm Tavily | status: {response.status_code} | data: {data}")

    results = data.get("results", [])
    if not results:
        return "Không tìm thấy kết quả tìm kiếm."

    answer = data.get("answer", "")
    lines = [f"【Kết quả tìm kiếm】\nTóm tắt: {answer}"]
    return "\n".join(lines)


def _item_value(item: dict, *keys: str) -> str:
    for key in keys:
        value = item.get(key)
        if value:
            return str(value)
    return ""


def _normalize_results(data: dict) -> list:
    for key in ("results", "webpages", "items", "data"):
        value = data.get(key)
        if isinstance(value, list):
            return value
    return []


def _search_9router(
    config: dict,
    query: str,
    max_results: int,
) -> str:
    """Gọi endpoint tìm kiếm kiểu OpenAI của 9Router/NRouter."""
    api_key = config.get("api_key", "")
    if not api_key:
        raise ValueError("Công cụ tìm kiếm 9Router chưa được cấu hình API Key. Vui lòng kiểm tra file cấu hình.")

    base_url = config.get("base_url") or config.get("url")
    if not base_url:
        raise ValueError("Công cụ tìm kiếm 9Router chưa được cấu hình base_url.")

    model = config.get("model", "searxng")
    search_type = config.get("search_type", "web")

    url = f"{base_url.rstrip('/')}/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "query": query,
        "search_type": search_type,
        "max_results": max_results,
    }
    logger.bind(tag=TAG).debug(f"Yêu cầu tìm kiếm 9Router | URL: {url} | payload: {payload}")
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()

    answer = data.get("answer") or data.get("summary")
    results = _normalize_results(data)
    logger.bind(tag=TAG).debug(
        f"Phản hồi tìm kiếm 9Router | status: {response.status_code} | "
        f"keys: {list(data.keys())} | results: {len(results)}"
    )
    if not answer and not results:
        return "Không tìm thấy kết quả."

    lines = ["【Kết quả tìm kiếm】"]
    if answer:
        lines.append(str(answer))

    for index, item in enumerate(results, 1):
        if not isinstance(item, dict):
            lines.append(f"{index}. {item}")
            continue

        title = _item_value(item, "title", "name")
        url_value = _item_value(item, "url", "link", "href")
        snippet = _item_value(item, "snippet", "content", "summary", "description")
        date = _item_value(item, "date", "published_date", "publishedAt")

        label = title or url_value or snippet
        if label:
            lines.append(f"{index}. {label}")
        if url_value and url_value != label:
            lines.append(f"   URL: {url_value}")
        if date:
            lines.append(f"   Ngày: {date}")
        if snippet and snippet != label:
            lines.append(f"   Tóm tắt: {snippet}")

    return "\n".join(lines)


PROVIDER_REGISTRY = {
    "metaso": _search_metaso,
    "tavily": _search_tavily,
    "9router": _search_9router,
    "nrouter": _search_9router,
}


@register_function("web_search", WEB_SEARCH_FUNCTION_DESC, ToolType.SYSTEM_CTL)
def web_search(conn: "ConnectionHandler", query: str = None):
    logger.bind(tag=TAG).info(f"web_search được sử dụng | query={query}")
    if not query:
        return ActionResponse(Action.REQLLM, "Vui lòng nhập từ khóa tìm kiếm.", None)

    web_search_config = conn.config.get("plugins", {}).get("web_search", {})
    provider = web_search_config.get("provider", "").lower()
    max_results = int(web_search_config.get("max_results", 3))
    logger.bind(tag=TAG).info(
        f"Cấu hình web_search | provider={provider} | max_results={max_results} | config_keys={list(web_search_config.keys())}"
    )

    search_fn = PROVIDER_REGISTRY.get(provider)
    if not search_fn:
        return ActionResponse(
            Action.REQLLM,
            f"Nhà cung cấp dịch vụ tìm kiếm không hợp lệ hoặc chưa được cấu hình (hiện tại: {provider}). Vui lòng kiểm tra lại cấu hình.",
            None,
        )

    try:
        result_text = search_fn(web_search_config, query, max_results)
        logger.bind(tag=TAG).info(f"Kết quả tìm kiếm hoàn thành:\n{result_text}")
    except ValueError as e:
        logger.bind(tag=TAG).error(f"Lỗi cấu hình tìm kiếm: {e}")
        result_text = str(e)
    except requests.exceptions.Timeout:
        logger.bind(tag=TAG).error("Yêu cầu tìm kiếm bị quá thời gian")
        result_text = "Yêu cầu tìm kiếm bị quá thời gian, vui lòng thử lại sau."
    except requests.exceptions.RequestException as e:
        logger.bind(tag=TAG).error(f"Yêu cầu tìm kiếm thất bại: {e}")
        result_text = "Yêu cầu tìm kiếm thất bại, vui lòng thử lại sau."
    except Exception as e:
        logger.bind(tag=TAG).error(f"Lỗi ngoại lệ tìm kiếm: {e}")
        result_text = "Xảy ra lỗi ngoại lệ khi tìm kiếm, vui lòng thử lại sau."

    return ActionResponse(Action.REQLLM, result_text, None)
