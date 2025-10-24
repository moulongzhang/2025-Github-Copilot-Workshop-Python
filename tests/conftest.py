"""
テスト用共通設定とフィクスチャ

pytest実行時に自動的に読み込まれます。
"""

import pytest
import tempfile
import os
from app.factories.app_factory import create_app, db


@pytest.fixture
def app():
    """テスト用Flaskアプリケーション"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """テスト用クライアント"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLIランナー"""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers():
    """認証ヘッダー（将来的な拡張用）"""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


@pytest.fixture
def sample_timer_data():
    """サンプルタイマーデータ"""
    return {
        'duration': 25,
        'session_type': 'work',
        'started_at': '2025-10-24T10:00:00Z'
    }