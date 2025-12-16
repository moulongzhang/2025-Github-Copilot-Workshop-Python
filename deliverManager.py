import time
import random
from typing import List, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum


class EventArgs:
    """イベント引数の基底クラス"""
    pass


class Event:
    """
    C#のeventに相当するクラス
    
    オブザーバーパターンを実装し、イベント駆動アーキテクチャをサポートします。
    複数のハンドラーを登録でき、イベント発火時に全てのハンドラーが順次実行されます。
    """
    
    def __init__(self):
        self._handlers: List[Callable] = []
    
    def add_handler(self, handler: Callable):
        """
        イベントハンドラーを追加
        
        Args:
            handler: イベント発火時に呼び出される関数。署名は handler(sender, args) であること
        
        Note:
            同じハンドラーは重複して追加されません
        """
        if handler not in self._handlers:
            self._handlers.append(handler)
    
    def remove_handler(self, handler: Callable):
        """
        イベントハンドラーを削除
        
        Args:
            handler: 削除するハンドラー関数
        """
        if handler in self._handlers:
            self._handlers.remove(handler)
    
    def invoke(self, sender, args: EventArgs = None):
        """
        イベントを発火し、全てのハンドラーを実行
        
        Args:
            sender: イベントを発火したオブジェクト
            args: イベント引数（省略時はEventArgsインスタンスが渡される）
        """
        for handler in self._handlers:
            handler(sender, args or EventArgs())


@dataclass
class KitchenObjectSO:
    """
    キッチンオブジェクトのデータクラス
    
    料理に使用される材料や食材を表現します。
    
    Attributes:
        name: オブジェクトの名前（例：'Tomato', 'Lettuce'）
        object_id: オブジェクトの一意識別子
    """
    name: str
    object_id: int


@dataclass
class RecipeSO:
    """
    レシピのデータクラス
    
    完成した料理のレシピを表現します。
    
    Attributes:
        name: レシピの名前（例：'Sandwich', 'Salad'）
        kitchen_object_so_list: レシピに必要な材料のリスト
    """
    name: str
    kitchen_object_so_list: List[KitchenObjectSO] = field(default_factory=list)


@dataclass
class RecipeListSO:
    """
    レシピリストのデータクラス
    
    ゲームで使用可能な全レシピのコレクションを保持します。
    
    Attributes:
        recipe_so_list: レシピのリスト
    """
    recipe_so_list: List[RecipeSO] = field(default_factory=list)


class PlateKitchenObject:
    """
    皿のキッチンオブジェクト
    
    プレイヤーが準備した料理を保持する皿を表現します。
    複数の材料を追加でき、最終的にレシピと照合されます。
    """
    
    def __init__(self):
        self._kitchen_object_so_list: List[KitchenObjectSO] = []
    
    def add_kitchen_object(self, kitchen_object: KitchenObjectSO):
        """
        キッチンオブジェクトを追加
        
        Args:
            kitchen_object: 皿に追加する材料
        """
        self._kitchen_object_so_list.append(kitchen_object)
    
    def get_kitchen_object_so_list(self) -> List[KitchenObjectSO]:
        """
        キッチンオブジェクトリストを取得
        
        Returns:
            材料リストのコピー（元のリストへの変更を防ぐため）
        """
        return self._kitchen_object_so_list.copy()


class KitchenGameManager:
    """
    キッチンゲームマネージャー（Singleton）
    
    ゲーム全体の状態を管理するシングルトンクラス。
    ゲームの開始・停止状態を保持します。
    """
    
    _instance: Optional['KitchenGameManager'] = None
    
    def __init__(self):
        self._is_game_playing = False
    
    @classmethod
    def get_instance(cls) -> 'KitchenGameManager':
        """
        Singletonインスタンスを取得
        
        Returns:
            KitchenGameManagerの唯一のインスタンス
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def is_game_playing(self) -> bool:
        """
        ゲームが進行中かどうか
        
        Returns:
            ゲーム進行中の場合True、それ以外False
        """
        return self._is_game_playing
    
    def start_game(self):
        """ゲーム開始"""
        self._is_game_playing = True
    
    def stop_game(self):
        """ゲーム停止"""
        self._is_game_playing = False


class DeliveryManager:
    """
    配達管理クラス（Python版）- Singleton
    
    レシピの生成と配達を管理するコアビジネスロジッククラス。
    定期的にレシピを生成し、プレイヤーの配達を検証します。
    
    Events:
        on_recipe_spawned: 新しいレシピが生成されたときに発火
        on_recipe_completed: レシピが完了したときに発火
        on_recipe_success: レシピ配達が成功したときに発火
        on_recipe_failed: レシピ配達が失敗したときに発火
    """
    
    _instance: Optional['DeliveryManager'] = None
    
    def __init__(self, recipe_list_so: RecipeListSO):
        # イベント定義
        self.on_recipe_spawned = Event()
        self.on_recipe_completed = Event()
        self.on_recipe_success = Event()
        self.on_recipe_failed = Event()
        
        # プライベート変数
        self._recipe_list_so = recipe_list_so
        self._waiting_recipe_so_list: List[RecipeSO] = []
        self._spawn_recipe_timer = 0.0
        self._spawn_recipe_timer_max = 4.0  # レシピ生成間隔（秒）
        self._waiting_recipes_max = 4  # 同時に待機できるレシピの最大数
        self._successful_recipes_amount = 0
        self._last_update_time = time.time()
    
    @classmethod
    def get_instance(cls, recipe_list_so: RecipeListSO = None) -> 'DeliveryManager':
        """
        Singletonインスタンスを取得
        
        Args:
            recipe_list_so: 初回作成時のみ必要なレシピリスト
        
        Returns:
            DeliveryManagerの唯一のインスタンス
        
        Raises:
            ValueError: 初回作成時にrecipe_list_soが指定されていない場合
        """
        if cls._instance is None:
            if recipe_list_so is None:
                raise ValueError("初回作成時にはrecipe_list_soが必要です")
            cls._instance = cls(recipe_list_so)
        return cls._instance
    
    def update(self):
        """
        フレーム更新処理（UnityのUpdate相当）
        
        定期的に呼び出され、タイマーを更新してレシピを生成します。
        ゲームループの一部として使用されることを想定しています。
        """
        current_time = time.time()
        delta_time = current_time - self._last_update_time
        self._last_update_time = current_time
        
        self._spawn_recipe_timer -= delta_time
        
        if self._spawn_recipe_timer <= 0.0:
            self._spawn_recipe_timer = self._spawn_recipe_timer_max
            
            kitchen_game_manager = KitchenGameManager.get_instance()
            if (kitchen_game_manager.is_game_playing() and 
                len(self._waiting_recipe_so_list) < self._waiting_recipes_max):
                
                # ランダムにレシピを選択
                waiting_recipe_so = random.choice(self._recipe_list_so.recipe_so_list)
                self._waiting_recipe_so_list.append(waiting_recipe_so)
                
                # イベント発火
                self.on_recipe_spawned.invoke(self)
    
    def deliver_recipe(self, plate_kitchen_object: PlateKitchenObject):
        """
        レシピの材料と皿の材料が一致しているかどうかを確認する
        
        プレイヤーが準備した料理（皿）と待機中のレシピを比較し、
        一致するレシピがあれば成功、なければ失敗イベントを発火します。
        
        Args:
            plate_kitchen_object: プレイヤーが準備した料理を保持する皿
        
        Note:
            材料の順序は問わず、全ての材料が揃っていれば成功とみなされます
        """
        
        for i, waiting_recipe_so in enumerate(self._waiting_recipe_so_list):
            plate_ingredients = plate_kitchen_object.get_kitchen_object_so_list()
            
            # 材料数が一致するかチェック
            if len(waiting_recipe_so.kitchen_object_so_list) == len(plate_ingredients):
                plate_contents_matches_recipe = True
                
                # レシピの各材料をチェック
                for recipe_kitchen_object_so in waiting_recipe_so.kitchen_object_so_list:
                    ingredient_found = False
                    
                    # 皿の材料と照合
                    for plate_kitchen_object_so in plate_ingredients:
                        if plate_kitchen_object_so == recipe_kitchen_object_so:
                            ingredient_found = True
                            break
                    
                    if not ingredient_found:
                        plate_contents_matches_recipe = False
                        break
                
                # 材料が完全に一致した場合
                if plate_contents_matches_recipe:
                    self._successful_recipes_amount += 1
                    self._waiting_recipe_so_list.pop(i)
                    
                    # 成功イベント発火
                    self.on_recipe_completed.invoke(self)
                    self.on_recipe_success.invoke(self)
                    return
        
        # 一致するレシピが見つからなかった場合
        self.on_recipe_failed.invoke(self)
    
    def get_waiting_recipe_so_list(self) -> List[RecipeSO]:
        """
        待機中のレシピリストを取得
        
        Returns:
            待機中のレシピリストのコピー
        """
        return self._waiting_recipe_so_list.copy()
    
    def get_successful_recipes_amount(self) -> int:
        """
        成功したレシピ数を取得
        
        Returns:
            配達に成功したレシピの合計数
        """
        return self._successful_recipes_amount