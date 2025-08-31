# Flaskでルート('/')でindex.htmlを表示する基本コード


from flask import Flask, render_template, request, jsonify, g
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DATABASE = 'pomodoro.db'

# --- DBサービス層 ---
def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def init_db():
	if not os.path.exists(DATABASE):
		with sqlite3.connect(DATABASE) as conn:
			c = conn.cursor()
			c.execute('''CREATE TABLE history (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				timestamp TEXT,
				work_minutes INTEGER
			)''')
			conn.commit()

def add_history(work_minutes, timestamp=None):
	if timestamp is None:
		timestamp = datetime.now().isoformat()
	db = get_db()
	db.execute('INSERT INTO history (timestamp, work_minutes) VALUES (?, ?)', (timestamp, work_minutes))
	db.commit()
	return True

def fetch_history(limit=20):
	db = get_db()
	cur = db.execute('SELECT timestamp, work_minutes FROM history ORDER BY id DESC LIMIT ?', (limit,))
	rows = cur.fetchall()
	return [{'timestamp': r[0], 'work_minutes': r[1]} for r in rows]

# --- Flaskルーティング ---
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/api/history', methods=['POST'])
def save_history():
	data = request.get_json()
	work_minutes = data.get('work_minutes', 25)
	add_history(work_minutes)
	return jsonify({'result': 'ok'})

@app.route('/api/history', methods=['GET'])
def get_history():
	history = fetch_history()
	return jsonify(history)

if __name__ == '__main__':
	init_db()
	app.run(debug=True)
