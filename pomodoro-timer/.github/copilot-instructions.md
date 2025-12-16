# ポモドーロタイマー プロジェクト

このプロジェクトは、ポモドーロタイマーをFlaskで実装するWebアプリケーションです。

## 重要なファイル

| ファイル | 説明 |
|---------|------|
| `design/pomodoro.png` | アプリケーションのUIモック画像 |
| `spec/architecture.md` | アーキテクチャドキュメント |
| `spec/features.md` | 実装する機能の一覧 |
| `spec/plan.md` | 段階的な実装計画 |

## プロジェクト構造

```
pomodoro-timer/
├── app.py                    # Flaskアプリ起動エントリーポイント
├── config.py                 # 環境別設定
├── pomodoro/                 # アプリケーションパッケージ
│   ├── __init__.py           # create_app ファクトリ
│   ├── routes.py             # ルーティング定義
│   ├── models.py             # データモデル
│   └── services/
│       └── timer_service.py  # ビジネスロジック（純粋Python）
├── static/
│   ├── css/style.css         # スタイルシート
│   └── js/
│       ├── timer.js          # UIバインディング
│       └── timerEngine.js    # タイマーロジック（純粋関数）
├── templates/
│   └── index.html            # メインHTMLテンプレート
└── tests/                    # ユニットテスト
```

## 設計原則

- **ユニットテストのしやすさ**: ビジネスロジックはFlaskに依存しない純粋なPythonで実装
- **JavaScript**: タイマーロジックはDOMに依存しない純粋関数として実装
- **ファクトリパターン**: `create_app()` でFlaskアプリを生成し、テスト時に設定を差し替え可能

## 技術スタック

- バックエンド: Flask
- フロントエンド: HTML/CSS/JavaScript（フレームワークなし）
- テスト: pytest, pytest-flask
