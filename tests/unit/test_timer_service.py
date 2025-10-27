from pomodoro.services.timer_service import TimerService


def test_service_start_reset_get_state():
    svc = TimerService()
    st0 = svc.get_state()
    assert st0["status"] == "stopped"

    st1 = svc.start()
    assert st1["status"] == "running"

    st2 = svc.reset()
    assert st2["status"] == "stopped"
    assert st2["remaining"] == st2["duration"]
