"""pytest フィクスチャ設定"""
import sys
from pathlib import Path

import pytest

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import TestConfig
from pomodoro import create_app
from pomodoro.services.timer_service import TimerService


@pytest.fixture
def app():
    """テスト用Flaskアプリケーション"""
    app = create_app(TestConfig)
    return app


@pytest.fixture
def client(app):
    """テストクライアント"""
    return app.test_client()


@pytest.fixture
def timer_service():
    """テスト用TimerService"""
    return TimerService({
        'pomodoro': 1,
        'short_break': 1,
        'long_break': 2
    })


@pytest.fixture
def default_settings():
    """デフォルトのタイマー設定"""
    return {
        'pomodoro': 25,
        'short_break': 5,
        'long_break': 15
    }
