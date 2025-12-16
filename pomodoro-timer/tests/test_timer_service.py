"""TimerService のユニットテスト"""
import pytest
from pomodoro.services.timer_service import TimerService


class TestTimerService:
    """TimerServiceクラスのテスト"""

    @pytest.fixture
    def service(self):
        """テスト用のTimerServiceインスタンス"""
        return TimerService({
            'pomodoro': 25,
            'short_break': 5,
            'long_break': 15
        })

    # get_duration のテスト
    def test_get_duration_pomodoro(self, service):
        """ポモドーロモードの時間取得"""
        assert service.get_duration('pomodoro') == 25 * 60

    def test_get_duration_short_break(self, service):
        """短い休憩モードの時間取得"""
        assert service.get_duration('short_break') == 5 * 60

    def test_get_duration_long_break(self, service):
        """長い休憩モードの時間取得"""
        assert service.get_duration('long_break') == 15 * 60

    def test_get_duration_unknown_mode(self, service):
        """不明なモードの場合は0を返す"""
        assert service.get_duration('unknown') == 0

    # should_take_long_break のテスト
    def test_should_take_long_break_at_4(self, service):
        """4回完了時は長い休憩"""
        assert service.should_take_long_break(4) is True

    def test_should_take_long_break_at_8(self, service):
        """8回完了時は長い休憩"""
        assert service.should_take_long_break(8) is True

    def test_should_not_take_long_break_at_1(self, service):
        """1回完了時は長い休憩ではない"""
        assert service.should_take_long_break(1) is False

    def test_should_not_take_long_break_at_3(self, service):
        """3回完了時は長い休憩ではない"""
        assert service.should_take_long_break(3) is False

    def test_should_not_take_long_break_at_0(self, service):
        """0回完了時は長い休憩ではない"""
        assert service.should_take_long_break(0) is False

    # get_next_mode のテスト
    def test_get_next_mode_from_pomodoro_to_short_break(self, service):
        """ポモドーロ完了後、4の倍数でなければ短い休憩"""
        assert service.get_next_mode('pomodoro', 1) == 'short_break'
        assert service.get_next_mode('pomodoro', 2) == 'short_break'
        assert service.get_next_mode('pomodoro', 3) == 'short_break'

    def test_get_next_mode_from_pomodoro_to_long_break(self, service):
        """ポモドーロ完了後、4の倍数なら長い休憩"""
        assert service.get_next_mode('pomodoro', 4) == 'long_break'
        assert service.get_next_mode('pomodoro', 8) == 'long_break'

    def test_get_next_mode_from_short_break_to_pomodoro(self, service):
        """短い休憩後はポモドーロ"""
        assert service.get_next_mode('short_break', 1) == 'pomodoro'

    def test_get_next_mode_from_long_break_to_pomodoro(self, service):
        """長い休憩後はポモドーロ"""
        assert service.get_next_mode('long_break', 4) == 'pomodoro'

    # format_time のテスト
    def test_format_time_25_minutes(self, service):
        """25分のフォーマット"""
        assert service.format_time(1500) == '25:00'

    def test_format_time_5_minutes(self, service):
        """5分のフォーマット"""
        assert service.format_time(300) == '05:00'

    def test_format_time_zero(self, service):
        """0秒のフォーマット"""
        assert service.format_time(0) == '00:00'

    def test_format_time_with_seconds(self, service):
        """秒を含むフォーマット"""
        assert service.format_time(90) == '01:30'
        assert service.format_time(65) == '01:05'

    # calculate_progress のテスト
    def test_calculate_progress_at_start(self, service):
        """開始時の進捗は0%"""
        assert service.calculate_progress(1500, 1500) == 0

    def test_calculate_progress_at_half(self, service):
        """半分経過時の進捗は50%"""
        assert service.calculate_progress(750, 1500) == 50

    def test_calculate_progress_at_end(self, service):
        """終了時の進捗は100%"""
        assert service.calculate_progress(0, 1500) == 100

    def test_calculate_progress_with_zero_total(self, service):
        """合計が0の場合は0%"""
        assert service.calculate_progress(0, 0) == 0
