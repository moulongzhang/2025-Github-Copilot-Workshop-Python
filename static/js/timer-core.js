// timer-core.js
// Pure timer logic helpers (placeholder for Phase 1)

export function formatMs(ms) {
  const totalSeconds = Math.max(0, Math.floor(ms / 1000));
  const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
  const seconds = (totalSeconds % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
}

// Minimal API for later expansion
export function createTimer(plannedMs, nowProvider = () => performance.now()) {
  let startTs = null;
  let pausedAt = null;

  function start() {
    if (startTs === null) startTs = nowProvider();
    if (pausedAt !== null) {
      // resume: shift startTs forward by paused duration
      const pausedDuration = nowProvider() - pausedAt;
      startTs += pausedDuration;
      pausedAt = null;
    }
  }

  function pause() {
    if (startTs === null || pausedAt !== null) return;
    pausedAt = nowProvider();
  }

  function reset() {
    startTs = null;
    pausedAt = null;
  }

  function getRemaining() {
    if (startTs === null) return plannedMs;
    const now = (pausedAt !== null) ? pausedAt : nowProvider();
    const elapsed = now - startTs;
    return Math.max(0, plannedMs - elapsed);
  }

  return {
    plannedMs,
    start,
    pause,
    reset,
    getRemaining,
  };
}
