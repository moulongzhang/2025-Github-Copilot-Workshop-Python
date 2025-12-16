"""データモデル"""
from dataclasses import dataclass
from typing import Literal


@dataclass
class TimerSettings:
    """タイマー設定を表すデータクラス"""
    pomodoro: int = 25  # 分
    short_break: int = 5  # 分
    long_break: int = 15  # 分
    
    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return {
            'pomodoro': self.pomodoro,
            'shortBreak': self.short_break,
            'longBreak': self.long_break
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TimerSettings':
        """辞書から生成"""
        return cls(
            pomodoro=data.get('pomodoro', 25),
            short_break=data.get('shortBreak', 5),
            long_break=data.get('longBreak', 15)
        )


@dataclass
class TimerState:
    """タイマーの状態を表すデータクラス"""
    mode: Literal['pomodoro', 'short_break', 'long_break'] = 'pomodoro'
    time_remaining: int = 1500  # 秒
    is_running: bool = False
    pomodoro_count: int = 0  # 完了したポモドーロ数
    
    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return {
            'mode': self.mode,
            'timeRemaining': self.time_remaining,
            'isRunning': self.is_running,
            'pomodoroCount': self.pomodoro_count
        }
