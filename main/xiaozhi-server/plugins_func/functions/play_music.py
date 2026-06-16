import os
import re
import time
import random
import difflib
import traceback
from pathlib import Path
from core.handle.sendAudioHandle import send_stt_message
from plugins_func.register import register_function, ToolType, ActionResponse, Action
from core.utils.dialogue import Message
from core.providers.tts.dto.dto import TTSMessageDTO, SentenceType, ContentType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

TAG = __name__

MUSIC_CACHE = {}

play_music_function_desc = {
    "type": "function",
    "function": {
        "name": "play_music",
        "description": "sử dụngphải、khi/thờisử dụng。",
        "parameters": {
            "type": "object",
            "properties": {
                "song_name": {
                    "type": "string",
                    "description": "，nhưsử dụngcóchỉ địnhcho'random', chỉ địnhcủkhi/thờitrả vềcủ : ```sử dụng:chỉ\ntham số：chỉ``` ```sử dụng: \ntham số：random ```",
                }
            },
            "required": ["song_name"],
        },
    },
}


@register_function("play_music", play_music_function_desc, ToolType.SYSTEM_CTL)
def play_music(conn: "ConnectionHandler", song_name: str):
    try:
        music_intent = (
            f" {song_name}" if song_name != "random" else ""
        )

        # kiểm tratrạng thái
        if not conn.loop.is_running():
            conn.logger.bind(tag=TAG).error("，nhiệm vụ")
            return ActionResponse(
                action=Action.RESPONSE, result="", response="sau"
            )

        # nhiệm vụ
        task = conn.loop.create_task(
            handle_music_command(conn, music_intent)  # 
        )

        # xử lý
        def handle_done(f):
            try:
                f.result()  # tại/trongnàyxử lýthành công
                conn.logger.bind(tag=TAG).info("hoàn thành")
            except Exception as e:
                conn.logger.bind(tag=TAG).error(f"thất bại: {e}")

        task.add_done_callback(handle_done)

        return ActionResponse(
            action=Action.RECORD, result="đãnhận", response="tại/trongcho"
        )
    except Exception as e:
        conn.logger.bind(tag=TAG).error(f"xử lýý địnhsai: {e}")
        return ActionResponse(
            action=Action.RESPONSE, result=str(e), response="khi/thờira"
        )


def _extract_song_name(text):
    """từsử dụngvàotrong"""
    for keyword in [""]:
        if keyword in text:
            parts = text.split(keyword)
            if len(parts) > 1:
                return parts[1].strip()
    return None


def _find_best_match(potential_song, music_files):
    """khớpcủ"""
    best_match = None
    highest_ratio = 0

    for music_file in music_files:
        song_name = os.path.splitext(music_file)[0]
        ratio = difflib.SequenceMatcher(None, potential_song, song_name).ratio()
        if ratio > highest_ratio and ratio > 0.4:
            highest_ratio = ratio
            best_match = music_file
    return best_match


def get_music_files(music_dir, music_ext):
    music_dir = Path(music_dir)
    music_files = []
    music_file_names = []
    for file in music_dir.rglob("*"):
        # làlàtệp
        if file.is_file():
            # lấytệp
            ext = file.suffix.lower()
            # làtại/trongtrong
            if ext in music_ext:
                # thêmvớiđường dẫn
                music_files.append(str(file.relative_to(music_dir)))
                music_file_names.append(
                    os.path.splitext(str(file.relative_to(music_dir)))[0]
                )
    return music_files, music_file_names


def initialize_music_handler(conn: "ConnectionHandler"):
    global MUSIC_CACHE
    if MUSIC_CACHE == {}:
        plugins_config = conn.config.get("plugins", {})
        if "play_music" in plugins_config:
            MUSIC_CACHE["music_config"] = plugins_config["play_music"]
            MUSIC_CACHE["music_dir"] = os.path.abspath(
                MUSIC_CACHE["music_config"].get("music_dir", "./music")  # mặc địnhđường dẫnsửa đổi
            )
            MUSIC_CACHE["music_ext"] = MUSIC_CACHE["music_config"].get(
                "music_ext", (".mp3", ".wav", ".p3")
            )
            MUSIC_CACHE["refresh_time"] = MUSIC_CACHE["music_config"].get(
                "refresh_time", 60
            )
        else:
            MUSIC_CACHE["music_dir"] = os.path.abspath("./music")
            MUSIC_CACHE["music_ext"] = (".mp3", ".wav", ".p3")
            MUSIC_CACHE["refresh_time"] = 60
        # lấytệp
        MUSIC_CACHE["music_files"], MUSIC_CACHE["music_file_names"] = get_music_files(
            MUSIC_CACHE["music_dir"], MUSIC_CACHE["music_ext"]
        )
        MUSIC_CACHE["scan_time"] = time.time()
    return MUSIC_CACHE


async def handle_music_command(conn: "ConnectionHandler", text):
    initialize_music_handler(conn)
    global MUSIC_CACHE

    """xử lý"""
    clean_text = re.sub(r"[^\w\s]", "", text).strip()
    conn.logger.bind(tag=TAG).debug(f"kiểm tralàlà: {clean_text}")

    # cố gắngkhớp
    if os.path.exists(MUSIC_CACHE["music_dir"]):
        if time.time() - MUSIC_CACHE["scan_time"] > MUSIC_CACHE["refresh_time"]:
            # làm mớitệp
            MUSIC_CACHE["music_files"], MUSIC_CACHE["music_file_names"] = (
                get_music_files(MUSIC_CACHE["music_dir"], MUSIC_CACHE["music_ext"])
            )
            MUSIC_CACHE["scan_time"] = time.time()

        potential_song = _extract_song_name(clean_text)
        if potential_song:
            best_match = _find_best_match(potential_song, MUSIC_CACHE["music_files"])
            if best_match:
                conn.logger.bind(tag=TAG).info(f"đếnkhớpcủ: {best_match}")
                await play_local_music(conn, specific_file=best_match)
                return True
    # kiểm tralàlàsử dụng
    await play_local_music(conn)
    return True


def _get_random_play_prompt(song_name):
    """tạo"""
    # loại bỏtệp
    clean_name = os.path.splitext(song_name)[0]
    prompts = [
        f"tại/trongcho，《{clean_name}》",
        f"，《{clean_name}》",
        f"sẽcho，《{clean_name}》",
        f"tại/trongchođến，《{clean_name}》",
        f"cho/phéptôinhững，《{clean_name}》",
        f"đến，《{clean_name}》",
        f"nàychotrên，《{clean_name}》",
    ]
    # làm chosử dụngrandom.choice，khôngđặtseed
    return random.choice(prompts)


async def play_local_music(conn: "ConnectionHandler", specific_file=None):
    global MUSIC_CACHE
    """địa phương/cục bộtệp"""
    try:
        if not os.path.exists(MUSIC_CACHE["music_dir"]):
            conn.logger.bind(tag=TAG).error(
                f"thư mụckhôngtại/trong: " + MUSIC_CACHE["music_dir"]
            )
            return

        # đảm bảođường dẫnđúng
        if specific_file:
            selected_music = specific_file
            music_path = os.path.join(MUSIC_CACHE["music_dir"], specific_file)
        else:
            if not MUSIC_CACHE["music_files"]:
                conn.logger.bind(tag=TAG).error("đếnMP3tệp")
                return
            selected_music = random.choice(MUSIC_CACHE["music_files"])
            music_path = os.path.join(MUSIC_CACHE["music_dir"], selected_music)

        if not os.path.exists(music_path):
            conn.logger.bind(tag=TAG).error(f"củtệpkhôngtại/trong: {music_path}")
            return
        text = _get_random_play_prompt(selected_music)
        conn.tts.store_tts_text(conn.sentence_id, text)
        # conn.dialogue.put(Message(role="assistant", content=text))

        if conn.intent_type == "intent_llm":
            conn.tts.tts_text_queue.put(
                TTSMessageDTO(
                    sentence_id=conn.sentence_id,
                    sentence_type=SentenceType.FIRST,
                    content_type=ContentType.ACTION,
                )
            )
        conn.tts.tts_text_queue.put(
            TTSMessageDTO(
                sentence_id=conn.sentence_id,
                sentence_type=SentenceType.MIDDLE,
                content_type=ContentType.TEXT,
                content_detail=text,
            )
        )
        conn.tts.tts_text_queue.put(
            TTSMessageDTO(
                sentence_id=conn.sentence_id,
                sentence_type=SentenceType.MIDDLE,
                content_type=ContentType.FILE,
                content_file=music_path,
            )
        )
        if conn.intent_type == "intent_llm":
            conn.tts.tts_text_queue.put(
                TTSMessageDTO(
                    sentence_id=conn.sentence_id,
                    sentence_type=SentenceType.LAST,
                    content_type=ContentType.ACTION,
                )
            )

    except Exception as e:
        conn.logger.bind(tag=TAG).error(f"thất bại: {str(e)}")
        conn.logger.bind(tag=TAG).error(f"sai: {traceback.format_exc()}")
