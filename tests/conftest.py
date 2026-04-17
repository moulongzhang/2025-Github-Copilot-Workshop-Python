import pytest
from app import create_app


@pytest.fixture
def client(tmp_path):
    data_file = str(tmp_path / "sessions.json")
    app = create_app({"TESTING": True, "DATA_FILE": data_file})
    with app.test_client() as client:
        yield client
