"""
Development server entry point
"""
import os
from app import create_app

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print(f"🍅 Starting Pomodoro Timer on http://{host}:{port}")
    print(f"   Debug mode: {debug}")
    print(f"   Environment: {os.getenv('FLASK_ENV', 'development')}")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )
