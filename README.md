ワークショップの手順：https://moulongzhang.github.io/20250708-Github-Copilot-Workshop/github-copilot-workshop/#13

# 🍅 ポモドーロタイマーWebアプリ

美しいUIと進捗記録機能を持つポモドーロタイマーWebアプリケーションです。

## 📁 プロジェクト構成

```
project_root/
├── app.py                    # Flaskアプリ本体
├── pomodoro_timer.py         # タイマーロジック（Phase 1で実装予定）
├── test_pomodoro_timer.py    # ユニットテスト（Phase 1で実装予定）
├── requirements.txt          # 依存関係
├── static/
│   ├── css/
│   │   └── style.css         # UI用CSS
│   ├── js/
│   │   └── timer.js          # タイマー・UI制御用JS
│   └── audio/
│       └── (通知音ファイル)   # Phase 5で追加予定
├── templates/
│   └── index.html            # メイン画面テンプレート
├── data/
│   └── (データベースファイル) # Phase 4で追加予定
├── docs/
│   ├── architecture.md       # アーキテクチャ設計
│   ├── features.md           # 機能一覧
│   └── plan.md               # 実装計画
└── old_files/                # 既存ファイルの一時保管
```

## 🚀 セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. アプリケーションの起動

```bash
python app.py
```

### 3. ブラウザでアクセス

```
http://localhost:5000
```

## 📋 実装予定

詳細な実装計画は `docs/plan.md` を参照してください。

### Phase 1: 基盤構築
- [ ] タイマーロジッククラス実装
- [ ] ユニットテスト実装
- [ ] Flaskアプリ基本構成

### Phase 2: 最小限のUI
- [ ] 基本的なWebアプリケーション
- [ ] タイマー機能の動作確認

### Phase 3: UI強化
- [ ] 円形プログレスバー
- [ ] 美しいデザイン適用

### Phase 4: 進捗記録
- [ ] セッション記録機能
- [ ] データ永続化

### Phase 5: 実用機能
- [ ] 通知機能
- [ ] 設定機能

## 🛠️ 開発

### テスト実行

```bash
pytest
```

### テストカバレッジ確認

```bash
pytest --cov=pomodoro_timer
```

## 📖 ドキュメント

- [アーキテクチャ設計](docs/architecture.md)
- [機能一覧](docs/features.md)
- [実装計画](docs/plan.md)

## 🎯 目標

- テスト駆動開発による高品質なコード
- 美しく使いやすいUI
- 段階的な機能実装
- 拡張性の高いアーキテクチャ

