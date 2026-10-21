# Vận hành Workflow RAS

Chạy PowerShell tại root repo này, Python 3.10+. Thay placeholder bằng giá trị thật.
Python chỉ dùng cho script workflow.

## Khởi tạo run (một lần cho mỗi chức năng)

Bình thường agent chạy lệnh này trong S1 từ BD user đưa (skill 01-pg-guide). User có thể tự
chạy trước nếu muốn; kết quả như nhau.

```powershell
python .agents/workflow/scripts/kit.py init --task-dir runs/<Function-ID> --function-id <Function-ID> --bd "runs/<Function-ID>/inputs/<BD.xlsx>" --scope "<scope>"
```

`--bd` phải là đường dẫn ổn định (không phải file đính kèm tạm của chat); tên file tiếng
Nhật nên lấy qua `Get-ChildItem -Filter "*BR_Com_004*.xlsx"` thay vì gõ tay.

## Agent: kiểm tra và tìm bước kế tiếp

```powershell
python .agents/workflow/scripts/kit.py next  --task-dir runs/<Function-ID>
python .agents/workflow/scripts/kit.py check --task-dir runs/<Function-ID> [--strict]
```

`next`/`check` chỉ đọc hồ sơ; không chạy PG/test, không ghi quyết định review. Bước chưa tới
có thể `INCOMPLETE`. `next` báo bước chưa hoàn thành kế tiếp hoặc `COMPLETE`; khi hồ sơ READY, kit in dòng thông tin review point Gx và agent dừng để user xác nhận trong chat.

## User/người review: quyết định gate

Sau khi review hồ sơ và có quyết định thật, user xác nhận trực tiếp trong chat (ví dụ: "tiếp tục S2", "đồng ý G0"). Không có file hay lệnh ghi nhận riêng. Nếu phát hiện sai, user yêu cầu agent làm lại từ bước/gate sớm nhất chịu ảnh hưởng.

G0: người review đọc `pg-guide.md` — bảng "Giả định của AI" (chấp nhận/sửa từng dòng) và "Kế hoạch code". G1: user tự review code, không có file review riêng. G2: người review đọc `reconciliation.md`, quyết định từng Finding (sửa PG / chấp nhận / hỏi Serio). G4/G5/G6 cần review tương ứng (review, code-review, acceptance) có `判定: PASS` và bảng Finding hợp lệ.

## Xem ô trong BD

```powershell
python .agents/workflow/scripts/xlsx_view.py "<BD.xlsx>" --list
python .agents/workflow/scripts/xlsx_view.py "<BD.xlsx>" --sheet イベント定義
```

`xlsx_view.py` chỉ in **giá trị ô** (sheetData); sheet tên `(非表示)…` vẫn được liệt kê.
Ảnh layout (EMF) và text shape đọc bằng `xlsx_media.py`:

```powershell
python .agents/workflow/scripts/xlsx_media.py "<BD.xlsx>" --out runs/<ID>/inputs/layout
```

Script in theo sheet: `IMAGE <ô neo>: <png>` và `SHAPE <ô neo>: <text>`; EMF/WMF được convert
sang PNG (Pillow trên Windows, fallback PowerShell System.Drawing). Agent **xem ảnh PNG** và
ghi mục "Layout spec" trong `pg-guide.md`. Exit code 2 = có ảnh convert lỗi → hỏi user ảnh chụp.

## Log công việc Excel

```powershell
python .agents/workflow/scripts/worklog.py add --json entry.json     # thêm L-xxx vào log/作業ログ.xlsx
python .agents/workflow/scripts/worklog.py set --id L-003 --field status --value "Thất bại"
python .agents/workflow/scripts/worklog.py list                    # bảng tổng hợp
python .agents/workflow/scripts/worklog.py template                # dựng lại file mẫu Excel
```

Ghi sau mỗi hoạt động (`rules/WORKLOG_RULES.md`: 17 mục, key JSON, quy tắc ghi log). Người
phụ trách có thể sửa trực tiếp trong Excel (đóng Excel trước khi chạy script). Cần `pip install openpyxl`.

## Git

Mọi thao tác Git (commit, push, branch, merge) do user làm sau khi review file agent đã sửa.
Agent chỉ đọc trạng thái để báo cáo. Không cần SHA để khóa bước; ghi SHA vào hồ sơ chỉ khi user cung cấp.
