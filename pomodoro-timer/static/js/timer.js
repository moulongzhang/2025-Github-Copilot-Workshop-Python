/**
 * タイマーUI - DOM操作とイベントハンドリング
 */

document.addEventListener('DOMContentLoaded', () => {
    // タイマー状態
    const timerState = {
        mode: 'pomodoro',          // 'pomodoro' | 'shortBreak' | 'longBreak'
        timeRemaining: 1500,        // 秒単位
        totalTime: 1500,            // 現在のモードの合計時間
        isRunning: false,
        pomodoroCount: 0,           // 完了したポモドーロ数
        totalFocusMinutes: 0,       // 合計集中時間（分）
        intervalId: null,
        settings: {
            pomodoro: 25,           // 分
            shortBreak: 5,
            longBreak: 15
        }
    };

    // DOM要素
    const elements = {
        modeLabel: document.getElementById('mode-label'),
        timerDisplay: document.getElementById('timer-display'),
        progressCircle: document.getElementById('progress-circle'),
        startBtn: document.getElementById('start-btn'),
        resetBtn: document.getElementById('reset-btn'),
        pomodoroCount: document.getElementById('pomodoro-count'),
        focusTime: document.getElementById('focus-time')
    };

    // 円周の長さ（2 * π * r, r = 100）
    const CIRCUMFERENCE = 628;

    /**
     * UIを更新
     */
    function updateUI() {
        // 時間表示を更新
        elements.timerDisplay.textContent = TimerEngine.formatTime(timerState.timeRemaining);
        
        // モードラベルを更新
        elements.modeLabel.textContent = TimerEngine.getModeLabel(timerState.mode);
        
        // プログレスサークルを更新
        const progress = TimerEngine.calculateProgress(
            timerState.timeRemaining,
            timerState.totalTime
        );
        const offset = TimerEngine.calculateStrokeOffset(progress, CIRCUMFERENCE);
        elements.progressCircle.style.strokeDashoffset = offset;
        
        // ボタンテキストを更新
        elements.startBtn.textContent = timerState.isRunning ? '一時停止' : '開始';
        
        // 進捗を更新
        elements.pomodoroCount.textContent = timerState.pomodoroCount;
        elements.focusTime.textContent = TimerEngine.formatTotalTime(timerState.totalFocusMinutes);
    }

    /**
     * タイマーを開始/一時停止
     */
    function toggleTimer() {
        if (timerState.isRunning) {
            pauseTimer();
        } else {
            startTimer();
        }
    }

    /**
     * タイマーを開始
     */
    function startTimer() {
        timerState.isRunning = true;
        timerState.intervalId = setInterval(() => {
            timerState.timeRemaining--;
            
            if (timerState.timeRemaining <= 0) {
                onTimerComplete();
            }
            
            updateUI();
        }, 1000);
        updateUI();
    }

    /**
     * タイマーを一時停止
     */
    function pauseTimer() {
        timerState.isRunning = false;
        if (timerState.intervalId) {
            clearInterval(timerState.intervalId);
            timerState.intervalId = null;
        }
        updateUI();
    }

    /**
     * タイマー完了時の処理
     */
    function onTimerComplete() {
        pauseTimer();
        
        // ポモドーロ完了時
        if (timerState.mode === 'pomodoro') {
            timerState.pomodoroCount++;
            timerState.totalFocusMinutes += timerState.settings.pomodoro;
        }
        
        // 次のモードへ切り替え
        const nextMode = TimerEngine.getNextMode(timerState.mode, timerState.pomodoroCount);
        switchMode(nextMode);
        
        // 通知（Phase 5で実装）
        // playNotification();
    }

    /**
     * モードを切り替え
     */
    function switchMode(mode) {
        timerState.mode = mode;
        timerState.totalTime = TimerEngine.getDuration(mode, timerState.settings);
        timerState.timeRemaining = timerState.totalTime;
        updateUI();
    }

    /**
     * タイマーをリセット
     */
    function resetTimer() {
        pauseTimer();
        timerState.timeRemaining = timerState.totalTime;
        updateUI();
    }

    /**
     * 設定を読み込む
     */
    async function loadSettings() {
        try {
            const response = await fetch('/api/settings');
            if (response.ok) {
                const settings = await response.json();
                timerState.settings = settings;
                timerState.totalTime = TimerEngine.getDuration(timerState.mode, settings);
                timerState.timeRemaining = timerState.totalTime;
                updateUI();
            }
        } catch (error) {
            console.log('デフォルト設定を使用します');
        }
    }

    // イベントリスナーの設定
    elements.startBtn.addEventListener('click', toggleTimer);
    elements.resetBtn.addEventListener('click', resetTimer);

    // 初期化
    loadSettings();
    updateUI();
});
