// timer.js用ユニットテスト（Jest + ESモジュール対応）
import * as timerModule from '../static/js/timer.js';

describe('Pomodoro Timer Logic', () => {
    let display;

    beforeEach(() => {
        timerModule.seconds = 25 * 60;
        timerModule.timer = null;
        display = { textContent: '' };
    });

    test('初期表示は25:00', () => {
        timerModule.updateDisplay(() => display);
        expect(display.textContent).toBe('25:00');
    });

    test('1秒減ると24:59になる', () => {
        timerModule.seconds--;
        timerModule.updateDisplay(() => display);
        expect(display.textContent).toBe('24:59');
    });

    test('0秒のとき00:00になる', () => {
        timerModule.seconds = 0;
        timerModule.updateDisplay(() => display);
        expect(display.textContent).toBe('00:00');
    });

    test('resetTimerで25:00に戻る', () => {
        timerModule.seconds = 10;
        timerModule.resetTimer(() => display);
        expect(display.textContent).toBe('25:00');
        expect(timerModule.seconds).toBe(25 * 60);
    });
});
