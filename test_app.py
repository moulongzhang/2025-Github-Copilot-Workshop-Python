import unittest
from app import app

class TestPomodoroApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('ポモドーロタイマー', html)
        self.assertIn('id="timer-display"', html)
        self.assertIn('id="start-btn"', html)
        self.assertIn('id="stop-btn"', html)
        self.assertIn('id="reset-btn"', html)

if __name__ == '__main__':
    unittest.main()
