"""Tiện ích lấy thời gian hiện tại cho prompt hệ thống."""

import cnlunar
from datetime import datetime

WEEKDAY_MAP = {
    "Monday": "Thứ Hai",
    "Tuesday": "Thứ Ba",
    "Wednesday": "Thứ Tư",
    "Thursday": "Thứ Năm",
    "Friday": "Thứ Sáu",
    "Saturday": "Thứ Bảy",
    "Sunday": "Chủ Nhật",
}


def get_current_time() -> str:
    """Lấy thời gian hiện tại, định dạng HH:MM."""
    return datetime.now().strftime("%H:%M")


def get_current_date() -> str:
    """Lấy ngày hiện tại, định dạng YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def get_current_weekday() -> str:
    """Lấy thứ trong tuần bằng tiếng Việt."""
    now = datetime.now()
    return WEEKDAY_MAP[now.strftime("%A")]


def get_current_lunar_date() -> str:
    """Lấy ngày âm lịch nếu thư viện cnlunar khả dụng."""
    try:
        now = datetime.now()
        today_lunar = cnlunar.Lunar(now, godType="8char")
        return "%s%s%s" % (
            today_lunar.lunarYearCn,
            today_lunar.lunarMonthCn[:-1],
            today_lunar.lunarDayCn,
        )
    except Exception:
        return "không lấy được âm lịch"


def get_current_time_info() -> tuple:
    """Trả về (giờ hiện tại, ngày hiện tại, thứ trong tuần, ngày âm lịch)."""
    current_time = get_current_time()
    today_date = get_current_date()
    today_weekday = get_current_weekday()
    lunar_date = get_current_lunar_date()
    
    return current_time, today_date, today_weekday, lunar_date
