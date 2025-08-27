"""
SocketIOのテスト
"""
from app import socketio, app


class TestSocketIO:
    """SocketIOのテストクラス"""

    def test_connect_event(self, socketio_client):
        """接続イベントのテスト"""
        received = socketio_client.get_received()
        assert len(received) == 1
        assert received[0]['name'] == 'connected'
        assert 'サーバーに正常に接続されました' in received[0]['args'][0]['message']

    def test_timer_state_broadcast(self, socketio_client):
        """タイマー状態配信のテスト"""
        test_timer_data = {
            'mode': 'work',
            'timeRemaining': 1500,
            'isRunning': True,
            'sessionCount': 2
        }
        
        # 別のクライアントを作成
        client2 = socketio.test_client(app, flask_test_client=app.test_client())
        
        # タイマー状態を送信
        socketio_client.emit('timer_state', test_timer_data)
        
        # 2番目のクライアントが更新を受信することを確認
        received = client2.get_received()
        # 接続イベント + タイマー更新を受信するはず
        timer_updates = [msg for msg in received if msg['name'] == 'timer_update']
        assert len(timer_updates) >= 1
        assert timer_updates[0]['args'][0] == test_timer_data

    def test_disconnect_event(self, socketio_client):
        """切断イベントのテスト"""
        # 明示的に切断
        socketio_client.disconnect()
        
        # 切断が正常に行われることを確認
        assert not socketio_client.is_connected()
