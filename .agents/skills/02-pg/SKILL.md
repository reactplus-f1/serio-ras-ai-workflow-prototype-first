---
name: 02-pg
description: S2 — code prototype trong repo user đưa sau khi user đã xác nhận G0 trong chat; dừng G1 để user review code.
---

# Skill 02-pg

## Mục tiêu

Triển khai đúng những gì "Kế hoạch code" của `pg-guide.md` nói, giữ Rule IDs trong code, có
build/lint thật và danh sách file đã sửa để user review tại G1. Review code là việc của user; agent
không viết review riêng.

## Điều kiện chạy

`next` chỉ định S2; user đã xác nhận G0 trong chat. **User đã đưa**: đường dẫn repo code, branch
được giao, quyền build/lint, API一覧, テーブル設計書. Thiếu → nêu rõ, hỏi và dừng; không đoán.
Không cần DD/Testspec ở bước này.

## Input (user đưa)

- **Bắt buộc**: repo code + branch; quyền build/lint; API一覧, テーブル設計書 (nếu chưa đưa ở
  S1). Xác nhận cấu trúc thật theo REPOSITORY_RULES và ghi vào task.md.
- **Nếu có**: PG_ルール, APアーキテクチャ設計.
- Từ run: `pg-guide.md` đã được user xác nhận ở G0 (kể cả giả định `A-xx` đã được chấp nhận/sửa).

Agent đọc: CODING_RULES, ARCHITECTURE_RULES, REPOSITORY_RULES; UI_RULES nếu frontend;
BR_COM_004_RULES nếu PoC. Config/code thật của module trong repo user đưa.

## Thực hiện

1. Chạy `git -C <repo> branch --show-current`; khác branch user giao → dừng và báo.
2. Đối chiếu "Vị trí dự kiến" của kế hoạch code với cấu trúc thật; lệch thì ghi vị trí
   thật vào pg-implementation, không sửa pg-guide đã duyệt.
3. Code theo từng dòng kế hoạch; mỗi điểm code ghi Rule ID (comment hoặc tên). Tái dùng
   common API/auth/messages/validators; mock đúng contract đã ghi. Phát hiện BD/guide thiếu
   khi code → ghi giả định mới `A-xx` trong pg-implementation (mục "Giả định phát sinh"),
   không dừng.
4. Build/lint khi được phép, ghi kết quả thật; không deploy, không chạy SQL seed.
5. Kiểm kê branch/atomic condition thực tế trong code cho S3.
6. Lập pg-artifact-manifest liệt kê từng file đã sửa. **Không commit**: liệt kê file để
   user commit. Code commit là tùy chọn, không dùng để khóa S2; chỉ ghi SHA nếu user cung cấp.
   Không bịa commit.
7. Ghi process log; `kit.py check` đến `READY`.

## Output

- [pg-implementation.md](../../workflow/templates/pg-implementation.md)
- [pg-artifact-manifest.md](../../workflow/templates/pg-artifact-manifest.md)
- Code trong repo user đưa (user commit).

## Kiểm tra hoàn thành

Mọi dòng kế hoạch code có trạng thái (xong / lệch / không làm + lý do); mapping Rule→file;
build/lint kết quả thật; real/mock rõ; danh sách file đầy đủ. PASS lint không chứng minh
nghiệp vụ.

## Dừng và bàn giao

Báo cáo bốn mục (AGENTS.md), trình G1 và dừng: danh sách file để user commit và review.
User thấy code sai → yêu cầu làm lại từ G1 trong chat.
G1 không cho phép merge/push/deploy. Không tự xác nhận, không Git.

## Lỗi thường gặp

Code ngoài kế hoạch đã duyệt mà không ghi lệch; chờ DD mới bắt đầu; tự tìm repo trên máy;
viết full related features thay mock; tắt lint; tự commit hoặc bịa commit; sửa pg-guide đã
duyệt.
