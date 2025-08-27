#!/bin/bash

# ポモドーロタイマーサーバー管理スクリプト

APP_NAME="ポモドーロタイマー"
APP_DIR="/workspaces/2025-Github-Copilot-Workshop-Python"
PID_FILE="$APP_DIR/server.pid"
LOG_FILE="$APP_DIR/server.log"

# 色の定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# 使用方法を表示
usage() {
    echo -e "${BLUE}使用方法:${NC}"
    echo "  $0 {start|stop|restart|status|logs}"
    echo ""
    echo -e "${BLUE}コマンド:${NC}"
    echo "  start   - サーバーを開始"
    echo "  stop    - サーバーを停止"
    echo "  restart - サーバーを再起動"
    echo "  status  - サーバーの状態を確認"
    echo "  logs    - サーバーログを表示"
}

# サーバー開始
start_server() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo -e "${YELLOW}$APP_NAME は既に動作中です (PID: $(cat $PID_FILE))${NC}"
        return 1
    fi
    
    echo -e "${GREEN}$APP_NAME を開始中...${NC}"
    cd "$APP_DIR"
    
    # バックグラウンドでサーバーを起動
    nohup .venv/bin/python app.py > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    
    sleep 2
    
    if kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo -e "${GREEN}✅ $APP_NAME が正常に開始されました (PID: $(cat $PID_FILE))${NC}"
        echo ""
        echo -e "${GREEN}🌐 アクセスURL:${NC}"
        echo "  • ローカル: http://127.0.0.1:8000"
        echo "  • ネットワーク: http://10.0.3.246:8000"
    else
        echo -e "${RED}❌ $APP_NAME の開始に失敗しました${NC}"
        rm -f "$PID_FILE"
        return 1
    fi
}

# サーバー停止
stop_server() {
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${YELLOW}$APP_NAME は動作していません${NC}"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo -e "${YELLOW}$APP_NAME を停止中... (PID: $PID)${NC}"
        kill "$PID"
        sleep 2
        
        if kill -0 "$PID" 2>/dev/null; then
            echo -e "${RED}強制停止中...${NC}"
            kill -9 "$PID"
        fi
        
        echo -e "${GREEN}✅ $APP_NAME が停止されました${NC}"
    else
        echo -e "${YELLOW}プロセス $PID は見つかりません${NC}"
    fi
    
    rm -f "$PID_FILE"
}

# サーバー状態確認
check_status() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        PID=$(cat "$PID_FILE")
        echo -e "${GREEN}✅ $APP_NAME は動作中です (PID: $PID)${NC}"
        echo ""
        echo -e "${BLUE}アクセスURL:${NC}"
        echo "  • ローカル: http://127.0.0.1:8000"
        echo "  • ネットワーク: http://10.0.3.246:8000"
        return 0
    else
        echo -e "${RED}❌ $APP_NAME は停止中です${NC}"
        [ -f "$PID_FILE" ] && rm -f "$PID_FILE"
        return 1
    fi
}

# ログ表示
show_logs() {
    if [ -f "$LOG_FILE" ]; then
        echo -e "${BLUE}$APP_NAME ログ (最新20行):${NC}"
        echo "================================="
        tail -20 "$LOG_FILE"
    else
        echo -e "${YELLOW}ログファイルが見つかりません${NC}"
    fi
}

# メイン処理
case "$1" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        stop_server
        sleep 1
        start_server
        ;;
    status)
        check_status
        ;;
    logs)
        show_logs
        ;;
    *)
        usage
        exit 1
        ;;
esac
