"""
TTStrêncó thểđãđếnConnectionHandlertrong。

trêncó thểbao gồm：
1. mỗikết nốivớicócủtrênhàng đợivàxử lýluồng
2. trênluồngcủvớikết nốivới
3. làm chosử dụngConnectionHandler.enqueue_tts_reportphương pháptiến hànhtrên

core/connection.pytrongcủ。
"""

import time
import json
import opuslib_next
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

from config.manage_api_client import report as manage_report

TAG = __name__


async def report(conn: "ConnectionHandler", type, text, opus_data, report_time):
    """ghi lạitrên

    Args:
        conn: kết nốivới
        type: trên，1chosử dụng，2chocó thể，3chocông cụsử dụng
        text: văn bản
        opus_data: opusdữ liệu âm thanh
        report_time: trênkhi/thời
    """
    try:
        if opus_data:
            audio_data = opus_to_wav(conn, opus_data)
        else:
            audio_data = None
        # trên
        await manage_report(
            mac_address=conn.device_id,
            session_id=conn.session_id,
            chat_type=type,
            content=text,
            audio=audio_data,
            report_time=report_time,
        )
    except Exception as e:
        conn.logger.bind(tag=TAG).error(f"ghi lạitrênthất bại: {e}")


def opus_to_wav(conn: "ConnectionHandler", opus_data):
    """sẽOpusdữ liệuchuyển đổichoWAVđịnh dạngcủ

    Args:
        output_dir: rathư mục（giữ lạitham sốbằng）
        opus_data: opusdữ liệu âm thanh

    Returns:
        bytes: WAVđịnh dạngcủdữ liệu âm thanh
    """
    decoder = None
    try:
        decoder = opuslib_next.Decoder(16000, 1)  # 16kHz, 
        pcm_data = []

        for opus_packet in opus_data:
            try:
                pcm_frame = decoder.decode(opus_packet, 960)  # 960 samples = 60ms
                pcm_data.append(pcm_frame)
            except opuslib_next.OpusError as e:
                conn.logger.bind(tag=TAG).error(f"Opusgiải mãsai: {e}", exc_info=True)

        if not pcm_data:
            raise ValueError("cóhiệu quảcủPCMdữ liệu")

        # tạoWAVtệp
        pcm_data_bytes = b"".join(pcm_data)
        num_samples = len(pcm_data_bytes) // 2  # 16-bit samples

        # WAVtệp
        wav_header = bytearray()
        wav_header.extend(b"RIFF")  # ChunkID
        wav_header.extend((36 + len(pcm_data_bytes)).to_bytes(4, "little"))  # ChunkSize
        wav_header.extend(b"WAVE")  # Format
        wav_header.extend(b"fmt ")  # Subchunk1ID
        wav_header.extend((16).to_bytes(4, "little"))  # Subchunk1Size
        wav_header.extend((1).to_bytes(2, "little"))  # AudioFormat (PCM)
        wav_header.extend((1).to_bytes(2, "little"))  # NumChannels
        wav_header.extend((16000).to_bytes(4, "little"))  # SampleRate
        wav_header.extend((32000).to_bytes(4, "little"))  # ByteRate
        wav_header.extend((2).to_bytes(2, "little"))  # BlockAlign
        wav_header.extend((16).to_bytes(2, "little"))  # BitsPerSample
        wav_header.extend(b"data")  # Subchunk2ID
        wav_header.extend(len(pcm_data_bytes).to_bytes(4, "little"))  # Subchunk2Size

        # trả vềhoàn chỉnhcủWAVdữ liệu
        return bytes(wav_header) + pcm_data_bytes
    finally:
        if decoder is not None:
            try:
                del decoder
            except Exception as e:
                conn.logger.bind(tag=TAG).debug(f"giải phóngdecodertài nguyênkhi/thờira: {e}")


def enqueue_tts_report(conn: "ConnectionHandler", text, opus_data):
    if not conn.read_config_from_api or conn.need_bind or not conn.report_tts_enable:
        return
    if conn.chat_history_conf == 0:
        return
    """sẽTTSdữ liệuvàotrênhàng đợi

    Args:
        conn: kết nốivới
        text: văn bản
        opus_data: opusdữ liệu âm thanh
    """
    try:
        # sử dụngkết nốivớicủhàng đợi，vàovăn bảnvàdữ liệumàtệpđường dẫn
        if conn.chat_history_conf == 2:
            conn.report_queue.put((2, text, opus_data, int(time.time() * 1000)))
            conn.logger.bind(tag=TAG).debug(
                f"TTSdữ liệuđãvàotrênhàng đợi: {conn.device_id}, âm thanh: {len(opus_data)} "
            )
        else:
            conn.report_queue.put((2, text, None, int(time.time() * 1000)))
            conn.logger.bind(tag=TAG).debug(
                f"TTSdữ liệuđãvàotrênhàng đợi: {conn.device_id}, khôngtrênâm thanh"
            )
    except Exception as e:
        conn.logger.bind(tag=TAG).error(f"vàoTTStrênhàng đợithất bại: {text}, {e}")


def enqueue_tool_report(conn: "ConnectionHandler", tool_name: str, tool_input: dict, tool_result: str = None, report_tool_call: bool = True):
    """sẽcông cụsử dụngdữ liệuvàotrênhàng đợi

    Args:
        conn: kết nốivới
        tool_name: công cụ
        tool_input: công cụvàotham số
        tool_result: công cụkết quả（tùy chọn）
        report_tool_call: làtrêncông cụsử dụng，mặc địnhTrue；chỉtrênkết quảkhi/thờichoFalse
    """
    if not conn.read_config_from_api or conn.need_bind:
        return
    if conn.chat_history_conf == 0:
        return

    try:
        timestamp = int(time.time() * 1000)

        # xây dựngcông cụsử dụngbên trong
        if report_tool_call:
            tool_text = json.dumps(
                [
                    {
                        "type": "tool",
                        "text": f"{tool_name}({json.dumps(tool_input, ensure_ascii=False)})",
                    }
                ]
            )
            conn.report_queue.put((3, tool_text, None, timestamp))

        # xây dựngcông cụkết quảbên trong
        if tool_result:
            result_display = f'{{"result":"{str(tool_result)}"}}'
            result_content = json.dumps([{"type": "tool_result", "text": result_display}], ensure_ascii=False)
            conn.report_queue.put((3, result_content, None, timestamp + 1))
    except Exception as e:
        conn.logger.bind(tag=TAG).error(f"vàocông cụtrênhàng đợithất bại: {e}")


def enqueue_asr_report(conn: "ConnectionHandler", text, opus_data):
    if not conn.read_config_from_api or conn.need_bind or not conn.report_asr_enable:
        return
    if conn.chat_history_conf == 0:
        return
    """sẽASRdữ liệuvàotrênhàng đợi

    Args:
        conn: kết nốivới
        text: văn bản
        opus_data: opusdữ liệu âm thanh
    """
    try:
        # sử dụngkết nốivớicủhàng đợi，vàovăn bảnvàdữ liệumàtệpđường dẫn
        if conn.chat_history_conf == 2:
            conn.report_queue.put((1, text, opus_data, int(time.time() * 1000)))
            conn.logger.bind(tag=TAG).debug(
                f"ASRdữ liệuđãvàotrênhàng đợi: {conn.device_id}, âm thanh: {len(opus_data)} "
            )
        else:
            conn.report_queue.put((1, text, None, int(time.time() * 1000)))
            conn.logger.bind(tag=TAG).debug(
                f"ASRdữ liệuđãvàotrênhàng đợi: {conn.device_id}, khôngtrênâm thanh"
            )
    except Exception as e:
        conn.logger.bind(tag=TAG).debug(f"vàoASRtrênhàng đợithất bại: {text}, {e}")
