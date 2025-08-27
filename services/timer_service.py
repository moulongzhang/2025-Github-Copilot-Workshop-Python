"""
ポモドーロタイマーのサービス層
ビジネスロジックとデータ処理を担当
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class HistoryService:
    """履歴管理を担当するサービス"""
    
    def __init__(self, history_file: str = 'pomodoro_history.json'):
        self.history_file = history_file
    
    def load_history(self) -> List[Dict]:
        """履歴データを読み込む"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"履歴読み込みエラー: {e}")
                return []
        return []
    
    def save_history(self, history: List[Dict]) -> bool:
        """履歴データを保存する"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"履歴保存エラー: {e}")
            return False
    
    def add_history_entry(self, session_type: str, duration: int, pomodoro_count: int) -> Optional[Dict]:
        """履歴エントリを追加する"""
        try:
            # 履歴エントリを作成
            history_entry = {
                'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
                'session_type': session_type,
                'duration': duration,
                'completed_at': datetime.now().isoformat(),
                'pomodoro_count': pomodoro_count
            }
            
            # 既存の履歴を読み込み
            history = self.load_history()
            history.append(history_entry)
            
            # 最新の100件のみ保持
            history = history[-100:]
            
            if self.save_history(history):
                return history_entry
            else:
                return None
                
        except Exception as e:
            print(f"履歴追加エラー: {e}")
            return None
    
    def get_statistics(self) -> Dict:
        """統計データを計算する"""
        try:
            history = self.load_history()
            
            # 基本統計
            total_pomodoros = len([h for h in history if h['session_type'] == 'work'])
            total_work_time = sum(h['duration'] for h in history if h['session_type'] == 'work')
            total_break_time = sum(h['duration'] for h in history if h['session_type'] == 'break')
            
            # 今日の統計
            today = datetime.now().strftime('%Y-%m-%d')
            today_history = [h for h in history if h['completed_at'].startswith(today)]
            today_pomodoros = len([h for h in today_history if h['session_type'] == 'work'])
            
            return {
                'total_pomodoros': total_pomodoros,
                'total_work_time': total_work_time,
                'total_break_time': total_break_time,
                'today_pomodoros': today_pomodoros,
                'total_sessions': len(history)
            }
            
        except Exception as e:
            print(f"統計計算エラー: {e}")
            return {
                'total_pomodoros': 0,
                'total_work_time': 0,
                'total_break_time': 0,
                'today_pomodoros': 0,
                'total_sessions': 0
            }


class TimerService:
    """タイマー関連のビジネスロジックを担当するサービス"""
    
    @staticmethod
    def validate_timer_settings(work_minutes: int, short_break_minutes: int, long_break_minutes: int) -> tuple[bool, List[str]]:
        """タイマー設定の検証"""
        errors = []
        
        if not isinstance(work_minutes, int) or work_minutes <= 0:
            errors.append("作業時間は正の整数である必要があります")
        elif work_minutes > 60:
            errors.append("作業時間は60分以下にしてください")
            
        if not isinstance(short_break_minutes, int) or short_break_minutes <= 0:
            errors.append("短い休憩時間は正の整数である必要があります")
        elif short_break_minutes > 30:
            errors.append("短い休憩時間は30分以下にしてください")
            
        if not isinstance(long_break_minutes, int) or long_break_minutes <= 0:
            errors.append("長い休憩時間は正の整数である必要があります")
        elif long_break_minutes > 60:
            errors.append("長い休憩時間は60分以下にしてください")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def format_time(total_seconds: int) -> str:
        """秒を MM:SS 形式に変換"""
        if total_seconds < 0:
            total_seconds = 0
            
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    @staticmethod
    def calculate_break_duration(completed_pomodoros: int, short_break_time: int, long_break_time: int) -> int:
        """完了したポモドーロ数に基づいて休憩時間を計算"""
        return long_break_time if completed_pomodoros % 4 == 0 and completed_pomodoros > 0 else short_break_time
    
    @staticmethod
    def get_session_type_display(session_type: str, completed_pomodoros: int) -> str:
        """セッションタイプの表示名を取得"""
        if session_type == 'work':
            return '作業中'
        else:
            is_long_break = completed_pomodoros % 4 == 0 and completed_pomodoros > 0
            return '長い休憩中' if is_long_break else '休憩中'
