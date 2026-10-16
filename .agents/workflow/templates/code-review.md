# Code review <Function ID>

判定: FAIL

## Finding

| ID | Severity | Location | Issue | Status | Decision |
|---|---|---|---|---|---|

## Reviewer checks

Kiểm tra source/commit thật, DD Rule IDs, UT Case/Test IDs, assertion không chỉ kiểm tra
mock, scope branch/atomic condition, side effect, integration/regression và lệnh tái hiện.
Severity BLOCKER/MAJOR/MINOR; Status OPEN/CLOSED/ACCEPTED. Chỉ MINOR được người review
ACCEPTED, dẫn quyết định ở Decision. Đóng finding phải có evidence sửa.
G4 là điểm review code/UT code của user, không phải merge/deploy authorization.
