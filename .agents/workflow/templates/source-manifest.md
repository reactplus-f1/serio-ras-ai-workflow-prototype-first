# Source manifest <Function ID>

Mọi nguồn **thực sự dùng** để đưa ra thiết kế/code ở S1–S3 (BD, tài liệu chung, API, DB schema,
rule nội bộ, source hiện tại, tài liệu tổng hợp). Không đưa nguồn chưa đọc. Path là đường dẫn
tuyệt đối hoặc tính từ thư mục task; repo source code được ghi bằng thư mục gốc repo. Phải có
BD chính. Thêm nguồn ở bước sau thì bổ sung dòng mới, ghi bước dùng; đổi nguồn đã chốt cần làm
lại từ gate chịu ảnh hưởng.

Category (phân biệt căn cứ):
- `CUSTOMER` — tài liệu gốc khách hàng/Serio (spec gốc, là căn cứ expected).
- `INTERNAL` — rule/quy ước nội bộ của team hoặc workflow (không thay spec gốc).
- `SOURCE` — source code / DB hiện có trong repo (hiện trạng, không phải spec).
- `DERIVED` — tài liệu tổng hợp hoặc kết luận do AI/team tự suy ra; không dùng thay spec gốc,
  mọi kết luận phải truy về nguồn `CUSTOMER` hoặc giả định `A-xx`.

Version: bản/ngày cập nhật ghi trong tài liệu (ví dụ 改訂履歴 Ver.), commit Git của repo, hoặc
ngày sửa file nếu không có phiên bản.

## Files

| ID | Path | Role | Category | Version | Used in |
|---|---|---|---|---|---|
