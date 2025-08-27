"""
JavaScriptロジックのテスト（統合テスト用）
将来的にはSelenium WebDriverやPlaywrightを使用してブラウザテストを実行
"""

class TestJavaScriptIntegration:
    """JavaScriptとの統合テスト"""

    def test_static_js_file_exists(self, client):
        """JavaScriptファイルの存在確認"""
        response = client.get('/static/js/app.js')
        assert response.status_code == 200
        assert b'PomodoroTimer' in response.data
        assert b'class PomodoroTimer' in response.data

    def test_static_css_file_exists(self, client):
        """CSSファイルの存在確認"""
        response = client.get('/static/css/style.css')
        assert response.status_code == 200
        assert b'timer-display' in response.data  # CSS内に確実に存在するクラス名を使用
        assert b'timer-display' in response.data

    def test_html_structure(self, client):
        """HTMLの基本構造テスト"""
        response = client.get('/')
        html_content = response.data.decode('utf-8')
        
        # 重要なHTML要素の存在確認
        assert 'id="timer-display"' in html_content
        assert 'id="start-btn"' in html_content
        assert 'id="pause-btn"' in html_content
        assert 'id="reset-btn"' in html_content
        assert 'id="skip-btn"' in html_content
        assert 'id="settings-panel"' in html_content
        
        # アクセシビリティ属性の確認
        assert 'aria-label' in html_content
        assert 'role=' in html_content

# 注意: 実際のブラウザでのJavaScript動作テストには別途Seleniumなどが必要
