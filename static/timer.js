let duration = 25 * 60;
let timeLeft = duration;
let timerInterval = null;
let running = false;
let pomodoroCount = 4;
let focusSeconds = 100 * 60; // 1時間40分

function updateTimerDisplay() {
    const min = String(Math.floor(timeLeft / 60)).padStart(2, '0');
    const sec = String(timeLeft % 60).padStart(2, '0');
    document.getElementById('timer').textContent = `${min}:${sec}`;
    // 円グラフ進捗
    const progress = document.getElementById('progress');
    const percent = (duration - timeLeft) / duration;
    progress.setAttribute('stroke-dashoffset', 502 * (1 - percent));
}

function startTimer() {
    if (running) return;
    running = true;
    document.getElementById('start-btn').disabled = true;
    timerInterval = setInterval(() => {
        if (timeLeft > 0) {
            timeLeft--;
            updateTimerDisplay();
        } else {
            clearInterval(timerInterval);
            running = false;
            document.getElementById('start-btn').disabled = false;
            pomodoroCount++;
            focusSeconds += duration;
            document.getElementById('pomodoro-count').textContent = pomodoroCount;
            document.getElementById('focus-time').textContent =
                `${Math.floor(focusSeconds/60/60)}時間${Math.floor((focusSeconds/60)%60)}分`;
        }
    }, 1000);
}

function resetTimer() {
    clearInterval(timerInterval);
    timeLeft = duration;
    running = false;
    updateTimerDisplay();
    document.getElementById('start-btn').disabled = false;
}

document.getElementById('start-btn').onclick = startTimer;
document.getElementById('reset-btn').onclick = resetTimer;

updateTimerDisplay();
