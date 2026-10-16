# Quality plan <Function ID>

Lập ở S3, sau khi PG (G1) đã có: module và branch/condition lấy từ code thật, method
TOOL/MATRIX đã thử trên stack thật. Mục tiêu C1 = 100%, C2 = 100% trong phạm vi hợp lệ được
người review xác nhận. Không thay bằng line coverage. Mọi case trong kế hoạch đã duyệt phải
chạy và PASS. Ngoại lệ coverage cần bằng chứng không khả thi và quyết định của người review.
Hồ sơ này được review tại G2 cùng ut-design.md.

## Modules

| Module ID | Scope | C1 method | C2 method | Evidence plan |
|---|---|---|---|---|

Mỗi module khai báo riêng, lấy từ pg-implementation.md / pg-artifact-manifest.md (G1).
C1 method/C2 method dùng TOOL hoặc MATRIX, sau khi
kiểm tra năng lực đo/xác minh trên stack thực, kể cả short-circuit. Không có điều kiện
thì báo N/A với inventory có evidence; không tự coi tỷ lệ 0/0 là 100%.

## Readiness

| Item | Status | Owner | Decision / evidence |
|---|---|---|---|
| Source/build/test environment/data | PENDING | | |
| Tool versions/config and C1/C2 trial | PENDING | | |
| Customer UT/evidence format | PENDING | | |
| Real/mock dependencies and regression scope | PENDING | | |
| Independent UT/code reviewer and acceptance owner | PENDING | | |

Trạng thái phải READY (có owner và evidence) trước G2; chi tiết ghi ở UT Design /
Readiness. Nếu thay scope, method hoặc plan đã đóng băng tại G2, user yêu cầu làm lại từ G2
và xác nhận lại trong chat.
Thời gian chuẩn bị, review, rework, retest và evidence ghi vào báo cáo PoC.
