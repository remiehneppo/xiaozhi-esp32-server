import re
from config.logger import setup_logging

TAG = __name__
logger = setup_logging()

EMOTION_EMOJI_MAP = {
    "HAPPY": "🙂",
    "SAD": "😔",
    "ANGRY": "😡",
    "NEUTRAL": "😶",
    "FEARFUL": "😰",
    "DISGUSTED": "🤢",
    "SURPRISED": "😲",
    "EMO_UNKNOWN": "😶",  # không xác địnhmặc địnhsử dụngtrong
}
# EVENT_EMOJI_MAP = {
#     "<|BGM|>": "🎼",
#     "<|Speech|>": "",
#     "<|Applause|>": "👏",
#     "<|Laughter|>": "😀",
#     "<|Cry|>": "😭",
#     "<|Sneeze|>": "🤧",
#     "<|Breath|>": "",
#     "<|Cough|>": "🤧",
# }

def lang_tag_filter(text: str) -> dict | str:
    """
    phân tích FunASR nhận dạngkết quả，vàvăn bảnnội dung

    Args:
        text: ASR nhận dạngban đầuvăn bản，có thểnhiều

    Returns:
        dict: {"language": "zh", "emotion": "SAD", "emoji": "😔", "content": "Xin chào"} nhưcó
        str: văn bản，nhưkhông có

    Examples:
        FunASR rađịnh dạng：<||><||><||><|nó|>
        >>> lang_tag_filter("<|zh|><|SAD|><|Speech|><|withitn|>，kiểm trakiểm tra。")
        {"language": "zh", "emotion": "SAD", "emoji": "😔", "content": "，kiểm trakiểm tra。"}
        >>> lang_tag_filter("<|en|><|HAPPY|><|Speech|><|withitn|>Hello hello.")
        {"language": "en", "emotion": "HAPPY", "emoji": "🙂", "content": "Hello hello."}
        >>> lang_tag_filter("plain text")
        "plain text"
    """
    # có（）
    tag_pattern = r"<\|([^|]+)\|>"
    all_tags = re.findall(tag_pattern, text)

    # loại bỏcó <|...|> định dạng，lấyvăn bản
    clean_text = re.sub(tag_pattern, "", text).strip()

    # nhưkhông có，trả vềvăn bản
    if not all_tags:
        return clean_text

    #  FunASR ，trả về dict
    language = all_tags[0] if len(all_tags) > 0 else "zh"
    emotion = all_tags[1] if len(all_tags) > 1 else "NEUTRAL"
    # event = all_tags[2] if len(all_tags) > 2 else "Speech"  # khônglàm chosử dụng

    result = {
        "content": clean_text,
        "language": language,
        "emotion": emotion,
        # "event": event,
    }

    # thêm emoji ánh xạ
    if emotion in EMOTION_EMOJI_MAP:
        result["emotion"] = EMOTION_EMOJI_MAP[emotion]
    # khônglàm chosử dụng
    # if event in EVENT_EMOJI_MAP:
    #     result["event"] = EVENT_EMOJI_MAP[event]

    return result

