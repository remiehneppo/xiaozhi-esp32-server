import re
import os
import json
import copy
import wave
import socket
import asyncio
import requests
import subprocess
import numpy as np
import opuslib_next
from io import BytesIO
from core.utils import p3
from pydub import AudioSegment
from typing import Callable, Any

TAG = __name__


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to Google's DNS servers
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return "127.0.0.1"


def is_private_ip(ip_addr):
    """
    Check if an IP address is a private IP address (compatible with IPv4 and IPv6).

    @param {string} ip_addr - The IP address to check.
    @return {bool} True if the IP address is private, False otherwise.
    """
    try:
        # Validate IPv4 or IPv6 address format
        if not re.match(
            r"^(\d{1,3}\.){3}\d{1,3}$|^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$", ip_addr
        ):
            return False  # Invalid IP address format

        # IPv4 private address ranges
        if "." in ip_addr:  # IPv4 address
            ip_parts = list(map(int, ip_addr.split(".")))
            if ip_parts[0] == 10:
                return True  # 10.0.0.0/8 range
            elif ip_parts[0] == 172 and 16 <= ip_parts[1] <= 31:
                return True  # 172.16.0.0/12 range
            elif ip_parts[0] == 192 and ip_parts[1] == 168:
                return True  # 192.168.0.0/16 range
            elif ip_addr == "127.0.0.1":
                return True  # Loopback address
            elif ip_parts[0] == 169 and ip_parts[1] == 254:
                return True  # Link-local address 169.254.0.0/16
            else:
                return False  # Not a private IPv4 address
        else:  # IPv6 address
            ip_addr = ip_addr.lower()
            if ip_addr.startswith("fc00:") or ip_addr.startswith("fd00:"):
                return True  # Unique Local Addresses (FC00::/7)
            elif ip_addr == "::1":
                return True  # Loopback address
            elif ip_addr.startswith("fe80:"):
                return True  # Link-local unicast addresses (FE80::/10)
            else:
                return False  # Not a private IPv6 address

    except (ValueError, IndexError):
        return False  # IP address format error or insufficient segments


def get_ip_info(ip_addr, logger):
    try:
        # Nhập trình quản lý bộ nhớ cache toàn cục
        from core.utils.cache.manager import cache_manager, CacheType

        # Lấy từ cache trước
        cached_ip_info = cache_manager.get(CacheType.IP_INFO, ip_addr)
        if cached_ip_info is not None:
            return cached_ip_info

        # Cache miss, gọi API
        if is_private_ip(ip_addr):
            ip_addr = ""
        url = f"https://whois.pconline.com.cn/ipJson.jsp?json=true&ip={ip_addr}"
        resp = requests.get(url).json()
        ip_info = {"city": resp.get("city")}

        # Lưu vào cache
        cache_manager.set(CacheType.IP_INFO, ip_addr, ip_info)
        return ip_info
    except Exception as e:
        logger.bind(tag=TAG).error(f"Error getting client ip info: {e}")
        return {}


def write_json_file(file_path, data):
    """Ghi dữ liệu vào file JSON"""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def remove_punctuation_and_length(text):
    # Phạm vi Unicode của ký tự full-width và half-width
    full_width_punctuations = (
        "！＂＃＄％＆＇（）＊＋，－。／：；＜＝＞？＠［＼］＾＿｀｛｜｝～"
    )
    half_width_punctuations = r'!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
    space = " "  # Dấu cách half-width
    full_width_space = "　"  # 

    # Loại bỏ ký tự full-width, half-width và khoảng cách
    result = "".join(
        [
            char
            for char in text
            if char not in full_width_punctuations
            and char not in half_width_punctuations
            and char not in space
            and char not in full_width_space
        ]
    )

    if result == "Yeah":
        return 0, ""
    return len(result), result


def check_model_key(modelType, modelKey):
    if "bạn" in modelKey:
        return f"Lỗi cấu hình: API key của {modelType} chưa được thiết lập, giá trị hiện tại là: {modelKey}"
    return None


def parse_string_to_list(value, separator=";"):
    """
    Chuyển đổi input value thành list
    Args:
        value: Giá trị đầu vào, có thể là None, chuỗi hoặc list
        separator: Ký tự phân cách, mặc định là dấu chấm phẩy
    Returns:
        list: List sau khi xử lý
    """
    if value is None or value == "":
        return []
    elif isinstance(value, str):
        return [item.strip() for item in value.split(separator) if item.strip()]
    elif isinstance(value, list):
        return value
    return []


def check_ffmpeg_installed() -> bool:
    """
    Kiểm tra ffmpeg đã được cài đặt và có thể thực thi trong current environment chưa.

    Returns:
        bool: Nếu ffmpeg hoạt động bình thường, trả về True; ngược lại ném ngoại lệ ValueError.

    Raises:
        ValueError: Khi phát hiện ffmpeg chưa được cài đặt hoặc thiếu dependency, ném thông tin chi tiết.
    """
    try:
        # Thử thực thi lệnh ffmpeg
        result = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,  # Mã thoát khác 0 sẽ kích hoạt CalledProcessError
        )

        output = (result.stdout + result.stderr).lower()
        if "ffmpeg version" in output:
            return True

        # Nếu không phát hiện thông tin phiên bản, cũng xem là trường hợp bất thường
        raise ValueError("Không phát hiện thông tin phiên bản ffmpeg hợp lệ.")

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        # Trích xuất thông báo lỗi
        stderr_output = ""
        if isinstance(e, subprocess.CalledProcessError):
            stderr_output = (e.stderr or "").strip()
        else:
            stderr_output = str(e).strip()

        # Xây dựng cảnh báo lỗi cơ bản
        error_msg = [
            "❌ Phát hiện ffmpeg không thể hoạt động bình thường.\n",
            "Đề xuất:",
            "1. Xác nhận đã kích hoạt đúng môi trường conda;",
            "2. Tham khảo tài liệu cài đặt dự án để biết cách cài đặt ffmpeg trong môi trường conda.\n",
        ]

        # 🎯 Cung cấp thông tin bổ sung dựa trên thông báo lỗi cụ thể
        if "libiconv.so.2" in stderr_output:
            error_msg.append("⚠️ Phát hiện thiếu dependency: libiconv.so.2")
            error_msg.append("Cách xử lý: Thực thi trong môi trường conda hiện tại:")
            error_msg.append("   conda install -c conda-forge libiconv\n")
        elif (
            "no such file or directory" in stderr_output
            and "ffmpeg" in stderr_output.lower()
        ):
            error_msg.append("⚠️ Hệ thống không tìm thấy file thực thi ffmpeg.")
            error_msg.append("Cách xử lý: Thực thi trong môi trường conda hiện tại:")
            error_msg.append("   conda install -c conda-forge ffmpeg\n")
        else:
            error_msg.append("Chi tiết lỗi:")
            error_msg.append(stderr_output or "Lỗi không xác định.")

        # Ném chi tiết exception info
        raise ValueError("\n".join(error_msg)) from e


def extract_json_from_string(input_string):
    """Trích xuất phần JSON trong chuỗi"""
    pattern = r"(\{.*\})"
    match = re.search(pattern, input_string, re.DOTALL)  # Thêm re.DOTALL
    if match:
        return match.group(1)  # Trả về chuỗi JSON đã trích xuất
    return None


def audio_to_data_stream(
    audio_file_path, is_opus=True, callback: Callable[[Any], Any] = None, sample_rate=16000, opus_encoder=None
) -> None:
    # Lấy phần mở rộng file
    file_type = os.path.splitext(audio_file_path)[1]
    if file_type:
        file_type = file_type.lstrip(".")
    # Đọc file âm thanh, tham số -nostdin: Không đọc dữ liệu từ stdin, nếu không FFmpeg sẽ block
    audio = AudioSegment.from_file(
        audio_file_path, format=file_type, parameters=["-nostdin"]
    )

    # Chuyển đổi sang mono/tốc độ lấy mẫu chỉ định/16-bit little-endian (đảm bảo khớp với encoder)
    audio = audio.set_channels(1).set_frame_rate(sample_rate).set_sample_width(2)

    # Lấy dữ liệu PCM gốc (16-bit little-endian)
    raw_data = audio.raw_data
    pcm_to_data_stream(raw_data, is_opus, callback, sample_rate, opus_encoder)


async def audio_to_data(
    audio_file_path: str, is_opus: bool = True, use_cache: bool = True
) -> list[bytes]:
    """
    Chuyển đổi audio file thành danh sách frame Opus/PCM encoded
    Args:
        audio_file_path: Đường dẫn audio file
        is_opus: Có thực hiện Opus encoding không
        use_cache: Có sử dụng cache không
    """
    from core.utils.cache.manager import cache_manager
    from core.utils.cache.config import CacheType

    # Sinh cache key, chứa file path và encoding type
    cache_key = f"{audio_file_path}:{is_opus}"

    # Thử lấy kết quả từ cache
    if use_cache:
        cached_result = cache_manager.get(CacheType.AUDIO_DATA, cache_key)
        if cached_result is not None:
            return cached_result

    def _sync_audio_to_data():
        # Lấy phần mở rộng file
        file_type = os.path.splitext(audio_file_path)[1]
        if file_type:
            file_type = file_type.lstrip(".")
        # Đọc file âm thanh, tham số -nostdin: Không đọc dữ liệu từ stdin, nếu không FFmpeg sẽ block
        audio = AudioSegment.from_file(
            audio_file_path, format=file_type, parameters=["-nostdin"]
        )

        # chuyển đổicho/16kHztần số lấy mẫu/16mã hóa（đảm bảovớimã hóakhớp）
        audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)

        # Lấy dữ liệu PCM gốc (16-bit little-endian)
        raw_data = audio.raw_data

        # khởi tạoOpusmã hóa
        encoder = opuslib_next.Encoder(16000, 1, opuslib_next.APPLICATION_AUDIO)

        # mã hóatham số
        frame_duration = 60  # 60ms per frame
        frame_size = int(16000 * frame_duration / 1000)  # 960 samples/frame

        datas = []
        # theokhungxử lýcódữ liệu âm thanh（bao gồmsaukhungcó thể）
        for i in range(0, len(raw_data), frame_size * 2):  # 16bit=2bytes/sample
            # lấyhiện tạikhungcủdữ liệu
            chunk = raw_data[i : i + frame_size * 2]

            # nhưsaukhungkhông，
            if len(chunk) < frame_size * 2:
                chunk += b"\x00" * (frame_size * 2 - len(chunk))

            if is_opus:
                # chuyển đổichonumpyxử lý
                np_frame = np.frombuffer(chunk, dtype=np.int16)
                # mã hóaOpusdữ liệu
                frame_data = encoder.encode(np_frame.tobytes(), frame_size)
            else:
                frame_data = chunk if isinstance(chunk, bytes) else bytes(chunk)

            datas.append(frame_data)

        return datas

    loop = asyncio.get_running_loop()
    # tại/trongcủluồngtrongcủâm thanhxử lý
    result = await loop.run_in_executor(None, _sync_audio_to_data)

    # sẽkết quảvàobộ nhớ đệm，làm chosử dụngcấu hìnhtrongđịnh nghĩacủTTL（10）
    if use_cache:
        cache_manager.set(CacheType.AUDIO_DATA, cache_key, result)

    return result


def audio_bytes_to_data_stream(
    audio_bytes, file_type, is_opus, callback: Callable[[Any], Any], sample_rate=16000, opus_encoder=None
) -> None:
    """
    sử dụngâm thanhdữ liệuchoopus/pcmdữ liệu，wav、mp3、p3
    """
    if file_type == "p3":
        # sử dụngp3giải mã
        return p3.decode_opus_from_bytes_stream(audio_bytes, callback)
    else:
        # nó/của nóđịnh dạngsử dụngpydub
        audio = AudioSegment.from_file(
            BytesIO(audio_bytes), format=file_type, parameters=["-nostdin"]
        )
        audio = audio.set_channels(1).set_frame_rate(sample_rate).set_sample_width(2)
        raw_data = audio.raw_data
        pcm_to_data_stream(raw_data, is_opus, callback, sample_rate, opus_encoder)


def pcm_to_data_stream(raw_data, is_opus=True, callback: Callable[[Any], Any] = None, sample_rate=16000, opus_encoder=None):
    """
    sẽPCMdữ liệuluồngmã hóachoOpushoặcraPCM

    Args:
        raw_data: PCMban đầudữ liệu
        is_opus: làmã hóachoOpus
        callback: hàm
        sample_rate: tần số lấy mẫu
        opus_encoder: OpusEncoderUtilsvới(bằngmã hóatrạng thái)
    """
    using_temp_encoder = False
    if is_opus and opus_encoder is None:
        encoder = opuslib_next.Encoder(sample_rate, 1, opuslib_next.APPLICATION_AUDIO)
        using_temp_encoder = True

    # mã hóatham số
    frame_duration = 60  # 60ms per frame
    frame_size = int(sample_rate * frame_duration / 1000)  # samples/frame

    # theokhungxử lýcódữ liệu âm thanh（bao gồmsaukhungcó thể）
    for i in range(0, len(raw_data), frame_size * 2):  # 16bit=2bytes/sample
        # lấyhiện tạikhungcủdữ liệu
        chunk = raw_data[i : i + frame_size * 2]

        # nhưsaukhungkhông，
        if len(chunk) < frame_size * 2:
            chunk += b"\x00" * (frame_size * 2 - len(chunk))

        if is_opus:
            if using_temp_encoder:
                # sử dụngtạm thờimã hóa（chỉsử dụngtạiâm thanh）
                np_frame = np.frombuffer(chunk, dtype=np.int16)
                frame_data = encoder.encode(np_frame.tobytes(), frame_size)
                callback(frame_data)
            else:
                # sử dụngbên ngoàimã hóa（TTSluồng,trạng thái）
                is_last = (i + frame_size * 2 >= len(raw_data))
                opus_encoder.encode_pcm_to_opus_stream(chunk, end_of_stream=is_last, callback=callback)
        else:
            # PCMchế độ,ra
            frame_data = chunk if isinstance(chunk, bytes) else bytes(chunk)
            callback(frame_data)


def opus_datas_to_wav_bytes(opus_datas, sample_rate=16000, channels=1):
    """
    sẽopuskhunggiải mãchowav
    """
    decoder = opuslib_next.Decoder(sample_rate, channels)
    try:
        pcm_datas = []

        frame_duration = 60  # ms
        frame_size = int(sample_rate * frame_duration / 1000)  # 960

        for opus_frame in opus_datas:
            # giải mãchoPCM（trả vềbytes，2/）
            pcm = decoder.decode(opus_frame, frame_size)
            pcm_datas.append(pcm)

        pcm_bytes = b"".join(pcm_datas)

        # ghiwav
        wav_buffer = BytesIO()
        with wave.open(wav_buffer, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 16bit
            wf.setframerate(sample_rate)
            wf.writeframes(pcm_bytes)
        return wav_buffer.getvalue()
    finally:
        if decoder is not None:
            try:
                del decoder
            except Exception:
                pass


def check_vad_update(before_config, new_config):
    if (
        new_config.get("selected_module") is None
        or new_config["selected_module"].get("VAD") is None
    ):
        return False
    update_vad = False
    current_vad_module = before_config["selected_module"]["VAD"]
    new_vad_module = new_config["selected_module"]["VAD"]
    current_vad_type = (
        current_vad_module
        if "type" not in before_config["VAD"][current_vad_module]
        else before_config["VAD"][current_vad_module]["type"]
    )
    new_vad_type = (
        new_vad_module
        if "type" not in new_config["VAD"][new_vad_module]
        else new_config["VAD"][new_vad_module]["type"]
    )
    update_vad = current_vad_type != new_vad_type
    return update_vad


def check_asr_update(before_config, new_config):
    if (
        new_config.get("selected_module") is None
        or new_config["selected_module"].get("ASR") is None
    ):
        return False
    update_asr = False
    current_asr_module = before_config["selected_module"]["ASR"]
    new_asr_module = new_config["selected_module"]["ASR"]

    # nhưkhông，thìcầncập nhật
    if current_asr_module != new_asr_module:
        return True

    # như，
    current_asr_type = (
        current_asr_module
        if "type" not in before_config["ASR"][current_asr_module]
        else before_config["ASR"][current_asr_module]["type"]
    )
    new_asr_type = (
        new_asr_module
        if "type" not in new_config["ASR"][new_asr_module]
        else new_config["ASR"][new_asr_module]["type"]
    )
    update_asr = current_asr_type != new_asr_type
    return update_asr


def filter_sensitive_info(config: dict) -> dict:
    """
    lọccấu hìnhtrongcủthông tin
    Args:
        config: ban đầucấu hình
    Returns:
        lọcsaucủcấu hình
    """
    sensitive_keys = [
        "api_key",
        "personal_access_token",
        "access_token",
        "token",
        "secret",
        "access_key_secret",
        "secret_key",
    ]

    def _filter_dict(d: dict) -> dict:
        filtered = {}
        for k, v in d.items():
            if any(sensitive in k.lower() for sensitive in sensitive_keys):
                filtered[k] = "***"
            elif isinstance(v, dict):
                filtered[k] = _filter_dict(v)
            elif isinstance(v, list):
                filtered[k] = [_filter_dict(i) if isinstance(i, dict) else i for i in v]
            elif isinstance(v, str):
                try:
                    json_data = json.loads(v)
                    if isinstance(json_data, dict):
                        filtered[k] = json.dumps(
                            _filter_dict(json_data), ensure_ascii=False
                        )
                    else:
                        filtered[k] = v
                except (json.JSONDecodeError, TypeError):
                    filtered[k] = v
            else:
                filtered[k] = v
        return filtered

    return _filter_dict(copy.deepcopy(config))


def get_vision_url(config: dict) -> str:
    """lấy vision URL

    Args:
        config: cấu hình

    Returns:
        str: vision URL
    """
    server_config = config["server"]
    vision_explain = server_config.get("vision_explain", "")
    if "củ" in vision_explain:
        local_ip = get_local_ip()
        port = int(server_config.get("http_port", 8003))
        vision_explain = f"http://{local_ip}:{port}/mcp/vision/explain"
    return vision_explain


def is_valid_image_file(file_data: bytes) -> bool:
    """
    kiểm tratệpdữ liệulàchohiệu quảcủđịnh dạng

    Args:
        file_data: tệpcủdữ liệu

    Returns:
        bool: nhưlàhiệu quảcủđịnh dạngtrả vềTrue，trả vềFalse
    """
    # định dạngcủ（tệp）
    image_signatures = {
        b"\xff\xd8\xff": "JPEG",
        b"\x89PNG\r\n\x1a\n": "PNG",
        b"GIF87a": "GIF",
        b"GIF89a": "GIF",
        b"BM": "BMP",
        b"II*\x00": "TIFF",
        b"MM\x00*": "TIFF",
        b"RIFF": "WEBP",
    }

    # kiểm tratệplàkhớpđãcủđịnh dạng
    for signature in image_signatures:
        if file_data.startswith(signature):
            return True

    return False


def sanitize_tool_name(name: str) -> str:
    """Sanitize tool names for OpenAI compatibility."""
    # trong、、、vàký tự
    return re.sub(r"[^a-zA-Z0-9_\-\u4e00-\u9fff]", "_", name)


def validate_mcp_endpoint(mcp_endpoint: str) -> bool:
    """
    kiểm traMCPvàođịnh dạng

    Args:
        mcp_endpoint: MCPvàoký tự

    Returns:
        bool: làhiệu quả
    """
    # 1. kiểm tralàbằngwsbắt đầu
    if not mcp_endpoint.startswith("ws"):
        return False

    # 2. kiểm tralàkey、call
    if "key" in mcp_endpoint.lower() or "call" in mcp_endpoint.lower():
        return False

    # 3. kiểm tralà/mcp/
    if "/mcp/" not in mcp_endpoint:
        return False

    return True

def get_system_error_response(config: dict) -> str:
    """lấysaikhi/thờicủ

    Args:
        config: cấu hình

    Returns:
        str: saikhi/thờicủ
    """
    return config.get("system_error_response", "，tại/trongcó，tôinhữngsau。")