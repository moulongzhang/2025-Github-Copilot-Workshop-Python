"""ポモドーロタイマー アプリケーションパッケージ"""
from flask import Flask


def create_app(config_class=None):
    """
    アプリケーションファクトリ
    
    Args:
        config_class: 設定クラス（テスト時に異なる設定を注入可能）
    
    Returns:
        Flask: 設定済みのFlaskアプリケーション
    """
    app = Flask(__name__,
                static_folder='../static',
                template_folder='../templates')
    
    # 設定の読み込み
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object('config.DevelopmentConfig')
    
    # ルートの登録
    from pomodoro.routes import bp
    app.register_blueprint(bp)
    
    return app
