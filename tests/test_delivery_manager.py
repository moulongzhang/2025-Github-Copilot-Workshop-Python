"""
Unit tests for DeliveryManager and related classes
"""
import unittest
import time
from deliverManager import (
    Event,
    EventArgs,
    KitchenObjectSO,
    RecipeSO,
    RecipeListSO,
    PlateKitchenObject,
    KitchenGameManager,
    DeliveryManager
)


class TestEvent(unittest.TestCase):
    """Eventクラスのテストケース"""
    
    def test_add_handler(self):
        """イベントハンドラー追加のテスト"""
        event = Event()
        handler_called = []
        
        def handler(sender, args):
            handler_called.append(True)
        
        event.add_handler(handler)
        event.invoke(self)
        self.assertEqual(len(handler_called), 1)
    
    def test_remove_handler(self):
        """イベントハンドラー削除のテスト"""
        event = Event()
        handler_called = []
        
        def handler(sender, args):
            handler_called.append(True)
        
        event.add_handler(handler)
        event.remove_handler(handler)
        event.invoke(self)
        self.assertEqual(len(handler_called), 0)
    
    def test_multiple_handlers(self):
        """複数のハンドラーのテスト"""
        event = Event()
        call_count = []
        
        def handler1(sender, args):
            call_count.append(1)
        
        def handler2(sender, args):
            call_count.append(2)
        
        event.add_handler(handler1)
        event.add_handler(handler2)
        event.invoke(self)
        self.assertEqual(len(call_count), 2)
        self.assertIn(1, call_count)
        self.assertIn(2, call_count)
    
    def test_duplicate_handler(self):
        """重複ハンドラーのテスト"""
        event = Event()
        call_count = []
        
        def handler(sender, args):
            call_count.append(1)
        
        event.add_handler(handler)
        event.add_handler(handler)  # 同じハンドラーを再度追加
        event.invoke(self)
        # 重複は追加されないので1回だけ呼ばれるはず
        self.assertEqual(len(call_count), 1)


class TestKitchenObjectSO(unittest.TestCase):
    """KitchenObjectSOのテストケース"""
    
    def test_creation(self):
        """オブジェクト作成のテスト"""
        obj = KitchenObjectSO("Tomato", 1)
        self.assertEqual(obj.name, "Tomato")
        self.assertEqual(obj.object_id, 1)
    
    def test_equality(self):
        """等価性のテスト"""
        obj1 = KitchenObjectSO("Tomato", 1)
        obj2 = KitchenObjectSO("Tomato", 1)
        # dataclassは自動的に__eq__を実装
        self.assertEqual(obj1, obj2)


class TestRecipeSO(unittest.TestCase):
    """RecipeSOのテストケース"""
    
    def test_creation_empty(self):
        """空のレシピ作成のテスト"""
        recipe = RecipeSO("Empty Recipe")
        self.assertEqual(recipe.name, "Empty Recipe")
        self.assertEqual(len(recipe.kitchen_object_so_list), 0)
    
    def test_creation_with_items(self):
        """材料ありレシピ作成のテスト"""
        tomato = KitchenObjectSO("Tomato", 1)
        lettuce = KitchenObjectSO("Lettuce", 2)
        recipe = RecipeSO("Salad", [tomato, lettuce])
        self.assertEqual(recipe.name, "Salad")
        self.assertEqual(len(recipe.kitchen_object_so_list), 2)


class TestPlateKitchenObject(unittest.TestCase):
    """PlateKitchenObjectのテストケース"""
    
    def test_add_kitchen_object(self):
        """キッチンオブジェクト追加のテスト"""
        plate = PlateKitchenObject()
        tomato = KitchenObjectSO("Tomato", 1)
        plate.add_kitchen_object(tomato)
        objects = plate.get_kitchen_object_so_list()
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0], tomato)
    
    def test_add_multiple_objects(self):
        """複数オブジェクト追加のテスト"""
        plate = PlateKitchenObject()
        tomato = KitchenObjectSO("Tomato", 1)
        lettuce = KitchenObjectSO("Lettuce", 2)
        plate.add_kitchen_object(tomato)
        plate.add_kitchen_object(lettuce)
        objects = plate.get_kitchen_object_so_list()
        self.assertEqual(len(objects), 2)
    
    def test_get_list_returns_copy(self):
        """リスト取得がコピーを返すことのテスト"""
        plate = PlateKitchenObject()
        tomato = KitchenObjectSO("Tomato", 1)
        plate.add_kitchen_object(tomato)
        
        objects1 = plate.get_kitchen_object_so_list()
        objects2 = plate.get_kitchen_object_so_list()
        
        # 異なるリストインスタンスであることを確認
        self.assertIsNot(objects1, objects2)
        # しかし内容は同じ
        self.assertEqual(objects1, objects2)


class TestKitchenGameManager(unittest.TestCase):
    """KitchenGameManagerのテストケース"""
    
    def setUp(self):
        """各テストの前にシングルトンをリセット"""
        KitchenGameManager._instance = None
    
    def test_singleton(self):
        """シングルトンパターンのテスト"""
        manager1 = KitchenGameManager.get_instance()
        manager2 = KitchenGameManager.get_instance()
        self.assertIs(manager1, manager2)
    
    def test_initial_state(self):
        """初期状態のテスト"""
        manager = KitchenGameManager.get_instance()
        self.assertFalse(manager.is_game_playing())
    
    def test_start_game(self):
        """ゲーム開始のテスト"""
        manager = KitchenGameManager.get_instance()
        manager.start_game()
        self.assertTrue(manager.is_game_playing())
    
    def test_stop_game(self):
        """ゲーム停止のテスト"""
        manager = KitchenGameManager.get_instance()
        manager.start_game()
        manager.stop_game()
        self.assertFalse(manager.is_game_playing())


class TestDeliveryManager(unittest.TestCase):
    """DeliveryManagerのテストケース"""
    
    def setUp(self):
        """各テストの前にシングルトンをリセット"""
        DeliveryManager._instance = None
        KitchenGameManager._instance = None
        
        # テスト用レシピリスト作成
        self.tomato = KitchenObjectSO("Tomato", 1)
        self.lettuce = KitchenObjectSO("Lettuce", 2)
        self.bread = KitchenObjectSO("Bread", 3)
        
        self.sandwich_recipe = RecipeSO("Sandwich", [self.bread, self.lettuce, self.tomato])
        self.salad_recipe = RecipeSO("Salad", [self.lettuce, self.tomato])
        
        self.recipe_list = RecipeListSO([self.sandwich_recipe, self.salad_recipe])
    
    def test_singleton(self):
        """シングルトンパターンのテスト"""
        manager1 = DeliveryManager.get_instance(self.recipe_list)
        manager2 = DeliveryManager.get_instance()
        self.assertIs(manager1, manager2)
    
    def test_singleton_requires_recipe_list_first_time(self):
        """初回作成時にrecipe_list_soが必要なことのテスト"""
        with self.assertRaises(ValueError):
            DeliveryManager.get_instance()
    
    def test_initial_state(self):
        """初期状態のテスト"""
        manager = DeliveryManager.get_instance(self.recipe_list)
        self.assertEqual(len(manager.get_waiting_recipe_so_list()), 0)
        self.assertEqual(manager.get_successful_recipes_amount(), 0)
    
    def test_deliver_recipe_success(self):
        """レシピ配達成功のテスト"""
        game_manager = KitchenGameManager.get_instance()
        game_manager.start_game()
        
        manager = DeliveryManager.get_instance(self.recipe_list)
        
        # 待機レシピを手動で追加
        manager._waiting_recipe_so_list.append(self.salad_recipe)
        
        # 成功イベントのテスト
        success_called = []
        def on_success(sender, args):
            success_called.append(True)
        
        manager.on_recipe_success.add_handler(on_success)
        
        # サラダを配達
        plate = PlateKitchenObject()
        plate.add_kitchen_object(self.lettuce)
        plate.add_kitchen_object(self.tomato)
        
        manager.deliver_recipe(plate)
        
        self.assertEqual(len(success_called), 1)
        self.assertEqual(manager.get_successful_recipes_amount(), 1)
        self.assertEqual(len(manager.get_waiting_recipe_so_list()), 0)
    
    def test_deliver_recipe_failure(self):
        """レシピ配達失敗のテスト"""
        game_manager = KitchenGameManager.get_instance()
        game_manager.start_game()
        
        manager = DeliveryManager.get_instance(self.recipe_list)
        
        # 待機レシピを手動で追加
        manager._waiting_recipe_so_list.append(self.salad_recipe)
        
        # 失敗イベントのテスト
        failed_called = []
        def on_failed(sender, args):
            failed_called.append(True)
        
        manager.on_recipe_failed.add_handler(on_failed)
        
        # 間違った材料で配達
        plate = PlateKitchenObject()
        plate.add_kitchen_object(self.bread)
        
        manager.deliver_recipe(plate)
        
        self.assertEqual(len(failed_called), 1)
        self.assertEqual(manager.get_successful_recipes_amount(), 0)
        self.assertEqual(len(manager.get_waiting_recipe_so_list()), 1)
    
    def test_deliver_recipe_wrong_ingredient_count(self):
        """材料数が違う場合の配達失敗のテスト"""
        game_manager = KitchenGameManager.get_instance()
        game_manager.start_game()
        
        manager = DeliveryManager.get_instance(self.recipe_list)
        
        # サラダレシピを待機
        manager._waiting_recipe_so_list.append(self.salad_recipe)
        
        # 材料が多すぎる
        plate = PlateKitchenObject()
        plate.add_kitchen_object(self.lettuce)
        plate.add_kitchen_object(self.tomato)
        plate.add_kitchen_object(self.bread)
        
        manager.deliver_recipe(plate)
        
        self.assertEqual(manager.get_successful_recipes_amount(), 0)
        self.assertEqual(len(manager.get_waiting_recipe_so_list()), 1)
    
    def test_recipe_spawn_event(self):
        """レシピ生成イベントのテスト"""
        game_manager = KitchenGameManager.get_instance()
        game_manager.start_game()
        
        manager = DeliveryManager.get_instance(self.recipe_list)
        
        spawn_called = []
        def on_spawn(sender, args):
            spawn_called.append(True)
        
        manager.on_recipe_spawned.add_handler(on_spawn)
        
        # タイマーをリセットして即座に発火させる
        manager._spawn_recipe_timer = 0.0
        manager.update()
        
        # レシピが生成されたはず
        self.assertGreater(len(spawn_called), 0)
    
    def test_waiting_recipes_max(self):
        """最大待機レシピ数のテスト"""
        game_manager = KitchenGameManager.get_instance()
        game_manager.start_game()
        
        manager = DeliveryManager.get_instance(self.recipe_list)
        
        # 最大数まで手動で追加
        for _ in range(manager._waiting_recipes_max):
            manager._waiting_recipe_so_list.append(self.salad_recipe)
        
        # タイマーをリセットして更新
        manager._spawn_recipe_timer = 0.0
        initial_count = len(manager.get_waiting_recipe_so_list())
        manager.update()
        
        # 最大数に達しているので増えないはず
        self.assertEqual(len(manager.get_waiting_recipe_so_list()), initial_count)
    
    def test_get_waiting_recipe_so_list_returns_copy(self):
        """待機レシピリスト取得がコピーを返すことのテスト"""
        manager = DeliveryManager.get_instance(self.recipe_list)
        
        list1 = manager.get_waiting_recipe_so_list()
        list2 = manager.get_waiting_recipe_so_list()
        
        # 異なるリストインスタンス
        self.assertIsNot(list1, list2)


if __name__ == '__main__':
    unittest.main()
