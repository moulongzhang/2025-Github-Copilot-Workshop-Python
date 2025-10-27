import time
from pomodoro.models.timer import Timer


def test_timer_initial_state():
    t = Timer()
    st = t.get_state()
    assert st["duration"] == 25 * 60
    assert st["remaining"] == 25 * 60
    assert st["status"] == "stopped"


def test_timer_start_and_elapsed():
    t = Timer()
    t.start()
    assert t.status == "running"
    # 少し待って経過を確認
    time.sleep(0.1)
    st = t.get_state()
    assert st["remaining"] <= t.duration


def test_timer_pause_and_reset():
    t = Timer()
    t.start()
    time.sleep(0.05)
    t.pause()
    assert t.status == "paused"
    rem_after_pause = t.get_state()["remaining"]
    assert rem_after_pause < t.duration

    t.reset()
    st = t.get_state()
    assert st["status"] == "stopped"
    assert st["remaining"] == st["duration"]


    def test_timer_completion():
        """タイマーが0になった時のcompletedステータスをテスト"""
        # 3秒のタイマーを作成
        t = Timer(duration=3)
        assert t.get_state()["remaining"] == 3
    
        # タイマーを開始
        t.start()
        assert t.status == "running"
    
        # 3秒以上待ってcompletedになることを確認
        time.sleep(3.1)
        st = t.get_state()
        assert st["status"] == "completed"
        assert st["remaining"] == 0


    def test_timer_completed_state_persistence():
        """completedステータスが永続的であることをテスト"""
        t = Timer(duration=1)
        t.start()
        time.sleep(1.1)
    
        # 最初のチェック
        st1 = t.get_state()
        assert st1["status"] == "completed"
        assert st1["remaining"] == 0
    
        # 少し待って再度チェック - 値が変化していないことを確認
        time.sleep(0.1)
        st2 = t.get_state()
        assert st2["status"] == "completed"
        assert st2["remaining"] == 0


    def test_timer_reset_from_completed():
        """completedステータスからのリセットをテスト"""
        t = Timer(duration=1)
        t.start()
        time.sleep(1.1)
    
        # completedになっていることを確認
        assert t.get_state()["status"] == "completed"
    
        # リセット
        t.reset()
        st = t.get_state()
        assert st["status"] == "stopped"
        assert st["remaining"] == st["duration"]
        assert t._start_ts is None
