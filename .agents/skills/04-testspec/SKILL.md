---
name: 04-testspec
description: Thiết kế Testspec S4 sau G2 (đối chiếu BD↔PG); expected từ BD/pg-guide đã duyệt, inventory từ PG; dừng G3.
---

# Skill 04-testspec

## Mục tiêu

Thiết kế case/decision table và lập kế hoạch chất lượng (module, method đo C1/C2, readiness)
trước DD và UT code. Quality plan chỉ lập được ở đây vì cần code PG thật để biết module và
thử tool coverage.

## Điều kiện chạy

`next` chỉ định S4; user đã xác nhận G2 (đối chiếu BD↔PG) trong chat; G0/G1 vẫn là baseline. DD chưa là input bắt buộc.

## Input (user đưa)

- **Bắt buộc**: 単体テスト仕様書_ルール của Serio. Thiếu → hỏi và dừng.
- **Nếu có**: mẫu UT spec/decision table của Serio.
- Từ run: pg-guide.md G0 (Rules, atomic conditions, giả định `A-xx` đã duyệt), PG
  snapshot/inventory G1 (pg-implementation.md, pg-artifact-manifest.md), reconciliation.md G2
  (Rule nào MATCH, Finding đã quyết định thế nào).

Agent đọc: QUALITY_RULES, QUALITY_RECORDS.

## Thực hiện

Lập quality-plan.md: chia module theo code PG thật (G1), chọn C1/C2 method TOOL hoặc
MATRIX sau khi thử trên stack thật, ghi evidence plan. Lập case thường/biên/lỗi với
precondition/input/expected/source và Case ID. Đối chiếu Rules
bắt buộc; condition T/F mapping kể cả short-circuit. Decision table cho join/tổ hợp; mỗi
pattern có case. Expected **từ BD/pg-guide đã duyệt**, không từ kết quả PG; PG chỉ cho
inventory. Rule `DEVIATION` chưa sửa vẫn lập case với expected từ BD (case sẽ FAIL
đến khi sửa); Rule `CONFIRM` dùng giả định đã duyệt ở G2. Bắt buộc có case quyền cho
mỗi API: chưa đăng nhập (401), role không được phép (403), role được phép. Readiness 5 mục có owner/evidence thật; thiếu tool C2 ghi chưa xác minh.

## Output

- [quality-plan.md](../../workflow/templates/quality-plan.md)
- [ut-design.md](../../workflow/templates/ut-design.md)
- [decision-table.md](../../workflow/templates/decision-table.md)

## Kiểm tra hoàn thành

Mỗi module có method TOOL/MATRIX đã thử; mỗi rule bắt buộc có case; atomic conditions có
T/F plan; expected có nguồn; readiness READY.
Kế hoạch chưa chứng minh coverage chạy.

## Dừng và bàn giao

Trước khi báo cáo: ghi log công việc cho từng hoạt động của lượt vào `log/作業ログ.xlsx`
(`worklog.py add`, `rules/WORKLOG_RULES.md`) và nêu ID log trong mục Thành phẩm.
Báo cáo bốn mục (AGENTS.md), trình G3 và dừng; nêu tài liệu cần cho S5 (mẫu DD/API定義書
nếu Serio có). Không tự xác nhận, không Git.

## Lỗi thường gặp

Lấy PG làm oracle; yêu cầu DD trước Testspec; coi truth table là C2 thực thi; bỏ case khó.
