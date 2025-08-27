"""
Flaskアプリケーションのユニットテスト
"""
import json
import pytest
from app import app


class TestFlaskApp:
    """Flaskアプリケーションのテストクラス"""

    def test_index_route(self, client):
        """メインページのテスト"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'pomodoro' in response.data.lower()
        assert b'<!DOCTYPE html>' in response.data

    def test_health_check(self, client):
        """ヘルスチェックエンドポイントのテスト"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'ポモドーロタイマー' in data['message']

    def test_settings_get(self, client):
        """設定取得APIのテスト"""
        response = client.get('/api/settings')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'workDuration' in data
        assert 'shortBreakDuration' in data
        assert 'longBreakDuration' in data
        assert data['workDuration'] == 25
        assert data['shortBreakDuration'] == 5
        assert data['longBreakDuration'] == 15

    def test_settings_post(self, client):
        """設定保存APIのテスト"""
        test_settings = {
            'workDuration': 30,
            'shortBreakDuration': 10,
            'longBreakDuration': 20,
            'sessionsUntilLongBreak': 3,
            'autoStartBreaks': True,
            'autoStartWork': False,
            'soundNotifications': False
        }
        
        response = client.post('/api/settings', 
                             data=json.dumps(test_settings),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert '保存されました' in data['message']

    def test_404_error(self, client):
        """404エラーハンドリングのテスト"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        # 404の場合もindex.htmlが返される
        assert b'<!DOCTYPE html>' in response.data

    def test_static_files(self, client):
        """静的ファイルのテスト"""
        # CSSファイルのテスト
        response = client.get('/static/css/style.css')
        assert response.status_code == 200
        assert b'timer-display' in response.data  # 'pomodoro'の代わりに確実に存在するクラス名を使用
        
        # JavaScriptファイルのテスト
        response = client.get('/static/js/app.js')
        assert response.status_code == 200
        assert b'PomodoroTimer' in response.data
