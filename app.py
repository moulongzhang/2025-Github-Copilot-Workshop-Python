from flask import Flask, render_template, request, jsonify
from datetime import datetime
from models import SessionRepository
from timer_service import get_today_sessions, calculate_total_focus_minutes, format_focus_time


def create_app(config: dict = None) -> Flask:
    app = Flask(__name__)

    if config:
        app.config.update(config)

    app.config.setdefault("DATA_FILE", "sessions.json")

    register_routes(app)
    return app


def register_routes(app: Flask) -> None:
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/sessions", methods=["GET"])
    def get_sessions():
        date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
        repo = SessionRepository(app.config["DATA_FILE"])
        sessions = repo.find_by_date(date)
        total_minutes = calculate_total_focus_minutes(sessions)
        return jsonify({
            "sessions": sessions,
            "count": len(sessions),
            "total_minutes": total_minutes,
            "focus_time": format_focus_time(total_minutes),
        })

    @app.route("/api/sessions", methods=["POST"])
    def post_session():
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "リクエストボディが空です"}), 400

        required_fields = ["date", "duration_minutes", "completed_at"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} は必須です"}), 400

        session = {
            "date": data["date"],
            "duration_minutes": int(data["duration_minutes"]),
            "completed_at": data["completed_at"],
        }

        repo = SessionRepository(app.config["DATA_FILE"])
        repo.save(session)
        return jsonify(session), 201


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
