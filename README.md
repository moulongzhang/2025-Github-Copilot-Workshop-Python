# 🍅 ポモドーロタイマーアプリケーション

高機能なポモドーロテクニックタイマーWebアプリケーションです。

## 🌟 主な機能

- **ポモドーロタイマー**: 25分作業 + 5分休憩の集中管理
- **カスタマイズ可能**: 作業時間・休憩時間の調整
- **統計・履歴**: 完了したポモドーロの記録と分析
- **通知機能**: タイマー完了時の音声・ブラウザ通知
- **レスポンシブデザイン**: PC・モバイル対応

## 🚀 クイックスタート

### サーバー起動（簡単な方法）
```bash
./server_manager.sh start
```

### サーバー管理コマンド
```bash
# サーバー状態確認
./server_manager.sh status

# サーバー停止
./server_manager.sh stop

# サーバー再起動
./server_manager.sh restart

# ログ確認
./server_manager.sh logs
```

### 手動でサーバー起動する場合
```bash
# インタラクティブモード（ログがコンソールに表示）
./start_server.sh

# または直接実行
.venv/bin/python app.py
```

## 🌐 アクセスURL

サーバー起動後、以下のURLでアクセスできます：
- **ローカル**: http://127.0.0.1:8000
- **ネットワーク**: http://10.0.3.246:8000

## 🏗️ 技術仕様

- **フレームワーク**: Flask (Python)
- **フロントエンド**: HTML5, CSS3, JavaScript (Vanilla)
- **データ保存**: JSON ファイル + LocalStorage
- **テスト**: pytest (25個の包括的テスト)
- **UI**: レスポンシブデザイン

## 🧪 テスト実行

```bash
# 全テスト実行
.venv/bin/python -m pytest tests/ -v

# カバレッジ付きテスト実行
.venv/bin/python -m pytest tests/ --cov=. --cov-report=html
```

## 📁 プロジェクト構造

```
├── app.py                    # メインFlaskアプリケーション
├── server_manager.sh         # サーバー管理スクリプト
├── start_server.sh          # サーバー起動スクリプト
├── services/
│   └── timer_service.py     # ビジネスロジック
├── templates/
│   └── index.html           # メインHTML
├── static/
│   ├── css/style.css        # スタイルシート
│   └── js/timer.js          # JavaScript
└── tests/                   # テストファイル
    ├── test_app.py
    ├── test_static_files.py
    └── test_timer_service.py
```

## 🎯 使用方法

1. **サーバー起動**: `./server_manager.sh start`
2. **ブラウザでアクセス**: http://127.0.0.1:8000
3. **▶ スタートボタン**でタイマー開始
4. **⚙️ 設定ボタン**で時間をカスタマイズ
5. **📊 履歴・統計ボタン**で進捗確認

---

ワークショップの手順：https://moulongzhang.github.io/2025-Github-Copilot-Workshop/github-copilot-workshop/#0
