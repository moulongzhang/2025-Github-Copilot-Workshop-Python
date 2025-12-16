# ポモドーロタイマーWebアプリケーション アーキテクチャ設計書

## 概要

FlaskとHTML/CSS/JavaScriptを使用したポモドーロタイマーWebアプリケーション。
テスタビリティとメンテナンス性を重視した設計。

## プロジェクト構成

```
/workspaces/2025-Github-Copilot-Workshop-Python/
├── app.py                              # Flaskアプリケーションのエントリーポイント
├── config.py                           # 設定管理(環境別)
├── requirements.txt                    # Python依存パッケージ
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── session.py                  # データモデル(Dataclass/Pydantic)
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py                     # Repository抽象基底クラス
│   │   └── session_repository.py      # データアクセス層
│   ├── services/
│   │   ├── __init__.py
│   │   └── timer_service.py           # ビジネスロジック層
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── api_controller.py          # API層(Flask Blueprint)
│   └── utils/
│       ├── __init__.py
│       └── datetime_helper.py         # ヘルパー関数
├── tests/
│   ├── __init__.py
│   ├── conftest.py                     # pytest共通設定
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_repositories.py
│   ├── integration/
│   │   └── test_api.py
│   └── fixtures/
│       └── sample_data.json
├── static/
│   ├── css/
│   │   └── style.css                   # スタイルシート
│   └── js/
│       └── timer.js                    # タイマーロジック
├── templates/
│   └── index.html                      # メインページ
└── data/
    └── sessions.json                   # セッションデータ(永続化用)
```

## アーキテクチャパターン

### レイヤードアーキテクチャ

```
┌─────────────────────────────────┐
│  Presentation Layer             │
│  (templates/ + static/)         │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  Controller Layer               │
│  (controllers/api_controller.py)│
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  Service Layer                  │
│  (services/timer_service.py)    │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  Repository Layer               │
│  (repositories/)                │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  Data Layer                     │
│  (data/sessions.json)           │
└─────────────────────────────────┘
```

### 各レイヤーの責務

#### 1. モデル層 (Models)
**責務:** データ構造の定義

**実装例:**
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class PomodoroSession:
    start_time: datetime
    duration: int = 25
    end_time: Optional[datetime] = None
    completed: bool = False
    
    def complete(self) -> None:
        self.end_time = datetime.now()
        self.completed = True
```

**特徴:**
- Pure Python、外部依存なし
- 不変性を考慮
- ビジネスルールを含めない

#### 2. リポジトリ層 (Repositories)
**責務:** データの永続化と取得

**実装例:**
```python
# base.py
from abc import ABC, abstractmethod

class SessionRepository(ABC):
    @abstractmethod
    def save(self, session: PomodoroSession) -> None:
        pass
    
    @abstractmethod
    def get_today_sessions(self) -> list[PomodoroSession]:
        pass
    
    @abstractmethod
    def get_sessions_by_date(self, date: str) -> list[PomodoroSession]:
        pass

# session_repository.py
class JsonSessionRepository(SessionRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def save(self, session: PomodoroSession) -> None:
        # JSON保存ロジック
        pass
    
    def get_today_sessions(self) -> list[PomodoroSession]:
        # JSON読み込みロジック
        pass
```

**特徴:**
- インターフェース(ABC)により実装を抽象化
- データソースの切り替えが容易(JSON → SQLite → PostgreSQL)
- テスト用のInMemoryRepositoryを簡単に作成可能

#### 3. サービス層 (Services)
**責務:** ビジネスロジックの実装

**実装例:**
```python
class TimerService:
    def __init__(self, 
                 repository: SessionRepository, 
                 datetime_provider=None):
        self.repository = repository
        self.datetime_provider = datetime_provider or datetime
    
    def start_session(self, duration: int = 25) -> PomodoroSession:
        """新しいポモドーロセッションを開始"""
        session = PomodoroSession(
            start_time=self.datetime_provider.now(),
            duration=duration
        )
        return session
    
    def complete_session(self, session: PomodoroSession) -> None:
        """セッションを完了してデータを保存"""
        session.complete()
        self.repository.save(session)
    
    def get_today_stats(self) -> dict:
        """今日の統計情報を取得"""
        sessions = self.repository.get_today_sessions()
        completed_sessions = [s for s in sessions if s.completed]
        
        return {
            "total_completed": len(completed_sessions),
            "total_minutes": sum(s.duration for s in completed_sessions)
        }
```

**特徴:**
- 依存性注入(DI)により、リポジトリを注入
- datetime_providerを注入して時間制御可能(テスト用)
- Pure function的、副作用が明確

#### 4. コントローラ層 (Controllers)
**責務:** HTTPリクエスト/レスポンスの処理

**実装例:**
```python
from flask import Blueprint, jsonify, request

def create_api_blueprint(timer_service: TimerService) -> Blueprint:
    api = Blueprint('api', __name__, url_prefix='/api')
    
    @api.route('/session/start', methods=['POST'])
    def start_session():
        data = request.get_json()
        duration = data.get('duration', 25)
        session = timer_service.start_session(duration)
        return jsonify({
            "success": True,
            "session_id": id(session)
        })
    
    @api.route('/session/complete', methods=['POST'])
    def complete_session():
        # セッション完了処理
        return jsonify({"success": True})
    
    @api.route('/stats/today', methods=['GET'])
    def get_today_stats():
        stats = timer_service.get_today_stats()
        return jsonify(stats)
    
    return api
```

**特徴:**
- Blueprintファクトリパターンでサービスを注入
- HTTPに関する処理のみ担当
- ビジネスロジックはサービス層に委譲

## API設計

### エンドポイント一覧

| メソッド | エンドポイント | 説明 | リクエスト | レスポンス |
|---------|---------------|------|-----------|-----------|
| GET | `/` | メインページ表示 | - | HTML |
| POST | `/api/session/start` | セッション開始 | `{"duration": 25}` | `{"success": true}` |
| POST | `/api/session/complete` | セッション完了 | `{"session_id": "..."}` | `{"success": true}` |
| GET | `/api/stats/today` | 今日の統計取得 | - | `{"total_completed": 4, "total_minutes": 100}` |
| POST | `/api/stats/reset` | 統計リセット | - | `{"success": true}` |

### データモデル

```json
{
  "date": "2025-12-16",
  "sessions": [
    {
      "start_time": "2025-12-16T10:00:00",
      "end_time": "2025-12-16T10:25:00",
      "duration": 25,
      "completed": true
    }
  ],
  "total_completed": 4,
  "total_minutes": 100
}
```

## フロントエンド設計

### 主要機能 (timer.js)

1. **タイマークラス**
   - カウントダウン機能
   - 開始/停止/リセット
   - イベント通知

2. **UI更新**
   - リアルタイムでタイマー表示
   - 円形プログレスバー更新(SVG)
   - ステータス表示(作業中/休憩中)

3. **API通信**
   - Fetch APIでバックエンド通信
   - 非同期処理
   - エラーハンドリング

4. **データ管理**
   - LocalStorageで一時保存
   - オフライン対応

### UI構成

```
┌────────────────────────────┐
│  ポモドーロタイマー         │  ← タイトル
├────────────────────────────┤
│      作業中                 │  ← ステータス
│                            │
│   ┌──────────────┐         │
│   │              │         │
│   │   25:00      │         │  ← タイマー表示
│   │              │         │     + 円形プログレス
│   └──────────────┘         │
│                            │
│   [開始]  [リセット]        │  ← アクションボタン
├────────────────────────────┤
│  今日の進捗                 │
│                            │
│  4 完了                     │
│  1時間40分 集中時間         │  ← 統計表示
└────────────────────────────┘
```

## テスト戦略

### 1. ユニットテスト (Unit Tests)

**対象:** Models, Services, Repositories

**ツール:** pytest, pytest-mock, freezegun

**例:**
```python
def test_start_session(timer_service):
    # Arrange
    mock_datetime = Mock()
    mock_datetime.now.return_value = datetime(2025, 12, 16, 10, 0, 0)
    timer_service.datetime_provider = mock_datetime
    
    # Act
    session = timer_service.start_session(duration=25)
    
    # Assert
    assert session.duration == 25
    assert session.start_time == datetime(2025, 12, 16, 10, 0, 0)
    assert not session.completed
```

### 2. 統合テスト (Integration Tests)

**対象:** API エンドポイント

**ツール:** Flask test client

**例:**
```python
def test_api_start_session(client):
    response = client.post('/api/session/start', 
                          json={'duration': 25})
    assert response.status_code == 200
    assert response.json['success'] is True
```

### 3. テストフィクスチャ (conftest.py)

```python
import pytest
from src.repositories.session_repository import SessionRepository

class InMemorySessionRepository(SessionRepository):
    def __init__(self):
        self.sessions = []
    
    def save(self, session):
        self.sessions.append(session)
    
    def get_today_sessions(self):
        return self.sessions

@pytest.fixture
def mock_repository():
    return InMemorySessionRepository()

@pytest.fixture
def timer_service(mock_repository):
    return TimerService(repository=mock_repository)

@pytest.fixture
def app(timer_service):
    app = create_app(timer_service)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()
```

### カバレッジ目標

- **全体:** 80%以上
- **サービス層:** 90%以上
- **リポジトリ層:** 80%以上
- **コントローラ層:** 70%以上

## 技術スタック

### バックエンド

```txt
Flask==3.0.0              # Webフレームワーク
pydantic==2.5.0           # データバリデーション
python-dotenv==1.0.0      # 環境変数管理
```

### テスト

```txt
pytest==7.4.0             # テストフレームワーク
pytest-cov==4.1.0         # カバレッジ測定
pytest-mock==3.12.0       # モック機能
freezegun==1.4.0          # 時間フリーズ
factory-boy==3.3.0        # テストデータ生成
```

### フロントエンド

- Vanilla JavaScript (ES6+)
- CSS3 (Flexbox, Grid, Animations)
- SVG (円形プログレスバー)

## 設計原則

### 1. 依存性注入 (Dependency Injection)

すべての依存関係をコンストラクタで注入し、テスト時にモックを注入可能にする。

### 2. 単一責任の原則 (Single Responsibility Principle)

各クラス・関数は1つの責務のみを持つ。

### 3. インターフェース分離 (Interface Segregation)

抽象基底クラス(ABC)を使用し、実装を抽象化。

### 4. 依存性逆転の原則 (Dependency Inversion Principle)

上位レイヤーは下位レイヤーの抽象に依存し、具体実装には依存しない。

## 実装の優先順位

### Phase 1: MVP (最小限の動作する製品)

1. 基本的なタイマー機能
   - カウントダウン
   - 開始/リセットボタン
   - シンプルなUI

2. データモデルとサービス層
   - PomodoroSessionモデル
   - TimerService基本機能

### Phase 2: データ永続化

1. リポジトリ層実装
   - JsonSessionRepository
   - データ保存/読み込み

2. 統計機能
   - 今日の進捗表示
   - セッション履歴

### Phase 3: UI/UX改善

1. 円形プログレスバー
2. アニメーション
3. 通知機能
4. レスポンシブデザイン

### Phase 4: テスト整備

1. ユニットテスト作成
2. 統合テスト作成
3. カバレッジ80%達成

## セキュリティ考慮事項

- **CSRF対策:** Flask-WTFを使用(必要に応じて)
- **入力検証:** Pydanticでバリデーション
- **XSS対策:** Flaskのテンプレートエスケープ機能
- **環境変数:** python-dotenvで機密情報管理

## パフォーマンス考慮事項

- **クライアントサイドタイマー:** ネットワーク負荷軽減
- **バッチ保存:** セッション完了時のみ保存
- **キャッシュ:** 統計データのキャッシング(将来的)

## 拡張性

### 将来的な拡張案

1. **ユーザー認証:** Flask-Loginで実装
2. **データベース移行:** SQLite → PostgreSQL
3. **WebSocket:** リアルタイム同期
4. **REST API:** 他クライアント対応
5. **統計ダッシュボード:** 週次/月次レポート

## まとめ

このアーキテクチャは以下の特徴を持つ:

- **テスタビリティ:** 依存性注入とレイヤー分離により高いテストカバレッジを実現
- **メンテナンス性:** 明確な責務分離により変更が容易
- **拡張性:** インターフェース抽象化により新機能追加が容易
- **シンプルさ:** 過度な複雑さを避け、必要十分な設計

このアーキテクチャに基づいて段階的に実装を進めることで、品質の高いWebアプリケーションを構築できます。
