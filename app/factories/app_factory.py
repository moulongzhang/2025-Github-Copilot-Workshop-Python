"""
アプリケーションファクトリー

Flaskアプリケーションの生成とセットアップを行います。
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS

from app.config.settings import get_config

# グローバル拡張オブジェクト
db = SQLAlchemy()
socketio = SocketIO()
cors = CORS()


def create_app(config_name=None):
    """
    Flaskアプリケーションを作成
    
    Args:
        config_name (str): 設定名 ('development', 'production', 'testing')
        
    Returns:
        Flask: 設定済みFlaskアプリケーション
    """
    app = Flask(__name__, 
                static_folder='../static',
                template_folder='../templates')
    
    # 設定を読み込み
    config = get_config(config_name)
    app.config.from_object(config)
    
    # 設定クラスの初期化処理を実行
    config.init_app(app)
    
    # 拡張機能を初期化
    init_extensions(app)
    
    # ルートを登録
    register_routes(app)
    
    # エラーハンドラーを登録
    register_error_handlers(app)
    
    return app


def init_extensions(app):
    """拡張機能を初期化"""
    
    # データベース
    db.init_app(app)
    
    # WebSocket
    socketio.init_app(app, 
                     cors_allowed_origins="*",
                     async_mode='threading')
    
    # CORS
    cors.init_app(app)
    
    # アプリケーションコンテキスト内でテーブル作成
    with app.app_context():
        db.create_all()


def register_routes(app):
    """ルートを登録"""
    
    # メインページルート
    @app.route('/')
    def index():
        return "ポモドーロタイマー - Phase 1 基盤完成"
    
    # ヘルスチェック
    @app.route('/health')
    def health():
        return {"status": "ok", "version": app.config.get('APP_VERSION')}
    
    # 将来的にここで他のルートを登録
    # from app.routes import api, websocket
    # app.register_blueprint(api.bp)
    # socketio.on_namespace(websocket.TimerNamespace('/timer'))


def register_error_handlers(app):
    """エラーハンドラーを登録"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Not Found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal Server Error"}, 500


def create_test_app():
    """テスト用アプリケーションを作成"""
    return create_app('testing')


def create_production_app():
    """本番用アプリケーションを作成"""
    return create_app('production')