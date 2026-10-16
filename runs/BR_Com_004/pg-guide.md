# Hướng dẫn triển khai prototype BR_Com_004

Tạo từ BD do user đưa (BD004 = `【RAS】(BR_Com_004)会議室タブレット登録_画面定義書.xlsx`). Mỗi rule,
điều kiện và việc cần code có `[SRC: file | sheet | ô/dòng]` hoặc `[DECISION: A-xx]`. Đây là hồ sơ
duy nhất S2 (code PG) dựa vào; người review G0 duyệt cả phân tích lẫn kế hoạch code.

Viết tắt nguồn: `BD004` = file BD ở trên; `RULES004` = `.agents/workflow/rules/BR_COM_004_RULES.md`
(bản tra nhanh tổng hợp từ API一覧 / テーブル設計書 / BD003 / BD005 — **chưa được xác nhận trên tài
liệu gốc trong run này**, xem mục "Tài liệu cần cho bước sau").

## 1. BD và phạm vi

| Function ID | Tên chức năng | File BD | Phiên bản / ngày (改訂履歴) | Scope | Ngoài scope |
|---|---|---|---|---|---|
| BR_Com_004 | 会議室タブレット登録 | runs/BR_Com_004/inputs/【RAS】(BR_Com_004)会議室タブレット登録_画面定義書.xlsx | Ver 1.01, 更新日 2026/07/31 (SRO 牟禮); 初版 1.00 2026/03/18 (SRO 尾崎). 1.01 chỉ thêm 全項目 của タブレット延長候補会議室マスタ vào SELECT_002 `[SRC: BD004 \| 改訂履歴 \| C7:P8, AR1:BJ2]` | Chức năng chính của màn 会議室タブレット登録 (4 event: 初期表示, chọn 設置会議室, nút tìm 延長候補会議室, 登録) gồm API + DB access + màn Angular (scope user chốt trong chat 2026-10-15) | BR_Com_003 会議室検索 (child screen) và BR_Com_005 一括予約エラー表示: **mock**. Không làm ứng dụng tablet WinUI, batch, BR_Com_002 |

Tên chức năng ở 表紙 ghi `(BR_Com004)` (không có gạch dưới) nhưng tên file và tài liệu dự án dùng
`BR_Com_004`; run dùng `BR_Com_004` `[SRC: BD004 | 表紙 | B7]`.

## 2. Sheet đã đọc và giới hạn

Đọc bằng `.agents/workflow/scripts/xlsx_view.py --sheet <tên>` (stdlib, đọc text ô + tọa độ).

| Sheet | Đọc bằng | Nội dung chính | Giới hạn |
|---|---|---|---|
| 表紙 | xlsx_view | Tên tài liệu, bộ phận, dự án | — |
| 改訂履歴 | xlsx_view | Ver 1.00 / 1.01, ngày, người, lý do sửa | Ngày là serial Excel (46099, 46234) → quy đổi 2026/03/18, 2026/07/31 |
| 機能概要 | xlsx_view | Mục đích, người dùng システム管理者, tiền đề なし, chạy khi cài tablet lần đầu, business flow liên quan | — |
| 機能間引数定義 | xlsx_view | IN: không (menu link); OUT: không | — |
| レイアウト | xlsx_view | Chỉ có tiêu đề ô B3 | **Layout là ảnh/shape — script không đọc được; cần người xem Excel** |
| 項目定義 | xlsx_view | 5 item: 登録 button, 設置会議室 dropdown, タブレット端末ID textbox, 延長候補会議室 textbox (OUT), 延長候補会議室 search icon | Không có 桁数/型 cho textbox (đều `--`) |
| イベント定義 | xlsx_view | 4 event với 処理詳細 1-1 … 4-5 | — |
| 画面遷移定義 | xlsx_view | 遷移 001 → 会議室検索 với 2 tham số | — |
| 画面表示定義 | xlsx_view | 表示 001 (sau SELECT_002), 002 (sau child search) | — |
| データアクセス定義 | xlsx_view | SELECT_001, SELECT_002, INSERT_001, INSERT_002, UPDATE_001, DELETE_001 | — |
| エラーチェック一覧 | xlsx_view | No.1 権限 (403), No.2 登録確認 (警告), No.3 タブレット端末ID存在チェック | — |
| (非表示)画面レイアウト | xlsx_view | Text của mock-up: menu trái (一括予約, 一括予約一覧, 会議出席者空き予約, 会議室タブレット登録), tiêu đề, 3 label, ログインユーザ名 | Chỉ đọc được text trong ô; vị trí/hiển thị nút không đọc được |
| (非表示)レイアウト部品 | xlsx_view | Danh sách loại component | Tham khảo |
| (非表示)リスト | xlsx_view | Danh sách giá trị chọn cho 項目定義 | Tham khảo |

## 3. Luồng chính theo event

| Thứ tự | Người dùng/trigger | Xử lý hệ thống | Dữ liệu thay đổi | Nguồn |
|---|---|---|---|---|
| E1-1 | Mở màn từ menu (初期表示) | Kiểm tra quyền: login user không có quyền システム管理者 → chuyển sang 一括予約エラー表示 (BR_Com_005, mock) với 403 | — | `[SRC: BD004 \| イベント定義 \| E6:G6]`, `[SRC: BD004 \| エラーチェック一覧 \| B7:H7]` |
| E1-2 | (tiếp E1) | SELECT_001: lấy toàn bộ 会議室マスタ, sort 会議室名 昇順, đổ vào dropdown 設置会議室; giá trị đầu `"未選択"` | — | `[SRC: BD004 \| イベント定義 \| E7:G7]`, `[SRC: BD004 \| データアクセス定義 \| D9:D22]`, `[SRC: BD004 \| 項目定義 \| J8]` |
| E2-1 | Chọn một phòng ở dropdown 設置会議室 | SELECT_002: lấy タブレット管理マスタ của phòng đó, outer join タブレット延長候補会議室マスタ và 会議室マスタ | — | `[SRC: BD004 \| イベント定義 \| B9:G9]`, `[SRC: BD004 \| データアクセス定義 \| D24:D39]` |
| E2-2 | (tiếp E2) | Hiển thị タブレット端末ID và 延長候補会議室 (tên phòng nối `;`); không có dữ liệu → clear 2 field | — | `[SRC: BD004 \| イベント定義 \| E10:G10]`, `[SRC: BD004 \| 画面表示定義 \| C6:D9]`, `[SRC: BD004 \| 項目定義 \| I10]` |
| E2-3 | Chọn lại `"未選択"` | Ẩn nút 登録 và search icon, タブレット端末ID không nhập được; clear giá trị | — | `[SRC: BD004 \| 項目定義 \| M7, N9, M11]`, `[DECISION: A-11]` |
| E3-1 | Bấm search icon 延長候補会議室 | Mở child 会議室検索 (BR_Com_003, mock) với 会議室ID = các phòng đang ở 延長候補会議室, 希望順位選択可フラグ = 0 | — | `[SRC: BD004 \| イベント定義 \| B12:G12]`, `[SRC: BD004 \| 画面遷移定義 \| C6:D10]` |
| E3-2 | Child trả kết quả | Thay 延長候補会議室 bằng 会議室名 các phòng đã chọn (nối `;`), giữ 会議室ID để đăng ký | — | `[SRC: BD004 \| イベント定義 \| E13:G13]`, `[SRC: BD004 \| 画面表示定義 \| C11:D13]`, `[DECISION: A-08]` |
| E4-1 | Bấm 登録 | Hiện 警告 xác nhận `入力情報を登録します。よろしいですか？`; OK → tiếp, Cancel → không làm gì | — | `[SRC: BD004 \| エラーチェック一覧 \| B8:G8]`, `[DECISION: A-04]` |
| E4-2 | (tiếp) | Check No.3: タブレット端末ID đã tồn tại trong タブレット管理マスタ và gắn với phòng khác phòng đang chọn → lỗi `タブレット端末ID：他の会議室に登録されています。（会議室名：{0}）`, dừng | — | `[SRC: BD004 \| エラーチェック一覧 \| B9:H9]` |
| E4-3 | (tiếp) | Chưa có タブレット管理マスタ cho phòng → INSERT_001 (タブレットID = UUID mới); đã có → UPDATE_001 (タブレット端末ID) | tablets_mst | `[SRC: BD004 \| イベント定義 \| E16:G17]`, `[SRC: BD004 \| データアクセス定義 \| D43:E50, D62:D69]` |
| E4-4 | (tiếp) | DELETE_001: xóa toàn bộ タブレット延長候補会議室マスタ theo 処理対象のタブレットID | candidate_rooms_mst | `[SRC: BD004 \| イベント定義 \| E18:G18]`, `[SRC: BD004 \| データアクセス定義 \| D73:D77]` |
| E4-5 | (tiếp) | INSERT_002: insert mỗi 延長候補会議室 đã chọn (タブレットID, 延長候補会議室ID) | candidate_rooms_mst | `[SRC: BD004 \| イベント定義 \| E19:G19]`, `[SRC: BD004 \| データアクセス定義 \| D52:F58]` |
| E4-6 | (tiếp) | Hiện success `タブレット情報を登録しました。`; nạp lại dữ liệu phòng đang chọn | — | `[SRC: BD004 \| イベント定義 \| E20:F21]`, `[DECISION: A-09]` |

E4-3 … E4-5 chạy trong **một transaction** `[DECISION: A-06]`.

## 4. Màn hình: field, validation, state

| Field ID | Tên | Kiểu / độ dài | Bắt buộc | Validation / message | State (enable/visible) | Nguồn |
|---|---|---|---|---|---|---|
| F-01 | 登録 | ボタン | — | Trước khi gọi API: confirm 警告 (エラーチェック No.2) | **Ẩn** khi 設置会議室 = `"未選択"` | `[SRC: BD004 \| 項目定義 \| B7:N7]` |
| F-02 | 設置会議室 | ドロップダウンリスト | ○ | Giá trị lấy từ 会議室マスタ．会議室名 (SELECT_001); không gõ tự do | Luôn hiển thị; 初期値 `"未選択"` | `[SRC: BD004 \| 項目定義 \| B8:N8]` |
| F-03 | タブレット端末ID | テキストボックス（文字）, IN/OUT; BD không ghi 桁数/型 | × | Không required, không max-length từ BD; check trùng ở server (No.3); lọc ký tự nguy hiểm theo common spec (backend bắt buộc) | **Không nhập được** khi 設置会議室 = `"未選択"`; giá trị từ 画面表示定義 001 | `[SRC: BD004 \| 項目定義 \| B9:N9]`, `[DECISION: A-02]`, `[DECISION: A-12]` |
| F-04 | 延長候補会議室 (hiển thị) | テキストボックス（文字）, OUT | × | Chỉ hiển thị; 会議室名 cách nhau `;` | Read-only (không gõ); giá trị từ 画面表示定義 001/002 | `[SRC: BD004 \| 項目定義 \| B10:N10]`, `[DECISION: A-01]` |
| F-05 | 延長候補会議室 (search icon) | 検索イメージボタン | — | Mở BR_Com_003 (mock) | **Ẩn** khi 設置会議室 = `"未選択"` | `[SRC: BD004 \| 項目定義 \| B11:N11]` |

Màn có shell chung: menu trái với 一括予約 / 一括予約一覧 / 会議出席者空き予約 / 会議室タブレット登録,
tiêu đề `会議室タブレット登録`, ログインユーザ名 `[SRC: BD004 | (非表示)画面レイアウト | B2:M10]`. Tái dùng shell
layout, select-box, text-input, search-icon-button, action-button, message-box của ras-web (UI_RULES).

## 5. Nhánh lỗi và tình huống biên

| Điều kiện | Hành vi | Message / chuyển màn | Nguồn |
|---|---|---|---|
| Login user không có quyền システム管理者 (初期表示) | Không hiển thị màn; chuyển BR_Com_005 (mock) với status 403 | Message do 一括予約エラー表示 định nghĩa (ngoài BD004) | `[SRC: BD004 \| エラーチェック一覧 \| B7:H7]`, `[DECISION: A-07]` |
| Bấm 登録 | Warning confirm trước khi gọi API | `入力情報を登録します。よろしいですか？` | `[SRC: BD004 \| エラーチェック一覧 \| B8:G8]` |
| タブレット端末ID tồn tại ở phòng khác | Trả 422 business error; màn hiển thị error đỏ dưới title, không ghi DB | `タブレット端末ID：他の会議室に登録されています。（会議室名：{0}）`, `{0}` = tên phòng đang gắn với ID đó | `[SRC: BD004 \| エラーチェック一覧 \| B9:H9]`, `[DECISION: A-04]`, `[DECISION: A-15]` |
| タブレット端末ID tồn tại nhưng gắn đúng phòng đang chọn | Không lỗi; UPDATE_001 | — | `[SRC: BD004 \| エラーチェック一覧 \| F9]` (điều kiện "異なる設置会議室") |
| タブレット端末ID để trống khi 登録 | Cho phép (必須 ×); lưu NULL; bỏ qua check No.3 | — | `[SRC: BD004 \| 項目定義 \| F9]`, `[DECISION: A-02]`, `[DECISION: A-03]` |
| 延長候補会議室 rỗng khi 登録 | DELETE_001 vẫn chạy, INSERT_002 không insert dòng nào | — | `[DECISION: A-05]` |
| SELECT_002 không có dữ liệu | Clear タブレット端末ID và 延長候補会議室 | — | `[SRC: BD004 \| イベント定義 \| F10]` |
| Child 会議室検索 bị cancel / không chọn gì | Giữ nguyên 延長候補会議室 hiện tại | — | `[DECISION: A-08]` |
| API lỗi hệ thống / timeout | Theo contract chung: global filter → 500/504; màn hiển thị theo common handler | Common | ARCHITECTURE_RULES (HTTP contract) |

## 6. Dữ liệu và API

Tên bảng vật lý theo RULES004 (`rooms_mst`, `tablets_mst`, `candidate_rooms_mst`) — xác nhận lại với
テーブル設計書 ở S2 `[DECISION: A-16]`.

| Mục | Bảng / API | Thao tác (R/W) | Điều kiện | Nguồn |
|---|---|---|---|---|
| SELECT_001 | 会議室マスタ (rooms_mst) | R, toàn bộ cột | Không filter; sort 会議室名 昇順; không giới hạn số dòng | `[SRC: BD004 \| データアクセス定義 \| D9:D22]` |
| SELECT_002 | タブレット管理マスタ LEFT JOIN タブレット延長候補会議室マスタ ON タブレットID LEFT JOIN 会議室マスタ ON 延長候補会議室ID = 会議室ID | R, toàn bộ cột 3 bảng | `タブレット管理マスタ.会議室ID = 画面.設置会議室`; **outer join**, không đổi inner | `[SRC: BD004 \| データアクセス定義 \| D24:D39]` |
| INSERT_001 | タブレット管理マスタ | W insert | タブレットID = UUID mới; 会議室ID = phòng đang chọn; タブレット端末ID = input | `[SRC: BD004 \| データアクセス定義 \| D43:E50]` |
| UPDATE_001 | タブレット管理マスタ | W update | SET タブレット端末ID = input WHERE タブレットID = 処理対象 | `[SRC: BD004 \| データアクセス定義 \| D62:D69]` |
| DELETE_001 | タブレット延長候補会議室マスタ | W delete | WHERE タブレットID = 処理対象 | `[SRC: BD004 \| データアクセス定義 \| D73:D77]` |
| INSERT_002 | タブレット延長候補会議室マスタ | W insert (n dòng) | タブレットID = 処理対象; 延長候補会議室ID = từng phòng đã chọn | `[SRC: BD004 \| データアクセス定義 \| D52:F58]` |
| Check No.3 | タブレット管理マスタ JOIN 会議室マスタ | R | WHERE タブレット端末ID = input AND 会議室ID <> phòng đang chọn → lấy 会議室名 | `[SRC: BD004 \| エラーチェック一覧 \| F9:H9]` |
| API_008 | `POST /private/rooms-mst-list` | R | Cho SELECT_001; role 社内ユーザ + システム管理者 | RULES004 (API一覧!B16:K16) `[DECISION: A-16]` |
| API_004 | `GET /private/tablet-info/{roomId}` | R | Cho SELECT_002; role システム管理者 | RULES004 (API一覧!B12:K12) `[DECISION: A-16]` |
| API_005 | `POST /private/tablet-info` | W | Cho check No.3 + INSERT/UPDATE/DELETE/INSERT; role システム管理者 | RULES004 (API一覧!B13:K13) `[DECISION: A-16]` |

Envelope HTTP `ApiResponse<T>` (data / errors[field,message]); 403 quyền, 422 business error (ARCHITECTURE_RULES).

## 7. Phụ thuộc và ranh giới mock

| Thành phần | Trong scope / mock / chỉ tham chiếu | Contract trao đổi | Nguồn hoặc giả định |
|---|---|---|---|
| Màn 会議室タブレット登録 (Angular) + API_004/005/008 + repository/EF | **Trong scope** | — | Scope user |
| BR_Com_003 会議室検索 (child) | **Mock** | IN: danh sách 会議室ID (các phòng đang ở 延長候補会議室), 希望順位選択可フラグ = 0. OUT: danh sách phòng đã chọn (ID, 会議室名; location/email không dùng ở màn này). Cancel → không có OUT | `[SRC: BD004 \| 画面遷移定義 \| C6:D10]`, RULES004 (BD003 機能間引数定義), `[DECISION: A-08]` |
| BR_Com_005 一括予約エラー表示 | **Mock** | IN: status code số (403). Không OUT | `[SRC: BD004 \| エラーチェック一覧 \| G7:H7]`, RULES004 (BD005 機能間引数定義), `[DECISION: A-07]` |
| Auth (Entra ID / policy role) | **Tái dùng cơ chế hiện có của repo** | Policy システム管理者 trên API_004/005; 社内ユーザ hoặc システム管理者 trên API_008 | ARCHITECTURE_RULES, RULES004, `[DECISION: A-17]` |
| 会議室マスタ dữ liệu | Chỉ đọc (do màn khác/seed tạo) | — | `[SRC: BD004 \| データアクセス定義 \| D12]` |
| Shared UI / ApiService / messages / validators của ras-web; Common của ras-system | Tái dùng, không sửa | — | UI_RULES, ARCHITECTURE_RULES |

## Giả định của AI (chỗ BD mơ hồ hoặc thiếu)

AI tự chọn cách hiểu và ghi ở đây, không dừng chờ. Mỗi dòng có ID `A-xx`; Rule/code dựa
trên giả định ghi `[DECISION: A-xx]`. Người review G0 đánh dấu Chấp nhận / Sửa; giả định bị
sửa sau G0 → user yêu cầu làm lại S1 trong chat.

| ID | Vị trí BD mơ hồ | Các cách hiểu | AI chọn | Lý do | Ảnh hưởng nếu sai | Review G0 |
|---|---|---|---|---|---|---|
| A-01 | 項目定義!B10 延長候補会議室 là テキストボックス nhưng I/O = OUT | (a) read-only, chỉ đổi qua search icon; (b) cho gõ tay tên phòng | (a) read-only | I/O OUT, 入力/表示規則 chỉ nói cách hiển thị; không có rule parse tên phòng → ID | Nếu (b): cần validation tên phòng → ID, thêm rule/case | |
| A-02 | 項目定義!F9 タブレット端末ID 必須 = × | (a) cho đăng ký với ID trống, lưu NULL; (b) chặn ở client | (a) | BD nói không bắt buộc; テーブル設計書 (theo RULES004) machine_id nullable | Nếu (b): thêm validation + message chưa có nguồn | |
| A-03 | エラーチェック No.3 khi タブレット端末ID trống | (a) bỏ qua check; (b) check với chuỗi rỗng | (a) | Không có ID thì không thể "tồn tại ở phòng khác" | Nếu (b): có thể trùng NULL/blank giữa các phòng | |
| A-04 | Thứ tự confirm (No.2) và check trùng (No.3), nơi thực hiện | (a) client confirm → gọi API_005 → server check No.3 → 422; (b) client check trước rồi confirm | (a) | 警告 là xác nhận người dùng, lỗi nghiệp vụ phải kiểm ở backend (ARCHITECTURE_RULES); giảm round-trip | Nếu (b): cần thêm API check riêng | |
| A-05 | 登録 khi 延長候補会議室 rỗng | (a) DELETE_001 chạy, INSERT_002 0 dòng (cho phép xóa hết candidate); (b) báo lỗi | (a) | BD không có check required cho candidate; flow 4-3/4-4 không điều kiện | Nếu (b): cần message chưa có nguồn | |
| A-06 | Transaction cho 4-2 … 4-4 | (a) một transaction cho toàn bộ 登録 ở UseCase; (b) từng câu lệnh riêng | (a) | ARCHITECTURE_RULES: boundary ở UseCase, một thao tác ghi = một transaction; tránh dữ liệu nửa chừng | Nếu (b): có thể còn tablet không có candidate khi lỗi giữa chừng | |
| A-07 | エラーチェック No.1 thực hiện ở đâu, chuyển màn thế nào | (a) backend trả 403 từ API_008/004 theo policy, frontend guard + interceptor điều hướng tới BR_Com_005 mock kèm 403; (b) chỉ guard frontend | (a) | Guard frontend chỉ là UX; API phải bảo vệ (ARCHITECTURE_RULES). API_008 dùng chung nên 初期表示 còn gọi thêm API_004? Không — 初期表示 chỉ gọi API_008; quyền màn kiểm bằng role trong token ở frontend guard, backend bảo vệ API_004/005 | Nếu khác: thay đổi điểm điều hướng/case 403 | |
| A-08 | Child 会議室検索 là mock: giao diện, cancel, kết quả rỗng | (a) mock = modal chọn nhiều phòng từ danh sách SELECT_001, pre-check theo IN; OK trả list đã chọn (có thể rỗng), Cancel giữ nguyên; (b) mock trả cố định | (a) | Đủ để thao tác và test luồng E3; không phát triển BR_Com_003 thật | Nếu contract BD003 khác (vd. không cho rỗng): sửa mock và case | |
| A-09 | Sau success 4-5 màn làm gì | (a) hiện success modal, giữ phòng đang chọn, gọi lại API_004 để nạp dữ liệu mới; (b) reset về 未選択 | (a) | Người dùng thấy kết quả vừa lưu; BD không nói reset | Nếu (b): case kết thúc khác | |
| A-10 | 延長候補会議室 có được chứa chính 設置会議室 hay trùng ID | (a) không chặn (mock trả gì lưu nấy, loại trùng ID); (b) chặn phòng đang chọn | (a) | BD không có check; PK ghép (tablet_id, room_id) nên chỉ cần loại trùng | Nếu (b): thêm validation chưa có nguồn | |
| A-11 | Chọn lại `"未選択"` sau khi đã có dữ liệu | (a) ẩn nút, disable input và **clear** タブレット端末ID / 延長候補会議室; (b) giữ giá trị | (a) | Nhất quán với "データが取得できない場合は値をクリアする" | Nếu (b): khác state UI, không ảnh hưởng DB | |
| A-12 | Lọc ký tự nguy hiểm (common spec) cho タブレット端末ID | (a) áp dụng check chuỗi cấm của 画面共通仕様 ở backend (và validator shared ở client nếu có), lỗi 400; (b) không áp | (a) | UI_RULES: backend phải kiểm tra; textbox chữ thuộc phạm vi | Nếu (b): bỏ 1 rule; nếu phạm vi/regex khác: sửa theo workbook gốc (PENDING) | |
| A-13 | Thứ tự hiển thị 延長候補会議室 (SELECT_002 ソート なし) | (a) 会議室名 昇順; (b) thứ tự DB trả về | (a) | Hiển thị xác định được để test | Nếu (b): expected hiển thị đổi | |
| A-14 | Kiểu dữ liệu 会議室ID / 希望順位選択可フラグ truyền cho child | (a) UUID string[] và number 0; (b) khác | (a) | RULES004: ID là UUID; flag ghi `0` | Chỉ ảnh hưởng mock contract | |
| A-15 | `{0}` trong message No.3 khi ID trùng ở nhiều phòng | (a) machine_id UNIQUE nên chỉ 1 phòng; lấy 会議室名 của dòng đó | (a) | RULES004: UNIQUE | Nếu không UNIQUE: nối nhiều tên hoặc lấy dòng đầu — cần quyết định | |
| A-16 | Endpoint/tên bảng/cột lấy từ RULES004 (bản tổng hợp), chưa có API一覧 / テーブル設計書 gốc | (a) dùng tạm theo RULES004, xác nhận ở S2; (b) dừng chờ | (a) | SOURCE_MAP: API一覧/テーブル設計書 là "nếu có" ở S1, bắt buộc ở S2 | Nếu khác: sửa DTO/route/entity ở S2, không đổi Rule | |
| A-17 | Auth thật hay mock cho PoC | (a) dùng nguyên cơ chế auth/policy đang có trong serio-ras (kể cả dev/mock nếu repo đã có), không bypass; (b) tạo mock auth riêng | (a) | Không bypass auth (ARCHITECTURE_RULES); tránh code ngoài scope | Nếu repo chưa có policy role phù hợp: ghi giả định mới ở S2 | |
| A-18 | タブレット端末ID so sánh trùng có phân biệt hoa/thường và khoảng trắng? | (a) trim rồi so sánh chính xác theo DB (citext nếu cột là citext); (b) so sánh thô | (a) | PostgreSQL citext dùng trong RAS (ARCHITECTURE_RULES) | Chỉ ảnh hưởng edge case | |

## Rules

Mỗi nghĩa vụ nghiệp vụ có ID ổn định, kể cả biên/lỗi cần kiểm tra. Required dùng YES/NO.
Source ghi file / sheet / ô hoặc `[DECISION: A-xx]`. Escape dấu pipe bằng \| trong bảng.

| Rule ID | Source | Statement | Required |
|---|---|---|---|
| R-001 | BD004 / エラーチェック一覧 / B7:H7; イベント定義 / E6:G6 | 初期表示: login user không có quyền システム管理者 → chuyển BR_Com_005 (mock) với 403, không hiển thị màn | YES |
| R-002 | BD004 / イベント定義 / E7:G7; データアクセス定義 / D9:D22 | 初期表示: SELECT_001 lấy toàn bộ 会議室マスタ, sort 会議室名 昇順, đổ vào dropdown 設置会議室 | YES |
| R-003 | BD004 / 項目定義 / J8 | Dropdown 設置会議室 có giá trị đầu `"未選択"` và là giá trị khởi tạo | YES |
| R-004 | BD004 / 項目定義 / M7, M11 | Khi 設置会議室 = `"未選択"`: ẩn nút 登録 và search icon 延長候補会議室; khác → hiển thị | YES |
| R-005 | BD004 / 項目定義 / N9 | Khi 設置会議室 = `"未選択"`: タブレット端末ID không nhập được; khác → nhập được | YES |
| R-006 | BD004 / イベント定義 / B9:G9; データアクセス定義 / D24:D39 | Chọn phòng: SELECT_002 lấy タブレット管理マスタ của phòng (WHERE 会議室ID = phòng chọn) outer join タブレット延長候補会議室マスタ (タブレットID) outer join 会議室マスタ (延長候補会議室ID = 会議室ID), trả toàn bộ cột 3 bảng | YES |
| R-007 | BD004 / イベント定義 / E10:G10; 画面表示定義 / C6:D9 | Có dữ liệu: hiển thị タブレット管理マスタ．タブレット端末ID vào textbox và 会議室名 các candidate vào 延長候補会議室 | YES |
| R-008 | BD004 / 項目定義 / I10; [DECISION: A-13] | 延長候補会議室 hiển thị tên phòng cách nhau `;` (không khoảng trắng thêm), sort 会議室名 昇順 | YES |
| R-009 | BD004 / イベント定義 / F10 | SELECT_002 không có dữ liệu → clear タブレット端末ID và 延長候補会議室 | YES |
| R-010 | [DECISION: A-11] | Chọn lại `"未選択"` → clear タブレット端末ID và 延長候補会議室 (kèm R-004/R-005) | NO |
| R-011 | BD004 / イベント定義 / B12:G12; 画面遷移定義 / C6:D10; [DECISION: A-14] | Bấm search icon: mở child 会議室検索 (mock) với 会議室ID = ID các phòng hiện ở 延長候補会議室 và 希望順位選択可フラグ = 0 | YES |
| R-012 | BD004 / イベント定義 / E13:G13; 画面表示定義 / C11:D13 | Child trả kết quả: thay toàn bộ 延長候補会議室 bằng danh sách phòng đã chọn (hiển thị 会議室名, giữ 会議室ID) | YES |
| R-013 | [DECISION: A-08] | Child cancel hoặc không trả kết quả → giữ nguyên 延長候補会議室 hiện tại | NO |
| R-014 | BD004 / エラーチェック一覧 / B8:G8; [DECISION: A-04] | Bấm 登録: hiện 警告 `入力情報を登録します。よろしいですか？`; OK mới gọi API_005; Cancel không gọi | YES |
| R-015 | BD004 / エラーチェック一覧 / B9:H9; [DECISION: A-04], [DECISION: A-15] | API_005: タブレット端末ID tồn tại trong タブレット管理マスタ và gắn với 会議室ID khác phòng đang chọn → 422 với message `タブレット端末ID：他の会議室に登録されています。（会議室名：{0}）`, `{0}` = 会議室名 của phòng đang gắn; không ghi DB | YES |
| R-016 | BD004 / エラーチェック一覧 / F9 | タブレット端末ID tồn tại nhưng gắn đúng phòng đang chọn → không lỗi, đi tiếp | YES |
| R-017 | BD004 / 項目定義 / F9; [DECISION: A-02], [DECISION: A-03] | タブレット端末ID trống được phép đăng ký; lưu NULL; bỏ qua check R-015 | YES |
| R-018 | BD004 / イベント定義 / F16; データアクセス定義 / D43:E50 | Chưa có タブレット管理マスタ cho phòng đang chọn → INSERT_001: タブレットID = UUID mới, 会議室ID = phòng chọn, タブレット端末ID = input | YES |
| R-019 | BD004 / イベント定義 / F17; データアクセス定義 / D62:D69 | Đã có タブレット管理マスタ cho phòng → UPDATE_001: SET タブレット端末ID = input WHERE タブレットID = 処理対象 (không tạo UUID mới) | YES |
| R-020 | BD004 / イベント定義 / E18:G18; データアクセス定義 / D73:D77 | DELETE_001: xóa toàn bộ タブレット延長候補会議室マスタ WHERE タブレットID = 処理対象 | YES |
| R-021 | BD004 / イベント定義 / E19:G19; データアクセス定義 / D52:F58; [DECISION: A-10] | INSERT_002: insert một dòng (処理対象 タブレットID, 延長候補会議室ID) cho mỗi phòng đã chọn (loại trùng ID) | YES |
| R-022 | [DECISION: A-05] | 延長候補会議室 rỗng → DELETE_001 vẫn chạy, INSERT_002 không insert dòng nào; không báo lỗi | YES |
| R-023 | [DECISION: A-06]; ARCHITECTURE_RULES (9.データアクセス設計方針) | R-018/R-019 + R-020 + R-021 trong một transaction ở UseCase; lỗi giữa chừng → rollback toàn bộ | YES |
| R-024 | BD004 / イベント定義 / E20:F21; [DECISION: A-09] | Thành công → hiện success `タブレット情報を登録しました。`; giữ phòng đang chọn và nạp lại dữ liệu (R-006) | YES |
| R-025 | RULES004 (API一覧 G12:H13, G16:H16); [DECISION: A-16], [DECISION: A-17] | API_004 và API_005 chỉ cho システム管理者 (403 nếu không); API_008 cho 社内ユーザ và システム管理者; dùng policy hiện có của repo | YES |
| R-026 | UI_RULES (6.入力仕様 I9:I31); [DECISION: A-12] | タブレット端末ID chứa chuỗi cấm của common spec → 400 từ backend (và validator shared ở client nếu đã có) | NO |
| R-027 | ARCHITECTURE_RULES (6.API設計方針) | API_004/005/008 trả envelope `ApiResponse<T>` chung; lỗi nghiệp vụ ở `errors[]` với field/message; không tạo wrapper mới | YES |
| R-028 | BD004 / (非表示)画面レイアウト / B2:M10; UI_RULES | Màn dùng shell layout chung (menu trái, tiêu đề `会議室タブレット登録`, ログインユーザ名) và shared components | NO |

## Atomic conditions

| Condition ID | Rule ID | Expression | True/False meaning | Source |
|---|---|---|---|---|
| C-001 | R-001 | login user có role システム管理者 | T: hiển thị màn, gọi SELECT_001 / F: chuyển BR_Com_005 mock với 403 | BD004 / エラーチェック一覧 / F7:H7 |
| C-002 | R-004 | 設置会議室 == `"未選択"` | T: ẩn 登録 và search icon / F: hiển thị | BD004 / 項目定義 / M7, M11 |
| C-003 | R-005 | 設置会議室 == `"未選択"` | T: タブレット端末ID disabled / F: enabled | BD004 / 項目定義 / N9 |
| C-004 | R-009 | SELECT_002 trả về tablet của phòng (có dòng) | T: hiển thị R-007 / F: clear R-009 | BD004 / イベント定義 / F10 |
| C-005 | R-007 | tablet có ít nhất một candidate (outer join có dòng con) | T: hiển thị tên nối `;` / F: 延長候補会議室 rỗng | BD004 / データアクセス定義 / D30:G31 |
| C-006 | R-017 | タブレット端末ID (sau trim) rỗng | T: lưu NULL, bỏ qua C-007/C-008 / F: thực hiện check trùng | [DECISION: A-02], [DECISION: A-03] |
| C-007 | R-015 | tồn tại タブレット管理マスタ có タブレット端末ID == input | T: kiểm C-008 / F: không lỗi | BD004 / エラーチェック一覧 / F9 |
| C-008 | R-015 | 会議室ID của dòng tìm thấy (C-007) != 設置会議室 đang chọn | T: 422 R-015 / F: không lỗi (R-016) | BD004 / エラーチェック一覧 / F9 |
| C-009 | R-018 | tồn tại タブレット管理マスタ WHERE 会議室ID == 設置会議室 đang chọn | T: UPDATE_001 (R-019) / F: INSERT_001 (R-018) | BD004 / イベント定義 / F16:F17 |
| C-010 | R-022 | danh sách 延長候補会議室 gửi lên rỗng | T: không INSERT_002 / F: INSERT_002 n dòng | [DECISION: A-05] |
| C-011 | R-014 | người dùng chọn OK ở confirm | T: gọi API_005 / F: không làm gì | BD004 / エラーチェック一覧 / B8:G8 |
| C-012 | R-013 | child 会議室検索 trả kết quả (không cancel) | T: thay 延長候補会議室 (R-012) / F: giữ nguyên | [DECISION: A-08] |
| C-013 | R-023 | một bước ghi trong transaction ném lỗi | T: rollback toàn bộ, trả 500 theo global filter / F: commit | [DECISION: A-06] |
| C-014 | R-025 | role trong token thỏa policy của endpoint | T: xử lý / F: 403 | RULES004 (API一覧 G12:H16) |
| C-015 | R-026 | タブレット端末ID khớp mẫu chuỗi cấm của common spec | T: 400 / F: hợp lệ | [DECISION: A-12] |

## Kế hoạch code

Chỉ rõ S2 phải code gì, ở đâu. "Vị trí dự kiến" theo cấu trúc repo đã biết từ
REPOSITORY_RULES / ARCHITECTURE_RULES; repo user chỉ định là `serio-ras` (cùng collection), đã
nhìn qua cấu trúc thư mục (ras-system/src/Services/Ras/{RasApi,RasDomain,RasUseCase,RasInfrastructure,
RasApi.UnitTests}, ras-web/src/app/{features,shared}) khớp bảng tham chiếu; tên file/namespace/
schema thật **xác nhận ở S2**. Thứ tự code theo 開発手順書: entity → DbContext → repository →
UseCase → Controller → DI/validation → frontend.

| Mục | Rule ID | Vị trí dự kiến | Việc cần làm | Tái dùng common | Mock |
|---|---|---|---|---|---|
| P-01 Entity | R-006, R-018, R-021 | ras-system/src/Services/Ras/RasDomain (Entities) | Entity `Room` (rooms_mst), `Tablet` (tablets_mst: id UUID, room_id UUID, machine_id text nullable), `CandidateRoom` (candidate_rooms_mst: PK ghép tablet_id + room_id); audit columns theo base entity hiện có; cột/kiểu đối chiếu テーブル設計書 ở S2 | Base entity / audit của repo | — |
| P-02 DbContext | R-006, R-020, R-021 | ras-system/src/Services/Ras/RasInfrastructure (DbContext + configurations) | Map 3 bảng, UNIQUE machine_id, composite key candidate, quan hệ Tablet 1-n CandidateRoom, CandidateRoom n-1 Room; không đổi schema mặc định nếu repo đã có | DbContext hiện có | — |
| P-03 Repository interface | R-002, R-006, R-015, R-018, R-019, R-020, R-021 | RasDomain (interfaces) | `IRoomRepository.GetAllOrderedByNameAsync()` (SELECT_001); `ITabletRepository.GetByRoomWithCandidatesAsync(roomId)` (SELECT_002, Include outer join), `FindByMachineIdAsync(machineId)` (check No.3), `AddAsync`, `UpdateMachineIdAsync`, `DeleteCandidatesByTabletIdAsync(tabletId)`, `AddCandidatesAsync(list)` | Repository base nếu có | — |
| P-04 Repository impl | R-002, R-006, R-015, R-018, R-019, R-020, R-021 | RasInfrastructure (Repositories) | EF Core: SELECT_001 OrderBy(name); SELECT_002 Where(room_id) + Include(Candidates).ThenInclude(Room) (LEFT JOIN); FindByMachineId Include(Room) để lấy 会議室名; Delete + AddRange cho candidate; ghi comment `SELECT_001`… tại từng method | Npgsql/EF config hiện có | — |
| P-05 UseCase DTO | R-007, R-008, R-027 | RasUseCase (DTOs) | `TabletInfoResponse { TabletId, RoomId, MachineId, Candidates[] {RoomId, RoomName} }` (candidates sort name asc); `RegisterTabletInfoRequest { RoomId, MachineId, CandidateRoomIds[] }`; `RoomListItem { RoomId, RoomName }` | Result / ResultMessage, DTO conventions | — |
| P-06 UseCase service | R-015, R-016, R-017, R-018, R-019, R-020, R-021, R-022, R-023, R-024 | RasUseCase (Services) | `TabletInfoService.GetByRoomAsync(roomId)`; `RegisterAsync(request)`: trim machineId → C-006; C-007/C-008 → Result lỗi 422 với message R-015 (format `{0}`); C-009 → insert (Guid.NewGuid) hoặc update; DELETE_001; distinct candidate IDs → INSERT_002 (C-010); toàn bộ trong một transaction (UnitOfWork/`BeginTransaction` theo pattern repo); trả Result thành công | Result pattern, UnitOfWork/transaction helper, message resources | — |
| P-07 Message | R-015, R-014, R-024 | ras-system/src/BuildingBlocks/Common (messages) và ras-web/src/app/shared (messages) | Đăng ký 3 literal đúng BD: `タブレット端末ID：他の会議室に登録されています。（会議室名：{0}）`, `入力情報を登録します。よろしいですか？`, `タブレット情報を登録しました。`; ID message theo quy ước repo (メッセージ一覧 PENDING) | Message resource hiện có | — |
| P-08 Controller | R-025, R-026, R-027 | RasApi (Controllers) | `GET /private/tablet-info/{roomId}` (API_004), `POST /private/tablet-info` (API_005) với policy システム管理者; `POST /private/rooms-mst-list` (API_008) với policy 社内ユーザ hoặc システム管理者 (nếu repo đã có endpoint tương đương thì tái dùng, ghi lệch); trả `ApiResponse<T>`; map Result lỗi → 422 | ApiResponse, auth policies, global exception filter | — |
| P-09 Validation server | R-026, R-017 | RasApi (validators / request validation) | Validator cho `RegisterTabletInfoRequest`: RoomId bắt buộc (GUID), MachineId optional, áp dụng check chuỗi cấm common spec (validator chung nếu có) → 400; CandidateRoomIds mỗi phần tử GUID | Validator chung của repo | — |
| P-10 DI | R-002, R-006, R-015, R-025 | RasApi (DI / Program) | Đăng ký repository, service, validator | Extension đăng ký DI hiện có | — |
| P-11 Feature Angular | R-002, R-003, R-004, R-005, R-007, R-008, R-009, R-010, R-028 | ras-web/src/app/features/tablet-registration | Component `tablet-registration` với route trong shell: select-box 設置会議室 (option đầu 未選択), text-input タブレット端末ID (disabled theo C-003), text-input read-only 延長候補会議室, search-icon-button và action-button 登録 (`*ngIf` theo C-002); `onRoomChange` gọi API_004 → set/clear (C-004) | shell layout, select-box, text-input, search-icon-button, action-button | — |
| P-12 Feature service | R-002, R-006, R-024, R-027 | ras-web/src/app/features/tablet-registration (service) | `TabletRegistrationService`: `getRooms()` → API_008, `getTabletInfo(roomId)` → API_004, `register(req)` → API_005 qua shared ApiService; không nhân bản HTTP/auth | shared ApiService, interceptors | — |
| P-13 Confirm / success / error | R-014, R-015, R-024 | ras-web feature + shared message-box | Nút 登録: message-box warning confirm (C-011) → gọi register; 422 → hiển thị error đỏ dưới title với message từ `errors[]`; thành công → success modal rồi gọi lại `getTabletInfo` | message-box, error display chung | — |
| P-14 Guard quyền màn | R-001 | ras-web/src/app/shared/guards (tái dùng) + route của feature | Route guard theo role システム管理者; không có → điều hướng tới BR_Com_005 mock với status 403; interceptor 403 từ API cũng điều hướng về mock | auth guard / interceptor hiện có | BR_Com_005 |
| P-15 Mock BR_Com_005 | R-001 | ras-web/src/app/features/bulk-reservation-error-mock (hoặc vị trí mock của repo) | Trang/route mock nhận tham số status code (403) và hiển thị code đó; không logic khác | — | **Mock** |
| P-16 Mock BR_Com_003 | R-011, R-012, R-013 | ras-web/src/app/features/room-search-mock | Modal/route mock: IN `roomIds: string[]`, `rankSelectable: 0`; hiển thị checkbox list phòng từ API_008 pre-check theo IN; OK → OUT `{roomId, roomName}[]` (có thể rỗng); Cancel → không OUT (C-012) | select/list components, dialog của repo | **Mock** |
| P-17 Unit test scaffold | R-015, R-018, R-019, R-022 | ras-system/src/Services/Ras/RasApi.UnitTests | Chỉ tạo project/thư mục test cho module mới nếu repo yêu cầu để build; **không** viết UT ở S2 (S5) | Test project hiện có | — |

## Tài liệu cần cho bước sau

| Bước | Tài liệu | Bắt buộc / nếu có | Trạng thái |
|---|---|---|---|
| S1 | API一覧 (`【RAS】API一覧.xlsx`) | Nếu có | PENDING — endpoint/role tạm lấy từ RULES004 (A-16); cần bản gốc để xác nhận API_004/005/008 |
| S1 | テーブル設計書 (`【RAS】テーブル設計書.xlsx`) | Nếu có | PENDING — tên bảng/cột/nullable/UNIQUE tạm theo RULES004 (A-02, A-15, A-16) |
| S1 | 画面共通仕様説明書, メッセージ一覧 | Nếu có | PENDING — quy tắc chuỗi cấm và ID message (A-12, P-07) |
| S1 | BD của BR_Com_003 / BR_Com_005 | Nếu có | PENDING — mock contract tạm theo RULES004 (A-07, A-08) |
| S1 | Người phụ trách (nghiệp vụ / thiết kế / reviewer / nghiệm thu) | Nếu có | PENDING — task.md chưa ghi |
| S2 PG | Đường dẫn repo code = `serio-ras` (user chỉ định), branch được giao, quyền build/lint; API一覧, テーブル設計書 | Bắt buộc | Repo đã có; **branch và quyền build/lint PENDING**; API一覧/テーブル設計書 PENDING |
| S3 Testspec | 単体テスト仕様書_ルール | Bắt buộc | PENDING |
| S4 DD | Mẫu 詳細設計書 / API定義書 | Nếu có | PENDING |
| S6 Evidence | 単体テスト実施_ルール, môi trường, tool coverage | Bắt buộc | PENDING |

Không suy rule từ code mẫu. Inventory nhánh/điều kiện code thực tế được kiểm tra ở
S2/S3/S5/S6.
