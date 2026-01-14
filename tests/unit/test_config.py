"""
設定クラスのユニットテスト

app/config/settings.py の各設定クラスの動作をテストします。
"""

import os
import pytest
import tempfile
from pathlib import Path

from app.config.settings import (
    Config, 
    DevelopmentConfig, 
    ProductionConfig, 
    TestConfig,
    get_config
)


class TestConfigBase:
    """基底設定クラスのテスト"""
    
    def test_basic_settings(self):
        """基本設定が正しく定義されているかテスト"""
        # ポモドーロタイマー設定
        assert Config.WORK_DURATION == 25
        assert Config.SHORT_BREAK_DURATION == 5
        assert Config.LONG_BREAK_DURATION == 15
        assert Config.SESSIONS_UNTIL_LONG_BREAK == 4
        
        # アプリケーション設定
        assert Config.APP_NAME == "ポモドーロタイマー"
        assert Config.APP_VERSION == "1.0.0"
        
        # Flask設定
        assert Config.STATIC_FOLDER == 'static'
        assert Config.TEMPLATE_FOLDER == 'templates'
        assert Config.SQLALCHEMY_TRACK_MODIFICATIONS is False
        assert Config.SQLALCHEMY_RECORD_QUERIES is True


class TestDevelopmentConfig:
    """開発環境設定のテスト"""
    
    def test_development_settings(self):
        """開発環境固有の設定をテスト"""
        assert DevelopmentConfig.DEBUG is True
        assert DevelopmentConfig.TESTING is False
        assert DevelopmentConfig.LOG_LEVEL == 'DEBUG'
    
    def test_development_database_uri(self):
        """開発環境のデータベースURI設定をテスト"""
        # 環境変数が設定されていない場合のデフォルト値
        original_env = os.environ.get('DEV_DATABASE_URL')
        if 'DEV_DATABASE_URL' in os.environ:
            del os.environ['DEV_DATABASE_URL']
        
        try:
            assert 'sqlite:///' in DevelopmentConfig.SQLALCHEMY_DATABASE_URI
            assert 'pomodoro_dev.db' in DevelopmentConfig.SQLALCHEMY_DATABASE_URI
        finally:
            if original_env:
                os.environ['DEV_DATABASE_URL'] = original_env
    
    def test_development_timer_settings_from_env(self):
        """環境変数からのタイマー設定をテスト"""
        original_work = os.environ.get('DEV_WORK_DURATION')
        original_short = os.environ.get('DEV_SHORT_BREAK_DURATION')
        original_long = os.environ.get('DEV_LONG_BREAK_DURATION')
        
        try:
            os.environ['DEV_WORK_DURATION'] = '30'
            os.environ['DEV_SHORT_BREAK_DURATION'] = '10'
            os.environ['DEV_LONG_BREAK_DURATION'] = '20'
            
            # クラスを再インポートして環境変数を反映
            import importlib
            import app.config.settings
            importlib.reload(app.config.settings)
            from app.config.settings import DevelopmentConfig
            
            assert DevelopmentConfig.WORK_DURATION == 30
            assert DevelopmentConfig.SHORT_BREAK_DURATION == 10
            assert DevelopmentConfig.LONG_BREAK_DURATION == 20
            
        finally:
            # 環境変数を元に戻す
            for key, value in [
                ('DEV_WORK_DURATION', original_work),
                ('DEV_SHORT_BREAK_DURATION', original_short),
                ('DEV_LONG_BREAK_DURATION', original_long)
            ]:
                if value is not None:
                    os.environ[key] = value
                elif key in os.environ:
                    del os.environ[key]
            
            # モジュールをリロード
            importlib.reload(app.config.settings)


class TestProductionConfig:
    """本番環境設定のテスト"""
    
    def test_production_settings(self):
        """本番環境固有の設定をテスト"""
        assert ProductionConfig.DEBUG is False
        assert ProductionConfig.TESTING is False
        assert ProductionConfig.LOG_LEVEL == 'INFO'
        
        # セキュリティ設定
        assert ProductionConfig.SESSION_COOKIE_SECURE is True
        assert ProductionConfig.SESSION_COOKIE_HTTPONLY is True
        assert ProductionConfig.SESSION_COOKIE_SAMESITE == 'Lax'
    
    def test_production_database_uri(self):
        """本番環境のデータベースURI設定をテスト"""
        # 環境変数が設定されていない場合のデフォルト値
        original_env = os.environ.get('DATABASE_URL')
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
        
        try:
            assert 'sqlite:///' in ProductionConfig.SQLALCHEMY_DATABASE_URI
            assert 'pomodoro.db' in ProductionConfig.SQLALCHEMY_DATABASE_URI
        finally:
            if original_env:
                os.environ['DATABASE_URL'] = original_env


class TestTestConfig:
    """テスト環境設定のテスト"""
    
    def test_test_settings(self):
        """テスト環境固有の設定をテスト"""
        assert TestConfig.DEBUG is True
        assert TestConfig.TESTING is True
        assert TestConfig.WTF_CSRF_ENABLED is False
        assert TestConfig.LOG_LEVEL == 'WARNING'
    
    def test_test_database_uri(self):
        """テスト環境のデータベースURI設定をテスト"""
        assert TestConfig.SQLALCHEMY_DATABASE_URI == 'sqlite:///:memory:'
    
    def test_test_timer_settings(self):
        """テスト環境のタイマー設定（高速化）をテスト"""
        assert TestConfig.WORK_DURATION == 0.1  # 6秒
        assert TestConfig.SHORT_BREAK_DURATION == 0.05  # 3秒
        assert TestConfig.LONG_BREAK_DURATION == 0.08  # 4.8秒


class TestGetConfig:
    """get_config関数のテスト"""
    
    def test_get_config_development(self):
        """開発環境設定の取得をテスト"""
        config = get_config('development')
        assert config.__name__ == 'DevelopmentConfig'
        assert config.DEBUG is True
    
    def test_get_config_production(self):
        """本番環境設定の取得をテスト"""
        config = get_config('production')
        assert config.__name__ == 'ProductionConfig'
        assert config.DEBUG is False
    
    def test_get_config_testing(self):
        """テスト環境設定の取得をテスト"""
        config = get_config('testing')
        assert config.__name__ == 'TestConfig'
        assert config.TESTING is True
    
    def test_get_config_default(self):
        """デフォルト設定の取得をテスト"""
        config = get_config('default')
        assert config.__name__ == 'DevelopmentConfig'
        
        config = get_config(None)
        assert config.__name__ == 'DevelopmentConfig'
    
    def test_get_config_unknown(self):
        """不明な設定名の場合はデフォルトを返すテスト"""
        config = get_config('unknown')
        assert config.__name__ == 'DevelopmentConfig'
    
    def test_get_config_from_env(self):
        """環境変数からの設定取得をテスト"""
        original_env = os.environ.get('FLASK_ENV')
        
        try:
            os.environ['FLASK_ENV'] = 'production'
            config = get_config()
            assert config.__name__ == 'ProductionConfig'
            
            os.environ['FLASK_ENV'] = 'testing'
            config = get_config()
            assert config.__name__ == 'TestConfig'
            
        finally:
            if original_env:
                os.environ['FLASK_ENV'] = original_env
            elif 'FLASK_ENV' in os.environ:
                del os.environ['FLASK_ENV']


class TestConfigInitialization:
    """設定クラスの初期化メソッドのテスト"""
    
    def test_development_init_app(self, capsys):
        """開発環境の初期化処理をテスト"""
        from unittest.mock import Mock
        
        app = Mock()
        DevelopmentConfig.init_app(app)
        
        # 標準出力に開発環境メッセージが出力されることを確認
        captured = capsys.readouterr()
        assert "開発環境で起動しています" in captured.out
    
    def test_test_init_app(self):
        """テスト環境の初期化処理をテスト（何もしない）"""
        from unittest.mock import Mock
        
        app = Mock()
        # 例外が発生しないことを確認
        TestConfig.init_app(app)
    
    @pytest.mark.slow
    def test_production_init_app_logging(self, tmp_path):
        """本番環境の初期化処理（ログ設定）をテスト"""
        from unittest.mock import Mock
        import tempfile
        import os
        
        # 一時ディレクトリでテスト
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            
            app = Mock()
            app.debug = False
            app.testing = False
            app.logger = Mock()
            
            ProductionConfig.init_app(app)
            
            # ログディレクトリが作成されることを確認
            assert (tmp_path / 'logs').exists()
            
            # ログハンドラーが追加されることを確認
            assert app.logger.addHandler.called
            assert app.logger.setLevel.called
            assert app.logger.info.called
            
        finally:
            os.chdir(original_cwd)