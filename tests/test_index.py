import pytest
from app import create_app

@ pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app


def test_index_contains_pomodoro(app):
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Pomodoro' in resp.data
