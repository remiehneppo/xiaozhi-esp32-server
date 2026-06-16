import time
import json
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler
from core.utils.util import audio_to_data
from core.handle.abortHandle import handleAbortMessage
from core.handle.intentHandler import handle_user_intent
from core.utils.output_counter import check_device_output_limit
from core.handle.sendAudioHandle import send_stt_message, SentenceType

TAG = __name__


async def handleAudioMessage(conn: "ConnectionHandler", audio):
    # hiện tạicócónói
    have_voice = conn.vad.is_vad(conn, audio)
    # nhưbị，VAD
    if hasattr(conn, "just_woken_up") and conn.just_woken_up:
        have_voice = False
        # đặtmộtđộ trễsautiếp tụcVAD
        if not hasattr(conn, "vad_resume_task") or conn.vad_resume_task.done():
            conn.vad_resume_task = asyncio.create_task(resume_vad_detection(conn))
        return
    # thời gian，dùng chosay goodbye
    await no_voice_close_connect(conn, have_voice)
    # nhậnâm thanh
    await conn.asr.receive_audio(conn, audio, have_voice)


async def resume_vad_detection(conn: "ConnectionHandler"):
    # chờ2sautiếp tụcVAD
    await asyncio.sleep(2)
    conn.just_woken_up = False


async def startToChat(conn: "ConnectionHandler", text):
    # kiểm trađầu vàocóJSONđịnh dạng（nóithông tin）
    speaker_name = None
    language_tag = None
    actual_text = text

    try:
        # thửphân tíchJSONđịnh dạngđầu vào
        if text.strip().startswith("{") and text.strip().endswith("}"):
            data = json.loads(text)
            if "speaker" in data and "content" in data:
                speaker_name = data["speaker"]
                language_tag = data["language"]
                actual_text = data["content"]
                conn.logger.bind(tag=TAG).info(f"phân tíchđếnnóithông tin: {speaker_name}")

                # làm chosử dụngJSONđịnh dạngvăn bản，khôngphân tích
                actual_text = text
    except (json.JSONDecodeError, KeyError):
        # nhưphân tíchthất bại，tiếp tụclàm chosử dụngban đầuvăn bản
        pass

    # lưunóithông tinđếnkết nốivới
    if speaker_name:
        conn.current_speaker = speaker_name
    else:
        conn.current_speaker = None

    if conn.need_bind:
        await check_bind_device(conn)
        return

    # nhưratại
    if conn.max_output_size > 0:
        if check_device_output_limit(
            conn.headers.get("device-id"), conn.max_output_size
        ):
            await max_out_size(conn)
            return

    # manual chế độkhôngngắttạinội dung
    if conn.client_is_speaking and conn.client_listen_mode != "manual":
        await handleAbortMessage(conn)

    # tiến hànhý định，làm chosử dụngvăn bảnnội dung
    intent_handled = await handle_user_intent(conn, actual_text)

    if intent_handled:
        # nhưý địnhđãbịxử lý，khôngtiến hành
        return

    # ý địnhbịxử lý，tiếp tục，làm chosử dụngvăn bảnnội dung
    await send_stt_message(conn, actual_text)

    # bắt đầuphiên
    conn.client_abort = False

    conn.executor.submit(conn.chat, actual_text)


async def no_voice_close_connect(conn: "ConnectionHandler", have_voice):
    if have_voice:
        conn.last_activity_time = time.time() * 1000
        return
    # chỉcótạiđãkhởi tạoquathời giantiến hànhquá thời giankiểm tra
    if conn.last_activity_time > 0.0:
        no_voice_time = time.time() * 1000 - conn.last_activity_time
        close_connection_no_voice_time = int(
            conn.config.get("close_connection_no_voice_time", 120)
        )
        if (
            not conn.close_after_chat
            and no_voice_time > 1000 * close_connection_no_voice_time
        ):
            conn.close_after_chat = True
            conn.client_abort = False
            end_prompt = conn.config.get("end_prompt", {})
            if end_prompt and end_prompt.get("enable", True) is False:
                conn.logger.bind(tag=TAG).info("kết thúchội thoại，gửikết thúcgợi ý")
                await conn.close()
                return
            prompt = end_prompt.get("prompt")
            if not prompt:
                prompt = "bằng```thời gianqua```đến，sử dụngcó、khôngđếnkết thúcnàyhội thoại。！"
            await startToChat(conn, prompt)


async def max_out_size(conn: "ConnectionHandler"):
    # raragợi ý
    conn.client_abort = False
    text = "không，tôitạicóphải，nàykhitôinhững，！khôngkhông，Tạm biệt！"
    await send_stt_message(conn, text)
    file_path = "config/assets/max_output_size.wav"
    opus_packets = await audio_to_data(file_path)
    conn.tts.tts_audio_queue.put((SentenceType.LAST, opus_packets, text))
    conn.close_after_chat = True


async def check_bind_device(conn: "ConnectionHandler"):
    if conn.bind_code:
        # đảm bảobind_code6
        if len(conn.bind_code) != 6:
            conn.logger.bind(tag=TAG).error(f"không hợp lệđịnh dạng: {conn.bind_code}")
            text = "định dạnglỗi，kiểm tracấu hình。"
            await send_stt_message(conn, text)
            return

        text = f"kiểm soát，đầu vào{conn.bind_code}，。"
        await send_stt_message(conn, text)

        # gợi ý
        music_path = "config/assets/bind_code.wav"
        opus_packets = await audio_to_data(music_path)
        conn.tts.tts_audio_queue.put((SentenceType.FIRST, opus_packets, text))

        # 
        for i in range(6):  # đảm bảochỉ6
            try:
                digit = conn.bind_code[i]
                num_path = f"config/assets/bind_code/{digit}.wav"
                num_packets = await audio_to_data(num_path)
                conn.tts.tts_audio_queue.put((SentenceType.MIDDLE, num_packets, None))
            except Exception as e:
                conn.logger.bind(tag=TAG).error(f"âm thanhthất bại: {e}")
                continue
        conn.tts.tts_audio_queue.put((SentenceType.LAST, [], None))
    else:
        # gợi ý
        conn.client_abort = False
        text = f"không cóđếnthông tin，đúngcấu hình OTAđịa chỉ，sau。"
        await send_stt_message(conn, text)
        music_path = "config/assets/bind_not_found.wav"
        opus_packets = await audio_to_data(music_path)
        conn.tts.tts_audio_queue.put((SentenceType.LAST, opus_packets, text))
