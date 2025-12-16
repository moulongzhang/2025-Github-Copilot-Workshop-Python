/**
 * timerEngine.js のユニットテスト
 * Node.js環境で実行: node timerEngine.test.js
 */

// シンプルなテストフレームワーク
const assert = (condition, message) => {
    if (!condition) {
        throw new Error(`❌ ${message}`);
    }
    console.log(`✅ ${message}`);
};

const assertEqual = (actual, expected, message) => {
    if (actual !== expected) {
        throw new Error(`❌ ${message}: expected ${expected}, got ${actual}`);
    }
    console.log(`✅ ${message}`);
};

// TimerEngineをインポート
const TimerEngine = require('./timerEngine.js');

console.log('\n=== TimerEngine Tests ===\n');

// formatTime のテスト
console.log('--- formatTime ---');
assertEqual(TimerEngine.formatTime(1500), '25:00', '25分のフォーマット');
assertEqual(TimerEngine.formatTime(300), '05:00', '5分のフォーマット');
assertEqual(TimerEngine.formatTime(0), '00:00', '0秒のフォーマット');
assertEqual(TimerEngine.formatTime(90), '01:30', '1分30秒のフォーマット');
assertEqual(TimerEngine.formatTime(65), '01:05', '1分5秒のフォーマット');
assertEqual(TimerEngine.formatTime(9), '00:09', '9秒のフォーマット');

// calculateProgress のテスト
console.log('\n--- calculateProgress ---');
assertEqual(TimerEngine.calculateProgress(1500, 1500), 0, '開始時は0%');
assertEqual(TimerEngine.calculateProgress(750, 1500), 50, '半分で50%');
assertEqual(TimerEngine.calculateProgress(0, 1500), 100, '終了時は100%');
assertEqual(TimerEngine.calculateProgress(0, 0), 0, '合計0の場合は0%');

// calculateStrokeOffset のテスト
console.log('\n--- calculateStrokeOffset ---');
assertEqual(TimerEngine.calculateStrokeOffset(0, 628), 628, '進捗0%でオフセット628');
assertEqual(TimerEngine.calculateStrokeOffset(50, 628), 314, '進捗50%でオフセット314');
assertEqual(TimerEngine.calculateStrokeOffset(100, 628), 0, '進捗100%でオフセット0');

// getNextMode のテスト
console.log('\n--- getNextMode ---');
assertEqual(TimerEngine.getNextMode('pomodoro', 1), 'shortBreak', 'ポモドーロ1回後は短い休憩');
assertEqual(TimerEngine.getNextMode('pomodoro', 2), 'shortBreak', 'ポモドーロ2回後は短い休憩');
assertEqual(TimerEngine.getNextMode('pomodoro', 3), 'shortBreak', 'ポモドーロ3回後は短い休憩');
assertEqual(TimerEngine.getNextMode('pomodoro', 4), 'longBreak', 'ポモドーロ4回後は長い休憩');
assertEqual(TimerEngine.getNextMode('pomodoro', 8), 'longBreak', 'ポモドーロ8回後は長い休憩');
assertEqual(TimerEngine.getNextMode('shortBreak', 1), 'pomodoro', '短い休憩後はポモドーロ');
assertEqual(TimerEngine.getNextMode('longBreak', 4), 'pomodoro', '長い休憩後はポモドーロ');

// getModeLabel のテスト
console.log('\n--- getModeLabel ---');
assertEqual(TimerEngine.getModeLabel('pomodoro'), '作業中', 'ポモドーロは作業中');
assertEqual(TimerEngine.getModeLabel('shortBreak'), '短い休憩', '短い休憩');
assertEqual(TimerEngine.getModeLabel('longBreak'), '長い休憩', '長い休憩');
assertEqual(TimerEngine.getModeLabel('unknown'), '作業中', '不明な場合は作業中');

// getDuration のテスト
console.log('\n--- getDuration ---');
const settings = { pomodoro: 25, shortBreak: 5, longBreak: 15 };
assertEqual(TimerEngine.getDuration('pomodoro', settings), 1500, 'ポモドーロは25分=1500秒');
assertEqual(TimerEngine.getDuration('shortBreak', settings), 300, '短い休憩は5分=300秒');
assertEqual(TimerEngine.getDuration('longBreak', settings), 900, '長い休憩は15分=900秒');
assertEqual(TimerEngine.getDuration('unknown', settings), 1500, '不明な場合はデフォルト1500秒');

// formatTotalTime のテスト
console.log('\n--- formatTotalTime ---');
assertEqual(TimerEngine.formatTotalTime(0), '0分', '0分');
assertEqual(TimerEngine.formatTotalTime(25), '25分', '25分');
assertEqual(TimerEngine.formatTotalTime(60), '1時間0分', '1時間');
assertEqual(TimerEngine.formatTotalTime(100), '1時間40分', '1時間40分');
assertEqual(TimerEngine.formatTotalTime(150), '2時間30分', '2時間30分');

console.log('\n=== All tests passed! ===\n');
