---
name: 08-acceptance
description: Review cuối S8 sau evidence S7; lập acceptance và dừng G6 cho con người nghiệm thu.
---

# Skill 08-acceptance

## Mục tiêu

Chuẩn bị bàn giao có chất lượng và quy trình AI tái hiện được.

## Điều kiện chạy

`next` chỉ định S8; S7 đủ hồ sơ; user đã xác nhận G4/G5 trong chat. Reviewer truy cập được nguồn/code/raw
artifacts đúng phiên bản.

## Input (user đưa)

Toàn bộ hồ sơ run (pg-guide/PG/Testspec/DD/UT, report/coverage/traceability/exceptions/
manifests) và log công việc `log/作業ログ.xlsx`. Không cần user đưa thêm tài liệu.

Agent đọc: QUALITY_RULES, QUALITY_RECORDS.

## Thực hiện

Đối chiếu inventory/expected/assertion/case results, C1/C2 từng module, findings/ngoại lệ,
integration/mock limits, raw versions. Giữ sáu Check của template với evidence/reviewer. Ghi
format hồ sơ, người nhận/storage/quyền truy cập và cách tái hiện quy trình AI (input/prompt/
model/tool, phần người sửa, thời gian). NOT VERIFIED/FAIL không đổi thành PASS; chưa có
baseline thì không kết luận tiết kiệm.

## Output

- [acceptance.md](../../workflow/templates/acceptance.md)

## Kiểm tra hoàn thành

Sáu Check đủ evidence; không N/A cho core quality; không finding chặn; ngoại lệ là quyết định
thật; có hướng dẫn tái hiện.

## Dừng và bàn giao

Trước khi báo cáo: ghi log công việc cho từng hoạt động của lượt vào `log/作業ログ.xlsx`
(`worklog.py add`, `rules/WORKLOG_RULES.md`) và nêu ID log trong mục Thành phẩm.
Báo cáo bốn mục (AGENTS.md), trình G6 và dừng. Chỉ khi user xác nhận G6 trong chat mới là nghiệm thu. Không
tự xác nhận, không merge/deploy, không Git.

## Lỗi thường gặp

Coi 100% coverage là đủ; tự ghi reviewer/xác nhận; bỏ phần chưa xác minh; gọi hoàn tất khi
gate pending.
