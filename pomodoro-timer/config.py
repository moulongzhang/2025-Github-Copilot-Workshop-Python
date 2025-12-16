"""環境別設定クラス"""


class Config:
    """基底設定"""
    POMODORO_DURATION = 25  # 分
    SHORT_BREAK_DURATION = 5  # 分
    LONG_BREAK_DURATION = 15  # 分
    SECRET_KEY = 'dev-secret-key'


class DevelopmentConfig(Config):
    """開発用設定"""
    DEBUG = True


class TestConfig(Config):
    """テスト用設定"""
    TESTING = True
    POMODORO_DURATION = 1  # テスト時は短い時間
    SHORT_BREAK_DURATION = 1
    LONG_BREAK_DURATION = 2


class ProductionConfig(Config):
    """本番用設定"""
    DEBUG = False
    SECRET_KEY = None  # 本番では環境変数から設定すること
