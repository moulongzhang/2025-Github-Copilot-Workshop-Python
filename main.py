"""
キッチンカオスゲーム - メインエントリーポイント
Kitchen Chaos Game - Main Entry Point

統合されたゲームシステムのデモンストレーション
"""
import time
from deliverManager import (
    KitchenGameManager, DeliveryManager, RecipeListSO, RecipeSO, 
    KitchenObjectSO, PlateKitchenObject
)
from settings_manager import SettingsManager
from notification_system import NotificationSystem, notify_info, notify_success, notify_error
from visual_effects import VisualEffects, Color


def setup_game():
    """ゲームの初期設定 / Initialize game"""
    # 設定を読み込み
    settings = SettingsManager.get_instance()
    
    # ビジュアル設定を取得
    enable_colors = settings.get_setting("enable_colors")
    enable_animations = settings.get_setting("enable_animations")
    
    # バナー表示
    if enable_colors:
        gradient_colors = [Color.RED, Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE, Color.MAGENTA]
        title = "🍳 Kitchen Chaos Game 🍕"
        print()
        print(VisualEffects.gradient_text(title, gradient_colors))
        print(VisualEffects.gradient_text("=" * len(title), gradient_colors))
        print()
    else:
        print("\n=== Kitchen Chaos Game ===\n")
    
    # レシピデータの作成
    tomato = KitchenObjectSO("Tomato 🍅", 1)
    lettuce = KitchenObjectSO("Lettuce 🥬", 2)
    bread = KitchenObjectSO("Bread 🍞", 3)
    cheese = KitchenObjectSO("Cheese 🧀", 4)
    
    # レシピの定義
    sandwich_recipe = RecipeSO("Sandwich 🥪", [bread, lettuce, tomato])
    salad_recipe = RecipeSO("Salad 🥗", [lettuce, tomato])
    cheeseburger_recipe = RecipeSO("Cheeseburger 🍔", [bread, cheese, tomato])
    
    recipe_list = RecipeListSO([sandwich_recipe, salad_recipe, cheeseburger_recipe])
    
    return recipe_list, settings


def setup_event_handlers(delivery_manager, notification_system):
    """イベントハンドラーの設定 / Setup event handlers"""
    
    def on_recipe_spawned(sender, args):
        waiting_recipes = delivery_manager.get_waiting_recipe_so_list()
        if waiting_recipes:
            recipe_name = waiting_recipes[-1].name
            message = f"新しいレシピ登場: {recipe_name}"
            notify_info(message, "recipe")
            VisualEffects.print_info(message)
    
    def on_recipe_success(sender, args):
        count = delivery_manager.get_successful_recipes_amount()
        message = f"配達成功！ 累計: {count}回"
        notify_success(message, "delivery")
        VisualEffects.print_success(message)
    
    def on_recipe_failed(sender, args):
        message = "配達失敗... 材料が間違っています"
        notify_error(message, "delivery")
        VisualEffects.print_error(message)
    
    # イベントハンドラーを登録
    delivery_manager.on_recipe_spawned.add_handler(on_recipe_spawned)
    delivery_manager.on_recipe_success.add_handler(on_recipe_success)
    delivery_manager.on_recipe_failed.add_handler(on_recipe_failed)


def display_game_status(delivery_manager, elapsed_time, game_duration):
    """ゲームステータスを表示 / Display game status"""
    waiting_recipes = delivery_manager.get_waiting_recipe_so_list()
    successful_count = delivery_manager.get_successful_recipes_amount()
    remaining_time = max(0, game_duration - elapsed_time)
    
    print()
    VisualEffects.print_box(
        f"時間: {remaining_time:.1f}秒 | 待機中: {len(waiting_recipes)}件 | 成功: {successful_count}回",
        Color.BRIGHT_CYAN
    )
    
    # 待機中のレシピを表示
    if waiting_recipes:
        print(VisualEffects.colorize("\n📋 待機中のレシピ:", Color.YELLOW, bold=True))
        for i, recipe in enumerate(waiting_recipes, 1):
            ingredients = ", ".join([obj.name for obj in recipe.kitchen_object_so_list])
            print(f"  {i}. {recipe.name} ({ingredients})")


def simulate_delivery(delivery_manager):
    """配達をシミュレート / Simulate delivery"""
    waiting_recipes = delivery_manager.get_waiting_recipe_so_list()
    
    if not waiting_recipes:
        VisualEffects.print_warning("配達するレシピがありません")
        return
    
    # 最初のレシピを配達してみる
    recipe_to_deliver = waiting_recipes[0]
    
    print(VisualEffects.colorize(f"\n🚚 配達準備中: {recipe_to_deliver.name}", Color.BRIGHT_YELLOW))
    
    # プログレスバーで配達の進行を表示
    for i in range(11):
        VisualEffects.print_progress_bar(i / 10, label="配達中", color=Color.CYAN)
        time.sleep(0.1)
    
    # 皿に材料を追加
    plate = PlateKitchenObject()
    for ingredient in recipe_to_deliver.kitchen_object_so_list:
        plate.add_kitchen_object(ingredient)
    
    # 配達を実行
    delivery_manager.deliver_recipe(plate)


def main():
    """メイン関数 / Main function"""
    # ゲームセットアップ
    recipe_list, settings = setup_game()
    
    # 通知システムを初期化
    notification_system = NotificationSystem.get_instance()
    
    # ゲーム設定を取得
    game_duration = settings.get_setting("game_duration")
    spawn_timer_max = settings.get_setting("spawn_recipe_timer_max")
    
    # ゲームマネージャーとデリバリーマネージャーを初期化
    game_manager = KitchenGameManager.get_instance()
    game_manager.start_game()
    
    delivery_manager = DeliveryManager.get_instance(recipe_list)
    delivery_manager._spawn_recipe_timer_max = spawn_timer_max  # 設定を適用
    
    # イベントハンドラーを設定
    setup_event_handlers(delivery_manager, notification_system)
    
    # ゲーム開始メッセージ
    notify_info("ゲームを開始します！", "game")
    VisualEffects.print_banner("ゲーム開始 / Game Start", color=Color.GREEN)
    print()
    
    # ゲームループ（デモ用に10秒間）
    demo_duration = 10
    start_time = time.time()
    last_status_time = start_time
    delivery_interval = 3.0  # 3秒ごとに配達を試みる
    last_delivery_time = start_time
    
    print(VisualEffects.colorize("レシピが自動生成されます... 3秒ごとに配達を試みます\n", Color.CYAN))
    
    while True:
        current_time = time.time()
        elapsed = current_time - start_time
        
        # デモ時間終了チェック
        if elapsed >= demo_duration:
            break
        
        # ゲーム更新
        delivery_manager.update()
        
        # ステータス表示（2秒ごと）
        if current_time - last_status_time >= 2.0:
            display_game_status(delivery_manager, elapsed, demo_duration)
            last_status_time = current_time
        
        # 配達を試みる（3秒ごと）
        if current_time - last_delivery_time >= delivery_interval:
            simulate_delivery(delivery_manager)
            last_delivery_time = current_time
        
        time.sleep(0.1)
    
    # ゲーム終了
    game_manager.stop_game()
    
    # 最終結果を表示
    print()
    VisualEffects.print_banner("ゲーム終了 / Game Over", color=Color.RED)
    
    successful_count = delivery_manager.get_successful_recipes_amount()
    result_message = f"成功した配達数: {successful_count}回\nTotal successful deliveries: {successful_count}"
    VisualEffects.print_box(result_message, Color.BRIGHT_GREEN, padding=3)
    
    # 通知の統計
    print(VisualEffects.colorize("\n📊 通知統計:", Color.MAGENTA, bold=True))
    print(f"  総通知数: {notification_system.get_notification_count()}件")
    
    # 最近の通知を表示
    print(VisualEffects.colorize("\n📝 最近の通知:", Color.CYAN, bold=True))
    recent_notifications = notification_system.get_recent_notifications(5)
    for notif in recent_notifications:
        print(f"  {notif}")
    
    print(VisualEffects.colorize("\n\n✨ ゲームを楽しんでいただきありがとうございました！ ✨", Color.BRIGHT_YELLOW, bold=True))
    print(VisualEffects.colorize("Thank you for playing!\n", Color.BRIGHT_YELLOW))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nゲームを中断しました / Game interrupted")
    except Exception as e:
        VisualEffects.print_error(f"エラーが発生しました / Error occurred: {e}")
        raise
