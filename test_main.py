import pytest
import json
import os
from main import app, progress_data, PROGRESS_FILE

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def cleanup():
    """Clean up progress data before and after each test"""
    # Clear in-memory data
    progress_data.clear()
    
    # Remove progress file if it exists
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
    
    yield
    
    # Clean up after test
    progress_data.clear()
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)

def test_index_route(client):
    """Test the index (/) route"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'endpoints' in data
    assert data['message'] == "Welcome to the Progress API"

def test_get_progress_empty(client):
    """Test GET /api/progress with no data"""
    response = client.get('/api/progress')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data'] == []

def test_post_progress_valid(client):
    """Test POST /api/progress with valid data"""
    test_data = {
        "task": "Implement Flask API",
        "status": "completed",
        "percentage": 100
    }
    
    response = client.post('/api/progress',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['message'] == "Progress saved successfully"
    assert data['data'] == test_data

def test_post_progress_no_data(client):
    """Test POST /api/progress with no data"""
    response = client.post('/api/progress',
                          data=json.dumps(None),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'error' in data

def test_get_progress_after_post(client):
    """Test GET /api/progress after posting data"""
    test_data = {
        "task": "Write tests",
        "status": "in progress",
        "percentage": 50
    }
    
    # Post data
    client.post('/api/progress',
               data=json.dumps(test_data),
               content_type='application/json')
    
    # Get data
    response = client.get('/api/progress')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['data']) == 1
    assert data['data'][0] == test_data

def test_multiple_progress_entries(client):
    """Test posting multiple progress entries"""
    entries = [
        {"task": "Task 1", "status": "completed"},
        {"task": "Task 2", "status": "in progress"},
        {"task": "Task 3", "status": "pending"}
    ]
    
    for entry in entries:
        response = client.post('/api/progress',
                              data=json.dumps(entry),
                              content_type='application/json')
        assert response.status_code == 201
    
    # Verify all entries are stored
    response = client.get('/api/progress')
    data = json.loads(response.data)
    assert len(data['data']) == 3
    assert data['data'] == entries

def test_progress_persistence(client):
    """Test that progress data persists to file"""
    test_data = {"task": "Test persistence", "status": "saved"}
    
    # Post data
    client.post('/api/progress',
               data=json.dumps(test_data),
               content_type='application/json')
    
    # Check that file was created
    assert os.path.exists(PROGRESS_FILE)
    
    # Read file and verify content
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        file_data = json.load(f)
    
    assert len(file_data) == 1
    assert file_data[0] == test_data
