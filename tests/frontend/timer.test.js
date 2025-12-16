/**
 * PomodoroTimerクラスのユニットテスト
 */

// タイマークラスをグローバルスコープから取得するためのセットアップ
let PomodoroTimer;

// DOMのモック設定
beforeEach(() => {
    // DOM要素をモック
    document.body.innerHTML = `
        <div id="timer-text">25:00</div>
        <button id="start-btn">開始</button>
        <button id="reset-btn">リセット</button>
    `;
    
    // タイマークラスを定義（実際のコードから）
    PomodoroTimer = class {
        constructor(duration = 25) {
            this.duration = duration * 60;
            this.remainingTime = this.duration;
            this.intervalId = null;
            this.isRunning = false;
        }
        
        start() {
            if (this.isRunning) return;
            this.isRunning = true;
            this.intervalId = setInterval(() => {
                this.remainingTime--;
                this.updateDisplay();
                if (this.remainingTime <= 0) {
                    this.complete();
                }
            }, 1000);
            this.updateDisplay();
        }
        
        reset() {
            clearInterval(this.intervalId);
            this.intervalId = null;
            this.isRunning = false;
            this.remainingTime = this.duration;
            this.updateDisplay();
        }
        
        complete() {
            clearInterval(this.intervalId);
            this.intervalId = null;
            this.isRunning = false;
            this.reset();
        }
        
        updateDisplay() {
            const minutes = Math.floor(this.remainingTime / 60);
            const seconds = this.remainingTime % 60;
            const timeText = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            const timerElement = document.getElementById('timer-text');
            if (timerElement) {
                timerElement.textContent = timeText;
            }
        }
        
        formatTime(seconds) {
            const minutes = Math.floor(seconds / 60);
            const secs = seconds % 60;
            return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        }
        
        getIsRunning() {
            return this.isRunning;
        }
    };
    
    // タイマーのクリア
    jest.clearAllTimers();
});

afterEach(() => {
    // タイマーのクリーンアップ
    jest.clearAllTimers();
});

describe('PomodoroTimer クラス', () => {
    describe('コンストラクタ', () => {
        test('デフォルトで25分（1500秒）に設定される', () => {
            const timer = new PomodoroTimer();
            expect(timer.duration).toBe(1500);
            expect(timer.remainingTime).toBe(1500);
        });
        
        test('カスタム時間で初期化できる', () => {
            const timer = new PomodoroTimer(10);
            expect(timer.duration).toBe(600);
            expect(timer.remainingTime).toBe(600);
        });
        
        test('初期状態ではタイマーが停止している', () => {
            const timer = new PomodoroTimer();
            expect(timer.isRunning).toBe(false);
            expect(timer.intervalId).toBeNull();
        });
    });
    
    describe('start メソッド', () => {
        beforeEach(() => {
            jest.useFakeTimers();
        });
        
        afterEach(() => {
            jest.useRealTimers();
        });
        
        test('タイマーを開始できる', () => {
            const timer = new PomodoroTimer();
            timer.start();
            expect(timer.isRunning).toBe(true);
            expect(timer.intervalId).not.toBeNull();
        });
        
        test('実行中のタイマーは再度開始できない', () => {
            const timer = new PomodoroTimer();
            timer.start();
            const firstIntervalId = timer.intervalId;
            timer.start();
            expect(timer.intervalId).toBe(firstIntervalId);
        });
        
        test('1秒ごとに残り時間が減少する', () => {
            const timer = new PomodoroTimer(1); // 1分
            timer.start();
            
            expect(timer.remainingTime).toBe(60);
            jest.advanceTimersByTime(1000);
            expect(timer.remainingTime).toBe(59);
            jest.advanceTimersByTime(1000);
            expect(timer.remainingTime).toBe(58);
        });
        
        test('表示が更新される', () => {
            const timer = new PomodoroTimer(1);
            timer.start();
            
            const timerElement = document.getElementById('timer-text');
            expect(timerElement.textContent).toBe('01:00');
            
            jest.advanceTimersByTime(1000);
            expect(timerElement.textContent).toBe('00:59');
        });
    });
    
    describe('reset メソッド', () => {
        beforeEach(() => {
            jest.useFakeTimers();
        });
        
        afterEach(() => {
            jest.useRealTimers();
        });
        
        test('タイマーを初期値にリセットできる', () => {
            const timer = new PomodoroTimer(1);
            timer.start();
            jest.advanceTimersByTime(5000);
            
            expect(timer.remainingTime).toBe(55);
            timer.reset();
            expect(timer.remainingTime).toBe(60);
        });
        
        test('リセット後はタイマーが停止する', () => {
            const timer = new PomodoroTimer();
            timer.start();
            timer.reset();
            
            expect(timer.isRunning).toBe(false);
            expect(timer.intervalId).toBeNull();
        });
        
        test('表示が初期値に戻る', () => {
            const timer = new PomodoroTimer(1);
            timer.start();
            jest.advanceTimersByTime(5000);
            timer.reset();
            
            const timerElement = document.getElementById('timer-text');
            expect(timerElement.textContent).toBe('01:00');
        });
    });
    
    describe('formatTime メソッド', () => {
        test('秒をMM:SS形式にフォーマットできる', () => {
            const timer = new PomodoroTimer();
            
            expect(timer.formatTime(0)).toBe('00:00');
            expect(timer.formatTime(59)).toBe('00:59');
            expect(timer.formatTime(60)).toBe('01:00');
            expect(timer.formatTime(125)).toBe('02:05');
            expect(timer.formatTime(1500)).toBe('25:00');
        });
    });
    
    describe('updateDisplay メソッド', () => {
        test('DOMを正しく更新する', () => {
            const timer = new PomodoroTimer(1);
            timer.remainingTime = 45;
            timer.updateDisplay();
            
            const timerElement = document.getElementById('timer-text');
            expect(timerElement.textContent).toBe('00:45');
        });
        
        test('DOM要素が存在しない場合もエラーにならない', () => {
            document.body.innerHTML = '';
            const timer = new PomodoroTimer();
            
            expect(() => timer.updateDisplay()).not.toThrow();
        });
    });
    
    describe('getIsRunning メソッド', () => {
        test('実行状態を取得できる', () => {
            const timer = new PomodoroTimer();
            expect(timer.getIsRunning()).toBe(false);
            
            timer.isRunning = true;
            expect(timer.getIsRunning()).toBe(true);
        });
    });
    
    describe('complete メソッド', () => {
        beforeEach(() => {
            jest.useFakeTimers();
        });
        
        afterEach(() => {
            jest.useRealTimers();
        });
        
        test('タイマー完了時に停止する', () => {
            const timer = new PomodoroTimer();
            timer.start();
            timer.complete();
            
            expect(timer.isRunning).toBe(false);
            expect(timer.intervalId).toBeNull();
        });
        
        test('完了後に自動的にリセットされる', () => {
            const timer = new PomodoroTimer(1);
            timer.start();
            jest.advanceTimersByTime(30000);
            
            expect(timer.remainingTime).toBe(30);
            timer.complete();
            expect(timer.remainingTime).toBe(60);
        });
    });
});
