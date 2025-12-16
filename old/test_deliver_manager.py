import pytest
from deliverManager import (
    KitchenObjectSO, RecipeSO, RecipeListSO, PlateKitchenObject,
    DeliveryManager, KitchenGameManager, InMemoryRecipeRepository
)

def make_sample_data():
    tomato = KitchenObjectSO("Tomato", 1)
    lettuce = KitchenObjectSO("Lettuce", 2)
    bread = KitchenObjectSO("Bread", 3)
    sandwich_recipe = RecipeSO("Sandwich", [bread, lettuce, tomato])
    salad_recipe = RecipeSO("Salad", [lettuce, tomato])
    recipe_list = RecipeListSO([sandwich_recipe, salad_recipe])
    return bread, lettuce, tomato, sandwich_recipe, salad_recipe, recipe_list

def setup_module(module):
    # シングルトンをリセット
    DeliveryManager._reset_instance()
    KitchenGameManager._reset_instance()

def teardown_module(module):
    DeliveryManager._reset_instance()
    KitchenGameManager._reset_instance()

def test_recipe_repository():
    _, _, _, sandwich, salad, recipe_list = make_sample_data()
    repo = InMemoryRecipeRepository(recipe_list)
    assert repo.get_recipe_by_name("Sandwich") == sandwich
    assert repo.get_recipe_by_name("Salad") == salad
    assert repo.get_recipe_by_name("NotExist") is None

def test_delivery_manager_spawn_and_deliver():
    bread, lettuce, tomato, sandwich, salad, recipe_list = make_sample_data()
    dm = DeliveryManager(recipe_list)
    kgm = KitchenGameManager.get_instance()
    kgm.start_game()
    # レシピ生成
    for _ in range(5):
        dm.update()
    waiting = dm.get_waiting_recipe_so_list()
    assert 0 < len(waiting) <= 4
    # 正しい材料で配達
    plate = PlateKitchenObject()
    for obj in sandwich.kitchen_object_so_list:
        plate.add_kitchen_object(obj)
    # waitingにサンドイッチがなければ追加
    if not any(r.name == "Sandwich" for r in waiting):
        dm._waiting_recipe_so_list.append(sandwich)
    before = dm.get_successful_recipes_amount()
    dm.deliver_recipe(plate)
    after = dm.get_successful_recipes_amount()
    assert after == before + 1

def test_delivery_manager_failed_delivery():
    bread, lettuce, tomato, sandwich, salad, recipe_list = make_sample_data()
    dm = DeliveryManager(recipe_list)
    kgm = KitchenGameManager.get_instance()
    kgm.start_game()
    # waitingにサンドイッチを追加
    dm._waiting_recipe_so_list.append(sandwich)
    # 間違った材料
    plate = PlateKitchenObject()
    plate.add_kitchen_object(bread)
    plate.add_kitchen_object(lettuce)
    # tomatoが足りない
    before = dm.get_successful_recipes_amount()
    dm.deliver_recipe(plate)
    after = dm.get_successful_recipes_amount()
    assert after == before

def test_event_handlers():
    _, _, _, sandwich, _, recipe_list = make_sample_data()
    dm = DeliveryManager(recipe_list)
    events = {"spawned": False, "success": False, "failed": False}
    def on_spawned(sender, args):
        events["spawned"] = True
    def on_success(sender, args):
        events["success"] = True
    def on_failed(sender, args):
        events["failed"] = True
    dm.on_recipe_spawned.add_handler(on_spawned)
    dm.on_recipe_success.add_handler(on_success)
    dm.on_recipe_failed.add_handler(on_failed)
    # spawn event
    dm._waiting_recipe_so_list.clear()
    kgm = KitchenGameManager.get_instance()
    kgm.start_game()
    dm.update()
    assert events["spawned"]
    # success event
    plate = PlateKitchenObject()
    for obj in sandwich.kitchen_object_so_list:
        plate.add_kitchen_object(obj)
    dm._waiting_recipe_so_list.append(sandwich)
    dm.deliver_recipe(plate)
    assert events["success"]
    # failed event
    plate2 = PlateKitchenObject()
    plate2.add_kitchen_object(sandwich.kitchen_object_so_list[0])
    dm.deliver_recipe(plate2)
    assert events["failed"]