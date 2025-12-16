# Copilot Instructions

このプロジェクトは、ポモドーロタイマーをFlaskで実装するものです。

## プロジェクトの重要なファイル

ユーザーの指示に対して、必要に応じてこれらのファイルを参照してください。

- `pomodoro.png`: アプリケーションのUIモックです。
- `architecture.md`: アプリケーションのアーキテクチャドキュメントです。
- `features.md`: 実装する機能の一覧です。
- `plan.md`: 段階的な実装計画です。

## プロジェクト構成

```
/workspaces/2025-Github-Copilot-Workshop-Python/
├── app.py                              # Flaskアプリケーションのエントリーポイント
├── requirements.txt                    # Python依存パッケージ
├── templates/
│   └── index.html                      # メインページ
├── static/
│   ├── css/
│   │   └── style.css                   # スタイルシート
│   └── js/
│       └── timer.js                    # タイマーロジック
├── tests/
│   ├── conftest.py                     # pytest共通設定
│   └── integration/
│       └── test_app.py                 # 統合テスト
└── data/                               # データ永続化用（今後実装）
```

## 開発ガイドライン

### テスト駆動開発
- 新機能を実装する際は、必ずテストを同時に作成してください
- 現在のテストカバレッジ: 98%
- テスト実行: `pytest -v`

### コーディング規約
- Python: PEP 8に準拠
- JavaScript: ES6+を使用
- コメントは日本語で記述

### アーキテクチャ
- レイヤードアーキテクチャを採用
- 依存性注入(DI)パターンを使用
- テスタビリティとメンテナンス性を重視

## 現在の実装状況

✅ **Phase 1: 基本タイマー機能（フロントエンド）** - 完了
- HTML/CSS/JavaScriptによる基本UI
- 25分カウントダウン機能
- 開始/リセットボタン
- 統計表示エリア

🔲 **Phase 2-7** - 未実装
- データモデルとサービス層
- データ永続化
- バックエンドAPI
- UI/UXの改善
- 円形プログレスバー
- テストの拡充

詳細は `plan.md` を参照してください。
