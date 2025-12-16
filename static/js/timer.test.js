// timer.test.js
// Jestでテストする場合の例

const { PomodoroTimer, TimerState } = require('./timer_class');

describe('PomodoroTimer', () => {
    let timer;
    beforeEach(() => {
        timer = new PomodoroTimer();
    });

    test('初期値は25分の作業状態', () => {
        expect(timer.timeLeft).toBe(25 * 60);
        expect(timer.isRunning).toBe(false);
        expect(timer.state).toBe(TimerState.WORK);
        expect(timer.completedSessions).toBe(0);
    });

    test('tickで1秒減る', () => {
        timer.tick();
        expect(timer.timeLeft).toBe(25 * 60 - 1);
    });

    test('tickで時間が0になるとtrueを返す', () => {
        timer.timeLeft = 1;
        const isComplete = timer.tick();
        expect(isComplete).toBe(true);
        expect(timer.timeLeft).toBe(0);
    });

    test('resetで初期値に戻る', () => {
        timer.tick();
        timer.completedSessions = 3;
        timer.state = TimerState.SHORT_BREAK;
        timer.reset();
        expect(timer.timeLeft).toBe(25 * 60);
        expect(timer.isRunning).toBe(false);
        expect(timer.state).toBe(TimerState.WORK);
        expect(timer.completedSessions).toBe(0);
    });

    test('start/stopでisRunningが切り替わる', () => {
        timer.start();
        expect(timer.isRunning).toBe(true);
        timer.stop();
        expect(timer.isRunning).toBe(false);
    });

    test('作業完了後は短い休憩に遷移', () => {
        timer.nextState();
        expect(timer.state).toBe(TimerState.SHORT_BREAK);
        expect(timer.completedSessions).toBe(1);
        expect(timer.timeLeft).toBe(5 * 60);
    });

    test('4回作業完了後は長い休憩に遷移', () => {
        timer.completedSessions = 3;
        timer.nextState();
        expect(timer.state).toBe(TimerState.LONG_BREAK);
        expect(timer.completedSessions).toBe(4);
        expect(timer.timeLeft).toBe(15 * 60);
    });

    test('休憩完了後は作業に戻る', () => {
        timer.state = TimerState.SHORT_BREAK;
        timer.nextState();
        expect(timer.state).toBe(TimerState.WORK);
        expect(timer.timeLeft).toBe(25 * 60);
    });

    test('getStateLabelは日本語ラベルを返す', () => {
        expect(timer.getStateLabel()).toBe('作業');
        timer.state = TimerState.SHORT_BREAK;
        expect(timer.getStateLabel()).toBe('短い休憩');
        timer.state = TimerState.LONG_BREAK;
        expect(timer.getStateLabel()).toBe('長い休憩');
    });

    test('getSessionsUntilLongBreakは次の長休憩までの回数を返す', () => {
        expect(timer.getSessionsUntilLongBreak()).toBe(4);
        timer.completedSessions = 1;
        expect(timer.getSessionsUntilLongBreak()).toBe(3);
        timer.completedSessions = 3;
        expect(timer.getSessionsUntilLongBreak()).toBe(1);
        timer.completedSessions = 4;
        expect(timer.getSessionsUntilLongBreak()).toBe(4);
    });
});
