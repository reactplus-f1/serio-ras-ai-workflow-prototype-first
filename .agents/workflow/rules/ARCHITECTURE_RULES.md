# Quy tắc kiến trúc và API

Tổng hợp từ `【RAS】APアーキテクチャ設計.xlsx` (sheet 4.レイヤー構成, 6.API設計方針,
7.ログ出力方針, 8.エラーハンドリング, 9.データアクセス設計方針) và
`【RAS】PG_ルール.xlsx` (sheet 開発手順書（API）), đối chiếu shared code của repo RAS khi tổng
hợp. Khi cần xác nhận một ô, yêu cầu user đưa workbook.

## Layer và dữ liệu

- Controller/Presentation: HTTP, quyền, input format. UseCase: workflow/transaction,
  DTO/Result. Domain: nghiệp vụ/interface. Infrastructure: EF/Repository/adapter. Tái dùng
  layer/shared code hiện có; không đưa DB logic vào UI.
- Thứ tự PG API (開発手順書): entity → DbContext → repository interface/implementation →
  UseCase DTO/service → Controller → DI/mapping/validation. Tên lớp/schema/endpoint theo
  BD/API一覧 và repo thật; không lấy tên mẫu (MeetingRoom/Employee/FeatureA) làm quy định.
- Mỗi thao tác ghi là một transaction, boundary tại UseCase (9.データアクセス設計方針!C30:C31).
  Giữ audit fields và mapping đã chốt; không bật concurrency mọi bảng chỉ từ ví dụ.
- PostgreSQL qua EF Core/Npgsql, citext. Schema mặc định trong DbContext hiện có là giá trị
  khung, cần đối chiếu; không mặc định cho PoC.

## HTTP contract và quyền

- Envelope chung `ApiResponse<T>`: `data` khi thành công, `errors` khi lỗi; mỗi error có
  `field`/`message`. Dùng contract/helper/messages hiện có, không tạo wrapper mới.
- Status chung (6.API設計方針, 8.エラーハンドリング): 400 format, 401 authentication,
  403 authorization, 404 missing, 409 concurrency, 422 business error/warning, 500 system,
  504 timeout. Request/response/role riêng từng API theo BD và API一覧.
- Business failure dùng Result/ResultMessage; presentation giải message/status. Lỗi hệ
  thống qua global filter. Không bắt mọi Exception rồi trả thành công.
- API bảo vệ bằng Entra ID và policy theo vai trò. Guard frontend chỉ là UX, không thay
  kiểm tra backend. Không bypass auth để demo; real/mock auth phải nằm trong scope đã chốt.
- Warning/confirmation theo contract chung và BD; kiểm tra semantics của ignore-warning/
  cancel trong ApiService trước khi tái dùng, không dùng để bỏ error.

## Logging và shared services

- Tái dùng request ID/interceptor, logger, common messages/resources, API services
  (7.ログ出力方針). Log đủ context để tái hiện lỗi/timeout/concurrency, không ghi token,
  password hay connection secret.
- Mock màn lỗi phải nhận status code và hành vi theo BR_Com_005; redirect sample hiện có
  không phải specification và không là expected UT.
- Frontend feature service dùng shared API adapter/messages/validators; không nhân bản
  HTTP/auth/message logic vào từng component.
