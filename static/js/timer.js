let timer = 1500; // 25分
let intervalId = null;
let isRunning = false;

const timerDisplay = document.getElementById('timer-display');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const resetBtn = document.getElementById('reset-btn');
const statusLabel = document.getElementById('status');

function updateDisplay() {
    const min = String(Math.floor(timer / 60)).padStart(2, '0');
    const sec = String(timer % 60).padStart(2, '0');
    timerDisplay.textContent = `${min}:${sec}`;
}

function startTimer() {
    if (isRunning) return;
    isRunning = true;
    intervalId = setInterval(() => {
        if (timer > 0) {
            timer--;
            updateDisplay();
        } else {
            clearInterval(intervalId);
            isRunning = false;
            statusLabel.textContent = '休憩中';
        }
    }, 1000);
}

function stopTimer() {
    if (!isRunning) return;
    clearInterval(intervalId);
    isRunning = false;
}

function resetTimer() {
    stopTimer();
    timer = 1500;
    updateDisplay();
    statusLabel.textContent = '作業中';
}

startBtn.addEventListener('click', startTimer);
stopBtn.addEventListener('click', stopTimer);
resetBtn.addEventListener('click', resetTimer);

updateDisplay();
