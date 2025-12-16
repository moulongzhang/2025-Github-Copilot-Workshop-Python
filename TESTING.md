# テスト実行ガイド

## Python テスト

### テスト環境のセットアップ

```bash
# 依存パッケージのインストール
pip install -r requirements.txt
```

### テストの実行

```bash
# すべてのテストを実行
pytest

# 特定のテストファイルを実行
pytest tests/integration/test_app.py

# 詳細な出力で実行
pytest -v

# カバレッジレポート付きで実行
pytest --cov=. --cov-report=html
```

### テストカバレッジの確認

```bash
# HTMLレポートを開く
open htmlcov/index.html
```

## JavaScript テスト

### テスト環境のセットアップ

```bash
# Node.jsの依存パッケージをインストール
npm install
```

### テストの実行

```bash
# すべてのテストを実行
npm test

# ウォッチモードで実行
npm run test:watch

# カバレッジレポート付きで実行
npm run test:coverage
```

## 現在のテストカバレッジ

### Python (統合テスト)
- **カバレッジ**: 98%
- **テスト数**: 15個
- **テスト内容**:
  - Flaskアプリケーションの基本動作
  - ルーティングの正常性
  - HTMLコンテンツの検証
  - 静的ファイルの配信
  - CSSとJavaScriptファイルの存在確認

### JavaScript (ユニットテスト)
- **テスト内容**:
  - PomodoroTimerクラスのコンストラクタ
  - タイマーの開始/停止/リセット機能
  - 時間フォーマット機能
  - DOM更新機能
  - タイマー完了時の動作

## テストの構成

```
tests/
├── conftest.py                 # pytest共通設定
├── integration/
│   └── test_app.py            # Flaskアプリの統合テスト
└── frontend/
    └── timer.test.js          # JavaScriptのユニットテスト
```

## CI/CDでのテスト実行

GitHub Actionsなどでの自動テスト実行例:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```
