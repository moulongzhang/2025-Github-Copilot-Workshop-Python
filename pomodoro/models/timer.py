import time
from dataclasses import dataclass, field


@dataclass
class Timer:
    """シンプルなタイマーモデル。

    - duration: 秒単位の設定時間（デフォルト25分）
    - remaining: 残り秒数
    - status: 'running'|'paused'|'stopped'
    """
    duration: int = 25 * 60
    remaining: int = field(init=False)
    status: str = field(default="stopped")
    _start_ts: float | None = field(default=None, init=False)

    def __post_init__(self):
        self.remaining = int(self.duration)

    def start(self) -> None:
        if self.status != "running":
            # 開始時刻を保存し、状態をrunningにする
            self._start_ts = time.time()
            self.status = "running"

    def pause(self) -> None:
        if self.status == "running":
            elapsed = time.time() - (self._start_ts or time.time())
            self.remaining = max(0, int(self.remaining - elapsed))
            self._start_ts = None
            self.status = "paused"

    def reset(self, duration: int | None = None) -> None:
        if duration is not None:
            self.duration = int(duration)
        self.remaining = int(self.duration)
        self.status = "stopped"
        self._start_ts = None

    def get_state(self) -> dict:
        """現在の状態を辞書で返す（残り時間は秒）。

        実行中の場合は経過時間を考慮して計算する。
        """
        remaining = int(self.remaining)
        if self.status == "running" and self._start_ts is not None:
            elapsed = time.time() - self._start_ts
            remaining = max(0, int(self.remaining - elapsed))

        # 残り時間が0になったら completed 状態に変更
        if remaining == 0 and self.status == "running":
            self.status = "completed"
            self._start_ts = None
            self.remaining = 0  # 残り時間を確実に0に設定

        return {
            "duration": int(self.duration),
            "remaining": int(remaining),
            "status": self.status,
        }
