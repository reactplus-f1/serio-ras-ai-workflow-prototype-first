---
name: 05-dd
description: Viết DD tiếng Nhật S5 sau G3, đối chiếu BD/pg-guide/PG/Testspec và trình review G4 (gate DD).
---

# Skill 05-dd

## Mục tiêu

DD tiếng Nhật đúng nghiệp vụ và phản ánh thiết kế thật, kèm findings đối chiếu độc lập.

## Điều kiện chạy

`next` chỉ định S5; user đã xác nhận G3 trong chat và các baseline trước còn hiệu lực. S5 không tự xác nhận DD.

## Input (user đưa)

- **Nếu có**: mẫu 詳細設計書 / API定義書 của Serio (để giữ cấu trúc Serio quen đọc).
- Từ run: pg-guide G0, PG snapshot G1, reconciliation G2, Testspec G3.

Agent đọc: ARCHITECTURE_RULES, UI_RULES, BR_COM_004_RULES; template DD/review.

## Thực hiện

Soạn scope, UI state, event, API/DB, quyền/message/nhánh lỗi với `[SRC]`/`[DECISION]`; giữ
toàn bộ Rules/Required/Condition IDs từ pg-guide. Review chéo BD ↔ pg-guide ↔ PG ↔ Testspec
↔ DD; ghi độ lệch thành finding, không hợp thức hóa PG sai hay sửa expected cho khớp. Nếu
cần đổi source/rule/PG/case, báo người review mở gate sớm nhất trước khi sửa.

## Output

- [DD.md](../../workflow/templates/DD.md)
- [review.md](../../workflow/templates/review.md)

## Kiểm tra hoàn thành

DD tiếng Nhật, nguồn đầy đủ, IDs và mapping giữ nguyên; review không còn finding chặn.
`判定: PASS` của agent chưa là xác nhận DD của user.

## Dừng và bàn giao

Trước khi báo cáo: ghi log công việc cho từng hoạt động của lượt vào `log/作業ログ.xlsx`
(`worklog.py add`, `rules/WORKLOG_RULES.md`) và nêu ID log trong mục Thành phẩm.
Báo cáo bốn mục (AGENTS.md), trình G4 (review DD) và dừng. Chỉ khi user xác nhận G4 trong chat thì DD mới chốt;
S6 bắt đầu sau đó. Không tự xác nhận, không Git.

## Lỗi thường gặp

Đặt DD trước PG/Testspec; gọi DD đã chốt khi user chưa xác nhận G4; thay baseline đã duyệt; tạo chi tiết kỹ
thuật thiếu nguồn.
