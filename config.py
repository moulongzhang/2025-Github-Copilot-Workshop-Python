"""
ポモドーロタイマー アプリケーション設定
"""
from pathlib import Path

# アプリケーション設定
class Config:
    # 基本設定
    DEBUG = False
    TESTING = False
    SECRET_KEY = "your-secret-key-here"  # 本番環境では環境変数から取得する
    
    # タイマー設定
    WORK_DURATION = 25 * 60  # 作業時間（秒）
    SHORT_BREAK_DURATION = 5 * 60  # 短い休憩時間（秒）
    LONG_BREAK_DURATION = 15 * 60  # 長い休憩時間（秒）
    LONG_BREAK_INTERVAL = 4  # 長い休憩までのセッション数
    
    # パス設定
    BASE_DIR = Path(__file__).resolve().parent
    STATIC_DIR = BASE_DIR / "static"
    TEMPLATE_DIR = BASE_DIR / "templates"

# 開発環境設定
class DevelopmentConfig(Config):
    DEBUG = True
    
# テスト環境設定
class TestingConfig(Config):
    TESTING = True
    
# 本番環境設定
class ProductionConfig(Config):
    # 本番環境固有の設定をここに追加
    pass

# 環境の設定
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}