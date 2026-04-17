# ポモドーロタイマー Webアプリケーション アーキテクチャ案

## ディレクトリ構成

```
プロジェクトルート/
│
├── app.py                  # Flask アプリケーション（ルーティングのみ）
├── timer_service.py        # ビジネスロジック（テスト可能な純粋関数）
├── models.py               # データモデル・SessionRepository
│
├── static/
│   ├── css/
│   │   └── style.css       # UIスタイル（紫系カラーテーマ、角丸ボタン等）
│   └── js/
│       └── timer.js        # タイマーロジック・UI制御
│
├── templates/
│   └── index.html          # メインページ（SVG円形プログレス含む）
│
├── sessions.json           # セッションデータの永続化ファイル
│
└── tests/
    ├── conftest.py         # pytest フィクスチャ定義
    ├── test_timer_service.py
    └── test_api.py
```

---

## 技術スタック

| レイヤー | 技術 |
|---|---|
| サーバーサイド | Python / Flask |
| フロントエンド | HTML / CSS / JavaScript（フレームワークなし） |
| データ永続化 | sessions.json（または SQLite） |
| テスト | pytest |

---

## レイヤー別の責務

### Flask（`app.py`）
- `create_app()` ファクトリパターンを採用し、テスト時に設定を差し替え可能にする
- ルーティングのみを記述し、ビジネスロジックは持たない

| エンドポイント | メソッド | 役割 |
|---|---|---|
| `/` | GET | `index.html` を返す |
| `/api/sessions` | GET | 今日の完了セッション一覧を返す |
| `/api/sessions` | POST | 完了セッションを保存する |

```python
# app.py の基本構造
def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.update(config)
    register_routes(app)
    return app
```

---

### ビジネスロジック（`timer_service.py`）
- Flaskに依存しない純粋な関数として実装する
- 日付・時刻は引数で受け取り、`datetime.now()` を関数内で直接呼ばない

```python
def get_today_sessions(sessions: list[dict], today: str) -> list[dict]:
    return [s for s in sessions if s["date"] == today]

def calculate_total_focus_minutes(sessions: list[dict]) -> int:
    return sum(s["duration_minutes"] for s in sessions)
```

---

### データモデル（`models.py`）
- `SessionRepository` クラスでファイルI/Oを抽象化する
- テスト時はコンストラクタ引数でファイルパスを差し替え可能にする

```python
class SessionRepository:
    def __init__(self, filepath: str = "sessions.json"):
        self.filepath = filepath

    def find_by_date(self, date: str) -> list[dict]: ...
    def save(self, session: dict) -> None: ...
```

セッション1件のデータ構造：
```json
{
  "id": 1,
  "date": "2026-04-17",
  "completed_at": "14:30:00",
  "duration_minutes": 25
}
```

---

### JavaScript（`static/js/timer.js`）
- タイマーのカウントダウンは `setInterval` でフロントエンド完結で実装する
- SVG の `stroke-dashoffset` アニメーションで円形プログレスを描画する
- セッション完了時に `/api/sessions` へ POST して進捗を保存・表示に反映する
- `localStorage` でページリロード後の状態復元（任意）

---

### CSS（`static/css/style.css`）
- フレームワーク不使用の Pure CSS で実装する
- カラーテーマ：紫系（`#6C63FF` 系統）
- 角丸ボタン、カード型の進捗パネルを再現する

---

## タイマーの状態遷移

```
[作業中 25:00] --タイムアップ--> [休憩中 5:00] --タイムアップ--> [作業中 25:00]
      |                                |
   開始/一時停止                    開始/一時停止
      |                                |
   リセット                          リセット
```

---

## テスト戦略

| 優先度 | 改善項目 | 効果 |
|---|---|---|
| 高 | ビジネスロジックを `timer_service.py` に分離 | Flaskなしで単体テストが書ける |
| 高 | `create_app()` ファクトリパターン | テスト用設定を差し替え可能 |
| 中 | `SessionRepository` で永続化を抽象化 | ファイルI/Oをモックせずにテスト可能 |
| 低 | 日時を引数で注入 | 日付依存のテストが安定する |

```python
# conftest.py
@pytest.fixture
def client():
    app = create_app({"TESTING": True, "DATA_FILE": "test_sessions.json"})
    with app.test_client() as client:
        yield client
```

---

## 実装順序

1. `app.py` — `create_app()` とルーティング骨格
2. `models.py` — `SessionRepository`
3. `timer_service.py` — ビジネスロジック関数
4. `templates/index.html` — UI骨格（SVG円形プログレス含む）
5. `static/css/style.css` — 紫系テーマのスタイリング
6. `static/js/timer.js` — タイマーロジックとAPI連携
7. `tests/` — 各層のユニットテスト
