/**
 * タイマーエンジン - 純粋関数でタイマーロジックを実装
 * DOMに依存しないため、テストが容易
 */

const TimerEngine = {
    /**
     * 秒数を MM:SS 形式にフォーマット
     * @param {number} seconds - 秒数
     * @returns {string} MM:SS 形式の文字列
     */
    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },

    /**
     * 進捗率を計算
     * @param {number} remaining - 残り時間（秒）
     * @param {number} total - 合計時間（秒）
     * @returns {number} 進捗率（0-100）
     */
    calculateProgress(remaining, total) {
        if (total === 0) return 0;
        return ((total - remaining) / total) * 100;
    },

    /**
     * SVG円のストロークオフセットを計算
     * @param {number} progress - 進捗率（0-100）
     * @param {number} circumference - 円周（デフォルト: 628）
     * @returns {number} ストロークオフセット
     */
    calculateStrokeOffset(progress, circumference = 628) {
        return circumference - (progress / 100) * circumference;
    },

    /**
     * 次のモードを取得
     * @param {string} currentMode - 現在のモード
     * @param {number} completedCount - 完了したポモドーロ数
     * @returns {string} 次のモード
     */
    getNextMode(currentMode, completedCount) {
        if (currentMode !== 'pomodoro') {
            return 'pomodoro';
        }
        return completedCount % 4 === 0 ? 'longBreak' : 'shortBreak';
    },

    /**
     * モードの表示名を取得
     * @param {string} mode - モード
     * @returns {string} 表示名
     */
    getModeLabel(mode) {
        const labels = {
            'pomodoro': '作業中',
            'shortBreak': '短い休憩',
            'longBreak': '長い休憩'
        };
        return labels[mode] || '作業中';
    },

    /**
     * モードに応じたデフォルトの時間（秒）を取得
     * @param {string} mode - モード
     * @param {object} settings - 設定オブジェクト
     * @returns {number} 時間（秒）
     */
    getDuration(mode, settings) {
        const durations = {
            'pomodoro': (settings.pomodoro || 25) * 60,
            'shortBreak': (settings.shortBreak || 5) * 60,
            'longBreak': (settings.longBreak || 15) * 60
        };
        return durations[mode] || 1500;
    },

    /**
     * 合計集中時間をフォーマット
     * @param {number} totalMinutes - 合計分数
     * @returns {string} フォーマットされた時間
     */
    formatTotalTime(totalMinutes) {
        const hours = Math.floor(totalMinutes / 60);
        const mins = totalMinutes % 60;
        
        if (hours === 0) {
            return `${mins}分`;
        }
        return `${hours}時間${mins}分`;
    }
};

// モジュールとして利用できない環境のためグローバルにも公開
if (typeof window !== 'undefined') {
    window.TimerEngine = TimerEngine;
}

// ES6モジュールとしてエクスポート（テスト用）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TimerEngine;
}
