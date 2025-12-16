# フロントエンドとAPIの連携 (Step 4)

## 概要
このステップでは、フロントエンドとバックエンドAPIを連携させ、進捗データの取得・保存、作業完了時の更新、通信エラーハンドリングを実装しました。

## 実装内容

### 1. バックエンドAPI (main.py)
Flask RESTful APIを使用して以下のエンドポイントを実装:

#### エンドポイント一覧:
- `GET /` - フロントエンドHTMLページを提供
- `GET /api/progress` - 現在の進捗データを取得
- `GET /api/recipes` - 待機中のレシピリストを取得
- `POST /api/deliver` - レシピを配達 (材料をJSON形式で送信)
- `POST /api/start` - ゲームを開始
- `POST /api/stop` - ゲームを停止

#### 主な機能:
- バックグラウンドスレッドでゲームロジックを継続的に更新
- CORS対応 (フロントエンドとの通信を許可)
- エラーハンドリング (try-catchブロックで全エンドポイントを保護)
- JSON形式での統一されたレスポンス構造

### 2. フロントエンド (index.html)
モダンなUIを持つシングルページアプリケーション:

#### 主な機能:
- **リアルタイム進捗表示**: 成功したレシピ数と待機中のレシピ数
- **レシピリスト表示**: 待機中のレシピとその材料を視覚的に表示
- **レシピ配達**: 材料選択と配達機能
- **ゲームコントロール**: 開始/停止/データ更新
- **自動更新**: 3秒ごとに進捗データを自動取得
- **エラーハンドリング**: 
  - 通信エラーの検知と表示
  - HTTPステータスコードのチェック
  - ユーザーフレンドリーなエラーメッセージ
  - 成功メッセージの表示

### 3. エラーハンドリング
以下の種類のエラーに対応:

- **ネットワークエラー**: fetch APIの例外キャッチ
- **HTTPエラー**: ステータスコードのチェック
- **アプリケーションエラー**: サーバーからのエラーレスポンス処理
- **データ検証**: 不正なデータ入力時のエラー

## 使用方法

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. サーバーの起動
```bash
python3 main.py
```

### 3. フロントエンドへのアクセス
ブラウザで以下のURLを開く:
```
http://localhost:5000/
```

### 4. テストの実行
```bash
python3 -m unittest test_api.py -v
```

## API使用例

### 進捗データの取得
```bash
curl http://localhost:5000/api/progress
```

レスポンス:
```json
{
  "success": true,
  "data": {
    "successful_recipes": 5,
    "waiting_recipes_count": 3
  }
}
```

### レシピの配達
```bash
curl -X POST http://localhost:5000/api/deliver \
  -H "Content-Type: application/json" \
  -d '{"ingredients": ["Bread", "Lettuce", "Tomato"]}'
```

レスポンス:
```json
{
  "success": true,
  "data": {
    "delivered": true,
    "successful_recipes": 6
  }
}
```

### エラー例
```bash
curl -X POST http://localhost:5000/api/deliver \
  -H "Content-Type: application/json" \
  -d '{"ingredients": ["Unknown"]}'
```

レスポンス:
```json
{
  "success": false,
  "error": "Unknown ingredient: Unknown"
}
```

## 技術スタック

- **バックエンド**: Flask 3.0.0, Flask-CORS 4.0.0
- **フロントエンド**: HTML5, CSS3, JavaScript (Vanilla JS)
- **API通信**: Fetch API
- **テスト**: Python unittest

## セキュリティ考慮事項

- CORSを適切に設定
- 入力データの検証
- エラーメッセージに機密情報を含めない
- 本番環境ではFlaskのdebugモードを無効化すること

## 今後の改善点

- 認証・認可の実装
- WebSocketによるリアルタイム通信
- より詳細なエラーログ
- パフォーマンスの最適化
- E2Eテストの追加
