"""
Flaskアプリケーションのユニットテスト
"""
import pytest
import sys
import os

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


class TestFlaskApp:
    """Flaskアプリケーションのテストクラス"""
    
    @pytest.fixture
    def client(self):
        """テストクライアントのフィクスチャ"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_index_route(self, client):
        """メインページのテスト"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
        assert 'ポモドーロタイマー'.encode('utf-8') in response.data
    
    def test_index_contains_required_elements(self, client):
        """メインページに必要な要素が含まれているかテスト"""
        response = client.get('/')
        assert response.status_code == 200
        
        # HTMLの基本構造
        assert b'<div class="container">' in response.data
        assert b'<div class="timer-container">' in response.data
        
        # タイマー表示要素
        assert b'<div class="time">25:00</div>' in response.data
        assert '作業中'.encode('utf-8') in response.data
        
        # ボタン要素
        assert b'<button id="start-btn"' in response.data
        assert b'<button id="reset-btn"' in response.data  # stop-btnを削除
        
        # カウンター要素
        assert '完了したポモドーロ:'.encode('utf-8') in response.data
        assert b'<span class="counter-value">0</span>' in response.data
    
    def test_static_files_paths(self, client):
        """静的ファイルのパスが正しく含まれているかテスト"""
        response = client.get('/')
        assert response.status_code == 200
        
        # CSS, JSファイルへのパス
        assert b'/static/css/style.css' in response.data
        assert b'/static/js/timer.js' in response.data
    
    def test_css_file_accessible(self, client):
        """CSSファイルにアクセス可能かテスト"""
        response = client.get('/static/css/style.css')
        assert response.status_code == 200
        assert b'body {' in response.data
        assert b'timer-container' in response.data
    
    def test_js_file_accessible(self, client):
        """JavaScriptファイルにアクセス可能かテスト"""
        response = client.get('/static/js/timer.js')
        assert response.status_code == 200
        assert b'PomodoroTimer' in response.data
        assert b'addEventListener' in response.data
    
    def test_app_configuration(self):
        """アプリケーションの基本設定テスト"""
        assert app.name == 'app'
        assert app.template_folder == 'templates'
        # static_folderは絶対パスになるため、末尾のみをチェック
        assert app.static_folder.endswith('static')
    
    def test_404_error(self, client):
        """存在しないページへのアクセステスト"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
