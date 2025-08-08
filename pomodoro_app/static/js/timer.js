let timer = null;
let remainingSeconds = 25 * 60;
let isRunning = false;

const timerDisplay = document.getElementById('timerDisplay');
const startBtn = document.getElementById('startBtn');
const resetBtn = document.getElementById('resetBtn');
const statusText = document.getElementById('statusText');

function updateDisplay() {
    const min = String(Math.floor(remainingSeconds / 60)).padStart(2, '0');
    const sec = String(remainingSeconds % 60).padStart(2, '0');
    timerDisplay.textContent = `${min}:${sec}`;
}

function updateStatus() {
    statusText.textContent = isRunning ? '作業中' : '停止中';
}

function startTimer() {
    if (isRunning) return;
    isRunning = true;
    updateStatus();
    timer = setInterval(() => {
        if (remainingSeconds > 0) {
            remainingSeconds--;
            updateDisplay();
        } else {
            clearInterval(timer);
            isRunning = false;
            updateStatus();
        }
    }, 1000);
}

function resetTimer() {
    clearInterval(timer);
    remainingSeconds = 25 * 60;
    isRunning = false;
    updateDisplay();
    updateStatus();
}

startBtn.addEventListener('click', startTimer);
resetBtn.addEventListener('click', resetTimer);

// 初期表示
updateDisplay();
updateStatus();
