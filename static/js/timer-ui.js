import { formatMs, createTimer } from './timer-core.js';

const defaultMs = 25 * 60 * 1000;

document.addEventListener('DOMContentLoaded', () => {
  const timer = createTimer(defaultMs);
  const timeDisplay = document.getElementById('time-display');
  const startBtn = document.getElementById('start-btn');
  const pauseBtn = document.getElementById('pause-btn');
  const resetBtn = document.getElementById('reset-btn');

  let interval = null;

  function updateDisplay() {
    timeDisplay.textContent = formatMs(timer.getRemaining());
  }

  function tick() {
    updateDisplay();
    if (timer.getRemaining() <= 0) {
      clearInterval(interval);
      interval = null;
      startBtn.disabled = false;
      pauseBtn.disabled = true;
      // TODO: notify backend /api/session/complete
    }
  }

  startBtn.addEventListener('click', () => {
    timer.start();
    if (interval) return;
    interval = setInterval(tick, 250);
    startBtn.disabled = true;
    pauseBtn.disabled = false;
  });

  pauseBtn.addEventListener('click', () => {
    timer.pause();
    if (interval) {
      clearInterval(interval);
      interval = null;
    }
    startBtn.disabled = false;
    pauseBtn.disabled = true;
  });

  resetBtn.addEventListener('click', () => {
    timer.reset();
    if (interval) {
      clearInterval(interval);
      interval = null;
    }
    startBtn.disabled = false;
    pauseBtn.disabled = true;
    updateDisplay();
  });

  // initialize UI state
  startBtn.disabled = false;
  pauseBtn.disabled = true;
  updateDisplay();
});
