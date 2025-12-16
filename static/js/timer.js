// timer.js
let workDuration = 25 * 60; // 25分
let breakDuration = 5 * 60; // 5分
let longBreakDuration = 15 * 60; // 15分
let currentMode = 'work'; // 'work' | 'break' | 'longbreak'
let timer = null;
let timeLeft = workDuration;
let sessionCount = 0;

const timerDisplay = document.getElementById('timer-display');
const modeDisplay = document.getElementById('mode-display');
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const resetBtn = document.getElementById('reset-btn');
const sessionProgress = document.getElementById('session-progress');

function updateDisplay() {
    const min = String(Math.floor(timeLeft / 60)).padStart(2, '0');
    const sec = String(timeLeft % 60).padStart(2, '0');
    timerDisplay.textContent = `${min}:${sec}`;
    if (currentMode === 'work') {
        modeDisplay.textContent = '作業中';
    } else if (currentMode === 'break') {
        modeDisplay.textContent = '休憩中';
    } else {
        modeDisplay.textContent = '長休憩中';
    }
    // セッション進捗表示
    let html = '';
    for (let i = 0; i < 4; i++) {
        html += `<span class="${i < sessionCount ? 'active' : ''}">${i < sessionCount ? '●' : '○'}</span>`;
    }
    sessionProgress.innerHTML = html;
}

function startTimer() {
    if (timer) return;
    timer = setInterval(() => {
        if (timeLeft > 0) {
            timeLeft--;
            updateDisplay();
        } else {
            clearInterval(timer);
            timer = null;
            onTimerEnd();
        }
    }, 1000);
}

function pauseTimer() {
    if (timer) {
        clearInterval(timer);
        timer = null;
    }
}

function resetTimer() {
    pauseTimer();
    if (currentMode === 'work') {
        timeLeft = workDuration;
    } else if (currentMode === 'break') {
        timeLeft = breakDuration;
    } else {
        timeLeft = longBreakDuration;
    }
    updateDisplay();
}

function onTimerEnd() {
    if (currentMode === 'work') {
        sessionCount++;
        if (sessionCount >= 4) {
            currentMode = 'longbreak';
            timeLeft = longBreakDuration;
            sessionCount = 0;
        } else {
            currentMode = 'break';
            timeLeft = breakDuration;
        }
        alert('作業セッション終了！休憩しましょう。');
    } else {
        currentMode = 'work';
        timeLeft = workDuration;
        alert('休憩終了！作業を再開しましょう。');
    }
    updateDisplay();
}

startBtn.onclick = startTimer;
pauseBtn.onclick = pauseTimer;
resetBtn.onclick = resetTimer;

// 初期表示
updateDisplay();
