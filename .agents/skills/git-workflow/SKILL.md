---
name: git-workflow
description: Quy định Git cho agent: chỉ đọc trạng thái và bàn giao danh sách file; mọi commit/push/pull/branch do user thực hiện.
---

# Git workflow

## Mục tiêu

Giữ lịch sử Git của repo do con người kiểm soát hoàn toàn. Agent sửa file trong working
tree, báo cáo thay đổi; user review và tự thực hiện mọi thao tác Git.

## Điều kiện chạy

Áp dụng cho mọi lượt làm việc, kể cả khi user gõ "commit", "push", "đẩy code". Khi nhận
yêu cầu như vậy, agent không chạy lệnh mà trả lời bằng danh sách file đã sửa và lệnh gợi ý
để user tự chạy.

## Agent được phép

Chỉ các lệnh đọc, dùng để báo cáo hoặc kiểm tra tiền đề của bước workflow:

- `git status`, `git diff`, `git log`, `git show`
- `git branch --show-current`, `git branch --list`
- `git rev-parse HEAD` (chỉ khi user yêu cầu ghi SHA vào hồ sơ)

## Agent không được phép

Mọi lệnh thay đổi index, lịch sử, branch hoặc remote: `git add`, `commit`, `commit --amend`,
`push`, `pull`, `fetch`, `merge`, `rebase`, `reset`, `revert`, `stash`, `cherry-pick`,
`checkout`/`switch`, `branch` (tạo/xóa/đổi tên), `tag`, `clean`, sửa `.git/config` hoặc
identity. Không có ngoại lệ theo gate đã được user xác nhận, theo skill khác hoặc theo yêu cầu ngắn
trong chat; nếu user muốn agent làm, user phải sửa skill này trước.

## Bàn giao

Cuối lượt, agent liệt kê: file thêm/sửa/xóa (từ `git status --short`), branch hiện tại,
và một thông điệp commit gợi ý. SHA không bắt buộc trong hồ sơ run và không dùng để khóa bước;
chỉ ghi khi user cung cấp hoặc yêu cầu; không bịa SHA.

## Lỗi thường gặp

Chạy `git add`/`commit` vì user nói "commit giúp"; tự đổi branch để "đúng nhánh"; ghi SHA
dự kiến vào manifest; coi gate đã được user xác nhận là quyền commit; xóa file người dùng bằng `git clean`.