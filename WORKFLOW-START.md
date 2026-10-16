# Workflow RAS 0.3.0 — chạy lần đầu

Luồng: **BD → Hướng dẫn PG → PG → Đối chiếu BD↔PG → Testspec → DD → UT → Nghiệm thu** (S1–S8), human gate G0–G6,
hồ sơ Markdown, mục tiêu chất lượng C1 + C2.

## Trong repo có gì

```text
AGENTS.md                       entrypoint cho agent
WORKFLOW-START.md               file này
.github/copilot-instructions.md
.agents/
  skills/                       8 skill công đoạn (01-pg-guide … 08-acceptance) và git-workflow
  workflow/
    WORKFLOW.md                 luồng, bàn giao, sửa sau review, báo cáo tiến độ
    RUNBOOK.md                  lệnh cho người vận hành và người review
    START_CHAT.md               đoạn mở đầu cho mỗi phiên agent
    config/workflow.json        step → skill → output → gate
    rules/                      quy định RAS đã tổng hợp từ tài liệu Serio
    templates/                  mẫu hồ sơ Markdown trống
    scripts/                    kit.py (gate/checker), quality.py, xlsx_view.py, worklog.py
log/
  作業ログ.docx                 log công việc chung (mọi hoạt động)
  作業ログ_template.docx        mẫu log
runs/
  <Function-ID>/                hồ sơ một chức năng (task.md, pg-guide.md, QA.md, …)
    inputs/                     bản BD làm việc
    process/                    test-guide.md (kịch bản test)
```

Repo không kèm tài liệu Serio hay code sản phẩm. Run đang có: `runs/BR_Com_004/` (S1, S2
READY; chờ review G1). Chức năng mới tạo `runs/<Function-ID>/` khi bắt đầu.

## Chuẩn bị

- Python 3.10+ (script workflow) và `python-docx` (để ghi log Word).
- BD của chức năng dưới dạng **Excel 画面定義書 (.xlsx)** do Serio cung cấp. User ném vào
  chat; agent lưu bản làm việc vào `runs/<Function-ID>/inputs/` (task.md ghi đường dẫn
  tương đối `inputs/...`, nên repo có thể chuyển thư mục/clone lại).
- Repo code RAS `serio-ras` (ras-system / ras-web) clone sẵn; user đưa đường dẫn và branch
  khi đến S2. Cách chạy DB/BE/FE local: `README.md` của serio-ras, mục "Chạy môi trường local".

## Lượt đầu tiên (S1)

Không cần lệnh chuẩn bị. Mở phiên agent tại root repo này, đính kèm BD và chat:

```text
Đọc AGENTS.md và .agents/workflow/START_CHAT.md, rồi chạy S1 cho file BD đính kèm.
Scope: chỉ chức năng chính của BR_Com_004; BR_Com_003/005 là mock.
```

Agent nhận ra Function ID từ BD, lưu BD vào `runs/BR_Com_004/inputs/`, chạy `kit.py init`
(tạo `task.md` và `source-manifest.md`), rồi làm S1 theo skill 01-pg-guide: đọc BD, lập
rule và giả định, viết `pg-guide.md` (code gì, ở đâu, mock gì) và `QA.md` (câu hỏi nghiệp vụ
gửi Serio, có cột 資料/シート/行 để truy vết), ghi log công việc `log/作業ログ.docx`, rồi
dừng tại G0 với
báo cáo: đã làm gì, thành phẩm ở đâu, gate kế tiếp, cần user đưa thêm gì. Thiếu scope thì
agent hỏi trước khi làm. Ở S1 agent không viết code, không build/test/SQL.

Các lượt sau: user xác nhận review trong chat rồi chỉ thị bước tiếp ("chạy S2 cho
BR_Com_004") kèm tài liệu bước đó cần (`rules/SOURCE_MAP.md`); thiếu mục bắt buộc thì agent
hỏi lại. Agent không tự xác nhận review và không thao tác Git (user tự commit; không cần SHA
để khóa bước). Mọi lệnh kit kiểm tra BD còn ở đúng đường dẫn; BD đổi phiên bản thì review
lại từ G0.

Lệnh `init` thủ công (khi muốn tự tạo run trước): xem RUNBOOK.

## Kiểm tra hồ sơ

```powershell
python .agents/workflow/scripts/kit.py next  --task-dir runs/BR_Com_004
python .agents/workflow/scripts/kit.py check --task-dir runs/BR_Com_004 --strict
```

`READY` là kết quả kiểm tra hồ sơ, chưa phải xác nhận của user. Người review xác nhận trong chat theo
[RUNBOOK](.agents/workflow/RUNBOOK.md).
