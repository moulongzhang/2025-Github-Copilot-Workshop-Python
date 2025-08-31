import pytest
from app import app, add_history, fetch_history

def test_add_and_fetch_history():
    # Flaskアプリケーションコンテキスト内で実行
    with app.app_context():
        add_history(25, '2025-08-31T10:00:00')
        add_history(15, '2025-08-31T11:00:00')
        # 履歴取得
        history = fetch_history(limit=2)
        assert len(history) == 2
        assert history[0]['work_minutes'] == 15
        assert history[1]['work_minutes'] == 25

def test_api_history(client):
    # POSTで履歴追加
    rv = client.post('/api/history', json={'work_minutes': 30})
    assert rv.status_code == 200
    # GETで履歴取得
    rv = client.get('/api/history')
    assert rv.status_code == 200
    data = rv.get_json()
    assert any(h['work_minutes'] == 30 for h in data)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
