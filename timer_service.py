def get_today_sessions(sessions: list[dict], today: str) -> list[dict]:
    return [s for s in sessions if s.get("date") == today]


def calculate_total_focus_minutes(sessions: list[dict]) -> int:
    return sum(s.get("duration_minutes", 0) for s in sessions)


def format_focus_time(total_minutes: int) -> str:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    if hours > 0:
        return f"{hours}時間{minutes}分" if minutes > 0 else f"{hours}時間"
    return f"{minutes}分"
