"""
thời giancông cụ
thống nhấtthời gianlấycó thể
"""

import cnlunar
from datetime import datetime

WEEKDAY_MAP = {
    "Monday": "",
    "Tuesday": "", 
    "Wednesday": "",
    "Thursday": "",
    "Friday": "",
    "Saturday": "",
    "Sunday": "",
}


def get_current_time() -> str:
    """
    lấyhiện tạithời gianký tự (định dạng: HH:MM)
    """
    return datetime.now().strftime("%H:%M")


def get_current_date() -> str:
    """
    lấyký tự (định dạng: YYYY-MM-DD)
    """
    return datetime.now().strftime("%Y-%m-%d")


def get_current_weekday() -> str:
    """
    lấy
    """
    now = datetime.now()
    return WEEKDAY_MAP[now.strftime("%A")]


def get_current_lunar_date() -> str:
    """
    lấyký tự
    """
    try:
        now = datetime.now()
        today_lunar = cnlunar.Lunar(now, godType="8char")
        return "%s%s%s" % (
            today_lunar.lunarYearCn,
            today_lunar.lunarMonthCn[:-1],
            today_lunar.lunarDayCn,
        )
    except Exception:
        return "lấythất bại"


def get_current_time_info() -> tuple:
    """
    lấyhiện tạithời gianthông tin
    trả về: (hiện tạithời gianký tự, , , )
    """
    current_time = get_current_time()
    today_date = get_current_date()
    today_weekday = get_current_weekday()
    lunar_date = get_current_lunar_date()
    
    return current_time, today_date, today_weekday, lunar_date
