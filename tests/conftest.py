"""
pytest設定ファイル
"""
import pytest
import sys
import os

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, socketio

@pytest.fixture
def client():
    """Flaskテストクライアントの設定"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def socketio_client():
    """SocketIOテストクライアントの設定"""
    app.config['TESTING'] = True
    
    client = socketio.test_client(app, flask_test_client=app.test_client())
    return client
