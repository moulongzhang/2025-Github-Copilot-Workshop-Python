"""
pytest共通設定
"""
import pytest
from app import app as flask_app


@pytest.fixture
def app():
    """Flaskアプリケーションのフィクスチャ"""
    flask_app.config.update({
        'TESTING': True,
    })
    yield flask_app


@pytest.fixture
def client(app):
    """Flaskテストクライアントのフィクスチャ"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Flask CLIランナーのフィクスチャ"""
    return app.test_cli_runner()
