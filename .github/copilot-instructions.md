# Copilot Instructions for 2025-Github-Copilot-Workshop-Python

## Project Overview
This is a cooking/kitchen game simulation system built in Python, inspired by Unity game development patterns. It demonstrates event-driven architecture, singleton patterns, and game state management for educational purposes.

## Core Architecture

### Singleton Pattern Usage
- `KitchenGameManager.get_instance()` - Controls game state (playing/stopped)
- `DeliveryManager.get_instance(recipe_list_so)` - Manages recipe delivery system
- Always check if instance exists before creating new singletons
- Use lazy initialization pattern: instance created only when first accessed

### Event System
The codebase implements a custom C#-like event system:
```python
# Event declaration
self.on_recipe_spawned = Event()

# Handler registration
delivery_manager.on_recipe_spawned.add_handler(on_recipe_spawned)

# Event firing
self.on_recipe_spawned.invoke(self)
```

### Game Loop Pattern
- `DeliveryManager.update()` implements Unity-style frame updates
- Uses delta time calculation for frame-rate independent behavior
- Call `update()` in a loop with `time.sleep(0.1)` for simulation

## Key Components

### Recipe System (`deliverManager.py`)
- `RecipeSO` contains recipe name and ingredient list
- `PlateKitchenObject` holds ingredients for comparison
- `deliver_recipe()` uses exact ingredient matching (order-independent)

### Testing Framework (`test_deliverManager.py`)
- Uses pytest with comprehensive fixture system
- Mock classes: `MockTimeProvider`, `MockRandomProvider`, `MockGameManager`
- Test isolation through dependency injection
- Fixtures provide sample data: `sample_objects`, `sample_recipes`, `recipe_list`

## Development Patterns

### Type Safety
- Strict mypy configuration in `mypy.ini` (disallow_untyped_defs=True)
- Use proper type hints: `from typing import List, Optional, Callable`
- Dataclasses with `@dataclass` decorator for data structures

### Code Organization
- Game objects use `KitchenObjectSO` suffix (ScriptableObject pattern from Unity)
- Event args inherit from `EventArgs` base class
- Keep business logic separate from presentation layer

## Development Workflow

### Running Tests
```bash
pytest test_deliverManager.py -v
```

### Type Checking
```bash
mypy deliverManager.py
```

### DevContainer Environment
- Python 3.11 in Debian container
- Pre-configured with GitHub Copilot extension
- No requirements.txt - uses built-in libraries only

## Anti-Patterns to Avoid
- Don't create multiple singleton instances without proper cleanup
- Don't ignore event handler cleanup (memory leaks)
- Don't use SQL injection vulnerable code like `f"SELECT * FROM recipes WHERE name = '{user_input}'"`
- Don't modify lists while iterating (use enumerate with reverse iteration or copy)

## Common Implementations
When adding new kitchen objects:
1. Create `KitchenObjectSO` with unique `object_id`
2. Add to recipe's `kitchen_object_so_list`
3. Implement equality comparison for recipe matching
4. Update test fixtures accordingly

When adding new events:
1. Declare as `Event()` instance in `__init__`
2. Create corresponding `EventArgs` subclass if needed
3. Invoke with `self.event_name.invoke(self, args)`
4. Add handler registration in setup code