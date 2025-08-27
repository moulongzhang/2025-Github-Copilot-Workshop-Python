import time
import random
from typing import List, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum


class EventArgs:
    """イベント引数の基底クラス"""
    pass

class RecipeSpawnedEventArgs(EventArgs):
    def __init__(self, recipe):
        self.recipe = recipe

class RecipeCompletedEventArgs(EventArgs):
    def __init__(self, recipe):
        self.recipe = recipe

class RecipeFailedEventArgs(EventArgs):
    def __init__(self, plate):
        self.plate = plate


class Event:
    """C#のeventに相当するクラス"""
    def __init__(self):
        self._handlers: List[Callable] = []

    def add_handler(self, handler: Callable):
        if handler not in self._handlers:
            self._handlers.append(handler)

    def remove_handler(self, handler: Callable):
        if handler in self._handlers:
            self._handlers.remove(handler)

    def invoke(self, sender, args: EventArgs = None):
        for handler in self._handlers:
            handler(sender, args or EventArgs())


@dataclass
class KitchenObjectSO:
    """キッチンオブジェクトのデータクラス"""
    name: str
    object_id: int


@dataclass
class RecipeSO:
    """レシピのデータクラス"""
    name: str
    kitchen_object_so_list: List[KitchenObjectSO] = field(default_factory=list)


@dataclass
class RecipeListSO:
    """レシピリストのデータクラス"""
    recipe_so_list: List[RecipeSO] = field(default_factory=list)


class PlateKitchenObject:
    """皿のキッチンオブジェクト"""
    
    def __init__(self):
        self._kitchen_object_so_list: List[KitchenObjectSO] = []
    
    def add_kitchen_object(self, kitchen_object: KitchenObjectSO):
        """キッチンオブジェクトを追加"""
        self._kitchen_object_so_list.append(kitchen_object)
    
    def get_kitchen_object_so_list(self) -> List[KitchenObjectSO]:
        """キッチンオブジェクトリストを取得"""
        return self._kitchen_object_so_list.copy()


class KitchenGameManager:
    """キッチンゲームマネージャー（Singleton）"""
    
    _instance: Optional['KitchenGameManager'] = None
    
    def __init__(self):
        self._is_game_playing = False
    
    @classmethod
    def get_instance(cls) -> 'KitchenGameManager':
        """Singletonインスタンスを取得"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def is_game_playing(self) -> bool:
        """ゲームが進行中かどうか"""
        return self._is_game_playing
    
    def start_game(self):
        """ゲーム開始"""
        self._is_game_playing = True
    
    def stop_game(self):
        """ゲーム停止"""
        self._is_game_playing = False


class RecipeManager:
    """レシピ管理専用クラス"""
    def __init__(self, recipe_list_so: RecipeListSO):
        self._recipe_list_so = recipe_list_so

    def get_random_recipe(self) -> RecipeSO:
        return random.choice(self._recipe_list_so.recipe_so_list)

    def get_recipe_by_name(self, user_input, cursor):
        # SQLインジェクション対策: パラメータ化クエリ
        try:
            cursor.execute("SELECT * FROM recipes WHERE name = ?", (user_input,))
            return cursor.fetchall()
        except Exception as e:
            print(f"DBエラー: {e}")
            return []

class EventManager:
    """イベント管理専用クラス"""
    def __init__(self):
        self.on_recipe_spawned = Event()
        self.on_recipe_completed = Event()
        self.on_recipe_success = Event()
        self.on_recipe_failed = Event()

class DeliveryManager:
    """配達管理クラス（Python版）"""
    _instance: Optional['DeliveryManager'] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, recipe_list_so: RecipeListSO):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.recipe_manager = RecipeManager(recipe_list_so)
        self.event_manager = EventManager()
        self._waiting_recipe_so_list: List[RecipeSO] = []
        self._spawn_recipe_timer = 0.0
        self._spawn_recipe_timer_max = 4.0
        self._waiting_recipes_max = 4
        self._successful_recipes_amount = 0
        self._last_update_time = time.time()

    @classmethod
    def get_instance(cls, recipe_list_so: RecipeListSO = None) -> 'DeliveryManager':
        if cls._instance is None:
            if recipe_list_so is None:
                raise ValueError("初回作成時にはrecipe_list_soが必要です")
            cls._instance = cls(recipe_list_so)
        return cls._instance

    def update(self):
        current_time = time.time()
        delta_time = current_time - self._last_update_time
        self._last_update_time = current_time
        self._spawn_recipe_timer -= delta_time
        if self._spawn_recipe_timer <= 0.0:
            self._spawn_recipe_timer = self._spawn_recipe_timer_max
            kitchen_game_manager = KitchenGameManager.get_instance()
            if (kitchen_game_manager.is_game_playing() and 
                len(self._waiting_recipe_so_list) < self._waiting_recipes_max):
                waiting_recipe_so = self.recipe_manager.get_random_recipe()
                self._waiting_recipe_so_list.append(waiting_recipe_so)
                self.event_manager.on_recipe_spawned.invoke(self, RecipeSpawnedEventArgs(waiting_recipe_so))

    def deliver_recipe(self, plate_kitchen_object: PlateKitchenObject):
        plate_ingredients = set(plate_kitchen_object.get_kitchen_object_so_list())
        for i, waiting_recipe_so in enumerate(self._waiting_recipe_so_list):
            recipe_ingredients = set(waiting_recipe_so.kitchen_object_so_list)
            if plate_ingredients == recipe_ingredients:
                self._successful_recipes_amount += 1
                self._waiting_recipe_so_list.pop(i)
                self.event_manager.on_recipe_completed.invoke(self, RecipeCompletedEventArgs(waiting_recipe_so))
                self.event_manager.on_recipe_success.invoke(self, RecipeCompletedEventArgs(waiting_recipe_so))
                return
        self.event_manager.on_recipe_failed.invoke(self, RecipeFailedEventArgs(plate_kitchen_object))

    def get_waiting_recipe_so_list(self) -> List[RecipeSO]:
        return self._waiting_recipe_so_list.copy()

    def get_successful_recipes_amount(self) -> int:
        return self._successful_recipes_amount


# 使用例
if __name__ == "__main__":
    # サンプルデータ作成
    tomato = KitchenObjectSO("Tomato", 1)
    lettuce = KitchenObjectSO("Lettuce", 2)
    bread = KitchenObjectSO("Bread", 3)
    
    # サンプルレシピ
    sandwich_recipe = RecipeSO("Sandwich", [bread, lettuce, tomato])
    salad_recipe = RecipeSO("Salad", [lettuce, tomato])
    
    recipe_list = RecipeListSO([sandwich_recipe, salad_recipe])
    
    # ゲームマネージャーとデリバリーマネージャーを初期化
    game_manager = KitchenGameManager.get_instance()
    game_manager.start_game()
    
    delivery_manager = DeliveryManager.get_instance(recipe_list)
    
    # イベントハンドラーの設定
    def on_recipe_spawned(sender, args):
        print("新しいレシピが生成されました！")
    
    def on_recipe_success(sender, args):
        print("レシピ配達成功！")
    
    def on_recipe_failed(sender, args):
        print("レシピ配達失敗...")
    
    delivery_manager.on_recipe_spawned.add_handler(on_recipe_spawned)
    delivery_manager.on_recipe_success.add_handler(on_recipe_success)
    delivery_manager.on_recipe_failed.add_handler(on_recipe_failed)
    
    # サンプル実行
    print("ゲーム開始...")
    
    # 5秒間更新処理を実行
    start_time = time.time()
    while time.time() - start_time < 5:
        delivery_manager.update()
        time.sleep(0.1)  # 100ms間隔で更新
    
    print(f"待機中のレシピ数: {len(delivery_manager.get_waiting_recipe_so_list())}")
    
    # サンプル配達テスト
    plate = PlateKitchenObject()
    plate.add_kitchen_object(bread)
    plate.add_kitchen_object(lettuce)
    plate.add_kitchen_object(tomato)
    
    print("サンドイッチを配達...")
    delivery_manager.deliver_recipe(plate)
    
    print(f"成功したレシピ数: {delivery_manager.get_successful_recipes_amount()}")