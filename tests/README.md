# テストスイート

このディレクトリにはKitchen Gameプロジェクトのユニットテストが含まれています。

## テストの実行

### すべてのテストを実行

```bash
python3 -m unittest discover tests -v
```

### 特定のテストファイルを実行

```bash
python3 -m unittest tests.test_point -v
python3 -m unittest tests.test_delivery_manager -v
```

### 特定のテストクラスを実行

```bash
python3 -m unittest tests.test_point.TestPoint2D -v
python3 -m unittest tests.test_delivery_manager.TestDeliveryManager -v
```

### 特定のテストメソッドを実行

```bash
python3 -m unittest tests.test_point.TestPoint2D.test_distance_to_diagonal -v
```

## テストカバレッジ

### Point2D (test_point.py)
- 初期化と基本機能
- 距離計算（水平、垂直、対角線）
- 負の座標の処理
- 文字列表現

### DeliveryManager関連 (test_delivery_manager.py)
- **Event**: ハンドラーの追加・削除、イベント発火
- **KitchenObjectSO**: オブジェクト作成、等価性
- **RecipeSO**: レシピ作成
- **PlateKitchenObject**: 材料の追加、リスト取得
- **KitchenGameManager**: シングルトンパターン、ゲーム状態管理
- **DeliveryManager**: レシピ生成、配達検証、イベント管理

## テスト構造

```
tests/
├── __init__.py              # テストパッケージ初期化
├── test_point.py            # Point2Dクラスのテスト
└── test_delivery_manager.py # DeliveryManager関連のテスト
```

## テスト作成のガイドライン

1. **命名規則**: テストメソッドは`test_`で始める
2. **ドキュメント**: 各テストに日本語の説明を追加
3. **セットアップ**: 必要に応じて`setUp`メソッドでシングルトンをリセット
4. **アサーション**: 適切なアサーションメソッドを使用
   - `assertEqual`: 値の等価性
   - `assertTrue`/`assertFalse`: 真偽値
   - `assertRaises`: 例外発生の確認
   - `assertIsNot`: インスタンスの非同一性

## 継続的改善

テストは継続的にメンテナンスされるべきです：
- 新機能追加時は対応するテストも追加
- バグ修正時は再現テストを追加
- リファクタリング後はテストが通ることを確認
