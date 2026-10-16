# Hướng dẫn triển khai prototype <Function ID>

Tạo từ BD do user đưa. Mỗi rule, điều kiện và việc cần code có `[SRC: file | sheet | ô/dòng]`
hoặc `[DECISION: A-xx]`. Đây là hồ sơ duy nhất S2 (code PG) dựa vào; người review G0 duyệt
cả phân tích lẫn kế hoạch code.

## 1. BD và phạm vi

| Function ID | Tên chức năng | File BD | Phiên bản / ngày (改訂履歴) | Scope | Ngoài scope |
|---|---|---|---|---|---|

## 2. Sheet đã đọc và giới hạn

| Sheet | Đọc bằng | Nội dung chính | Giới hạn |
|---|---|---|---|

Ghi rõ: layout dạng ảnh, text shape ngoài ô, merged cell, sheet `(非表示)` — cái nào script
không đọc được và cần người xem Excel.

## 3. Luồng chính theo event

| Thứ tự | Người dùng/trigger | Xử lý hệ thống | Dữ liệu thay đổi | Nguồn |
|---|---|---|---|---|

## 4. Màn hình: field, validation, state

| Field ID | Tên | Kiểu / độ dài | Bắt buộc | Validation / message | State (enable/visible) | Nguồn |
|---|---|---|---|---|---|---|

## 5. Nhánh lỗi và tình huống biên

| Điều kiện | Hành vi | Message / chuyển màn | Nguồn |
|---|---|---|---|

## 6. Dữ liệu và API

| Mục | Bảng / API | Thao tác (R/W) | Điều kiện | Nguồn |
|---|---|---|---|---|

## 7. Phụ thuộc và ranh giới mock

| Thành phần | Trong scope / mock / chỉ tham chiếu | Contract trao đổi | Nguồn hoặc giả định |
|---|---|---|---|

## Giả định của AI (chỗ BD mơ hồ hoặc thiếu)

AI tự chọn cách hiểu và ghi ở đây, không dừng chờ. Mỗi dòng có ID `A-xx`; Rule/code dựa
trên giả định ghi `[DECISION: A-xx]`. Người review G0 đánh dấu Chấp nhận / Sửa; giả định bị
sửa sau G0 → user yêu cầu làm lại từ G0.

| ID | Vị trí BD mơ hồ | Các cách hiểu | AI chọn | Lý do | Ảnh hưởng nếu sai | Review G0 |
|---|---|---|---|---|---|---|
| A-01 | | | | | | |

## Rules

Mỗi nghĩa vụ nghiệp vụ có ID ổn định, kể cả biên/lỗi cần kiểm tra. Required dùng YES/NO.
Source ghi file / sheet / ô hoặc `[DECISION: A-xx]`. Escape dấu pipe bằng \| trong bảng.

| Rule ID | Source | Statement | Required |
|---|---|---|---|

## Atomic conditions

| Condition ID | Rule ID | Expression | True/False meaning | Source |
|---|---|---|---|---|

## Kế hoạch code

Chỉ rõ S2 phải code gì, ở đâu. "Vị trí dự kiến" theo cấu trúc repo đã biết từ
REPOSITORY_RULES / ARCHITECTURE_RULES; chưa xác nhận repo thì ghi layer (API/Service/
Repository/Component) và đánh dấu "xác nhận ở S2". Rule ID có thể nhiều, cách nhau bằng dấu
phẩy.

| Mục | Rule ID | Vị trí dự kiến | Việc cần làm | Tái dùng common | Mock |
|---|---|---|---|---|---|

Nhóm gợi ý: endpoint API, request/response DTO, validation server, service logic, truy cập
DB, component màn hình, validation client, message, chuyển màn, quyền.

## Tài liệu cần cho bước sau

| Bước | Tài liệu | Bắt buộc / nếu có | Trạng thái |
|---|---|---|---|
| S2 PG | Đường dẫn repo code, branch, API一覧, テーブル設計書 | Bắt buộc | PENDING |
| S4 Testspec | 単体テスト仕様書_ルール | Bắt buộc | PENDING |
| S5 DD | Mẫu 詳細設計書 / API定義書 | Nếu có | PENDING |
| S7 Evidence | 単体テスト実施_ルール, môi trường, tool coverage | Bắt buộc | PENDING |

Không suy rule từ code mẫu. Inventory nhánh/điều kiện code thực tế được kiểm tra ở
S2/S4/S6/S7.
