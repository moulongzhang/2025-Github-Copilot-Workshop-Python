import time
import random
import threading
import logging
from collections import Counter
from typing import List, Callable, Optional, Tuple
from dataclasses import dataclass, field


class EventArgs:
    """イベント引数の基底クラス"""
    pass


class Event:
    """C#のeventに相当するクラス"""

    def __init__(self):
        self._handlers: List[Callable] = []

    def add_handler(self, handler: Callable) -> None:
        """イベントハンドラーを追加"""
        if handler not in self._handlers:
            self._handlers.append(handler)

    def remove_handler(self, handler: Callable) -> None:
        """イベントハンドラーを削除"""
        if handler in self._handlers:
            self._handlers.remove(handler)

    def invoke(self, sender, args: EventArgs = None) -> None:
        """イベントを発火（各ハンドラーは独立して実行継続）"""
        args = args or EventArgs()
        logger = logging.getLogger(__name__)
        for handler in list(self._handlers):
            try:
                handler(sender, args)
            except Exception as e:
                logger.error(f"Error in event handler {getattr(handler, '__name__', repr(handler))}: {e}", exc_info=True)


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


@dataclass
class DeliveryConfig:
    """配達機能の設定値"""
    SPAWN_INTERVAL_SECONDS: float = 4.0
    MAX_WAITING_RECIPES: int = 4


class DeliveryManager:
    """配達管理クラス（Python版）

    - レシピのスポーン（生成）
    - 配達の検証
    - スコア管理
    - イベント発火

    設定値は`DeliveryConfig`、時間は`time_provider`で注入可能。
    Singletonだが、テストのために`reset_instance()`も提供する。
    """

    _instance: Optional['DeliveryManager'] = None
    _lock = threading.Lock()

    def __init__(
        self,
        recipe_list_so: RecipeListSO,
        config: Optional[DeliveryConfig] = None,
        time_provider: Callable[[], float] = time.time,
        rnd: Optional[random.Random] = None,
    ) -> None:
        # イベント定義
        self.on_recipe_spawned = Event()
        self.on_recipe_completed = Event()
        self.on_recipe_success = Event()
        self.on_recipe_failed = Event()

        # 設定・依存
        self._config = config or DeliveryConfig()
        self._time_provider = time_provider
        self._random = rnd or random.Random()

        # 状態
        self._recipe_list_so = recipe_list_so
        self._waiting_recipe_so_list: List[RecipeSO] = []
        self._spawn_recipe_timer = 0.0
        self._spawn_recipe_timer_max = self._config.SPAWN_INTERVAL_SECONDS
        self._waiting_recipes_max = self._config.MAX_WAITING_RECIPES
        self._successful_recipes_amount = 0
        self._last_update_time = self._time_provider()

        # 並行保護
        self._state_lock = threading.Lock()

    @classmethod
    def get_instance(
        cls,
        recipe_list_so: RecipeListSO = None,
        config: Optional[DeliveryConfig] = None,
        time_provider: Callable[[], float] = time.time,
        rnd: Optional[random.Random] = None,
    ) -> 'DeliveryManager':
        """Singletonインスタンスを取得（スレッドセーフ）"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    if recipe_list_so is None:
                        raise ValueError("初回作成時にはrecipe_list_soが必要です")
                    cls._instance = cls(recipe_list_so, config, time_provider, rnd)
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """テスト用: Singletonインスタンスをリセット"""
        with cls._lock:
            cls._instance = None

    def get_recipe_by_name(self, user_input: str) -> Optional[RecipeSO]:
        """名前でレシピを検索（安全なメモリ検索）"""
        if not isinstance(user_input, str):
            return None
        normalized = user_input.strip()
        if not normalized:
            return None
        # ここではDBを使わず、メモリ内のリストから検索
        for recipe in self._recipe_list_so.recipe_so_list:
            if recipe.name == normalized:
                return recipe
        return None

    def update(self) -> None:
        """フレーム更新処理（UnityのUpdate相当）"""
        current_time = self._time_provider()
        delta_time = current_time - self._last_update_time
        self._last_update_time = current_time

        self._spawn_recipe_timer -= delta_time

        if self._spawn_recipe_timer <= 0.0:
            self._spawn_recipe_timer = self._spawn_recipe_timer_max

            kitchen_game_manager = KitchenGameManager.get_instance()
            if kitchen_game_manager.is_game_playing():
                with self._state_lock:
                    if len(self._waiting_recipe_so_list) < self._waiting_recipes_max:
                        # ランダムにレシピを選択
                        if not self._recipe_list_so.recipe_so_list:
                            return
                        waiting_recipe_so = self._random.choice(self._recipe_list_so.recipe_so_list)
                        self._waiting_recipe_so_list.append(waiting_recipe_so)
                        # イベント発火
                        self.on_recipe_spawned.invoke(self)

    def _recipe_to_counter(self, recipe: RecipeSO) -> Counter:
        """レシピの材料をobject_idベースのCounterへ変換"""
        return Counter(ko.object_id for ko in recipe.kitchen_object_so_list)

    def _plate_to_counter(self, plate: PlateKitchenObject) -> Counter:
        """皿の材料をobject_idベースのCounterへ変換"""
        return Counter(ko.object_id for ko in plate.get_kitchen_object_so_list())

    def deliver_recipe(self, plate_kitchen_object: PlateKitchenObject) -> None:
        """皿の内容を待機中レシピと照合して配達処理を行う"""
        plate_counter = self._plate_to_counter(plate_kitchen_object)

        with self._state_lock:
            for i, waiting_recipe_so in enumerate(list(self._waiting_recipe_so_list)):
                recipe_counter = self._recipe_to_counter(waiting_recipe_so)
                if recipe_counter == plate_counter:
                    self._successful_recipes_amount += 1
                    # pop by index needs original index in current list
                    idx = self._waiting_recipe_so_list.index(waiting_recipe_so)
                    self._waiting_recipe_so_list.pop(idx)
                    # 成功イベント（順序: completed -> success）
                    self.on_recipe_completed.invoke(self)
                    self.on_recipe_success.invoke(self)
                    return

        # 一致するレシピが見つからなかった場合
        self.on_recipe_failed.invoke(self)

    def get_waiting_recipe_so_list(self) -> Tuple[RecipeSO, ...]:
        """待機中のレシピリスト（読み取り専用ビュー）を取得"""
        with self._state_lock:
            return tuple(self._waiting_recipe_so_list)

    def get_successful_recipes_amount(self) -> int:
        """成功したレシピ数を取得"""
        with self._state_lock:
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