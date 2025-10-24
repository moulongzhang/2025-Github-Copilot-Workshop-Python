#!/usr/bin/env python3
"""
ポモドーロタイマー Webアプリケーション

メインエントリーポイント
"""

import os
from app.factories.app_factory import create_app, socketio


def main():
    """アプリケーションを起動"""
    
    # 環境変数から設定を取得
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # アプリケーションを作成
    app = create_app(config_name)
    
    # デバッグ情報を表示
    if app.config['DEBUG']:
        print(f"🍅 {app.config['APP_NAME']} v{app.config['APP_VERSION']}")
        print(f"📝 環境: {config_name}")
        print(f"🗄️ データベース: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"⏰ 作業時間: {app.config['WORK_DURATION']}分")
        print("🚀 アプリケーション起動中...")
    
    # サーバーを起動
    socketio.run(
        app,
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )


if __name__ == '__main__':
    main()