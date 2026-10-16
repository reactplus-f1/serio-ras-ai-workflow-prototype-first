# Workflow RAS 0.3.0

Bộ agent dùng rule đã tổng hợp từ tài liệu RAS của Serio và các tài liệu **user đưa vào từng
bước**. Không có đường dẫn nguồn cố định: tài liệu nào được dùng thì ghi tên file vào
`source-manifest.md` của run.

| Vị trí | Nội dung |
|---|---|
| WORKFLOW.md, config/workflow.json | Luồng và mapping step → skill → output → gate |
| rules/PROJECT_RULES.md | Phạm vi, thứ tự căn cứ, xử lý phần chưa xác định |
| rules/SOURCE_MAP.md | Mỗi bước cần user đưa tài liệu gì, agent đọc rule gì |
| rules/REPOSITORY_RULES.md | Cách nhận và xác nhận repo code từ user |
| rules/CODING_RULES.md | Quy tắc C#/Angular/format tổng hợp từ PG rule và config repo |
| rules/ARCHITECTURE_RULES.md | Layer, API envelope, quyền, dữ liệu, logging |
| rules/UI_RULES.md | Quy định UI chung và shared components |
| rules/BR_COM_004_RULES.md | Phạm vi PoC, nghiệp vụ BR_Com_004, mock contracts |
| rules/QUALITY_RULES.md, QUALITY_RECORDS.md | Chất lượng C1/C2, evidence, schema hồ sơ |
| rules/SKILL_AUTHORING.md | Cách bảo trì skill |
| rules/WORKLOG_RULES.md | Log công việc Excel: khi nào ghi, 17 mục (Run ID, lệnh + exit code, thời gian tách riêng), quy tắc ghi log |
| ../skills/ | 8 skill công đoạn (01-pg-guide … 08-acceptance) và git-workflow (chỉ đọc) |
| templates/ | Mẫu hồ sơ Markdown |
| scripts/ | kit.py, quality.py, xlsx_view.py, worklog.py (log công việc) |
| ../../log/ | `作業ログ.xlsx` (log chung mọi hoạt động) và `作業ログ_template.xlsx` |
| RUNBOOK.md, START_CHAT.md | Vận hành và mở phiên |

Run của một chức năng ở `runs/<Function-ID>/` trong repo này. Raw evidence/snapshot ở nơi
user chỉ định, có manifest. Không tự tạo run khi chưa được yêu cầu. Lịch sử làm việc của mọi run và mọi lần chỉnh workflow ghi ở `log/作業ログ.xlsx` (rules/WORKLOG_RULES.md).
Cách chạy DB/BE/FE local để test: `README.md` của repo code (serio-ras, mục Chạy môi trường local).
Hướng dẫn chạy lần đầu: [WORKFLOW-START.md](../../WORKFLOW-START.md).
