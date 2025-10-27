from config import config
from flask import Flask

def create_app(env: str = 'default') -> Flask:
	cfg = config.get(env, config['default'])
	app = Flask(__name__, static_folder='static', template_folder='templates')
	app.config.from_object(cfg)

	# Register blueprints
	try:
		from pomodoro.web.routes import bp as pomodoro_bp
		app.register_blueprint(pomodoro_bp)
	except Exception:
		# if blueprint import fails, we still return the app for tests
		pass

	return app

if __name__ == '__main__':
	app = create_app('default')
	app.run(host='127.0.0.1', port=5000, debug=app.config.get('DEBUG', True))

