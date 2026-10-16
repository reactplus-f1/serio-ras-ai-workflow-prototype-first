# Phạm vi và quy tắc PoC BR_Com_004

Bản tra nhanh tổng hợp từ BD `【RAS】(BR_Com_004)会議室タブレット登録_画面定義書.xlsx`
(viết tắt BD004), BD003/BD005 cho mock contract, `【RAS】API一覧.xlsx`,
`【RAS】テーブル設計書.xlsx` và kickoff 2026-10-08. **Khi lập baseline task, đối chiếu đúng
file/version user đưa**; bản này không là xác nhận G0/G1 và không thay Rule IDs của run.

## Scope

Chức năng chính: BR_Com_004 会議室タブレット登録 — quản trị viên liên kết tablet với phòng cài
đặt và chọn phòng gia hạn. BR_Com_003 会議室検索 và BR_Com_005 一括予約エラー表示 gọi dưới dạng
mock. BR_Com_002 社内ユーザ検索 chỉ tham khảo. Auth/DB/API thật hay mock phải ghi scope riêng
trong task; không suy toàn bộ backend là mock.

Căn cứ: kickoff slide 6/15; BD004/機能概要!D7:D17.

## Hành vi bắt buộc từ BD

| Event / mục | Quy định | Nguồn BD004 |
|---|---|---|
| Khởi tạo | Kiểm tra quyền; lấy danh sách phòng cho dropdown | イベント定義!F6:F7 |
| Chưa chọn phòng | Default 未選択; ẩn nút đăng ký/search icon; tablet ID không nhập được | 項目定義!M7,J8,N9,M11 |
| Chọn phòng | Lấy tablet và extension candidates theo phòng; không có thì clear | イベント定義!D9:F10 |
| Search candidates | Gọi child search, hiển thị phòng đã chọn; tên phòng cách nhau `;` | イベント定義!D12:F13; 項目定義!I10 |
| Thiếu quyền | Chuyển error screen 403 | エラーチェック一覧!F7:H7 |
| Confirmation | 入力情報を登録します。よろしいですか？ | エラーチェック一覧!G8 |
| Duplicate machine ID | ID tồn tại ở phòng khác → lỗi kèm tên phòng | エラーチェック一覧!F9:H9 |
| Insert/update tablet | Chưa có tablet master của phòng → insert UUID mới; có → update | イベント定義!F16:F17; データアクセス定義!E48:E50,D67:D69 |
| Candidate links | Xóa links cũ theo tablet ID rồi insert selected | イベント定義!F18:F19; データアクセス定義!D57:F58,D77 |
| Thành công | タブレット情報を登録しました。 | イベント定義!F20:F21 |

Data access giữ IDs SELECT_001, SELECT_002, INSERT_001, INSERT_002, UPDATE_001, DELETE_001.
SELECT_001 lấy rooms sort tên tăng dần; SELECT_002 lấy tablet/candidate/room với outer join
theo tablet ID và candidate room ID, filter phòng cài đặt đã chọn. Không đổi sang inner join.
Căn cứ: データアクセス定義!E9:D39, E43:D77.

## API và schema

API_004 `GET /private/tablet-info/{roomId}`; API_005 `POST /private/tablet-info`;
API_008 `POST /private/rooms-mst-list`. Mapping theo API一覧!B12:K16 và contract chung.

| API | 社内ユーザ | システム管理者 | Nguồn |
|---|---|---|---|
| API_004 | Không | Có | API一覧!G12:H12 |
| API_005 | Không | Có | API一覧!G13:H13 |
| API_008 | Có | Có | API一覧!G16:H16 |

Vai trò tại API一覧!G6:H6; mỗi endpoint có role riêng (ルール!D22:D23). API_008 dùng chung
nên không áp admin-only lên toàn API. Người dùng màn là システム管理者 (機能概要!D11); thiếu
quyền → 403 (エラーチェック一覧!F7:H7). Quyền màn không thay bảo vệ API; quyền API và
credential DB là hai việc riêng. Đối chiếu tên vai trò nghiệp vụ với giá trị role trong
token trên source thật; cần evidence trước khi kết luận test phân quyền PASS.

Tables: rooms_mst, tablets_mst, candidate_rooms_mst. ID/room_id/tablet_id UUID; machine_id
text nullable, UNIQUE; candidate PK ghép tablet_id + room_id; giữ audit columns. Nullable DB
không tự quyết blank-vs-null của UI. Căn cứ: テーブル設計書 sheets 会議室マスタ,
タブレット管理マスタ, タブレット延長候補会議室マスタ hàng 9–17.

## Mock contracts

- BR_Com_003 IN: selected room IDs (nhiều) và 希望順位選択可フラグ=0. OUT: room ID/name/
  location/email đã chọn. Cancel/empty cần nguồn hoặc quyết định. Căn cứ: BD004/画面遷移定義!
  C9:D10; BD003/機能間引数定義!E15:H16, F32:H35.
- BR_Com_005 IN: status code số, không OUT. Chứng minh gọi mock cho 403; 422 xử lý message
  trên màn theo common spec. Căn cứ: BD005/機能間引数定義!F9:G9,
  補足資料_対象ステータスコード!D11:T18.
- Mock không chứng minh child-screen thật; case/expected cho interface dựa vào nguồn và
  reviewer.

## Điểm cần quyết định trong task

Auth/data/environment thật hay mock; mapping DTO/DB; hành vi chưa rõ (cancel, empty
candidate, lỗi sau từng thao tác); transaction chung một thao tác, không tạo quy định
concurrency/rollback riêng thiếu căn cứ; scope C1/C2 và giới hạn integration. Đây là danh
mục cần phân tích/Q&A, chưa có testcase/PASS/xác nhận review.
