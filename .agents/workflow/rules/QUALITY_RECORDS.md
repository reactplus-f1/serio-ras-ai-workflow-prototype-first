# Hợp đồng hồ sơ kiểm tra 0.3.0

Giữ tên section `##` và tên cột trong templates; nội dung Việt/Nhật tùy loại hồ sơ.
ID ASCII ổn định, duy nhất trong bảng. Escape pipe trong ô bằng `\|`. Không có records
thì để header/separator, không ghi dòng ví dụ chưa xác nhận.

## Nguồn và manifest

Source/artifact/evidence manifest có Files: ID / Path / Role. Path tuyệt đối hoặc từ task.
Source phải có BD chính đúng đường dẫn trong task. Code/test artifacts liệt kê đúng file;
user tự commit, SHA ghi nếu có. Evidence là raw
result/log/inventory/coverage/evaluation trace của đúng run; không chỉ URL mất quyền.

## Rule, case và readiness

pg-guide/DD có Rules: Rule ID / Source / Statement / Required YES/NO. DD giữ toàn bộ
Rule IDs và Required. Reviewer đối chiếu nguồn BD để biết pg-guide đã đủ nghĩa vụ.
pg-guide có Atomic conditions và Kế hoạch code (mỗi dòng trỏ Rule tồn tại); UT có Cases,
Condition plan và Readiness. Điều kiện phân tích phải có kế hoạch T/F trỏ case tồn tại.
Readiness phải READY với owner/evidence trước G2. Testspec dựa pg-guide/BD; DD đối chiếu ở
S4 và chốt tại G3.
Decisions có thể rỗng nếu không có logic ghép và giải thích rõ. Quality plan lập ở S3 từ
code PG đã duyệt G1: Modules chốt scope/method TOOL hoặc MATRIX; thay plan mở G2.

## Execution và traceability

pg-implementation.md ở G1 không bắt buộc Code commit (user tự commit; ghi SHA nếu có).
Implementation/test-report cuối ở G4/G5: Code/Test commit tùy chọn; nếu ghi thì phải khớp nhau.
Test report có Run ID, Environment, Tool versions, Data version. Results chứa mọi case:
Case ID / Test ID / Status / Actual / Evidence ID. PASS/FAIL/SKIPPED/NOT_RUN đều được ghi
trung thực, nhưng mọi case phải PASS trước nghiệm thu. Parameterized datasets có ID riêng.
Reviewer đối chiếu raw result với Results và file thực; không do AI tự tạo PASS.

Traceability: Rule ID / Source / Case ID / Test ID / Run ID / Evidence ID, khớp Cases
và Results. Case có primary Rule ID; nghĩa vụ nhiều rule cần tách case hoặc giải thích
mapping bổ sung được reviewer kiểm tra. Một case PASS không tự chứng minh đủ cả rule.

## Coverage

- Branches: mỗi dòng một branch outcome thực ở code, Module ID và Location.
- Conditions: mỗi dòng atomic condition, case/evidence T/F; inventory bao gồm kế hoạch
  và điều kiện kỹ thuật phát sinh. Case mới mở G2, không xóa điều kiện khó test.
- ID lists dùng dấu phẩy; case/evidence ghép theo vị trí. Evidence phải đúng Evidence ID
  của case trong Results. `-` là không có. Raw artifact có thể chứa nhiều case, reviewer
  xác minh locator và kết quả đánh giá thật, kể cả short-circuit.
- Modules báo raw/excluded/covered từng C1/C2; C2 raw = 2 × conditions. Validator đối chiếu
  counts với inventory và buộc covered = raw - accepted exclusions từng module.
- Counts 0 vẫn cần inventory evidence và human N/A verification. Không lấy trung bình.
- Exceptions chỉ BRANCH/CONDITION, khớp Target ID, ACCEPTED + reviewer/date/reason/evidence.
  Agent không tự điền ACCEPTED. Miễn case cần thay scope/plan và duyệt lại.

## Findings và acceptance

PG review/DD review/code-review/acceptance có `判定: PASS` hoặc FAIL dòng riêng và bảng Finding:
ID / Severity / Status / Decision. Severity BLOCKER/MAJOR/MINOR; Status OPEN/CLOSED/ACCEPTED.
CLOSED dẫn evidence; chỉ MINOR được người review ACCEPTED. Không có finding để bảng rỗng.
Validator kiểm tra bảng, không chỉ chữ PASS. Acceptance giữ đủ sáu Check trong template,
mỗi Check PASS hoặc N/A có evidence/reviewer. Coverage, case PASS, version/evidence
không được N/A (inventory 0 vẫn cần người xác minh check coverage PASS).

## Giới hạn

Schema kiểm tra được, không phải test runner/chữ ký điện tử. Kit không tự tìm mọi branch
trong ngôn ngữ bất kỳ, diễn giải assertion hoặc chứng minh thẩm quyền reviewer. Human
gates, tool/stack trial và raw evidence vẫn bắt buộc.
