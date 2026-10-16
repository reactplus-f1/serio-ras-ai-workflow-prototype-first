# Chất lượng RAS C1 và C2

Profile 0.3.0 giữ chất lượng đã chốt: C1 = 100%, C2 = 100% trên scope hợp lệ từng module,
mọi case trong kế hoạch chạy và PASS, không còn BLOCKER/MAJOR mở. MINOR ACCEPTED chỉ với
quyết định người review. G2 chốt đối chiếu BD↔PG, G3 chốt Testspec, G4 chốt DD, G5 chốt code/UT, G6 nghiệm thu.

## Định nghĩa và bằng chứng

- C1: covered branch outcomes / total required branch outcomes.
- C2: covered atomic True/False outcomes / total required atomic outcomes.
  Một atomic condition có 2 outcomes. Phải thật sự đánh giá T/F; short-circuit không
  phải evaluation. Line/branch report hoặc input truth table không thay bằng chứng C2.
- Báo raw/excluded/covered và tỷ lệ riêng từng module. Không lấy trung bình module.
  Không có branch/condition: counts 0 với inventory và human N/A verification.
- Ngoại lệ chỉ cho phần chứng minh không khả thi, cần evidence và quyết định thật;
  thiếu tool/thời gian hoặc khó test không phải lý do loại trừ. Báo raw và effective.
- TOOL/MATRIX phải được thử trên stack thật; MATRIX có evaluation trace thực, không chỉ
  case plan. Thiếu capability/evidence ghi NOT VERIFIED. MC/DC chỉ là scope mở rộng.

## Expected và phạm vi kiểm chứng

Expected từ BD/pg-guide đã duyệt (kể cả giả định `A-xx` được chấp nhận ở G0); Testspec có
trước DD nên không yêu cầu DD tồn tại ở G3. PG dùng kiểm kê branches/conditions, không tạo
expected từ hành vi code. DD ở S5 phải giữ Rules/Required và đối chiếu với BD/pg-guide/PG/
Testspec. G4 review độc lập DD; G5 review
assertion, PG và test snapshot. Khi lệch, sửa sản phẩm sai qua gate chịu ảnh hưởng.

UT design rule của khách yêu cầu decision table cho join patterns và conditional cases
phức tạp; performance dùng dữ liệu phù hợp nghiệp vụ và chuẩn phản hồi 5 giây nếu thuộc
scope. Không gán yêu cầu performance của mọi hệ thống vào mỗi unit test. Case trong plan
không được skip/xóa để tạo PASS; mọi case đã đưa vào plan nghiệm thu phải chạy.
UI/DB/integration/regression theo scope, real/mock limits phải rõ; mock không thay DB
evidence hoặc kiểm chứng child-screen thật.

## Evidence và tái hiện

Source → Rule → Case → Test → Run → Evidence liên kết đúng versions. DD/PG mapping
theo Rule ID. Code/Test commit ghi nếu có (user tự commit), data/tool/config/environment và Run ID thật.
Evidence gồm raw result/log/coverage/inventory/T-F trace, ảnh thao tác UI và DB trước/sau
khi phù hợp case. Markdown report dẫn path; không cần copy workbook evidence generator
vào agent rules. QD thiếu thì ghi khả năng/cách thu evidence tương đương cần được chốt.

Theo kickoff, báo quy trình AI ở mức SERIO tái hiện được, gồm input/prompt/tool/model,
phần AI/con người sửa, thời gian tạo/review/rework/retest/chờ và giới hạn. Chưa có baseline
tương đương thì không tự tính phần trăm tiết kiệm.

Căn cứ: 単体テスト仕様書_ルール.xlsx / 単体テスト設計ルール!E16,E41,E57 và
単体テスト仕様書作成方針!G19:G22; 単体テスト実施_ルール.xlsx /
証跡取得・運用ルール一覧!C7,C19,C28,D28; kickoff 20261008 slides 7–8/16–17. Hai workbook này
do user đưa ở S4/S7; khi cần xác nhận ô, yêu cầu file gốc.
Counts/schema không xác thực reviewer hoặc chứng minh inventory/expected đúng; người review
phải kiểm tra raw artifacts, code và nguồn. Không tự xác nhận finding, ngoại lệ hoặc gate.
