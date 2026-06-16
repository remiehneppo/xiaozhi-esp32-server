import time
import uuid
import asyncio
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

from core.utils.dialogue import Message
from core.providers.asr.dto.dto import InterfaceType
from core.handle.receiveAudioHandle import startToChat
from core.handle.reportHandle import enqueue_asr_report
from core.handle.sendAudioHandle import send_stt_message, send_tts_message
from core.handle.textMessageHandler import TextMessageHandler
from core.handle.textMessageType import TextMessageType
from core.utils.util import remove_punctuation_and_length
from core.providers.tts.dto.dto import ContentType, TTSMessageDTO, SentenceType


TAG = __name__

class ListenTextMessageHandler(TextMessageHandler):
    """Listentin nhắnxử lý"""

    @property
    def message_type(self) -> TextMessageType:
        return TextMessageType.LISTEN

    async def handle(self, conn: "ConnectionHandler", msg_json: Dict[str, Any]) -> None:
        if "mode" in msg_json:
            conn.client_listen_mode = msg_json["mode"]
            conn.logger.bind(tag=TAG).debug(
                f"máy kháchchế độ：{conn.client_listen_mode}"
            )
        if msg_json["state"] == "start":
            # chế độchế độ,xóacóâm thanhtrạng tháivà
            conn.reset_audio_states()
        elif msg_json["state"] == "stop":
            conn.client_voice_stop = True
            if conn.asr.interface_type == InterfaceType.STREAM:
                # luồngchế độ，gửikết thúcyêu cầu
                asyncio.create_task(conn.asr._send_stop_request())
            else:
                # luồngchế độ：ASRnhận dạng
                if len(conn.asr_audio) > 0:
                    asr_audio_task = conn.asr_audio.copy()
                    conn.reset_audio_states()

                    if len(asr_audio_task) > 0:
                        await conn.asr.handle_voice_stop(conn, asr_audio_task)
        elif msg_json["state"] == "detect":
            conn.client_have_voice = False
            conn.reset_audio_states()
            if "text" in msg_json:
                conn.last_activity_time = time.time() * 1000
                original_text = msg_json["text"]  # giữ lạiban đầuvăn bản
                filtered_len, filtered_text = remove_punctuation_and_length(
                    original_text
                )

                # kiểm tracó [device_call]
                if original_text.startswith("[device_call]"):
                    #  tag sauvăn bản
                    call_text = original_text[len("[device_call]"):].strip()
                    conn.logger.bind(tag=TAG).info(f"nhận được: {call_text}")

                    # bắt đầuphiên
                    conn.sentence_id = uuid.uuid4().hex

                    await send_stt_message(conn, call_text)
                    conn.tts.store_tts_text(conn.sentence_id, call_text)
                    conn.tts.tts_text_queue.put(TTSMessageDTO(sentence_id=conn.sentence_id, sentence_type=SentenceType.FIRST, content_type=ContentType.ACTION))
                    conn.tts.tts_one_sentence(conn, ContentType.TEXT, content_detail=call_text)
                    conn.tts.tts_text_queue.put(TTSMessageDTO(sentence_id=conn.sentence_id, sentence_type=SentenceType.LAST, content_type=ContentType.ACTION))

                    # thêmđếnhội thoại，chomô hìnhngữ cảnh
                    conn.dialogue.put(Message(role="assistant", content=call_text))
                    return

                # nhận dạngcó
                is_wakeup_words = filtered_text in conn.config.get("wakeup_words")
                # có
                enable_greeting = conn.config.get("enable_greeting", True)

                if is_wakeup_words and not enable_greeting:
                    # như，vàđóng，thìkhôngsử dụng
                    await send_stt_message(conn, original_text)
                    await send_tts_message(conn, "stop", None)
                    conn.client_is_speaking = False
                elif is_wakeup_words:
                    conn.just_woken_up = True
                    # báo cáodữ liệu（sử dụngASRbáo cáocó thể，nhưngkhôngdữ liệu âm thanh）
                    enqueue_asr_report(conn, "，", [])
                    await startToChat(conn, "，")
                else:
                    conn.just_woken_up = True
                    # báo cáodữ liệu（sử dụngASRbáo cáocó thể，nhưngkhôngdữ liệu âm thanh）
                    enqueue_asr_report(conn, original_text, [])
                    # cầnLLMvớinội dungtiến hành
                    await startToChat(conn, original_text)