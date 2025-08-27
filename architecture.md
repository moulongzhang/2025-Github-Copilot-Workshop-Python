# ポモドーロタイマーWebアプリケーション アーキテクチャ仕様書

## 1. 概要

本文書は、FlaskとHTML/CSS/JavaScriptを使用したポモドーロタイマーWebアプリケーションのアーキテクチャ設計について記載します。

### 1.1 目的
- 25分の作業時間と5分の休憩時間を管理するポモドーロタイマー機能の提供
- 日別の作業統計とセッション履歴の記録・表示
- レスポンシブでモダンなUIの提供
- 高いテスタビリティと保守性を持つアーキテクチャの実現

### 1.2 技術スタック
- **バックエンド**: Flask (Python 3.9+)
- **フロントエンド**: HTML5, CSS3, JavaScript (ES6+)
- **リアルタイム通信**: Flask-SocketIO (WebSocket)
- **データベース**: SQLite (開発用) / PostgreSQL (本番用)
- **セッション管理**: Flask-Session
- **テストフレームワーク**: pytest

## 2. アーキテクチャ概要

### 2.1 アーキテクチャパターン
- **レイヤードアーキテクチャ**: プレゼンテーション層、ビジネスロジック層、データアクセス層の分離
- **依存性注入**: テスタビリティと疎結合を実現
- **リポジトリパターン**: データアクセス層の抽象化
- **MVC パターン**: Model-View-Controller の分離

### 2.2 アーキテクチャ図
```
┌─────────────────────────────────────────────┐
│              Frontend Layer                  │
│  ┌─────────────┐ ┌─────────────────────────┐ │
│  │    HTML     │ │     JavaScript          │ │
│  │   CSS       │ │  ┌─────────────────────┐ │ │
│  │             │ │  │ Timer Controller    │ │ │
│  └─────────────┘ │  │ UI Controller       │ │ │
│                  │  │ WebSocket Client    │ │ │
│                  │  └─────────────────────┘ │ │
│                  └─────────────────────────┘ │
└─────────────────────────────────────────────┘
                        │ HTTP/WebSocket
┌─────────────────────────────────────────────┐
│              Backend Layer                   │
│  ┌─────────────────────────────────────────┐ │
│  │         Flask Application                │ │
│  │  ┌─────────────┐ ┌─────────────────────┐ │ │
│  │  │   Routes    │ │    WebSocket        │ │ │
│  │  │  (API/Web)  │ │    Handlers         │ │ │
│  │  └─────────────┘ └─────────────────────┘ │ │
│  └─────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────┐ │
│  │         Service Layer                    │ │
│  │  ┌─────────────┐ ┌─────────────────────┐ │ │
│  │  │TimerService │ │  StatsService       │ │ │
│  │  │             │ │                     │ │ │
│  │  └─────────────┘ └─────────────────────┘ │ │
│  └─────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────┐ │
│  │       Repository Layer                   │ │
│  │  ┌─────────────┐ ┌─────────────────────┐ │ │
│  │  │Session Repo │ │   Stats Repo        │ │ │
│  │  │             │ │                     │ │ │
│  │  └─────────────┘ └─────────────────────┘ │ │
│  └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────┐
│            Data Layer                        │
│  ┌─────────────────────────────────────────┐ │
│  │         Database                         │ │
│  │  ┌─────────────┐ ┌─────────────────────┐ │ │
│  │  │pomodoro_    │ │   daily_stats       │ │ │
│  │  │sessions     │ │                     │ │ │
│  │  └─────────────┘ └─────────────────────┘ │ │
│  └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## 3. プロジェクト構造

```
pomodoro_app/
├── app.py                          # Flask アプリケーションのエントリーポイント
├── config/
│   ├── __init__.py
│   ├── base.py                     # 基本設定
│   ├── development.py              # 開発環境設定
│   ├── testing.py                  # テスト環境設定
│   └── production.py               # 本番環境設定
├── models/
│   ├── __init__.py
│   ├── timer.py                    # タイマー関連のドメインモデル
│   └── session.py                  # セッション記録モデル
├── services/
│   ├── __init__.py
│   ├── timer_service.py            # タイマーのビジネスロジック
│   └── stats_service.py            # 統計情報の処理
├── repositories/
│   ├── __init__.py
│   ├── session_repository.py       # セッションデータアクセス
│   └── stats_repository.py         # 統計データアクセス
├── routes/
│   ├── __init__.py
│   ├── main.py                     # メインページのルート
│   └── api.py                      # REST API エンドポイント
├── websocket/
│   ├── __init__.py
│   └── handlers.py                 # WebSocket イベントハンドラー
├── static/
│   ├── css/
│   │   ├── style.css              # メインスタイルシート
│   │   └── components.css         # コンポーネント別スタイル
│   ├── js/
│   │   ├── timer.js               # タイマー機能
│   │   ├── ui.js                  # UI制御
│   │   ├── websocket.js           # WebSocket通信
│   │   └── utils.js               # ユーティリティ関数
│   └── images/
│       └── icons/                 # アイコン類
├── templates/
│   ├── base.html                  # ベーステンプレート
│   └── index.html                 # メインページ
├── database/
│   ├── __init__.py
│   ├── models.py                  # SQLAlchemy モデル定義
│   └── migrations/                # データベースマイグレーション
├── utils/
│   ├── __init__.py
│   ├── factories.py               # テスト用ファクトリー
│   └── mocks.py                   # モッククラス
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # pytest設定とフィクスチャ
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_timer_service.py  # タイマーサービスのテスト
│   │   ├── test_models.py         # モデルのテスト
│   │   └── test_stats_service.py  # 統計サービスのテスト
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_api_endpoints.py  # API統合テスト
│   │   └── test_websocket.py      # WebSocket統合テスト
│   └── fixtures/
│       └── test_data.py           # テストデータ
├── requirements/
│   ├── base.txt                   # 基本依存関係
│   ├── development.txt            # 開発用依存関係
│   └── testing.txt                # テスト用依存関係
├── pytest.ini                     # pytest設定
├── architecture.md                # 本文書
└── README.md                      # プロジェクト説明
```

## 4. 主要コンポーネント設計

### 4.1 ドメインモデル (`models/timer.py`)

```python
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional

class TimerState(Enum):
    IDLE = "idle"
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"
    PAUSED = "paused"

class SessionType(Enum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"

@dataclass
class PomodoroSession:
    id: Optional[int] = None
    duration_minutes: int = 25
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    session_type: SessionType = SessionType.WORK
    state: TimerState = TimerState.IDLE
    completed: bool = False
    paused_duration: timedelta = timedelta(0)
```

### 4.2 サービス層 (`services/timer_service.py`)

```python
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, Callable
from models.timer import PomodoroSession, TimerState, SessionType
from repositories.session_repository import SessionRepositoryInterface

class TimeProvider(ABC):
    @abstractmethod
    def now(self) -> datetime: pass
    
    @abstractmethod
    def sleep(self, seconds: float): pass

class TimerService:
    def __init__(self, 
                 session_repository: SessionRepositoryInterface,
                 time_provider: TimeProvider,
                 event_emitter: Optional[Callable] = None):
        self.session_repository = session_repository
        self.time_provider = time_provider
        self.event_emitter = event_emitter
        self.current_session: Optional[PomodoroSession] = None
        
    def start_session(self, session_type: SessionType, duration_minutes: int) -> bool:
        """新しいセッションを開始"""
        
    def pause_session(self) -> bool:
        """現在のセッションを一時停止"""
        
    def resume_session(self) -> bool:
        """一時停止中のセッションを再開"""
        
    def complete_session(self) -> bool:
        """現在のセッションを完了"""
        
    def reset_session(self) -> bool:
        """現在のセッションをリセット"""
        
    def get_remaining_time(self) -> Optional[timedelta]:
        """残り時間を取得"""
        
    def get_current_session(self) -> Optional[PomodoroSession]:
        """現在のセッションを取得"""
```

### 4.3 リポジトリ層 (`repositories/session_repository.py`)

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date, datetime
from models.timer import PomodoroSession

class SessionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, session: PomodoroSession) -> int: pass
    
    @abstractmethod
    def get_by_id(self, session_id: int) -> Optional[PomodoroSession]: pass
    
    @abstractmethod
    def get_by_date_range(self, start_date: date, end_date: date) -> List[PomodoroSession]: pass
    
    @abstractmethod
    def get_completed_sessions_by_date(self, target_date: date) -> List[PomodoroSession]: pass
    
    @abstractmethod
    def update(self, session: PomodoroSession) -> bool: pass
    
    @abstractmethod
    def delete(self, session_id: int) -> bool: pass

class SQLiteSessionRepository(SessionRepositoryInterface):
    """SQLite実装のセッションリポジトリ"""
    
class InMemorySessionRepository(SessionRepositoryInterface):
    """テスト用インメモリリポジトリ"""
```

### 4.4 API レイヤー (`routes/api.py`)

```python
from flask import Blueprint, request, jsonify
from services.timer_service import TimerService
from models.timer import SessionType

api_bp = Blueprint('api', __name__)

@api_bp.route('/timer/start', methods=['POST'])
def start_timer():
    """タイマー開始 API"""
    
@api_bp.route('/timer/pause', methods=['POST'])
def pause_timer():
    """タイマー一時停止 API"""
    
@api_bp.route('/timer/resume', methods=['POST'])
def resume_timer():
    """タイマー再開 API"""
    
@api_bp.route('/timer/reset', methods=['POST'])
def reset_timer():
    """タイマーリセット API"""
    
@api_bp.route('/timer/status', methods=['GET'])
def get_timer_status():
    """タイマー状態取得 API"""
    
@api_bp.route('/stats/today', methods=['GET'])
def get_today_stats():
    """今日の統計取得 API"""
    
@api_bp.route('/stats/history', methods=['GET'])
def get_history():
    """履歴取得 API"""
```

## 5. データベース設計

### 5.1 テーブル構造

```sql
-- ポモドーロセッションテーブル
CREATE TABLE pomodoro_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duration_minutes INTEGER NOT NULL DEFAULT 25,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    session_type VARCHAR(20) NOT NULL CHECK (session_type IN ('work', 'short_break', 'long_break')),
    state VARCHAR(20) NOT NULL DEFAULT 'idle' CHECK (state IN ('idle', 'work', 'short_break', 'long_break', 'paused')),
    completed BOOLEAN DEFAULT FALSE,
    paused_duration INTEGER DEFAULT 0, -- 秒単位
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 日別統計テーブル
CREATE TABLE daily_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    completed_work_sessions INTEGER DEFAULT 0,
    completed_break_sessions INTEGER DEFAULT 0,
    total_focus_time INTEGER DEFAULT 0, -- 分単位
    total_break_time INTEGER DEFAULT 0, -- 分単位
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- インデックス
CREATE INDEX idx_pomodoro_sessions_date ON pomodoro_sessions(date(start_time));
CREATE INDEX idx_pomodoro_sessions_type ON pomodoro_sessions(session_type);
CREATE INDEX idx_pomodoro_sessions_completed ON pomodoro_sessions(completed);
CREATE INDEX idx_daily_stats_date ON daily_stats(date);
```

## 6. WebSocket通信設計

### 6.1 イベント定義

**クライアント → サーバー**
```javascript
// タイマー操作要求
socket.emit('timer_start', { sessionType: 'work', duration: 25 });
socket.emit('timer_pause');
socket.emit('timer_resume');
socket.emit('timer_reset');

// 状態同期要求
socket.emit('sync_request');
```

**サーバー → クライアント**
```javascript
// タイマー状態更新
socket.emit('timer_tick', { 
    remainingTime: 1485, // 秒
    totalTime: 1500,
    state: 'work',
    sessionId: 123
});

// セッション状態変更
socket.emit('session_started', { session: sessionData });
socket.emit('session_paused', { session: sessionData });
socket.emit('session_completed', { session: sessionData });
socket.emit('session_reset');

// 統計更新
socket.emit('stats_updated', { todayStats: statsData });

// エラー通知
socket.emit('error', { message: 'エラーメッセージ' });
```

## 7. フロントエンド設計

### 7.1 主要コンポーネント

**TimerController (`static/js/timer.js`)**
```javascript
class TimerController {
    constructor() {
        this.socket = io();
        this.state = {
            isRunning: false,
            isPaused: false,
            remainingTime: 1500, // 25分
            totalTime: 1500,
            sessionType: 'work'
        };
        
        this.initializeWebSocket();
        this.bindEvents();
    }
    
    start(sessionType = 'work', duration = 25) {}
    pause() {}
    resume() {}
    reset() {}
    updateDisplay() {}
}
```

**UIController (`static/js/ui.js`)**
```javascript
class UIController {
    constructor(timerController) {
        this.timer = timerController;
        this.elements = {
            display: document.querySelector('.timer-display'),
            progressRing: document.querySelector('.progress-ring-circle'),
            startBtn: document.getElementById('startBtn'),
            resetBtn: document.getElementById('resetBtn'),
            statusText: document.querySelector('.status')
        };
        
        this.bindUIEvents();
    }
    
    updateTimerDisplay(remainingTime, totalTime) {}
    updateProgressRing(progress) {}
    updateStatus(state) {}
    updateStats(stats) {}
}
```

## 8. テスト戦略

### 8.1 テストレベル

1. **単体テスト (Unit Tests)**
   - モデルクラス
   - サービス層ロジック
   - リポジトリ層
   - ユーティリティ関数

2. **統合テスト (Integration Tests)**
   - API エンドポイント
   - WebSocket 通信
   - データベース操作

3. **エンドツーエンドテスト (E2E Tests)**
   - 完全なユーザーシナリオ

### 8.2 テスト設計原則

- **依存性注入**: モックとスタブの活用
- **時間の抽象化**: TimeProvider で時間制御をテスト可能に
- **データの分離**: テスト用データベースとフィクスチャ
- **並行テスト**: テスト間の独立性確保

### 8.3 テストカバレッジ目標

- **単体テスト**: 90%以上
- **統合テスト**: 主要フロー100%
- **全体**: 80%以上

## 9. セキュリティ考慮事項

### 9.1 実装予定のセキュリティ対策

- **CSRF防護**: Flask-WTF によるCSRFトークン
- **XSS対策**: テンプレートエスケープとContent Security Policy
- **SQLインジェクション対策**: SQLAlchemy ORM使用
- **セッション管理**: Flask-Session による安全なセッション管理
- **入力検証**: フォームバリデーションとサニタイゼーション

## 10. パフォーマンス考慮事項

### 10.1 最適化戦略

- **データベース**: 適切なインデックス設計
- **WebSocket**: イベントの最適化と適切な切断処理
- **フロントエンド**: CSS/JavaScript の最小化と圧縮
- **キャッシュ**: 静的ファイルのブラウザキャッシュ活用

## 11. 拡張性と保守性

### 11.1 設計原則

- **単一責任の原則**: 各クラスは一つの責任のみ持つ
- **開放閉鎖の原則**: 拡張に対して開放、修正に対して閉鎖
- **依存性逆転の原則**: 抽象に依存し、具象に依存しない
- **インターフェース分離**: 不要な依存を避ける

### 11.2 将来の拡張ポイント

- **ユーザー認証**: マルチユーザー対応
- **カスタム設定**: 作業時間・休憩時間の調整
- **通知機能**: ブラウザ通知、メール通知
- **統計の詳細化**: 週次・月次レポート
- **チーム機能**: グループでのポモドーロ管理

## 12. 開発・運用

### 12.1 環境構成

- **開発環境**: Flask Development Server + SQLite
- **テスト環境**: pytest + In-Memory Database
- **本番環境**: Gunicorn + PostgreSQL + Nginx

### 12.2 デプロイメント

- **コンテナ化**: Docker対応
- **CI/CD**: GitHub Actions
- **監視**: ログ監視とヘルスチェック

---

**作成日**: 2025年8月8日  
**バージョン**: 1.0  
**作成者**: Development Team
