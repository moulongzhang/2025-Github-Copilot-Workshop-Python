// ポモドーロタイマーアプリケーション

class PomodoroTimer {
    constructor() {
        this.timeDisplay = document.querySelector('.time');
        this.statusDisplay = document.querySelector('.status');
        this.counterDisplay = document.querySelector('.counter-value');
        
        this.startBtn = document.getElementById('start-btn');
        this.resetBtn = document.getElementById('reset-btn');
        
        // 設定関連の要素
        this.settingsBtn = document.getElementById('settings-btn');
        this.settingsPanel = document.getElementById('settings-panel');
        this.workTimeInput = document.getElementById('work-time');
        this.shortBreakTimeInput = document.getElementById('short-break-time');
        this.longBreakTimeInput = document.getElementById('long-break-time');
        this.saveSettingsBtn = document.getElementById('save-settings');
        this.cancelSettingsBtn = document.getElementById('cancel-settings');
        
        // 履歴関連の要素
        this.historyBtn = document.getElementById('history-btn');
        this.historyPanel = document.getElementById('history-panel');
        this.refreshHistoryBtn = document.getElementById('refresh-history');
        this.closeHistoryBtn = document.getElementById('close-history');
        
        // タイマー設定（秒）
        this.workTime = 25 * 60; // 25分
        this.shortBreakTime = 5 * 60; // 5分
        this.longBreakTime = 15 * 60; // 15分
        
        // 現在の状態
        this.currentTime = this.workTime;
        this.isRunning = false;
        this.isWorkSession = true;
        this.completedPomodoros = 0;
        this.intervalId = null;
        
        // 初期化
        this.init();
    }
    
    init() {
        // イベントリスナーを設定
        this.startBtn.addEventListener('click', () => this.start());
        this.resetBtn.addEventListener('click', () => this.reset());
        
        // 設定関連のイベントリスナー
        this.settingsBtn.addEventListener('click', () => this.toggleSettings());
        this.saveSettingsBtn.addEventListener('click', () => this.saveSettings());
        this.cancelSettingsBtn.addEventListener('click', () => this.cancelSettings());
        
        // 履歴関連のイベントリスナー
        this.historyBtn.addEventListener('click', () => this.toggleHistory());
        this.refreshHistoryBtn.addEventListener('click', () => this.loadHistory());
        this.closeHistoryBtn.addEventListener('click', () => this.closeHistory());
        
        // 設定を読み込み
        this.loadSettings();
        
        // 初期表示を更新
        this.updateDisplay();
        
        console.log('ポモドーロタイマーが初期化されました');
    }
    
    start() {
        if (!this.isRunning) {
            this.isRunning = true;
            this.intervalId = setInterval(() => {
                this.tick();
            }, 1000);
            
            // ボタンの状態を更新
            this.startBtn.textContent = '⏸ 一時停止';
            
            console.log('タイマー開始');
        } else {
            // 一時停止
            this.pause();
        }
    }
    
    pause() {
        this.isRunning = false;
        clearInterval(this.intervalId);
        this.intervalId = null;
        
        // ボタンの状態を更新
        this.startBtn.textContent = '▶ 再開';
        
        console.log('タイマー一時停止');
    }
    
    reset() {
        this.pause();
        
        // 現在のセッションタイプに応じて時間をリセット
        if (this.isWorkSession) {
            this.currentTime = this.workTime;
        } else {
            // 休憩時間の決定（4セット目後は長い休憩）
            this.currentTime = (this.completedPomodoros % 4 === 0 && this.completedPomodoros > 0) 
                ? this.longBreakTime 
                : this.shortBreakTime;
        }
        
        // ボタンの状態をリセット
        this.startBtn.textContent = '▶ スタート';
        
        this.updateDisplay();
        console.log('タイマーリセット');
    }
    
    tick() {
        if (this.currentTime > 0) {
            this.currentTime--;
            this.updateDisplay();
        } else {
            // タイマー終了
            this.onTimerComplete();
        }
    }
    
    onTimerComplete() {
        this.pause();
        
        if (this.isWorkSession) {
            // 作業セッション完了 - 履歴に保存
            this.saveToHistory('work', this.workTime);
            
            this.completedPomodoros++;
            this.isWorkSession = false;
            
            // 次は休憩セッション
            this.currentTime = (this.completedPomodoros % 4 === 0) 
                ? this.longBreakTime 
                : this.shortBreakTime;
                
            this.showNotification('作業時間終了！', '休憩時間を開始しましょう。');
        } else {
            // 休憩セッション完了 - 履歴に保存
            const breakDuration = (this.completedPomodoros % 4 === 0) 
                ? this.longBreakTime 
                : this.shortBreakTime;
            this.saveToHistory('break', breakDuration);
            
            this.isWorkSession = true;
            this.currentTime = this.workTime;
            
            this.showNotification('休憩時間終了！', '次のポモドーロを開始しましょう。');
        }
        
        // ボタンの状態をリセット
        this.startBtn.textContent = '▶ スタート';
        
        this.updateDisplay();
        console.log('タイマー完了 - セッション切り替え');
    }
    
    updateDisplay() {
        // 時間表示を更新
        this.timeDisplay.textContent = this.formatTime(this.currentTime);
        
        // 状態表示を更新
        if (this.isWorkSession) {
            this.statusDisplay.textContent = '作業中';
            this.statusDisplay.className = 'status work';
        } else {
            const isLongBreak = (this.completedPomodoros % 4 === 0 && this.completedPomodoros > 0);
            this.statusDisplay.textContent = isLongBreak ? '長い休憩中' : '休憩中';
            this.statusDisplay.className = 'status break';
        }
        
        // カウンター表示を更新
        this.counterDisplay.textContent = this.completedPomodoros;
        
        // ページタイトルも更新
        document.title = `${this.formatTime(this.currentTime)} - ポモドーロタイマー`;
    }
    
    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    
    showNotification(title, message) {
        // ブラウザ通知（基本的なアラート）
        if (Notification.permission === 'granted') {
            new Notification(title, { body: message });
        } else if (Notification.permission !== 'denied') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    new Notification(title, { body: message });
                }
            });
        } else {
            // フォールバック: アラート
            alert(`${title}\n${message}`);
        }
        
        // 音の再生（可能な場合）
        this.playNotificationSound();
    }
    
    playNotificationSound() {
        try {
            // Web Audio APIを使用した簡単なビープ音
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.value = 800; // 800Hz
            gainNode.gain.value = 0.1; // 音量
            
            oscillator.start();
            oscillator.stop(audioContext.currentTime + 0.2); // 0.2秒間
        } catch (error) {
            console.log('音声再生に失敗しました:', error);
        }
    }
    
    // 設定関連のメソッド
    toggleSettings() {
        this.settingsPanel.classList.toggle('hidden');
        if (!this.settingsPanel.classList.contains('hidden')) {
            // 設定パネルを開く時は現在の値を表示
            this.workTimeInput.value = this.workTime / 60;
            this.shortBreakTimeInput.value = this.shortBreakTime / 60;
            this.longBreakTimeInput.value = this.longBreakTime / 60;
        }
    }
    
    saveSettings() {
        const workTime = parseInt(this.workTimeInput.value) * 60;
        const shortBreakTime = parseInt(this.shortBreakTimeInput.value) * 60;
        const longBreakTime = parseInt(this.longBreakTimeInput.value) * 60;
        
        // バリデーション
        if (workTime < 60 || workTime > 3600 || 
            shortBreakTime < 60 || shortBreakTime > 1800 || 
            longBreakTime < 60 || longBreakTime > 3600) {
            alert('設定値が範囲外です。適切な値を入力してください。');
            return;
        }
        
        // 設定を更新
        this.workTime = workTime;
        this.shortBreakTime = shortBreakTime;
        this.longBreakTime = longBreakTime;
        
        // ローカルストレージに保存
        const settings = {
            workTime: this.workTime,
            shortBreakTime: this.shortBreakTime,
            longBreakTime: this.longBreakTime
        };
        localStorage.setItem('pomodoroSettings', JSON.stringify(settings));
        
        // 現在のタイマーをリセット
        this.reset();
        
        // 設定パネルを閉じる
        this.settingsPanel.classList.add('hidden');
        
        console.log('設定が保存されました');
        alert('設定が保存されました！');
    }
    
    cancelSettings() {
        this.settingsPanel.classList.add('hidden');
    }
    
    loadSettings() {
        try {
            const savedSettings = localStorage.getItem('pomodoroSettings');
            if (savedSettings) {
                const settings = JSON.parse(savedSettings);
                this.workTime = settings.workTime || this.workTime;
                this.shortBreakTime = settings.shortBreakTime || this.shortBreakTime;
                this.longBreakTime = settings.longBreakTime || this.longBreakTime;
                
                // 現在の時間も更新
                if (this.isWorkSession) {
                    this.currentTime = this.workTime;
                }
                
                console.log('設定が読み込まれました');
            }
        } catch (error) {
            console.log('設定の読み込みに失敗しました:', error);
        }
    }
    
    // 履歴関連のメソッド
    toggleHistory() {
        this.historyPanel.classList.toggle('hidden');
        if (!this.historyPanel.classList.contains('hidden')) {
            this.loadHistory();
        }
    }
    
    closeHistory() {
        this.historyPanel.classList.add('hidden');
    }
    
    async loadHistory() {
        try {
            // 統計情報を取得
            const statsResponse = await fetch('/api/stats');
            const stats = await statsResponse.json();
            
            // 統計情報を表示
            document.getElementById('today-pomodoros').textContent = stats.today_pomodoros || 0;
            document.getElementById('total-pomodoros').textContent = stats.total_pomodoros || 0;
            
            const totalHours = Math.floor((stats.total_work_time || 0) / 3600);
            const totalMinutes = Math.floor(((stats.total_work_time || 0) % 3600) / 60);
            document.getElementById('total-work-time').textContent = `${totalHours}時間${totalMinutes}分`;
            
            // 履歴データを取得
            const historyResponse = await fetch('/api/history');
            const history = await historyResponse.json();
            
            // 履歴リストを表示
            this.displayHistory(history);
            
        } catch (error) {
            console.error('履歴の読み込みに失敗しました:', error);
            alert('履歴の読み込みに失敗しました');
        }
    }
    
    displayHistory(history) {
        const historyList = document.getElementById('history-list');
        historyList.innerHTML = '';
        
        if (history.length === 0) {
            historyList.innerHTML = '<p style="text-align: center; color: #666;">履歴がありません</p>';
            return;
        }
        
        // 最新10件のみ表示
        const recentHistory = history.slice(-10).reverse();
        
        recentHistory.forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = `history-item ${item.session_type}`;
            
            const sessionType = item.session_type === 'work' ? '作業' : '休憩';
            const duration = this.formatTime(item.duration);
            const date = new Date(item.completed_at);
            const timeStr = date.toLocaleString('ja-JP', {
                month: 'numeric',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
            
            historyItem.innerHTML = `
                <span>${sessionType} (${duration})</span>
                <span>${timeStr}</span>
            `;
            
            historyList.appendChild(historyItem);
        });
    }
    
    async saveToHistory(sessionType, duration) {
        try {
            const historyData = {
                session_type: sessionType,
                duration: duration,
                pomodoro_count: this.completedPomodoros
            };
            
            const response = await fetch('/api/history', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(historyData)
            });
            
            if (response.ok) {
                console.log('履歴が保存されました');
            } else {
                console.error('履歴の保存に失敗しました');
            }
            
        } catch (error) {
            console.error('履歴の保存エラー:', error);
        }
    }
}

// ページ読み込み完了後にタイマーを初期化
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimer();
});
