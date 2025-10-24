
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import pytest
from flask import Flask
from app import create_app

def test_create_app():
    app = create_app()
    assert isinstance(app, Flask)

def test_index_route():
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "ポモドーロタイマー" in html
    assert "25:00" in html
    assert "開始" in html
    assert "リセット" in html
