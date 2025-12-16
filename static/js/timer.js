/**
 * ポモドーロタイマークラス
 */
class PomodoroTimer {
    constructor(duration = 25) {
        this.duration = duration * 60; // 分を秒に変換
        this.remainingTime = this.duration;
        this.intervalId = null;
        this.isRunning = false;
    }
    
    /**
     * タイマーを開始
     */
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
    
    /**
     * タイマーをリセット
     */
    reset() {
        clearInterval(this.intervalId);
        this.intervalId = null;
        this.isRunning = false;
        this.remainingTime = this.duration;
        this.updateDisplay();
    }
    
    /**
     * タイマー完了時の処理
     */
    complete() {
        clearInterval(this.intervalId);
        this.intervalId = null;
        this.isRunning = false;
        
        // 完了通知
        alert('ポモドーロが完了しました！お疲れ様でした。');
        
        // タイマーをリセット
        this.reset();
    }
    
    /**
     * 表示を更新
     */
    updateDisplay() {
        const minutes = Math.floor(this.remainingTime / 60);
        const seconds = this.remainingTime % 60;
        const timeText = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        
        const timerElement = document.getElementById('timer-text');
        if (timerElement) {
            timerElement.textContent = timeText;
        }
    }
    
    /**
     * 時間をMM:SS形式にフォーマット
     */
    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }
    
    /**
     * タイマーの実行状態を取得
     */
    getIsRunning() {
        return this.isRunning;
    }
}

// グローバルタイマーインスタンス
let pomodoroTimer = null;

/**
 * DOMContentLoadedイベントリスナー
 */
document.addEventListener('DOMContentLoaded', () => {
    // タイマーインスタンスを作成
    pomodoroTimer = new PomodoroTimer(25);
    
    // 初期表示を更新
    pomodoroTimer.updateDisplay();
    
    // ボタン要素を取得
    const startBtn = document.getElementById('start-btn');
    const resetBtn = document.getElementById('reset-btn');
    
    // 開始ボタンのクリックイベント
    if (startBtn) {
        startBtn.addEventListener('click', () => {
            if (!pomodoroTimer.getIsRunning()) {
                pomodoroTimer.start();
                startBtn.disabled = true;
                startBtn.textContent = '実行中...';
            }
        });
    }
    
    // リセットボタンのクリックイベント
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            pomodoroTimer.reset();
            
            // 開始ボタンを有効化
            if (startBtn) {
                startBtn.disabled = false;
                startBtn.textContent = '開始';
            }
        });
    }
});
