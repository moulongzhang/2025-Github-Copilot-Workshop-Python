"""
Flaskアプリケーションの統合テスト
"""
import pytest


class TestApp:
    """アプリケーションの基本的なテスト"""
    
    def test_app_exists(self, app):
        """Flaskアプリが存在することを確認"""
        assert app is not None
    
    def test_app_is_testing(self, app):
        """テストモードが有効であることを確認"""
        assert app.config['TESTING'] is True


class TestRoutes:
    """ルーティングのテスト"""
    
    def test_index_route_exists(self, client):
        """トップページが存在することを確認"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_route_returns_html(self, client):
        """トップページがHTMLを返すことを確認"""
        response = client.get('/')
        assert response.content_type == 'text/html; charset=utf-8'
    
    def test_index_route_contains_title(self, client):
        """トップページにタイトルが含まれることを確認"""
        response = client.get('/')
        assert 'ポモドーロタイマー' in response.data.decode('utf-8')
    
    def test_index_route_contains_timer_display(self, client):
        """トップページにタイマー表示が含まれることを確認"""
        response = client.get('/')
        data = response.data.decode('utf-8')
        assert 'timer-text' in data
        assert '25:00' in data
    
    def test_index_route_contains_buttons(self, client):
        """トップページにボタンが含まれることを確認"""
        response = client.get('/')
        data = response.data.decode('utf-8')
        assert 'start-btn' in data
        assert 'reset-btn' in data
        assert '開始' in data
        assert 'リセット' in data
    
    def test_index_route_contains_stats_section(self, client):
        """トップページに統計セクションが含まれることを確認"""
        response = client.get('/')
        data = response.data.decode('utf-8')
        assert '今日の進捗' in data
        assert 'completed-count' in data
        assert 'total-time' in data
    
    def test_index_route_loads_css(self, client):
        """トップページがCSSをロードすることを確認"""
        response = client.get('/')
        data = response.data.decode('utf-8')
        assert '/static/css/style.css' in data
    
    def test_index_route_loads_js(self, client):
        """トップページがJavaScriptをロードすることを確認"""
        response = client.get('/')
        data = response.data.decode('utf-8')
        assert '/static/js/timer.js' in data
    
    def test_nonexistent_route_returns_404(self, client):
        """存在しないルートが404を返すことを確認"""
        response = client.get('/nonexistent')
        assert response.status_code == 404


class TestStaticFiles:
    """静的ファイルのテスト"""
    
    def test_css_file_exists(self, client):
        """CSSファイルが存在することを確認"""
        response = client.get('/static/css/style.css')
        assert response.status_code == 200
        assert 'text/css' in response.content_type
    
    def test_js_file_exists(self, client):
        """JavaScriptファイルが存在することを確認"""
        response = client.get('/static/js/timer.js')
        assert response.status_code == 200
        # JavaScriptのContent-Typeは環境によって異なる可能性がある
        assert response.content_type in [
            'application/javascript',
            'text/javascript',
            'application/javascript; charset=utf-8',
            'text/javascript; charset=utf-8'
        ]
    
    def test_css_contains_timer_styles(self, client):
        """CSSファイルにタイマー関連のスタイルが含まれることを確認"""
        response = client.get('/static/css/style.css')
        data = response.data.decode('utf-8')
        assert '.timer-text' in data
        assert '.btn-primary' in data
        assert '.stats-section' in data
    
    def test_js_contains_timer_class(self, client):
        """JavaScriptファイルにPomodoroTimerクラスが含まれることを確認"""
        response = client.get('/static/js/timer.js')
        data = response.data.decode('utf-8')
        assert 'PomodoroTimer' in data
        assert 'start()' in data or 'start ()' in data
        assert 'reset()' in data or 'reset ()' in data
