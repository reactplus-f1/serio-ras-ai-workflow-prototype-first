---
name: 05-ut-code
description: Viết và review UT code S5 theo Testspec G2 và DD G3; chốt code/test tại G4 trước thực thi.
---

# Skill 05-ut-code

## Mục tiêu

UT code/assertion và snapshot cuối để reviewer chốt code/test.

## Điều kiện chạy

`next` chỉ định S5; user đã xác nhận G1/G2/G3 trong chat và các baseline còn hiệu lực. **User đã cho phép** chạy test project
và cung cấp dữ liệu test; chưa có → hỏi và dừng.

## Input (user đưa)

- **Bắt buộc**: quyền chạy test project, dữ liệu test, tool đo coverage (tên/phiên bản).
- Từ run: Testspec G2, DD/review G3, PG G1, quality-plan.

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

Báo cáo bốn mục (AGENTS.md), trình G4 và dừng; nêu môi trường/tool cần cho S6. Không tự xác nhận,
không Git.

## Lỗi thường gặp

Sửa PG nhưng chỉ mở G4; sửa DD mà không mở G3; sửa expected thay vì lỗi; tự commit hoặc ghi
SHA dự kiến; assert mock mà bỏ dữ liệu/kết quả.
