# Workflow RAS 0.3.0 — chạy lần đầu

Luồng: **BD → Hướng dẫn PG → PG → Testspec → DD → UT → Nghiệm thu** (S1–S7), human gate G0–G5,
hồ sơ Markdown, mục tiêu chất lượng C1 + C2.

## Trong gói có gì

```text
AGENTS.md                       entrypoint cho agent
WORKFLOW-START.md               file này
.github/copilot-instructions.md
.agents/
  skills/                       7 skill công đoạn (01-pg-guide … 07-acceptance) và git-workflow
  workflow/
    WORKFLOW.md                 luồng, bàn giao, sửa sau review
    RUNBOOK.md                  lệnh cho người vận hành và người review
    START_CHAT.md               đoạn mở đầu cho mỗi phiên agent
    config/workflow.json        step → skill → output → gate
    rules/                      quy định RAS đã tổng hợp từ tài liệu Serio
    templates/                  mẫu hồ sơ Markdown trống
    scripts/                    kit.py (gate/checker), quality.py, xlsx_view.py
```

Gói không kèm BD, tài liệu Serio, code sản phẩm hay run cũ. Mỗi chức năng tạo
`runs/<Function-ID>/` khi bắt đầu; bản sao đầu vào nằm ở `runs/<Function-ID>/inputs/`.

## Chuẩn bị

- Python 3.10+ (chỉ cho script workflow, không thay SDK .NET/Node của sản phẩm).
- BD của chức năng dưới dạng **Excel 画面定義書 (.xlsx)** do Serio cung cấp. User ném vào
  chat; agent lưu bản làm việc vào `runs/<Function-ID>/inputs/`.
- Repo code RAS (ras-system / ras-web) được clone sẵn; user sẽ đưa đường dẫn cho agent khi
  đến bước PG.

## Lượt đầu tiên (S1)

Không cần lệnh chuẩn bị. Mở phiên agent tại root repo này, đính kèm BD và chat:

```text
Đọc AGENTS.md và .agents/workflow/START_CHAT.md. Đây là BD. Scope: toàn bộ màn hình
BR_Com_004; BR_Com_003/005 mock. Người phụ trách: <tên>.
```

Agent nhận ra Function ID từ BD, lưu BD vào `runs/BR_Com_004/inputs/`, chạy `kit.py init`
(tạo `task.md` ghi đường dẫn BD và `source-manifest.md`),
rồi làm S1 theo skill 01-pg-guide — đọc BD, lập rule và giả định, viết `pg-guide.md`
(hướng dẫn triển khai prototype: code gì, ở đâu, mock gì) — và dừng tại G0 với báo cáo: đã
làm gì, thành phẩm ở đâu,
gate kế tiếp, cần user đưa thêm gì. Thiếu scope thì agent hỏi trước khi làm. Mọi lệnh sau
đó đều kiểm tra BD còn ở đúng đường dẫn; BD đổi phiên bản thì review lại từ G0. Agent không tự xác nhận review, không viết PG, không
build/test/SQL, không thao tác Git.

Các lượt sau cũng vậy: chat "tiếp tục run BR_Com_004" kèm tài liệu bước đó cần
(`rules/SOURCE_MAP.md`); thiếu mục bắt buộc thì agent hỏi lại thay vì làm tiếp.

Lệnh `init` thủ công (khi muốn tự tạo run trước): xem RUNBOOK.

## Kiểm tra hồ sơ

```powershell
python .agents/workflow/scripts/kit.py next  --task-dir runs/BR_Com_004
python .agents/workflow/scripts/kit.py check --task-dir runs/BR_Com_004 --strict
```

`READY` là kết quả kiểm tra hồ sơ, chưa phải xác nhận của user. Người review xác nhận trong chat theo
[RUNBOOK](.agents/workflow/RUNBOOK.md).
