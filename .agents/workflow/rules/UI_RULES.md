# Quy tắc UI chung RAS

Tổng hợp từ `【RAS】画面共通仕様説明書.xlsx` (sheet 1.前提条件, 4.画面共通機能, 5.出力仕様,
6.入力仕様), đối chiếu shared components của ras-web khi tổng hợp. Áp dụng cho web; BR_Com_004
thuộc web, không phát triển ứng dụng tablet WinUI chỉ vì tên có tablet. Khi cần xác nhận một
ô, yêu cầu user đưa workbook.

## Layout và component

- Tái dùng shell layout, text-input/select-box/search-icon-button/action-button, message-box
  và shared validators. Feature ở `features/<screen-id>` (vd `br-com-004`), route `BrCom004`,
  API service ở `shared/services`, Request/Response ở `shared/interfaces`, label/message ở
  `assets/i18n/ja.json` (PG_ルール 開発手順書 (Angular); chi tiết CODING_RULES). Màn sample chỉ là minh họa.
- Dropdown lấy giá trị từ danh sách, không gõ tự do. Search icon mở màn/chức năng tìm kiếm.
- Bảng search mặc định tối đa 10 dòng/trang; text canh trái, number canh phải, date và control
  canh giữa. Phân trang theo scope màn, không áp cho mọi màn.
- Date hiển thị yyyy/MM/dd, time HH:mm. Không tự cắt nội dung bằng `…` nếu đặc tả không cho.
  Null/empty, disable/hide/default theo BD từng field.

Căn cứ: 4.画面共通機能!AN14:AN22; 5.出力仕様!G10, D108:D114.

## Message và validation

- Ghi chính xác message/ID/placeholder theo BD và メッセージ一覧; tiếng Nhật です・ます;
  separator theo nguồn, không tự dịch/thay literal.
- Trước đăng ký/cập nhật/xóa có confirmation theo BD. Warning vàng, success modal xanh lá,
  input/check error dưới title nền đỏ, info nền xanh. Error và warning cùng có thì chỉ hiện
  error.
- Shared input hỗ trợ required/numeric/date/past-date/time/max-length. Chỉ gắn constraint
  BD/common spec xác định; DB type không tự tạo required/max length ở UI.
- Common spec cấm chuỗi chứa `<` ngay trước chữ ASCII a–z/A–Z; các cặp `<!`, `</`, `<?`;
  `&#`; hoặc `script` + whitespace + `:`. Áp dụng theo phạm vi trường nguồn ghi; không dùng
  regex phỏng đoán; backend phải kiểm tra, không chỉ frontend.
- Khi spec/config/mock khác nhau, nêu vị trí và giới hạn; expected vẫn từ spec/quyết định.

Căn cứ: 1.前提条件!L35:L38; 5.出力仕様!F19, Z29:Z37, G57, E69, E81, F93; 6.入力仕様!I9:I31.
