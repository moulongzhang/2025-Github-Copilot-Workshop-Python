/**
 * Pomodoro Timer Class
 * Core timer logic (will be fully implemented in Stage 1)
 */

class PomodoroTimer {
    constructor() {
        // Duration in seconds
        this.workDuration = 25 * 60;      // 25 minutes
        this.shortBreak = 5 * 60;         // 5 minutes
        this.longBreak = 15 * 60;         // 15 minutes
        
        // Timer state
        this.currentTime = this.workDuration;
        this.isRunning = false;
        this.intervalId = null;
        
        // Session tracking
        this.sessionCount = 0;
        this.currentType = 'work';        // 'work', 'short_break', 'long_break'
        this.sessionsUntilLongBreak = 4;
    }
    
    /**
     * Start the timer
     */
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.intervalId = setInterval(() => this.tick(), 1000);
        console.log('Timer started');
    }
    
    /**
     * Pause the timer
     */
    pause() {
        if (!this.isRunning) return;
        
        this.isRunning = false;
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        console.log('Timer paused');
    }
    
    /**
     * Reset the timer to initial state
     */
    reset() {
        this.pause();
        this.currentTime = this.getDurationForCurrentType();
        console.log('Timer reset');
    }
    
    /**
     * Timer tick (called every second)
     */
    tick() {
        if (this.currentTime > 0) {
            this.currentTime--;
        } else {
            this.onTimerComplete();
        }
    }
    
    /**
     * Called when timer reaches 0
     */
    onTimerComplete() {
        this.pause();
        console.log(`${this.currentType} session completed!`);
        
        // Auto-switch to next session (will be implemented in Stage 1)
        // this.nextSession();
    }
    
    /**
     * Switch to next session type
     */
    nextSession() {
        if (this.currentType === 'work') {
            this.sessionCount++;
            
            // Long break after 4 work sessions
            if (this.sessionCount % this.sessionsUntilLongBreak === 0) {
                this.currentType = 'long_break';
            } else {
                this.currentType = 'short_break';
            }
        } else {
            // After any break, return to work
            this.currentType = 'work';
        }
        
        this.currentTime = this.getDurationForCurrentType();
        console.log(`Switched to ${this.currentType} session`);
    }
    
    /**
     * Get duration for current session type
     */
    getDurationForCurrentType() {
        switch (this.currentType) {
            case 'work':
                return this.workDuration;
            case 'short_break':
                return this.shortBreak;
            case 'long_break':
                return this.longBreak;
            default:
                return this.workDuration;
        }
    }
    
    /**
     * Format time as MM:SS
     */
    formatTime() {
        const minutes = Math.floor(this.currentTime / 60);
        const seconds = this.currentTime % 60;
        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    /**
     * Get current state
     */
    getState() {
        return {
            currentTime: this.currentTime,
            isRunning: this.isRunning,
            sessionType: this.currentType,
            sessionCount: this.sessionCount,
            formattedTime: this.formatTime()
        };
    }
}
