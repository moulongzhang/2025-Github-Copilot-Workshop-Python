import pytest
from pomodoro_timer import PomodoroTimer, TimerState

def test_initial_state():
    timer = PomodoroTimer()
    assert timer.get_state() == TimerState.STOPPED
    assert timer.get_remaining() == 25*60
    assert timer.get_session_count() == 0

def test_start_and_tick():
    timer = PomodoroTimer()
    timer.start()
    assert timer.get_state() == TimerState.WORKING
    timer.tick(10)
    assert timer.get_remaining() == 25*60 - 10

def test_work_to_break_transition():
    timer = PomodoroTimer(work_duration=3, break_duration=2)
    timer.start()
    timer.tick(3)
    assert timer.get_state() == TimerState.BREAK
    assert timer.get_remaining() == 2
    assert timer.get_session_count() == 1

def test_break_to_stopped():
    timer = PomodoroTimer(work_duration=3, break_duration=2)
    timer.start()
    timer.tick(3)  # work終了→break
    timer.tick(2)  # break終了→stopped
    assert timer.get_state() == TimerState.STOPPED
    assert timer.get_remaining() == 0

def test_pause_and_reset():
    timer = PomodoroTimer()
    timer.start()
    timer.tick(5)
    timer.pause()
    assert timer.get_state() == TimerState.STOPPED
    timer.reset()
    assert timer.get_state() == TimerState.STOPPED
    assert timer.get_remaining() == 25*60
