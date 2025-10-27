async function getState() {
  const res = await fetch('/api/timer/state');
  return res.json();
}

function formatTime(sec) {
  const m = Math.floor(sec / 60).toString().padStart(2, '0');
  const s = (sec % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}

async function refreshUI() {
  const state = await getState();
  const statusElem = document.getElementById('status');
  const timeElem = document.getElementById('time');
  
  // ステータスの日本語表示
  const statusText = {
    'running': '実行中',
    'paused': '一時停止',
    'stopped': '停止中',
    'completed': '完了'
  }[state.status] || state.status;
  
  statusElem.textContent = statusText;
  timeElem.textContent = formatTime(state.remaining);

  // 完了状態の視覚的フィードバック
  if (state.status === 'completed') {
    statusElem.classList.add('completed');
    timeElem.classList.add('completed');
  } else {
    statusElem.classList.remove('completed');
    timeElem.classList.remove('completed');
  }
}

document.getElementById('start').addEventListener('click', async () => {
  await fetch('/api/timer/start', { method: 'POST' });
  refreshUI();
});

document.getElementById('pause').addEventListener('click', async () => {
  await fetch('/api/timer/pause', { method: 'POST' });
  refreshUI();
});

document.getElementById('reset').addEventListener('click', async () => {
  await fetch('/api/timer/reset', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({}) });
  refreshUI();
});

// デバッグボタン: 30秒に設定して開始
const dbg30 = document.getElementById('dbg30');
if (dbg30) {
  dbg30.addEventListener('click', async () => {
    await fetch('/api/timer/set_remaining', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ seconds: 30 }) });
    await fetch('/api/timer/start', { method: 'POST' });
    refreshUI();
  });
}

// 簡易ポーリング（UI更新） — 10秒間隔に変更
setInterval(refreshUI, 10000);
window.addEventListener('load', refreshUI);
