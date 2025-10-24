import time
import random
from typing import List, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum


class EventArgs:
    """イベント引数の基底クラス"""
    pass


class Event:
    """C#のeventに相当するクラス"""
    
    def __init__(self):
        self._handlers: List[Callable] = []
    
    def add_handler(self, handler: Callable):
        """イベントハンドラーを追加"""
        if handler not in self._handlers:
            self._handlers.append(handler)
    
    def remove_handler(self, handler: Callable):
        """イベントハンドラーを削除"""
        if handler in self._handlers:
            self._handlers.remove(handler)
    
    def invoke(self, sender, args: EventArgs = None):
        """イベントを発火"""
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



from collections import Counter

class DeliveryEventArgs(EventArgs):
    """
    配達イベント用のEventArgs
    Attributes:
        recipe_so (RecipeSO): 対象レシピ
        reason (str): 失敗理由など
    """
    def __init__(self, recipe_so: Optional['RecipeSO'], reason: Optional[str] = None):
        self.recipe_so = recipe_so
        self.reason = reason

class DeliveryManager:
    """
    配達管理クラス（Python版）
    - レシピ生成、配達判定、イベント管理を担当
    - シングルトンを廃止し、インスタンス生成を呼び出し側に委ねる
    - マジックナンバーや設定値は引数で注入可能
    - テスト容易性・保守性・拡張性を重視
    """

    def __init__(
        self,
        recipe_list_so: RecipeListSO,
        spawn_recipe_timer_max: float = 4.0,
        waiting_recipes_max: int = 4
    ):
        """
        Args:
            recipe_list_so (RecipeListSO): レシピリスト
            spawn_recipe_timer_max (float): レシピ生成間隔（秒）
            waiting_recipes_max (int): 同時に待機できるレシピ数
        """
        # イベント定義
        self.on_recipe_spawned = Event()
        self.on_recipe_completed = Event()
        self.on_recipe_success = Event()
        self.on_recipe_failed = Event()

        # プライベート変数
        self._recipe_list_so = recipe_list_so
        self._waiting_recipe_so_list: List[RecipeSO] = []
        self._spawn_recipe_timer = 0.0
        self._spawn_recipe_timer_max = spawn_recipe_timer_max
        self._waiting_recipes_max = waiting_recipes_max
        self._successful_recipes_amount = 0
        self._last_update_time = time.time()

    def reset(self):
        """状態をリセット（テスト用）"""
        self._waiting_recipe_so_list.clear()
        self._spawn_recipe_timer = 0.0
        self._successful_recipes_amount = 0
        self._last_update_time = time.time()

    def update(self):
        """フレーム更新処理（UnityのUpdate相当）"""
        current_time = time.time()
        delta_time = current_time - self._last_update_time
        self._last_update_time = current_time

        self._spawn_recipe_timer -= delta_time

        kitchen_game_manager = KitchenGameManager.get_instance()
        if (
            self._spawn_recipe_timer <= 0.0
            and kitchen_game_manager.is_game_playing()
            and len(self._waiting_recipe_so_list) < self._waiting_recipes_max
        ):
            self._spawn_recipe_timer = self._spawn_recipe_timer_max
            # ランダムにレシピを選択
            waiting_recipe_so = random.choice(self._recipe_list_so.recipe_so_list)
            self._waiting_recipe_so_list.append(waiting_recipe_so)
            # イベント発火
            self.on_recipe_spawned.invoke(self, DeliveryEventArgs(waiting_recipe_so))

    def deliver_recipe(self, plate_kitchen_object: PlateKitchenObject):
        """
        レシピの材料と皿の材料が一致しているかどうかを確認する
        Args:
            plate_kitchen_object (PlateKitchenObject): 配達対象の皿
        """
        try:
            if plate_kitchen_object is None:
                self.on_recipe_failed.invoke(self, DeliveryEventArgs(None, reason="plate_kitchen_object is None"))
                return

            plate_ingredients = plate_kitchen_object.get_kitchen_object_so_list()
            if not plate_ingredients:
                self.on_recipe_failed.invoke(self, DeliveryEventArgs(None, reason="plate_ingredients is empty"))
                return

            plate_counter = Counter(plate_ingredients)

            for i, waiting_recipe_so in enumerate(self._waiting_recipe_so_list):
                recipe_ingredients = waiting_recipe_so.kitchen_object_so_list
                if len(recipe_ingredients) != len(plate_ingredients):
                    continue
                recipe_counter = Counter(recipe_ingredients)
                if plate_counter == recipe_counter:
                    self._successful_recipes_amount += 1
                    matched_recipe = self._waiting_recipe_so_list.pop(i)
                    self.on_recipe_completed.invoke(self, DeliveryEventArgs(matched_recipe))
                    self.on_recipe_success.invoke(self, DeliveryEventArgs(matched_recipe))
                    return

            # 一致するレシピが見つからなかった場合
            self.on_recipe_failed.invoke(self, DeliveryEventArgs(None, reason="no matching recipe"))
        except Exception as e:
            # 予期しない例外も失敗扱い
            self.on_recipe_failed.invoke(self, DeliveryEventArgs(None, reason=str(e)))

    def get_waiting_recipe_so_list(self) -> List['RecipeSO']:
        """待機中のレシピリストを取得"""
        return self._waiting_recipe_so_list.copy()

    def get_successful_recipes_amount(self) -> int:
        """成功したレシピ数を取得"""
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