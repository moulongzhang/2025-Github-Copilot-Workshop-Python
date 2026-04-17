import json
import pytest
from models import SessionRepository


@pytest.fixture
def repo(tmp_path):
    return SessionRepository(filepath=str(tmp_path / "sessions.json"))


# --- find_by_date ---

def test_find_by_date_returns_empty_when_file_not_exists(tmp_path):
    repo = SessionRepository(filepath=str(tmp_path / "nonexistent.json"))
    assert repo.find_by_date("2026-04-17") == []


def test_find_by_date_returns_matching_sessions(repo):
    repo.save({"date": "2026-04-17", "duration_minutes": 25, "completed_at": "10:00:00"})
    repo.save({"date": "2026-04-16", "duration_minutes": 25, "completed_at": "10:00:00"})
    result = repo.find_by_date("2026-04-17")
    assert len(result) == 1
    assert result[0]["date"] == "2026-04-17"


def test_find_by_date_returns_empty_when_no_match(repo):
    repo.save({"date": "2026-04-16", "duration_minutes": 25, "completed_at": "10:00:00"})
    assert repo.find_by_date("2026-04-17") == []


# --- save ---

def test_save_assigns_sequential_ids(repo):
    repo.save({"date": "2026-04-17", "duration_minutes": 25, "completed_at": "10:00:00"})
    repo.save({"date": "2026-04-17", "duration_minutes": 25, "completed_at": "11:00:00"})
    result = repo.find_by_date("2026-04-17")
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


def test_save_persists_to_file(repo, tmp_path):
    repo.save({"date": "2026-04-17", "duration_minutes": 25, "completed_at": "10:00:00"})
    with open(repo.filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["date"] == "2026-04-17"


def test_save_appends_to_existing_data(repo):
    repo.save({"date": "2026-04-17", "duration_minutes": 25, "completed_at": "10:00:00"})
    repo.save({"date": "2026-04-17", "duration_minutes": 25, "completed_at": "11:00:00"})
    result = repo.find_by_date("2026-04-17")
    assert len(result) == 2
