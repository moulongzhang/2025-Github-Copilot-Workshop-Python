"""タイマービジネスロジック - Flaskに依存しない純粋なPython"""
from typing import Literal


class TimerService:
    """純粋なビジネスロジック"""
    
    def __init__(self, settings: dict):
        """
        Args:
            settings: タイマー設定
                - pomodoro: ポモドーロ時間（分）
                - short_break: 短い休憩時間（分）
                - long_break: 長い休憩時間（分）
        """
        self.settings = settings
    
    def get_duration(self, mode: str) -> int:
        """
        モードに応じた時間（秒）を返す
        
        Args:
            mode: 'pomodoro', 'short_break', 'long_break' のいずれか
        
        Returns:
            int: 時間（秒）
        """
        durations = {
            'pomodoro': self.settings.get('pomodoro', 25) * 60,
            'short_break': self.settings.get('short_break', 5) * 60,
            'long_break': self.settings.get('long_break', 15) * 60,
        }
        return durations.get(mode, 0)
    
    def should_take_long_break(self, completed_count: int) -> bool:
        """
        長い休憩を取るべきか判定
        
        Args:
            completed_count: 完了したポモドーロ数
        
        Returns:
            bool: 長い休憩を取るべきならTrue
        """
        return completed_count > 0 and completed_count % 4 == 0
    
    def get_next_mode(
        self, 
        current_mode: str, 
        completed_count: int
    ) -> Literal['pomodoro', 'short_break', 'long_break']:
        """
        次のモードを取得
        
        Args:
            current_mode: 現在のモード
            completed_count: 完了したポモドーロ数
        
        Returns:
            str: 次のモード
        """
        if current_mode != 'pomodoro':
            return 'pomodoro'
        
        if self.should_take_long_break(completed_count):
            return 'long_break'
        
        return 'short_break'
    
    def format_time(self, seconds: int) -> str:
        """
        秒数を MM:SS 形式に変換
        
        Args:
            seconds: 秒数
        
        Returns:
            str: MM:SS 形式の文字列
        """
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"
    
    def calculate_progress(self, remaining: int, total: int) -> float:
        """
        進捗率を計算
        
        Args:
            remaining: 残り時間（秒）
            total: 合計時間（秒）
        
        Returns:
            float: 進捗率（0-100）
        """
        if total == 0:
            return 0
        return ((total - remaining) / total) * 100
