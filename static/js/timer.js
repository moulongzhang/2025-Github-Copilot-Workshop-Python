// timer.js
let timerDuration = 25 * 60; // 25分（秒）
let remaining = timerDuration;
let timerInterval = null;
let isRunning = false;

const timerDisplay = document.getElementById('timer');
const startBtn = document.getElementById('start-btn');
const resetBtn = document.getElementById('reset-btn');
const progressCircle = document.getElementById('progress');

function updateDisplay() {
    const min = String(Math.floor(remaining / 60)).padStart(2, '0');
    const sec = String(remaining % 60).padStart(2, '0');
    timerDisplay.textContent = `${min}:${sec}`;
    // 円グラフ進捗
    const total = 2 * Math.PI * 90;
    const percent = (timerDuration - remaining) / timerDuration;
    progressCircle.setAttribute('stroke-dashoffset', total * (1 - percent));
}

function tick() {
    if (remaining > 0) {
        remaining--;
        updateDisplay();
    } else {
        clearInterval(timerInterval);
        isRunning = false;
        startBtn.disabled = false;
        // TODO: 完了時の通知
    }
}

startBtn.addEventListener('click', () => {
    if (!isRunning) {
        isRunning = true;
        startBtn.disabled = true;
        timerInterval = setInterval(tick, 1000);
    }
});

resetBtn.addEventListener('click', () => {
    clearInterval(timerInterval);
    isRunning = false;
    remaining = timerDuration;
    updateDisplay();
    startBtn.disabled = false;
});

// 初期表示
updateDisplay();
