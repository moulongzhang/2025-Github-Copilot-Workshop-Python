// Timer configuration
const CONFIG = {
    WORK_TIME: 25 * 60, // 25 minutes in seconds
    BREAK_TIME: 5 * 60, // 5 minutes in seconds
    LONG_BREAK_TIME: 15 * 60, // 15 minutes in seconds
    SESSIONS_BEFORE_LONG_BREAK: 4
};

// Timer states
const STATE = {
    IDLE: 'idle',
    RUNNING: 'running',
    PAUSED: 'paused'
};

const MODE = {
    WORK: 'work',
    BREAK: 'break',
    LONG_BREAK: 'long-break'
};

// Timer class
class PomodoroTimer {
    constructor() {
        this.timeLeft = CONFIG.WORK_TIME;
        this.totalTime = CONFIG.WORK_TIME;
        this.state = STATE.IDLE;
        this.mode = MODE.WORK;
        this.completedSessions = 0;
        this.totalFocusTime = 0; // in seconds
        this.timerInterval = null;
        
        this.initElements();
        this.initProgressRing();
        this.updateDisplay();
        this.updateProgress();
    }
    
    initElements() {
        this.timeText = document.getElementById('timeText');
        this.statusText = document.getElementById('statusText');
        this.startBtn = document.getElementById('startBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.completedCount = document.getElementById('completedCount');
        this.focusTime = document.getElementById('focusTime');
        this.progressCircle = document.getElementById('progressCircle');
        this.timerCard = document.querySelector('.timer-card');
        
        this.startBtn.addEventListener('click', () => this.toggleTimer());
        this.resetBtn.addEventListener('click', () => this.reset());
    }
    
    initProgressRing() {
        const radius = 130;
        const circumference = 2 * Math.PI * radius;
        this.progressCircle.style.strokeDasharray = circumference;
        this.progressCircle.style.strokeDashoffset = 0;
        this.circumference = circumference;
    }
    
    toggleTimer() {
        if (this.state === STATE.RUNNING) {
            this.pause();
        } else {
            this.start();
        }
    }
    
    start() {
        this.state = STATE.RUNNING;
        this.startBtn.textContent = '一時停止';
        this.startBtn.classList.add('running');
        
        this.timerInterval = setInterval(() => {
            this.tick();
        }, 1000);
    }
    
    pause() {
        this.state = STATE.PAUSED;
        this.startBtn.textContent = '再開';
        clearInterval(this.timerInterval);
    }
    
    tick() {
        if (this.timeLeft > 0) {
            this.timeLeft--;
            this.updateDisplay();
        } else {
            this.complete();
        }
    }
    
    complete() {
        clearInterval(this.timerInterval);
        
        // Update stats based on mode
        if (this.mode === MODE.WORK) {
            this.completedSessions++;
            this.totalFocusTime += CONFIG.WORK_TIME;
            this.updateProgress();
        }
        
        // Transition to next mode
        this.transitionToNextMode();
    }
    
    transitionToNextMode() {
        if (this.mode === MODE.WORK) {
            // After work, go to break
            if (this.completedSessions % CONFIG.SESSIONS_BEFORE_LONG_BREAK === 0) {
                this.mode = MODE.LONG_BREAK;
                this.timeLeft = CONFIG.LONG_BREAK_TIME;
                this.totalTime = CONFIG.LONG_BREAK_TIME;
                this.updateStatusText('長休憩');
                this.timerCard.className = 'timer-card long-break';
            } else {
                this.mode = MODE.BREAK;
                this.timeLeft = CONFIG.BREAK_TIME;
                this.totalTime = CONFIG.BREAK_TIME;
                this.updateStatusText('休憩中');
                this.timerCard.className = 'timer-card break';
            }
        } else {
            // After break, go back to work
            this.mode = MODE.WORK;
            this.timeLeft = CONFIG.WORK_TIME;
            this.totalTime = CONFIG.WORK_TIME;
            this.updateStatusText('作業中');
            this.timerCard.className = 'timer-card working';
        }
        
        this.state = STATE.IDLE;
        this.startBtn.textContent = '開始';
        this.updateDisplay();
    }
    
    reset() {
        clearInterval(this.timerInterval);
        this.state = STATE.IDLE;
        this.mode = MODE.WORK;
        this.timeLeft = CONFIG.WORK_TIME;
        this.totalTime = CONFIG.WORK_TIME;
        this.startBtn.textContent = '開始';
        this.updateStatusText('作業中');
        this.timerCard.className = 'timer-card working';
        this.updateDisplay();
    }
    
    updateDisplay() {
        const minutes = Math.floor(this.timeLeft / 60);
        const seconds = this.timeLeft % 60;
        this.timeText.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // Update progress ring
        const progress = (this.totalTime - this.timeLeft) / this.totalTime;
        const offset = this.circumference * (1 - progress);
        this.progressCircle.style.strokeDashoffset = offset;
    }
    
    updateStatusText(text) {
        this.statusText.textContent = text;
    }
    
    updateProgress() {
        this.completedCount.textContent = this.completedSessions;
        
        const hours = Math.floor(this.totalFocusTime / 3600);
        const minutes = Math.floor((this.totalFocusTime % 3600) / 60);
        
        if (hours > 0) {
            this.focusTime.textContent = `${hours}時間${minutes}分`;
        } else {
            this.focusTime.textContent = `${minutes}分`;
        }
    }
}

// Initialize timer when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const timer = new PomodoroTimer();
});
