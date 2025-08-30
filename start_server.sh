#!/bin/bash

# ポモドーロタイマーサーバー起動スクリプト

# 色の定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🍅 ポモドーロタイマーサーバー起動スクリプト${NC}"
echo "================================="

# 作業ディレクトリに移動
cd /workspaces/2025-Github-Copilot-Workshop-Python

# 既存のプロセスを確認・停止
echo -e "${YELLOW}既存のサーバープロセスを確認中...${NC}"
if pgrep -f "python.*app.py" > /dev/null; then
    echo -e "${YELLOW}既存のサーバーを停止中...${NC}"
    pkill -f "python.*app.py"
    sleep 2
fi

# 仮想環境の確認
if [ ! -d ".venv" ]; then
    echo -e "${RED}エラー: 仮想環境が見つかりません${NC}"
    exit 1
fi

# サーバー起動
echo -e "${GREEN}サーバーを起動中...${NC}"
echo ""
echo -e "${GREEN}アクセスURL:${NC}"
echo "- ローカル: http://127.0.0.1:8000"
echo "- ネットワーク: http://10.0.3.246:8000"
echo ""
echo -e "${YELLOW}サーバーを停止するには Ctrl+C を押してください${NC}"
echo "================================="

# サーバー起動
.venv/bin/python app.py
