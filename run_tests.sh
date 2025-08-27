#!/bin/bash

# ポモドーロタイマーアプリケーション テスト実行スクリプト

echo "=== ポモドーロタイマー ユニットテスト ==="
echo "Python環境: $(python --version)"
echo "pytest バージョン: $(pytest --version)"
echo ""

echo "=== 全テスト実行 ==="
python -m pytest tests/ -v

echo ""
echo "=== カバレッジレポート ==="
python -m pytest tests/ --cov=app --cov-report=term-missing --cov-report=html

echo ""
echo "=== テスト実行完了 ==="
echo "HTMLカバレッジレポートが htmlcov/index.html に生成されました"
