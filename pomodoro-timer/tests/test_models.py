"""Models のユニットテスト"""
import pytest
from pomodoro.models import TimerSettings, TimerState


class TestTimerSettings:
    """TimerSettingsクラスのテスト"""

    def test_default_values(self):
        """デフォルト値が正しい"""
        settings = TimerSettings()
        assert settings.pomodoro == 25
        assert settings.short_break == 5
        assert settings.long_break == 15

    def test_custom_values(self):
        """カスタム値を設定できる"""
        settings = TimerSettings(pomodoro=30, short_break=10, long_break=20)
        assert settings.pomodoro == 30
        assert settings.short_break == 10
        assert settings.long_break == 20

    def test_to_dict(self):
        """辞書形式に変換できる"""
        settings = TimerSettings(pomodoro=25, short_break=5, long_break=15)
        result = settings.to_dict()
        assert result == {
            'pomodoro': 25,
            'shortBreak': 5,
            'longBreak': 15
        }

    def test_from_dict(self):
        """辞書から生成できる"""
        data = {'pomodoro': 30, 'shortBreak': 10, 'longBreak': 20}
        settings = TimerSettings.from_dict(data)
        assert settings.pomodoro == 30
        assert settings.short_break == 10
        assert settings.long_break == 20

    def test_from_dict_with_missing_keys(self):
        """辞書にキーがない場合はデフォルト値を使用"""
        data = {'pomodoro': 30}
        settings = TimerSettings.from_dict(data)
        assert settings.pomodoro == 30
        assert settings.short_break == 5  # デフォルト値
        assert settings.long_break == 15  # デフォルト値


class TestTimerState:
    """TimerStateクラスのテスト"""

    def test_default_values(self):
        """デフォルト値が正しい"""
        state = TimerState()
        assert state.mode == 'pomodoro'
        assert state.time_remaining == 1500
        assert state.is_running is False
        assert state.pomodoro_count == 0

    def test_custom_values(self):
        """カスタム値を設定できる"""
        state = TimerState(
            mode='short_break',
            time_remaining=300,
            is_running=True,
            pomodoro_count=3
        )
        assert state.mode == 'short_break'
        assert state.time_remaining == 300
        assert state.is_running is True
        assert state.pomodoro_count == 3

    def test_to_dict(self):
        """辞書形式に変換できる"""
        state = TimerState(
            mode='pomodoro',
            time_remaining=1200,
            is_running=True,
            pomodoro_count=2
        )
        result = state.to_dict()
        assert result == {
            'mode': 'pomodoro',
            'timeRemaining': 1200,
            'isRunning': True,
            'pomodoroCount': 2
        }
