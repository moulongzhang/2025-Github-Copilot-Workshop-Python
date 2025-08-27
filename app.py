from flask import Flask, render_template, request, jsonify
from services.timer_service import HistoryService, TimerService

app = Flask(__name__)

# サービスインスタンス
history_service = HistoryService()
timer_service = TimerService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/history', methods=['GET'])
def get_history():
    """履歴データを取得するAPI"""
    history = history_service.load_history()
    return jsonify(history)

@app.route('/api/history', methods=['POST'])
def add_history():
    """履歴データを追加するAPI"""
    try:
        data = request.json
        
        # 必要なデータの検証
        if not data or 'session_type' not in data or 'duration' not in data:
            return jsonify({'error': '必要なデータが不足しています'}), 400
        
        # 履歴エントリを追加
        history_entry = history_service.add_history_entry(
            session_type=data['session_type'],
            duration=data['duration'],
            pomodoro_count=data.get('pomodoro_count', 0)
        )
        
        if history_entry:
            return jsonify({'message': '履歴が保存されました', 'entry': history_entry}), 201
        else:
            return jsonify({'error': '履歴の保存に失敗しました'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """統計データを取得するAPI"""
    try:
        stats = history_service.get_statistics()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/validate-settings', methods=['POST'])
def validate_settings():
    """タイマー設定の検証API"""
    try:
        data = request.json
        work_minutes = data.get('work_minutes', 25)
        short_break_minutes = data.get('short_break_minutes', 5)
        long_break_minutes = data.get('long_break_minutes', 15)
        
        is_valid, errors = timer_service.validate_timer_settings(
            work_minutes, short_break_minutes, long_break_minutes
        )
        
        return jsonify({
            'valid': is_valid,
            'errors': errors
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)