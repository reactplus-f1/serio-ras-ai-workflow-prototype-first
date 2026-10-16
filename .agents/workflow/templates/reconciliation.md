# Reconciliation <Function ID> (BD ↔ PG)

Đối chiếu từng Rule của `pg-guide.md` (đã xác nhận G0) với code PG (đã xác nhận G1) trước khi
lập Testspec. Expected luôn lấy từ BD/pg-guide; code chỉ là đối tượng được kiểm tra, không
dùng để hợp thức hóa hành vi lệch.

## Metadata

| Item | Value |
|---|---|
| BD | |
| pg-guide baseline | |
| Code baseline | |
| Phương pháp | |

## Rule reconciliation

Status: `MATCH` (code khớp BD) / `DEVIATION` (code khác BD) / `CONFIRM` (BD mơ hồ hoặc
dựa trên giả định A-xx chưa được Serio trả lời) / `NOT_IMPLEMENTED` (chưa code).
Mọi Rule ID trong pg-guide phải có đúng một dòng.

| Rule ID | BD source | BD expected | Code location | Status | Evidence / note |
|---|---|---|---|---|---|

## Findings

Mỗi Rule có Status khác `MATCH` cần ít nhất một Finding. Action: `FIX_PG` (sửa code, mở lại
G1), `ACCEPT` (giữ lệch, cần quyết định của người review trong chat), `QA` (hỏi Serio qua
QA.md), `DEFER` (để bước/màn sau, nêu lý do).

| Finding ID | Rule ID | Kind | Description | Action | Decision / reference |
|---|---|---|---|---|---|

## Cơ sở cho Testspec

Ghi Rule nào S4 được lập case với expected từ BD, Rule nào chờ quyết định (CONFIRM/QA) và
giới hạn real/mock.
