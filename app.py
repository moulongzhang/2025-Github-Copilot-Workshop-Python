from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import os
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))

# セッションデータの初期化
def init_session():
    if 'stats' not in session:
        session['stats'] = {
            'completed_pomodoros': 0,
            'completed_breaks': 0,
            'total_work_time': 0,  # 秒単位
            'total_break_time': 0,  # 秒単位
            'sessions_today': 0,
            'last_session_date': None
        }


@app.route('/')
def index():
    """メインページを表示"""
    init_session()
    return render_template('index.html', stats=session.get('stats', {}))


@app.route('/api/complete_pomodoro', methods=['POST'])
def complete_pomodoro():
    """ポモドーロ完了時の処理"""
    init_session()
    data = request.get_json()
    timer_type = data.get('type', 'work')
    duration = data.get('duration', 0)  # 秒単位
    
    stats = session['stats']
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 日付が変わったらセッション数をリセット
    if stats['last_session_date'] != today:
        stats['sessions_today'] = 0
        stats['last_session_date'] = today
    
    if timer_type == 'work':
        stats['completed_pomodoros'] += 1
        stats['total_work_time'] += duration
        stats['sessions_today'] += 1
    elif timer_type == 'break':
        stats['completed_breaks'] += 1
        stats['total_break_time'] += duration
    
    session['stats'] = stats
    session.modified = True
    
    return jsonify({
        'success': True,
        'stats': stats
    })


@app.route('/api/get_stats', methods=['GET'])
def get_stats():
    """統計情報を取得"""
    init_session()
    return jsonify(session.get('stats', {}))


@app.route('/api/reset_stats', methods=['POST'])
def reset_stats():
    """統計情報をリセット"""
    session['stats'] = {
        'completed_pomodoros': 0,
        'completed_breaks': 0,
        'total_work_time': 0,
        'total_break_time': 0,
        'sessions_today': 0,
        'last_session_date': None
    }
    session.modified = True
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
