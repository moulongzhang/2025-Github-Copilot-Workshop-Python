# ポモドーロタイマーアプリケーション 段階的実装計画

## 概要
このドキュメントは、ポモドーロタイマーWebアプリケーションを段階的に実装するための詳細な計画です。
各ステップは独立して動作確認可能で、テストとレビューを挟みながら進められるように設計されています。

---

## 実装フェーズ概要

```
Phase 1: 基本タイマー機能（フロントエンド）           → 2-3時間
Phase 2: Flask基盤とシンプルなAPI                   → 2-3時間
Phase 3: データモデルとサービス層                    → 2-3時間
Phase 4: データ永続化とリポジトリ層                  → 2-3時間
Phase 5: 統計機能の実装                             → 2-3時間
Phase 6: UI/UXの改善とアニメーション                 → 3-4時間
Phase 7: テストコード整備                           → 3-4時間
```

**総見積もり時間:** 約16-23時間（初学者の場合は1.5倍程度）

---

## Phase 1: 基本タイマー機能（フロントエンド）

**目標:** ブラウザ上で動作する最小限のタイマーを実装

### Step 1.1: HTMLの基本構造作成
**ファイル:** `templates/index.html`

**実装内容:**
- [ ] HTML5基本テンプレート作成
- [ ] タイトル「ポモドーロタイマー」
- [ ] タイマー表示エリア（25:00）
- [ ] 開始ボタン
- [ ] リセットボタン

**確認方法:**
```bash
# 静的HTMLとしてブラウザで開く
open templates/index.html
```

**成功基準:**
- レイアウトが中央に配置されている
- ボタンが表示されている
- テキストが読みやすい

---

### Step 1.2: 基本CSSスタイリング
**ファイル:** `static/css/style.css`

**実装内容:**
- [ ] リセットCSS（margin, padding）
- [ ] 中央配置レイアウト（Flexbox）
- [ ] フォント設定（読みやすいサイズ）
- [ ] ボタンスタイル
  - 開始ボタン: 背景色あり
  - リセットボタン: ボーダーのみ
- [ ] カラースキーム（紫系）

**確認方法:**
```bash
# HTMLをブラウザで開いて確認
open templates/index.html
```

**成功基準:**
- 見た目が整っている
- ボタンがクリック可能に見える
- カラースキームが適用されている

---

### Step 1.3: JavaScriptタイマーロジック実装
**ファイル:** `static/js/timer.js`

**実装内容:**
- [ ] タイマークラス作成
  ```javascript
  class PomodoroTimer {
    constructor(duration = 25) {
      this.duration = duration * 60; // 秒に変換
      this.remainingTime = this.duration;
      this.intervalId = null;
    }
    
    start() { /* ... */ }
    reset() { /* ... */ }
    formatTime(seconds) { /* ... */ }
  }
  ```
- [ ] カウントダウンロジック（setInterval使用）
- [ ] MM:SS形式のフォーマット関数
- [ ] DOM更新処理

**確認方法:**
```javascript
// ブラウザのコンソールでテスト
const timer = new PomodoroTimer(1); // 1分でテスト
timer.start();
```

**成功基準:**
- タイマーが1秒ごとに減る
- 00:00まで正確にカウントダウン
- 開始ボタンで開始、リセットボタンでリセット

---

### Step 1.4: イベントハンドラ接続
**ファイル:** `static/js/timer.js`

**実装内容:**
- [ ] DOMContentLoadedイベントリスナー
- [ ] 開始ボタンのクリックイベント
- [ ] リセットボタンのクリックイベント
- [ ] タイマー表示の更新

**確認方法:**
```bash
# HTMLをブラウザで開いて操作
open templates/index.html
```

**成功基準:**
- 開始ボタンでタイマーが動く
- リセットボタンで25:00に戻る
- 複数回の開始/リセットが正常動作

---

### ✅ Phase 1 完了チェックリスト
- [ ] タイマーが25:00から00:00までカウントダウン
- [ ] 開始ボタンでタイマー開始
- [ ] リセットボタンで25:00に戻る
- [ ] UIが見やすく、操作しやすい
- [ ] ブラウザのコンソールにエラーがない

**デモ:** Phase 1完了時点で、完全にフロントエンドのみで動作するタイマーが完成

---

## Phase 2: Flask基盤とシンプルなAPI

**目標:** Flaskアプリを起動し、HTMLを配信できるようにする

### Step 2.1: プロジェクト構造セットアップ
**実装内容:**
- [ ] `requirements.txt` 作成
  ```txt
  Flask==3.0.0
  python-dotenv==1.0.0
  ```
- [ ] ディレクトリ作成
  ```bash
  mkdir -p src/{models,repositories,services,controllers,utils}
  mkdir -p tests/{unit,integration,fixtures}
  mkdir -p data
  touch src/__init__.py
  ```

**確認方法:**
```bash
pip install -r requirements.txt
```

**成功基準:**
- 依存パッケージがインストールされる
- ディレクトリ構造が正しい

---

### Step 2.2: 最小限のFlaskアプリ作成
**ファイル:** `app.py`

**実装内容:**
- [ ] Flaskアプリ初期化
- [ ] ルートエンドポイント `/` でindex.html表示
- [ ] 静的ファイル配信設定

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**確認方法:**
```bash
python app.py
# ブラウザで http://localhost:5000 にアクセス
```

**成功基準:**
- Flaskサーバーが起動
- ブラウザでタイマーが表示される
- Phase 1のタイマー機能が動作

---

### Step 2.3: シンプルなヘルスチェックAPI
**ファイル:** `app.py`

**実装内容:**
- [ ] `/api/health` エンドポイント追加
- [ ] JSONレスポンス返却

```python
@app.route('/api/health')
def health_check():
    return {'status': 'ok', 'message': 'Pomodoro Timer API is running'}
```

**確認方法:**
```bash
curl http://localhost:5000/api/health
# または
# ブラウザで http://localhost:5000/api/health にアクセス
```

**成功基準:**
- JSONレスポンスが返る
- ステータスコード200

---

### ✅ Phase 2 完了チェックリスト
- [ ] Flaskサーバーが正常起動
- [ ] ブラウザでタイマーUIが表示される
- [ ] `/api/health` が正常応答
- [ ] 静的ファイル（CSS/JS）が正しく読み込まれる

---

## Phase 3: データモデルとサービス層

**目標:** ビジネスロジックを実装し、テスト可能な設計にする

### Step 3.1: データモデル定義
**ファイル:** `src/models/session.py`

**実装内容:**
- [ ] PomodoroSessionクラス作成（dataclass使用）
- [ ] フィールド定義
  - `session_id`: str
  - `start_time`: datetime
  - `end_time`: Optional[datetime]
  - `duration`: int（分）
  - `completed`: bool

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class PomodoroSession:
    start_time: datetime
    duration: int = 25
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    end_time: Optional[datetime] = None
    completed: bool = False
    
    def complete(self) -> None:
        """セッションを完了する"""
        self.end_time = datetime.now()
        self.completed = True
    
    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return {
            'session_id': self.session_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'completed': self.completed
        }
```

**確認方法:**
```python
# Pythonインタープリタで確認
from src.models.session import PomodoroSession
from datetime import datetime

session = PomodoroSession(start_time=datetime.now())
print(session)
session.complete()
print(session.to_dict())
```

**成功基準:**
- セッションオブジェクトが作成できる
- `complete()` メソッドで完了できる
- `to_dict()` で辞書に変換できる

---

### Step 3.2: タイマーサービス実装
**ファイル:** `src/services/timer_service.py`

**実装内容:**
- [ ] TimerServiceクラス作成
- [ ] セッション開始メソッド
- [ ] セッション完了メソッド
- [ ] 統計計算メソッド

```python
from datetime import datetime, date
from typing import List, Dict
from src.models.session import PomodoroSession

class TimerService:
    def __init__(self):
        self.sessions: List[PomodoroSession] = []
    
    def start_session(self, duration: int = 25) -> PomodoroSession:
        """新しいポモドーロセッションを開始"""
        session = PomodoroSession(
            start_time=datetime.now(),
            duration=duration
        )
        self.sessions.append(session)
        return session
    
    def complete_session(self, session_id: str) -> bool:
        """セッションを完了"""
        for session in self.sessions:
            if session.session_id == session_id:
                session.complete()
                return True
        return False
    
    def get_today_stats(self) -> Dict:
        """今日の統計を取得"""
        today = date.today()
        today_sessions = [
            s for s in self.sessions 
            if s.start_time.date() == today and s.completed
        ]
        
        total_completed = len(today_sessions)
        total_minutes = sum(s.duration for s in today_sessions)
        
        return {
            'total_completed': total_completed,
            'total_minutes': total_minutes,
            'hours': total_minutes // 60,
            'minutes': total_minutes % 60
        }
```

**確認方法:**
```python
from src.services.timer_service import TimerService

service = TimerService()
session = service.start_session()
print(f"Session started: {session.session_id}")

service.complete_session(session.session_id)
stats = service.get_today_stats()
print(f"Stats: {stats}")
```

**成功基準:**
- セッションが開始できる
- セッションが完了できる
- 統計が正しく計算される

---

### Step 3.3: ユーティリティ関数
**ファイル:** `src/utils/datetime_helper.py`

**実装内容:**
- [ ] 日付フォーマット関数
- [ ] 時間差計算関数

```python
from datetime import datetime, date

def format_duration(minutes: int) -> str:
    """分を「X時間Y分」形式に変換"""
    hours = minutes // 60
    mins = minutes % 60
    
    if hours > 0:
        return f"{hours}時間{mins}分"
    else:
        return f"{mins}分"

def get_today_string() -> str:
    """今日の日付を文字列で返す"""
    return date.today().isoformat()

def is_today(dt: datetime) -> bool:
    """指定のdatetimeが今日かどうか判定"""
    return dt.date() == date.today()
```

**確認方法:**
```python
from src.utils.datetime_helper import format_duration

print(format_duration(100))  # "1時間40分"
print(format_duration(25))   # "25分"
```

**成功基準:**
- format_durationが正しく動作
- テストケースが通る

---

### ✅ Phase 3 完了チェックリスト
- [ ] PomodoroSessionモデルが動作
- [ ] TimerServiceが正しく統計計算
- [ ] ユーティリティ関数が動作
- [ ] Pythonインタープリタで手動テスト完了

---

## Phase 4: データ永続化とリポジトリ層

**目標:** セッションデータをJSONファイルに保存・読み込み

### Step 4.1: リポジトリ抽象基底クラス
**ファイル:** `src/repositories/base.py`

**実装内容:**
- [ ] SessionRepository抽象クラス作成
- [ ] インターフェース定義

```python
from abc import ABC, abstractmethod
from typing import List
from datetime import date
from src.models.session import PomodoroSession

class SessionRepository(ABC):
    @abstractmethod
    def save(self, session: PomodoroSession) -> None:
        """セッションを保存"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[PomodoroSession]:
        """全セッションを取得"""
        pass
    
    @abstractmethod
    def get_by_date(self, target_date: date) -> List[PomodoroSession]:
        """指定日のセッションを取得"""
        pass
    
    @abstractmethod
    def get_today_sessions(self) -> List[PomodoroSession]:
        """今日のセッションを取得"""
        pass
```

---

### Step 4.2: JSON永続化実装
**ファイル:** `src/repositories/session_repository.py`

**実装内容:**
- [ ] JsonSessionRepository実装
- [ ] JSON読み込み・書き込み
- [ ] エラーハンドリング

```python
import json
from pathlib import Path
from typing import List
from datetime import datetime, date
from src.models.session import PomodoroSession
from src.repositories.base import SessionRepository

class JsonSessionRepository(SessionRepository):
    def __init__(self, file_path: str = 'data/sessions.json'):
        self.file_path = Path(file_path)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """ファイルが存在しない場合は作成"""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text('[]')
    
    def save(self, session: PomodoroSession) -> None:
        """セッションを保存"""
        sessions = self.get_all()
        sessions.append(session)
        self._write_sessions(sessions)
    
    def get_all(self) -> List[PomodoroSession]:
        """全セッションを取得"""
        data = json.loads(self.file_path.read_text())
        return [self._dict_to_session(s) for s in data]
    
    def get_by_date(self, target_date: date) -> List[PomodoroSession]:
        """指定日のセッションを取得"""
        all_sessions = self.get_all()
        return [
            s for s in all_sessions 
            if s.start_time.date() == target_date
        ]
    
    def get_today_sessions(self) -> List[PomodoroSession]:
        """今日のセッションを取得"""
        return self.get_by_date(date.today())
    
    def _write_sessions(self, sessions: List[PomodoroSession]) -> None:
        """セッション一覧をファイルに書き込み"""
        data = [s.to_dict() for s in sessions]
        self.file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    
    def _dict_to_session(self, data: dict) -> PomodoroSession:
        """辞書からセッションオブジェクトに変換"""
        return PomodoroSession(
            session_id=data['session_id'],
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']) if data['end_time'] else None,
            duration=data['duration'],
            completed=data['completed']
        )
```

**確認方法:**
```python
from src.repositories.session_repository import JsonSessionRepository
from src.models.session import PomodoroSession
from datetime import datetime

repo = JsonSessionRepository('data/test_sessions.json')
session = PomodoroSession(start_time=datetime.now())
session.complete()

repo.save(session)
loaded = repo.get_all()
print(f"Loaded {len(loaded)} sessions")
```

**成功基準:**
- JSONファイルが作成される
- セッションが保存される
- 保存したセッションが読み込める

---

### Step 4.3: サービス層とリポジトリ層の統合
**ファイル:** `src/services/timer_service.py`（更新）

**実装内容:**
- [ ] TimerServiceにリポジトリを注入
- [ ] セッション完了時に永続化

```python
class TimerService:
    def __init__(self, repository: SessionRepository):
        self.repository = repository
    
    def start_session(self, duration: int = 25) -> PomodoroSession:
        session = PomodoroSession(
            start_time=datetime.now(),
            duration=duration
        )
        return session
    
    def complete_session(self, session: PomodoroSession) -> None:
        """セッションを完了して保存"""
        session.complete()
        self.repository.save(session)
    
    def get_today_stats(self) -> Dict:
        """今日の統計を取得（リポジトリから）"""
        today_sessions = self.repository.get_today_sessions()
        completed = [s for s in today_sessions if s.completed]
        
        total_completed = len(completed)
        total_minutes = sum(s.duration for s in completed)
        
        return {
            'total_completed': total_completed,
            'total_minutes': total_minutes,
            'hours': total_minutes // 60,
            'minutes': total_minutes % 60
        }
```

**確認方法:**
```python
from src.services.timer_service import TimerService
from src.repositories.session_repository import JsonSessionRepository

repo = JsonSessionRepository()
service = TimerService(repository=repo)

session = service.start_session()
service.complete_session(session)

stats = service.get_today_stats()
print(stats)
```

**成功基準:**
- セッション完了後、JSONファイルに保存される
- 統計がリポジトリから取得できる

---

### ✅ Phase 4 完了チェックリスト
- [ ] JSONファイルにデータが保存される
- [ ] アプリ再起動後もデータが残る
- [ ] 統計が正しく計算される
- [ ] `data/sessions.json` が確認できる

---

## Phase 5: 統計機能とAPI実装

**目標:** フロントエンドとバックエンドを接続し、統計を表示

### Step 5.1: API Blueprintとコントローラ作成
**ファイル:** `src/controllers/api_controller.py`

**実装内容:**
- [ ] Flask Blueprint作成
- [ ] セッション開始API
- [ ] セッション完了API
- [ ] 統計取得API

```python
from flask import Blueprint, jsonify, request
from src.services.timer_service import TimerService

def create_api_blueprint(timer_service: TimerService) -> Blueprint:
    api = Blueprint('api', __name__, url_prefix='/api')
    
    # セッション管理用（一時的にメモリに保持）
    active_sessions = {}
    
    @api.route('/session/start', methods=['POST'])
    def start_session():
        """セッションを開始"""
        data = request.get_json() or {}
        duration = data.get('duration', 25)
        
        session = timer_service.start_session(duration)
        active_sessions[session.session_id] = session
        
        return jsonify({
            'success': True,
            'session_id': session.session_id,
            'duration': session.duration
        })
    
    @api.route('/session/complete', methods=['POST'])
    def complete_session():
        """セッションを完了"""
        data = request.get_json()
        session_id = data.get('session_id')
        
        if session_id in active_sessions:
            session = active_sessions[session_id]
            timer_service.complete_session(session)
            del active_sessions[session_id]
            
            return jsonify({
                'success': True,
                'message': 'Session completed'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Session not found'
            }), 404
    
    @api.route('/stats/today', methods=['GET'])
    def get_today_stats():
        """今日の統計を取得"""
        stats = timer_service.get_today_stats()
        return jsonify(stats)
    
    return api
```

---

### Step 5.2: app.pyの更新
**ファイル:** `app.py`

**実装内容:**
- [ ] サービスとリポジトリの初期化
- [ ] Blueprint登録

```python
from flask import Flask, render_template
from src.repositories.session_repository import JsonSessionRepository
from src.services.timer_service import TimerService
from src.controllers.api_controller import create_api_blueprint

def create_app():
    app = Flask(__name__)
    
    # 依存性注入
    repository = JsonSessionRepository()
    timer_service = TimerService(repository=repository)
    
    # Blueprint登録
    api_blueprint = create_api_blueprint(timer_service)
    app.register_blueprint(api_blueprint)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**確認方法:**
```bash
# サーバー起動
python app.py

# 別ターミナルでAPIテスト
curl -X POST http://localhost:5000/api/session/start

curl -X POST http://localhost:5000/api/session/complete \
  -H "Content-Type: application/json" \
  -d '{"session_id": "セッションID"}'

curl http://localhost:5000/api/stats/today
```

**成功基準:**
- すべてのAPIエンドポイントが応答
- セッション完了後、JSONファイルに保存される
- 統計APIが正しいデータを返す

---

### Step 5.3: フロントエンドのAPI統合
**ファイル:** `static/js/timer.js`（更新）

**実装内容:**
- [ ] セッション開始時にAPI呼び出し
- [ ] タイマー完了時にAPI呼び出し
- [ ] 統計取得とUI更新

```javascript
class PomodoroTimer {
    constructor(duration = 25) {
        this.duration = duration * 60;
        this.remainingTime = this.duration;
        this.intervalId = null;
        this.sessionId = null;
    }
    
    async start() {
        if (this.intervalId) return;
        
        // APIでセッション開始
        const response = await fetch('/api/session/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ duration: this.duration / 60 })
        });
        const data = await response.json();
        this.sessionId = data.session_id;
        
        // タイマー開始
        this.intervalId = setInterval(() => {
            this.remainingTime--;
            this.updateDisplay();
            
            if (this.remainingTime <= 0) {
                this.complete();
            }
        }, 1000);
    }
    
    async complete() {
        clearInterval(this.intervalId);
        this.intervalId = null;
        
        // APIでセッション完了
        if (this.sessionId) {
            await fetch('/api/session/complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId })
            });
            
            // 統計を更新
            await this.updateStats();
        }
        
        this.reset();
    }
    
    async updateStats() {
        const response = await fetch('/api/stats/today');
        const stats = await response.json();
        
        document.getElementById('completed-count').textContent = stats.total_completed;
        document.getElementById('total-time').textContent = 
            `${stats.hours}時間${stats.minutes}分`;
    }
    
    // ... 他のメソッド
}

// ページ読み込み時に統計を取得
document.addEventListener('DOMContentLoaded', async () => {
    const timer = new PomodoroTimer(25);
    await timer.updateStats();
    
    // ボタンイベント設定
    // ...
});
```

---

### Step 5.4: HTMLの統計表示エリア追加
**ファイル:** `templates/index.html`（更新）

**実装内容:**
- [ ] 統計表示セクション追加

```html
<div class="stats-section">
    <h3>今日の進捗</h3>
    <div class="stats-grid">
        <div class="stat-item">
            <span id="completed-count" class="stat-value">0</span>
            <span class="stat-label">完了</span>
        </div>
        <div class="stat-item">
            <span id="total-time" class="stat-value">0時間0分</span>
            <span class="stat-label">集中時間</span>
        </div>
    </div>
</div>
```

**確認方法:**
1. ブラウザで http://localhost:5000 にアクセス
2. タイマーを25分（テストは1分で）スタート
3. 完了後、統計が更新されることを確認

**成功基準:**
- タイマー完了後、統計が自動更新される
- ページリロード後も統計が表示される
- JSONファイルにデータが保存されている

---

### ✅ Phase 5 完了チェックリスト
- [ ] APIがフロントエンドから呼び出せる
- [ ] セッション完了時に統計が更新される
- [ ] JSONファイルにデータが永続化
- [ ] ページリロード後も統計が表示される
- [ ] 複数セッション完了で統計が正しく累積

---

## Phase 6: UI/UXの改善とアニメーション

**目標:** 画像のような美しいUIを実装

### Step 6.1: 円形プログレスバーのSVG実装
**ファイル:** `templates/index.html`（更新）

**実装内容:**
- [ ] SVG円形プログレスバー追加

```html
<div class="timer-container">
    <svg class="progress-ring" width="280" height="280">
        <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
            </linearGradient>
        </defs>
        <!-- 背景の円 -->
        <circle
            class="progress-ring__background"
            stroke="#e0e0e0"
            stroke-width="20"
            fill="transparent"
            r="120"
            cx="140"
            cy="140"
        />
        <!-- 進捗の円 -->
        <circle
            class="progress-ring__circle"
            stroke="url(#gradient)"
            stroke-width="20"
            fill="transparent"
            r="120"
            cx="140"
            cy="140"
            stroke-dasharray="753.98"
            stroke-dashoffset="753.98"
        />
    </svg>
    <div class="timer-display">
        <div class="timer-status">作業中</div>
        <div id="timer-text" class="timer-text">25:00</div>
    </div>
</div>
```

---

### Step 6.2: プログレスバーのアニメーション
**ファイル:** `static/css/style.css`

**実装内容:**
- [ ] CSSアニメーション設定

```css
.progress-ring {
    transform: rotate(-90deg); /* 12時の位置から開始 */
}

.progress-ring__circle {
    transition: stroke-dashoffset 1s linear;
}

.timer-container {
    position: relative;
    width: 280px;
    height: 280px;
}

.timer-display {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}

.timer-text {
    font-size: 48px;
    font-weight: bold;
    color: #333;
}

.timer-status {
    font-size: 14px;
    color: #666;
    margin-bottom: 10px;
}
```

**ファイル:** `static/js/timer.js`（更新）

```javascript
class PomodoroTimer {
    updateDisplay() {
        // 時間表示
        const minutes = Math.floor(this.remainingTime / 60);
        const seconds = this.remainingTime % 60;
        const timeText = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        document.getElementById('timer-text').textContent = timeText;
        
        // プログレスバー更新
        const progress = (this.duration - this.remainingTime) / this.duration;
        const circumference = 2 * Math.PI * 120; // r=120
        const offset = circumference * (1 - progress);
        
        const circle = document.querySelector('.progress-ring__circle');
        circle.style.strokeDashoffset = offset;
    }
}
```

**確認方法:**
- タイマーを開始して、円形プログレスバーが滑らかにアニメーションすることを確認

**成功基準:**
- プログレスバーが0%から100%に進む
- グラデーションが適用されている
- アニメーションが滑らか

---

### Step 6.3: ボタンスタイルと統計セクションのデザイン
**ファイル:** `static/css/style.css`

**実装内容:**
- [ ] ボタンのホバーエフェクト
- [ ] 統計セクションの背景色
- [ ] 全体のレイアウト調整

```css
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 20px;
}

.app-container {
    background: white;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    max-width: 450px;
    width: 100%;
}

.app-title {
    text-align: center;
    font-size: 24px;
    margin-bottom: 30px;
    color: #333;
}

.button-group {
    display: flex;
    gap: 15px;
    justify-content: center;
    margin: 30px 0;
}

.btn {
    padding: 12px 30px;
    font-size: 16px;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
    background: transparent;
    color: #667eea;
    border: 2px solid #667eea;
}

.btn-secondary:hover {
    background: #f0f4ff;
}

.stats-section {
    background: #f5f7fa;
    border-radius: 15px;
    padding: 20px;
    margin-top: 30px;
}

.stats-section h3 {
    margin: 0 0 15px 0;
    font-size: 16px;
    color: #666;
}

.stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.stat-item {
    text-align: center;
}

.stat-value {
    display: block;
    font-size: 32px;
    font-weight: bold;
    color: #667eea;
    margin-bottom: 5px;
}

.stat-label {
    font-size: 14px;
    color: #666;
}
```

**確認方法:**
- ブラウザで確認し、添付画像と比較

**成功基準:**
- デザインが画像に近い
- ホバー時のアニメーションが滑らか
- レスポンシブ対応

---

### Step 6.4: レスポンシブデザイン
**ファイル:** `static/css/style.css`（追加）

**実装内容:**
- [ ] モバイル対応

```css
@media (max-width: 600px) {
    .app-container {
        padding: 20px;
    }
    
    .timer-container {
        width: 220px;
        height: 220px;
    }
    
    .timer-text {
        font-size: 36px;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
}
```

---

### ✅ Phase 6 完了チェックリスト
- [ ] 円形プログレスバーが動作
- [ ] グラデーションが適用
- [ ] ボタンにホバーエフェクト
- [ ] 統計セクションのデザインが完成
- [ ] モバイルでも正常表示

---

## Phase 7: テストコード整備

**目標:** 自動テストを実装し、品質を保証

### Step 7.1: テスト環境セットアップ
**ファイル:** `requirements.txt`（更新）

```txt
Flask==3.0.0
python-dotenv==1.0.0

# テスト関連
pytest==7.4.0
pytest-cov==4.1.0
pytest-mock==3.12.0
freezegun==1.4.0
```

**確認方法:**
```bash
pip install -r requirements.txt
```

---

### Step 7.2: モデルのユニットテスト
**ファイル:** `tests/unit/test_models.py`

**実装内容:**
```python
import pytest
from datetime import datetime
from src.models.session import PomodoroSession

def test_create_session():
    """セッションが正しく作成できる"""
    start_time = datetime(2025, 12, 16, 10, 0, 0)
    session = PomodoroSession(start_time=start_time, duration=25)
    
    assert session.duration == 25
    assert session.start_time == start_time
    assert not session.completed
    assert session.end_time is None

def test_complete_session():
    """セッションが正しく完了する"""
    session = PomodoroSession(start_time=datetime.now())
    session.complete()
    
    assert session.completed
    assert session.end_time is not None

def test_to_dict():
    """辞書変換が正しく動作する"""
    start_time = datetime(2025, 12, 16, 10, 0, 0)
    session = PomodoroSession(start_time=start_time)
    session.complete()
    
    data = session.to_dict()
    assert data['duration'] == 25
    assert data['completed'] is True
    assert 'session_id' in data
```

**確認方法:**
```bash
pytest tests/unit/test_models.py -v
```

---

### Step 7.3: サービス層のユニットテスト
**ファイル:** `tests/unit/test_services.py`

**実装内容:**
```python
import pytest
from datetime import datetime, date
from unittest.mock import Mock
from src.services.timer_service import TimerService
from src.models.session import PomodoroSession

@pytest.fixture
def mock_repository():
    """モックリポジトリ"""
    repo = Mock()
    repo.get_today_sessions.return_value = []
    return repo

@pytest.fixture
def timer_service(mock_repository):
    """TimerServiceフィクスチャ"""
    return TimerService(repository=mock_repository)

def test_start_session(timer_service):
    """セッション開始が正しく動作"""
    session = timer_service.start_session(duration=25)
    
    assert session.duration == 25
    assert isinstance(session.start_time, datetime)
    assert not session.completed

def test_complete_session(timer_service, mock_repository):
    """セッション完了が正しく動作"""
    session = PomodoroSession(start_time=datetime.now())
    timer_service.complete_session(session)
    
    assert session.completed
    mock_repository.save.assert_called_once_with(session)

def test_get_today_stats_empty(timer_service):
    """統計取得（データなし）"""
    stats = timer_service.get_today_stats()
    
    assert stats['total_completed'] == 0
    assert stats['total_minutes'] == 0

def test_get_today_stats_with_sessions(timer_service, mock_repository):
    """統計取得（データあり）"""
    # 完了済みセッションを2つ準備
    session1 = PomodoroSession(start_time=datetime.now(), duration=25)
    session1.complete()
    session2 = PomodoroSession(start_time=datetime.now(), duration=25)
    session2.complete()
    
    mock_repository.get_today_sessions.return_value = [session1, session2]
    
    stats = timer_service.get_today_stats()
    
    assert stats['total_completed'] == 2
    assert stats['total_minutes'] == 50
    assert stats['hours'] == 0
    assert stats['minutes'] == 50
```

**確認方法:**
```bash
pytest tests/unit/test_services.py -v
```

---

### Step 7.4: リポジトリのテスト
**ファイル:** `tests/unit/test_repositories.py`

**実装内容:**
```python
import pytest
import tempfile
from pathlib import Path
from datetime import datetime, date
from src.repositories.session_repository import JsonSessionRepository
from src.models.session import PomodoroSession

@pytest.fixture
def temp_file():
    """一時ファイルを作成"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        yield f.name
    Path(f.name).unlink(missing_ok=True)

@pytest.fixture
def repository(temp_file):
    """テスト用リポジトリ"""
    return JsonSessionRepository(file_path=temp_file)

def test_save_and_load(repository):
    """保存と読み込みが正しく動作"""
    session = PomodoroSession(start_time=datetime.now())
    session.complete()
    
    repository.save(session)
    loaded = repository.get_all()
    
    assert len(loaded) == 1
    assert loaded[0].session_id == session.session_id
    assert loaded[0].completed is True

def test_get_today_sessions(repository):
    """今日のセッション取得"""
    today_session = PomodoroSession(start_time=datetime.now())
    repository.save(today_session)
    
    today_sessions = repository.get_today_sessions()
    assert len(today_sessions) == 1
```

---

### Step 7.5: 統合テスト（API）
**ファイル:** `tests/integration/test_api.py`

**実装内容:**
```python
import pytest
import tempfile
from pathlib import Path
from app import create_app

@pytest.fixture
def client():
    """テスト用Flaskクライアント"""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """ヘルスチェックAPI"""
    response = client.get('/api/health')
    assert response.status_code == 200

def test_start_session(client):
    """セッション開始API"""
    response = client.post('/api/session/start',
                          json={'duration': 25})
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'session_id' in data

def test_complete_session(client):
    """セッション完了API"""
    # まずセッション開始
    start_response = client.post('/api/session/start',
                                 json={'duration': 25})
    session_id = start_response.get_json()['session_id']
    
    # セッション完了
    complete_response = client.post('/api/session/complete',
                                    json={'session_id': session_id})
    data = complete_response.get_json()
    
    assert complete_response.status_code == 200
    assert data['success'] is True

def test_get_stats(client):
    """統計取得API"""
    response = client.get('/api/stats/today')
    data = response.get_json()
    
    assert response.status_code == 200
    assert 'total_completed' in data
    assert 'total_minutes' in data
```

---

### Step 7.6: テスト実行とカバレッジ
**ファイル:** `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --cov=src
    --cov-report=html
    --cov-report=term-missing
```

**確認方法:**
```bash
# 全テスト実行
pytest

# カバレッジレポート確認
open htmlcov/index.html
```

**成功基準:**
- 全テストが通る
- カバレッジ80%以上

---

### ✅ Phase 7 完了チェックリスト
- [ ] ユニットテストがすべて通る
- [ ] 統合テストがすべて通る
- [ ] コードカバレッジ80%以上
- [ ] CI/CD準備完了（GitHub Actionsなど）

---

## 最終確認チェックリスト

### 機能要件
- [ ] タイマーが25分正確にカウントダウン
- [ ] 開始ボタンでタイマー開始
- [ ] リセットボタンでリセット
- [ ] タイマー完了時に統計更新
- [ ] 今日の完了セッション数表示
- [ ] 今日の集中時間表示
- [ ] データが永続化される

### 非機能要件
- [ ] レスポンシブデザイン対応
- [ ] アニメーションが滑らか
- [ ] エラーハンドリング実装
- [ ] テストカバレッジ80%以上
- [ ] コードが読みやすい（コメント、命名）

### デプロイ準備
- [ ] README.md更新
- [ ] requirements.txt完成
- [ ] .gitignore設定
- [ ] 環境変数設定（.env.example作成）

---

## トラブルシューティング

### よくある問題と解決策

#### 1. JSONファイルが作成されない
```bash
# ディレクトリの確認
ls -la data/

# 権限の確認
chmod -R 755 data/
```

#### 2. タイマーが正確にカウントダウンしない
- `setInterval` の代わりに `requestAnimationFrame` を検討
- サーバー時刻との同期を検討

#### 3. CORSエラー
```python
# Flask-CORSをインストール
pip install flask-cors

# app.pyに追加
from flask_cors import CORS
CORS(app)
```

#### 4. テストが失敗する
```bash
# テストデータのクリーンアップ
rm -rf data/test_*.json

# キャッシュクリア
pytest --cache-clear
```

---

## 次のステップ（Phase 8以降）

### 拡張機能案
1. **休憩時間機能**
   - 5分休憩
   - 15分長時間休憩
   - 自動切り替え

2. **カスタムタイマー設定**
   - ユーザーが時間を設定可能
   - プリセット保存

3. **通知機能**
   - 音声通知
   - デスクトップ通知（Notification API）

4. **データ可視化**
   - グラフ表示（Chart.js）
   - 週次/月次レポート

5. **ユーザー認証**
   - 複数ユーザー対応
   - ログイン機能

6. **デプロイ**
   - Heroku/Railway/Render
   - Docker化
   - CI/CD（GitHub Actions）

---

## まとめ

この実装計画に従うことで、以下を達成できます:

1. **段階的な実装**: 各フェーズが独立して動作確認可能
2. **テスト駆動**: 各フェーズでテストを実施
3. **品質保証**: 80%以上のテストカバレッジ
4. **保守性**: クリーンアーキテクチャによる高い保守性
5. **拡張性**: 将来の機能追加が容易

各フェーズを完了するごとに、動作するアプリケーションが手元にあります。
焦らず、1つずつ確実に実装していきましょう！
