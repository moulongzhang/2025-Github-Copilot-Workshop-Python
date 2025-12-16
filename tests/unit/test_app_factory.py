"""
Unit tests for the Flask application factory (app/__init__.py)
"""
import os
import pytest
from flask import Flask

# Patch environment variables for test isolation
def test_create_app_default(monkeypatch):
    from app import create_app
    app = create_app()
    assert isinstance(app, Flask)
    assert app.config['SECRET_KEY']
    assert app.config['DEBUG'] is True or app.config['DEBUG'] is False
    # Test basic route
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Pomodoro Timer' in resp.data
    # Health check
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json['status'] == 'ok'


def test_create_app_with_env(monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'test-secret')
    monkeypatch.setenv('DEBUG', 'False')
    monkeypatch.setenv('FLASK_ENV', 'testing')
    from app import create_app
    app = create_app()
    assert app.config['SECRET_KEY'] == 'test-secret'
    assert app.config['DEBUG'] is False


def test_index_template_renders():
    from app import create_app
    app = create_app()
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Pomodoro Timer' in resp.data
    assert '集中力を高めて生産性を向上させましょう'.encode('utf-8') in resp.data


def test_health_endpoint():
    from app import create_app
    app = create_app()
    client = app.test_client()
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json['status'] == 'ok'
    assert 'message' in resp.json
