"""
通知システム - ゲームイベントの通知を管理
Notification System - Manages game event notifications
"""
from typing import List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class NotificationLevel(Enum):
    """通知レベル / Notification level"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class Notification:
    """通知データクラス / Notification data class"""
    message: str
    level: NotificationLevel
    timestamp: datetime
    category: str = "general"
    
    def __str__(self):
        time_str = self.timestamp.strftime("%H:%M:%S")
        return f"[{time_str}] [{self.level.value.upper()}] {self.message}"


class NotificationSystem:
    """通知システムクラス（Singleton） / Notification system class (Singleton)"""
    
    _instance: Optional['NotificationSystem'] = None
    
    def __init__(self):
        self._notifications: List[Notification] = []
        self._max_notifications = 50  # 保存する通知の最大数
        self._subscribers: List[Callable[[Notification], None]] = []
    
    @classmethod
    def get_instance(cls) -> 'NotificationSystem':
        """Singletonインスタンスを取得 / Get Singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def add_notification(self, message: str, level: NotificationLevel = NotificationLevel.INFO, 
                        category: str = "general"):
        """通知を追加 / Add notification"""
        notification = Notification(
            message=message,
            level=level,
            timestamp=datetime.now(),
            category=category
        )
        
        self._notifications.append(notification)
        
        # 最大数を超えたら古い通知を削除
        if len(self._notifications) > self._max_notifications:
            self._notifications.pop(0)
        
        # 購読者に通知
        self._notify_subscribers(notification)
    
    def subscribe(self, callback: Callable[[Notification], None]):
        """通知の購読を登録 / Subscribe to notifications"""
        if callback not in self._subscribers:
            self._subscribers.append(callback)
    
    def unsubscribe(self, callback: Callable[[Notification], None]):
        """通知の購読を解除 / Unsubscribe from notifications"""
        if callback in self._subscribers:
            self._subscribers.remove(callback)
    
    def _notify_subscribers(self, notification: Notification):
        """購読者に通知を送信 / Notify subscribers"""
        for subscriber in self._subscribers:
            try:
                subscriber(notification)
            except Exception as e:
                print(f"通知の配信中にエラーが発生しました / Error during notification delivery: {e}")
    
    def get_notifications(self, level: Optional[NotificationLevel] = None, 
                         category: Optional[str] = None) -> List[Notification]:
        """通知を取得（フィルタリング可能） / Get notifications (filterable)"""
        notifications = self._notifications.copy()
        
        if level:
            notifications = [n for n in notifications if n.level == level]
        
        if category:
            notifications = [n for n in notifications if n.category == category]
        
        return notifications
    
    def get_recent_notifications(self, count: int = 10) -> List[Notification]:
        """最新の通知を取得 / Get recent notifications"""
        return self._notifications[-count:] if len(self._notifications) > count else self._notifications.copy()
    
    def clear_notifications(self):
        """すべての通知をクリア / Clear all notifications"""
        self._notifications.clear()
    
    def get_notification_count(self) -> int:
        """通知の総数を取得 / Get total notification count"""
        return len(self._notifications)


# 便利な通知メソッド / Convenience notification methods
def notify_info(message: str, category: str = "general"):
    """情報通知 / Info notification"""
    NotificationSystem.get_instance().add_notification(message, NotificationLevel.INFO, category)


def notify_success(message: str, category: str = "general"):
    """成功通知 / Success notification"""
    NotificationSystem.get_instance().add_notification(message, NotificationLevel.SUCCESS, category)


def notify_warning(message: str, category: str = "general"):
    """警告通知 / Warning notification"""
    NotificationSystem.get_instance().add_notification(message, NotificationLevel.WARNING, category)


def notify_error(message: str, category: str = "general"):
    """エラー通知 / Error notification"""
    NotificationSystem.get_instance().add_notification(message, NotificationLevel.ERROR, category)


# 使用例 / Usage example
if __name__ == "__main__":
    # 通知システムのインスタンスを取得
    notification_system = NotificationSystem.get_instance()
    
    # 通知の購読
    def print_notification(notification: Notification):
        print(notification)
    
    notification_system.subscribe(print_notification)
    
    # 各種通知を送信
    print("=== 通知システムのテスト / Notification System Test ===\n")
    
    notify_info("ゲームを開始しました / Game started", "game")
    notify_success("レシピを配達しました！ / Recipe delivered!", "delivery")
    notify_warning("時間が残り少なくなっています / Time is running out", "timer")
    notify_info("新しいレシピが生成されました / New recipe spawned", "recipe")
    notify_error("配達に失敗しました / Delivery failed", "delivery")
    
    # 通知の統計を表示
    print(f"\n総通知数 / Total notifications: {notification_system.get_notification_count()}")
    
    # カテゴリ別の通知を表示
    print("\n配達関連の通知 / Delivery notifications:")
    for notification in notification_system.get_notifications(category="delivery"):
        print(f"  - {notification}")
    
    # 最新の通知を取得
    print("\n最新の3件の通知 / Recent 3 notifications:")
    for notification in notification_system.get_recent_notifications(3):
        print(f"  - {notification}")
