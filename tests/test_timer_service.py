"""
タイマーサービスのユニットテスト
"""
import pytest
import tempfile
import os
import json
from unittest.mock import patch
from services.timer_service import HistoryService, TimerService


class TestHistoryService:
    """HistoryServiceのテストクラス"""
    
    def setup_method(self):
        """各テストメソッドの前に実行される"""
        # 一時ファイルを作成
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.history_service = HistoryService(self.temp_file.name)
    
    def teardown_method(self):
        """各テストメソッドの後に実行される"""
        # 一時ファイルを削除
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_load_empty_history(self):
        """空の履歴ファイルの読み込みテスト"""
        history = self.history_service.load_history()
        assert history == []
    
    def test_save_and_load_history(self):
        """履歴の保存と読み込みテスト"""
        test_history = [
            {
                'id': '20250827_120000',
                'session_type': 'work',
                'duration': 1500,
                'completed_at': '2025-08-27T12:00:00',
                'pomodoro_count': 1
            }
        ]
        
        # 保存
        result = self.history_service.save_history(test_history)
        assert result is True
        
        # 読み込み
        loaded_history = self.history_service.load_history()
        assert loaded_history == test_history
    
    def test_add_history_entry(self):
        """履歴エントリ追加テスト"""
        with patch('services.timer_service.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = '20250827_120000'
            mock_datetime.now.return_value.isoformat.return_value = '2025-08-27T12:00:00'
            
            entry = self.history_service.add_history_entry('work', 1500, 1)
            
            assert entry is not None
            assert entry['session_type'] == 'work'
            assert entry['duration'] == 1500
            assert entry['pomodoro_count'] == 1
    
    def test_get_statistics(self):
        """統計情報取得テスト"""
        # テストデータを準備
        test_history = [
            {
                'session_type': 'work',
                'duration': 1500,
                'completed_at': '2025-08-27T12:00:00'
            },
            {
                'session_type': 'break',
                'duration': 300,
                'completed_at': '2025-08-27T12:25:00'
            }
        ]
        
        self.history_service.save_history(test_history)
        
        with patch('services.timer_service.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = '2025-08-27'
            
            stats = self.history_service.get_statistics()
            
            assert stats['total_pomodoros'] == 1
            assert stats['total_work_time'] == 1500
            assert stats['total_break_time'] == 300
            assert stats['total_sessions'] == 2


class TestTimerService:
    """TimerServiceのテストクラス"""
    
    def test_validate_timer_settings_valid(self):
        """有効な設定値のテスト"""
        is_valid, errors = TimerService.validate_timer_settings(25, 5, 15)
        assert is_valid is True
        assert len(errors) == 0
    
    def test_validate_timer_settings_invalid_work_time(self):
        """無効な作業時間のテスト"""
        is_valid, errors = TimerService.validate_timer_settings(-1, 5, 15)
        assert is_valid is False
        assert "作業時間は正の整数である必要があります" in errors
    
    def test_validate_timer_settings_work_time_too_long(self):
        """作業時間が長すぎる場合のテスト"""
        is_valid, errors = TimerService.validate_timer_settings(65, 5, 15)
        assert is_valid is False
        assert "作業時間は60分以下にしてください" in errors
    
    def test_format_time(self):
        """時間フォーマットのテスト"""
        assert TimerService.format_time(0) == "00:00"
        assert TimerService.format_time(59) == "00:59"
        assert TimerService.format_time(60) == "01:00"
        assert TimerService.format_time(1500) == "25:00"
        assert TimerService.format_time(-10) == "00:00"  # 負の値は0として扱う
    
    def test_calculate_break_duration(self):
        """休憩時間計算のテスト"""
        # 短い休憩
        duration = TimerService.calculate_break_duration(1, 300, 900)
        assert duration == 300
        
        # 長い休憩（4の倍数）
        duration = TimerService.calculate_break_duration(4, 300, 900)
        assert duration == 900
        
        # ポモドーロ0の場合は短い休憩
        duration = TimerService.calculate_break_duration(0, 300, 900)
        assert duration == 300
    
    def test_get_session_type_display(self):
        """セッションタイプ表示名のテスト"""
        assert TimerService.get_session_type_display('work', 1) == '作業中'
        assert TimerService.get_session_type_display('break', 1) == '休憩中'
        assert TimerService.get_session_type_display('break', 4) == '長い休憩中'


class TestTimerUtilities:
    """タイマーユーティリティ関数のテスト（既存のテストを保持）"""
    
    def test_seconds_to_minutes_seconds(self):
        """秒を分:秒形式に変換する関数のテスト"""
        
        def seconds_to_mm_ss(total_seconds):
            """秒を MM:SS 形式に変換"""
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes:02d}:{seconds:02d}"
        
        # テストケース
        assert seconds_to_mm_ss(0) == "00:00"
        assert seconds_to_mm_ss(59) == "00:59"
        assert seconds_to_mm_ss(60) == "01:00"
        assert seconds_to_mm_ss(61) == "01:01"
        assert seconds_to_mm_ss(1500) == "25:00"
        assert seconds_to_mm_ss(3661) == "61:01"
    
    def test_validate_timer_settings(self):
        """タイマー設定の検証テスト"""
        
        def validate_timer_settings(work_minutes, break_minutes, long_break_minutes):
            """タイマー設定値の検証"""
            errors = []
            
            if not isinstance(work_minutes, int) or work_minutes <= 0:
                errors.append("作業時間は正の整数である必要があります")
            
            if not isinstance(break_minutes, int) or break_minutes <= 0:
                errors.append("休憩時間は正の整数である必要があります")
                
            if not isinstance(long_break_minutes, int) or long_break_minutes <= 0:
                errors.append("長い休憩時間は正の整数である必要があります")
            
            if work_minutes > 60:
                errors.append("作業時間は60分以下にしてください")
                
            return len(errors) == 0, errors
        
        # 正常なケース
        valid, errors = validate_timer_settings(25, 5, 15)
        assert valid is True
        assert len(errors) == 0
        
        # 異常なケース
        valid, errors = validate_timer_settings(-1, 5, 15)
        assert valid is False
        assert "作業時間は正の整数である必要があります" in errors
        
        # 境界値テスト
        valid, errors = validate_timer_settings(61, 5, 15)
        assert valid is False
        assert "作業時間は60分以下にしてください" in errors
