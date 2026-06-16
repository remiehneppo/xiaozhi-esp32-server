import requests
import sys
from config.logger import setup_logging
from plugins_func.register import register_function, ToolType, ActionResponse, Action
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

TAG = __name__
logger = setup_logging()

# định nghĩahàm
SEARCH_FROM_RAGFLOW_FUNCTION_DESC = {
    "type": "function",
    "function": {
        "name": "search_from_ragflow",
        "description": "trongthông tin",
        "parameters": {
            "type": "object",
            "properties": {"question": {"type": "string", "description": ""}},
            "required": ["question"],
        },
    },
}


@register_function(
    "search_from_ragflow", SEARCH_FROM_RAGFLOW_FUNCTION_DESC, ToolType.SYSTEM_CTL
)
def search_from_ragflow(conn: "ConnectionHandler", question=None):
    # đảm bảoký tựtham sốđúngxử lýmã hóa
    if question and isinstance(question, str):
        # đảm bảotham sốUTF-8mã hóaký tự
        pass
    else:
        question = str(question) if question is not None else ""

    ragflow_config = conn.config.get("plugins", {}).get("search_from_ragflow", {})
    base_url = ragflow_config.get("base_url", "")
    api_key = ragflow_config.get("api_key", "")
    dataset_ids = ragflow_config.get("dataset_ids", [])

    url = base_url + "/api/v1/retrieval"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # đảm bảopayloadtrongký tựUTF-8mã hóa
    payload = {"question": question, "dataset_ids": dataset_ids}

    try:
        # làm chosử dụngensure_ascii=Falseđảm bảoJSONtuần tự hóathờiđúngxử lýtrong
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=5,
            verify=False,
        )

        # đặtphản hồimã hóachoutf-8
        response.encoding = "utf-8"

        response.raise_for_status()

        # lấyvăn bảnnội dung，sauxử lýJSONgiải mã
        response_text = response.text
        import json

        result = json.loads(response_text)

        if result.get("code") != 0:
            error_detail = result.get("error", {}).get("detail", "lỗi không xác định")
            error_message = result.get("error", {}).get("message", "")
            error_code = result.get("code", "")

            # an toànghi lạilỗithông tin
            logger.bind(tag=TAG).error(
                f"RAGFlow APIsử dụngthất bại，phản hồi：{error_code}，lỗi：{error_detail}，hoàn chỉnhphản hồi：{result}"
            )

            # xây dựnglỗiphản hồi
            error_response = f"RAGtrả vềngoại lệ（lỗi：{error_code}）"

            if error_message:
                error_response += f"：{error_message}"
            if error_detail:
                error_response += f"\n：{error_detail}"

            return ActionResponse(Action.RESPONSE, None, error_response)

        chunks = result.get("data", {}).get("chunks", [])
        contents = []
        for chunk in chunks:
            content = chunk.get("content", "")
            if content:
                # an toànxử lýnội dungký tự
                if isinstance(content, str):
                    contents.append(content)
                elif isinstance(content, bytes):
                    contents.append(content.decode("utf-8", errors="replace"))
                else:
                    contents.append(str(content))

        if contents:
            # nội dungchosử dụngchế độ
            context_text = f"# về【{question}】đếnnhư\n"
            context_text += "```\n\n\n".join(contents[:5])
            context_text += "\n```"
        else:
            context_text = "theokết quả，không cóthông tin。"
        return ActionResponse(Action.REQLLM, context_text, None)

    except requests.exceptions.RequestException as e:
        # yêu cầungoại lệ
        error_type = type(e).__name__
        logger.bind(tag=TAG).error(
            f"RAGflowyêu cầuthất bại，ngoại lệ：{error_type}，：{str(e)}"
        )

        # theongoại lệhơnlỗithông tinvà
        if isinstance(e, requests.exceptions.ConnectTimeout):
            error_response = "RAGkết nối quá thời gian（5）"
            error_response += "\ncó thểdo：RAGflowdịch vụkhởi độnghoặckết nối"
            error_response += "\n：kiểm traRAGflowdịch vụtrạng tháivàkết nối"

        elif isinstance(e, requests.exceptions.ConnectionError):
            error_response = "kết nốiđếnRAG"
            error_response += "\ncó thểdo：RAGflowdịch vụđịa chỉlỗihoặcdịch vụ"
            error_response += "\n：kiểm traRAGflowdịch vụđịa chỉcấu hìnhvàdịch vụtrạng thái"

        elif isinstance(e, requests.exceptions.Timeout):
            error_response = "RAGyêu cầuquá thời gian"
            error_response += "\ncó thểdo：RAGflowdịch vụphản hồichậmhoặcđộ trễ"
            error_response += "\n：sauthử lạihoặckiểm traRAGflowdịch vụhiệu suất"

        elif isinstance(e, requests.exceptions.HTTPError):
            # xử lýHTTPlỗitrạng thái
            if hasattr(e.response, "status_code"):
                status_code = e.response.status_code
                error_response = f"RAGHTTPlỗi（trạng thái：{status_code}）"

                # thửlấyphản hồinội dungtronglỗithông tin
                try:
                    error_detail = e.response.json().get("error", {}).get("message", "")
                    if error_detail:
                        error_response += f"\nlỗi：{error_detail}"
                except:
                    pass
            else:
                error_response = f"RAGHTTPngoại lệ：{str(e)}"

        else:
            error_response = f"RAGngoại lệ（{error_type}）：{str(e)}"

        return ActionResponse(Action.RESPONSE, None, error_response)

    except Exception as e:
        # nóngoại lệ
        error_type = type(e).__name__
        logger.bind(tag=TAG).error(
            f"RAGflowxử lýngoại lệ，ngoại lệ：{error_type}，：{str(e)}"
        )

        # lỗithông tin
        error_response = f"RAGxử lýngoại lệ（{error_type}）：{str(e)}"
        return ActionResponse(Action.RESPONSE, None, error_response)
