"""
設定マネージャー - ゲームの設定を管理するクラス
Settings Manager - Class for managing game settings
"""
import json
import os
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class GameSettings:
    """ゲーム設定データクラス / Game settings data class"""
    
    # ゲーム設定 / Game settings
    spawn_recipe_timer_max: float = 4.0
    waiting_recipes_max: int = 4
    game_duration: int = 60  # 秒 / seconds
    
    # 視覚設定 / Visual settings
    enable_colors: bool = True
    enable_animations: bool = True
    enable_sound_effects: bool = False
    
    # 通知設定 / Notification settings
    enable_notifications: bool = True
    notification_level: str = "all"  # "all", "important", "none"
    
    # デバッグ設定 / Debug settings
    debug_mode: bool = False
    verbose_logging: bool = False


class SettingsManager:
    """設定管理クラス（Singleton） / Settings management class (Singleton)"""
    
    _instance: Optional['SettingsManager'] = None
    _settings_file: str = "game_settings.json"
    
    def __init__(self):
        self._settings = GameSettings()
        self._load_settings()
    
    @classmethod
    def get_instance(cls) -> 'SettingsManager':
        """Singletonインスタンスを取得 / Get Singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _load_settings(self):
        """設定ファイルから設定を読み込む / Load settings from file"""
        if os.path.exists(self._settings_file):
            try:
                with open(self._settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 既存の設定を更新
                    for key, value in data.items():
                        if hasattr(self._settings, key):
                            setattr(self._settings, key, value)
            except (json.JSONDecodeError, IOError) as e:
                print(f"設定ファイルの読み込みに失敗しました / Failed to load settings: {e}")
    
    def save_settings(self):
        """設定をファイルに保存 / Save settings to file"""
        try:
            with open(self._settings_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self._settings), f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"設定ファイルの保存に失敗しました / Failed to save settings: {e}")
    
    def get_setting(self, key: str) -> Any:
        """設定値を取得 / Get setting value"""
        return getattr(self._settings, key, None)
    
    def set_setting(self, key: str, value: Any):
        """設定値を更新 / Update setting value"""
        if hasattr(self._settings, key):
            setattr(self._settings, key, value)
    
    def get_all_settings(self) -> Dict[str, Any]:
        """すべての設定を取得 / Get all settings"""
        return asdict(self._settings)
    
    def reset_to_defaults(self):
        """設定をデフォルトに戻す / Reset settings to defaults"""
        self._settings = GameSettings()
        self.save_settings()


# 使用例 / Usage example
if __name__ == "__main__":
    # 設定マネージャーのインスタンスを取得
    settings = SettingsManager.get_instance()
    
    # 設定を表示
    print("現在の設定 / Current settings:")
    for key, value in settings.get_all_settings().items():
        print(f"  {key}: {value}")
    
    # 設定を変更
    print("\n設定を変更します / Changing settings...")
    settings.set_setting("spawn_recipe_timer_max", 3.0)
    settings.set_setting("enable_animations", True)
    
    # 設定を保存
    settings.save_settings()
    print("設定を保存しました / Settings saved!")
    
    # 変更後の設定を表示
    print("\n変更後の設定 / Updated settings:")
    print(f"  spawn_recipe_timer_max: {settings.get_setting('spawn_recipe_timer_max')}")
    print(f"  enable_animations: {settings.get_setting('enable_animations')}")
