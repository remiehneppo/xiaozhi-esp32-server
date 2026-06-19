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
    "tìm kiếmcông cụ。sử dụngcầntìm kiếmthờilàm chosử dụngnàycông cụ。"
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
                    "description": "tìm kiếmhoặc",
                }
            },
            "required": ["query"],
        },
    },
}


def _search_metaso(api_key: str, query: str, max_results: int) -> str:
    """sử dụngtìm kiếmAPI"""
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
    logger.bind(tag=TAG).debug(f"tìm kiếmyêu cầu | URL: {url} | payload: {payload}")
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    logger.bind(tag=TAG).debug(f"tìm kiếmphản hồi | status: {response.status_code}")

    webpages = data.get("webpages", [])
    if not webpages:
        return "đếntìm kiếmkết quả。"

    lines = ["【tìm kiếmkết quả】"]
    for i, item in enumerate(webpages, 1):
        title = item.get("title", "")
        snippet = item.get("summary", "")
        date = item.get("date", "")
        lines.append(f"{i}. ：{title}")
        if date:
            lines.append(f"   ：{date}")
        if snippet:
            lines.append(f"   phải：{snippet}")

    return "\n".join(lines)


def _search_tavily(api_key: str, query: str, max_results: int) -> str:
    """sử dụngTavilytìm kiếmAPI"""
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
    logger.bind(tag=TAG).debug(f"Tavilytìm kiếmyêu cầu | URL: {url} | payload: {payload}")
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    logger.bind(tag=TAG).debug(f"Tavilytìm kiếmphản hồi | status: {response.status_code} | data: {data}")

    results = data.get("results", [])
    if not results:
        return "đếntìm kiếmkết quả。"

    answer = data.get("answer", "")
    lines = [f"【tìm kiếmkết quả】\n：{answer}"]
    # for i, item in enumerate(results, 1):
    #     title = item.get("title", "")
    #     summary = item.get("content", "")
    #     lines.append(f"{i}. ：{title}")
    #     if summary:
    #         lines.append(f"   phải：{summary}")

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
    base_url: str,
    api_key: str,
    model: str,
    query: str,
    search_type: str,
    max_results: int,
) -> str:
    """Call 9Router/NRouter OpenAI-style search endpoint."""
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
    logger.bind(tag=TAG).debug(f"9Router tìm kiếm yêu cầu | URL: {url} | payload: {payload}")
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    logger.bind(tag=TAG).debug(f"9Router tìm kiếm phản hồi | status: {response.status_code} | data: {data}")

    answer = data.get("answer") or data.get("summary")
    results = _normalize_results(data)
    if not answer and not results:
        return "Không tìm thấy kết quả."

    lines = ["【kết quả tìm kiếm】"]
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


@register_function("web_search", WEB_SEARCH_FUNCTION_DESC, ToolType.SYSTEM_CTL)
def web_search(conn: "ConnectionHandler", query: str = None):
    logger.bind(tag=TAG).info(f"web_search bịsử dụng | query={query}")
    if not query:
        return ActionResponse(Action.REQLLM, "tìm kiếm。", None)

    web_search_config = conn.config.get("plugins", {}).get("web_search", {})
    provider = web_search_config.get("provider", "").lower()
    max_results = int(web_search_config.get("max_results", 3))
    logger.bind(tag=TAG).info(f"web_search cấu hình | provider={provider} | max_results={max_results} | config_keys={list(web_search_config.keys())}")

    api_key = web_search_config.get("api_key", "")
    if not api_key:
        return ActionResponse(
            Action.REQLLM,
            "tìm kiếmcó thểcấu hìnhAPI Key，tạicấu hìnhtệptrong。",
            None,
        )

    if provider == "metaso":
        search_fn = lambda: _search_metaso(api_key, query, max_results)
    elif provider == "tavily":
        search_fn = lambda: _search_tavily(api_key, query, max_results)
    elif provider in ("9router", "nrouter"):
        base_url = web_search_config.get("base_url") or web_search_config.get("url")
        if not base_url:
            return ActionResponse(
                Action.REQLLM,
                "tìm kiếm 9Router chưa cấu hình base_url。",
                None,
            )
        model = web_search_config.get("model", "searxng")
        search_type = web_search_config.get("search_type", "web")
        search_fn = lambda: _search_9router(
            base_url, api_key, model, query, search_type, max_results
        )
    else:
        return ActionResponse(
            Action.REQLLM,
            f"tìm kiếmcó thểcấu hìnhhoặccấu hìnhtìm kiếmkhông hợp lệ（hiện tại：{provider}），kiểm tracấu hình。",
            None,
        )

    try:
        result_text = search_fn()
        logger.bind(tag=TAG).info(f"tìm kiếmkết quảhoàn thành:\n{result_text}")
    except requests.exceptions.Timeout:
        logger.bind(tag=TAG).error("tìm kiếmyêu cầuquá thời gian")
        result_text = "tìm kiếmyêu cầuquá thời gian，sauthử lại。"
    except requests.exceptions.RequestException as e:
        logger.bind(tag=TAG).error(f"tìm kiếmyêu cầuthất bại: {e}")
        result_text = "tìm kiếmyêu cầuthất bại，sauthử lại。"
    except Exception as e:
        logger.bind(tag=TAG).error(f"tìm kiếmngoại lệ: {e}")
        result_text = "tìm kiếmrangoại lệ，sauthử lại。"

    return ActionResponse(Action.REQLLM, result_text, None)
