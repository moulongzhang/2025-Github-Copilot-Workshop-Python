# 🔧 API ドキュメント / API Documentation

キッチンカオスゲームのPython実装のAPIリファレンスです。

## 📦 モジュール一覧 / Module List

### 1. deliverManager.py

配達システムの中核となるモジュールです。

#### クラス / Classes

##### `KitchenObjectSO`
キッチンオブジェクト（材料や料理）を表すデータクラス。

**属性:**
- `name: str` - オブジェクト名
- `object_id: int` - 一意の識別子

**例 / Example:**
```python
tomato = KitchenObjectSO("Tomato", 1)
bread = KitchenObjectSO("Bread", 2)
```

##### `RecipeSO`
レシピを表すデータクラス。必要な材料のリストを含みます。

**属性:**
- `name: str` - レシピ名
- `kitchen_object_so_list: List[KitchenObjectSO]` - 必要な材料リスト

**例 / Example:**
```python
sandwich = RecipeSO("Sandwich", [bread, tomato, lettuce])
```

##### `RecipeListSO`
複数のレシピをまとめて管理するクラス。

**属性:**
- `recipe_so_list: List[RecipeSO]` - レシピリスト

##### `PlateKitchenObject`
皿に載せられた材料を管理するクラス。

**メソッド:**
- `add_kitchen_object(kitchen_object: KitchenObjectSO)` - 材料を追加
- `get_kitchen_object_so_list() -> List[KitchenObjectSO]` - 材料リストを取得

**例 / Example:**
```python
plate = PlateKitchenObject()
plate.add_kitchen_object(tomato)
plate.add_kitchen_object(bread)
```

##### `KitchenGameManager`
ゲーム全体の状態を管理するSingletonクラス。

**メソッド:**
- `get_instance() -> KitchenGameManager` - インスタンスを取得
- `is_game_playing() -> bool` - ゲームが進行中かチェック
- `start_game()` - ゲームを開始
- `stop_game()` - ゲームを停止

##### `DeliveryManager`
レシピの生成と配達を管理するSingletonクラス。

**イベント:**
- `on_recipe_spawned` - レシピが生成された時
- `on_recipe_completed` - レシピが完了した時
- `on_recipe_success` - 配達が成功した時
- `on_recipe_failed` - 配達が失敗した時

**メソッド:**
- `get_instance(recipe_list_so: RecipeListSO) -> DeliveryManager` - インスタンスを取得
- `update()` - フレーム更新処理（定期的に呼び出す必要あり）
- `deliver_recipe(plate_kitchen_object: PlateKitchenObject)` - レシピを配達
- `get_waiting_recipe_so_list() -> List[RecipeSO]` - 待機中のレシピリストを取得
- `get_successful_recipes_amount() -> int` - 成功した配達数を取得

**例 / Example:**
```python
# 初期化
recipe_list = RecipeListSO([sandwich, salad])
manager = DeliveryManager.get_instance(recipe_list)

# イベントハンドラーを設定
def on_success(sender, args):
    print("配達成功！")
manager.on_recipe_success.add_handler(on_success)

# ゲームループで更新
while game_running:
    manager.update()
    time.sleep(0.1)
```

---

### 2. settings_manager.py

ゲーム設定を管理するモジュールです。

#### クラス / Classes

##### `GameSettings`
ゲーム設定を保持するデータクラス。

**属性:**
- `spawn_recipe_timer_max: float = 4.0` - レシピ生成間隔（秒）
- `waiting_recipes_max: int = 4` - 最大待機レシピ数
- `game_duration: int = 60` - ゲーム時間（秒）
- `enable_colors: bool = True` - カラー表示の有効化
- `enable_animations: bool = True` - アニメーションの有効化
- `enable_sound_effects: bool = False` - 音響効果の有効化
- `enable_notifications: bool = True` - 通知の有効化
- `notification_level: str = "all"` - 通知レベル
- `debug_mode: bool = False` - デバッグモード
- `verbose_logging: bool = False` - 詳細ログ

##### `SettingsManager`
設定を管理するSingletonクラス。JSON形式で設定を永続化します。

**メソッド:**
- `get_instance() -> SettingsManager` - インスタンスを取得
- `get_setting(key: str) -> Any` - 設定値を取得
- `set_setting(key: str, value: Any)` - 設定値を更新
- `get_all_settings() -> Dict[str, Any]` - すべての設定を取得
- `save_settings()` - 設定をファイルに保存
- `reset_to_defaults()` - 設定をデフォルトに戻す

**例 / Example:**
```python
settings = SettingsManager.get_instance()

# 設定を変更
settings.set_setting("spawn_recipe_timer_max", 3.0)
settings.set_setting("enable_animations", True)

# 設定を保存
settings.save_settings()

# 設定を取得
timer = settings.get_setting("spawn_recipe_timer_max")
```

---

### 3. notification_system.py

イベント通知システムを提供するモジュールです。

#### Enum / Enumerations

##### `NotificationLevel`
通知のレベルを定義。
- `INFO` - 情報
- `SUCCESS` - 成功
- `WARNING` - 警告
- `ERROR` - エラー

#### クラス / Classes

##### `Notification`
通知データを表すデータクラス。

**属性:**
- `message: str` - 通知メッセージ
- `level: NotificationLevel` - 通知レベル
- `timestamp: datetime` - タイムスタンプ
- `category: str` - カテゴリ

##### `NotificationSystem`
通知を管理するSingletonクラス。

**メソッド:**
- `get_instance() -> NotificationSystem` - インスタンスを取得
- `add_notification(message: str, level: NotificationLevel, category: str)` - 通知を追加
- `subscribe(callback: Callable)` - 通知の購読を登録
- `unsubscribe(callback: Callable)` - 通知の購読を解除
- `get_notifications(level: Optional[NotificationLevel], category: Optional[str]) -> List[Notification]` - 通知を取得
- `get_recent_notifications(count: int) -> List[Notification]` - 最新の通知を取得
- `clear_notifications()` - すべての通知をクリア

#### 便利関数 / Convenience Functions

- `notify_info(message: str, category: str)` - 情報通知
- `notify_success(message: str, category: str)` - 成功通知
- `notify_warning(message: str, category: str)` - 警告通知
- `notify_error(message: str, category: str)` - エラー通知

**例 / Example:**
```python
from notification_system import notify_success, NotificationSystem

# 通知を送信
notify_success("レシピを配達しました！", "delivery")

# 通知を購読
system = NotificationSystem.get_instance()
def print_notification(notif):
    print(f"{notif.level}: {notif.message}")
system.subscribe(print_notification)
```

---

### 4. visual_effects.py

コンソール出力の視覚的強化を提供するモジュールです。

#### Enum / Enumerations

##### `Color`
ANSIカラーコードを定義。基本色、明るい色、背景色、スタイルが含まれます。

**主要な色:**
- `RED`, `GREEN`, `BLUE`, `YELLOW`, `CYAN`, `MAGENTA`, `WHITE`
- `BRIGHT_RED`, `BRIGHT_GREEN`, `BRIGHT_BLUE` など
- `BOLD`, `UNDERLINE`, `BLINK`, `REVERSE`
- `RESET` - 色とスタイルをリセット

#### クラス / Classes

##### `VisualEffects`
視覚効果を提供する静的メソッドクラス。

**メソッド:**

- `colorize(text: str, color: Color, bg_color: Optional[Color], bold: bool, underline: bool) -> str`
  - テキストに色とスタイルを適用

- `gradient_text(text: str, colors: list) -> str`
  - グラデーションテキストを作成

- `print_with_animation(text: str, delay: float, color: Optional[Color])`
  - アニメーション付きでテキストを表示

- `print_box(text: str, color: Color, padding: int)`
  - テキストをボックスで囲んで表示

- `print_progress_bar(progress: float, width: int, color: Color, label: str)`
  - プログレスバーを表示

- `print_spinner(message: str, duration: float)`
  - スピナーアニメーションを表示

- `print_banner(text: str, char: str, color: Color)`
  - バナーを表示

- `print_success(message: str)`
  - 成功メッセージを表示（✓マーク付き）

- `print_error(message: str)`
  - エラーメッセージを表示（✗マーク付き）

- `print_warning(message: str)`
  - 警告メッセージを表示（⚠マーク付き）

- `print_info(message: str)`
  - 情報メッセージを表示（ℹマーク付き）

**例 / Example:**
```python
from visual_effects import VisualEffects, Color

# カラフルなメッセージ
VisualEffects.print_success("配達成功！")
VisualEffects.print_error("配達失敗...")

# プログレスバー
for i in range(11):
    VisualEffects.print_progress_bar(i / 10, label="料理中")
    time.sleep(0.2)

# ボックス表示
VisualEffects.print_box("ゲーム開始！", Color.CYAN)

# グラデーション
colors = [Color.RED, Color.YELLOW, Color.GREEN]
print(VisualEffects.gradient_text("Kitchen Chaos", colors))
```

---

### 5. point.py

2D座標を扱うシンプルなモジュールです。

#### クラス / Classes

##### `Point2D`
2次元座標を表すクラス。

**属性:**
- `x: float` - X座標
- `y: float` - Y座標

**メソッド:**
- `distance_to(other: Point2D) -> float` - 他の点との距離を計算
- `__str__() -> str` - 文字列表現

**例 / Example:**
```python
p1 = Point2D(0, 0)
p2 = Point2D(3, 4)
distance = p1.distance_to(p2)  # 5.0
print(p1)  # Point2D(0, 0)
```

---

## 🔄 統合例 / Integration Example

すべてのモジュールを統合した完全な例：

```python
import time
from deliverManager import *
from settings_manager import SettingsManager
from notification_system import *
from visual_effects import VisualEffects, Color

# 設定を読み込み
settings = SettingsManager.get_instance()

# 通知システムを初期化
notification_system = NotificationSystem.get_instance()
notification_system.subscribe(lambda n: print(n))

# レシピを定義
tomato = KitchenObjectSO("Tomato", 1)
bread = KitchenObjectSO("Bread", 2)
sandwich = RecipeSO("Sandwich", [bread, tomato])
recipe_list = RecipeListSO([sandwich])

# ゲームを開始
game_manager = KitchenGameManager.get_instance()
game_manager.start_game()

# 配達マネージャーを初期化
delivery_manager = DeliveryManager.get_instance(recipe_list)
delivery_manager.on_recipe_success.add_handler(
    lambda s, a: VisualEffects.print_success("配達成功！")
)

# ゲームループ
for i in range(10):
    delivery_manager.update()
    time.sleep(0.5)

game_manager.stop_game()
```

---

## 📝 注意事項 / Notes

- Singletonクラス（`KitchenGameManager`, `DeliveryManager`, `SettingsManager`, `NotificationSystem`）は最初の取得時に初期化されます
- `DeliveryManager.update()` は定期的に呼び出す必要があります（ゲームループ内で）
- 視覚効果はANSIエスケープコードを使用するため、対応していない環境では正しく表示されない場合があります
- 設定ファイル `game_settings.json` は自動的に作成・更新されます

---

**Happy Coding! 🍳**
