# BR_Com_004 会議室タブレット登録：ローカルデモ・テスト手順

DB、バックエンド、フロントエンドの構築・起動方法は `serio-ras/README.md` を参照してください。この文書は BR_Com_004 固有のサンプルデータ、画面操作、DB・API 確認を扱います。`serio-ras/docs/BR_Com_004_DEMO.md` は顧客向けの画面デモガイドです。

## 1. 準備

1. `serio-ras/README.md` に従い、PostgreSQL、RasApi、ras-web を起動します。毎回の SQL 再実行は不要です。初期データからテストする場合に限り、**デモ用 DB** に `ras_tables.sql` を再投入します。この SQL は対象テーブルを DROP して再作成します。
2. `Administrator` ロールを持つアカウントで `http://localhost:4200/BRCom004` を開きます。権限エラーの確認には、同ロールを持たない別アカウントが必要です。
3. `https://localhost:5101/swagger` で API_004 `GET /private/tablet-info/{roomId}`、API_005 `POST /private/tablet-info`、API_008 `POST /private/rooms-mst-list` を確認します。

`ras-system/sql/ras_tables.sql` の主な初期データ：

| テーブル | サンプルデータ |
|---|---|
| `rooms_mst` | `aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1` = A会議室、`…aaa2` = B会議室、`…aaa3` = C会議室 |
| `tablets_mst` | A会議室 = `TAB-A-001`（ID `dddddddd-dddd-dddd-dddd-ddddddddddd1`）、B会議室 = `TAB-B-001`（`…ddd2`） |
| `candidate_rooms_mst` | A のタブレット → B/C、B のタブレット → A |

A/B/C は検証用に作成した会議室名であり、画面に固定された値ではありません。

## 2. 画面テスト

| No. | 操作 | 期待結果 | 関連ルール |
|---|---|---|---|
| 1 | `Administrator` 以外のアカウントで `/BRCom004` を開く | `/error/403` に遷移する。BR_Com_005 はモック。 | R-001, R-025 |
| 2 | 管理者で開く | 設置会議室の初期値は「未選択」。API_008 の A/B/C が名前順で表示され、端末IDは入力不可、延長候補は読み取り専用、登録ボタンと検索アイコンは非表示。 | R-002–R-005 |
| 3 | A会議室を選択 | 端末IDは `TAB-A-001`、延長候補の表示は `B会議室;C会議室`。登録ボタンと検索アイコンが表示される。 | R-006–R-009 |
| 4 | C会議室を選択 | タブレット未登録のため端末IDと延長候補は空欄。端末IDは入力可能。 | R-006, D-6 |
| 5 | A会議室で検索アイコンを押し、C のチェックを外して OK | BR_Com_003 のモックが開く。選択肢は A/B/C **すべて**（現在の設置会議室も除外しない）。親画面の表示は B のみになり、DB はまだ変更されない。モックのキャンセルは親画面の値を維持する。 | R-011–R-013 |
| 6 | 確認ダイアログで Cancel | API_005 を呼ばず、DB は変更されない。画面上の入力は残る。 | R-014 |
| 7 | A会議室の端末IDに B の `TAB-B-001` を入力し、登録 → OK | HTTP 422。B会議室に登録済みである旨をタイトル下に表示し、DB は変更されない。 | R-015, R-016 |
| 8 | A会議室の端末IDを `TAB-A-002`、候補を B のみにして登録 → OK | 成功。`tablets_mst` の端末IDを更新し、候補 C を削除、B を維持する。画面は保存後に再取得する。 | R-018–R-021, R-024, D-1 |
| 9 | C会議室で `TAB-C-001` と候補 A/B を登録 → OK | 成功。`tablets_mst` に新規1件、`candidate_rooms_mst` に候補2件を登録する。 | R-017–R-021, R-024 |
| 10 | C会議室の端末IDと候補を空欄にして登録 → OK | 成功。端末IDは `NULL`、C の候補は0件になる。 | A-02, A-03, A-05 |

モック内の **OK は画面内の候補を一時変更するだけ**です。DB に保存するには親画面右上の**登録**を押し、確認ダイアログでも **OK** を押します。ブラウザー再読み込み後は設置会議室が「未選択」に戻るため、保存結果を見るには会議室を再選択してください。

### DB 確認 SQL

```sql
SELECT t.id, r.room_name, t.machine_id, t.update_at
FROM tablets_mst t JOIN rooms_mst r ON r.id = t.room_id
ORDER BY r.room_name;

SELECT t.machine_id, r.room_name AS candidate, c.create_at
FROM candidate_rooms_mst c
JOIN tablets_mst t ON t.id = c.tablet_id
JOIN rooms_mst r ON r.id = c.room_id
ORDER BY t.machine_id, r.room_name;
```

## 3. API 単体確認（任意）

`Administrator` アカウントのアクセストークンを取得してから実行します。トークンを文書やログに記録しないでください。以下は PowerShell の例です。

```powershell
$token = '<Administrator のアクセストークン>'
$headers = @{ Authorization = "Bearer $token" }

# API_008: 会議室マスタ一覧（BR_Com_004 からの検索条件は空）
Invoke-RestMethod -Method Post -Uri https://localhost:5101/private/rooms-mst-list -Headers $headers -ContentType 'application/json' -Body '{}'

# API_004: A会議室のタブレット情報
Invoke-RestMethod -Uri 'https://localhost:5101/private/tablet-info/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1' -Headers $headers

# API_005: C会議室の登録例
$body = @{ roomId = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa3'; machineId = 'TAB-C-001'; candidateRoomIds = @('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1') } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri https://localhost:5101/private/tablet-info -Headers $headers -ContentType 'application/json' -Body $body
```

期待する HTTP ステータス：`roomId` の欠落・GUID 形式エラーや `candidateRoomIds` 内の形式エラーは 400、未認証は 401、必要なロールがない場合は 403、他会議室の端末IDとの重複は 422 です。API_004/005 は `Administrator`、API_008 は `InternalUser` または `Administrator` を要求します。

## 4. トラブルシューティング

| 症状 | 確認すること |
|---|---|
| サインイン後に `/error/403` | Entra ID のアプリロール `Administrator` が対象アカウントに付与されているか。 |
| 会議室一覧が空 | DB に `rooms_mst` のサンプルデータがあり、API_008 が成功しているか。 |
| 422 の文言がメッセージキーのまま | RasApi の `Messages.resx` に `E_BRCOM004_001` があり、修正後に再起動したか。 |
| 検索モックの OK 後に再読み込みすると選択が消える | 親画面の登録 → 確認 OK まで行ったか。 |
