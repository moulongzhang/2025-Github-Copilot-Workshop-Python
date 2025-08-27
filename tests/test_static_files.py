"""
JavaScriptファイルの基本的なテスト
"""
import pytest
import os


class TestStaticFiles:
    """静的ファイルの構造テスト"""
    
    def test_javascript_file_exists(self):
        """JavaScriptファイルの存在確認"""
        js_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'static', 'js', 'timer.js'
        )
        assert os.path.exists(js_path)
    
    def test_css_file_exists(self):
        """CSSファイルの存在確認"""
        css_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'static', 'css', 'style.css'
        )
        assert os.path.exists(css_path)
    
    def test_javascript_basic_structure(self):
        """JavaScriptファイルの基本構造確認"""
        js_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'static', 'js', 'timer.js'
        )
        
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 基本的なクラス構造の確認
        assert 'class PomodoroTimer' in content
        assert 'constructor()' in content
        assert 'start()' in content
        assert 'pause()' in content  # stop()からpause()に変更
        assert 'reset()' in content
        assert 'addEventListener' in content
    
    def test_css_basic_structure(self):
        """CSSファイルの基本構造確認"""
        css_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'static', 'css', 'style.css'
        )
        
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 基本的なCSSクラスの確認
        assert '.container' in content
        assert '.timer-container' in content
        assert '.time-circle' in content
        assert '.btn' in content
        assert '@media' in content  # レスポンシブ対応


class TestTemplateStructure:
    """HTMLテンプレートの構造テスト"""
    
    def test_html_template_exists(self):
        """HTMLテンプレートファイルの存在確認"""
        template_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'templates', 'index.html'
        )
        assert os.path.exists(template_path)
    
    def test_html_template_structure(self):
        """HTMLテンプレートの基本構造確認"""
        template_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'templates', 'index.html'
        )
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # HTML構造の確認
        assert '<!DOCTYPE html>' in content
        assert '<html lang="ja">' in content
        assert '<meta charset="UTF-8">' in content
        assert '<meta name="viewport"' in content
        
        # 必要な要素の確認
        assert 'id="start-btn"' in content
        assert 'id="reset-btn"' in content  # stop-btnを削除
        assert 'class="time"' in content
        assert 'class="status"' in content
        assert 'class="counter-value"' in content
