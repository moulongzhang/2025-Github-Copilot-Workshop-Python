// タイマーのロジック（ESモジュール化）
export let timer = null;
export let seconds = 25 * 60;

export function updateDisplay(getDisplay = () => document.getElementById('timer-display')) {
    const min = String(Math.floor(seconds / 60)).padStart(2, '0');
    const sec = String(seconds % 60).padStart(2, '0');
    getDisplay().textContent = `${min}:${sec}`;
}

export function startTimer(onFinish = () => alert('時間になりました！'), getDisplay) {
    if (timer) return;
    timer = setInterval(() => {
        if (seconds > 0) {
            seconds--;
            updateDisplay(getDisplay);
        } else {
            clearInterval(timer);
            timer = null;
            onFinish();
        }
    }, 1000);
}

export function stopTimer() {
    if (timer) {
        clearInterval(timer);
        timer = null;
    }
}

export function resetTimer(getDisplay) {
    stopTimer();
    seconds = 25 * 60;
    updateDisplay(getDisplay);
}

if (typeof document !== 'undefined') {
    document.getElementById('start-btn').onclick = () => startTimer();
    document.getElementById('stop-btn').onclick = stopTimer;
    document.getElementById('reset-btn').onclick = () => resetTimer();
    updateDisplay();
}
