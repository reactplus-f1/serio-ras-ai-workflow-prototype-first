---
name: 07-test-evidence
description: Chạy UT S7 sau G5 và thu evidence C1/C2 thật; chuẩn bị hồ sơ S8 khi mọi kiểm tra đạt.
---

# Skill 07-test-evidence

## Mục tiêu

Chứng minh execution, coverage và truy vết đúng phiên bản; không tự nghiệm thu.

## Điều kiện chạy

`next` chỉ định S7; user đã xác nhận G5 trong chat; đúng code/test/data/tool snapshot; **user cho
phép chạy** trên môi trường chỉ định.

## Input (user đưa)

- **Bắt buộc**: 単体テスト実施_ルール của Serio (yêu cầu evidence, QD); môi trường/DB/tool
  coverage/config/data; Run ID quy ước. Thiếu → hỏi và dừng.
- Từ run: DD/Testspec/code/UT đã review, manifests.

Agent đọc: QUALITY_RULES, QUALITY_RECORDS.

## Thực hiện

Chạy đúng plan; ghi status/actual/Run ID/commits/tool/data/environment. Thu raw result/log/
inventory/C1/C2 evaluation và UI/DB evidence theo scope, lưu ở nơi user chỉ định, ghi đường dẫn.
Counts riêng từng module, raw/effective/exclusions. Traceability toàn case, real/mock limits,
defects. FAIL/SKIPPED/NOT_RUN trung thực; muốn sửa gì mở gate tương ứng trước, review, rerun.

## Output

- [test-report.md](../../workflow/templates/test-report.md)
- [coverage.md](../../workflow/templates/coverage.md)
- [traceability.md](../../workflow/templates/traceability.md)
- [exceptions.md](../../workflow/templates/exceptions.md)
- [evidence-manifest.md](../../workflow/templates/evidence-manifest.md)

## Kiểm tra hoàn thành

Mọi planned case PASS; C1/C2 đủ từng module có inventory/raw evidence; versions/mapping nhất
quán; ngoại lệ có quyết định con người. Thiếu evidence → NOT VERIFIED.

## Dừng và bàn giao

Trước khi báo cáo: ghi log công việc cho từng hoạt động của lượt vào `log/作業ログ.docx`
(`worklog.py add`, `rules/WORKLOG_RULES.md`) và nêu ID log trong mục Thành phẩm.
S7 không có gate riêng. Báo cáo bốn mục (AGENTS.md); đạt thì chuẩn bị S8; còn FAIL/thiếu
evidence thì báo và dừng. Không tự xác nhận, không Git.

## Lỗi thường gặp

Tự tạo log/PASS; coi short-circuit là evaluation; dùng report khác commit; lấy trung bình
module; tự xác nhận exceptions.
