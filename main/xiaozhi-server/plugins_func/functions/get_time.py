from datetime import datetime
import cnlunar
from plugins_func.register import register_function, ToolType, ActionResponse, Action

get_lunar_function_desc = {
    "type": "function",
    "function": {
        "name": "get_lunar",
        "description": (
            "dùng cho/vàthông tin。"
            "sử dụngcó thểchỉ địnhnội dung，như：、、、、、、v.v.。"
            "nhưkhông cóchỉ địnhnội dung，mặc địnhvà。"
            "đối với'nhiều'、''này，làm chosử dụngcontexttrongthông tin，khôngphảisử dụngnàycông cụ。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "phải，định dạngchoYYYY-MM-DD，như2024-01-01。nhưkhông，làm chosử dụnghiện tại",
                },
                "query": {
                    "type": "string",
                    "description": "phảinội dung，như、、、、、、、v.v.",
                },
            },
            "required": [],
        },
    },
}


@register_function("get_lunar", get_lunar_function_desc, ToolType.WAIT)
def get_lunar(date=None, query=None):
    """
    dùng cholấyhiện tại/，và、、、、、v.v.thông tin
    """
    from core.utils.cache.manager import cache_manager, CacheType

    # nhưtham số，làm chosử dụngchỉ định；làm chosử dụnghiện tại
    if date:
        try:
            now = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return ActionResponse(
                Action.REQLLM,
                f"định dạnglỗi，làm chosử dụngYYYY-MM-DDđịnh dạng，như：2024-01-01",
                None,
            )
    else:
        now = datetime.now()

    current_date = now.strftime("%Y-%m-%d")

    # như query cho None，làm chosử dụngmặc địnhvăn bản
    if query is None:
        query = "mặc địnhvà"

    # thửbộ nhớ đệmlấythông tin
    lunar_cache_key = f"lunar_info_{current_date}"
    cached_lunar_info = cache_manager.get(CacheType.LUNAR, lunar_cache_key)
    if cached_lunar_info:
        return ActionResponse(Action.REQLLM, cached_lunar_info, None)

    response_text = f"theobằngthông tináp dụngyêu cầu，vàvới{query}thông tin：\n"

    lunar = cnlunar.Lunar(now, godType="8char")
    response_text += (
        "thông tin：\n"
        "%s%s%s\n" % (lunar.lunarYearCn, lunar.lunarMonthCn[:-1], lunar.lunarDayCn)
        + ": %s %s %s\n" % (lunar.year8Char, lunar.month8Char, lunar.day8Char)
        + ": %s\n" % (lunar.chineseYearZodiac)
        + ": %s\n"
        % (
            " ".join(
                [lunar.year8Char, lunar.month8Char, lunar.day8Char, lunar.twohour8Char]
            )
        )
        + ": %s\n"
        % (
            ",".join(
                filter(
                    None,
                    (
                        lunar.get_legalHolidays(),
                        lunar.get_otherHolidays(),
                        lunar.get_otherLunarHolidays(),
                    ),
                )
            )
        )
        + ": %s\n" % (lunar.todaySolarTerms)
        + ": %s %s%s%s\n"
        % (
            lunar.nextSolarTerm,
            lunar.nextSolarTermYear,
            lunar.nextSolarTermDate[0],
            lunar.nextSolarTermDate[1],
        )
        + ": %s\n"
        % (
            ", ".join(
                [
                    f"{term}({date[0]}{date[1]})"
                    for term, date in lunar.thisYearSolarTermsDic.items()
                ]
            )
        )
        + ": %s\n" % (lunar.chineseZodiacClash)
        + ": %s\n" % (lunar.starZodiac)
        + ": %s\n" % lunar.get_nayin()
        + ": %s\n" % (lunar.get_pengTaboo(delimit=", "))
        + ": %s\n" % lunar.get_today12DayOfficer()[0]
        + ": %s(%s)\n"
        % (lunar.get_today12DayOfficer()[1], lunar.get_today12DayOfficer()[2])
        + ": %s\n" % lunar.get_the28Stars()
        + ": %s\n" % " ".join(lunar.get_luckyGodsDirection())
        + ": %s\n" % lunar.get_fetalGod()
        + ": %s\n" % "、".join(lunar.goodThing[:10])
        + ": %s\n" % "、".join(lunar.badThing[:10])
        + "(mặc địnhtrả vềvà；chỉtạiphảithông tinthờitrả về)"
    )

    # bộ nhớ đệmthông tin
    cache_manager.set(CacheType.LUNAR, lunar_cache_key, response_text)

    return ActionResponse(Action.REQLLM, response_text, None)
