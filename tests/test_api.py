import pytest


# --- GET / ---

def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


# --- GET /api/sessions ---

def test_get_sessions_returns_empty_initially(client):
    response = client.get("/api/sessions?date=2026-04-17")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 0
    assert data["sessions"] == []
    assert data["total_minutes"] == 0
    assert data["focus_time"] == "0分"


def test_get_sessions_filters_by_date(client):
    # 2日分のセッションを登録
    client.post("/api/sessions", json={"date": "2026-04-17", "duration_minutes": 25, "completed_at": "10:00:00"})
    client.post("/api/sessions", json={"date": "2026-04-16", "duration_minutes": 25, "completed_at": "10:00:00"})

    response = client.get("/api/sessions?date=2026-04-17")
    data = response.get_json()
    assert data["count"] == 1
    assert data["sessions"][0]["date"] == "2026-04-17"


def test_get_sessions_aggregates_total_minutes(client):
    client.post("/api/sessions", json={"date": "2026-04-17", "duration_minutes": 25, "completed_at": "10:00:00"})
    client.post("/api/sessions", json={"date": "2026-04-17", "duration_minutes": 25, "completed_at": "11:00:00"})

    response = client.get("/api/sessions?date=2026-04-17")
    data = response.get_json()
    assert data["count"] == 2
    assert data["total_minutes"] == 50
    assert data["focus_time"] == "50分"


# --- POST /api/sessions ---

def test_post_session_returns_201(client):
    payload = {"date": "2026-04-17", "duration_minutes": 25, "completed_at": "14:30:00"}
    response = client.post("/api/sessions", json=payload)
    assert response.status_code == 201


def test_post_session_response_contains_saved_fields(client):
    payload = {"date": "2026-04-17", "duration_minutes": 25, "completed_at": "14:30:00"}
    response = client.post("/api/sessions", json=payload)
    data = response.get_json()
    assert data["date"] == "2026-04-17"
    assert data["duration_minutes"] == 25
    assert data["completed_at"] == "14:30:00"


def test_post_session_and_retrieve(client):
    payload = {"date": "2026-04-17", "duration_minutes": 25, "completed_at": "14:30:00"}
    client.post("/api/sessions", json=payload)

    get_res = client.get("/api/sessions?date=2026-04-17")
    data = get_res.get_json()
    assert data["count"] == 1
    assert data["sessions"][0]["date"] == "2026-04-17"


# --- バリデーション ---

@pytest.mark.parametrize("missing_field", ["date", "duration_minutes", "completed_at"])
def test_post_session_missing_required_field_returns_400(client, missing_field):
    payload = {"date": "2026-04-17", "duration_minutes": 25, "completed_at": "14:30:00"}
    del payload[missing_field]
    response = client.post("/api/sessions", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_post_session_empty_body_returns_400(client):
    response = client.post("/api/sessions", data="", content_type="application/json")
    assert response.status_code == 400
