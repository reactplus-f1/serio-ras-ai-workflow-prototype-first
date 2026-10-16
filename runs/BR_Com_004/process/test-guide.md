# Hướng dẫn test BR_Com_004 (会議室タブレット登録) trên môi trường local

Cách khởi động DB / Backend / Frontend dùng chung cho cả project: xem **`serio-ras/README.md` – mục "Chạy môi trường local"**. File này chỉ ghi phần riêng của BR_Com_004: dữ liệu mẫu, kịch bản test, SQL và API kiểm tra.

## 1. Chuẩn bị

1. Khởi động DB, BE, FE theo `serio-ras/README.md`. Trước mỗi lượt test nên **reset dữ liệu** (README – mục ① "Reset dữ liệu").
2. Mở **http://localhost:4200/BRCom004**, đăng nhập Entra ID bằng tài khoản có app role **`Administrator`** (R-001/R-025); tài khoản không có role dùng cho kịch bản #1.
3. Swagger https://localhost:5101/swagger phải có: `GET /private/tablet-info/{roomId}` (API_004), `POST /private/tablet-info` (API_005), `POST /private/rooms-mst-list` (API_008).

Dữ liệu mẫu (từ `ras-system/sql/ras_tables.sql`):

| Bảng | Dữ liệu |
|---|---|
| rooms_mst | `aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1` A会議室, `…aaa2` B会議室, `…aaa3` C会議室 |
| tablets_mst | `dddddddd-dddd-dddd-dddd-ddddddddddd1` (A会議室, `TAB-A-001`), `…ddd2` (B会議室, `TAB-B-001`) |
| candidate_rooms_mst | ddd1 → B, C; ddd2 → A |

Thêm phòng để test (chạy trong psql – README mục ①):

```sql
INSERT INTO rooms_mst (id, room_name, location, email_address, create_user_email_address, update_user_email_address)
VALUES (gen_random_uuid(), 'D会議室', '東京本社 6F', 'room-d@example.co.jp', 'system@local', 'system@local');
```

## 2. Kịch bản test màn hình

| # | Thao tác | Kỳ vọng | Rule |
|---|---|---|---|
| 1 | Vào `/BRCom004` bằng tài khoản **không** phải Administrator | Chuyển sang `/error/403` (mock BR_Com_005) | R-001, R-025 |
| 2 | Vào bằng tài khoản Administrator | Dropdown 設置会議室 = 未選択, danh sách có A/B/C会議室; タブレット端末ID bị disable (xám); 延長候補会議室 chỉ đọc; nút 登録 và icon 検索 **ẩn** | R-002…R-005 |
| 3 | Chọn A会議室 | タブレット端末ID = `TAB-A-001` (nhập được); 延長候補会議室 = `B会議室;C会議室`; hiện nút 登録 và icon 検索 (kính lúp) | R-006…R-009 |
| 4 | Chọn C会議室 (chưa có tablet) | ID trống, 延長候補 trống, control enable | R-006, D-6 |
| 5 | Bấm 検索 | Mở modal mock BR_Com_003, phòng đang chọn ở 設置会議室 không xuất hiện trong danh sách; chọn nhiều → OK → text join bằng `;`; Cancel giữ nguyên | R-011…R-013 |
| 6 | C会議室, nhập ID `TAB-C-001`, chọn 延長候補 A,B → 登録 | Hộp confirm (warning) → OK → thông báo success; DB có dòng mới tablets_mst + 2 dòng candidate_rooms_mst | R-014, R-017, R-019, R-021, R-024 |
| 7 | Chọn A会議室, nhập ID `TAB-B-001` (đang thuộc B) → 登録 → OK | 422, message `タブレット端末ID：他の会議室に登録されています。（会議室名：B会議室）`, không thay đổi DB | R-015, R-016 |
| 8 | A会議室, đổi ID thành `TAB-A-002`, bỏ C khỏi 延長候補 → 登録 → OK | UPDATE tablets_mst (machine_id mới); candidate chỉ còn B | R-018, R-020, R-021, D-1 |
| 9 | A会議室, xóa trống ID, 延長候補 trống → 登録 → OK | Thành công; machine_id NULL; candidate_rooms_mst của ddd1 = 0 dòng | A-02/A-03, A-05 |
| 10 | Confirm → Cancel | Không gọi API, màn giữ nguyên | R-014 |
| 11 | Tắt backend rồi 登録 | Chuyển `/error/504` hoặc `/error/0` tùy interceptor (mock BR_Com_005) | D-8 |

### SQL kiểm tra sau mỗi bước (chạy trong psql)

```sql
SELECT t.id, r.room_name, t.machine_id, t.update_at
FROM tablets_mst t JOIN rooms_mst r ON r.id = t.room_id ORDER BY r.room_name;

SELECT t.machine_id, r.room_name AS candidate, c.create_at
FROM candidate_rooms_mst c
JOIN tablets_mst t ON t.id = c.tablet_id
JOIN rooms_mst r ON r.id = c.room_id ORDER BY t.machine_id, r.room_name;
```

## 3. Test API trực tiếp (không qua FE)

Cần access token của tài khoản Administrator (lấy từ DevTools tab Network của FE, header `Authorization: Bearer …`, hoặc `az account get-access-token --scope api://368cd8cd-aa07-4da1-8618-42162760a9b4/user_impersonation`).

```powershell
$tok = "<access token>"
$h = @{ Authorization = "Bearer $tok" }

# API_008 danh sách phòng (POST, body rỗng)
Invoke-RestMethod -Method Post -Uri https://localhost:5101/private/rooms-mst-list -Headers $h -ContentType "application/json" -Body "{}"

# API_004 thông tin tablet theo phòng
Invoke-RestMethod -Uri "https://localhost:5101/private/tablet-info/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1" -Headers $h

# API_005 đăng ký
$body = @{ roomId = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa3"; machineId = "TAB-C-001";
           candidateRoomIds = @("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1") } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri https://localhost:5101/private/tablet-info -Headers $h -ContentType "application/json" -Body $body
```

Kỳ vọng mã lỗi: `roomId` thiếu/sai GUID hoặc phần tử `candidateRoomIds` sai GUID → 400 (validation); không có token → 401; token không có role Administrator → 403; machine_id trùng phòng khác → 422 với `E_BRCOM004_001`.

Chi tiết endpoint xem `RasApi\Controllers\TabletInfoController.cs` (`private/tablet-info`), `RoomsController.cs` (`private/rooms-mst-list`) và `pg-implementation.md`.


## 4. Sự cố riêng BR_Com_004

| Hiện tượng | Xử lý |
|---|---|
| Đăng nhập xong vẫn `/error/403` | Tài khoản chưa có app role `Administrator` trên Entra app `368cd8cd-…` |
| 422 nhưng message hiển thị key thô | Thiếu `E_BRCOM004_001` trong `Messages.resx` (đã thêm ở S2) hoặc BE chưa chạy lại sau khi build |