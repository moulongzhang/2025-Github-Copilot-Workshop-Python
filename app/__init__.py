"""
Pomodoro Timer Application Factory
"""
from flask import Flask, render_template
from flask_cors import CORS
import os


def create_app(config_name: str = None) -> Flask:
    """
    Application factory pattern for creating Flask app instances.
    
    Args:
        config_name: Configuration name ('development', 'testing', 'production')
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Basic configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # CORS configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": os.getenv('CORS_ORIGINS', 'http://localhost:5000').split(',')
        }
    })
    
    # Register blueprints (will be added in later stages)
    # from app.routes.main import main_bp
    # from app.routes.api import api_bp
    # app.register_blueprint(main_bp)
    # app.register_blueprint(api_bp, url_prefix='/api')
    
    # Basic route for testing
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'Pomodoro Timer API is running'}, 200
    
    return app
