// タイマーの状態管理
class PomodoroTimer {
    constructor() {
        // 初期設定: 25分 = 1500秒
        this.initialTime = 25 * 60;
        this.timeRemaining = this.initialTime;
        this.isRunning = false;
        this.timerInterval = null;
        
        // DOM要素の取得
        this.timerDisplay = document.getElementById('timerDisplay');
        this.statusDisplay = document.getElementById('statusDisplay');
        this.startBtn = document.getElementById('startBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.progressCircle = document.getElementById('progressCircle');
        
        // 円の周の長さを計算 (2πr, r=130)
        this.circumference = 2 * Math.PI * 130;
        
        // イベントリスナーの設定
        this.startBtn.addEventListener('click', () => this.toggleTimer());
        this.resetBtn.addEventListener('click', () => this.resetTimer());
        
        // 初期表示の更新
        this.updateDisplay();
        this.updateStatus();
    }
    
    // タイマーの開始/停止を切り替え
    toggleTimer() {
        if (this.isRunning) {
            this.stopTimer();
        } else {
            this.startTimer();
        }
    }
    
    // タイマーを開始
    startTimer() {
        this.isRunning = true;
        this.startBtn.textContent = '停止';
        this.updateStatus();
        
        // 1秒ごとにカウントダウン
        this.timerInterval = setInterval(() => {
            if (this.timeRemaining > 0) {
                this.timeRemaining--;
                this.updateDisplay();
                this.updateProgress();
            } else {
                // タイマー終了
                this.stopTimer();
                this.playSound();
                alert('ポモドーロ完了！お疲れ様でした！');
            }
        }, 1000);
    }
    
    // タイマーを停止
    stopTimer() {
        this.isRunning = false;
        this.startBtn.textContent = '開始';
        this.updateStatus();
        
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }
    
    // タイマーをリセット
    resetTimer() {
        this.stopTimer();
        this.timeRemaining = this.initialTime;
        this.updateDisplay();
        this.updateProgress();
    }
    
    // 時間表示を更新
    updateDisplay() {
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        
        // 2桁表示にフォーマット
        const formattedMinutes = String(minutes).padStart(2, '0');
        const formattedSeconds = String(seconds).padStart(2, '0');
        
        this.timerDisplay.textContent = `${formattedMinutes}:${formattedSeconds}`;
    }
    
    // 状態表示を更新
    updateStatus() {
        if (this.isRunning) {
            this.statusDisplay.textContent = '作業中';
            this.statusDisplay.className = 'status-display running';
        } else {
            this.statusDisplay.textContent = '停止中';
            this.statusDisplay.className = 'status-display stopped';
        }
    }
    
    // 円形プログレスバーを更新
    updateProgress() {
        const progress = this.timeRemaining / this.initialTime;
        const offset = this.circumference * (1 - progress);
        this.progressCircle.style.strokeDashoffset = offset;
    }
    
    // 音を鳴らす（オプション）
    playSound() {
        // ブラウザのビープ音を使用
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.5);
    }
}

// ページ読み込み時にタイマーを初期化
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimer();
});
