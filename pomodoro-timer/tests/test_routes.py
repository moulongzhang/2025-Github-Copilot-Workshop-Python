"""Routes のユニットテスト"""
import pytest


class TestRoutes:
    """ルーティングのテスト"""

    def test_index_returns_html(self, client):
        """メインページがHTMLを返す"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
        assert 'text/html' in response.content_type

    def test_index_contains_timer_elements(self, client):
        """メインページにタイマー要素が含まれる"""
        response = client.get('/')
        html = response.data.decode('utf-8')
        assert 'timer-display' in html
        assert 'start-btn' in html
        assert 'reset-btn' in html
        assert 'progress-circle' in html

    def test_get_settings_returns_json(self, client):
        """設定APIがJSONを返す"""
        response = client.get('/api/settings')
        assert response.status_code == 200
        assert response.content_type == 'application/json'

    def test_get_settings_contains_all_values(self, client):
        """設定APIが全ての設定値を含む"""
        response = client.get('/api/settings')
        data = response.get_json()
        assert 'pomodoro' in data
        assert 'shortBreak' in data
        assert 'longBreak' in data

    def test_get_settings_values_are_correct(self, client):
        """設定APIの値が正しい（TestConfig使用）"""
        response = client.get('/api/settings')
        data = response.get_json()
        # TestConfigでは短い時間が設定されている
        assert data['pomodoro'] == 1
        assert data['shortBreak'] == 1
        assert data['longBreak'] == 2

    def test_post_settings_accepts_json(self, client):
        """設定保存APIがJSONを受け付ける"""
        response = client.post('/api/settings',
                               json={'pomodoro': 30, 'shortBreak': 10, 'longBreak': 20})
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'

    def test_post_settings_echoes_received_data(self, client):
        """設定保存APIが受信データを返す"""
        test_data = {'pomodoro': 30, 'shortBreak': 10, 'longBreak': 20}
        response = client.post('/api/settings', json=test_data)
        data = response.get_json()
        assert data['received'] == test_data

    def test_404_for_unknown_route(self, client):
        """存在しないルートは404"""
        response = client.get('/unknown')
        assert response.status_code == 404
