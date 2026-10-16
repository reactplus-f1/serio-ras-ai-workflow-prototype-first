---
name: 03-testspec
description: Thiết kế Testspec S3 sau G1; expected từ BD/pg-guide đã duyệt, inventory từ PG; dừng G2.
---

# Skill 03-testspec

## Mục tiêu

Thiết kế case/decision table và lập kế hoạch chất lượng (module, method đo C1/C2, readiness)
trước DD và UT code. Quality plan chỉ lập được ở đây vì cần code PG thật để biết module và
thử tool coverage.

## Điều kiện chạy

`next` chỉ định S3; user đã xác nhận G1 trong chat; G0 vẫn là baseline. DD chưa là input bắt buộc.

## Input (user đưa)

- **Bắt buộc**: 単体テスト仕様書_ルール của Serio. Thiếu → hỏi và dừng.
- **Nếu có**: mẫu UT spec/decision table của Serio.
- Từ run: pg-guide.md G0 (Rules, atomic conditions, giả định `A-xx` đã duyệt), PG
  snapshot/inventory G1 (pg-implementation.md, pg-artifact-manifest.md).

Agent đọc: QUALITY_RULES, QUALITY_RECORDS.

## Thực hiện

Lập quality-plan.md: chia module theo code PG thật (G1), chọn C1/C2 method TOOL hoặc
MATRIX sau khi thử trên stack thật, ghi evidence plan. Lập case thường/biên/lỗi với
precondition/input/expected/source và Case ID. Đối chiếu Rules
bắt buộc; condition T/F mapping kể cả short-circuit. Decision table cho join/tổ hợp; mỗi
pattern có case. Expected **từ BD/pg-guide đã duyệt**, không từ kết quả PG; PG chỉ cho
inventory. Readiness 5 mục có owner/evidence thật; thiếu tool C2 ghi chưa xác minh.

## Output

- [quality-plan.md](../../workflow/templates/quality-plan.md)
- [ut-design.md](../../workflow/templates/ut-design.md)
- [decision-table.md](../../workflow/templates/decision-table.md)

## Kiểm tra hoàn thành

Mỗi module có method TOOL/MATRIX đã thử; mỗi rule bắt buộc có case; atomic conditions có
T/F plan; expected có nguồn; readiness READY.
Kế hoạch chưa chứng minh coverage chạy.

## Dừng và bàn giao

Báo cáo bốn mục (AGENTS.md), trình G2 và dừng; nêu tài liệu cần cho S4 (mẫu DD/API定義書
nếu Serio có). Không tự xác nhận, không Git.

## Lỗi thường gặp

Lấy PG làm oracle; yêu cầu DD trước Testspec; coi truth table là C2 thực thi; bỏ case khó.
