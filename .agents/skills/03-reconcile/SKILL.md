---
name: 03-reconcile
description: S3 — đối chiếu BD với code PG sau G1 (rule nào xử lý ở đâu, khớp/lệch/cần xác nhận) trước Testspec; dừng G2.
---

# Skill 03-reconcile

## Mục tiêu

Chứng minh từng Rule của BD (qua `pg-guide.md` đã duyệt G0) đã được xử lý ở đâu trong code PG
(G1) và kết luận khớp / lệch / cần xác nhận / chưa làm, để Testspec (S4) không lấy phần code
chưa đối chiếu làm cơ sở. Đây là bước bắt buộc của flow chuẩn giữa PG và Testspec/DD.

## Điều kiện chạy

`next` chỉ định S3; user đã xác nhận G1 trong chat; G0 vẫn là baseline. Không cần tài liệu
mới; nếu Rule dựa trên tài liệu `CUSTOMER` chưa có trong `source-manifest.md` thì yêu cầu user
đưa file gốc và dừng.

## Input (user đưa)

- **Bắt buộc**: không có tài liệu mới; code PG đã review G1 trong repo user đưa.
- **Nếu có**: câu trả lời QA của Serio, API一覧 / テーブル設計書 bản mới.
- Từ run: `pg-guide.md` (Rules, atomic conditions, giả định `A-xx`), `pg-implementation.md`
  (Changes, Deviations, inventory), `pg-artifact-manifest.md`, `source-manifest.md`, `QA.md`.

Agent đọc: QUALITY_RULES, ARCHITECTURE_RULES, CODING_RULES; file BD/API/DB gốc trong
source-manifest (`CUSTOMER`) để lấy expected — không lấy expected từ RULES tổng hợp (`DERIVED`).

## Thực hiện

1. Ghi Metadata: BD + version, baseline pg-guide (G0), baseline code (repo, branch, commit nếu
   user đã commit, file chưa commit), phương pháp (đọc code, build, test nếu có).
2. Với **từng Rule ID** của pg-guide: ghi nguồn BD (file | sheet | ô), expected theo BD, vị trí
   code thật (file + class/method/template) đã đọc lại ở thời điểm đối chiếu, Status
   `MATCH` / `DEVIATION` / `CONFIRM` / `NOT_IMPLEMENTED`, bằng chứng (đoạn code, build/test).
   Không chép lại từ pg-implementation mà không mở code.
3. Kiểm riêng các mục dễ sót: quyền/role từng API theo API一覧 (policy thật, không chỉ
   `[Authorize]`), validation, message ID/literal, transaction, mock contract, DB constraint
   theo テーブル設計書, UI so với "Layout spec" (ảnh chụp màn cạnh ảnh BD từng state).
4. Mỗi Rule không `MATCH` → một Finding: mô tả lệch, Action `FIX_PG` / `ACCEPT` / `QA` /
   `DEFER`. `FIX_PG` thì sửa code theo chỉ thị user, cập nhật pg-implementation (mục Deviations
   / thay đổi sau G1), build/test, và nêu rõ G1 được mở lại. `QA` thì thêm câu hỏi vào QA.md.
5. Mục "Cơ sở cho Testspec": Rule nào S4 lập case với expected từ BD; Rule chờ quyết định.
6. Bổ sung nguồn mới đã dùng vào source-manifest.md; `kit.py check` đến `READY`.

## Output

- [reconciliation.md](../../workflow/templates/reconciliation.md)
- Cập nhật nếu có: QA.md, source-manifest.md, pg-implementation.md (khi FIX_PG), code (user commit).

## Kiểm tra hoàn thành

Mọi Rule ID của pg-guide có đúng một dòng; Status hợp lệ; Rule đã code có vị trí code thật;
mọi Rule không `MATCH` có Finding với Action; kết luận dựa trên tài liệu `CUSTOMER` hoặc `A-xx`.

## Dừng và bàn giao

Trước khi báo cáo: ghi log công việc cho từng hoạt động của lượt vào `log/作業ログ.xlsx`
(`worklog.py add`, `rules/WORKLOG_RULES.md`) và nêu ID log trong mục Thành phẩm.
Báo cáo bốn mục (AGENTS.md), trình G2: người review xác nhận từng `DEVIATION`/`CONFIRM`
(sửa, chấp nhận hay hỏi Serio) trong chat rồi mới sang S4. Không tự xác nhận, không Git.

## Lỗi thường gặp

Đánh `MATCH` dựa trên tên file/comment thay vì đọc logic; lấy hành vi code làm expected;
bỏ qua phân quyền theo role; dùng RULES tổng hợp thay spec gốc; không tạo Finding cho
`CONFIRM`; sửa code mà không mở lại G1.
