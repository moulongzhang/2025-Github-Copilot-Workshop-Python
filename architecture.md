# ポモドーロタイマー Webアプリケーション アーキテクチャ仕様書

## 📋 概要

このドキュメントでは、Flask + HTML/CSS/JavaScriptを使用したポモドーロタイマーWebアプリケーションのアーキテクチャ設計について詳述します。テスタビリティ、保守性、拡張性を重視した設計となっています。

## 🎯 要件

### 機能要件
- 25分の作業タイマー機能
- 5分/15分の休憩タイマー機能
- タイマーの開始/停止/リセット操作
- リアルタイムでの進捗表示（円形プログレスバー）
- 1日の完了セッション数追跡
- セッション履歴の保存

### 非機能要件
- レスポンシブUI（モバイル対応）
- リアルタイム更新（WebSocket）
- 高いテストカバレッジ
- 保守性の高い設計

## 🏗️ アーキテクチャ概要

### レイヤード・アーキテクチャ
```
┌─────────────────────┐
│   Presentation      │ ← Flask Routes, Templates, Static Files
├─────────────────────┤
│   Application       │ ← Services, Event Handlers
├─────────────────────┤
│   Domain            │ ← Entities, Value Objects, Business Logic
├─────────────────────┤
│   Infrastructure    │ ← Repositories, External Services
└─────────────────────┘
```

## 📁 プロジェクト構造

```
/workspaces/2025-Github-Copilot-Workshop-Python/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── pomodoro_session.py     # セッションエンティティ
│   │   │   └── timer_state.py          # タイマー状態値オブジェクト
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── session_repository.py   # セッションデータアクセス抽象化
│   │   │   ├── sqlite_repository.py    # SQLite実装
│   │   │   └── memory_repository.py    # テスト用インメモリ実装
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── timer_service.py        # タイマービジネスロジック
│   │   │   └── notification_service.py # 通知サービス
│   │   └── validators/
│   │       ├── __init__.py
│   │       └── timer_validator.py      # 入力値検証
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── timer_interface.py          # タイマー関連インターフェース
│   │   └── storage_interface.py        # ストレージインターフェース
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py                 # アプリケーション設定
│   │   └── test_config.py             # テスト用設定
│   ├── factories/
│   │   ├── __init__.py
│   │   └── app_factory.py             # アプリケーションファクトリー
│   ├── events/
│   │   ├── __init__.py
│   │   ├── timer_events.py            # タイマー関連イベント
│   │   └── event_bus.py               # イベントバス
│   └── routes/
│       ├── __init__.py
│       ├── api.py                     # REST API エンドポイント
│       └── websocket.py               # WebSocket ハンドラー
├── static/
│   ├── css/
│   │   ├── style.css                  # メインスタイル
│   │   └── components.css             # コンポーネント別スタイル
│   ├── js/
│   │   ├── pomodoro.js               # メインアプリケーションロジック
│   │   ├── timer.js                  # タイマー制御
│   │   ├── ui.js                     # UI更新ロジック
│   │   └── websocket.js              # WebSocket通信
│   └── images/
│       └── favicon.ico
├── templates/
│   ├── base.html                     # ベーステンプレート
│   └── index.html                    # メインページ
├── tests/
│   ├── unit/
│   │   ├── test_timer_service.py
│   │   ├── test_pomodoro_session.py
│   │   └── test_validators.py
│   ├── integration/
│   │   ├── test_api_endpoints.py
│   │   └── test_websocket.py
│   ├── e2e/
│   │   └── test_user_flows.py
│   ├── fixtures/
│   │   └── timer_fixtures.py
│   └── conftest.py
├── app.py                            # アプリケーションエントリーポイント
├── requirements.txt                  # 本番依存関係
├── requirements-test.txt             # テスト依存関係
├── pytest.ini                       # pytest設定
├── .gitignore
└── README.md
```

## 🔧 技術スタック

### バックエンド
- **Flask**: Webフレームワーク
- **Flask-SocketIO**: リアルタイム通信
- **SQLite**: データベース（軽量、開発に適している）
- **SQLAlchemy**: ORM（オプション）

### フロントエンド
- **HTML5**: 構造
- **CSS3**: スタイリング（Flexbox/Grid、アニメーション）
- **Vanilla JavaScript**: アプリケーションロジック
- **Socket.IO Client**: リアルタイム通信

### テスト・開発ツール
- **pytest**: テストフレームワーク
- **pytest-cov**: カバレッジ測定
- **pytest-flask**: Flask専用テストヘルパー
- **pytest-mock**: モック化
- **factory-boy**: テストデータ生成
- **freezegun**: 時間のモック化

## 🎨 UI/UX 設計

### デザインコンセプト
- **カラーパレット**: 紫系グラデーション（#6366f1 → #8b5cf6）
- **タイポグラフィ**: 大きく読みやすいタイマー表示
- **レイアウト**: 中央集約型、ミニマルデザイン
- **アニメーション**: スムーズな円形プログレスバー

### レスポンシブ対応
```css
/* デスクトップ */
@media (min-width: 768px) {
  .pomodoro-container { width: 400px; }
}

/* モバイル */
@media (max-width: 767px) {
  .pomodoro-container { width: 90vw; }
}
```

## 🔄 データフロー

### 1. タイマー開始フロー
```
1. ユーザーが「開始」ボタンクリック
2. JavaScript → REST API (/api/timer/start)
3. TimerService → PomodoroSession作成
4. SessionRepository → データベース保存
5. EventBus → TimerStartedEvent発火
6. WebSocket → 全クライアントに状態通知
7. JavaScript → UI更新（プログレスバー開始）
```

### 2. リアルタイム更新フロー
```
1. サーバー側タイマー → 1秒ごとに残り時間計算
2. WebSocket → クライアントに残り時間送信
3. JavaScript → プログレスバー更新
4. タイマー完了時 → 通知表示、次のフェーズ提案
```

## 🏛️ 設計パターン

### 1. 依存性注入パターン
```python
class TimerService:
    def __init__(
        self,
        time_provider: ITimeProvider,
        storage_provider: IStorageProvider,
        notification_provider: INotificationProvider
    ):
        self._time_provider = time_provider
        self._storage = storage_provider
        self._notification = notification_provider
```

### 2. リポジトリパターン
```python
class ISessionRepository(ABC):
    @abstractmethod
    def save(self, session: PomodoroSession) -> bool:
        pass
    
    @abstractmethod
    def get_today_sessions(self) -> List[PomodoroSession]:
        pass
```

### 3. ファクトリーパターン
```python
class AppFactory:
    @staticmethod
    def create_app(config_name: str = "production"):
        if config_name == "test":
            return create_test_app()
        return create_production_app()
```

### 4. イベント駆動パターン
```python
@dataclass
class TimerCompletedEvent:
    session_id: str
    completion_time: datetime
    session_type: SessionType
```

## 🧪 テスト戦略

### テストピラミッド
```
    ┌──────────────┐
    │  E2E Tests   │ ← ユーザーフロー全体
    │   (少数)     │
    ├──────────────┤
    │ Integration  │ ← API、DB、WebSocket
    │   Tests      │
    │   (中程度)    │
    ├──────────────┤
    │  Unit Tests  │ ← ビジネスロジック
    │   (多数)     │ 
    └──────────────┘
```

### テストの種類

#### 1. Unit Tests
- **対象**: Services, Entities, Validators
- **モック**: 外部依存関係すべて
- **実行速度**: 高速（< 1秒）

#### 2. Integration Tests
- **対象**: API エンドポイント、データベース操作
- **モック**: 外部API、通知サービスのみ
- **実行速度**: 中程度（< 10秒）

#### 3. E2E Tests
- **対象**: ユーザーシナリオ全体
- **モック**: なし（実環境に近い状態）
- **実行速度**: 低速（< 60秒）

### テスト環境分離
```python
# テスト用設定
class TestSettings:
    WORK_DURATION = 0.1  # 6秒（テスト高速化）
    SHORT_BREAK = 0.05   # 3秒
    DATABASE_URL = ":memory:"
    TESTING = True
```

## 🚀 API 設計

### REST API エンドポイント
```
GET    /                    # メインページ
POST   /api/timer/start     # タイマー開始
POST   /api/timer/pause     # タイマー一時停止
POST   /api/timer/reset     # タイマーリセット
GET    /api/timer/status    # 現在のタイマー状態
GET    /api/sessions/today  # 今日のセッション一覧
```

### WebSocket イベント
```javascript
// クライアント → サーバー
emit('timer_start', { duration: 25 })
emit('timer_pause')
emit('timer_reset')

// サーバー → クライアント
on('timer_update', { remaining_time: 1480, progress: 0.12 })
on('timer_completed', { session_type: 'work', next_phase: 'short_break' })
on('session_count_updated', { today_count: 4 })
```

## 📊 パフォーマンス考慮

### フロントエンド最適化
- CSS/JSの最小化
- 画像の最適化
- ブラウザキャッシュの活用
- プログレスバーのスムーズアニメーション（CSS transform使用）

### バックエンド最適化
- データベースインデックス設定
- WebSocket接続の効率的な管理
- セッションデータの適切なクリーンアップ

## 🔒 セキュリティ

### 基本的な対策
- CSRF トークン
- XSS 対策（テンプレートエスケープ）
- HTTPS 対応（本番環境）
- 入力値検証

## 🚀 デプロイメント

### 開発環境
```bash
# 依存関係インストール
pip install -r requirements.txt
pip install -r requirements-test.txt

# アプリケーション起動
python app.py

# テスト実行
pytest
```

### 本番環境候補
- **Heroku**: 簡単デプロイ
- **Railway**: モダンなプラットフォーム
- **Vercel**: フロントエンド最適化
- **VPS**: フルコントロール

## 📈 拡張性

### 将来的な機能追加案
- ユーザー認証・登録
- カスタムタイマー設定
- 統計・分析画面
- 音声通知機能
- テーマカスタマイズ
- チーム機能（共有セッション）

### アーキテクチャの拡張性
- マイクロサービス化への対応
- 複数データベース対応
- 外部API連携
- モバイルアプリとの連携

## 📝 開発段階

### Phase 1: 基本機能（MVP）
- [x] アーキテクチャ設計
- [ ] Flask基本セットアップ
- [ ] 基本的なHTML/CSSレイアウト
- [ ] 25分タイマー機能
- [ ] 基本的なunit tests

### Phase 2: UI強化
- [ ] 円形プログレスバー実装
- [ ] 紫色グラデーションデザイン
- [ ] レスポンシブ対応
- [ ] アニメーション追加

### Phase 3: リアルタイム機能
- [ ] WebSocketでリアルタイム更新
- [ ] セッション履歴保存
- [ ] 休憩時間自動切り替え
- [ ] Integration tests追加

### Phase 4: 拡張機能
- [ ] 音声通知
- [ ] 統計画面
- [ ] 設定カスタマイズ
- [ ] E2E tests追加

## 🎯 成功指標

### 品質指標
- テストカバレッジ > 90%
- 全テスト実行時間 < 30秒
- ページロード時間 < 2秒
- WebSocket遅延 < 100ms

### ユーザビリティ指標
- 操作の直感性
- レスポンシブ対応
- アクセシビリティ準拠

---

## 📚 参考資料

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [ポモドーロ・テクニック](https://ja.wikipedia.org/wiki/%E3%83%9D%E3%83%A2%E3%83%89%E3%83%BC%E3%83%AD%E3%83%BB%E3%83%86%E3%82%AF%E3%83%8B%E3%83%83%E3%82%AF)

---

*最終更新日: 2025年10月24日*