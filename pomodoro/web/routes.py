from flask import Blueprint, render_template, jsonify, request
from pomodoro.services.timer_service import TimerService

bp = Blueprint("pomodoro", __name__)

# シンプルにプロセスローカルなサービスを使う（後でDIに変えられる）
service = TimerService()


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/api/timer/start", methods=["POST"])
def api_start():
    state = service.start()
    return jsonify(state)


@bp.route("/api/timer/pause", methods=["POST"])
def api_pause():
    state = service.pause()
    return jsonify(state)


@bp.route("/api/timer/reset", methods=["POST"])
def api_reset():
    data = request.get_json(silent=True) or {}
    duration = data.get("duration")
    state = service.reset(duration)
    return jsonify(state)


@bp.route("/api/timer/state", methods=["GET"])
def api_state():
    return jsonify(service.get_state())


@bp.route("/api/timer/set_remaining", methods=["POST"])
def api_set_remaining():
    """デバッグ用: 残り秒数を直接セットする。JSON: {"seconds": <int>}"""
    data = request.get_json(silent=True) or {}
    seconds = data.get("seconds")
    if seconds is None:
        return jsonify({"error": "seconds required"}), 400
    state = service.set_remaining(seconds)
    return jsonify(state)
