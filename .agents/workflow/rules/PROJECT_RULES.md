# Quy tắc dự án RAS

## Đầu vào và nguồn

- **BD do Serio cung cấp là đầu vào**, dưới dạng Excel 画面定義書. User đưa file cho agent
  ở S1; `kit.py init` ghi đường dẫn BD vào task.md và mọi lệnh sau đó kiểm tra file còn tồn tại. BD đổi
  → run dừng, review lại từ G0.
- Các tài liệu khác (API一覧, テーブル設計書, PG_ルール, 画面共通仕様説明書, UT rule,
  メッセージ一覧, mẫu DD/UT…) **do user đưa khi bước đó cần** (SOURCE_MAP). Agent không tự
  tìm trên máy, không dùng đường dẫn ghi sẵn, không coi rule tổng hợp trong `.agents` là
  thay cho tài liệu gốc khi cần xác nhận một ô cụ thể.
- Thứ tự căn cứ: BD đúng version → tài liệu chung liên quan → quyết định đã duyệt (có ID,
  người, ngày) → template. Code mẫu/hiện có trong repo không quyết định expected nghiệp vụ.
- Mỗi rule/điều kiện ghi nguồn dạng `[SRC: tên file | sheet | ô/dòng]` hoặc
  `[DECISION: ID]`. Hai nguồn mâu thuẫn thì ghi cả hai, không âm thầm chọn; không tự tạo
  endpoint/schema/message/quyền/expected.
- Tài liệu thiếu ghi `PENDING`/`未確定` và ảnh hưởng. Chỉ nguồn thực sự đã đọc mới vào
  source-manifest; chưa đọc không được ghi "đã đọc".
- Giữ Function ID, API/data-access/message IDs của Serio; giữ Rule/Condition/Case IDs của run.
  DD tiếng Nhật; báo cáo quản lý/review có thể tiếng Việt. Hồ sơ chính thức là `.md`.

## Repo code

User đưa đường dẫn repo code và branch được giao khi đến S2 (REPOSITORY_RULES). Agent xác
nhận cấu trúc/config thật tại thời điểm đó và ghi vào task.md; không mặc định từ tài liệu.
Build/lint/test chỉ chạy khi nhiệm vụ cho phép; config có mặt chưa chứng minh build hay C1/C2.

## Chất lượng và sửa lại

Theo WORKFLOW và QUALITY_RULES. Expected từ BD/quyết định đã duyệt; reviewer độc lập kiểm
tra expected và assertion. PG có trước DD nhưng không được đổi rule/expected. Lỗi PG mở G1,
lỗi case mở G2, DD mở G3, UT code mở G4, nguồn/rule/giả định/kế hoạch code mở G0. Hồ sơ đã
chốt chỉ sửa khi user yêu cầu làm lại từ gate chịu ảnh hưởng.

## Dữ liệu, quyền và Git

Chỉ dùng tài liệu/source/tool/môi trường user cho phép. Không đưa secret (appsettings,
environment, token, connection string), account hay thông tin cá nhân vào rule, prompt,
log hay hồ sơ; chỉ ghi tên key. Agent không thao tác Git (skill git-workflow). Không tự
xác nhận review/miễn test/accept ngoại lệ/merge/deploy. Bảo trì kit không chạy công đoạn task.
