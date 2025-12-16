// timer_class.js
// テスト容易性のための純粋なタイマークラス

const TimerState = {
    WORK: 'work',
    SHORT_BREAK: 'short_break',
    LONG_BREAK: 'long_break'
};

class PomodoroTimer {
    constructor(config = {}) {
        this.workTime = config.workTime || 25 * 60;
        this.shortBreakTime = config.shortBreakTime || 5 * 60;
        this.longBreakTime = config.longBreakTime || 15 * 60;
        this.sessionsBeforeLongBreak = config.sessionsBeforeLongBreak || 4;
        
        this.state = TimerState.WORK;
        this.completedSessions = 0;
        this.timeLeft = this.workTime;
        this.isRunning = false;
    }
    
    tick() {
        if (this.timeLeft > 0) {
            this.timeLeft--;
        }
        return this.timeLeft === 0;
    }
    
    nextState() {
        if (this.state === TimerState.WORK) {
            this.completedSessions++;
            if (this.completedSessions % this.sessionsBeforeLongBreak === 0) {
                this.state = TimerState.LONG_BREAK;
                this.timeLeft = this.longBreakTime;
            } else {
                this.state = TimerState.SHORT_BREAK;
                this.timeLeft = this.shortBreakTime;
            }
        } else {
            this.state = TimerState.WORK;
            this.timeLeft = this.workTime;
        }
    }
    
    reset() {
        this.state = TimerState.WORK;
        this.completedSessions = 0;
        this.timeLeft = this.workTime;
        this.isRunning = false;
    }
    
    start() {
        this.isRunning = true;
    }
    
    stop() {
        this.isRunning = false;
    }
    
    getStateLabel() {
        switch(this.state) {
            case TimerState.WORK:
                return '作業';
            case TimerState.SHORT_BREAK:
                return '短い休憩';
            case TimerState.LONG_BREAK:
                return '長い休憩';
        }
    }
    
    getSessionsUntilLongBreak() {
        return this.sessionsBeforeLongBreak - (this.completedSessions % this.sessionsBeforeLongBreak);
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PomodoroTimer, TimerState };
}
