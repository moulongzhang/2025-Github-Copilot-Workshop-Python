import json
import os
from datetime import datetime


class SessionRepository:
    def __init__(self, filepath: str = "sessions.json"):
        self.filepath = filepath

    def _load(self) -> list[dict]:
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_all(self, sessions: list[dict]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)

    def find_by_date(self, date: str) -> list[dict]:
        return [s for s in self._load() if s.get("date") == date]

    def save(self, session: dict) -> None:
        sessions = self._load()
        session["id"] = len(sessions) + 1
        sessions.append(session)
        self._save_all(sessions)
