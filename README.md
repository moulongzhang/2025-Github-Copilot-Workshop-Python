# 🍅 Pomodoro Timer

生産性を向上させるためのシンプルで効果的なポモドーロタイマーWebアプリケーション

## 📖 概要

ポモドーロテクニックは、25分の作業セッションと短い休憩を交互に繰り返す時間管理法です。
このアプリケーションは、そのテクニックを実践するための使いやすいタイマーを提供します。

### 主な機能

- ⏱️ カスタマイズ可能なタイマー（作業・休憩時間）
- 📊 セッション履歴と統計
- 🔔 音声・デスクトップ通知
- 📱 PWA対応（オフライン動作、インストール可能）
- ♿ アクセシビリティ対応
- 🌓 ライト/ダークモード

## 🚀 クイックスタート

### 前提条件

- Python 3.11以上
- Redis（セッション管理に使用）

### インストール

1. **リポジトリのクローン**
```bash
git clone https://github.com/moulongzhang/2025-Github-Copilot-Workshop-Python.git
cd 2025-Github-Copilot-Workshop-Python
```

2. **仮想環境の作成と有効化**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **依存関係のインストール**
```bash
pip install -r requirements.txt
```

4. **環境変数の設定**
```bash
cp .env.example .env
# .envファイルを編集して必要な設定を行う
```

5. **アプリケーションの起動**
```bash
python run.py
```

6. **ブラウザでアクセス**
```
http://localhost:5000
```

## 🏗️ プロジェクト構成

```
pomodoro-timer/
├── app/
│   ├── __init__.py           # アプリケーションファクトリ
│   ├── models/               # データモデル（ORMクラス）
│   ├── routes/               # ルート（Blueprints）
│   ├── services/             # ビジネスロジック
│   ├── repositories/         # データアクセス層
│   ├── static/               # 静的ファイル（CSS, JS, 画像）
│   │   ├── css/
│   │   ├── js/
│   │   └── assets/
│   └── templates/            # Jinjaテンプレート
├── tests/                    # テストコード
│   ├── unit/                 # ユニットテスト
│   └── integration/          # 統合テスト
├── migrations/               # データベースマイグレーション
├── docs/                     # ドキュメント
├── examples/                 # 旧ファイル・サンプルコード
├── .env.example              # 環境変数テンプレート
├── .gitignore
├── pytest.ini                # pytest設定
├── requirements.txt          # 本番依存関係
├── requirements-dev.txt      # 開発依存関係
├── run.py                    # 開発サーバー起動スクリプト
├── architecture.md           # アーキテクチャ設計書
├── features.md               # 機能一覧
├── plan.md                   # 実装計画
└── README.md                 # このファイル
```

## 📚 開発ドキュメント

- [architecture.md](architecture.md) - システムアーキテクチャ設計書
- [features.md](features.md) - 実装機能一覧とチェックリスト
- [plan.md](plan.md) - 段階的実装計画（Stage 0-7）

## 🧪 テスト

### テストの実行

```bash
# すべてのテストを実行
pytest

# カバレッジレポート付き
pytest --cov=app --cov-report=html

# 特定のテストマーカーのみ実行
pytest -m unit
pytest -m integration
```

### テストカバレッジ目標

- ユニットテスト: 80%以上
- 統合テスト: 70%以上

## 🛠️ 開発

### 開発環境のセットアップ

```bash
# 開発依存関係のインストール
pip install -r requirements-dev.txt

# コード品質チェック
black app tests          # フォーマット
flake8 app tests         # リント
mypy app                 # 型チェック
isort app tests          # import文の整理
```

### データベースマイグレーション

```bash
# マイグレーションファイルの作成
flask db migrate -m "説明"

# マイグレーションの適用
flask db upgrade

# マイグレーションのロールバック
flask db downgrade
```

## 📈 実装状況

| Stage | 内容 | ステータス |
|-------|------|-----------|
| **Stage 0** | プロジェクトセットアップ | ✅ 完了 |
| **Stage 1** | 最小限の動くタイマー | ⬜ 未着手 |
| **Stage 2** | バックエンドAPI | ⬜ 未着手 |
| **Stage 3** | DB・履歴機能 | ⬜ 未着手 |
| **Stage 4** | 統計・設定 | ⬜ 未着手 |
| **Stage 5** | 通知・セキュリティ | ⬜ 未着手 |
| **Stage 6** | PWA・A11y | ⬜ 未着手 |
| **Stage 7** | 最適化 | ⬜ 未着手 |

詳細は [plan.md](plan.md) を参照してください。

## 🤝 コントリビューション

プルリクエストを歓迎します！大きな変更の場合は、まずissueを開いて変更内容を議論してください。

### 開発フロー

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

MIT License

## 🙏 謝辞

- [Pomodoro Technique](https://francescocirillo.com/pages/pomodoro-technique) - Francesco Cirillo
- Flask Framework
- VS Code GitHub Copilot Workshop

---

**作成日**: 2025-12-16  
**最終更新日**: 2025-12-16  
**バージョン**: 0.1.0 (Stage 0)
