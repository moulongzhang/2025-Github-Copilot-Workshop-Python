// ポモドーロタイマー JavaScript制御

class PomodoroTimerUI {
    constructor() {
        this.isRunning = false;
        this.isPaused = false;
        this.currentTime = 25 * 60; // 25分（秒）
        this.currentMode = 'work'; // 'work' or 'break'
        this.interval = null;
        
        this.initializeElements();
        this.updateDisplay();
    }
    
    initializeElements() {
        this.timerDisplay = document.getElementById('timer-display');
        this.statusDisplay = document.getElementById('status');
        this.startBtn = document.getElementById('start-btn');
        this.resetBtn = document.getElementById('reset-btn');
        
        // イベントリスナー設定
        this.startBtn.addEventListener('click', () => this.toggleTimer());
        this.resetBtn.addEventListener('click', () => this.resetTimer());
    }
    
    toggleTimer() {
        if (this.isRunning) {
            this.pauseTimer();
        } else {
            this.startTimer();
        }
    }
    
    startTimer() {
        this.isRunning = true;
        this.isPaused = false;
        this.startBtn.textContent = '一時停止';
        this.statusDisplay.textContent = this.currentMode === 'work' ? '作業中' : '休憩中';
        
        this.interval = setInterval(() => {
            this.currentTime--;
            this.updateDisplay();
            
            if (this.currentTime <= 0) {
                this.completeSession();
            }
        }, 1000);
    }
    
    pauseTimer() {
        this.isRunning = false;
        this.isPaused = true;
        this.startBtn.textContent = '再開';
        this.statusDisplay.textContent = '一時停止中';
        
        if (this.interval) {
            clearInterval(this.interval);
        }
    }
    
    resetTimer() {
        this.isRunning = false;
        this.isPaused = false;
        this.currentTime = this.currentMode === 'work' ? 25 * 60 : 5 * 60;
        this.startBtn.textContent = '開始';
        this.statusDisplay.textContent = '準備完了';
        
        if (this.interval) {
            clearInterval(this.interval);
        }
        
        this.updateDisplay();
    }
    
    completeSession() {
        this.isRunning = false;
        
        if (this.interval) {
            clearInterval(this.interval);
        }
        
        // セッション完了の処理
        if (this.currentMode === 'work') {
            this.currentMode = 'break';
            this.currentTime = 5 * 60; // 5分休憩
            this.statusDisplay.textContent = '休憩時間です！';
        } else {
            this.currentMode = 'work';
            this.currentTime = 25 * 60; // 25分作業
            this.statusDisplay.textContent = '作業時間です！';
        }
        
        this.startBtn.textContent = '開始';
        this.updateDisplay();
        
        // 完了通知
        this.showNotification();
    }
    
    updateDisplay() {
        const minutes = Math.floor(this.currentTime / 60);
        const seconds = this.currentTime % 60;
        this.timerDisplay.textContent = 
            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    showNotification() {
        // 簡単な通知（後でWeb Notification APIに置き換え）
        alert(this.currentMode === 'break' ? '休憩時間です！' : '作業時間です！');
    }
}

// ページ読み込み時に初期化
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimerUI();
});
