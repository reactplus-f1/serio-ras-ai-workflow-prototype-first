# Coding rules đã tổng hợp

Tổng hợp từ `【RAS】コーディング規約.xlsx` (Ver 1.00, 2026-06-29, sheet コーディング規約(Angular)
F1–F9 và コーディング規約(C#) B1–B9), `【RAS】PG_ルール.xlsx` (sheet PGルール, 開発手順書（API）,
開発手順書 (Angular)) và config thật của repo RAS (`.editorconfig`, `eslint.config.js`, Prettier,
`tsconfig.json`) tại 10/2026. Rule ID (F*/B*) giữ nguyên để trích dẫn:
`[SRC: 【RAS】コーディング規約.xlsx | コーディング規約(C#) | B2-4]`. Bản này là tra nhanh; khi
cần xác nhận câu chữ, mở file gốc user đưa (lưu ở `runs/<ID>/inputs/`).

## Thứ tự áp dụng khi xung đột

1. Config analyzer/formatter thật của repo (EditorConfig IDE*, ESLint, Prettier) — B9, F8.
2. Nhất quán với file/feature đang sửa (F1, F7-1): không đổi style code cũ; đổi style lớn tách PR.
3. コーディング規約 → PG_ルール 開発手順書 → rule này.

Xung đột đã biết (ghi vào pg-implementation, không tự refactor):

| Điểm | Quy định | Thực tế repo | Áp dụng |
|---|---|---|---|
| Private field | B2-2 camelCase | EditorConfig IDE1006 + ví dụ PG_ルール: `_camelCase` | `_camelCase` (theo B9/IDE1006) |
| Namespace | B3-6 file-scoped khi có thể | Toàn bộ code main dùng block namespace | Block namespace (F7/nhất quán); IDE0161 info không coi là vi phạm |
| JSDoc vị trí | Google TS: JSDoc trước decorator | Shared component đặt JSDoc giữa decorator và class | Theo repo |
| Spec file | F2-2 không tạo spec | Ví dụ PG_ルール Angular có `*.component.spec.ts` | Không tạo spec (F2-2) |
| Branch | PGルール: không tạo nhánh làm việc, chỉ main | Run dùng nhánh do user chỉ định | Theo user; agent không thao tác Git |

## Trạng thái nguồn

PGルール!D10,D13,D74:E77: UTF-8, CRLF, phân tích tĩnh không còn warning trước commit.
Coding convention: theo `【RAS】コーディング規約.xlsx` (PGルール!C57:C58 tham chiếu).

## Format theo phạm vi file

| Phạm vi | Quy tắc |
|---|---|
| Backend (ras-system) | UTF-8; CRLF; final newline; bỏ trailing whitespace; indent 4 |
| C# | Indent 4; brace xuống dòng; luôn dùng brace; System using trước và ngoài namespace |
| Project/JSON/YAML/XML, JS/TS/CSS/HTML trong backend | Indent 2 |
| .sh | LF |
| Markdown backend | Không trim trailing whitespace, không giới hạn line length |
| Frontend (ras-web) | UTF-8; indent 2; final newline; trim trailing whitespace; Markdown giữ trailing whitespace |
| TypeScript | Single quote; Prettier singleQuote=true, printWidth=100 |
| HTML | Prettier parser angular |

Frontend editorconfig không khai báo end_of_line; PG rule đặt CRLF làm baseline, ghi căn cứ
khi áp dụng. Không đổi hàng loạt format file cũ; không sửa config gốc để loại warning.

## C# (コーディング規約(C#))

| ID | Quy định |
|---|---|
| B1 | Dùng tính năng C# ổn định mới; không nuốt exception; I/O dùng async |
| B2-1/3 | Type/method/property/const PascalCase; interface `I` + PascalCase; local/parameter camelCase |
| B2-4 | Method async có hậu tố `Async` (kể cả action của Controller) |
| B2-5 | Không viết tắt vô nghĩa |
| B2-6 | Động từ đầu method: Get/Find/Create/Update/Save/Delete/Validate/Check/Initialize |
| B2-7 | bool (method/biến/property) bắt đầu bằng Is/Can/Has/Exists |
| B2-8 | Event handler `OnClickXxx` |
| B2-9 | ViewModel tầng Presentation (RasApi) kết thúc `{Data}Request` / `{Data}Response` (Data: ○○Mst, ○○Info…) |
| B3-1..5 | Indent 4; Allman brace; 1 câu lệnh/khai báo mỗi dòng; dòng trống giữa member; using ngoài namespace |
| B4 | `var` chỉ khi type hiển nhiên; `?.`/`??`; pattern matching; initializer/collection expression; string interpolation; `using` declaration; static member gọi qua tên type |
| B5 | Comment tiếng Nhật, ghi ý đồ; câu kết thúc bằng 「。」 (kể cả `//` cuối dòng); XML doc (`summary`/`param`/`returns`) cho class, method (kể cả constructor), property; implementation dùng `/// <inheritdoc />` |
| B6 | Tránh `catch (Exception)`; rethrow bằng `throw;` |
| B7 | Trả `Task`/`Task<T>`; không `async void`; truyền `CancellationToken` tới I/O; `ConfigureAwait(false)` trong library |
| B8 | Validate input; không để secret trong code |
| B9 | Analyzer qua EditorConfig: IDE0011/0049/0055/0065/0090/1006 ở mức warning. Giữ severity thật; CS8618 silent không chứng minh nullable đúng |

## Angular/TypeScript (コーディング規約(Angular))

| ID | Quy định |
|---|---|
| F2-1/5 | Tên file kebab-case; ts/html/css cùng base name; F2-2 không tạo spec |
| F2-3/4 | Tên class khớp nội dung file; không đặt helpers/utils/common |
| F2-6/7 | Type PascalCase; member camelCase; F2-8 request header Pascal-Kebab-Case |
| F3 | Folder theo feature; 1 file 1 khái niệm |
| F4-1 | DI bằng `inject()` |
| F5-1 | Selector prefix `app` |
| F5-2 | Member Angular (DI, input, output, query) ở đầu class |
| F5-3/4 | Logic không thuộc UI đưa vào service; biểu thức template phức tạp chuyển sang TS |
| F5-5 | Member chỉ dùng trong template là `protected` (kể cả event handler) |
| F5-6 | `readonly` cho input/output/model/query |
| F5-7 | `[class]`/`[style]` binding thay `ngClass`/`ngStyle` |
| F5-8 | Event handler đặt theo sự kiện: `onClickXxxButton`, `onChangeXxx` |
| F5-9 | Động từ method: get/find/create/update/save/delete/validate/check/initialize |
| F5-10/11 | Lifecycle hook mỏng, gọi method có tên rõ; class implements interface hook |
| F5-12 | input/output dạng signal |
| F6 | Comment tiếng Nhật, ghi ý đồ; `//` kết thúc 「。」; JSDoc cho Component/Directive/Pipe/Service/Guard/Resolver/Interceptor và public method/property; tránh comment HTML |
| F7 | File cũ theo style hiện có; đổi style lớn tách PR riêng |
| F8/F9 | Google TypeScript Style Guide; best practice Angular về security, a11y, performance |

Repo: TypeScript strict + strict templates (không tắt để build đạt); Prettier singleQuote,
printWidth 100; ESLint của repo chọn rule cụ thể, không giả định toàn bộ recommended đã bật.

## PG_ルール 開発手順書 (cấu trúc code)

API (開発手順書（API）): Domain Model `RasDomain/Models` → DbContext (không dùng EF migration;
DDL ở `ras-system/sql/ras_tables.sql`) → Repository interface `RasDomain/Repositories` (UnitOfWork) →
Repository `RasInfrastructure/Repositories` → UseCase ViewModel `RasUseCase/ViewModels`
(ví dụ `MeetingRoomOutput`) → UseCase Service (gọi `SaveChangesAsync()` 1 lần cho 1 thao tác) →
API Request/Response `RasApi/ViewModels` (ví dụ `GetMeetingRoomResponse`) → **AutoMapper Profile
theo nghiệp vụ** `RasApi/Mapper/<Nghiệp vụ>Profile.cs` (UseCase ViewModel ⇔ API ViewModel) →
Controller → DI trong Startup.

- URI chữ thường, nối bằng `-`; update dùng PATCH (không PUT); 1 API = 1 thao tác màn hình.
  Method/URI theo API一覧 khi đã có.
- Property request body khai báo `string?`, kiểm tra bằng attribute
  `RasApi.Infrastructure.Validation.Attributes` (`[RequiredInput]`, `[GuidFormat]`, `[DateFormat]`,
  `[TimeFormat]`, `[NumericFormat]`, `[PastDate]`); format attribute cho qua null/rỗng nên phải
  kèm `[RequiredInput]` nếu bắt buộc.
- Controller không trả trực tiếp ViewModel của UseCase; map sang Response của RasApi.

Angular (開発手順書 (Angular)): component `features/<screen-id>/components/<screen-id>.component.*`
(ví dụ `br-com-005`); route `path: 'BrCom005'` với `canActivate: [AuthGuard, AdminGuard]` khi cần
quyền; Request/Response interface ở `shared/interfaces`, interface hiển thị ở
`features/<screen-id>/interfaces`; service gọi API ở `shared/services` (component không gọi
HttpClient); label/message ở `assets/i18n/ja.json`; validate bằng `shared/validators`.

## Checklist review thủ công (tool không bắt)

Sau lệnh verify ở mục dưới, đọc lại các file PG thêm/sửa và tick: 「。」 cuối comment (B5/F6);
XML doc/JSDoc đủ (B5/F6); hậu tố `Async` (B2-4); động từ method (B2-6/F5-9); tên handler (F5-8);
`protected` cho member template (F5-5); hậu tố Request/Response và tầng đặt ViewModel (B2-9,
開発手順書); AutoMapper Profile; `string?` + validation attribute; vị trí folder/route/shared
(開発手順書 Angular); `catch (Exception)`, `async void`, `CancellationToken`.

`npm run lint` / `dotnet build` chỉ chạy khi được phép; báo warning/error của đúng commit.
PASS lint không chứng minh convention đầy đủ, nghiệp vụ hay coverage.

## Kiểm tra convention trên file đã sửa (bắt buộc ở S2)

Chạy trên **đúng các file đã sửa/thêm** (`git diff --name-only <base>...HEAD` + working tree),
không chạy format toàn repo:

| Phạm vi | Lệnh (chỉ verify, không ghi) |
|---|---|
| C# | Tại `ras-system/src`: `dotnet format Ras.sln --verify-no-changes --severity warn --include <path tương đối từ src>` (path tuyệt đối sẽ không khớp và báo PASS giả) |
| TS/HTML | Tại `ras-web`: `npx prettier --check --end-of-line crlf <files>`; `npx tsc -p tsconfig.app.json --noEmit` |
| ESLint | `npx eslint <files>`; nếu config repo lỗi, dùng config tạm **ngoài repo** chỉ bỏ rule lỗi, ghi rõ trong pg-implementation |
| EOL/encoding | CRLF thống nhất cả file (kể cả dòng 1), UTF-8 không BOM, có newline cuối file |

Phân loại mỗi vi phạm: **do PG tạo** (dòng PG thêm/sửa, so với `git show <base>:<file>`) →
sửa trước G1; **có sẵn trên base** → không sửa, ghi vào pg-implementation. Khi ghi lại file bằng
formatter, hoàn tác các hunk chỉ đổi dòng có sẵn. Cảnh báo info (IDE0161, IDE0008…) trùng
style hiện tại của repo không coi là vi phạm.
