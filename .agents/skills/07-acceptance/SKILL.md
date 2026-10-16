---
name: 07-acceptance
description: Review cuối S7 sau evidence S6; lập acceptance và dừng G5 cho con người nghiệm thu.
---

# Skill 07-acceptance

## Mục tiêu

Chuẩn bị bàn giao có chất lượng và quy trình AI tái hiện được.

## Điều kiện chạy

`next` chỉ định S7; S6 đủ hồ sơ; user đã xác nhận G3/G4 trong chat. Reviewer truy cập được nguồn/code/raw
artifacts đúng phiên bản.

## Input (user đưa)

Toàn bộ hồ sơ run (pg-guide/PG/Testspec/DD/UT, report/coverage/traceability/exceptions/
manifests) và process log. Không cần user đưa thêm tài liệu.

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

Báo cáo bốn mục (AGENTS.md), trình G5 và dừng. Chỉ khi user xác nhận G5 trong chat mới là nghiệm thu. Không
tự xác nhận, không merge/deploy, không Git.

## Lỗi thường gặp

Coi 100% coverage là đủ; tự ghi reviewer/xác nhận; bỏ phần chưa xác minh; gọi hoàn tất khi
gate pending.
