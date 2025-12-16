// ポモドーロタイマー - メインJavaScript

class PomodoroTimer {
    constructor() {
        // タイマー状態
        this.timeLeft = 1500; // 秒単位（デフォルト25分）
        this.totalTime = 1500;
        this.isRunning = false;
        this.currentType = 'work';
        this.intervalId = null;
        
        // 統計
        this.stats = {
            completed_pomodoros: 0,
            completed_breaks: 0,
            total_work_time: 0,
            total_break_time: 0,
            sessions_today: 0
        };
        
        // 設定
        this.settings = {
            notifications: true,
            sound: true,
            autoStartBreak: false,
            autoStartWork: false
        };
        
        // DOM要素
        this.timerDisplay = document.getElementById('timer');
        this.timerLabel = document.getElementById('timer-label');
        this.startBtn = document.getElementById('start-btn');
        this.pauseBtn = document.getElementById('pause-btn');
        this.resetBtn = document.getElementById('reset-btn');
        this.progressCircle = document.querySelector('.progress-ring-circle');
        
        // プログレスサークルの設定
        this.circleRadius = 130;
        this.circleCircumference = 2 * Math.PI * this.circleRadius;
        this.progressCircle.style.strokeDasharray = this.circleCircumference;
        this.progressCircle.style.strokeDashoffset = this.circleCircumference;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadSettings();
        this.loadStats();
        this.requestNotificationPermission();
        this.updateDisplay();
    }
    
    setupEventListeners() {
        // タブボタン
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTimerType(e.target));
        });
        
        // コントロールボタン
        this.startBtn.addEventListener('click', () => this.start());
        this.pauseBtn.addEventListener('click', () => this.pause());
        this.resetBtn.addEventListener('click', () => this.reset());
        
        // カスタムタイマー設定
        document.getElementById('set-custom-btn').addEventListener('click', () => this.setCustomTime());
        
        // 統計リセット
        document.getElementById('reset-stats-btn').addEventListener('click', () => this.resetStats());
        
        // 設定トグル
        document.getElementById('notification-toggle').addEventListener('change', (e) => {
            this.settings.notifications = e.target.checked;
            this.saveSettings();
        });
        
        document.getElementById('sound-toggle').addEventListener('change', (e) => {
            this.settings.sound = e.target.checked;
            this.saveSettings();
        });
        
        document.getElementById('auto-start-break').addEventListener('change', (e) => {
            this.settings.autoStartBreak = e.target.checked;
            this.saveSettings();
        });
        
        document.getElementById('auto-start-work').addEventListener('change', (e) => {
            this.settings.autoStartWork = e.target.checked;
            this.saveSettings();
        });
        
        // ページを離れる前の警告
        window.addEventListener('beforeunload', (e) => {
            if (this.isRunning) {
                e.preventDefault();
                e.returnValue = '';
            }
        });
    }
    
    switchTimerType(btn) {
        if (this.isRunning) {
            if (!confirm('タイマーが実行中です。切り替えますか？')) {
                return;
            }
            this.pause();
        }
        
        // アクティブクラスを切り替え
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // タイマータイプと時間を設定
        this.currentType = btn.dataset.type;
        this.totalTime = parseInt(btn.dataset.duration);
        this.timeLeft = this.totalTime;
        
        // ラベルを更新
        const labels = {
            'work': '作業時間',
            'break': '休憩時間',
            'long-break': '長休憩'
        };
        this.timerLabel.textContent = labels[this.currentType];
        
        // 色を変更
        const colors = {
            'work': '#e74c3c',
            'break': '#3498db',
            'long-break': '#9b59b6'
        };
        this.progressCircle.style.stroke = colors[this.currentType];
        
        this.updateDisplay();
        this.reset();
    }
    
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.startBtn.disabled = true;
        this.pauseBtn.disabled = false;
        
        this.intervalId = setInterval(() => {
            this.timeLeft--;
            this.updateDisplay();
            
            if (this.timeLeft <= 0) {
                this.complete();
            }
        }, 1000);
    }
    
    pause() {
        if (!this.isRunning) return;
        
        this.isRunning = false;
        this.startBtn.disabled = false;
        this.pauseBtn.disabled = true;
        
        clearInterval(this.intervalId);
    }
    
    reset() {
        this.pause();
        this.timeLeft = this.totalTime;
        this.updateDisplay();
    }
    
    complete() {
        this.pause();
        
        // 完了したタイマーの種類に応じて処理
        const duration = this.totalTime;
        
        // サーバーに完了を通知
        fetch('/api/complete_pomodoro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: this.currentType,
                duration: duration
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.stats = data.stats;
                this.updateStatsDisplay();
            }
        })
        .catch(error => console.error('Error:', error));
        
        // 通知とサウンド
        this.showNotification();
        this.playSound();
        
        // 自動開始
        if (this.currentType === 'work' && this.settings.autoStartBreak) {
            setTimeout(() => {
                document.querySelector('[data-type="break"]').click();
                this.start();
            }, 2000);
        } else if (this.currentType === 'break' && this.settings.autoStartWork) {
            setTimeout(() => {
                document.querySelector('[data-type="work"]').click();
                this.start();
            }, 2000);
        }
        
        // タイマーをリセット
        this.reset();
    }
    
    setCustomTime() {
        const minutes = parseInt(document.getElementById('custom-minutes').value) || 0;
        const seconds = parseInt(document.getElementById('custom-seconds').value) || 0;
        
        if (minutes === 0 && seconds === 0) {
            alert('有効な時間を入力してください');
            return;
        }
        
        if (this.isRunning && !confirm('タイマーが実行中です。変更しますか？')) {
            return;
        }
        
        this.pause();
        this.totalTime = (minutes * 60) + seconds;
        this.timeLeft = this.totalTime;
        this.updateDisplay();
    }
    
    updateDisplay() {
        // 時間表示を更新
        const minutes = Math.floor(this.timeLeft / 60);
        const seconds = this.timeLeft % 60;
        this.timerDisplay.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        
        // プログレスサークルを更新
        const progress = (this.totalTime - this.timeLeft) / this.totalTime;
        const offset = this.circleCircumference * (1 - progress);
        this.progressCircle.style.strokeDashoffset = offset;
        
        // ドキュメントタイトルを更新
        if (this.isRunning) {
            document.title = `${this.timerDisplay.textContent} - ポモドーロタイマー`;
        } else {
            document.title = 'ポモドーロタイマー';
        }
    }
    
    updateStatsDisplay() {
        document.getElementById('stat-pomodoros').textContent = this.stats.completed_pomodoros;
        document.getElementById('stat-breaks').textContent = this.stats.completed_breaks;
        document.getElementById('stat-work-time').textContent = Math.floor(this.stats.total_work_time / 60) + '分';
        document.getElementById('stat-sessions').textContent = this.stats.sessions_today;
    }
    
    loadStats() {
        fetch('/api/get_stats')
            .then(response => response.json())
            .then(data => {
                this.stats = data;
                this.updateStatsDisplay();
            })
            .catch(error => console.error('Error loading stats:', error));
    }
    
    resetStats() {
        if (!confirm('統計をリセットしますか？この操作は取り消せません。')) {
            return;
        }
        
        fetch('/api/reset_stats', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.stats = {
                    completed_pomodoros: 0,
                    completed_breaks: 0,
                    total_work_time: 0,
                    total_break_time: 0,
                    sessions_today: 0
                };
                this.updateStatsDisplay();
                alert('統計をリセットしました');
            }
        })
        .catch(error => console.error('Error resetting stats:', error));
    }
    
    requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }
    
    showNotification() {
        if (!this.settings.notifications) return;
        
        if ('Notification' in window && Notification.permission === 'granted') {
            const messages = {
                'work': '作業時間が終了しました！休憩しましょう 🍅',
                'break': '休憩時間が終了しました！作業に戻りましょう ⚡',
                'long-break': '長休憩が終了しました！また頑張りましょう 💪'
            };
            
            new Notification('ポモドーロタイマー', {
                body: messages[this.currentType],
                icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🍅</text></svg>',
                badge: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🍅</text></svg>',
                vibrate: [200, 100, 200]
            });
        }
    }
    
    playSound() {
        if (!this.settings.sound) return;
        
        // Web Audio APIを使用してビープ音を生成
        try {
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
        } catch (error) {
            console.error('Error playing sound:', error);
        }
    }
    
    saveSettings() {
        localStorage.setItem('pomodoroSettings', JSON.stringify(this.settings));
    }
    
    loadSettings() {
        const saved = localStorage.getItem('pomodoroSettings');
        if (saved) {
            this.settings = { ...this.settings, ...JSON.parse(saved) };
            
            // UIを更新
            document.getElementById('notification-toggle').checked = this.settings.notifications;
            document.getElementById('sound-toggle').checked = this.settings.sound;
            document.getElementById('auto-start-break').checked = this.settings.autoStartBreak;
            document.getElementById('auto-start-work').checked = this.settings.autoStartWork;
        }
    }
}

// アプリケーション初期化
document.addEventListener('DOMContentLoaded', () => {
    const timer = new PomodoroTimer();
    
    // グローバルスコープに追加（デバッグ用）
    window.pomodoroTimer = timer;
});
