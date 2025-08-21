import os
import re

CSS_PATH = os.path.join(os.path.dirname(__file__), 'static', 'css', 'style.css')

def test_file_exists():
    assert os.path.exists(CSS_PATH), 'style.cssが存在しません'

def test_main_container():
    with open(CSS_PATH, encoding='utf-8') as f:
        css = f.read()
    # .containerのスタイルが含まれているか
    assert re.search(r'\.container\s*{[^}]*max-width:\s*400px', css), 'メインコンテナのmax-width指定がありません'
    assert 'text-align: center' in css, 'メインコンテナのtext-align指定がありません'

def test_body_gradient():
    with open(CSS_PATH, encoding='utf-8') as f:
        css = f.read()
    assert 'background: linear-gradient' in css, 'bodyのグラデーション指定がありません'

def test_button_style():
    with open(CSS_PATH, encoding='utf-8') as f:
        css = f.read()
    assert '.btn' in css, 'ボタンスタイルがありません'
    assert 'border-radius: 50px' in css, 'ボタンの角丸指定がありません'

def test_responsive():
    with open(CSS_PATH, encoding='utf-8') as f:
        css = f.read()
    assert '@media (max-width: 768px)' in css, 'レスポンシブ対応のメディアクエリがありません'
