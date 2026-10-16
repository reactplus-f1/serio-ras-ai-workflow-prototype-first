# Agent entrypoint — Workflow RAS 0.3.0

Đọc `.agents/workflow/WORKFLOW.md`, `rules/PROJECT_RULES.md`, `rules/SOURCE_MAP.md` và
`config/workflow.json`. Luồng: **BD → Hướng dẫn PG → PG → Testspec → DD → UT → Nghiệm thu**
(S1–S7), human gate G0–G5.

## Nguyên tắc đầu vào

Agent không tự tìm tài liệu. **User ném đầu vào vào đoạn chat** (đính kèm file hoặc đường
dẫn): BD (Excel 画面定義書) ở S1, tài liệu liên quan (API一覧, テーブル設計書, rule, common
spec…) khi bước đó cần, đường dẫn repo code khi bắt đầu PG. Với mỗi file nhận được agent:

1. Lưu một bản vào `runs/<Function-ID>/inputs/<tên file gốc>` (file đính kèm nằm ở thư mục
   tạm; bản trong `inputs/` là bản run làm việc). Nếu đã có file cùng tên nhưng nội dung khác → hỏi
   user, không ghi đè.
2. Ghi tên file + vai trò vào `source-manifest.md`.

Function ID lấy từ tên file BD (`(BR_Com_004)`) hoặc sheet 表紙; user không cần nói "run
mới". `runs/<ID>/task.md` chưa có → agent chạy `kit.py init` rồi làm S1; đã có → tiếp bước
mà `kit.py next` chỉ định.

**Thiếu đầu vào thì hỏi, không đoán.** `rules/SOURCE_MAP.md` chia đầu vào mỗi bước thành
*bắt buộc* và *nếu có*. Thiếu mục bắt buộc (BD, scope ở S1; repo code ở S2; UT rule ở S3;
quyền chạy test ở S5/S6…) → agent nêu rõ thiếu gì và dừng, không tạo hồ sơ nửa chừng. Thiếu mục *nếu có* →
ghi `PENDING` + ảnh hưởng và hỏi trong báo cáo cuối lượt.

**Nội dung mơ hồ thì tự quyết và ghi lại, không dừng.** Khác với thiếu *tài liệu*, một chỗ
trong BD khó hiểu hoặc không nói tới không làm agent dừng: agent chọn cách hiểu hợp lý
nhất, ghi vào bảng "Giả định của AI" trong `pg-guide.md` (`A-xx`: vị trí, các cách hiểu,
lựa chọn, lý do, ảnh hưởng nếu sai) và gắn `[DECISION: A-xx]` vào rule/DD/code dựa trên nó.
Người review chấp nhận hoặc sửa tại gate; AI làm sai thì user yêu cầu làm lại
từ bước/gate chịu ảnh hưởng trong chat.

## Báo cáo cuối lượt

Mỗi lượt kết thúc bằng bốn mục, đúng thứ tự:

1. **Đã làm**: bước, skill, lệnh kit.py đã chạy và kết quả `check`/`next`.
2. **Thành phẩm**: đường dẫn từng file đã tạo/sửa trong `runs/<ID>/` (và trong repo code nếu
   có).
3. **Gate kế tiếp**: tên điểm review G0–G5, điều gì cần người review xem, user xác nhận trong chat rồi mới tiếp tục.
4. **Cần user đưa thêm / câu hỏi**: tài liệu bước sau cần, điểm chưa rõ.

Khi một bước đạt READY, trước khi báo cáo, cập nhật dồn báo cáo Word duy nhất của màn hình
`runs/<ID>/process/報告_<ID>.docx` (WORKFLOW.md "Báo cáo tiến độ"); không tạo file theo bước.

## Vận hành

Hồ sơ của một chức năng nằm ở `runs/<Function-ID>/` trong repo này. Từ root repo chạy
`python .agents/workflow/scripts/kit.py next --task-dir runs/<Function-ID>`; chỉ đọc skill
mà `next` chỉ định và rule chuyên biệt của bước đó. Hồ sơ là Markdown theo `templates/`;
code và raw artifacts ở repo code / nơi user chỉ định, manifest dẫn đường dẫn thật.
Giữ Rule/Condition/Case IDs. Dừng tại điểm review G0–G5; user xác nhận trong chat rồi mới tiếp tục, không tự xác nhận/accept ngoại lệ. `READY`/`PASS` của checker chưa là xác nhận của user.

## Agent không thực hiện thao tác Git

Không `git add`, `commit`, `push`, `pull`, `merge`, `rebase`, `reset`, `stash`,
`checkout`/`switch` hoặc tạo/xóa branch. Chỉ được đọc trạng thái (`status`, `diff`, `log`,
`branch --show-current`) để báo cáo. Kết thúc lượt bằng danh sách file đã sửa để user review
và tự commit. Chi tiết: `.agents/skills/git-workflow/SKILL.md`.

## Giới hạn khác

Yêu cầu bảo trì/sync chỉ sửa workflow/rule/skill; không init/chạy task, viết PG, chạy
build/test/Docker/SQL hoặc thay quyết định review của user. Không copy workbook/deck/PDF, secret, account hay
thông tin kết nối vào thư mục `.agents`; bản sao đầu vào của run chỉ nằm trong
`runs/<ID>/inputs/`. Nếu repo đã có AGENTS.md riêng, giữ hướng dẫn của
repo và ghép phần workflow.
