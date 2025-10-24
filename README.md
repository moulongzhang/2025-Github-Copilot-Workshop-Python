# 🍅 ポモドーロタイマー Webアプリケーション

Flask + HTML/CSS/JavaScriptを使用したポモドーロタイマーWebアプリケーション

ワークショップの手順：https://moulongzhang.github.io/2025-Github-Copilot-Workshop/github-copilot-workshop/#0

## 📋 プロジェクト概要

このプロジェクトは、効率的な作業時間管理のためのポモドーロタイマーWebアプリケーションです。25分の作業セッションと短い休憩を繰り返すポモドーロ・テクニックをサポートします。

### 🎯 主要機能

- **25分作業タイマー**: 集中作業のための基本タイマー
- **休憩タイマー**: 5分（短い休憩）/ 15分（長い休憩）
- **リアルタイム更新**: WebSocketによる即座の状態同期
- **セッション履歴**: 完了セッションの記録と統計
- **レスポンシブUI**: デスクトップ・モバイル対応

## 🏗️ アーキテクチャ

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

### 技術スタック
- **バックエンド**: Flask, Flask-SocketIO, SQLite
- **フロントエンド**: HTML5, CSS3, Vanilla JavaScript
- **テスト**: pytest, pytest-cov, factory-boy
- **データベース**: SQLite（開発・本番）/ インメモリ（テスト）

## 📁 プロジェクト構造

```
/workspaces/2025-Github-Copilot-Workshop-Python/
├── app/                          # メインアプリケーション
│   ├── models/                   # ドメインレイヤー
│   │   ├── entities/            # エンティティ
│   │   ├── repositories/        # データアクセス
│   │   ├── services/            # ビジネスロジック
│   │   └── validators/          # 入力値検証
│   ├── interfaces/              # インターフェース定義
│   ├── config/                  # 設定管理
│   ├── factories/               # アプリケーションファクトリー
│   ├── events/                  # イベント処理
│   └── routes/                  # ルーティング（API, WebSocket）
├── static/                      # 静的ファイル
│   ├── css/                    # スタイルシート
│   ├── js/                     # JavaScript
│   └── images/                 # 画像リソース
├── templates/                   # HTMLテンプレート
├── tests/                       # テストスイート
│   ├── unit/                   # 単体テスト
│   ├── integration/            # 結合テスト
│   ├── e2e/                    # E2Eテスト
│   └── fixtures/               # テストフィクスチャ
├── main.py                      # アプリケーションエントリーポイント
├── requirements.txt             # 本番依存関係
├── requirements-test.txt        # テスト依存関係
└── pytest.ini                  # テスト設定
```

## 🚀 クイックスタート

### 1. 依存関係のインストール

```bash
# 本番用依存関係
pip install -r requirements.txt

# テスト用依存関係（開発者向け）
pip install -r requirements-test.txt
```

### 2. アプリケーション起動

```bash
# 開発環境で起動
python main.py

# または環境変数で指定
FLASK_ENV=development python main.py
```

### 3. アクセス

- **メインページ**: http://localhost:5000
- **ヘルスチェック**: http://localhost:5000/health

## 🧪 テスト実行

```bash
# 全テスト実行
pytest

# カバレッジ付きテスト
pytest --cov=app --cov-report=html

# 特定のテストマーカー
pytest -m unit          # 単体テストのみ
pytest -m integration   # 結合テストのみ
```

## 📊 開発段階

### ✅ Phase 1: プロジェクト基盤設定（完了）
- Flask アプリケーション基本構造
- 依存関係管理
- 設定ファイル（開発/本番/テスト環境）
- アプリケーションファクトリーパターン
- 基本テスト設定

### 🔄 Phase 2: ドメインモデル実装（次のステップ）
- PomodoroSession エンティティ
- TimerState 値オブジェクト
- ビジネスロジック
- 単体テスト

### 📅 今後の予定
- Phase 3: 基本タイマー機能
- Phase 4: データ永続化層
- Phase 5: REST API基盤
- Phase 6: 基本UI実装（MVP完成）
- Phase 7-10: UI強化、リアルタイム通信、完成版

## 🎯 品質目標

- **テストカバレッジ**: > 90%
- **実行速度**: 全テスト < 30秒
- **ページロード**: < 2秒
- **WebSocket遅延**: < 100ms

## 📝 設定

### 環境変数

```bash
# 実行環境
FLASK_ENV=development|production|testing

# データベース
DATABASE_URL=sqlite:///pomodoro.db

# セキュリティ
SECRET_KEY=your-secret-key

# タイマー設定（開発時のみ）
DEV_WORK_DURATION=25
DEV_SHORT_BREAK_DURATION=5
DEV_LONG_BREAK_DURATION=15
```

## 🤝 コントリビューション

1. フィーチャーブランチを作成
2. テスト駆動開発（TDD）でコード実装
3. 動作確認とテスト追加
4. プルリクエスト作成

## 📚 関連ドキュメント

- [アーキテクチャ仕様書](./architecture.md)
- [機能一覧](./features.md)
- [段階的実装計画](./plan.md)

## 📄 ライセンス

MIT License

---

*最終更新: 2025年10月24日*
*現在のバージョン: v1.0.0-phase1*
