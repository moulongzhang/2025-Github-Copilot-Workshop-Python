import time
import random
import threading
from typing import List, Callable, Optional
from dataclasses import dataclass, field
from collections import Counter



class EventArgs:
    """Base class for event arguments."""
    pass


from typing import TypeVar, Generic
TEventArgs = TypeVar('TEventArgs', bound=EventArgs)


class Event(Generic[TEventArgs]):
    """C# event-like class for Python, type-safe."""
    def __init__(self):
        self._handlers: List[Callable[[Any, TEventArgs], None]] = []

    def add_handler(self, handler: Callable[[Any, TEventArgs], None]) -> None:
        if handler not in self._handlers:
            self._handlers.append(handler)

    def remove_handler(self, handler: Callable[[Any, TEventArgs], None]) -> None:
        if handler in self._handlers:
            self._handlers.remove(handler)

    def invoke(self, sender: Any, args: TEventArgs = None) -> None:
        for handler in self._handlers:
            try:
                handler(sender, args or EventArgs())
            except Exception as e:
                print(f"[Event] Handler exception: {e}")


class Event:
    """C# event-like class for Python."""
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
            try:
                handler(sender, args or EventArgs())
            except Exception as e:
                print(f"[Event] Handler exception: {e}")


@dataclass
class KitchenObjectSO:
    """Data class for kitchen objects."""
    name: str
    object_id: int


@dataclass
class RecipeSO:
    """Data class for recipes."""
    name: str
    kitchen_object_so_list: List[KitchenObjectSO] = field(default_factory=list)


@dataclass
class RecipeListSO:
    """Data class for recipe lists."""
    recipe_so_list: List[RecipeSO] = field(default_factory=list)



class PlateKitchenObject:
    """Plate kitchen object."""
    def __init__(self) -> None:
        self._kitchen_object_so_list: List[KitchenObjectSO] = []

    def add_kitchen_object(self, kitchen_object: KitchenObjectSO) -> None:
        self._kitchen_object_so_list.append(kitchen_object)

    def get_kitchen_object_so_list(self) -> List[KitchenObjectSO]:
        return self._kitchen_object_so_list.copy()



class KitchenGameManager:
    """Kitchen game manager (Singleton, thread-safe)."""
    _instance: Optional['KitchenGameManager'] = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self._is_game_playing: bool = False

    @classmethod
    def get_instance(cls) -> 'KitchenGameManager':
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    @classmethod
    def _reset_instance(cls):
        """テスト用: シングルトンインスタンスをリセット"""
        with cls._lock:
            cls._instance = None

    def is_game_playing(self) -> bool:
        return self._is_game_playing

    def start_game(self) -> None:
        self._is_game_playing = True

    def stop_game(self) -> None:
        self._is_game_playing = False



from typing import Protocol, runtime_checkable, Any

@runtime_checkable
class RecipeRepositoryProtocol(Protocol):
    def get_recipe_by_name(self, name: str) -> Any:
        ...


class InMemoryRecipeRepository:
    """In-memory implementation for RecipeRepositoryProtocol (for test/demo)."""
    def __init__(self, recipe_list_so: RecipeListSO):
        self._recipes = {r.name: r for r in recipe_list_so.recipe_so_list}

    def get_recipe_by_name(self, name: str) -> Optional[RecipeSO]:
        return self._recipes.get(name)



class DeliveryManager:
    """Delivery manager class (Python version, improved)."""
    _instance: Optional['DeliveryManager'] = None
    _lock = threading.Lock()

    def __init__(self, recipe_list_so: RecipeListSO, recipe_repository: Optional[RecipeRepositoryProtocol] = None) -> None:
        self.on_recipe_spawned: Event[EventArgs] = Event()
        self.on_recipe_completed: Event[EventArgs] = Event()
        self.on_recipe_success: Event[EventArgs] = Event()
        self.on_recipe_failed: Event[EventArgs] = Event()

        self._recipe_list_so: RecipeListSO = recipe_list_so
        self._waiting_recipe_so_list: List[RecipeSO] = []
        self._spawn_recipe_timer: float = 0.0
        self._spawn_recipe_timer_max: float = 4.0
        self._waiting_recipes_max: int = 4
        self._successful_recipes_amount: int = 0
        self._last_update_time: float = time.time()
        self._recipe_repository: RecipeRepositoryProtocol = recipe_repository or InMemoryRecipeRepository(recipe_list_so)

    @classmethod
    def get_instance(cls, recipe_list_so: RecipeListSO = None, recipe_repository: Optional[RecipeRepositoryProtocol] = None) -> 'DeliveryManager':
        with cls._lock:
            if cls._instance is None:
                if recipe_list_so is None:
                    raise ValueError("recipe_list_so is required for the first instantiation")
                cls._instance = cls(recipe_list_so, recipe_repository)
        return cls._instance

    @classmethod
    def _reset_instance(cls):
        """テスト用: シングルトンインスタンスをリセット"""
        with cls._lock:
            cls._instance = None

    def get_recipe_by_name(self, name: str) -> Optional[RecipeSO]:
        """Repository経由でレシピを安全に取得する。"""
        return self._recipe_repository.get_recipe_by_name(name)

    def update(self) -> None:
        """Frame update (equivalent to Unity's Update)."""
        current_time = time.time()
        delta_time = current_time - self._last_update_time
        self._last_update_time = current_time

        self._spawn_recipe_timer -= delta_time

        if self._spawn_recipe_timer <= 0.0:
            self._spawn_recipe_timer = self._spawn_recipe_timer_max

            kitchen_game_manager = KitchenGameManager.get_instance()
            if (kitchen_game_manager.is_game_playing() and
                len(self._waiting_recipe_so_list) < self._waiting_recipes_max):

                # Choose a recipe randomly
                waiting_recipe_so = random.choice(self._recipe_list_so.recipe_so_list)
                self._waiting_recipe_so_list.append(waiting_recipe_so)

                # Fire event
                self._safe_invoke(self.on_recipe_spawned)

    def deliver_recipe(self, plate_kitchen_object: PlateKitchenObject) -> None:
        """Check if the plate's ingredients match any waiting recipe."""
        if not isinstance(plate_kitchen_object, PlateKitchenObject):
            print("Error: plate_kitchen_object must be a PlateKitchenObject instance")
            self._safe_invoke(self.on_recipe_failed)
            return

        plate_ingredients = plate_kitchen_object.get_kitchen_object_so_list()

        for i, waiting_recipe_so in enumerate(self._waiting_recipe_so_list):
            recipe_ingredients = waiting_recipe_so.kitchen_object_so_list
            if len(recipe_ingredients) != len(plate_ingredients):
                continue
            # 材料比較をCounterで簡素化（順序・重複非依存）
            if Counter(recipe_ingredients) == Counter(plate_ingredients):
                self._successful_recipes_amount += 1
                self._waiting_recipe_so_list.pop(i)
                self._safe_invoke(self.on_recipe_completed)
                self._safe_invoke(self.on_recipe_success)
                return

        # No matching recipe found
        self._safe_invoke(self.on_recipe_failed)

    def _safe_invoke(self, event: Event) -> None:
        try:
            event.invoke(self)
        except Exception as e:
            print(f"[DeliveryManager] Event invoke exception: {e}")

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