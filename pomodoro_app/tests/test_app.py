
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import pytest
from app import app

def test_index_route():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'ポモドーロタイマー' in html
    assert '開始' in html
    assert 'リセット' in html
    assert '25:00' in html
