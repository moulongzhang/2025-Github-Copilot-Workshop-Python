# 🍳 Kitchen Chaos Game - Python版

**キッチンカオスゲーム** - レシピ配達システムのPython実装

## 📋 概要 / Overview

このプロジェクトは、キッチン環境でレシピを管理し、料理を配達するゲームシステムのPython実装です。
Unityゲーム「Kitchen Chaos」のロジックをPythonに移植したものです。

This project is a Python implementation of a kitchen recipe management and delivery game system.
It's a Python port of the logic from the Unity game "Kitchen Chaos".

## ✨ 機能 / Features

### コアシステム / Core Systems
- 🎮 **ゲームマネージャー** - ゲーム状態の管理
- 📦 **配達マネージャー** - レシピの生成と配達処理
- 🍽️ **キッチンオブジェクト** - 料理の材料と皿の管理
- 📊 **レシピシステム** - レシピの定義と検証

### 拡張機能 / Extensions (Step 6)
- ⚙️ **設定マネージャー** - ゲーム設定のカスタマイズと永続化
- 🔔 **通知システム** - イベント通知とログ管理
- 🎨 **ビジュアルエフェクト** - カラフルなコンソール出力とアニメーション

## 🚀 使い方 / Usage

### 基本的な実行 / Basic Execution

```bash
# メインゲームを実行（統合デモ）
python3 main.py

# サンプルコード集を実行（各機能の個別デモ）
python3 examples.py

# 配達マネージャーのデモを実行
python3 deliverManager.py

# 設定マネージャーのデモを実行
python3 settings_manager.py

# 通知システムのデモを実行
python3 notification_system.py

# ビジュアルエフェクトのデモを実行
python3 visual_effects.py
```

### コード例 / Code Examples

#### 1. 基本的なゲームループ

```python
from deliverManager import KitchenGameManager, DeliveryManager, RecipeListSO, RecipeSO, KitchenObjectSO

# レシピを定義
tomato = KitchenObjectSO("Tomato", 1)
lettuce = KitchenObjectSO("Lettuce", 2)
sandwich_recipe = RecipeSO("Sandwich", [tomato, lettuce])
recipe_list = RecipeListSO([sandwich_recipe])

# ゲーム開始
game_manager = KitchenGameManager.get_instance()
game_manager.start_game()

# 配達マネージャーを初期化
delivery_manager = DeliveryManager.get_instance(recipe_list)
```

#### 2. 設定のカスタマイズ

```python
from settings_manager import SettingsManager

# 設定を取得
settings = SettingsManager.get_instance()

# 設定を変更
settings.set_setting("spawn_recipe_timer_max", 3.0)
settings.set_setting("enable_animations", True)

# 設定を保存
settings.save_settings()
```

#### 3. 通知システムの使用

```python
from notification_system import NotificationSystem, notify_success, notify_error

# 通知システムを初期化
notification_system = NotificationSystem.get_instance()

# 通知を送信
notify_success("レシピを配達しました！")
notify_error("配達に失敗しました")

# 通知を取得
recent_notifications = notification_system.get_recent_notifications(5)
```

#### 4. ビジュアルエフェクトの使用

```python
from visual_effects import VisualEffects, Color

# カラフルなメッセージを表示
VisualEffects.print_success("配達成功！")
VisualEffects.print_error("配達失敗...")

# プログレスバーを表示
for i in range(11):
    VisualEffects.print_progress_bar(i / 10, label="料理中")
    time.sleep(0.2)
```

## 📁 ファイル構成 / File Structure

```
.
├── README.md                   # このファイル / This file
├── main.py                     # メインエントリーポイント / Main entry point
├── examples.py                 # サンプルコード集 / Example code collection
├── deliverManager.py           # 配達マネージャー / Delivery manager
├── point.py                    # 2D座標クラス / 2D point class
├── settings_manager.py         # 設定管理 / Settings management
├── notification_system.py      # 通知システム / Notification system
├── visual_effects.py           # ビジュアルエフェクト / Visual effects
├── API_DOCUMENTATION.md        # APIドキュメント / API documentation
└── game_settings.json          # ゲーム設定ファイル / Game settings file (auto-generated)
```

## 🎨 ビジュアル機能 / Visual Features

- **カラーテキスト** - ANSI エスケープコードを使用した色付きテキスト
- **グラデーション** - 複数色を使用したグラデーションテキスト
- **プログレスバー** - 進行状況の可視化
- **スピナーアニメーション** - ローディング表示
- **ボックス装飾** - テキストをボックスで装飾
- **ステータスアイコン** - 成功/エラー/警告/情報アイコン

## ⚙️ 設定項目 / Configuration Options

| 設定項目 | デフォルト値 | 説明 |
|---------|------------|------|
| spawn_recipe_timer_max | 4.0 | レシピ生成間隔（秒） |
| waiting_recipes_max | 4 | 最大待機レシピ数 |
| game_duration | 60 | ゲーム時間（秒） |
| enable_colors | True | カラー表示の有効化 |
| enable_animations | True | アニメーションの有効化 |
| enable_notifications | True | 通知の有効化 |
| notification_level | "all" | 通知レベル（all/important/none） |
| debug_mode | False | デバッグモード |

## 🔔 通知レベル / Notification Levels

- **INFO** - 一般的な情報メッセージ
- **SUCCESS** - 成功メッセージ
- **WARNING** - 警告メッセージ
- **ERROR** - エラーメッセージ

## 📝 開発ノート / Development Notes

このプロジェクトはGitHub Copilotワークショップの一環として開発されました。

### ステップ6の実装内容 / Step 6 Implementation
1. ✅ デザイン微調整 - カラー、グラデーション、アニメーション
2. ✅ 設定画面の土台 - 設定マネージャーとJSON設定ファイル
3. ✅ 通知機能の土台 - イベント通知システムとサブスクリプション
4. ✅ ドキュメント整備 - README、コード内コメント、使用例

## 🔗 参考リンク / References

- ワークショップの手順：https://moulongzhang.github.io/2025-Github-Copilot-Workshop/github-copilot-workshop/#0

## 📄 ライセンス / License

このプロジェクトはワークショップ用の教材です。

---

**Enjoy Cooking! 🍳🍕**
