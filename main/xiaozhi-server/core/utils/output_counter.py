import datetime
from typing import Dict, Tuple

# toàn cục，dùng cholưu trữmỗira
_device_daily_output: Dict[Tuple[str, datetime.date], int] = {}
# ghi lạisaulầnkiểm tra
_last_check_date: datetime.date = None


def reset_device_output():
    """
    đặt lạicóra
    0sử dụngnàyhàm
    """
    _device_daily_output.clear()


def get_device_output(device_id: str) -> int:
    """
    lấyra
    """
    current_date = datetime.datetime.now().date()
    return _device_daily_output.get((device_id, current_date), 0)


def add_device_output(device_id: str, char_count: int):
    """
    ra
    """
    current_date = datetime.datetime.now().date()
    global _last_check_date

    # nhưlầnsử dụnghoặc，
    if _last_check_date is None or _last_check_date != current_date:
        _device_daily_output.clear()
        _last_check_date = current_date

    current_count = _device_daily_output.get((device_id, current_date), 0)
    _device_daily_output[(device_id, current_date)] = current_count + char_count


def check_device_output_limit(device_id: str, max_output_size: int) -> bool:
    """
    kiểm tracóvượt quára
    :return: True nhưvượt quá，False nhưvượt quá
    """
    if not device_id:
        return False
    current_output = get_device_output(device_id)
    return current_output >= max_output_size
