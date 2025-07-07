from enum import Enum, auto

class TimerState(Enum):
    STOPPED = auto()
    WORKING = auto()
    BREAK = auto()

class PomodoroTimer:
    def __init__(self, work_duration=25*60, break_duration=5*60):
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.state = TimerState.STOPPED
        self.remaining = work_duration
        self.session_count = 0

    def start(self):
        if self.state == TimerState.STOPPED:
            self.state = TimerState.WORKING
            self.remaining = self.work_duration
        elif self.state == TimerState.BREAK:
            self.state = TimerState.WORKING
            self.remaining = self.work_duration
        # すでにWORKINGなら何もしない

    def pause(self):
        if self.state in (TimerState.WORKING, TimerState.BREAK):
            self.state = TimerState.STOPPED

    def reset(self):
        if self.state == TimerState.WORKING:
            self.remaining = self.work_duration
        elif self.state == TimerState.BREAK:
            self.remaining = self.break_duration
        else:
            self.remaining = self.work_duration
        self.state = TimerState.STOPPED

    def tick(self, seconds=1):
        if self.state in (TimerState.WORKING, TimerState.BREAK):
            self.remaining = max(0, self.remaining - seconds)
            if self.remaining == 0:
                if self.state == TimerState.WORKING:
                    self.state = TimerState.BREAK
                    self.remaining = self.break_duration
                    self.session_count += 1
                else:
                    self.state = TimerState.STOPPED

    def get_state(self):
        return self.state

    def get_remaining(self):
        return self.remaining

    def get_session_count(self):
        return self.session_count
