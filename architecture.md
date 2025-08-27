# ポモドーロタイマー Webアプリケーション アーキテクチャ仕様書

## 概要

本ドキュメントは、Flask + HTML/CSS/JavaScript を使用したポモドーロタイマーWebアプリケーションのアーキテクチャ設計書です。テスタビリティ、保守性、拡張性を重視した設計となっています。

## 技術スタック

### バックエンド
- **フレームワーク**: Flask (Python 3.9+)
- **リアルタイム通信**: Flask-SocketIO
- **データベース**: SQLite (開発環境) / PostgreSQL (本番環境)
- **ORM**: SQLAlchemy
- **テストフレームワーク**: pytest

### フロントエンド
- **マークアップ**: HTML5
- **スタイリング**: CSS3 (CSS Grid, Flexbox)
- **JavaScript**: Vanilla JS (ES6+)
- **リアルタイム通信**: Socket.IO Client

### 開発・テスト
- **パッケージ管理**: pip + requirements.txt
- **コード品質**: flake8, black
- **テスト**: pytest, coverage

## アーキテクチャ原則

### 1. レイヤードアーキテクチャ
- **プレゼンテーション層**: API Controller, WebSocket Handler
- **ビジネスロジック層**: Service Classes
- **データアクセス層**: Repository Pattern
- **ドメインモデル層**: Entity Classes

### 2. 依存性注入 (DI)
- 外部依存の抽象化とテスタビリティの向上
- DIコンテナによる依存関係の管理

### 3. 単一責任原則 (SRP)
- 各クラス・モジュールが単一の責務を持つ
- 疎結合な設計による変更影響の局所化

### 4. インターフェース分離
- 抽象基底クラス (ABC) による契約定義
- 本番環境とテスト環境での実装切り替え

## プロジェクト構造

```
/workspaces/2025-Github-Copilot-Workshop-Python/
├── app.py                          # アプリケーションエントリーポイント
├── wsgi.py                         # WSGI エントリーポイント
├── architecture.md                 # 本ドキュメント
├── README.md                       # プロジェクト説明
├── config/
│   ├── __init__.py
│   ├── settings.py                 # 環境別設定管理
│   ├── development.py              # 開発環境設定
│   ├── production.py               # 本番環境設定
│   └── testing.py                  # テスト環境設定
├── controllers/                    # プレゼンテーション層
│   ├── __init__.py
│   ├── timer_controller.py         # REST API コントローラー
│   └── websocket_controller.py     # WebSocket ハンドラー
├── services/                       # ビジネスロジック層
│   ├── __init__.py
│   ├── timer_service.py            # タイマービジネスロジック
│   ├── session_service.py          # セッション管理サービス
│   └── notification_service.py     # 通知サービス
├── repositories/                   # データアクセス層
│   ├── __init__.py
│   ├── base_repository.py          # リポジトリ抽象基底クラス
│   ├── session_repository.py       # セッションデータアクセス
│   ├── sqlite_repository.py        # SQLite実装
│   └── memory_repository.py        # テスト用インメモリ実装
├── models/                         # ドメインモデル層
│   ├── __init__.py
│   ├── timer_session.py            # タイマーセッションエンティティ
│   ├── timer_state.py              # タイマー状態列挙型
│   └── user_progress.py            # ユーザー進捗エンティティ
├── utils/                          # ユーティリティ
│   ├── __init__.py
│   ├── container.py                # DIコンテナ
│   ├── time_utils.py               # 時間処理抽象化
│   ├── validators.py               # 入力検証
│   ├── exceptions.py               # カスタム例外
│   └── metrics.py                  # メトリクス収集
├── static/                         # フロントエンドアセット
│   ├── css/
│   │   ├── style.css               # メインスタイルシート
│   │   └── responsive.css          # レスポンシブ対応
│   ├── js/
│   │   ├── app.js                  # メインアプリケーション
│   │   ├── timer.js                # タイマーロジック
│   │   ├── websocket.js            # WebSocket通信
│   │   └── components/
│   │       ├── progress-ring.js    # 円形プログレスバー
│   │       └── notification.js     # 通知コンポーネント
│   └── images/
│       └── pomodoro.png            # アプリアイコン
├── templates/
│   ├── base.html                   # ベーステンプレート
│   └── index.html                  # メインページテンプレート
├── tests/                          # テストディレクトリ
│   ├── __init__.py
│   ├── conftest.py                 # pytest 設定・フィクスチャ
│   ├── unit/                       # ユニットテスト
│   │   ├── test_timer_service.py
│   │   ├── test_session_service.py
│   │   ├── test_repositories.py
│   │   └── test_models.py
│   ├── integration/                # 統合テスト
│   │   ├── test_api_endpoints.py
│   │   ├── test_websocket.py
│   │   └── test_database.py
│   ├── e2e/                        # E2Eテスト
│   │   └── test_user_scenarios.py
│   └── fixtures/
│       └── test_data.py            # テストデータファクトリ
├── migrations/                     # データベースマイグレーション
│   └── versions/
├── requirements/                   # 依存関係管理
│   ├── base.txt                    # 共通依存関係
│   ├── development.txt             # 開発環境用
│   ├── production.txt              # 本番環境用
│   └── testing.txt                 # テスト環境用
└── .env.example                    # 環境変数テンプレート
```

## 主要コンポーネント設計

### 1. ドメインモデル

#### TimerSession
```python
@dataclass
class TimerSession:
    id: str
    user_id: str
    session_type: SessionType
    duration: int  # 秒
    remaining_time: int  # 秒
    start_time: datetime
    end_time: Optional[datetime]
    completed: bool
    paused: bool
```

#### SessionType
```python
class SessionType(Enum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"
```

#### TimerState
```python
class TimerState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
```

### 2. サービス層

#### TimerService
- タイマーの開始/停止/リセット
- セッション状態管理
- ポモドーロサイクル制御

#### SessionService
- セッション履歴管理
- 統計データ生成
- 進捗追跡

#### NotificationService
- セッション完了通知
- ブレイク通知
- ブラウザ通知統合

### 3. データアクセス層

#### SessionRepository Interface
```python
class SessionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, session: TimerSession) -> TimerSession:
        pass
    
    @abstractmethod
    def find_by_id(self, session_id: str) -> Optional[TimerSession]:
        pass
    
    @abstractmethod
    def find_today_sessions(self, user_id: str) -> List[TimerSession]:
        pass
    
    @abstractmethod
    def find_by_date_range(self, user_id: str, start_date: date, end_date: date) -> List[TimerSession]:
        pass
```

## API 設計

### REST Endpoints

#### タイマー操作
- `POST /api/timer/start` - タイマー開始
- `POST /api/timer/pause` - タイマー一時停止
- `POST /api/timer/resume` - タイマー再開
- `POST /api/timer/reset` - タイマーリセット
- `GET /api/timer/status` - 現在のタイマー状態取得

#### セッション管理
- `GET /api/sessions/today` - 今日のセッション一覧
- `GET /api/sessions/{session_id}` - 特定セッション詳細
- `GET /api/progress/weekly` - 週間進捗データ
- `GET /api/progress/monthly` - 月間進捗データ

### WebSocket Events

#### クライアント → サーバー
- `start_timer` - タイマー開始要求
- `pause_timer` - タイマー一時停止要求
- `reset_timer` - タイマーリセット要求

#### サーバー → クライアント
- `timer_update` - タイマー状態更新
- `session_completed` - セッション完了通知
- `timer_tick` - 1秒ごとのタイマー更新

## 設定管理

### 環境変数
```bash
# .env
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///pomodoro.db
WORK_DURATION=1500          # 25分
SHORT_BREAK_DURATION=300    # 5分
LONG_BREAK_DURATION=900     # 15分
CYCLES_FOR_LONG_BREAK=4     # 長い休憩までのサイクル数
```

### 設定クラス階層
```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    WORK_DURATION = int(os.environ.get('WORK_DURATION', '1500'))
    # 共通設定...

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = 'sqlite:///pomodoro_dev.db'

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
```

## テスト戦略

### テストピラミッド

#### 1. ユニットテスト (70%)
- **対象**: Service, Repository, Model クラス
- **特徴**: 高速実行、外部依存なし
- **ツール**: pytest, unittest.mock

#### 2. 統合テスト (20%)
- **対象**: API エンドポイント、データベース連携
- **特徴**: 実際のDB使用、WebSocket通信テスト
- **ツール**: pytest, Flask test client

#### 3. E2Eテスト (10%)
- **対象**: ユーザーシナリオ全体
- **特徴**: ブラウザ自動化、実環境テスト
- **ツール**: Selenium WebDriver

### テストダブル活用

#### モック対象
- 外部API呼び出し
- データベースアクセス
- 時間依存処理
- 通知サービス

#### テストフィクスチャ
```python
@pytest.fixture
def timer_service():
    mock_repo = Mock(spec=SessionRepositoryInterface)
    mock_time_provider = Mock(spec=TimeProvider)
    mock_notification = Mock(spec=NotificationService)
    
    return TimerService(
        session_repository=mock_repo,
        time_provider=mock_time_provider,
        notification_service=mock_notification
    )
```

## フロントエンド設計

### コンポーネント構成

#### 1. Timer Component
- 円形プログレスバー表示
- 残り時間カウントダウン
- 開始/停止/リセットボタン

#### 2. Progress Component
- 今日の完了セッション数表示
- 週間/月間統計グラフ

#### 3. Notification Component
- セッション完了アラート
- ブラウザ通知管理

### 状態管理
```javascript
class TimerApp {
    constructor() {
        this.state = {
            currentSession: null,
            timerState: 'idle',
            remainingTime: 0,
            todayProgress: {
                completedSessions: 0,
                totalFocusTime: 0
            }
        };
    }
    
    // 状態更新メソッド
    updateTimerState(newState) { /* ... */ }
    updateProgress(progress) { /* ... */ }
}
```

## セキュリティ考慮事項

### 1. 認証・認可
- セッション管理
- CSRF 保護
- XSS 対策

### 2. 入力検証
- API パラメータ検証
- SQL インジェクション対策
- バリデーションライブラリ使用

### 3. データ保護
- 機密データの暗号化
- セキュアなクッキー設定
- HTTPS 強制

## パフォーマンス最適化

### 1. フロントエンド
- リソース最小化・圧縮
- 効率的なDOM操作
- ブラウザキャッシュ活用

### 2. バックエンド
- データベースクエリ最適化
- 接続プーリング
- レスポンスキャッシュ

### 3. ネットワーク
- WebSocket接続の効率的管理
- 不要なAPIコール削減
- gzip圧縮

## 監視・ロギング

### 1. アプリケーションメトリクス
- セッション開始/完了数
- エラー発生率
- レスポンス時間

### 2. ログ出力
- 構造化ログ (JSON)
- ログレベル管理
- セキュリティログ

### 3. 監視
- ヘルスチェックエンドポイント
- アラート設定
- パフォーマンス監視

## デプロイメント

### 1. コンテナ化
- Docker コンテナ使用
- マルチステージビルド
- 軽量ベースイメージ

### 2. CI/CD パイプライン
- 自動テスト実行
- コード品質チェック
- 自動デプロイ

### 3. 環境管理
- 開発/ステージング/本番環境
- 環境変数による設定管理
- データベースマイグレーション

## 今後の拡張性

### 1. 機能拡張
- ユーザー認証システム
- カスタマイズ可能なタイマー設定
- 統計ダッシュボード
- チーム機能

### 2. 技術的改善
- マイクロサービス化
- リアルタイムデータベース
- PWA対応
- モバイルアプリ

### 3. 運用改善
- A/Bテスト基盤
- 機能フラグ管理
- 段階的デプロイ
- 障害対応自動化

---

*このドキュメントは開発進行に合わせて継続的に更新されます。*

**最終更新**: 2025年8月27日
**バージョン**: 1.0
