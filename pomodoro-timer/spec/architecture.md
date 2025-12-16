# ポモドーロタイマー Webアプリケーション アーキテクチャ

## 概要

Flask と HTML/CSS/JavaScript を使用したポモドーロタイマー Web アプリケーションの設計ドキュメント。
ユニットテストのしやすさを考慮した設計となっている。

---

## ディレクトリ構造

```
/workspaces/2025-Github-Copilot-Workshop-Python/
├── app.py                        # Flaskアプリ起動エントリーポイント
├── config.py                     # 設定クラス（環境別設定）
├── requirements.txt              # 依存パッケージ
├── requirements-dev.txt          # 開発・テスト用依存パッケージ
│
├── pomodoro/                     # アプリケーションパッケージ
│   ├── __init__.py               # Flaskアプリファクトリ
│   ├── routes.py                 # ルーティング定義
│   ├── models.py                 # データモデル（タイマー設定など）
│   └── services/
│       └── timer_service.py      # ビジネスロジック（純粋Python）
│
├── static/
│   ├── css/
│   │   └── style.css             # スタイルシート
│   └── js/
│       ├── timer.js              # UIバインディング
│       ├── timerEngine.js        # タイマーロジック（純粋関数）
│       └── timerEngine.test.js   # JavaScriptテスト
│
├── templates/
│   └── index.html                # メインHTMLテンプレート
│
└── tests/                        # Pythonテスト
    ├── __init__.py
    ├── conftest.py               # pytest fixtures
    ├── test_routes.py            # エンドポイントテスト
    ├── test_models.py            # モデルテスト
    └── test_timer_service.py     # サービスロジックテスト
```

---

## コンポーネント設計

### バックエンド（Flask）

| ファイル | 役割 |
|---------|------|
| `app.py` | アプリケーション起動エントリーポイント |
| `config.py` | 環境別設定クラス |
| `pomodoro/__init__.py` | アプリファクトリ（create_app） |
| `pomodoro/routes.py` | ルーティング定義 |
| `pomodoro/models.py` | データモデル |
| `pomodoro/services/timer_service.py` | ビジネスロジック |

#### 主なエンドポイント

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/` | メインページ表示 |
| GET | `/api/settings` | タイマー設定取得（オプション） |
| POST | `/api/settings` | タイマー設定保存（オプション） |

### フロントエンド（HTML/CSS/JavaScript）

| ファイル | 役割 |
|---------|------|
| `templates/index.html` | UIレイアウト |
| `static/css/style.css` | スタイリング（円形タイマー、ボタンなど） |
| `static/js/timer.js` | DOM操作・イベントハンドリング |
| `static/js/timerEngine.js` | タイマーロジック（純粋関数） |

---

## 状態管理設計

### JavaScript 状態管理

```javascript
const timerState = {
    mode: 'pomodoro',      // 'pomodoro' | 'shortBreak' | 'longBreak'
    timeRemaining: 1500,   // 秒単位
    isRunning: false,
    pomodoroCount: 0,      // 完了したポモドーロ数
    settings: {
        pomodoro: 25,      // 分
        shortBreak: 5,
        longBreak: 15
    }
};
```

---

## テスタビリティ設計

### 設計原則

| 原則 | 適用箇所 | 効果 |
|------|----------|------|
| **依存性注入** | `create_app(config)` | テスト用設定の注入が容易 |
| **関心の分離** | サービス層の追加 | ビジネスロジックを独立してテスト |
| **純粋関数** | `timerEngine.js` | 副作用なしで単体テスト可能 |
| **インターフェース分離** | routes ↔ services | モック化が容易 |
| **設定の外部化** | `config.py` | 環境別テストが可能 |

### アプリケーションファクトリパターン

```python
# pomodoro/__init__.py
from flask import Flask

def create_app(config_class=None):
    """テスト時に異なる設定を注入可能"""
    app = Flask(__name__)
    
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object('config.ProductionConfig')
    
    from pomodoro.routes import bp
    app.register_blueprint(bp)
    
    return app
```

### 設定クラス

```python
# config.py
class Config:
    """基底設定"""
    POMODORO_DURATION = 25
    SHORT_BREAK_DURATION = 5
    LONG_BREAK_DURATION = 15

class TestConfig(Config):
    """テスト用設定"""
    TESTING = True
    POMODORO_DURATION = 1  # テスト時は短い時間

class ProductionConfig(Config):
    """本番用設定"""
    pass
```

### サービス層（純粋なビジネスロジック）

```python
# pomodoro/services/timer_service.py
class TimerService:
    """純粋なビジネスロジック - Flaskに依存しない"""
    
    def __init__(self, settings: dict):
        self.settings = settings
    
    def get_duration(self, mode: str) -> int:
        """モードに応じた時間（秒）を返す"""
        durations = {
            'pomodoro': self.settings['pomodoro'] * 60,
            'short_break': self.settings['short_break'] * 60,
            'long_break': self.settings['long_break'] * 60,
        }
        return durations.get(mode, 0)
    
    def should_take_long_break(self, completed_count: int) -> bool:
        """長い休憩を取るべきか判定"""
        return completed_count > 0 and completed_count % 4 == 0
```

### JavaScript 純粋関数

```javascript
// static/js/timerEngine.js
export const TimerEngine = {
    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },
    
    calculateProgress(remaining, total) {
        return ((total - remaining) / total) * 100;
    },
    
    getNextMode(currentMode, completedCount) {
        if (currentMode !== 'pomodoro') return 'pomodoro';
        return completedCount % 4 === 0 ? 'longBreak' : 'shortBreak';
    }
};
```

### テストフィクスチャ

```python
# tests/conftest.py
import pytest
from pomodoro import create_app
from config import TestConfig

@pytest.fixture
def app():
    """テスト用Flaskアプリ"""
    return create_app(TestConfig)

@pytest.fixture
def client(app):
    """テストクライアント"""
    return app.test_client()

@pytest.fixture
def timer_service():
    """テスト用TimerService"""
    from pomodoro.services.timer_service import TimerService
    return TimerService({
        'pomodoro': 1,
        'short_break': 1,
        'long_break': 2
    })
```

---

## 技術スタック

| レイヤー | 技術 | 理由 |
|---------|------|------|
| バックエンド | Flask | 軽量、学習コスト低、テンプレートエンジン内蔵 |
| フロントエンド | Vanilla JS | シンプルなアプリなのでフレームワーク不要 |
| スタイリング | CSS3 | カスタムプロパティ、アニメーション対応 |
| ストレージ | localStorage | セッション永続化（DB不要） |

---

## テストツール

| 用途 | ツール |
|------|--------|
| Python単体テスト | `pytest` |
| Flaskテスト | `pytest-flask` |
| カバレッジ | `pytest-cov` |
| JavaScriptテスト | `Jest` または `Vitest` |
| E2Eテスト（オプション） | `Playwright` |

---

## 依存パッケージ

### requirements.txt

```
Flask>=3.0.0
```

### requirements-dev.txt

```
pytest>=7.0.0
pytest-flask>=1.2.0
pytest-cov>=4.0.0
```

---

## 開発フェーズ

| フェーズ | 内容 |
|---------|------|
| **Phase 1** | 基本構造セットアップ（Flask + 静的ファイル） |
| **Phase 2** | タイマーUI実装（HTML/CSS） |
| **Phase 3** | タイマーロジック実装（JavaScript） |
| **Phase 4** | モード切り替え・設定機能 |
| **Phase 5** | 通知・サウンド・アニメーション追加 |
| **Phase 6** | ユニットテスト・E2Eテスト追加 |
