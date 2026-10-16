# Bắt đầu với agent

Đọc AGENTS.md, .agents/workflow/WORKFLOW.md, rules/PROJECT_RULES.md, rules/SOURCE_MAP.md,
config/workflow.json. Xác định run từ file user đưa (Function ID trong tên BD hoặc sheet
表紙) hoặc từ run user nêu; lưu file nhận được vào `runs/<ID>/inputs/`. Chưa có
`runs/<ID>/task.md` → đọc skill 01-pg-guide (bắt đầu bằng `kit.py init`). Đã có → chạy
`kit.py next` để biết bước và skill được phép; chỉ đọc skill đó.

Đầu vào của bước do user đưa trong lượt chat. Agent kiểm tra tên file và phiên bản,
ghi vào source-manifest.md. Thiếu đầu vào *bắt buộc* của bước (SOURCE_MAP) → hỏi và dừng;
thiếu đầu vào *nếu có* → ghi PENDING, nêu ảnh hưởng và hỏi cuối lượt. Không tự tìm tài
liệu. Nội dung BD mơ hồ → tự chọn, ghi giả định `A-xx` trong pg-guide.md, không dừng.

Hồ sơ là Markdown; giữ Rule/Condition/Case IDs; run/evidence phải thật; user tự commit. Dừng tại
điểm review G0–G6 để người review xác nhận trong chat; không tự xác nhận, không thao tác Git. Kết thúc
lượt bằng báo cáo bốn mục (AGENTS.md): đã làm, thành phẩm ở đâu, gate kế tiếp, cần user đưa
thêm.
Sau mỗi hoạt động tạo thay đổi (chạy bước, hiệu chỉnh, tạo lại, thử thất bại, chỉnh workflow/skill,
chỉnh repo code/môi trường; không ghi hỏi đáp; mục yêu cầu viết dạng chỉ thị chuyên môn) ghi
một mục vào `log/作業ログ.xlsx` bằng `worklog.py add` theo `rules/WORKLOG_RULES.md`.

Luồng: BD → Hướng dẫn PG → PG → Đối chiếu BD↔PG → Testspec → DD → UT → Nghiệm thu (S1–S8, gate G0–G6). BR_Com_004 chỉ triển khai
chức năng chính; BR_Com_003/005 gọi dưới dạng mock theo scope đã chốt.
Yêu cầu sync/review tài liệu là bảo trì, không kích hoạt công đoạn task.
