# PG implementation BR_Com_004

## Metadata

| Item | Value |
|---|---|
| Repository | `D:\Serio-AI\serio-ras` (reactplus-f1/serio-ras), branch `bd-to-pg` (branch đang checkout; user chưa chỉ định branch riêng) |
| Code commit | — (user tự commit trên `bd-to-pg`; SHA không bắt buộc theo quyết định user 2026-10-16) |
| Build/lint commands and evidence | Backend: `dotnet build src\Services\Ras\RasApi\RasApi.csproj` (từ `ras-system`) → **Build succeeded, 0 error**, 19 warning đều có sẵn trước thay đổi (NU1902/NU1903, CS0618, CS8625…; không warning nào ở file mới). Frontend: `npx ng build --configuration development` → **bundle generation complete, 0 error**. `npm run build` (production) compile OK nhưng fail budget `initial > 1.20 MB` (1.47 MB) — vượt budget đã có sẵn trước thay đổi (file mới chỉ vài KB). `npm run lint` không chạy được do lỗi cấu hình có sẵn: rule `@angular-eslint/template/prefer-style-binding` không tồn tại trong plugin đã cài. Sau review 2.4 (2026-10-17): `dotnet test src\Services\Ras\RasApi.ComponentTests\RasApi.ComponentTests.csproj --artifacts-path %TEMP%\ras-artifacts` (từ `ras-system`) → **13/13 Passed**, exit 0 (dùng artifacts-path vì BE đang chạy khóa bin). Convention check (2026-10-19, file đã sửa so với `main`): `dotnet format --verify-no-changes --severity warn` → sửa vi phạm do PG tạo (dòng 1 LF ở `Room.cs`/`Tablet.cs`/`CandidateRoom.cs`; IDE0005 `using RasApi.Shared.Constants` thừa trong `Startup.cs`); còn lại có sẵn trên main: IMPORTS ordering (`Startup.cs`, `RasDbContext.cs`), FINALNEWLINE (`AppRoles.cs`, `AuthorizationPolicies.cs`). `prettier --check --end-of-line crlf` → format 6 file FE do PG tạo/sửa; còn lại dòng có sẵn trên main (`app.routes.ts` route bulk/redirect, `admin.guard.ts`, `api-error-handler.service.ts`). ESLint (config tạm ngoài repo, bỏ rule lỗi) → sửa a11y backdrop mock BR_Com_003 (`tabindex="-1"`, `(keydown.escape)`), exit 0. `tsc --noEmit` exit 0; `ng build` dev exit 0; `dotnet test` 13/13 Passed. Sau đối chiếu コーディング規約/PG_ルール và refactor (2026-10-19, xem mục Tuân thủ): `dotnet build` ComponentTests → Build succeeded (warning có sẵn); `dotnet test` → **16/16 Passed** (thêm 3 test AutoMapper); `dotnet format --verify-no-changes --severity warn --include <26 file .cs đã sửa>` exit 0; `prettier --check --end-of-line crlf` file FE mới exit 0; ESLint (config tạm, bỏ rule lỗi) exit 0; `tsc -p tsconfig.app.json --noEmit` exit 0; `ng build --configuration development` exit 0. |

Code commit là tùy chọn: user tự commit; ghi SHA nếu user cung cấp, không dùng để khóa baseline.
Không có Test commit tại G1 vì Testspec và UT code là công đoạn sau. Agent không commit/push.

## Changes

Đường dẫn backend tương đối từ `ras-system/src/Services/Ras/`, frontend từ `ras-web/src/app/`.

| Module ID | File / function | Rule IDs | Source / decision | Impact / regression |
|---|---|---|---|---|
| P-01 | `RasDomain/Models/Room.cs`, `Tablet.cs` (`CreateNew`, `UpdateMachineId`), `CandidateRoom.cs` (`Create`) | R-006, R-017, R-018, R-019, R-021 | テーブル設計書 (会議室マスタ/タブレット管理マスタ/タブレット延長候補会議室マスタ); `Entity<Guid>`/`AuditableEntity` có sẵn | Mới; không ảnh hưởng code cũ. `CandidateRoom` kế thừa `AuditableEntity` (không có Id đơn) vì PK ghép |
| P-02 | `RasInfrastructure/RasDbContext.cs` (3 DbSet + ApplyConfiguration), `EntityConfigurations/{Room,Tablet,CandidateRoom}EntityTypeConfiguration.cs` | R-006, R-020, R-021 | テーブル設計書: UNIQUE machine_id, PK (tablet_id, room_id), FK | Sửa file dùng chung `RasDbContext` (chỉ thêm, không đổi hành vi cũ). Bảng ở schema public, không dùng `DEFAULT_SCHEMA` |
| P-03 | `RasDomain/Repositories/IRoomRepository.cs` (`GetAllOrderedByNameAsync`), `ITabletRepository.cs` (`GetByRoomIdWithCandidatesAsync`, `FindRoomByMachineIdExcludingRoomAsync`, `Create`, `UpdateCandidateRooms`) | R-002, R-006, R-015, R-018, R-019, R-020, R-021 | pg-guide P-03; コーディング規約 B2-8 (động từ Create/Update) | Mới. **Lệch kế hoạch**: `DeleteCandidatesByTabletIdAsync` + `AddCandidatesAsync` gộp thành `UpdateCandidateRooms` (xem Deviations D-1) |
| P-04 | `RasInfrastructure/Repositories/RoomRepository.cs` (SELECT_001), `TabletRepository.cs` (SELECT_002/003, SELECT_004 check No.3, INSERT_001, DELETE_001+INSERT_002) | R-002, R-006, R-015, R-018, R-020, R-021 | BD004 データアクセス定義 | Mới. SELECT_001 không filter `is_deleted` (A-19) |
| P-05 | `RasUseCase/ViewModels/RoomsMstOutput.cs`, `CandidateRoomOutput.cs`, `TabletInfoOutput.cs`, `SaveTabletInfoInput.cs` (1 class/file) | R-007, R-008, R-027 | pg-guide P-05; PG_ルール 開発手順書（API） (UseCase ViewModel `XxxOutput`) | Mới |
| P-06 | `RasUseCase/Services/ITabletInfoService.cs`, `TabletInfoService.cs` (`GetRoomsMstListAsync`, `GetTabletInfoAsync`, `SaveTabletInfoAsync`) | R-015, R-016, R-017, R-018, R-019, R-020, R-021, R-022, R-023, R-024 | BD004 イベント定義/エラーチェック一覧; A-02…A-06, A-13, A-15, A-18 | Mới. Transaction R-023 = một `SaveChangesAsync` duy nhất (EF Core bọc trong 1 DB transaction); không mở transaction tường minh (D-2) |
| P-07 | `ras-system/src/BuildingBlocks/Common/Util/Resources/Messages.resx` key `E_BRCOM004_001`; `ras-web/src/assets/i18n/ja.json` keys `message.tabletRegistration.confirmRegister`, `message.tabletRegistration.registered`, nhóm `tabletRegistration.*` (label) | R-014, R-015, R-024 | BD004 エラーチェック一覧 G8:G9, イベント定義 F20 (literal nguyên văn) | Sửa file dùng chung (chỉ thêm key). ID message tạm `E_BRCOM004_001` vì メッセージ一覧 chưa có (D-3) |
| P-08 | `RasApi/Controllers/TabletInfoController.cs` (`GetTabletInfoAsync` `GET private/tablet-info/{roomId}` API_004, `SaveTabletInfoAsync` `POST private/tablet-info` API_005; policy `AdministratorOnly`), `RoomsController.cs` (`GetRoomsMstListAsync` `POST private/rooms-mst-list` API_008; policy `InternalUserOrAdministrator` — sửa sau review 2.4). Controller inject `IMapper`, trả API Response (không trả UseCase ViewModel) | R-025, R-027 | API一覧 B12:K13, B16:K16 (G6:H6, G16:H16 利用可能ロール); PG_ルール 開発手順書（API） | Mới. API_004 trả `data = null` khi không có tablet (200, không 404) để frontend clear theo R-009. 422 qua `CreateFailResponse` có sẵn. JSON contract không đổi khi refactor |
| P-09 | `RasApi/ViewModels/SaveTabletInfoRequest.cs` (`RequiredInput`+`GuidFormat` RoomId, `IValidatableObject` cho từng `CandidateRoomIds[i]`), `RoomsMstListRequest.cs` (rỗng), `RoomsMstResponse.cs`, `CandidateRoomResponse.cs`, `TabletInfoResponse.cs` | R-017, R-026 | pg-guide P-09; コーディング規約 B2-9 (`{Data}Request/Response`) | Mới. **R-026 (chuỗi cấm) chưa implement**: repo chưa có validator chung và 画面共通仕様 chưa được cung cấp (D-4) |
| P-10 | `RasApi/Startup.cs` (`AddScoped` IRoomRepository/ITabletRepository/ITabletInfoService trong `if (IsDatabaseEnabled)`) | R-002, R-006, R-015, R-025 | Pattern DI inline của Startup | Sửa file dùng chung (thêm 3 dòng + 3 using). Khi `Database:Enabled=false` controller mới sẽ không resolve được → 500 (giống các service DB khác) |
| P-11 | `features/br-com-004/components/br-com-004.component.{ts,html,css}` (`BrCom004Component`, selector `app-br-com-004`), `features/br-com-004/interfaces/candidate-room-view-model.interface.ts` | R-002, R-003, R-004, R-005, R-007, R-008, R-009, R-010, R-028 | BD004 項目定義, 画面表示定義; A-11, A-13; PG_ルール 開発手順書（Angular） | Mới. Route `BrCom004`. Separator `;` lấy từ `Constants.separator.trim()` (D-5) |
| P-12 | `shared/services/rooms-mst.service.ts` (`getRoomsMstList`), `shared/services/tablet-info.service.ts` (`getTabletInfo`, `saveTabletInfo`), `shared/interfaces/{rooms-mst-response,candidate-room-response,tablet-info-response,save-tablet-info-request}.interface.ts` | R-002, R-006, R-024, R-027 | API一覧; PG_ルール (API service/interface đặt ở `shared`) | Mới; dùng `ApiService` chung |
| P-13 | `br-com-004.component.ts`: `onClickRegisterButton` (warning confirm), `onMessageAnswered` (C-011), `saveTabletInfo()` (422 → `errorMessages` đỏ dưới title; success → message-box success + `getTabletInfo`) | R-014, R-015, R-024 | BD004 エラーチェック一覧 No.2/No.3; A-04, A-09 | Mới; dùng `app-message-box` chung (`answered` output) |
| P-14 | `app.routes.ts` (route `BrCom004` với `[AuthGuard, AdminGuard]`), `shared/components/app-shell-layout/app-shell-layout.component.ts` (menu map `'BRCom004'` → `'BrCom004'`),  `shared/guards/admin.guard.ts` (navigate `['/error', 403]`), `shared/services/api-error-handler.service.ts` (mọi handler navigate `['/error', error.status]`) | R-001 | BD004 エラーチェック一覧 No.1; A-07; dependency-analysis D-02 | **Sửa shared**: thay 2 TODO "tạm chuyển /sample" bằng điều hướng tới mock BR_Com_005. Ảnh hưởng mọi màn khi API trả 400/401/403/404/409/500/504 (trước đây về /sample) |
| P-15 | `features/br-com-005/components/br-com-005-mock.component.{ts,html,css}` (`BrCom005MockComponent`); route `error/:statusCode` | R-001 | A-07; dependency-analysis D-02 | **Mock** BR_Com_005: chỉ hiển thị status code |
| P-16 | `features/br-com-003/components/br-com-003-mock.component.{ts,html,css}` (`BrCom003MockComponent`), `features/br-com-003/interfaces/room-search-input.interface.ts` (`RoomSearchInput {roomIds, rankSelectable}`), `room-search-result-item.interface.ts` (`RoomSearchResultItem`) | R-011, R-012, R-013 | BD004 画面遷移定義 C6:D10; A-08, A-14; dependency-analysis D-01 | **Mock** BR_Com_003: modal checkbox dùng danh sách API_008 do màn cha truyền vào; OK → `selected` (0 件可), Cancel → `cancelled` |
| P-17 | — | — | pg-guide P-17 | Không tạo project test mới: `RasApi.UnitTests` đã tồn tại và build không yêu cầu |
| P-18 | `RasApi/Infrastructure/Authorization/AuthorizationPolicySetup.cs` (đăng ký policy `AdministratorOnly`, `InternalUserOrAdministrator`), `Shared/Constants/AppRoles.cs` (`InternalUser`), `Shared/Constants/AuthorizationPolicies.cs`, `Startup.cs` (`AddAuthorization(AuthorizationPolicySetup.Configure)`) | R-025 | API一覧 G16:H16; A-20; review 2.4 | Sửa shared auth: tách đăng ký policy khỏi Startup để test dùng chung. User đã login nhưng không có role `InternalUser`/`Administrator` → API_008 trả 403 (trước: 200) |
| P-19 | `RasApi.ComponentTests/Authorization/ApiRoleAuthorizationTests.cs` (13 test) | R-025, C-014 | review 2.4 | Test phân quyền theo yêu cầu review (sớm hơn S6): chưa đăng nhập → Challenge (401); đăng nhập không role / role khác → Forbid (403); role được phép → thành công; handler trả 403 chung. Case chính thức vẫn lập ở S4 |
| P-20 | `RasApi/Mapper/TabletInfoProfile.cs` (Output→Response, `SaveTabletInfoRequest`→`SaveTabletInfoInput` với `Guid.Parse`); `RasApi.ComponentTests/Mapper/TabletInfoProfileTests.cs` (3 test) | R-017, R-027 | PG_ルール 開発手順書（API） 8. Mapper実装 | Mới; Profile tự đăng ký qua `AddAutoMapper(...AddMaps)` có sẵn trong Startup |
### Deviations / assumptions mới ở S2

| ID | Nội dung | Lý do | Ảnh hưởng |
|---|---|---|---|
| D-1 | DELETE_001 + INSERT_002 thực hiện bằng `UpdateCandidateRooms` (xóa dòng không còn trong danh sách, thêm dòng mới) thay vì xóa hết rồi insert lại | EF Core không cho phép Deleted + Added cùng khóa (tablet_id, room_id) trong một context; kết quả cuối trong DB giống BD (tập candidate = danh sách gửi lên) | S4 cần case: candidate giữ nguyên / bỏ / thêm. Audit `update_at` của dòng giữ nguyên không đổi |
| D-2 | Transaction R-023 dựa trên một `SaveChangesAsync` (EF Core tự bọc transaction) | Repo không có helper transaction; UseCase không tham chiếu Infrastructure | Không có bước ghi nào ngoài SaveChanges → vẫn all-or-nothing |
| D-3 | Message ID backend `E_BRCOM004_001`, i18n key `message.tabletRegistration.*` | メッセージ一覧 chưa được cung cấp | Đổi ID khi có メッセージ一覧 |
| D-4 | R-026 (chuỗi cấm, Required = NO) **chưa implement** | Không có validator chung trong repo, 画面共通仕様 (regex/chuỗi cấm) chưa có | Bổ sung khi có spec; S4 không lập case C-015 |
| D-5 | Separator hiển thị `;` (không khoảng trắng) dù `Constants.separator = '; '` | BD 項目定義 I10 ghi `;`; pg-guide R-008; dependency-analysis §4 | Nếu Serio chọn `'; '` → bỏ `.trim()` |
| A-19 | SELECT_001 không lọc `is_deleted` | BD không có điều kiện; dependency-analysis §4 đề xuất | Nếu cần lọc → thêm `Where(!IsDeleted)` ở `RoomRepository` |
| D-6 | API_004 trả 200 `data: null` khi không có タブレット管理マスタ | BD イベント定義 F10 "データが取得できない場合は値をクリア" → không phải lỗi | Frontend xử lý `data == null` |
| D-7 | API_008 nhận body `RoomsMstListRequest` rỗng, bỏ qua điều kiện tìm kiếm | Điều kiện là của BR_Com_003 (ngoài scope) | BR_Com_003 bổ sung field sau |
| A-20 | Role 社内ユーザ map tới app role `InternalUser` | Repo chỉ có `Administrator`; API一覧 API_008 cho 社内ユーザ + システム管理者; QA No.15 | Đổi hằng `AppRoles.InternalUser` khi Serio trả lời |
| D-8 | AdminGuard/ApiErrorHandlerService chuyển tới `/error/{status}` cho **mọi** status (không chỉ 403) | Thay thế TODO có sẵn, một đích cho mock BR_Com_005 | Hành vi màn sample khi lỗi API thay đổi (trước: về /sample) |
| D-9 | Route mock BR_Com_005 giữ `error/:statusCode` (không theo dạng `BrCom005`) | Contract D-02 đã dùng ở `admin.guard`/`api-error-handler`; BR_Com_005 thật sẽ quyết định route | Đổi đồng thời guard/handler khi có BR_Com_005 |

## Tuân thủ コーディング規約 / PG_ルール (2026-10-19)

Nguồn: CODE01 【RAS】コーディング規約.xlsx Ver 1.00, PGR01 【RAS】PG_ルール.xlsx (source-manifest). Chi tiết rule: `.agents/workflow/rules/CODING_RULES.md`.

| Hạng mục | Trước | Sau |
|---|---|---|
| Comment `//` kết thúc 「。」 (B7, F7) | 23 chỗ thiếu | Đã sửa toàn bộ trong file PG tạo/sửa (còn comment có sẵn ở `Startup.cs` main, ngoài scope) |
| XML doc / JSDoc cho member (B7, F7) | 18 member thiếu | Đã bổ sung (`<inheritdoc />` cho override/implement) |
| Hậu tố `Async` cho action/method async (B2) | Action controller thiếu | `GetTabletInfoAsync`, `SaveTabletInfoAsync`, `GetRoomsMstListAsync` |
| Động từ method (B2-8, F5-9) | `Add`, `ReplaceCandidateRooms`, `loadRooms`, `register`… | `Create`, `UpdateCandidateRooms`, `getRoomsMstList`, `saveTabletInfo`, `initializeTabletFields` |
| Tên handler FE (F5-8) + `protected` (F5-5) | `onRoomChange`, `onRegisterClick`, `onOk`… public | `onChangeRoom`, `onClickRegisterButton`, `onClickOkButton`… protected |
| Controller trả UseCase ViewModel; không có Mapper | Có | API Request/Response riêng + AutoMapper Profile (P-20) |
| Thư mục/route FE theo screen ID | `features/tablet-registration`, route `BRCom004` | `features/br-com-004`, route `BrCom004`; mock `br-com-003`, `br-com-005` |
| API service/interface FE ở `shared` | Trong feature | `shared/services`, `shared/interfaces` (1 interface/file) |

Giữ nguyên theo repo (ghi ở CODING_RULES "Thứ tự áp dụng khi xung đột"): block namespace C# (B3-6), field `_camelCase` (B2-2), vị trí JSDoc giữa decorator và class, branch `bd-to-pg`, route mock `error/:statusCode` (D-9).

## Branch and condition inventory

| Condition ID | Vị trí code | Nhánh |
|---|---|---|
| C-001 | `admin.guard.ts` `hasRole('Administrator')` | T: return true / F: navigate `/error/403` |
| C-002 | `br-com-004.component.html` `@if (!isRoomUnselected)` ×2 (nút 登録, search icon) | T (未選択): ẩn / F: hiển thị |
| C-003 | `br-com-004.component.html` `[disabled]="isRoomUnselected"` | T: disabled / F: enabled |
| C-004 | `br-com-004.component.ts` `getTabletInfo` `if (!data)` | T: set machineId/candidates / F: `initializeTabletFields` |
| C-005 | `TabletInfoService.GetTabletInfoAsync` `CandidateRooms.Where(Room != null)…OrderBy`; FE `candidateRoomsText` join `;` | T: chuỗi tên / F: rỗng |
| C-006 | `TabletInfoService.SaveTabletInfoAsync` `string.IsNullOrWhiteSpace(input.MachineId)` | T: machineId = null, bỏ qua check / F: check trùng |
| C-007, C-008 | `TabletRepository.FindRoomByMachineIdExcludingRoomAsync` (`MachineId == machineId && RoomId != excludeRoomId`); service `if (otherRoom is not null)` | T: `Result.Fail(E_BRCOM004_001, roomName)` → 422 / F: tiếp |
| C-009 | `TabletInfoService.SaveTabletInfoAsync` `if (tablet is null)` | T (null): `Tablet.CreateNew` + `Create` / F: `UpdateMachineId` |
| C-010 | `TabletRepository.UpdateCandidateRooms` `toRemove`/`toAdd` | danh sách rỗng → xóa hết, không thêm |
| C-011 | `br-com-004.component.ts` `onMessageAnswered(accepted)` | T: `saveTabletInfo()` / F: return |
| C-012 | `br-com-003-mock.component.ts` `onClickOkButton` → `selected` / `onClickCancelButton` → `cancelled`; cha `onRoomSearchSelected` / `onRoomSearchCancelled` | T: thay candidates / F: giữ nguyên |
| C-013 | `TabletInfoService.SaveTabletInfoAsync` `SaveChangesAsync` | Exception → không commit → global filter 500 |
| C-014 | `TabletInfoController` `[Authorize(Policy = AdministratorOnly)]`; `RoomsController` `[Authorize(Policy = InternalUserOrAdministrator)]`; policy ở `AuthorizationPolicySetup` | chưa login: 401 / sai role: 403 (`ApiAuthorizationResultHandler`) / đúng role: tiếp |
| C-015 | — | **Chưa implement** (D-4) |
| (FE 422) | `br-com-004.component.ts` `saveTabletInfo().error` `if (error?.status === 422)` | T: `errorMessages` / F: để interceptor xử lý |
| (API validation) | `SaveTabletInfoRequest` RoomId required+GUID; `Validate()` từng CandidateRoomIds | fail → 400 qua `AddValidationBehavior` |

Giới hạn real/mock: BR_Com_003 và BR_Com_005 là mock (P-15, P-16); auth dùng Entra ID thật của repo (A-17), chưa chạy end-to-end với DB thật ở S2 (chỉ build).
