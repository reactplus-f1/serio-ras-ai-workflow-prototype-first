# Phân tích phụ thuộc BR_Com_004 会議室タブレット登録 ↔ BR_Com_003 / BR_Com_005

Ngày: 2026-10-16. Người lập: AI (Copilot), chưa review.
Mục đích: trả lời checklist "Nội dung thực hiện" của task phụ thuộc; làm căn cứ cho mục §7
(Phụ thuộc và ranh giới mock) và P-14/P-15/P-16 của `pg-guide.md`.

## 0. Nguồn đã đọc

| ID | Nguồn | Cách đọc | Ghi chú |
|---|---|---|---|
| BD004 | `inputs/【RAS】(BR_Com_004)会議室タブレット登録_画面定義書.xlsx` v1.01 | openpyxl, toàn bộ 14 sheet (giá trị ô) | Sheet レイアウト là ảnh, không đọc được bằng script |
| API | `【RAS】API一覧.xlsx` v1.01, sheet API一覧 r12–r16 | openpyxl | |
| SQL | `serio-ras/ras-system/sql/ras_tables.sql` | đọc file | Khớp テーブル設計書 cho 3 bảng liên quan |
| SRC | `serio-ras` branch `main` (966def8): `ras-web/src/app/**`, `ras-system/src/Services/Ras/**` | liệt kê + đọc file liên quan | Repo mới chỉ có khung + sample |
| CTX | Digest BD003/BD005 trong kit cũ (`profiles/serio_ras/docs/serio-context.md`, mục "Errors: (BR_Com_005)", "Room search: (BR_Com_003)", "How a user reaches each PoC screen") | đọc | **File BD003/BD005 gốc chưa được đưa vào run này.** Mọi dòng dựa vào CTX cần xác nhận lại với file gốc |

Không đọc: BD003/BD005 gốc, 画面遷移図 gốc, 画面共通仕様説明書, メッセージ一覧.

## 1. Kết luận ngắn

| Câu hỏi | Trả lời | Căn cứ |
|---|---|---|
| BR004 có phụ thuộc BR003 không? | **Có, một chiều, tại một event.** Event 3 (延長候補会議室検索イメージボタン押下) mở child 会議室検索 và nhận lại danh sách phòng đã chọn. Ngoài event này BR004 không cần BR003. | BD004 イベント定義 B12:G13, 画面遷移定義 C6:D10 |
| BR004 có phụ thuộc BR005 không? | **Có, gián tiếp qua cơ chế lỗi chung.** エラーチェック No.1 (không có quyền システム管理者) chuyển sang 一括予約エラー表示 với 403. BR004 không gọi BR005 trực tiếp; việc điều hướng là của guard/interceptor chung. | BD004 エラーチェック一覧 B7:H7; SRC `admin.guard.ts`, `api-error.interceptor.ts` |
| BR003/BR005 có phụ thuộc ngược BR004 không? | **Không.** BR003 còn được gọi từ BR_Res_003/004; BR005 nhận từ mọi màn 一括予約. Không màn nào cần dữ liệu BR004 tạo ra ngoài tablet app (RM_Res, ngoài scope). | CTX "How a user reaches each PoC screen" |
| Trong source hiện có gì của BR003/BR005? | **Chưa có gì.** Không có component/route/API nào cho 会議室検索 hay エラー表示. Guard và error handler đều `navigate(['/sample'])` kèm TODO "専用エラー画面が未実装". | SRC `app.routes.ts`, `admin.guard.ts`, `api-error-handler.service.ts` |
| Cái gì dùng chung được ngay? | Guard/interceptor/error-handler, `AuthService.hasRole`, shared components (select-box, text-input, search-icon-button, action-button, message-box, checkbox-group), `ApiService`, policy `AdministratorOnly`, DDL 3 bảng. | SRC |

→ Scope "BR003/BR005 = mock" trong `task.md` là hợp lý: BR004 chỉ cần **contract** của hai màn đó, không cần hành vi đầy đủ.

## 2. Danh sách phụ thuộc

Mức ảnh hưởng: **Cao** = BR004 không chạy được luồng chính nếu thiếu; **Trung** = một event/nhánh không chạy; **Thấp** = chỉ UX/hiển thị.

### D-01 BR_Com_003 会議室検索 (child screen)

| Mục | Nội dung |
|---|---|
| Màn/chức năng liên quan | BR_Com_003 会議室検索, gọi từ event 3 của BR004 |
| Căn cứ | BD004 イベント定義 B12:G13 (3-1 遷移, 3-2 hiển thị kết quả); 画面遷移定義 No.001: 遷移先 = 会議室検索, 引数 = 会議室ID (= phòng hiện ở 延長候補会議室), 希望順位選択可フラグ = False; 画面表示定義 No.002: 延長候補会議室テキストボックス ← 会議室マスタ．会議室名. CTX: BR003 là modal trên màn cha, URL không đổi; OUT = 会議室ID, 会議室名, 場所, 会議室メールアドレス của các phòng được chọn |
| Vị trí source liên quan | Chưa có. Thành phần tái dùng được cho mock: `shared/components/checkbox-group`, `data-table`, `message-box`, `search-icon-button`; API_008 `POST /private/rooms-mst-list` (chưa implement) |
| Dữ liệu vào | `roomIds: string[]` (UUID các phòng đang là 延長候補), `rankSelectable: false` |
| Dữ liệu ra | `{ roomId, roomName }[]` (BR004 chỉ dùng 2 trường; 場所/メールアドレス bỏ qua). Cancel → không có OUT |
| Mức ảnh hưởng | **Trung**: thiếu thì không sửa được 延長候補会議室 (event 3), nhưng 初期表示 / chọn phòng / 登録 vẫn chạy (INSERT_002 0 dòng) |
| Cách xử lý dự kiến | **Mock trong BR004** (P-16): modal chọn nhiều phòng từ API_008, pre-check theo IN, OK trả list, Cancel giữ nguyên. Tách interface `RoomSearchDialog` để sau thay bằng BR003 thật không sửa BR004 |
| Đã xác nhận | BR004 mở 会議室検索 với 2 tham số; kết quả là tên phòng hiển thị cách nhau `;` (BD004 項目定義 I10; `Constants.separator = '; '` trong SRC — lưu ý SRC có khoảng trắng sau `;`, BD ghi `(;)`: cần chốt) |
| Còn cần điều tra / xác nhận với Serio | (a) Trả về **thay thế** hay **thêm** vào danh sách hiện tại (CTX FND-006: BD003 chỉ nói "一覧で選択された会議室分のデータを返却"); (b) định dạng truyền nhiều 会議室ID (型 文字列 — CSV? JSON?); (c) hành vi khi chọn 0 phòng rồi OK; (d) BR003 dùng API_008 với 検索条件 nào. Hiện AI chọn (a) thay thế, (c) cho phép rỗng → ghi `A-08` trong pg-guide |
| Giới hạn / rủi ro | Mock không kiểm thử được 検索条件 và paging của BR003 thật. Nếu BR003 thật trả thêm/khác kiểu dữ liệu, chỉ sửa adapter của mock |

### D-02 BR_Com_005 一括予約エラー表示

| Mục | Nội dung |
|---|---|
| Màn/chức năng liên quan | BR_Com_005 一括予約エラー表示; BR004 cần cho 403 (エラーチェック No.1) |
| Căn cứ | BD004 エラーチェック一覧 No.1: 初期表示, ログインユーザの権限にシステム管理者が付与されていない → 一括予約エラー表示画面へ遷移する（403エラー）; メッセージ内容 "※一括予約エラー表示画面で定義". CTX: BD005 IN = ステータスコード (数値) từ mọi màn 一括予約; 403 → 「アクセス権限がありません。」; 400/404/409/500/504 cũng chuyển sang màn này, 422 thì không |
| Vị trí source liên quan | `ras-web/src/app/shared/guards/admin.guard.ts` (check `hasRole('Administrator')`, tạm `navigate(['/sample'])`); `shared/interceptors/api-error.interceptor.ts` (switch theo status, 422 bỏ qua); `shared/services/api-error-handler.service.ts` (mọi handler tạm `navigate(['/sample'])`, TODO thay bằng màn lỗi); backend `AuthorizationPolicies.AdministratorOnly`, `ApiAuthorizationResultHandler.cs`, `HttpGlobalExceptionFilter.cs` |
| Dữ liệu vào | `statusCode: number` (403; mock cũng nên nhận 400/404/409/500/504 vì interceptor chung sẽ gọi) |
| Dữ liệu ra | Không |
| Mức ảnh hưởng | **Thấp với luồng chính, Cao với rule R-001**: không có màn đích thì user không quyền vẫn bị chặn (guard trả false) nhưng rơi vào `/sample`, không chứng minh được "chuyển 403" |
| Cách xử lý dự kiến | **Mock route** (P-15) `error/:statusCode` hiển thị code; sửa đích `navigate` trong `AdminGuard` và `ApiErrorHandlerService` từ `/sample` sang route mock. Đây là sửa **shared** (ngoài feature folder) — cần user đồng ý vì ảnh hưởng mọi màn |
| Đã xác nhận | Điểm cắm đã có sẵn trong source (TODO ghi rõ); 422 do màn tự hiển thị (interceptor + CTX khớp nhau) |
| Còn cần điều tra / xác nhận với Serio | (a) 403 ở 初期表示 do guard frontend quyết hay phải gọi API rồi nhận 403 (AI chọn: guard chặn trước, API vẫn bảo vệ → `A-07`); (b) message 403 chính xác và `{0}` địa chỉ liên hệ cho 500/504 — mock không hiển thị message, chỉ code |
| Giới hạn / rủi ro | Mock không có message tiếng Nhật → test "message đúng" của BR005 nằm ngoài BR004. Nếu Serio yêu cầu BR005 thật thì thay component tại cùng route, không đổi guard |

### D-03 Quyền システム管理者 (auth / role)

| Mục | Nội dung |
|---|---|
| Căn cứ | BD004 機能概要 D11 利用者 = システム管理者; エラーチェック No.1; API一覧 r12–r13: API_004/005 利用可能ロール chỉ 1 dấu ○ (cột システム管理者), API_008 2 dấu ○ |
| Vị trí source | `AppRoles.Administrator = "Administrator"`, `AuthorizationPolicies.AdministratorOnly`; frontend `AuthService.getRoles()` đọc claim `roles` của id token, `AdminGuard` |
| Dữ liệu | Role string `Administrator` trong token Entra ID |
| Mức ảnh hưởng | **Cao**: không có role này thì không vào được màn, không gọi được API_004/005 |
| Cách xử lý | **Dùng trực tiếp**, không mock (`A-17`). API_004/005 gắn `[Authorize(Policy = AdministratorOnly)]`; API_008 `[Authorize]` (mọi user đã đăng nhập) |
| Cần xác nhận | Mapping システム管理者 ↔ `Administrator`, 社内ユーザ ↔ user đã login không role: là suy luận từ SRC, BD không ghi tên role kỹ thuật. Môi trường test có tài khoản mang role này không (PENDING readiness) |

### D-04 会議室マスタ (rooms_mst) — dữ liệu dùng chung

| Mục | Nội dung |
|---|---|
| Căn cứ | BD004 SELECT_001 (全項目, sort 会議室名 昇順), SELECT_002 join; SQL `rooms_mst` có `is_deleted` |
| Vị trí source | DDL `ras_tables.sql` r46–r69; chưa có entity/DbSet trong `RasDbContext` |
| Dữ liệu | Đọc: `id`, `room_name` (citext). BR004 không ghi |
| Mức ảnh hưởng | **Cao**: không có dữ liệu phòng thì màn trống |
| Cách xử lý | Dùng trực tiếp; seed dữ liệu test (`RasDbContextSeed.cs` hiện trống). Entity `Room` tạo trong BR004 nhưng đặt ở Domain dùng chung vì BR003/RM_Res cũng cần |
| Cần xác nhận với Serio | SELECT_001 không có 抽出条件 nhưng bảng có `is_deleted`: có lọc phòng đã xóa không? BD004 ghi なし → AI theo BD (không lọc) nhưng nên ghi thành giả định mới `A-19` |

### D-05 API_008 会議室マスタ一覧取得API — dùng chung với BR003

| Mục | Nội dung |
|---|---|
| Căn cứ | API一覧 r16: 利用機能 = 会議室検索 / 会議室タブレット登録; リクエスト = 会議室検索画面の検索条件 |
| Vị trí source | Chưa có controller. `PingController` là mẫu `[Authorize] [Route("private")]` |
| Dữ liệu | Request là **検索条件 của BR003** (BR004 không có điều kiện → gửi rỗng); response list 会議室マスタ |
| Mức ảnh hưởng | **Cao** cho 初期表示 |
| Cách xử lý | Implement trong BR004 với request DTO chấp nhận tất cả trường optional; contract thật của 検索条件 lấy từ BD003 khi có. Đây là điểm **tái sử dụng một phần**: BR003 thật sau này dùng lại endpoint, bổ sung filter |
| Cần xác nhận | Trường 検索条件 của BR003 (tên phòng? 場所?) — cần BD003 gốc |

### D-06 Common screen rules (画面共通仕様説明書, メッセージ一覧)

| Mục | Nội dung |
|---|---|
| Căn cứ | BD004 データアクセス定義 C6 (抽出条件 theo 画面共通仕様説明書); エラーチェック No.2 warning confirm, No.3 message với `{0}`; SRC có `ResxMessageManager`, `MessageResourceService`, `ValidationController`, `common-validators.ts` |
| Mức ảnh hưởng | **Trung**: ảnh hưởng validation chuỗi cấm (`A-12`) và ID message (P-07) |
| Cách xử lý | Tái dùng cơ chế message resource hai phía; literal theo BD004; ID message tạm theo quy ước repo (`E_9000007` kiểu trong `AuthController`) |
| Cần xác nhận | Hai workbook chưa có trong run (PENDING). Không phải phụ thuộc vào BR003/005 nhưng là phụ thuộc chung cần liệt kê |

### Không phải phụ thuộc (đã kiểm tra, loại)

| Ứng viên | Lý do loại | Căn cứ |
|---|---|---|
| BR_Com_002 社内ユーザ検索 | BR004 không mở; chỉ cùng pattern child screen với BR003 | CTX 画面遷移図 |
| 補足資料_データの整合性チェック (楽観排他 / version) | 会議室タブレット登録 là 例外機能 của check ②; check ① cần màn nguồn truyền version, BR004 vào từ menu | CTX; BD004 機能間引数定義 IN = なし（メニューリンク） |
| 採番ルール (会議予定番号) | BR004 chỉ dùng UUID nội bộ (`{新規採番したUUID}`), không dùng số hiển thị | BD004 INSERT_001 E48 |
| Tablet app WinUI (`Applications/Ras`), batch (`Batches`) | Tiêu thụ dữ liệu BR004 tạo nhưng là RM_Res, ngoài scope PoC | task.md Ngoài scope |
| `ErrorScreenNavigationService.cs` (WinUI) | Là màn lỗi của tablet app, không phải BR005 | SRC path `Applications/Ras/...` |

## 3. Phần tái sử dụng từ source hiện có

| Thành phần | Dùng cho | Cách dùng |
|---|---|---|
| `AdminGuard`, `AuthGuard` | R-001 (quyền màn) | Gắn `canActivate: [AuthGuard, AdminGuard]` cho route BR004; sửa đích redirect (D-02) |
| `apiErrorInterceptor` + `ApiErrorHandlerService` | 403/400/404/500 → BR005 mock | Chỉ đổi đích navigate |
| `ApiService`, `auth-token.interceptor`, `request-id.interceptor` | Gọi API_004/005/008 | Dùng nguyên |
| `select-box`, `text-input`, `search-icon-button`, `action-button`, `message-box`, `app-shell-layout` | Layout BR004 (項目定義 No.1–5) | Dùng nguyên; `search-icon-button` đã có `disabled` input |
| `checkbox-group` / `data-table` | Mock BR003 | Dùng nguyên |
| `bulk-reservation-layout-sample` | Mẫu bố cục `app-form-table`, `app-search-field` | Tham khảo class CSS, không copy logic |
| `AuthorizationPolicies.AdministratorOnly`, `ApiResponse<T>`, `ErrorResponse`, `HttpGlobalExceptionFilter`, validation attributes (`GuidFormat`, `RequiredInput`) | Controller/validator API_004/005 | Dùng nguyên |
| `AuditableEntity`, `IRepository`, `IUnitOfWork` (= `RasDbContext`), `AuditSaveChangesInterceptor` | Entity/repository 3 bảng | Kế thừa; audit columns tự điền |
| `ras_tables.sql` | Schema | Không sửa; map EF đúng tên cột |

## 4. Đề xuất xử lý tổng hợp

| # | Phụ thuộc | Quyết định đề xuất | Ai chốt |
|---|---|---|---|
| 1 | BR003 | Mock modal trong BR004 sau interface; contract theo D-01; thay thế danh sách khi OK | Reviewer G0 (`A-08`, `A-14`) |
| 2 | BR005 | Mock route nhận status code; **sửa 2 file shared** để trỏ vào | User (vì sửa shared) |
| 3 | Role | Dùng thật, `Administrator` = システム管理者 | Reviewer G0 (`A-17`) |
| 4 | rooms_mst / API_008 | Implement trong BR004, DTO request mở để BR003 dùng lại | Dev BR003 sau này |
| 5 | `is_deleted` trong SELECT_001 | Theo BD (không lọc), ghi giả định mới | Reviewer G0 |
| 6 | BD003/BD005 gốc | Yêu cầu user đưa vào run để thay CTX | User |

## 5. Việc tiếp theo

- Thêm `A-19` (is_deleted) vào pg-guide nếu reviewer đồng ý.
- Khi user đưa BD003/BD005 gốc: đối chiếu lại D-01/D-02, cập nhật source-manifest.
- Mục "cần xác nhận với Serio" ở trên **không** phải Q&A do agent gửi; agent đã chọn phương án và ghi `A-xx`. Người review quyết định có đưa cho Serio hay không.
