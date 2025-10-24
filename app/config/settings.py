"""
アプリケーション設定管理

開発、本番、テスト環境の設定を管理します。
"""

import os
from abc import ABC, abstractmethod
from pathlib import Path


class Config(ABC):
    """設定基底クラス"""
    
    # 基本設定
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # データベース設定
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # ポモドーロタイマー設定（分単位）
    WORK_DURATION = 25
    SHORT_BREAK_DURATION = 5
    LONG_BREAK_DURATION = 15
    SESSIONS_UNTIL_LONG_BREAK = 4
    
    # アプリケーション設定
    APP_NAME = "ポモドーロタイマー"
    APP_VERSION = "1.0.0"
    
    # 静的ファイル設定
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'
    
    @staticmethod
    @abstractmethod
    def init_app(app):
        """アプリケーション初期化時の処理"""
        pass


class DevelopmentConfig(Config):
    """開発環境設定"""
    
    DEBUG = True
    TESTING = False
    
    # 開発用データベース
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + str(Path(__file__).parent.parent.parent / 'pomodoro_dev.db')
    
    # 開発用ログレベル
    LOG_LEVEL = 'DEBUG'
    
    # 開発用タイマー設定（テスト用に短縮）
    WORK_DURATION = int(os.environ.get('DEV_WORK_DURATION', 25))
    SHORT_BREAK_DURATION = int(os.environ.get('DEV_SHORT_BREAK_DURATION', 5))
    LONG_BREAK_DURATION = int(os.environ.get('DEV_LONG_BREAK_DURATION', 15))
    
    @staticmethod
    def init_app(app):
        """開発環境用初期化"""
        print("開発環境で起動しています")


class ProductionConfig(Config):
    """本番環境設定"""
    
    DEBUG = False
    TESTING = False
    
    # 本番用データベース
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + str(Path(__file__).parent.parent.parent / 'pomodoro.db')
    
    # 本番用ログレベル
    LOG_LEVEL = 'INFO'
    
    # セキュリティ設定
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    @staticmethod
    def init_app(app):
        """本番環境用初期化"""
        # 本番用ログ設定など
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(
                'logs/pomodoro.log', maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('ポモドーロタイマー 起動')


class TestConfig(Config):
    """テスト環境設定"""
    
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    
    # テスト用インメモリデータベース
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # テスト用タイマー設定（高速化）
    WORK_DURATION = 0.1  # 6秒
    SHORT_BREAK_DURATION = 0.05  # 3秒
    LONG_BREAK_DURATION = 0.08  # 4.8秒
    
    # ログレベル
    LOG_LEVEL = 'WARNING'
    
    @staticmethod
    def init_app(app):
        """テスト環境用初期化"""
        pass


# 設定辞書
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """設定を取得"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])