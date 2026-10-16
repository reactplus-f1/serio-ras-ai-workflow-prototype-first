# Test report <Function ID>

## Metadata

| Item | Value |
|---|---|
| Code commit | |
| Test commit | |
| Run ID | |
| Environment | |
| Tool versions | |
| Data version | |

Commit (nếu ghi) phải khớp implementation.md. Report từ kết quả chạy thật; AI không tự tạo PASS.
Thêm từng case đã duyệt, cả FAIL/SKIPPED/NOT_RUN. Chỉ khi mọi case PASS mới sẵn sàng G6.

## Results

| Case ID | Test ID | Status | Actual | Evidence ID |
|---|---|---|---|---|

## Integration and regression

Ghi phần thực/mock, UI/DB/dependency, scope regression, lệnh chạy và evidence.
Case parameterized có Case ID riêng từng dataset. Một case có thể ánh xạ nhiều hàm test;
Test ID là nhóm ID xác định, giữ cùng chuỗi ở traceability.

## Defects and effort

Ghi defect, retest, người xác nhận và effort chuẩn bị/thực hiện/review/rework/evidence;
thời gian chờ riêng. Không suy ra tiết kiệm khi chưa có baseline tương đương.
