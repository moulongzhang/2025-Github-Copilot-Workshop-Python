from flask import Flask, render_template
from config import DevelopmentConfig


def create_app(config_object=DevelopmentConfig):
	app = Flask(__name__, template_folder='templates', static_folder='static')
	app.config.from_object(config_object)

	@app.route('/')
	def index():
		return render_template('index.html')

	return app


if __name__ == '__main__':
	app = create_app()
	app.run(host='127.0.0.1', port=5000)

