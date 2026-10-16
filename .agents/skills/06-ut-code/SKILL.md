---
name: 06-ut-code
description: Viết và review UT code S6 theo Testspec G3 và DD G4; chốt code/test tại G5 trước thực thi.
---

# Skill 06-ut-code

## Mục tiêu

UT code/assertion và snapshot cuối để reviewer chốt code/test.

## Điều kiện chạy

`next` chỉ định S6; user đã xác nhận G1/G2/G3/G4 trong chat và các baseline còn hiệu lực. **User đã cho phép** chạy test project
và cung cấp dữ liệu test; chưa có → hỏi và dừng.

## Input (user đưa)

- **Bắt buộc**: quyền chạy test project, dữ liệu test, tool đo coverage (tên/phiên bản).
- Từ run: Testspec G3, DD/review G4, PG G1, quality-plan.

Agent đọc: CODING_RULES, QUALITY_RULES, QUALITY_RECORDS.

## Thực hiện

Viết UT theo Case/Test IDs và expected đã review. Assertion kiểm tra hành vi/side effects;
mock call một mình không đủ. Rà inventory/condition coverage, giới hạn thật/mock, regression.
Không sửa PG (sửa cần mở G1). Lập implementation (Code/Test commit tùy chọn, ghi nếu user
cung cấp; agent liệt kê file, user commit), code-review và artifact-manifest gồm
PG/UT/config snapshot. Test sơ bộ chỉ khi được phép; kết quả chưa là nghiệm thu.

## Output

- [implementation.md](../../workflow/templates/implementation.md)
- [code-review.md](../../workflow/templates/code-review.md)
- [artifact-manifest.md](../../workflow/templates/artifact-manifest.md)

## Kiểm tra hoàn thành

DD/rule mapping, assertion và inventory có căn cứ; snapshots thật; code review không
finding chặn. Không tự ký reviewer.

## Dừng và bàn giao

Trước khi báo cáo: ghi log công việc cho từng hoạt động của lượt vào `log/作業ログ.docx`
(`worklog.py add`, `rules/WORKLOG_RULES.md`) và nêu ID log trong mục Thành phẩm.
Báo cáo bốn mục (AGENTS.md), trình G5 và dừng; nêu môi trường/tool cần cho S7. Không tự xác nhận,
không Git.

## Lỗi thường gặp

Sửa PG nhưng chỉ mở G5; sửa DD mà không mở G4; sửa expected thay vì lỗi; tự commit hoặc ghi
SHA dự kiến; assert mock mà bỏ dữ liệu/kết quả.
