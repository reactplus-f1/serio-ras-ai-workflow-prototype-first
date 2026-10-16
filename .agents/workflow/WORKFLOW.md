# Workflow RAS 0.3.0

Luồng: **BD do Serio cung cấp → Hướng dẫn PG → PG → Testspec → DD → UT → Nghiệm thu**.
Mỗi bước bắt đầu bằng việc **user đưa đầu vào** cho agent; agent tạo hồ sơ Markdown theo
template; user review tại điểm G0–G5 và xác nhận trong chat. Không nhập hoặc migrate run của kit cũ.

## Công đoạn, đầu vào và bàn giao

| Step / skill | User đưa vào | Agent làm | Output Markdown | Gate |
|---|---|---|---|---|
| S1 / 01-pg-guide | BD (.xlsx), scope; nếu có: người phụ trách, API一覧, テーブル設計書, tài liệu chung | Init run, đọc BD, lập Rule/Condition IDs, ghi giả định `A-xx` chỗ mơ hồ, viết **Hướng dẫn triển khai prototype** (code gì, ở đâu, mock gì), lập QA nghiệp vụ gửi Serio | task.md, pg-guide.md, source-manifest.md, QA.md | G0: hướng dẫn PG và giả định |
| S2 / 02-pg | Đường dẫn repo code, branch, quyền build/lint; API一覧, テーブル設計書 | Code PG theo kế hoạch của pg-guide, build/lint, kiểm kê branch/condition, liệt kê file | pg-implementation.md, pg-artifact-manifest.md + code | G1: user review code |
| S3 / 03-testspec | 単体テスト仕様書_ルール; mẫu UT nếu có | Lập kế hoạch chất lượng (module theo code PG, method đo C1/C2 đã thử trên stack), thiết kế case/expected từ BD và pg-guide đã duyệt, decision table, readiness | quality-plan.md, ut-design.md, decision-table.md | G2: Testspec |
| S4 / 04-dd | Mẫu DD/API定義書 của Serio (nếu có) | Viết DD tiếng Nhật, đối chiếu BD/pg-guide/PG/Testspec, lập findings | DD.md, review.md | G3: DD |
| S5 / 05-ut-code | Quyền chạy test project, dữ liệu test | Viết UT theo Testspec, review code/assertion, snapshot cuối | implementation.md, code-review.md, artifact-manifest.md + test code | G4: code/UT |
| S6 / 06-test-evidence | 単体テスト実施_ルール; môi trường/DB/tool coverage, quyền chạy | Chạy UT, thu kết quả/C1/C2/truy vết | test-report.md, coverage.md, traceability.md, exceptions.md, evidence-manifest.md | (chuẩn bị G5) |
| S7 / 07-acceptance | — | Review chất lượng, evidence, khả năng tái hiện | acceptance.md | G5: nghiệm thu |

S1 gộp việc đọc BD, phân tích và lập kế hoạch code vào một tài liệu (`pg-guide.md`) để S2
code ngay sau một gate. PG ở S2 không chờ DD. Testspec ở S3 lấy expected từ BD và pg-guide
đã duyệt, không từ hành vi PG; PG chỉ dùng để tìm nhánh/điều kiện kỹ thuật cần đo. S4 mô tả
thiết kế đã đối chiếu và ghi độ lệch, không hợp thức hóa code sai; G3 là mốc review DD độc
lập (tương ứng đầu việc "tạo và review DD"). S6 không có gate riêng.

## Vận hành một lượt

1. User mở phiên bằng `START_CHAT.md` và ném đầu vào của bước vào chat. Agent lưu file vào
   `runs/<Function-ID>/inputs/`; chưa có `task.md` → `kit.py init` từ BD rồi làm S1.
2. Agent chạy `python .agents/workflow/scripts/kit.py next --task-dir runs/<Function-ID>`.
3. `next` báo bước chưa hoàn thành kế tiếp hoặc `COMPLETE`. Agent kiểm tra đầu vào bắt buộc của bước (SOURCE_MAP); thiếu thì
   hỏi và dừng. Đủ thì đọc đúng skill đó và rule theo `SOURCE_MAP.md`, tạo hồ sơ,
   chạy `check` đến `READY`. Khi hồ sơ READY, kit có thể in dòng thông tin review point Gx; agent bàn giao và dừng.
4. Agent ghi mọi tài liệu đã dùng (tên file, vai trò) vào `source-manifest.md`;
   tài liệu *nếu có* còn thiếu ghi `PENDING` + ảnh hưởng vào pg-guide ("Tài liệu cần cho
   bước sau").
5. Agent kết thúc bằng báo cáo bốn mục (AGENTS.md): đã làm, thành phẩm ở đâu, gate kế tiếp,
   cần user đưa thêm.
6. Agent cập nhật **báo cáo tiến độ Word** của màn hình (xem "Báo cáo tiến độ") rồi dừng.
7. User review; nếu đồng ý thì nhắn xác nhận/"tiếp tục" trong chat để mở lượt tiếp theo. Nếu sai, user yêu cầu làm lại từ bước/gate chịu ảnh hưởng.

Agent không tự xác nhận review, không chấp nhận finding/ngoại lệ, không vượt điểm review khi chưa có xác nhận trong chat,
không thao tác Git (skill git-workflow). Bảo trì workflow không kích hoạt task.

## Báo cáo tiến độ (Word)

Mỗi màn hình có **một** file báo cáo quản lý `runs/<Function-ID>/process/報告_<Function-ID>.docx`
(tiếng Việt, cho PA1/ticket). Không tạo file riêng theo bước (không `S1_報告…`, `…_S1-S2`).
Sau mỗi bước hoàn thành (check READY) agent cập nhật dồn vào file này:

- Bảng đầu: Bước / trạng thái hiện tại, ngày thực hiện từng bước, kết quả checker, thư mục hồ sơ.
- Mục 1 Checklist ticket (bổ sung bằng chứng của bước mới), mục 2 Đầu vào đã dùng (thêm tài liệu mới nhận).
- Một mục "Thành phẩm bước N (Sx)" cho mỗi bước đã làm; mục Công số (#9) cộng dồn; mục
  "Điểm cần user quyết định tại review Gx" theo gate đang chờ; mục cuối "Bước tiếp theo".
- Mục của bước cũ giữ nguyên, chỉ sửa khi làm lại từ gate đó.

File sinh bằng script `runs/<Function-ID>/process/make_report.py` (python-docx); agent sửa
script rồi chạy lại để ghi đè `.docx`, không sửa tay file Word. Hồ sơ chính thức vẫn là `.md`.

## Sửa sau review

| Thay đổi | Gate sớm nhất chịu ảnh hưởng |
|---|---|
| BD/nguồn, scope, phương pháp quality, Rule/Condition, giả định `A-xx`, kế hoạch code | G0 |
| PG hoặc config/snapshot PG | G1 |
| Case/expected/decision table | G2 |
| DD | G3 |
| UT code/assertion hoặc snapshot cuối | G4 |
| Kết quả/evidence hoặc acceptance | G5 |

User yêu cầu làm lại từ gate đó và các gate sau trước khi sửa bản đã chốt. Giữ lịch sử,
không xóa output cũ để vượt kiểm tra. Sửa PG khi đang UT thì mở G1, không chỉ G4. Không sửa
pg-implementation/pg-manifest đã chốt tại G1; snapshot cuối ghi ở S5.

## Chất lượng và tái hiện

Mục tiêu C1 = C2 = 100% trong phạm vi hợp lệ người review xác nhận; mọi case đã duyệt phải
PASS. Mỗi lượt ghi process log (input/prompt/tool/model, thời gian thật) để quy trình AI tái
hiện được và so sánh công số giữa các 方式.
