# DD review <Function ID>

判定: FAIL

## Kiểm tra bao phủ

| Mục | Số mục BD | Đã có trong DD | Thiếu | Bằng chứng |
|---|---:|---:|---:|---|
| Event | | | | |
| Field | | | | |
| Lỗi/message | | | | |
| API/DB | | | | |
| Chuyển màn | | | | |

## Finding

| ID | Severity | Vị trí DD | Nguồn đối chiếu | Vấn đề và cách sửa | Status | Decision |
|---|---|---|---|---|---|---|

## Thay đổi agent đã thực hiện

| Vị trí | Trước → sau | Nguồn chứng minh |
|---|---|---|

## Phần dev cần kiểm tra thủ công

- Logic nghiệp vụ, API/DB, khả năng triển khai, tiếng Nhật và format.
- Rule/Condition ID đầy đủ, điều kiện và expected kiểm thử được, mapping BD → DD không thiếu nghĩa vụ.
- Severity: BLOCKER/MAJOR/MINOR. Status: OPEN/CLOSED/ACCEPTED.
  CLOSED có Decision dẫn evidence sửa; chỉ MINOR được ACCEPTED với quyết định của người review.
  Agent không tự chấp nhận finding. Task 0.3.0 kiểm tra bảng Finding ngay cả khi ghi PASS.
