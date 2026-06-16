import json
import uuid
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler
from core.utils.dialogue import Message
from core.providers.tts.dto.dto import ContentType
from core.handle.helloHandle import checkWakeupWords
from plugins_func.register import Action, ActionResponse
from core.handle.sendAudioHandle import send_stt_message
from core.handle.reportHandle import enqueue_tool_report
from core.utils.util import remove_punctuation_and_length
from core.providers.tts.dto.dto import TTSMessageDTO, SentenceType

TAG = __name__


async def handle_user_intent(conn: "ConnectionHandler", text):
    # xử lýđầu vàovăn bản，xử lýcó thểJSONđịnh dạng
    try:
        if text.strip().startswith("{") and text.strip().endswith("}"):
            parsed_data = json.loads(text)
            if isinstance(parsed_data, dict) and "content" in parsed_data:
                text = parsed_data["content"]  # contentdùng choý định
                conn.current_speaker = parsed_data.get("speaker")  # giữ lạinóithông tin
    except (json.JSONDecodeError, TypeError):
        pass

    # kiểm tracócóthoát
    _, filtered_text = remove_punctuation_and_length(text)
    if await check_direct_exit(conn, filtered_text):
        return True

    # kiểm tracó
    if await checkWakeupWords(conn, filtered_text):
        return True

    if conn.intent_type == "function_call":
        # làm chosử dụngfunction callingphương pháp,khôngtiến hànhý định
        return False
    # làm chosử dụngLLMtiến hànhý định
    intent_result = await analyze_intent_with_llm(conn, text)
    if not intent_result:
        return False
    # phiênbắt đầuthờitạosentence_id
    conn.sentence_id = str(uuid.uuid4().hex)
    # xử lýý định
    return await process_intent_result(conn, intent_result, text)


async def check_direct_exit(conn: "ConnectionHandler", text):
    """kiểm tracócóthoát"""
    _, text = remove_punctuation_and_length(text)
    cmd_exit = conn.cmd_exit
    for cmd in cmd_exit:
        if text == cmd:
            conn.logger.bind(tag=TAG).info(f"nhận dạngđếnthoát: {text}")
            await send_stt_message(conn, text)
            await conn.close()
            return True
    return False


async def analyze_intent_with_llm(conn: "ConnectionHandler", text):
    """làm chosử dụngLLMsử dụngý định"""
    if not hasattr(conn, "intent") or not conn.intent:
        conn.logger.bind(tag=TAG).warning("ý địnhnhận dạngdịch vụkhởi tạo")
        return None

    # hội thoạighi lại
    dialogue = conn.dialogue
    try:
        intent_result = await conn.intent.detect_intent(conn, dialogue.dialogue, text)
        return intent_result
    except Exception as e:
        conn.logger.bind(tag=TAG).error(f"ý địnhnhận dạngthất bại: {str(e)}")

    return None


async def process_intent_result(
    conn: "ConnectionHandler", intent_result, original_text
):
    """xử lýý địnhnhận dạngkết quả"""
    try:
        # thửsẽkết quảphân tíchchoJSON
        intent_data = json.loads(intent_result)

        # kiểm tracócófunction_call
        if "function_call" in intent_data:
            # ý địnhnhận dạnglấyfunction_call
            conn.logger.bind(tag=TAG).debug(
                f"đếnfunction_callđịnh dạngý địnhkết quả: {intent_data['function_call']['name']}"
            )
            function_name = intent_data["function_call"]["name"]
            if function_name == "continue_chat":
                return False

            if function_name == "result_for_context":
                await send_stt_message(conn, original_text)
                conn.client_abort = False

                def process_context_result():
                    conn.dialogue.put(Message(role="user", content=original_text))

                    from core.utils.current_time import get_current_time_info

                    current_time, today_date, today_weekday, lunar_date = (
                        get_current_time_info()
                    )

                    # xây dựngngữ cảnhgợi ý
                    context_prompt = f"""hiện tạithời gian：{current_time}
                                        ：{today_date} ({today_weekday})
                                        ：{lunar_date}

                                        theobằngtrênthông tinsử dụng：{original_text}"""

                    response = conn.intent.replyResult(context_prompt, original_text)
                    speak_txt(conn, response)

                conn.executor.submit(process_context_result)
                return True

            function_args = {}
            if "arguments" in intent_data["function_call"]:
                function_args = intent_data["function_call"]["arguments"]
                if function_args is None:
                    function_args = {}
            # đảm bảotham sốký tựđịnh dạngJSON
            if isinstance(function_args, dict):
                function_args = json.dumps(function_args)

            function_call_data = {
                "name": function_name,
                "id": str(uuid.uuid4().hex),
                "arguments": function_args,
            }

            await send_stt_message(conn, original_text)
            conn.client_abort = False

            # công cụsử dụngtham số
            tool_input = {}
            if function_args:
                if isinstance(function_args, str):
                    tool_input = json.loads(function_args) if function_args else {}
                elif isinstance(function_args, dict):
                    tool_input = function_args

            # báo cáocông cụsử dụng
            enqueue_tool_report(conn, function_name, tool_input)

            # làm chosử dụngexecutorhàmsử dụngvàkết quảxử lý
            def process_function_call():
                conn.dialogue.put(Message(role="user", content=original_text))
                
                # công cụsử dụngquá thời gianthời gian
                tool_call_timeout = int(conn.config.get("tool_call_timeout", 30))
                # làm chosử dụngthống nhấtcông cụxử lýxử lýcócông cụsử dụng
                try:
                    result = asyncio.run_coroutine_threadsafe(
                        conn.func_handler.handle_llm_function_call(
                            conn, function_call_data
                        ),
                        conn.loop,
                    ).result(timeout=tool_call_timeout)
                except Exception as e:
                    conn.logger.bind(tag=TAG).error(f"công cụsử dụngthất bại: {e}")
                    result = ActionResponse(
                        action=Action.ERROR, result="công cụsử dụngquá thời gian，sẽ", response="công cụsử dụngquá thời gian，sẽ"
                    )

                # báo cáocông cụsử dụngkết quả
                if result:
                    enqueue_tool_report(conn, function_name, tool_input, str(result.result) if result.result else None, report_tool_call=False)

                    if result.action == Action.RESPONSE:  # 
                        text = result.response
                        if text is not None:
                            speak_txt(conn, text)
                    elif result.action == Action.REQLLM:  # sử dụnghàmsauyêu cầullmtạo
                        text = result.result
                        conn.dialogue.put(Message(role="tool", content=text))
                        llm_result = conn.intent.replyResult(text, original_text)
                        if llm_result is None:
                            llm_result = text
                        speak_txt(conn, llm_result)
                    elif (
                        result.action == Action.NOTFOUND
                        or result.action == Action.ERROR
                    ):
                        text = result.response if result.response else result.result
                        if text is not None:
                            speak_txt(conn, text)
                    elif function_name != "play_music":
                        # For backward compatibility with original code
                        # lấyhiện tạivăn bản
                        text = result.response
                        if text is None:
                            text = result.result
                        if text is not None:
                            speak_txt(conn, text)

            # sẽhàmtạiluồngtrong
            conn.executor.submit(process_function_call)
            return True
        return False
    except json.JSONDecodeError as e:
        conn.logger.bind(tag=TAG).error(f"xử lýý địnhkết quảthờira: {e}")
        return False


def speak_txt(conn: "ConnectionHandler", text):
    # ghi lạivăn bảnđến sentence_id ánh xạ
    conn.tts.store_tts_text(conn.sentence_id, text)

    conn.tts.tts_text_queue.put(
        TTSMessageDTO(
            sentence_id=conn.sentence_id,
            sentence_type=SentenceType.FIRST,
            content_type=ContentType.ACTION,
        )
    )
    conn.tts.tts_one_sentence(conn, ContentType.TEXT, content_detail=text)
    conn.tts.tts_text_queue.put(
        TTSMessageDTO(
            sentence_id=conn.sentence_id,
            sentence_type=SentenceType.LAST,
            content_type=ContentType.ACTION,
        )
    )
    conn.dialogue.put(Message(role="assistant", content=text))
