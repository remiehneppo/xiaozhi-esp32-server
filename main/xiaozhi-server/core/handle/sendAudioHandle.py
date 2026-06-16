import json
import time
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler
from core.utils import textUtils
from core.utils.util import audio_to_data
from core.providers.tts.dto.dto import SentenceType
from core.utils.audioRateController import AudioRateController

TAG = __name__
# Độ dài frame audio (ms)
AUDIO_FRAME_DURATION = 60
# Số gói pre-buffer, gửi trực tiếp để giảm latency
PRE_BUFFER_COUNT = 5


async def sendAudioMessage(conn: "ConnectionHandler", sentenceType, audios, text, sentence_id=None):
    # Bỏ qua audio dư của câu cũ
    if sentence_id is not None and sentence_id != conn.sentence_id:
        return

    if conn.tts.tts_audio_first_sentence:
        conn.logger.bind(tag=TAG).info(f"Gửigiọng nói đầu tiên: {text}")
        conn.tts.tts_audio_first_sentence = False

    if sentenceType == SentenceType.FIRST:
        # Message tiếp theo của cùng câu thêm vào flow control queue, các trường hợp khác gửi ngay
        if (
            hasattr(conn, "audio_rate_controller")
            and conn.audio_rate_controller
            and getattr(conn, "audio_flow_control", {}).get("sentence_id")
            == conn.sentence_id
        ):
            conn.audio_rate_controller.add_message(
                lambda: send_tts_message(conn, "sentence_start", text)
            )
        else:
            # Câu mới hoặc flow controller chưa khởi tạo, gửi ngay
            await send_tts_message(conn, "sentence_start", text)

    await sendAudio(conn, audios)
    # Gửi message bắt đầu câu
    if sentenceType is not SentenceType.MIDDLE:
        conn.logger.bind(tag=TAG).info(f"Gửi audio message: {sentenceType}, {text}")

    # Gửi message kết thúc (nếu là text cuối cùng)
    # Cuộc gọi cần duy trì speaking state
    if not conn.calling and sentenceType == SentenceType.LAST:
        await send_tts_message(conn, "stop", None)
        if conn.close_after_chat:
            await conn.close()


async def _wait_for_audio_completion(conn: "ConnectionHandler"):
    """
    Đợi audio queue trống và đợi pre-buffer packet phát hoàn thành

    Args:
        conn: Kết nối object
    """
    if hasattr(conn, "audio_rate_controller") and conn.audio_rate_controller:
        rate_controller = conn.audio_rate_controller
        conn.logger.bind(tag=TAG).debug(
            f"Đợi audio gửi hoàn thành, trong queue còn {len(rate_controller.queue)} gói"
        )
        await rate_controller.queue_empty_event.wait()

        # Đợi pre-buffer packet phát hoàn thành
        # Gói N đầu gửi trực tiếp, thêm 2 gói network jitter, cần thêm thời gian chờ chúng phát hoàn thành ở client
        frame_duration_ms = rate_controller.frame_duration
        pre_buffer_playback_time = (PRE_BUFFER_COUNT + 2) * frame_duration_ms / 1000.0
        await asyncio.sleep(pre_buffer_playback_time)

        conn.logger.bind(tag=TAG).debug("Audio gửi hoàn thành")


async def _send_to_mqtt_gateway(
    conn: "ConnectionHandler", opus_packet, timestamp, sequence
):
    """
    Gửi opus packet có 16-byte header đến mqtt_gateway
    Args:
        conn: Kết nối object
        opus_packet: opus packet
        timestamp: Timestamp
        sequence: Sequence number
    """
    # Thêm 16-byte header cho opus packet
    header = bytearray(16)
    header[0] = 1  # type
    header[2:4] = len(opus_packet).to_bytes(2, "big")  # payload length
    header[4:8] = sequence.to_bytes(4, "big")  # sequence
    header[8:12] = timestamp.to_bytes(4, "big")  # Timestamp
    header[12:16] = len(opus_packet).to_bytes(4, "big")  # Độ dài opus

    # Gửi packet hoàn chỉnh có header
    complete_packet = bytes(header) + opus_packet
    await conn.websocket.send(complete_packet)


async def sendAudio(
    conn: "ConnectionHandler", audios, frame_duration=AUDIO_FRAME_DURATION
):
    """
    Gửi audio packet, dùng AudioRateController để thực hiện precise traffic control

    Args:
        conn: Kết nối object
        audios: Đơn opus packet(bytes) hoặc danh sách opus packets
        frame_duration: Độ dài frame (ms), mặc định dùng global constant AUDIO_FRAME_DURATION
    """
    if audios is None or len(audios) == 0:
        return

    send_delay = conn.config.get("tts_audio_send_delay", -1) / 1000.0
    is_single_packet = isinstance(audios, bytes)

    # Khởi tạo hoặc lấy RateController
    rate_controller, flow_control = _get_or_create_rate_controller(
        conn, frame_duration, is_single_packet
    )

    # Chuyển đổi thống nhất thành list để xử lý
    audio_list = [audios] if is_single_packet else audios

    # Gửi audio packet
    await _send_audio_with_rate_control(
        conn, audio_list, rate_controller, flow_control, send_delay
    )


def _get_or_create_rate_controller(
    conn: "ConnectionHandler", frame_duration, is_single_packet
):
    """
    Lấy hoặc tạo RateController và flow_control

    Args:
        conn: Kết nối object
        frame_duration: Độ dài frame
        is_single_packet: Có phải single packet mode (True: TTS stream single packet, False: batch packets)

    Returns:
        (rate_controller, flow_control)
    """
    # Kiểm tra có cần reset controller không
    need_reset = False

    if not hasattr(conn, "audio_rate_controller"):
        # Controller không tồn tại, cần tạo
        need_reset = True
    else:
        rate_controller = conn.audio_rate_controller

        # Background send task đã dừng, thì cần reset
        if (
            not rate_controller.pending_send_task
            or rate_controller.pending_send_task.done()
        ):
            need_reset = True
        # Khi sentence_id thay đổi, cần reset
        elif (
            getattr(conn, "audio_flow_control", {}).get("sentence_id")
            != conn.sentence_id
        ):
            need_reset = True

    if need_reset:
        # Tạo hoặc lấy rate_controller
        if not hasattr(conn, "audio_rate_controller"):
            conn.audio_rate_controller = AudioRateController(frame_duration)
        else:
            conn.audio_rate_controller.reset()

        # Khởi tạo flow_control
        conn.audio_flow_control = {
            "packet_count": 0,
            "sequence": 0,
            "sentence_id": conn.sentence_id,
        }

        # Khởi động background send loop
        _start_background_sender(
            conn, conn.audio_rate_controller, conn.audio_flow_control
        )

    return conn.audio_rate_controller, conn.audio_flow_control


def _start_background_sender(conn: "ConnectionHandler", rate_controller, flow_control):
    """
    Khởi động background send loopnhiệm vụ

    Args:
        conn: Kết nối object
        rate_controller: Rate controller
        flow_control: Trạng thái flow control
    """

    async def send_callback(packet):
        # Kiểm tra có nêntrong không
        if conn.client_abort:
            raise asyncio.CancelledError("máy kháchđãtrong")

        conn.last_activity_time = time.time() * 1000
        await _do_send_audio(conn, packet, flow_control)

    # Dùng start_sending khởi động background loop
    rate_controller.start_sending(send_callback)


async def _send_audio_with_rate_control(
    conn: "ConnectionHandler", audio_list, rate_controller, flow_control, send_delay
):
    """
    làm chosử dụng rate_controller Gửi audio packet

    Args:
        conn: Kết nối object
        audio_list: Danh sách audio packet
        rate_controller: Rate controller
        flow_control: Trạng thái flow control
        send_delay: Độ trễ cố định (s), -1 là dùng dynamic flow control
    """
    for packet in audio_list:
        if conn.client_abort:
            return

        conn.last_activity_time = time.time() * 1000

        # Pre-buffer: Gửi trực tiếp N gói đầu
        if flow_control["packet_count"] < PRE_BUFFER_COUNT:
            await _do_send_audio(conn, packet, flow_control)
        elif send_delay > 0:
            # Chế độ độ trễ cố định
            await asyncio.sleep(send_delay)
            await _do_send_audio(conn, packet, flow_control)
        else:
            # Chế độ dynamic flow control: Chỉ thêm vào queue, background loop chịu trách nhiệm gửi
            rate_controller.add_audio(packet)


async def _do_send_audio(conn: "ConnectionHandler", opus_packet, flow_control):
    """
    Thực hiện gửi audio thực tế
    """
    packet_index = flow_control.get("packet_count", 0)
    sequence = flow_control.get("sequence", 0)

    if conn.conn_from_mqtt_gateway:
        # tính toánTimestamp（dựa trênvị trí）
        start_time = time.time()
        timestamp = int(start_time * 1000) % (2**32)
        await _send_to_mqtt_gateway(conn, opus_packet, timestamp, sequence)
    else:
        # Gửi trực tiếp opus packet
        await conn.websocket.send(opus_packet)

    # Cập nhật trạng thái flow control
    flow_control["packet_count"] = packet_index + 1
    flow_control["sequence"] = sequence + 1


async def send_tts_message(conn: "ConnectionHandler", state, text=None):
    """Gửi message trạng thái TTS"""
    if text is None and state == "sentence_start":
        return
    message = {"type": "tts", "state": state, "session_id": conn.session_id}
    if text is not None:
        message["text"] = textUtils.check_emoji(text)

    # TTS playback kết thúc
    if state == "stop":
        # Lưu sentence_id hiện tại, dùng để xác định sau đó có phải round hiện tại không
        current_sentence_id = conn.sentence_id
        # Phátgợi ý sound
        tts_notify = conn.config.get("enable_stop_tts_notify", False)
        if tts_notify:
            stop_tts_notify_voice = conn.config.get(
                "stop_tts_notify_voice", "config/assets/tts_notify.mp3"
            )
            audios = await audio_to_data(stop_tts_notify_voice, is_opus=True)
            await sendAudio(conn, audios)
        # Đợi tất cả audio packet gửi hoàn thành
        await _wait_for_audio_completion(conn)

        # Kiểm tra có phải round hiện tại không
        if current_sentence_id != conn.sentence_id:
            return

        # Dừng audio send loop (chỉ gọi khi flow controller đã khởi tạo)
        if hasattr(conn, "audio_rate_controller") and conn.audio_rate_controller:
            conn.audio_rate_controller.stop_sending()
        conn.clearSpeakStatus()

    # Gửi message đến client
    await conn.websocket.send(json.dumps(message))


async def send_stt_message(conn: "ConnectionHandler", text):
    """Gửi message trạng thái STT"""
    end_prompt_str = conn.config.get("end_prompt", {}).get("prompt")
    if end_prompt_str and end_prompt_str == text:
        await send_tts_message(conn, "start")
        return

    # Parse JSON format, extract actual user speech content
    display_text = text
    try:
        # Thử parse JSON format
        if text.strip().startswith("{") and text.strip().endswith("}"):
            parsed_data = json.loads(text)
            if isinstance(parsed_data, dict) and "content" in parsed_data:
                # Nếu là JSON format chứa speaker info, chỉ hiển thị phần content
                display_text = parsed_data["content"]
                # Lưu speaker info vào conn object
                if "speaker" in parsed_data:
                    conn.current_speaker = parsed_data["speaker"]
    except (json.JSONDecodeError, TypeError):
        # Nếu không phải JSON format, dùng trực tiếp original text
        display_text = text
    stt_text = textUtils.get_string_no_punctuation_or_emoji(display_text)
    await conn.websocket.send(
        json.dumps({"type": "stt", "text": stt_text, "session_id": conn.session_id})
    )
    await send_tts_message(conn, "start")
    # Sau khi gửi start message client state sẽtại speaking state, sync server state
    conn.client_is_speaking = True


async def send_display_message(conn: "ConnectionHandler", text):
    """Gửi display message"""
    message = {
        "type": "stt",
        "text": text,
        "session_id": conn.session_id
    }
    await conn.websocket.send(json.dumps(message))
