"""
ポモドーロタイマー Webアプリケーション
Flask + SocketIO + HTML/CSS/JavaScript で構築されたポモドーロタイマー
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import os

# Flask アプリケーションの初期化
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'pomodoro-timer-secret-key-change-in-production')

# SocketIOの初期化
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    """メインページの表示"""
    return render_template('index.html')

@app.route('/health')
def health():
    """ヘルスチェック用エンドポイント"""
    return jsonify({
        'status': 'healthy', 
        'message': 'ポモドーロタイマーアプリケーションが正常に動作しています'
    })

@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    """
    設定の取得・保存API（将来の拡張用）
    """
    if request.method == 'GET':
        # デフォルト設定を返す
        default_settings = {
            'workDuration': 25,
            'shortBreakDuration': 5,
            'longBreakDuration': 15,
            'sessionsUntilLongBreak': 4,
            'autoStartBreaks': False,
            'autoStartWork': False,
            'soundNotifications': True
        }
        return jsonify(default_settings)
    
    elif request.method == 'POST':
        # 設定の保存（現在はクライアントサイドのみ）
        settings = request.get_json()
        # 実際のアプリケーションではデータベースに保存
        return jsonify({
            'status': 'success',
            'message': '設定が保存されました'
        })

# SocketIOイベントハンドラー（将来のリアルタイム機能用）
@socketio.on('connect')
def handle_connect():
    """クライアント接続時の処理"""
    print('クライアントが接続されました')
    emit('connected', {'message': 'サーバーに正常に接続されました'})

@socketio.on('disconnect')
def handle_disconnect():
    """クライアント切断時の処理"""
    print('クライアントが切断されました')

@socketio.on('timer_state')
def handle_timer_state(data):
    """タイマー状態の同期（将来の拡張用）"""
    # 他のクライアントに状態を配信（マルチユーザー機能用）
    emit('timer_update', data, broadcast=True, include_self=False)

# エラーハンドラー
@app.errorhandler(404)
def not_found_error(error):
    """404エラーハンドラー"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500エラーハンドラー"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'サーバー内部エラーが発生しました'
    }), 500

if __name__ == '__main__':
    # 開発環境での実行
    socketio.run(app, 
                 debug=True, 
                 host='0.0.0.0', 
                 port=5000,
                 allow_unsafe_werkzeug=True)