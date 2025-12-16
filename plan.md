# ポモドーロタイマー 段階的実装計画

## 🎯 段階的実装計画

### 全体方針

**アプローチ**: Vertical Slice（垂直スライス）方式
- 各段階で完全に動作する機能を実装
- UI → ロジック → データ層を一気通貫で実装
- 常にデプロイ可能な状態を維持
- 早期からユーザーフィードバックを得られる

---

## Stage 0: プロジェクトセットアップ（1日）

### 目的
開発環境を整え、最初のコミットまで完了させる

### 実装内容
- [ ] **プロジェクト構造の作成**
  ```bash
  mkdir -p app/{static/{css,js,assets/sounds},templates,models,routes,services}
  mkdir -p tests/{unit,integration}
  ```

- [ ] **依存関係のセットアップ**
  - `requirements.txt` 作成（Flask, SQLAlchemy等）
  - `requirements-dev.txt` 作成（pytest, black等）
  - 仮想環境の作成とインストール

- [ ] **基本設定ファイル**
  - `.env.example` 作成
  - `.gitignore` 作成
  - `pytest.ini` 作成
  - `README.md` 作成

- [ ] **Hello World Flask アプリ**
  - `app/__init__.py` でアプリケーションファクトリ
  - `run.py` で開発サーバー起動
  - 動作確認: `http://localhost:5000`

### 完了条件
- ✅ Flask アプリが起動する
- ✅ トップページが表示される
- ✅ Git リポジトリが初期化されている

### 成果物
```
pomodoro-timer/
├── app/
│   ├── __init__.py
│   ├── static/
│   └── templates/
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

---

## Stage 1: 最小限の動くタイマー（2-3日）

### 目的
**フロントエンドのみで動作するタイマーを実装**（バックエンドは静的ファイル配信のみ）

### 実装内容

#### 1.1 基本HTML構造
- [ ] `templates/base.html` - 基底テンプレート
- [ ] `templates/index.html` - メインページ
  - タイマー表示エリア（25:00）
  - ボタン（開始/一時停止/リセット）
  - セッションタイプ表示（Work/Break）
  - セッションカウンター

#### 1.2 CSS スタイリング
- [ ] `static/css/variables.css` - CSS変数定義
  ```css
  :root {
    --color-primary: #e74c3c;
    --color-work: #e74c3c;
    --color-break: #27ae60;
    --color-long-break: #3498db;
  }
  ```
- [ ] `static/css/main.css` - メインスタイル
  - レイアウト（Flexbox/Grid）
  - タイマー表示（大きなフォント）
  - ボタンスタイル
  - 円形プログレスバー（CSS/SVG）

#### 1.3 JavaScript タイマーロジック
- [ ] `static/js/timer.js` - タイマークラス
  ```javascript
  class PomodoroTimer {
    constructor() {
      this.workDuration = 25 * 60;      // 25分
      this.shortBreak = 5 * 60;         // 5分
      this.longBreak = 15 * 60;         // 15分
      this.currentTime = this.workDuration;
      this.isRunning = false;
      this.sessionCount = 0;
      this.currentType = 'work';
    }
    
    start() { /* カウントダウン開始 */ }
    pause() { /* 一時停止 */ }
    reset() { /* リセット */ }
    tick() { /* 1秒ごとの処理 */ }
  }
  ```

- [ ] `static/js/app.js` - UI制御
  - タイマー表示の更新
  - ボタンイベント処理
  - プログレスバー更新
  - セッション自動切り替え

#### 1.4 LocalStorage対応
- [ ] タイマー状態の保存
- [ ] ページリロード時の復元

### テスト
- [ ] 手動テスト: タイマーが正常に動作するか
- [ ] タイマーの開始/停止/リセット
- [ ] セッションの自動切り替え
- [ ] リロード時の状態復元

### 完了条件
- ✅ タイマーが正しくカウントダウンする
- ✅ 開始/一時停止/リセットが動作する
- ✅ 作業→休憩のセッション切り替えが動作する
- ✅ ページをリロードしても状態が保持される
- ✅ モバイルでも表示が崩れない

### デモ可能なこと
「25分のポモドーロタイマーが動く！」

---

## Stage 2: バックエンド基盤とAPI（2-3日）

### 目的
**フロントエンドとバックエンドを分離し、REST APIを導入**

### 実装内容

#### 2.1 ドメインモデル
- [ ] `app/models/session.py`
  ```python
  from enum import Enum
  from dataclasses import dataclass
  from datetime import datetime
  
  class SessionType(Enum):
      WORK = "work"
      SHORT_BREAK = "short_break"
      LONG_BREAK = "long_break"
  
  @dataclass
  class TimerState:
      current_time: int
      is_running: bool
      session_type: SessionType
      session_count: int
  ```

#### 2.2 サービス層
- [ ] `app/services/timer_service.py`
  - タイマーのビジネスロジック
  - セッション管理
  - 状態管理

#### 2.3 API エンドポイント
- [ ] `app/routes/api.py`
  ```python
  @api_bp.route('/timer/start', methods=['POST'])
  @api_bp.route('/timer/pause', methods=['POST'])
  @api_bp.route('/timer/reset', methods=['POST'])
  @api_bp.route('/timer/state', methods=['GET'])
  ```

#### 2.4 フロントエンド改修
- [ ] `static/js/api-client.js` - API通信モジュール
  ```javascript
  class PomodoroAPI {
    async startTimer() { /* POST /api/timer/start */ }
    async pauseTimer() { /* POST /api/timer/pause */ }
    async getState() { /* GET /api/timer/state */ }
  }
  ```
- [ ] `app.js` をAPI連携に書き換え

#### 2.5 エラーハンドリング
- [ ] APIエラーの適切な処理
- [ ] ネットワークエラー時のフォールバック

### テスト
- [ ] **ユニットテスト**
  - `tests/unit/test_timer_service.py`
  - タイマーロジックのテスト
  
- [ ] **統合テスト**
  - `tests/integration/test_api.py`
  - APIエンドポイントのテスト

### 完了条件
- ✅ すべてのタイマー操作がAPIを経由する
- ✅ APIが正しいレスポンスを返す
- ✅ テストカバレッジ > 70%
- ✅ Stage 1の機能が引き続き動作する

### デモ可能なこと
「フロントエンドとバックエンドが分離され、REST APIで通信する」

---

## Stage 3: データベースとセッション履歴（3-4日）

### 目的
**セッションの記録と履歴表示機能を追加**

### 実装内容

#### 3.1 データベース設計
- [ ] `app/models/session.py` - ORMモデル追加
  ```python
  class PomodoroSession(db.Model):
      id = db.Column(UUID, primary_key=True)
      session_type = db.Column(Enum(SessionType))
      duration = db.Column(Integer)
      started_at = db.Column(DateTime)
      completed_at = db.Column(DateTime, nullable=True)
      interrupted = db.Column(Boolean, default=False)
  ```

- [ ] マイグレーション設定（Flask-Migrate）
  ```bash
  flask db init
  flask db migrate -m "Create sessions table"
  flask db upgrade
  ```

#### 3.2 リポジトリ層
- [ ] `app/repositories/session_repository.py`
  ```python
  class SessionRepository:
      def save(self, session: PomodoroSession)
      def find_by_date(self, date: datetime)
      def find_recent(self, limit: int)
  ```

#### 3.3 サービス層拡張
- [ ] `app/services/session_service.py`
  - セッション開始時にDB記録
  - セッション完了時に更新
  - 中断時の処理

#### 3.4 API拡張
- [ ] `GET /api/sessions` - セッション一覧
- [ ] `GET /api/sessions/today` - 今日のセッション
- [ ] `DELETE /api/sessions/{id}` - セッション削除

#### 3.5 UI追加
- [ ] `templates/components/session-history.html`
  - 今日のセッション一覧
  - セッション詳細（開始時刻、終了時刻、中断の有無）
  
- [ ] `static/js/session-history.js`
  - セッション履歴の表示
  - 削除機能

### テスト
- [ ] **リポジトリテスト**
  - `tests/unit/test_session_repository.py`
  
- [ ] **統合テスト**
  - セッション記録のE2Eテスト

### 完了条件
- ✅ セッションがDBに保存される
- ✅ 履歴が正しく表示される
- ✅ マイグレーションが正常に動作する
- ✅ テストカバレッジ > 75%

### デモ可能なこと
「完了したセッションが記録され、履歴を確認できる」

---

## Stage 4: 統計機能と設定（3-4日）

### 目的
**統計ダッシュボードと設定機能を追加**

### 実装内容

#### 4.1 統計計算サービス
- [ ] `app/services/statistics_service.py`
  ```python
  class StatisticsService:
      def get_daily_stats(self, date)
      def get_weekly_stats(self, week)
      def get_monthly_stats(self, month)
      def calculate_focus_score(self, sessions)
  ```

#### 4.2 設定機能
- [ ] `app/models/settings.py` - 設定モデル
  ```python
  @dataclass
  class Settings:
      work_duration: int = 1500
      short_break_duration: int = 300
      long_break_duration: int = 900
      sessions_until_long_break: int = 4
      auto_start_breaks: bool = False
  ```

- [ ] `app/repositories/settings_repository.py`
- [ ] LocalStorage または DB に保存

#### 4.3 API追加
- [ ] `GET /api/statistics/today`
- [ ] `GET /api/statistics/week`
- [ ] `GET /api/statistics/month`
- [ ] `GET /api/settings`
- [ ] `PUT /api/settings`

#### 4.4 UI実装
- [ ] `templates/statistics.html` - 統計ページ
  - 今日の完了セッション数
  - 総作業時間
  - 中断率
  - 集中度スコア
  
- [ ] 設定モーダル
  - 各種時間の設定
  - 保存・リセット機能
  
- [ ] `static/js/statistics.js`

#### 4.5 簡易グラフ（オプション）
- [ ] Chart.js 統合
- [ ] 日別セッション数の棒グラフ
- [ ] 週間推移の折れ線グラフ

### テスト
- [ ] 統計計算のユニットテスト
- [ ] 設定保存・読み込みのテスト

### 完了条件
- ✅ 統計が正しく計算される
- ✅ 設定が保存・適用される
- ✅ グラフが表示される（オプション）
- ✅ テストカバレッジ > 80%

### デモ可能なこと
「統計ダッシュボードで生産性を確認でき、タイマーをカスタマイズできる」

---

## Stage 5: 通知機能とセキュリティ（2-3日）

### 目的
**ユーザー体験を向上させる通知機能とセキュリティ強化**

### 実装内容

#### 5.1 音声通知
- [ ] `static/assets/sounds/` - 通知音ファイル追加
  - work-complete.mp3
  - break-complete.mp3
  
- [ ] `static/js/notifications.js`
  ```javascript
  class NotificationManager {
    playSound(type) { /* Audio API */ }
    showDesktopNotification(title, body) { /* Notifications API */ }
  }
  ```

#### 5.2 デスクトップ通知
- [ ] Web Notifications API 実装
- [ ] 通知権限のリクエスト
- [ ] セッション完了時の通知

#### 5.3 セキュリティ実装
- [ ] CSRF保護（Flask-WTF）
  ```python
  from flask_wtf.csrf import CSRFProtect
  csrf = CSRFProtect(app)
  ```
  
- [ ] レート制限（Flask-Limiter）
  ```python
  limiter = Limiter(
      app,
      default_limits=["200 per day", "50 per hour"]
  )
  ```
  
- [ ] 入力バリデーション（Pydantic）
- [ ] CORS設定

#### 5.4 環境変数管理
- [ ] `.env` での設定管理
- [ ] 環境別設定（開発/本番）

### テスト
- [ ] 通知機能の手動テスト
- [ ] セキュリティ設定の確認

### 完了条件
- ✅ セッション完了時に音声が鳴る
- ✅ デスクトップ通知が表示される
- ✅ CSRF保護が有効
- ✅ レート制限が動作する

### デモ可能なこと
「セッション完了時に音と通知でお知らせしてくれる」

---

## Stage 6: PWAとアクセシビリティ（2-3日）

### 目的
**アプリをインストール可能にし、アクセシビリティを向上**

### 実装内容

#### 6.1 PWA対応
- [ ] `static/manifest.json`
  ```json
  {
    "name": "Pomodoro Timer",
    "short_name": "Pomodoro",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#e74c3c",
    "icons": [ /* 各サイズのアイコン */ ]
  }
  ```
  
- [ ] `static/service-worker.js`
  - オフライン対応
  - キャッシュ戦略
  
- [ ] アプリアイコン作成（192x192, 512x512等）

#### 6.2 アクセシビリティ
- [ ] ARIA属性の追加
  ```html
  <button aria-label="Start timer">Start</button>
  <div role="timer" aria-live="polite">25:00</div>
  ```
  
- [ ] キーボードショートカット
  - Space: 開始/停止
  - R: リセット
  - S: スキップ
  
- [ ] フォーカス管理
- [ ] スクリーンリーダー対応

#### 6.3 テーマ機能
- [ ] ライトモード/ダークモード
- [ ] システム設定との連動
- [ ] CSS変数での実装

### テスト
- [ ] Lighthouse監査（PWAスコア > 90）
- [ ] アクセシビリティ監査（スコア > 90）
- [ ] 各種デバイスでの動作確認

### 完了条件
- ✅ アプリがインストール可能
- ✅ オフラインで動作する
- ✅ キーボードで操作できる
- ✅ Lighthouseスコア > 90

### デモ可能なこと
「スマホにアプリとしてインストールでき、オフラインでも使える」

---

## Stage 7: 最終調整と最適化（2-3日）

### 目的
**パフォーマンス最適化とバグ修正**

### 実装内容

#### 7.1 パフォーマンス最適化
- [ ] CSS/JSの最小化
- [ ] 画像の最適化
- [ ] レンダリングパフォーマンス改善
- [ ] データベースクエリ最適化
- [ ] インデックス追加

#### 7.2 エラーハンドリング改善
- [ ] 包括的なエラーハンドリング
- [ ] ユーザーフレンドリーなエラーメッセージ
- [ ] ロギング実装

#### 7.3 ドキュメント整備
- [ ] README.md の充実
- [ ] API仕様書
- [ ] セットアップガイド
- [ ] デプロイガイド

#### 7.4 テストカバレッジ向上
- [ ] カバレッジ 80%以上を目指す
- [ ] E2Eテスト追加（オプション）

### 完了条件
- ✅ すべての機能が安定動作
- ✅ パフォーマンスが良好
- ✅ ドキュメントが整備されている
- ✅ テストカバレッジ > 80%

---

## 📊 実装スケジュール概要

| Stage | 内容 | 期間 | 累積工数 | マイルストーン |
|-------|------|------|----------|---------------|
| **Stage 0** | プロジェクトセットアップ | 1日 | 1日 | 開発環境構築完了 |
| **Stage 1** | 最小限のタイマー | 2-3日 | 3-4日 | **🎯 MVP完成** |
| **Stage 2** | バックエンドAPI | 2-3日 | 5-7日 | API統合完了 |
| **Stage 3** | DB・履歴機能 | 3-4日 | 8-11日 | **🎯 履歴機能完成** |
| **Stage 4** | 統計・設定 | 3-4日 | 11-15日 | **🎯 主要機能完成** |
| **Stage 5** | 通知・セキュリティ | 2-3日 | 13-18日 | UX向上完了 |
| **Stage 6** | PWA・A11y | 2-3日 | 15-21日 | **🎯 本格リリース** |
| **Stage 7** | 最適化 | 2-3日 | 17-24日 | **🎉 完成** |

**合計予想工数**: 約3-4週間（1人フルタイム）

---

## 🎯 各段階の判断基準

### 次の段階に進む条件
1. ✅ 現在の段階の全機能が動作する
2. ✅ テストが書かれ、全て通る
3. ✅ コードレビュー完了（チームの場合）
4. ✅ ドキュメントが更新されている
5. ✅ Git にコミット・プッシュ済み

### 各段階でのテストデモ
- **Stage 1後**: 「タイマーが動きます！」
- **Stage 3後**: 「履歴を記録できます！」
- **Stage 4後**: 「統計が見られます！」
- **Stage 6後**: 「スマホにインストールできます！」

---

## 💡 実装のコツ

### 1. **Vertical Slice（垂直スライス）を心がける**
各機能を実装する際は、UI → API → サービス → DB まで一気通貫で実装する。

### 2. **動くものを常に維持**
どの段階でも「デモ可能な状態」を保つ。壊れたコードをコミットしない。

### 3. **テストを先に書く（TDD）**
特に Stage 2 以降は、テストを先に書くことで設計が良くなる。

### 4. **小さくコミット**
機能単位で細かくコミットし、いつでも戻れるようにする。

### 5. **早めにフィードバックを得る**
Stage 1 が完成したら、すぐに誰かに使ってもらう。

### 6. **パフォーマンスは後回し**
まずは動くものを作り、Stage 7 で最適化する。

---

## 🚀 推奨開発フロー

```
1. 機能をfeatures.mdでチェック
2. テストを書く (tests/unit/)
3. 実装する (app/)
4. テストを実行 (pytest)
5. 手動テスト
6. Git commit
7. features.mdを更新 [x]
8. 次の機能へ
```

---

## 📝 進捗トラッキング

### 現在のステータス

| Stage | ステータス | 開始日 | 完了日 | 備考 |
|-------|-----------|--------|--------|------|
| Stage 0 | ⬜ 未着手 | - | - | - |
| Stage 1 | ⬜ 未着手 | - | - | - |
| Stage 2 | ⬜ 未着手 | - | - | - |
| Stage 3 | ⬜ 未着手 | - | - | - |
| Stage 4 | ⬜ 未着手 | - | - | - |
| Stage 5 | ⬜ 未着手 | - | - | - |
| Stage 6 | ⬜ 未着手 | - | - | - |
| Stage 7 | ⬜ 未着手 | - | - | - |

### ステータスアイコン
- ⬜ 未着手
- 🚧 進行中
- ✅ 完了
- ⏸️ 一時停止
- ❌ スキップ

---

## 🔗 関連ドキュメント

- [architecture.md](architecture.md) - アーキテクチャ設計書
- [features.md](features.md) - 実装機能一覧
- [README.md](README.md) - プロジェクト概要

---

**作成日**: 2025-12-16  
**最終更新日**: 2025-12-16  
**バージョン**: 1.0
