from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# In-memory storage for progress data
progress_data = []

# File path for persistence
PROGRESS_FILE = 'progress.json'

# Load progress from file if it exists
def load_progress():
    global progress_data
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                progress_data = json.load(f)
        except Exception as e:
            print(f"Error loading progress: {e}")
            progress_data = []

# Save progress to file
def save_progress():
    try:
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving progress: {e}")

# Load progress on startup
load_progress()

@app.route('/')
def index():
    """Top page route"""
    return jsonify({
        "message": "Welcome to the Progress API",
        "endpoints": {
            "/": "This page",
            "/api/progress": "GET - Retrieve progress data, POST - Save progress data"
        }
    })

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get progress data"""
    return jsonify({
        "success": True,
        "data": progress_data
    })

@app.route('/api/progress', methods=['POST'])
def post_progress():
    """Save progress data"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        progress_data.append(data)
        save_progress()
        
        return jsonify({
            "success": True,
            "message": "Progress saved successfully",
            "data": data
        }), 201
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
