"""API統合テスト"""
import unittest
import json
from main import app, delivery_manager, game_manager


class TestAPIIntegration(unittest.TestCase):
    """フロントエンドとAPIの統合テスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.app = app.test_client()
        self.app.testing = True
        game_manager.start_game()
    
    def test_get_progress(self):
        """進捗データ取得のテスト"""
        response = self.app.get('/api/progress')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('successful_recipes', data['data'])
        self.assertIn('waiting_recipes_count', data['data'])
    
    def test_get_recipes(self):
        """レシピリスト取得のテスト"""
        response = self.app.get('/api/recipes')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['data'], list)
    
    def test_deliver_recipe_success(self):
        """レシピ配達成功のテスト"""
        response = self.app.post(
            '/api/deliver',
            data=json.dumps({'ingredients': ['Lettuce', 'Tomato']}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('delivered', data['data'])
    
    def test_deliver_recipe_invalid_ingredient(self):
        """無効な材料でのエラーハンドリングテスト"""
        response = self.app.post(
            '/api/deliver',
            data=json.dumps({'ingredients': ['InvalidIngredient']}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_deliver_recipe_missing_data(self):
        """データ不足時のエラーハンドリングテスト"""
        response = self.app.post(
            '/api/deliver',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_start_game(self):
        """ゲーム開始のテスト"""
        response = self.app.post('/api/start')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_stop_game(self):
        """ゲーム停止のテスト"""
        response = self.app.post('/api/stop')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])


if __name__ == '__main__':
    unittest.main()
