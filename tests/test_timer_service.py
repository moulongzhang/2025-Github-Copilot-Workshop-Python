from timer_service import get_today_sessions, calculate_total_focus_minutes, format_focus_time


# --- get_today_sessions ---

def test_get_today_sessions_returns_matching_date():
    sessions = [
        {"date": "2026-04-17", "duration_minutes": 25},
        {"date": "2026-04-16", "duration_minutes": 25},
    ]
    result = get_today_sessions(sessions, "2026-04-17")
    assert len(result) == 1
    assert result[0]["date"] == "2026-04-17"


def test_get_today_sessions_returns_empty_when_no_match():
    sessions = [{"date": "2026-04-16", "duration_minutes": 25}]
    result = get_today_sessions(sessions, "2026-04-17")
    assert result == []


def test_get_today_sessions_returns_all_matching():
    sessions = [
        {"date": "2026-04-17", "duration_minutes": 25},
        {"date": "2026-04-17", "duration_minutes": 25},
        {"date": "2026-04-16", "duration_minutes": 25},
    ]
    result = get_today_sessions(sessions, "2026-04-17")
    assert len(result) == 2


def test_get_today_sessions_empty_input():
    assert get_today_sessions([], "2026-04-17") == []


# --- calculate_total_focus_minutes ---

def test_calculate_total_focus_minutes_single():
    assert calculate_total_focus_minutes([{"duration_minutes": 25}]) == 25


def test_calculate_total_focus_minutes_multiple():
    sessions = [{"duration_minutes": 25}, {"duration_minutes": 25}]
    assert calculate_total_focus_minutes(sessions) == 50


def test_calculate_total_focus_minutes_empty():
    assert calculate_total_focus_minutes([]) == 0


# --- format_focus_time ---

def test_format_focus_time_minutes_only():
    assert format_focus_time(25) == "25分"


def test_format_focus_time_exact_hour():
    assert format_focus_time(60) == "1時間"


def test_format_focus_time_hours_and_minutes():
    assert format_focus_time(100) == "1時間40分"


def test_format_focus_time_zero():
    assert format_focus_time(0) == "0分"
