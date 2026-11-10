from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

_UNIT_SECONDS: dict[str, int] = {
    "minute": 60,
    "minutes": 60,
    "min": 60,
    "mins": 60,
    "hour": 3600,
    "hours": 3600,
    "hr": 3600,
    "hrs": 3600,
    "day": 86400,
    "days": 86400,
    "week": 604800,
    "weeks": 604800,
    "month": 2592000,
    "months": 2592000,
    # Vietnamese units
    "phút": 60,
    "gio": 3600,
    "giờ": 3600,
    "ngay": 86400,
    "ngày": 86400,
    "tuan": 604800,
    "tuần": 604800,
    "thang": 2592000,
    "tháng": 2592000,
}

_VN_ALIASES: dict[str, str] = {
    "hôm nay": "today",
    "hom nay": "today",
    "hôm qua": "yesterday",
    "hom qua": "yesterday",
    "tuần này": "this week",
    "tuan nay": "this week",
    "tuần trước": "last week",
    "tuan truoc": "last week",
    "tháng này": "this month",
    "thang nay": "this month",
    "tháng trước": "last month",
    "thang truoc": "last month",
}


def _unit_to_code(value: int, unit: str) -> str:
    unit = unit.lower().rstrip("s")
    if unit in {"hour", "hr", "gio", "giờ"}:
        return f"{value}h"
    if unit in {"day", "ngay", "ngày"}:
        return f"{value}d"
    if unit in {"week", "tuan", "tuần"}:
        return f"{value * 7}d"
    if unit in {"month", "thang", "tháng"}:
        return f"{value * 30}d"
    return f"{value}d"


def _normalize_timeframe(timeframe_lc: str) -> str:
    return _VN_ALIASES.get(timeframe_lc, timeframe_lc)


def datetime_window(
    timeframe: str,
    reference_date: str | None = None,
    tz: str = "UTC",
) -> dict[str, Any]:
    """Chuẩn hoá timeframe ngôn ngữ tự nhiên (VI/EN) thành start/end ISO."""
    if not timeframe or not isinstance(timeframe, str):
        return {"error": "timeframe phải là chuỗi không rỗng."}

    timeframe_raw = timeframe.strip()
    timeframe_lc = _normalize_timeframe(timeframe_raw.lower())

    try:
        tzinfo: timezone | ZoneInfo = ZoneInfo(tz) if tz and tz != "UTC" else timezone.utc
    except Exception:
        return {
            "error": (
                f"Timezone không hợp lệ: {tz!r}. "
                "Dùng tên IANA như 'Asia/Ho_Chi_Minh', 'America/New_York', hoặc 'UTC'."
            )
        }

    if reference_date:
        try:
            now = datetime.fromisoformat(reference_date)
            if now.tzinfo is None:
                now = now.replace(tzinfo=tzinfo)
        except ValueError:
            return {
                "error": (
                    f"Không parse được reference_date: {reference_date!r}. "
                    "Dùng định dạng ISO 8601, ví dụ '2026-11-10T17:00:00'."
                )
            }
    else:
        now = datetime.now(tz=tzinfo)

    end = now
    start = None
    label = timeframe_raw
    timeframe_code: str | None = None

    # EN: last/past N units | N units ago
    match = re.fullmatch(
        r"(?:last|past)\s+(\d+)\s+([a-zA-Z]+)|((\d+)\s+([a-zA-Z]+)\s+ago)",
        timeframe_lc,
    )
    # VI: N ngày/tuần/tháng gần đây | N ngày/tuần/tháng trước | trong N ngày
    vn_match = re.fullmatch(
        r"(?:trong\s+)?(\d+)\s+(phút|gio|giờ|ngay|ngày|tuan|tuần|thang|tháng)"
        r"(?:\s+(?:gần đây|gan day|trước|truoc))?",
        timeframe_lc,
    )

    if match:
        if match.group(1):
            value = int(match.group(1))
            unit = match.group(2)
        else:
            value = int(match.group(4))
            unit = match.group(5)
        unit = unit.lower().rstrip("s")
        if unit not in _UNIT_SECONDS:
            return {"error": f"Đơn vị thời gian không nhận ra: {unit!r}."}
        start = now - timedelta(seconds=_UNIT_SECONDS[unit] * value)
        timeframe_code = _unit_to_code(value, unit)

    elif vn_match:
        value = int(vn_match.group(1))
        unit = vn_match.group(2)
        start = now - timedelta(seconds=_UNIT_SECONDS[unit] * value)
        timeframe_code = _unit_to_code(value, unit)

    elif timeframe_lc == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        timeframe_code = "1d"

    elif timeframe_lc == "yesterday":
        start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start = start_of_today - timedelta(days=1)
        end = start_of_today
        timeframe_code = "1d"

    elif timeframe_lc == "this week":
        start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        timeframe_code = "7d"

    elif timeframe_lc == "last week":
        start_of_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start_of_week
        start = start_of_week - timedelta(days=7)
        timeframe_code = "7d"

    elif timeframe_lc == "this month":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        timeframe_code = "30d"

    elif timeframe_lc == "last month":
        first_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = first_of_month
        if first_of_month.month == 1:
            start = first_of_month.replace(year=first_of_month.year - 1, month=12)
        else:
            start = first_of_month.replace(month=first_of_month.month - 1)
        timeframe_code = "30d"

    else:
        return {
            "error": (
                f"Không thể parse timeframe: {timeframe_raw!r}. "
                "Thử dùng: 'tuần trước', '3 ngày gần đây', 'hôm qua', 'tháng này', "
                "'last 7 days', 'yesterday', 'this week'."
            )
        }

    duration_days = round((end - start).total_seconds() / 86400, 4)
    return {
        "start": start.isoformat(),
        "end": end.isoformat(),
        "label": label,
        "duration_days": duration_days,
        "timeframe_code": timeframe_code,
    }
