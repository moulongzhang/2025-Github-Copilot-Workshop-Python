from pomodoro.models.timer import Timer


class TimerService:
    """タイマーに対するビジネスロジック層（非常に軽量）。"""

    def __init__(self, timer: Timer | None = None):
        self.timer = timer or Timer()

    def start(self) -> dict:
        self.timer.start()
        return self.get_state()

    def pause(self) -> dict:
        self.timer.pause()
        return self.get_state()

    def reset(self, duration: int | None = None) -> dict:
        self.timer.reset(duration)
        return self.get_state()

    def set_remaining(self, seconds: int) -> dict:
        """デバッグ用: 残り秒数を直接セットする"""
        try:
            sec = int(seconds)
        except Exception:
            sec = 0
        # clamp
        if sec < 0:
            sec = 0
        self.timer.remaining = sec
        # if timer was stopped, keep it stopped; caller may start it explicitly
        return self.get_state()

    def get_state(self) -> dict:
        return self.timer.get_state()
