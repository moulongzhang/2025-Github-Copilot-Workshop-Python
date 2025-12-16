
// 設定の読み込み
function loadSettings() {
    const settings = JSON.parse(localStorage.getItem('pomodoroSettings') || '{}');
    return {
        workTime: (settings.workTime || 25) * 60,
        shortBreakTime: (settings.shortBreakTime || 5) * 60,
        longBreakTime: (settings.longBreakTime || 15) * 60,
        sessionsBeforeLongBreak: settings.sessionsBeforeLongBreak || 4,
        soundEnabled: settings.soundEnabled !== false,
        notificationEnabled: settings.notificationEnabled !== false
    };
}

let settings = loadSettings();
let pomodoroTimer = new PomodoroTimer(settings);
let intervalId = null;

const timerDisplay = document.getElementById('timer-display');
const timerProgress = document.getElementById('timer-progress');
const stateLabel = document.getElementById('state-label');
const completedSessionsEl = document.getElementById('completed-sessions');
const sessionsUntilLongBreakEl = document.getElementById('sessions-until-long-break');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const resetBtn = document.getElementById('reset-btn');
const settingsBtn = document.getElementById('settings-btn');
const settingsPanel = document.getElementById('settings-panel');
const saveSettingsBtn = document.getElementById('save-settings-btn');
const clearHistoryBtn = document.getElementById('clear-history-btn');

const radius = 100;
const circumference = 2 * Math.PI * radius;
timerProgress.setAttribute('stroke-dasharray', circumference);
timerProgress.setAttribute('stroke-dashoffset', 0);

function getTotalTimeForCurrentState() {
    if (pomodoroTimer.state === 'work') {
        return pomodoroTimer.workTime;
    } else if (pomodoroTimer.state === 'short_break') {
        return pomodoroTimer.shortBreakTime;
    } else {
        return pomodoroTimer.longBreakTime;
    }
}

function updateDisplay() {
    const min = String(Math.floor(pomodoroTimer.timeLeft / 60)).padStart(2, '0');
    const sec = String(pomodoroTimer.timeLeft % 60).padStart(2, '0');
    timerDisplay.textContent = `${min}:${sec}`;
    
    // 円形進捗
    const totalTime = getTotalTimeForCurrentState();
    const percent = pomodoroTimer.timeLeft / totalTime;
    const offset = circumference * (1 - percent);
    timerProgress.setAttribute('stroke-dashoffset', offset);
    
    // 状態ラベル
    stateLabel.textContent = pomodoroTimer.getStateLabel();
    
    // セッション情報
    completedSessionsEl.textContent = pomodoroTimer.completedSessions;
    sessionsUntilLongBreakEl.textContent = pomodoroTimer.getSessionsUntilLongBreak();
    
    // 状態に応じた色変更
    updateStateStyles();
}

function updateStateStyles() {
    const isBreak = pomodoroTimer.state === 'short_break' || pomodoroTimer.state === 'long_break';
    
    if (isBreak) {
        stateLabel.classList.add(pomodoroTimer.state);
        timerProgress.classList.add(pomodoroTimer.state);
        timerDisplay.classList.add(pomodoroTimer.state);
    } else {
        stateLabel.className = 'state-label';
        timerProgress.className = '';
        timerDisplay.className = '';
    }
    
    // 進捗ドット更新
    updateProgressDots();
}

function updateProgressDots() {
    for (let i = 1; i <= 4; i++) {
        const dot = document.getElementById(`dot-${i}`);
        if (dot) {
            if (i <= (pomodoroTimer.completedSessions % pomodoroTimer.sessionsBeforeLongBreak)) {
                dot.classList.add('completed');
            } else {
                dot.classList.remove('completed');
            }
        }
    }
}

function tick() {
    const isComplete = pomodoroTimer.tick();
    updateDisplay();
    
    if (isComplete) {
        clearInterval(intervalId);
        pomodoroTimer.stop();
        
        // 履歴保存
        saveHistory(pomodoroTimer.state);
        
        // 次の状態へ遷移
        const previousState = pomodoroTimer.getStateLabel();
        pomodoroTimer.nextState();
        updateDisplay();
        
        // 通知
        showNotification(previousState);
    }
}

function showNotification(completedState) {
    const nextState = pomodoroTimer.getStateLabel();
    const message = `${completedState}が終了しました！次は${nextState}です。`;
    
    // ブラウザ通知
    if (settings.notificationEnabled && 'Notification' in window && Notification.permission === 'granted') {
        new Notification('ポモドーロタイマー', {
            body: message,
            icon: '/static/pomodoro-icon.png'
        });
    }
    
    // アラート音
    if (settings.soundEnabled) {
        playAlertSound();
    }
    
    // フォールバックアラート
    if (!settings.notificationEnabled || Notification.permission !== 'granted') {
        alert(message);
    }
}

function playAlertSound() {
    // Web Audio APIで簡単なビープ音を生成
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.5);
}

function saveHistory(state) {
    const history = JSON.parse(localStorage.getItem('pomodoroHistory') || '[]');
    const today = new Date().toLocaleDateString('ja-JP');
    const time = new Date().toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit' });
    
    history.push({
        date: today,
        time: time,
        state: state === 'work' ? '作業' : state === 'short_break' ? '短い休憩' : '長い休憩',
        timestamp: Date.now()
    });
    
    localStorage.setItem('pomodoroHistory', JSON.stringify(history));
    displayHistory();
}

function displayHistory() {
    const history = JSON.parse(localStorage.getItem('pomodoroHistory') || '[]');
    const today = new Date().toLocaleDateString('ja-JP');
    const todayHistory = history.filter(h => h.date === today);
    
    const historyList = document.getElementById('history-list');
    if (todayHistory.length === 0) {
        historyList.innerHTML = '<p style="color: #999; font-size: 14px;">まだ記録がありません</p>';
    } else {
        historyList.innerHTML = todayHistory.reverse().map(h => 
            `<div class="history-item">${h.time} - ${h.state}完了</div>`
        ).join('');
    }
}

startBtn.onclick = function() {
    if (!pomodoroTimer.isRunning) {
        pomodoroTimer.start();
        intervalId = setInterval(tick, 1000);
    }
};

stopBtn.onclick = function() {
    if (pomodoroTimer.isRunning) {
        clearInterval(intervalId);
        pomodoroTimer.stop();
    }
};

resetBtn.onclick = function() {
    clearInterval(intervalId);
    pomodoroTimer.reset();
    updateDisplay();
};

// 設定パネルの表示/非表示
settingsBtn.onclick = function() {
    settingsPanel.classList.toggle('active');
    if (settingsPanel.classList.contains('active')) {
        // 現在の設定値を表示
        document.getElementById('work-time').value = pomodoroTimer.workTime / 60;
        document.getElementById('short-break-time').value = pomodoroTimer.shortBreakTime / 60;
        document.getElementById('long-break-time').value = pomodoroTimer.longBreakTime / 60;
        document.getElementById('sessions-before-long-break').value = pomodoroTimer.sessionsBeforeLongBreak;
        document.getElementById('sound-enabled').checked = settings.soundEnabled;
        document.getElementById('notification-enabled').checked = settings.notificationEnabled;
    }
};

// 設定の保存
saveSettingsBtn.onclick = function() {
    const newSettings = {
        workTime: parseInt(document.getElementById('work-time').value),
        shortBreakTime: parseInt(document.getElementById('short-break-time').value),
        longBreakTime: parseInt(document.getElementById('long-break-time').value),
        sessionsBeforeLongBreak: parseInt(document.getElementById('sessions-before-long-break').value),
        soundEnabled: document.getElementById('sound-enabled').checked,
        notificationEnabled: document.getElementById('notification-enabled').checked
    };
    
    localStorage.setItem('pomodoroSettings', JSON.stringify(newSettings));
    settings = loadSettings();
    
    // タイマーをリセットして新しい設定を反映
    clearInterval(intervalId);
    pomodoroTimer = new PomodoroTimer(settings);
    updateDisplay();
    
    settingsPanel.classList.remove('active');
    alert('設定を保存しました！');
};

// 履歴のクリア
clearHistoryBtn.onclick = function() {
    if (confirm('本当に履歴をクリアしますか？')) {
        localStorage.setItem('pomodoroHistory', '[]');
        displayHistory();
    }
};

// ブラウザ通知の許可をリクエスト
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}

// 初期表示
updateDisplay();
displayHistory();
