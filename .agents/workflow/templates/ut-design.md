# UT Design <Function ID>

Expected lấy từ BD/pg-guide đã duyệt (kể cả giả định A-xx), không suy ra từ PG. Testspec ở S3 có trước DD.
Mỗi nghĩa vụ bắt buộc trong Rules phải có đủ case. Required dùng YES/NO.
Không có giá trị input mơ hồ. Ghi null/rỗng, biên và nhánh lỗi phù hợp nguồn.

## Cases

| Case ID | Rule ID | Precondition | Input | Expected | Source | Required |
|---|---|---|---|---|---|---|

## Condition plan

| Condition ID | Rule ID | Expression | True cases | False cases | Short-circuit / unresolved |
|---|---|---|---|---|---|

## Review

Reviewer độc lập kiểm tra expected, đủ biên/tổ hợp cần thiết và assertion dự kiến.
Case plan không chứng minh execution coverage; đối chiếu inventory PG thực tế đã review G1.
G2 là điểm review UT Design; user xác nhận trong chat. Câu hỏi chặn mới phải mở lại gate nguồn.

## Readiness

| Item | Status | Owner | Evidence |
|---|---|---|---|
| Build/test environment/data | PENDING | | |
| Tool versions/config and C1/C2 trial | PENDING | | |
| Customer UT/evidence format | PENDING | | |
| Real/mock dependencies and regression scope | PENDING | | |
| Independent reviewers and acceptance owner | PENDING | | |

Giữ đủ năm Item này, mỗi mục READY trước G2, có owner và evidence. Bảng này là trạng thái
chuẩn bị chi tiết; quality-plan.md cùng gate giữ bản tóm tắt.
