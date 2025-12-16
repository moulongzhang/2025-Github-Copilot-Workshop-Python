import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"ポモドーロタイマー" in response.data
    assert b"timer-display" in response.data
    assert b"start-btn" in response.data
    assert b"pause-btn" in response.data
    assert b"reset-btn" in response.data
