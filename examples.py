"""
サンプルコード集 - 各機能の使用例
Example Code Collection - Usage examples for each feature

このファイルには、プロジェクトの主要機能のサンプルコードが含まれています。
"""


def example_1_basic_game():
    """例1: 基本的なゲームの実行 / Example 1: Basic game execution"""
    print("\n=== 例1: 基本的なゲームの実行 ===\n")
    
    import time
    from deliverManager import (
        KitchenGameManager, DeliveryManager, RecipeListSO, 
        RecipeSO, KitchenObjectSO, PlateKitchenObject
    )
    
    # レシピデータの作成
    tomato = KitchenObjectSO("Tomato", 1)
    lettuce = KitchenObjectSO("Lettuce", 2)
    sandwich = RecipeSO("Sandwich", [tomato, lettuce])
    recipe_list = RecipeListSO([sandwich])
    
    # ゲーム開始
    game_manager = KitchenGameManager.get_instance()
    game_manager.start_game()
    
    # 配達マネージャーを初期化
    delivery_manager = DeliveryManager.get_instance(recipe_list)
    
    # イベントハンドラーを設定
    delivery_manager.on_recipe_success.add_handler(
        lambda s, a: print("✓ 配達成功！")
    )
    
    # ゲームループ（3秒間）
    print("ゲームを実行中...")
    start_time = time.time()
    while time.time() - start_time < 3:
        delivery_manager.update()
        time.sleep(0.5)
    
    # レシピを配達
    plate = PlateKitchenObject()
    plate.add_kitchen_object(tomato)
    plate.add_kitchen_object(lettuce)
    delivery_manager.deliver_recipe(plate)
    
    print(f"成功数: {delivery_manager.get_successful_recipes_amount()}")
    game_manager.stop_game()


def example_2_settings_manager():
    """例2: 設定マネージャーの使用 / Example 2: Using settings manager"""
    print("\n=== 例2: 設定マネージャーの使用 ===\n")
    
    from settings_manager import SettingsManager
    
    # 設定マネージャーを取得
    settings = SettingsManager.get_instance()
    
    # 現在の設定を表示
    print("現在の設定:")
    for key, value in settings.get_all_settings().items():
        print(f"  {key}: {value}")
    
    # 設定を変更
    print("\n設定を変更...")
    settings.set_setting("spawn_recipe_timer_max", 2.5)
    settings.set_setting("enable_animations", True)
    
    # 変更後の設定を表示
    print(f"spawn_recipe_timer_max: {settings.get_setting('spawn_recipe_timer_max')}")
    print(f"enable_animations: {settings.get_setting('enable_animations')}")
    
    # 設定を保存（コメントアウト：実際のファイルを作成しないため）
    # settings.save_settings()


def example_3_notification_system():
    """例3: 通知システムの使用 / Example 3: Using notification system"""
    print("\n=== 例3: 通知システムの使用 ===\n")
    
    from notification_system import (
        NotificationSystem, notify_info, notify_success, 
        notify_warning, notify_error
    )
    
    # 通知システムを取得
    notification_system = NotificationSystem.get_instance()
    
    # 通知の購読
    def print_notification(notification):
        print(f"  → {notification}")
    
    notification_system.subscribe(print_notification)
    
    # 各種通知を送信
    print("通知を送信:")
    notify_info("ゲームを開始しました", "game")
    notify_success("レシピを配達しました", "delivery")
    notify_warning("時間が残り少なくなっています", "timer")
    notify_error("配達に失敗しました", "delivery")
    
    # 統計を表示
    print(f"\n総通知数: {notification_system.get_notification_count()}")
    
    # カテゴリ別の通知を取得
    delivery_notifications = notification_system.get_notifications(category="delivery")
    print(f"配達関連の通知数: {len(delivery_notifications)}")
    
    # クリーンアップ
    notification_system.clear_notifications()


def example_4_visual_effects():
    """例4: ビジュアルエフェクトの使用 / Example 4: Using visual effects"""
    print("\n=== 例4: ビジュアルエフェクトの使用 ===\n")
    
    import time
    from visual_effects import VisualEffects, Color
    
    # カラーテキスト
    print("カラーテキスト:")
    print(VisualEffects.colorize("  赤色のテキスト", Color.RED))
    print(VisualEffects.colorize("  緑色のテキスト", Color.GREEN, bold=True))
    print(VisualEffects.colorize("  青色のテキスト", Color.BLUE, underline=True))
    
    # グラデーション
    print("\nグラデーション:")
    colors = [Color.RED, Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE]
    print(VisualEffects.gradient_text("  Kitchen Chaos Game", colors))
    
    # ボックス
    print("\nボックス:")
    VisualEffects.print_box("ゲーム開始！", Color.CYAN)
    
    # ステータスメッセージ
    print("\nステータスメッセージ:")
    VisualEffects.print_success("配達成功")
    VisualEffects.print_error("配達失敗")
    VisualEffects.print_warning("時間切れ")
    VisualEffects.print_info("新しいレシピ")
    
    # プログレスバー
    print("\nプログレスバー:")
    for i in range(6):
        VisualEffects.print_progress_bar(i / 5, label="料理中", color=Color.GREEN)
        time.sleep(0.3)


def example_5_integrated():
    """例5: 統合された例 / Example 5: Integrated example"""
    print("\n=== 例5: 統合された例 ===\n")
    
    import time
    from deliverManager import (
        KitchenGameManager, DeliveryManager, RecipeListSO, 
        RecipeSO, KitchenObjectSO
    )
    from settings_manager import SettingsManager
    from notification_system import notify_info, notify_success
    from visual_effects import VisualEffects, Color
    
    # 設定を取得
    settings = SettingsManager.get_instance()
    enable_colors = settings.get_setting("enable_colors")
    
    # タイトル表示
    if enable_colors:
        colors = [Color.RED, Color.YELLOW, Color.GREEN, Color.CYAN]
        print(VisualEffects.gradient_text("Kitchen Chaos Demo", colors))
    
    # レシピデータ
    tomato = KitchenObjectSO("🍅 Tomato", 1)
    bread = KitchenObjectSO("🍞 Bread", 2)
    sandwich = RecipeSO("🥪 Sandwich", [bread, tomato])
    recipe_list = RecipeListSO([sandwich])
    
    # ゲーム開始
    game_manager = KitchenGameManager.get_instance()
    game_manager.start_game()
    notify_info("ゲームを開始しました", "game")
    
    # 配達マネージャー
    delivery_manager = DeliveryManager.get_instance(recipe_list)
    
    # イベント設定
    delivery_manager.on_recipe_success.add_handler(
        lambda s, a: notify_success("レシピ配達成功！", "delivery")
    )
    
    # 短いゲームループ
    print("\nゲーム実行中...")
    for i in range(3):
        delivery_manager.update()
        time.sleep(0.5)
    
    # 結果表示
    waiting = len(delivery_manager.get_waiting_recipe_so_list())
    successful = delivery_manager.get_successful_recipes_amount()
    
    result = f"待機: {waiting}件 | 成功: {successful}回"
    VisualEffects.print_box(result, Color.BRIGHT_CYAN)
    
    game_manager.stop_game()


def example_6_point2d():
    """例6: Point2Dクラスの使用 / Example 6: Using Point2D class"""
    print("\n=== 例6: Point2Dクラスの使用 ===\n")
    
    from point import Point2D
    
    # 点を作成
    p1 = Point2D(0, 0)
    p2 = Point2D(3, 4)
    p3 = Point2D(6, 8)
    
    print(f"点1: {p1}")
    print(f"点2: {p2}")
    print(f"点3: {p3}")
    
    # 距離を計算
    dist_12 = p1.distance_to(p2)
    dist_23 = p2.distance_to(p3)
    
    print(f"\n点1から点2までの距離: {dist_12:.2f}")
    print(f"点2から点3までの距離: {dist_23:.2f}")


def main():
    """すべての例を実行 / Run all examples"""
    print("=" * 60)
    print("キッチンカオスゲーム - サンプルコード集")
    print("Kitchen Chaos Game - Example Code Collection")
    print("=" * 60)
    
    examples = [
        ("基本的なゲーム", example_1_basic_game),
        ("設定マネージャー", example_2_settings_manager),
        ("通知システム", example_3_notification_system),
        ("ビジュアルエフェクト", example_4_visual_effects),
        ("統合された例", example_5_integrated),
        ("Point2Dクラス", example_6_point2d),
    ]
    
    print("\n実行する例を選択してください:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  0. すべて実行")
    
    try:
        choice = input("\n選択 (0-6): ").strip()
        choice = int(choice) if choice else 0
        
        if choice == 0:
            for name, func in examples:
                func()
        elif 1 <= choice <= len(examples):
            examples[choice - 1][1]()
        else:
            print("無効な選択です")
    except (ValueError, KeyboardInterrupt):
        print("\n中断しました")
    except Exception as e:
        print(f"エラー: {e}")


if __name__ == "__main__":
    main()
