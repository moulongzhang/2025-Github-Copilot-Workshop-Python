# ポモドーロタイマー 段階的実装計画

## Phase 1：動くFlask土台を作る
**目標：ブラウザで画面が開けること**

- [ ] `app.py` — `create_app()` + `GET /` ルート
- [ ] `models.py` — `SessionRepository`（`save` / `find_by_date`）
- [ ] `timer_service.py` — `get_today_sessions` / `calculate_total_focus_minutes`
- [ ] `app.py` — `GET /api/sessions` + `POST /api/sessions` ルート
- [ ] `templates/index.html` — HTMLの骨格のみ（スタイルなし）

完了の確認：`flask run` でAPIが動作すること

---

## Phase 2：UIの見た目を作る
**目標：モック画像に近い静的な見た目になること**

- [ ] `templates/index.html` — SVG円形プログレス・ボタン・進捗パネルのマークアップ追加
- [ ] `static/css/style.css` — 紫系カラーテーマ・角丸ボタン・カードパネル・フォント

完了の確認：静的な状態でモックと外見が一致すること

---

## Phase 3：タイマーのコア動作を実装する
**目標：カウントダウンが動き、ボタン操作が機能すること**

- [ ] `static/js/timer.js` — カウントダウン（`setInterval`）
- [ ] `static/js/timer.js` — 開始／一時停止のトグル
- [ ] `static/js/timer.js` — リセット処理
- [ ] `static/js/timer.js` — 円形プログレスの `stroke-dashoffset` 更新
- [ ] `static/js/timer.js` — 時間テキスト（`MM:SS`）・ページタイトルの更新

完了の確認：タイマーが正確に動作し、プログレスリングが連動すること

---

## Phase 4：フェーズ遷移と進捗保存を実装する
**目標：セッションが完了してデータが記録されること**

- [ ] `static/js/timer.js` — 作業→休憩→作業のフェーズ自動切替
- [ ] `static/js/timer.js` — フェーズラベル「作業中」「休憩中」の切り替え
- [ ] `static/js/timer.js` — セッション完了時に `POST /api/sessions` を呼び出す
- [ ] `static/js/timer.js` — 画面ロード時に `GET /api/sessions` で進捗パネルを初期化
- [ ] `static/js/timer.js` — セッション完了後に進捗パネルをリアルタイム更新

完了の確認：25分後にセッションが保存され、進捗パネルに反映されること

---

## Phase 5：通知・品質向上
**目標：ユーザー体験を完成させること**

- [ ] タイムアップ時のブラウザ通知（Notification API）または音声アラート
- [ ] レスポンシブレイアウトの調整
- [ ] `static/js/timer.js` — `localStorage` によるリロード後の状態復元（任意）

---

## Phase 6：テストを書く
**目標：主要ロジックの動作を自動検証できること**

- [ ] `tests/conftest.py` — pytestフィクスチャ（`client`・`tmp_path` ベースのリポジトリ）
- [ ] `tests/test_timer_service.py` — `get_today_sessions` / `calculate_total_focus_minutes`
- [ ] `tests/test_api.py` — `GET /api/sessions` / `POST /api/sessions` のエンドポイントテスト

---

## まとめ

```
Phase 1 → Flask + API + モデルの骨格          （バックエンド基盤）
Phase 2 → HTML + CSS で見た目を完成           （フロントエンド基盤）
Phase 3 → タイマーのコア動作                  （最重要機能）
Phase 4 → フェーズ遷移 + データ保存・表示     （機能完成）
Phase 5 → 通知・レスポンシブ・状態復元        （品質向上）
Phase 6 → ユニットテスト                      （品質保証）
```
