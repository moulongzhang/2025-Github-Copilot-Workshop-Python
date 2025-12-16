from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from deliverManager import (
    DeliveryManager, KitchenGameManager, RecipeListSO, RecipeSO,
    KitchenObjectSO, PlateKitchenObject
)
import threading
import time
import os

app = Flask(__name__)
CORS(app)

# Initialize game data
tomato = KitchenObjectSO("Tomato", 1)
lettuce = KitchenObjectSO("Lettuce", 2)
bread = KitchenObjectSO("Bread", 3)
cheese = KitchenObjectSO("Cheese", 4)

# Sample recipes
sandwich_recipe = RecipeSO("Sandwich", [bread, lettuce, tomato])
salad_recipe = RecipeSO("Salad", [lettuce, tomato])
cheese_sandwich_recipe = RecipeSO("Cheese Sandwich", [bread, cheese, lettuce])

recipe_list = RecipeListSO([sandwich_recipe, salad_recipe, cheese_sandwich_recipe])

# Initialize game manager and delivery manager
game_manager = KitchenGameManager.get_instance()
game_manager.start_game()

delivery_manager = DeliveryManager.get_instance(recipe_list)

# Background thread to update delivery manager
update_thread = None
stop_event = threading.Event()


def update_loop():
    """Background thread to update the delivery manager"""
    while not stop_event.is_set():
        delivery_manager.update()
        time.sleep(0.1)  # Update every 100ms


@app.route('/')
def index():
    """Serve the frontend HTML page"""
    return send_from_directory('.', 'index.html')


@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get current progress data"""
    try:
        progress_data = {
            'successful_recipes': delivery_manager.get_successful_recipes_amount(),
            'waiting_recipes_count': len(delivery_manager.get_waiting_recipe_so_list())
        }
        return jsonify({
            'success': True,
            'data': progress_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get list of waiting recipes"""
    try:
        waiting_recipes = delivery_manager.get_waiting_recipe_so_list()
        recipes_data = [
            {
                'name': recipe.name,
                'ingredients': [
                    {'name': ingredient.name, 'id': ingredient.object_id}
                    for ingredient in recipe.kitchen_object_so_list
                ]
            }
            for recipe in waiting_recipes
        ]
        return jsonify({
            'success': True,
            'data': recipes_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/deliver', methods=['POST'])
def deliver_recipe():
    """Deliver a recipe with specified ingredients"""
    try:
        data = request.get_json()
        if not data or 'ingredients' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing ingredients data'
            }), 400
        
        # Create a plate with the specified ingredients
        plate = PlateKitchenObject()
        ingredient_objects = {
            'Tomato': tomato,
            'Lettuce': lettuce,
            'Bread': bread,
            'Cheese': cheese
        }
        
        for ingredient_name in data['ingredients']:
            if ingredient_name in ingredient_objects:
                plate.add_kitchen_object(ingredient_objects[ingredient_name])
            else:
                return jsonify({
                    'success': False,
                    'error': f'Unknown ingredient: {ingredient_name}'
                }), 400
        
        # Try to deliver the recipe
        initial_success_count = delivery_manager.get_successful_recipes_amount()
        delivery_manager.deliver_recipe(plate)
        final_success_count = delivery_manager.get_successful_recipes_amount()
        
        # Check if delivery was successful
        is_successful = final_success_count > initial_success_count
        
        return jsonify({
            'success': True,
            'data': {
                'delivered': is_successful,
                'successful_recipes': final_success_count
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/start', methods=['POST'])
def start_game():
    """Start the game"""
    try:
        game_manager.start_game()
        return jsonify({
            'success': True,
            'message': 'Game started'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stop', methods=['POST'])
def stop_game():
    """Stop the game"""
    try:
        game_manager.stop_game()
        return jsonify({
            'success': True,
            'message': 'Game stopped'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def start_background_thread():
    """Start the background update thread"""
    global update_thread
    stop_event.clear()
    update_thread = threading.Thread(target=update_loop, daemon=True)
    update_thread.start()


if __name__ == '__main__':
    # Start the background thread for game updates
    start_background_thread()
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode, use_reloader=False)
