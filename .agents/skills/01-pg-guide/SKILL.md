---
name: 01-pg-guide
description: S1 — từ BD user đưa, lập hồ sơ run và viết Hướng dẫn triển khai prototype (phân tích BD, rule, giả định, kế hoạch code), dừng tại G0.
---

# Skill 01-pg-guide

## Mục tiêu

Biến BD thành một tài liệu duy nhất mà S2 có thể code theo: BD đã được đọc và index, mọi
nghĩa vụ nghiệp vụ có Rule ID và nguồn, chỗ mơ hồ đã có giả định `A-xx`, và bảng "Kế hoạch
code" nói rõ code gì, ở đâu, tái dùng gì, mock gì. Không viết code ở bước này.

## Điều kiện chạy

User đưa BD và `runs/<Function-ID>/task.md` chưa tồn tại, hoặc `next` chỉ định S1. Nếu
S1 đã READY thì dừng ở G0, trừ khi user đã xác nhận tiếp tục trong chat.

## Input (user đưa)

- **Bắt buộc**: BD Excel 画面定義書 (đính kèm chat hoặc đường dẫn); scope / ngoài scope.
  Thiếu scope → hỏi một câu và dừng, không init.
- **Nếu có**: người phụ trách; API一覧, テーブル設計書, 画面共通仕様説明書, メッセージ一覧,
  BD của màn liên quan (003/005) cho mock contract; quyết định nghiệp vụ đã có. Không có thì
  ghi PENDING trong "Tài liệu cần cho bước sau" và đi tiếp bằng giả định.

Agent đọc: PROJECT_RULES, SOURCE_MAP, UI_RULES, ARCHITECTURE_RULES, REPOSITORY_RULES (cấu
trúc tham chiếu và phần "phải hỏi user"), BR_COM_004_RULES nếu là PoC.

## Thực hiện

0. Lấy Function ID từ tên file BD (`(BR_Com_004)` → `BR_Com_004`) hoặc sheet 表紙. Lưu BD
   vào `runs/<ID>/inputs/<tên file gốc>`, rồi chạy
   `python .agents/workflow/scripts/kit.py init --task-dir runs/<ID> --function-id <ID> --bd runs/<ID>/inputs/<tên file> --scope "<scope>"`.
   Tìm file bằng glob, không gõ tay tên tiếng Nhật. `kit.py next` phải trả `STEP S1`.
1. Xác nhận Function ID, tên chức năng, version/ngày (改訂履歴) và đường dẫn BD khớp task.md.
2. Liệt kê sheet bằng `xlsx_view.py --list`; đọc từng sheet nghiệp vụ (機能概要, 項目定義,
   イベント定義, 画面遷移定義, 画面表示定義, データアクセス定義, エラーチェック一覧,
   機能間引数定義, các sheet `(非表示)`). Ghi **giới hạn**: layout dạng ảnh và text shape
   ngoài ô không đọc được bằng script; nói rõ phần nào cần người xem Excel.
3. Viết `pg-guide.md` theo template, theo thứ tự: BD và phạm vi → sheet đã đọc → luồng event
   → field/validation/state → nhánh lỗi → dữ liệu/API → phụ thuộc/mock → Giả định → Rules →
   Atomic conditions → **Kế hoạch code** → Tài liệu cần cho bước sau. Mỗi dòng có
   `[SRC: …]` hoặc `[DECISION: A-xx]`.
4. Chỗ BD mơ hồ hoặc thiếu: **không dừng hỏi** — chọn cách hiểu hợp lý nhất, ghi `A-xx` với
   các cách hiểu, lựa chọn, lý do, ảnh hưởng nếu sai.
5. Viết `QA.md` theo template: bảng duy nhất `No. | 資料 | シート | 行（セル） | 質問 | 回答`
   (資料 = tên file nguồn đầy đủ kèm phần mở rộng, không dùng mã viết tắt như BD01; 行 = số dòng Excel thật,
   kèm ô và tên mục/No. trong ngoặc, đã đối chiếu bằng `xlsx_view.py` để truy vết được), câu hỏi bằng tiếng
   Nhật để gửi Serio. **Chỉ hỏi nghiệp vụ** (hành vi màn hình, luồng đăng ký, dữ liệu nghiệp
   vụ, quyền sử dụng). **Không** hỏi: xin tài liệu (API一覧, テーブル設計書, ảnh layout, 引数定義,
   người phụ trách), môi trường/tài khoản test, hay chi tiết kỹ thuật hiện thực (endpoint,
   tên bảng, kiểu dữ liệu, HTTP status, transaction) — những thứ đó agent tự quyết theo rules
   và ghi `A-xx` trong pg-guide. Không ghi A-ID, 暫定案, trạng thái hay bản dịch vào QA.md;
   cột 回答 để trống cho Serio điền.
6. Kế hoạch code: mỗi việc gắn Rule ID, vị trí dự kiến theo cấu trúc repo đã biết
   (REPOSITORY_RULES/ARCHITECTURE_RULES; repo thật xác nhận ở S2), tái dùng common nào,
   mock nào. Đủ chi tiết để một dev khác code được mà không mở lại BD.
7. Ghi source-manifest.md: **mọi** nguồn thực sự đọc để ra thiết kế (BD, API一覧, テーブル設計書,
   tài liệu chung, rule nội bộ, source/DB hiện có, tài liệu tổng hợp), kèm đường dẫn, Category
   (`CUSTOMER`/`INTERNAL`/`SOURCE`/`DERIVED`), Version (改訂履歴 Ver./更新日, commit Git) và bước
   dùng. Tài liệu tổng hợp (`DERIVED`) không thay spec gốc. Hoàn thiện task.md (scope,
   người phụ trách, dependency thật/mock). Chưa lập quality-plan: chưa có code để chọn
   module/method đo C1/C2 — việc đó ở S4.
8. Ghi log công việc vào `log/作業ログ.xlsx` (`worklog.py add`, `rules/WORKLOG_RULES.md`; kể cả bản đầu AI tạo, lần sửa và thử thất bại); chạy `kit.py check` đến `READY`, rồi `kit.py next`.

## Output

- [task.md](../../workflow/templates/task.md)
- [pg-guide.md](../../workflow/templates/pg-guide.md)
- [source-manifest.md](../../workflow/templates/source-manifest.md)
- [QA.md](../../workflow/templates/QA.md)

## Kiểm tra hoàn thành

ID/đường dẫn BD/scope đúng; mọi Rule có Source và Required YES/NO; atomic condition trỏ Rule tồn
tại; Kế hoạch code không rỗng và chỉ trỏ Rule tồn tại; mọi giả định có dòng `A-xx` với ảnh
hưởng nếu sai; QA.md có câu hỏi nghiệp vụ (không xin tài liệu, không hỏi kỹ thuật); giới hạn đọc layout được ghi; tài liệu cần cho S2 (repo, API一覧,
テーブル設計書) được liệt kê. `READY` chưa là xác nhận của user.

## Dừng và bàn giao

Báo cáo bốn mục (AGENTS.md): đã làm; thành phẩm (`runs/<ID>/pg-guide.md`, `task.md`,
`source-manifest.md`, `QA.md`, `inputs/<BD>`; mục log L-xxx trong `log/作業ログ.xlsx`); gate G0 — nêu nổi
bật các giả định `A-xx` để người review chấp nhận/sửa; user xác nhận G0 trong chat rồi mới tiếp tục S2. Nêu tài liệu cần
user đưa cho S2. Rồi dừng. Không tự xác nhận, không code, không Git.

## Lỗi thường gặp

Viết code hoặc tạo file trong repo code ở S1; ghi "đã đọc" khi mới thấy tên sheet; dùng giả
định mà không ghi `A-xx`; QA.md hỏi xin tài liệu/môi trường hoặc hỏi kỹ thuật thay vì nghiệp vụ; kế hoạch code chung chung ("implement API") không gắn Rule; suy
rule từ code mẫu; init trỏ vào file đính kèm tạm; đoán scope thay vì hỏi; tự xác nhận G0.
