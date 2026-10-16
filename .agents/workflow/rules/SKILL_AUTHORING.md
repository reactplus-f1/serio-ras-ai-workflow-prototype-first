# Bảo trì skill repository

Mỗi skill có YAML name/description, name khớp thư mục và 8 section: Mục tiêu,
Điều kiện chạy, Input (user đưa), Thực hiện, Output, Kiểm tra hoàn thành, Dừng và bàn giao,
Lỗi thường gặp. Shared rules ở workflow/rules, templates ở workflow/templates.
Không nhân bản rule theo từng agent. Không ghi đường dẫn nguồn/repo cố định vào skill hay
rule: tài liệu do user đưa theo bước, repo code do user đưa ở S2.

Description nhận diện capability, không cấp quyền vượt gate. Mapping theo WORKFLOW/config
0.3.0; không dùng thứ tự 0.2.0 hoặc đổi Kit version của run đã có. Bảo trì/sync không
kích hoạt task. Với yêu cầu không chạy test, chỉ rà tài liệu/config/link/syntax, báo phần
chưa thực thi. Sửa source config/schemas/checker cần scope tương ứng và kiểm chứng phù hợp.
