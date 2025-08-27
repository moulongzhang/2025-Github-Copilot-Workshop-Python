# ポモドーロタイマーWebアプリケーション アーキテクチャ案

## 1. 概要
Flask（Python）とHTML/CSS/JavaScriptを用いたポモドーロタイマーWebアプリの設計方針。

## 2. 構成
- **バックエンド**: Flask
  - タイマー状態管理（必要に応じて）、API提供、静的ファイル配信
- **フロントエンド**: HTML/CSS/JavaScript
  - UI表示、タイマー操作、必要に応じてAPI通信

## 3. ディレクトリ構成例
```
/2025-Github-Copilot-Workshop-Python/
├── app.py                # Flaskアプリ本体
├── routes.py             # ルーティング・API定義
├── pomodoro.py           # タイマー管理ロジック
├── templates/
│   └── index.html        # メイン画面
├── static/
│   ├── css/
│   │   └── style.css     # スタイル
│   ├── js/
│   │   └── timer.js      # タイマー制御JS
│   └── img/
│       └── pomodoro.png  # UI画像
├── tests/
│   ├── test_pomodoro.py  # タイマーロジックのテスト
│   └── test_routes.py    # APIのテスト
└── README.md
```

## 4. ユニットテスト容易化のための工夫
- Flaskインスタンスとルーティング・ロジックの分離
- タイマーのロジックをPythonクラス/関数として分離
- テスト用ディレクトリ・ファイルの追加
- `pytest`等のテストフレームワーク導入
- フロントエンドJSは関数化し、Jest等でテスト可能な構造に

## 5. 実装の流れ
1. Flaskで基本画面表示（index.html）を実装
2. HTML/CSSでUIを再現
3. JavaScriptでタイマー機能を実装
4. 必要に応じてAPI・DB連携を追加
5. 各モジュールのユニットテストを作成

## 6. 拡張性・保守性
- ロジックとWeb部分の分離（テスト容易化・保守性向上）
- 履歴やユーザー設定保存はAPI＋DB（SQLite等）で拡張可能
- UI/ロジックの分離（MVC的設計）

---
このアーキテクチャにより、シンプルかつ拡張・保守・テストが容易なWebアプリケーション開発が可能です。
