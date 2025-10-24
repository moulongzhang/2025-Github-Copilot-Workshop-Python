let timer = null;
let timeLeft = 25 * 60; // 25分
const timeText = document.getElementById('time-text');
const startBtn = document.getElementById('start-btn');
const resetBtn = document.getElementById('reset-btn');

function updateDisplay() {
    const min = String(Math.floor(timeLeft / 60)).padStart(2, '0');
    const sec = String(timeLeft % 60).padStart(2, '0');
    timeText.textContent = `${min}:${sec}`;
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
            alert('タイマー終了！');
        }
    }, 1000);
}

function resetTimer() {
    clearInterval(timer);
    timer = null;
    timeLeft = 25 * 60;
    updateDisplay();
}

startBtn.addEventListener('click', startTimer);
resetBtn.addEventListener('click', resetTimer);

updateDisplay();
