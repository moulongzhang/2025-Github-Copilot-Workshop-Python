// =============================================================================
// ポモドーロタイマー - メインJavaScript
// =============================================================================

/**
 * ポモドーロタイマーアプリケーションのメインクラス
 * タイマー機能、設定管理、UI制御を統合管理
 */
class PomodoroTimer {
    constructor() {
        // タイマー設定（デフォルト値）
        this.defaultSettings = {
            workDuration: 25,        // 作業時間（分）
            shortBreakDuration: 5,   // 短休憩時間（分）
            longBreakDuration: 15,   // 長休憩時間（分）
            sessionsUntilLongBreak: 4, // 長休憩までのセッション数
            autoStartBreaks: false,  // 休憩の自動開始
            autoStartWork: false,    // 作業の自動開始
            soundNotifications: true // 音声通知
        };

        // 現在の設定
        this.settings = { ...this.defaultSettings };

        // タイマー状態
        this.currentMode = 'work'; // 'work', 'short-break', 'long-break'
        this.isRunning = false;
        this.isPaused = false;
        this.timeRemaining = this.settings.workDuration * 60; // 秒単位
        this.sessionCount = 0;
        
        // タイマーID
        this.timerId = null;
        
        // DOM要素の参照
        this.elements = {};
        
        // 初期化
        this.init();
    }

    /**
     * アプリケーションの初期化
     */
    init() {
        this.getDOMElements();
        this.loadSettings();
        this.bindEvents();
        this.updateDisplay();
        this.setupAccessibility();
        
        console.log('ポモドーロタイマーアプリケーションが初期化されました');
    }

    /**
     * DOM要素の参照を取得
     */
    getDOMElements() {
        // タイマー表示
        this.elements.timerDisplay = document.getElementById('timer-display');
        this.elements.timerMode = document.getElementById('timer-mode');
        this.elements.currentMode = document.getElementById('current-mode');
        this.elements.sessionCount = document.getElementById('session-count');
        this.elements.progressCircle = document.getElementById('progress-circle');
        
        // コントロールボタン
        this.elements.startBtn = document.getElementById('start-btn');
        this.elements.pauseBtn = document.getElementById('pause-btn');
        this.elements.resetBtn = document.getElementById('reset-btn');
        this.elements.skipBtn = document.getElementById('skip-btn');
        
        // 設定パネル
        this.elements.settingsToggle = document.getElementById('settings-toggle');
        this.elements.settingsPanel = document.getElementById('settings-panel');
        this.elements.workDuration = document.getElementById('work-duration');
        this.elements.shortBreak = document.getElementById('short-break');
        this.elements.longBreak = document.getElementById('long-break');
        this.elements.sessionsUntilLongBreak = document.getElementById('sessions-until-long-break');
        this.elements.autoStartBreaks = document.getElementById('auto-start-breaks');
        this.elements.autoStartWork = document.getElementById('auto-start-work');
        this.elements.soundNotifications = document.getElementById('sound-notifications');
        this.elements.saveSettings = document.getElementById('save-settings');
        this.elements.resetSettings = document.getElementById('reset-settings');
        
        // モーダル
        this.elements.modal = document.getElementById('notification-modal');
        this.elements.modalTitle = document.getElementById('modal-title');
        this.elements.modalMessage = document.getElementById('modal-message');
        this.elements.modalConfirm = document.getElementById('modal-confirm');
        this.elements.modalClose = document.getElementById('modal-close');
        
        // スクリーンリーダー用
        this.elements.srAnnouncements = document.getElementById('sr-announcements');
    }

    /**
     * イベントリスナーの設定
     */
    bindEvents() {
        // コントロールボタン
        this.elements.startBtn.addEventListener('click', () => this.startTimer());
        this.elements.pauseBtn.addEventListener('click', () => this.pauseTimer());
        this.elements.resetBtn.addEventListener('click', () => this.resetTimer());
        this.elements.skipBtn.addEventListener('click', () => this.skipSession());
        
        // 設定パネル
        this.elements.settingsToggle.addEventListener('click', () => this.toggleSettings());
        this.elements.saveSettings.addEventListener('click', () => this.saveSettings());
        this.elements.resetSettings.addEventListener('click', () => this.resetSettingsToDefault());
        
        // モーダル
        this.elements.modalConfirm.addEventListener('click', () => this.closeModal());
        this.elements.modalClose.addEventListener('click', () => this.closeModal());
        
        // キーボードショートカット
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
        
        // ページ離脱時の警告
        window.addEventListener('beforeunload', (e) => {
            if (this.isRunning) {
                e.preventDefault();
                e.returnValue = 'タイマーが実行中です。ページを離れますか？';
            }
        });

        // ページフォーカス復帰時の同期
        document.addEventListener('visibilitychange', () => this.handleVisibilityChange());
    }

    /**
     * タイマー開始
     */
    startTimer() {
        if (this.isRunning && !this.isPaused) return;

        this.isRunning = true;
        this.isPaused = false;
        
        this.updateButtonStates();
        this.announceToScreenReader(`タイマーが開始されました。${this.getModeDisplayName()}モードです。`);
        
        this.timerId = setInterval(() => {
            this.tick();
        }, 1000);

        console.log(`タイマー開始: ${this.currentMode} モード`);
    }

    /**
     * タイマー一時停止
     */
    pauseTimer() {
        if (!this.isRunning || this.isPaused) return;

        this.isPaused = true;
        clearInterval(this.timerId);
        
        this.updateButtonStates();
        this.announceToScreenReader('タイマーが一時停止されました');
        
        console.log('タイマー一時停止');
    }

    /**
     * タイマーリセット
     */
    resetTimer() {
        this.isRunning = false;
        this.isPaused = false;
        clearInterval(this.timerId);
        
        this.timeRemaining = this.getCurrentModeDuration() * 60;
        this.updateDisplay();
        this.updateButtonStates();
        this.announceToScreenReader('タイマーがリセットされました');
        
        console.log('タイマーリセット');
    }

    /**
     * セッションスキップ
     */
    skipSession() {
        this.completeSession();
        this.announceToScreenReader('セッションがスキップされました');
        console.log('セッションスキップ');
    }

    /**
     * タイマーの1秒ずつの処理
     */
    tick() {
        if (!this.isRunning || this.isPaused) return;

        this.timeRemaining--;
        this.updateDisplay();

        // 時間終了チェック
        if (this.timeRemaining <= 0) {
            this.completeSession();
        }
    }

    /**
     * セッション完了処理
     */
    completeSession() {
        this.isRunning = false;
        clearInterval(this.timerId);

        // セッション数の更新
        if (this.currentMode === 'work') {
            this.sessionCount++;
        }

        // 完了通知
        this.showCompletionNotification();
        
        // 次のモードに切り替え
        this.switchToNextMode();
        
        // 自動開始チェック
        this.checkAutoStart();
    }

    /**
     * 次のモードに切り替え
     */
    switchToNextMode() {
        if (this.currentMode === 'work') {
            // 作業完了後は休憩
            if (this.sessionCount % this.settings.sessionsUntilLongBreak === 0) {
                this.currentMode = 'long-break';
            } else {
                this.currentMode = 'short-break';
            }
        } else {
            // 休憩完了後は作業
            this.currentMode = 'work';
        }

        this.timeRemaining = this.getCurrentModeDuration() * 60;
        this.updateDisplay();
        this.updateButtonStates();
        this.updateBodyClass();

        console.log(`モード切替: ${this.currentMode}`);
    }

    /**
     * 自動開始チェック
     */
    checkAutoStart() {
        const shouldAutoStart = 
            (this.currentMode === 'work' && this.settings.autoStartWork) ||
            ((this.currentMode === 'short-break' || this.currentMode === 'long-break') && this.settings.autoStartBreaks);

        if (shouldAutoStart) {
            setTimeout(() => {
                this.startTimer();
            }, 2000); // 2秒後に自動開始
        }
    }

    /**
     * 現在のモードの表示名を取得
     */
    getModeDisplayName() {
        const modeNames = {
            'work': '集中',
            'short-break': '短休憩',
            'long-break': '長休憩'
        };
        return modeNames[this.currentMode] || '不明';
    }

    /**
     * 現在のモードの継続時間を取得（分）
     */
    getCurrentModeDuration() {
        switch (this.currentMode) {
            case 'work': return this.settings.workDuration;
            case 'short-break': return this.settings.shortBreakDuration;
            case 'long-break': return this.settings.longBreakDuration;
            default: return this.settings.workDuration;
        }
    }

    /**
     * 表示の更新
     */
    updateDisplay() {
        // 時間表示の更新
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        const timeString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        this.elements.timerDisplay.textContent = timeString;
        this.elements.timerMode.textContent = this.getModeDisplayText();
        this.elements.currentMode.textContent = `${this.getModeDisplayName()}モード`;
        this.elements.sessionCount.textContent = this.sessionCount;

        // プログレス円の更新
        this.updateProgressCircle();
        
        // ページタイトルの更新
        if (this.isRunning && !this.isPaused) {
            document.title = `${timeString} - ${this.getModeDisplayName()} | ポモドーロタイマー`;
        } else {
            document.title = 'ポモドーロタイマー';
        }
    }

    /**
     * モード表示テキストを取得
     */
    getModeDisplayText() {
        switch (this.currentMode) {
            case 'work': return '作業時間';
            case 'short-break': return '短休憩';
            case 'long-break': return '長休憩';
            default: return '作業時間';
        }
    }

    /**
     * プログレス円の更新
     */
    updateProgressCircle() {
        const totalTime = this.getCurrentModeDuration() * 60;
        const progressRatio = (totalTime - this.timeRemaining) / totalTime;
        const circumference = 2 * Math.PI * 90; // r=90の円周
        const offset = circumference * (1 - progressRatio);
        
        this.elements.progressCircle.style.strokeDashoffset = offset;
    }

    /**
     * bodyクラスの更新（CSS用）
     */
    updateBodyClass() {
        document.body.className = document.body.className.replace(/mode-\w+/g, '');
        document.body.classList.add(`mode-${this.currentMode}`);
    }

    /**
     * ボタン状態の更新
     */
    updateButtonStates() {
        const isIdle = !this.isRunning && !this.isPaused;
        const isRunning = this.isRunning && !this.isPaused;
        const isPaused = this.isPaused;

        this.elements.startBtn.disabled = isRunning;
        this.elements.pauseBtn.disabled = isIdle;
        
        // ボタンテキストの更新
        if (isPaused) {
            this.elements.startBtn.querySelector('.btn-text').textContent = '再開';
        } else {
            this.elements.startBtn.querySelector('.btn-text').textContent = '開始';
        }
    }

    /**
     * 完了通知の表示
     */
    showCompletionNotification() {
        const modeNameMap = {
            'work': '作業時間',
            'short-break': '短休憩',
            'long-break': '長休憩'
        };

        const title = `${modeNameMap[this.currentMode]}完了！`;
        const message = this.currentMode === 'work' 
            ? 'お疲れさまでした！休憩時間です。'
            : 'リフレッシュできましたか？作業時間です。';

        this.showModal(title, message);
        
        // 音声通知
        if (this.settings.soundNotifications) {
            this.playNotificationSound();
        }

        // スクリーンリーダー通知
        this.announceToScreenReader(`${title} ${message}`);
    }

    /**
     * モーダル表示
     */
    showModal(title, message) {
        this.elements.modalTitle.textContent = title;
        this.elements.modalMessage.textContent = message;
        this.elements.modal.classList.add('active');
        this.elements.modal.setAttribute('aria-hidden', 'false');
        
        // モーダル内の確認ボタンにフォーカス
        this.elements.modalConfirm.focus();
    }

    /**
     * モーダル非表示
     */
    closeModal() {
        this.elements.modal.classList.remove('active');
        this.elements.modal.setAttribute('aria-hidden', 'true');
    }

    /**
     * 通知音の再生
     */
    playNotificationSound() {
        // Web Audio APIを使用して通知音を生成・再生
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.value = 800; // 周波数
            gainNode.gain.value = 0.1; // 音量

            oscillator.start();
            oscillator.stop(audioContext.currentTime + 0.3); // 0.3秒間再生
        } catch (error) {
            console.warn('音声通知の再生に失敗しました:', error);
        }
    }

    /**
     * 設定パネルの表示切替
     */
    toggleSettings() {
        this.elements.settingsPanel.classList.toggle('active');
        const isActive = this.elements.settingsPanel.classList.contains('active');
        
        this.elements.settingsToggle.textContent = isActive ? '⚙️ 設定を閉じる' : '⚙️ 設定';
        
        if (isActive) {
            this.loadSettingsToForm();
        }
    }

    /**
     * フォームに設定値を読み込み
     */
    loadSettingsToForm() {
        this.elements.workDuration.value = this.settings.workDuration;
        this.elements.shortBreak.value = this.settings.shortBreakDuration;
        this.elements.longBreak.value = this.settings.longBreakDuration;
        this.elements.sessionsUntilLongBreak.value = this.settings.sessionsUntilLongBreak;
        this.elements.autoStartBreaks.checked = this.settings.autoStartBreaks;
        this.elements.autoStartWork.checked = this.settings.autoStartWork;
        this.elements.soundNotifications.checked = this.settings.soundNotifications;
    }

    /**
     * 設定の保存
     */
    saveSettings() {
        // フォームから値を取得
        const newSettings = {
            workDuration: parseInt(this.elements.workDuration.value, 10),
            shortBreakDuration: parseInt(this.elements.shortBreak.value, 10),
            longBreakDuration: parseInt(this.elements.longBreak.value, 10),
            sessionsUntilLongBreak: parseInt(this.elements.sessionsUntilLongBreak.value, 10),
            autoStartBreaks: this.elements.autoStartBreaks.checked,
            autoStartWork: this.elements.autoStartWork.checked,
            soundNotifications: this.elements.soundNotifications.checked
        };

        // バリデーション
        if (!this.validateSettings(newSettings)) {
            return;
        }

        // 設定を更新
        this.settings = newSettings;
        
        // ローカルストレージに保存
        try {
            localStorage.setItem('pomodoroSettings', JSON.stringify(this.settings));
            console.log('設定が保存されました');
        } catch (error) {
            console.error('設定の保存に失敗しました:', error);
        }

        // タイマーが停止中なら時間を更新
        if (!this.isRunning) {
            this.timeRemaining = this.getCurrentModeDuration() * 60;
            this.updateDisplay();
        }

        // 設定パネルを閉じる
        this.toggleSettings();
        this.announceToScreenReader('設定が保存されました');
    }

    /**
     * 設定値のバリデーション
     */
    validateSettings(settings) {
        if (settings.workDuration < 1 || settings.workDuration > 60) {
            alert('作業時間は1-60分の間で設定してください');
            return false;
        }
        if (settings.shortBreakDuration < 1 || settings.shortBreakDuration > 30) {
            alert('短休憩時間は1-30分の間で設定してください');
            return false;
        }
        if (settings.longBreakDuration < 1 || settings.longBreakDuration > 60) {
            alert('長休憩時間は1-60分の間で設定してください');
            return false;
        }
        if (settings.sessionsUntilLongBreak < 1 || settings.sessionsUntilLongBreak > 10) {
            alert('長休憩までのセッション数は1-10の間で設定してください');
            return false;
        }
        return true;
    }

    /**
     * 設定をデフォルトにリセット
     */
    resetSettingsToDefault() {
        if (confirm('設定をデフォルト値に戻しますか？')) {
            this.settings = { ...this.defaultSettings };
            this.loadSettingsToForm();
            this.announceToScreenReader('設定がデフォルトに戻されました');
            
            // タイマーが停止中なら時間を更新
            if (!this.isRunning) {
                this.timeRemaining = this.getCurrentModeDuration() * 60;
                this.updateDisplay();
            }
        }
    }

    /**
     * ローカルストレージから設定を読み込み
     */
    loadSettings() {
        try {
            const savedSettings = localStorage.getItem('pomodoroSettings');
            if (savedSettings) {
                this.settings = { ...this.defaultSettings, ...JSON.parse(savedSettings) };
                console.log('保存された設定を読み込みました');
            }
        } catch (error) {
            console.error('設定の読み込みに失敗しました:', error);
        }
        
        this.timeRemaining = this.getCurrentModeDuration() * 60;
    }

    /**
     * キーボードショートカット処理
     */
    handleKeyboard(event) {
        // 設定パネルが開いているときは無効
        if (this.elements.settingsPanel.classList.contains('active')) {
            if (event.key === 'Escape') {
                this.toggleSettings();
            }
            return;
        }

        // モーダルが開いているときは無効
        if (this.elements.modal.classList.contains('active')) {
            if (event.key === 'Escape' || event.key === 'Enter') {
                this.closeModal();
            }
            return;
        }

        switch (event.key) {
            case ' ': // スペースキー
                event.preventDefault();
                if (this.isRunning && !this.isPaused) {
                    this.pauseTimer();
                } else {
                    this.startTimer();
                }
                break;
            case 'r':
                event.preventDefault();
                this.resetTimer();
                break;
            case 's':
                event.preventDefault();
                this.skipSession();
                break;
            case 'Escape':
                if (this.elements.settingsPanel.classList.contains('active')) {
                    this.toggleSettings();
                }
                break;
        }
    }

    /**
     * ページの表示状態変更時の処理
     */
    handleVisibilityChange() {
        if (!document.hidden && this.isRunning) {
            // ページがアクティブになったときの時刻同期処理
            // 実際のアプリではより精密な同期が必要
            console.log('ページがアクティブになりました');
        }
    }

    /**
     * アクセシビリティ機能の設定
     */
    setupAccessibility() {
        // ARIA属性の設定
        this.elements.timerDisplay.setAttribute('aria-label', 'タイマー表示');
        this.elements.sessionCount.setAttribute('aria-label', '完了セッション数');
        
        // フォーカス可能要素の設定
        this.elements.timerDisplay.setAttribute('tabindex', '0');
        
        this.updateBodyClass();
    }

    /**
     * スクリーンリーダー用の音声読み上げ
     */
    announceToScreenReader(message) {
        this.elements.srAnnouncements.textContent = message;
        // 少し遅延させて確実に読み上げられるようにする
        setTimeout(() => {
            this.elements.srAnnouncements.textContent = '';
        }, 1000);
    }
}

// =============================================================================
// アプリケーション初期化
// =============================================================================

// DOMが読み込まれたら初期化
document.addEventListener('DOMContentLoaded', () => {
    window.pomodoroTimer = new PomodoroTimer();
});

// Service Worker登録（将来のPWA化のため）
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered: ', registration))
        //     .catch(registrationError => console.log('SW registration failed: ', registrationError));
    });
}

// =============================================================================
// ユーティリティ関数
// =============================================================================

/**
 * 時間（秒）を分:秒形式に変換
 * @param {number} seconds - 秒数
 * @returns {string} - MM:SS形式の文字列
 */
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

/**
 * 分を秒に変換
 * @param {number} minutes - 分数
 * @returns {number} - 秒数
 */
function minutesToSeconds(minutes) {
    return minutes * 60;
}

/**
 * デバッグモード（開発用）
 */
if (process.env.NODE_ENV === 'development') {
    window.debugPomodoro = {
        setTime: (seconds) => {
            if (window.pomodoroTimer) {
                window.pomodoroTimer.timeRemaining = seconds;
                window.pomodoroTimer.updateDisplay();
            }
        },
        getState: () => {
            if (window.pomodoroTimer) {
                return {
                    mode: window.pomodoroTimer.currentMode,
                    timeRemaining: window.pomodoroTimer.timeRemaining,
                    isRunning: window.pomodoroTimer.isRunning,
                    isPaused: window.pomodoroTimer.isPaused,
                    sessionCount: window.pomodoroTimer.sessionCount
                };
            }
        }
    };
}
