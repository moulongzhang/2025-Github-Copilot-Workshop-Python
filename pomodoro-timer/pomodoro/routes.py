"""ルーティング定義"""
from flask import Blueprint, render_template, jsonify, request

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """メインページを表示"""
    return render_template('index.html')


@bp.route('/api/settings', methods=['GET'])
def get_settings():
    """タイマー設定を取得"""
    from flask import current_app
    settings = {
        'pomodoro': current_app.config.get('POMODORO_DURATION', 25),
        'shortBreak': current_app.config.get('SHORT_BREAK_DURATION', 5),
        'longBreak': current_app.config.get('LONG_BREAK_DURATION', 15)
    }
    return jsonify(settings)


@bp.route('/api/settings', methods=['POST'])
def save_settings():
    """タイマー設定を保存（将来的な拡張用）"""
    data = request.get_json()
    # 現時点ではクライアント側でlocalStorageに保存するため、
    # 受け取ったデータを確認してOKを返すのみ
    return jsonify({'status': 'ok', 'received': data})
