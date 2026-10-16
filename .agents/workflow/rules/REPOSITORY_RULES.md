# Repo code: nhận và xác nhận

## Nguyên tắc

Gói workflow này nằm **riêng** với repo code. Agent không biết trước repo code ở đâu: **user
đưa đường dẫn và branch** khi đến S2 (hoặc sớm hơn nếu cần đọc config). Agent xác nhận cấu
trúc thật rồi ghi vào task.md, hàng "Repository / build / test". Mọi quan sát về repo
(cấu trúc, TFM, warning, config lệch) ghi vào pg-guide/pg-implementation của run, không
ghi vào rule.

## Cấu trúc tham khảo của RAS

Theo tài liệu kiến trúc và snapshot repo đã đọc khi tổng hợp rule (10/2026). **Xác nhận lại
trên repo user đưa** trước khi dùng:

| Phần | Vị trí tương đối trong repo code |
|---|---|
| API/Controller, validation, DI, HTTP pipeline | ras-system/src/Services/Ras/RasApi |
| Entity/interface, domain rules | ras-system/src/Services/Ras/RasDomain |
| Service/DTO/Result nghiệp vụ | ras-system/src/Services/Ras/RasUseCase |
| EF Core/Repository, audit, adapter | ras-system/src/Services/Ras/RasInfrastructure |
| Shared messages, auth, logging | ras-system/src/BuildingBlocks/Common |
| Unit test project | ras-system/src/Services/Ras/RasApi.UnitTests |
| Component test project | ras-system/src/Services/Ras/RasApi.ComponentTests |
| Angular feature | ras-web/src/app/features/<feature> |
| Angular shared UI/auth/API/messages/validators | ras-web/src/app/shared |
| PostgreSQL schema và seed | ras-system/sql |

Backend .NET (API net10.0), frontend Angular/TypeScript; batch và WinUI target khác và
không thuộc BR_Com_004. Chọn project theo task, không build cả solution.

## Lệnh tham khảo (chỉ khi nhiệm vụ cho phép)

| Phạm vi | Lệnh |
|---|---|
| ras-web | npm ci; npm run lint; npm run build; npm test |
| API | dotnet build <RasApi.csproj> |
| UT | dotnet test <RasApi.UnitTests csproj> |
| Chạy local DB/BE/FE | Theo `README.md` của serio-ras, mục "Chạy môi trường local" (Docker `ras-pg` 5432, BE `dotnet run` trong RasApi, FE `npm start`) |

Lệnh có mặt không chứng minh môi trường, UT hay C1/C2 đạt. Tool đo C2 phải thử trên stack
thật; không suy atomic T/F từ branch coverage. Không cài tool/dependency, không chạy SQL
seed (có `DROP TABLE … CASCADE`) hay Docker khi chỉ phân tích/bảo trì.

## Những gì phải hỏi user trước S2

- Đường dẫn repo, branch được giao, có được build/lint/test không.
- DB dùng cho PoC (local/Docker/shared), quyền tạo schema, dữ liệu test.
- Auth thật hay mock (Azure AD tenant của dự án), tài khoản test theo vai trò.
- Nơi lưu raw artifacts/snapshot và cách user muốn nhận file để tự commit.
