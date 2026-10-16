# Quy tắc ghi log công việc (作業ログ)

Áp dụng cho mọi phiên agent và người phụ trách. Mục đích: tái hiện và kiểm tra quy trình AI.
Đây là nơi duy nhất ghi lịch sử/tiến độ làm việc (không có báo cáo riêng theo màn).

## Nơi ghi

- **Một file log chung**: `log/作業ログ.xlsx` (root repo workflow), cho mọi ticket/chức năng và
  mọi lần chỉnh workflow. Không dùng log Markdown, không tạo log hay báo cáo riêng theo bước/run.
- Mẫu: `log/作業ログ_template.xlsx`. Excel hai sheet, cùng 17 cột (hàng 1 là tiêu đề:
  ID + 17 mục bên dưới), mỗi hoạt động một dòng; ID `L-xxx` đánh số chung cho cả hai sheet:
  - **Hiệu chỉnh workflow** (key JSON `"log": "workflow"`): chỉnh workflow, quy trình, rule,
    skill, template, script, format log.
  - **Tạo thành phẩm** (`"log": "output"`): tạo/hiệu chỉnh/tạo lại/thử thất bại thành phẩm của
    bước S1–S8 (hồ sơ run, code, hướng dẫn test) và chỉnh môi trường test cho run.
  - Một lượt có cả hai loại thì ghi hai mục; không tách được thì ghi vào sheet của phần chính. File chỉ chứa dữ liệu log; nội dung cần ghi và quy tắc nằm
  ở file này, không chép vào Excel.
- Agent ghi bằng script:

```powershell
python .agents/workflow/scripts/worklog.py add --json <entry.json>   # thêm L-xxx
python .agents/workflow/scripts/worklog.py set --id L-003 --field status --value "Thất bại"
python .agents/workflow/scripts/worklog.py list                      # liệt kê + tổng phút
python .agents/workflow/scripts/worklog.py template                  # dựng lại file mẫu
```

  Người phụ trách được sửa trực tiếp trong Excel (đóng Excel trước khi agent chạy script); không
  đổi tên/thứ tự cột hàng 1.
  JSON truyền bằng file UTF-8 (không pipe từ PowerShell vì lỗi mã hóa tiếng Việt).

## Khi nào phải ghi

Ngay sau **mỗi hoạt động tạo thay đổi**, trước báo cáo cuối lượt — không gộp vào cuối ngày:

- Chạy một bước workflow (S1–S8) tạo thành phẩm, kể cả lượt bị dừng vì thiếu đầu vào hoặc kẹt gate.
- Hiệu chỉnh hoặc tạo lại thành phẩm (hồ sơ run, code, hướng dẫn) theo yêu cầu/review của user.
- Thử thất bại (build/test/lệnh lỗi, kết quả bị user từ chối).
- Chỉnh workflow, quy trình, rule, skill, template, script.
- Chỉnh repo code hoặc môi trường (config, DB, container) ngoài bước.

**Không ghi**: hỏi đáp, giải thích, trao đổi trong chat không làm thay đổi file/môi trường.
Kết quả review/test của user ghi vào mục 12 của hoạt động tương ứng, không tạo mục riêng.
Một lượt chat có nhiều hoạt động tách biệt thì ghi nhiều mục.

## Cách viết mục 7 (Yêu cầu / chỉ thị)

Ghi dưới dạng **chỉ thị chuyên môn** do agent biên tập từ yêu cầu của user, không chép
nguyên văn hội thoại, không dạng hỏi/nhờ giúp. Câu mệnh lệnh nêu: hành động — đối tượng (file,
bước, skill) — phạm vi/ràng buộc — tiêu chí hoàn thành. Ví dụ:

- Không viết: "tạo giúp tôi 1 file md hướng dẫn chạy môi trường fe và be để test"
- Viết: "Lập hướng dẫn khởi động môi trường test (DB, BE, FE) dùng chung cho dự án trong
  serio-ras/README.md: lệnh sao chép được, thư mục chạy từng lệnh; tách kịch bản riêng
  BR_Com_004 sang test-guide.md."

Các mục khác cũng viết văn phong báo cáo (không trích lời chat).

## Nội dung cần ghi (17 mục, key JSON)

Mục đích bổ sung (review PoC 2.5): người khác chạy lại được từng bước và tổng kết PoC bằng số
liệu thời gian đáng tin cậy.

| # | Mục | Key |
|---|---|---|
| 1 | Ngày và thời gian thực hiện, bắt đầu–kết thúc (giờ +07:00) | `time` (`YYYY-MM-DD HH:MM–HH:MM`) |
| 2 | Run ID | `run_id` (`<Function-ID>-S<n>-<yyyymmdd-HHMM>`; chỉnh workflow: `WF-<yyyymmdd-HHMM>`) |
| 3 | Người thực hiện (người chỉ thị/review và AI thực hiện) | `people` |
| 4 | Ticket hoặc nội dung công việc liên quan | `ticket` |
| 5 | Loại hoạt động | `type`: Chạy bước (AI tạo mới) / Hiệu chỉnh / Tạo lại / Thử thất bại / Chỉnh workflow / Chỉnh repo code / môi trường |
| 6 | Tài liệu hoặc code đầu vào (tên file đầy đủ, phiên bản/commit nếu có) | `inputs` |
| 7 | Yêu cầu / chỉ thị gửi AI (dạng chỉ thị chuyên môn, xem trên) | `prompt` |
| 8 | Công cụ AI và model (nếu xác định được) | `tool` |
| 9 | Lệnh đã chạy và kết quả: thư mục chạy, lệnh, exit code, kết quả rút gọn | `commands` |
| 10 | Kết quả ban đầu do AI tạo | `ai_result` |
| 11 | Nội dung con người đã hiệu chỉnh, bổ sung hoặc loại bỏ | `human_changes` |
| 12 | Kết quả review và test | `review` |
| 13 | Trạng thái: Thành công / Thất bại / Cần thực hiện lại | `status` (bắt đầu bằng một trong ba giá trị) |
| 14 | Thời gian AI xử lý (phút) | `time_ai` |
| 15 | Thời gian review thủ công (phút) | `time_review` |
| 16 | Thời gian sửa lại (phút) | `time_rework` |
| 17 | Ghi chú hoặc vấn đề phát sinh — ngắn gọn, một ý/dòng, không lặp nội dung các mục khác | `notes` |

Mục không có nội dung ghi `—`; script từ chối entry thiếu key. Mục 14–16 là số phút, hoặc
`chờ user ghi`, hoặc `— (lý do)`; `worklog.py list` in tổng phút từng loại.

## Quy tắc ghi log

- Ghi lại bản đầu tiên do AI tạo (mục 10), kể cả khi sau đó bị sửa.
- Ghi lại các lần hiệu chỉnh, tạo lại và thử thất bại — mỗi lần một mục, Run ID mới; mục trước
  đó đổi Trạng thái thành `Cần thực hiện lại`/`Thất bại` và ghi ở mục 11 ai yêu cầu sửa gì.
  Không xóa mục cũ.
- Ghi rõ người thực hiện cho từng hoạt động.
- Mục 9 ghi đủ để chạy lại: thư mục làm việc, lệnh nguyên văn (kit.py, build, test, script),
  exit code và kết quả (ví dụ `13/13 Passed`). Lệnh lỗi cũng ghi.
- Thời gian, tách riêng, không cộng trùng một khoảng thời gian:
  - **AI xử lý**: từ lúc gửi chỉ thị đến khi AI bàn giao (kể cả thời gian chờ AI). Agent tự đo
    (giờ nhận chỉ thị → giờ kết thúc lượt).
  - **Review thủ công**: thời gian người phụ trách đọc/kiểm tra/test kết quả.
  - **Sửa lại**: thời gian hiệu chỉnh sau review (người và AI) của chính hoạt động này.
  - Review/sửa lại do người phụ trách cung cấp; chưa có thì ghi `chờ user ghi`, cập nhật sau bằng
    `worklog.py set --id L-xxx --field time_review --value <phút>` hoặc sửa trực tiếp trong Excel.
  - Người thực hiện làm việc khác trong lúc chờ AI thì không tính khoảng đó vào review/sửa lại.
- Mục ghi trước khi áp dụng tiêu chuẩn này: Run ID/lệnh ghi `— (mục cũ…)`. Thời gian L-001–L-019
  tái dựng từ timestamp phiên agent: AI = từ chỉ thị đến sự kiện cuối của AI; review = khoảng chờ
  đến chỉ thị kế tiếp (>30 phút coi là rời phiên, ghi `— (rời phiên)`); sửa lại = thời gian AI
  của các lượt hiệu chỉnh.
- Không ghi secrets, mật khẩu, chuỗi kết nối.
