# Đầu vào theo bước và rule cần đọc

Agent không tự tìm tài liệu. Bảng dưới nói **user cần đưa gì** ở mỗi bước và agent đọc
rule tổng hợp nào. Mỗi file nhận được lưu vào `runs/<ID>/inputs/` và ghi source-manifest
(tên file, vai trò).

- **Bắt buộc**: thiếu thì agent nêu rõ thiếu gì, hỏi user và dừng; không tạo hồ sơ bước đó.
- **Nếu có**: thiếu thì ghi PENDING trong pg-guide ("Tài liệu cần cho bước sau"), nêu ảnh
  hưởng và hỏi cuối lượt.

| Bước | Bắt buộc | Nếu có | Rule agent đọc |
|---|---|---|---|
| S1 Hướng dẫn PG | BD (.xlsx); scope | Người phụ trách; API一覧, テーブル設計書; 画面共通仕様説明書, メッセージ一覧; BD của màn liên quan (003/005) cho mock contract; quyết định nghiệp vụ đã có | UI_RULES, ARCHITECTURE_RULES, REPOSITORY_RULES (cấu trúc tham chiếu, phần tiền đề), BR_COM_004_RULES nếu là PoC |
| S2 PG | Đường dẫn repo code + branch; quyền build/lint; API一覧, テーブル設計書 | PG_ルール, APアーキテクチャ設計 | CODING_RULES, ARCHITECTURE_RULES, REPOSITORY_RULES, UI_RULES (nếu frontend) |
| S3 Testspec | 単体テスト仕様書_ルール | Mẫu UT/decision table của Serio | QUALITY_RULES, QUALITY_RECORDS |
| S4 DD | — | Mẫu 詳細設計書/API定義書 của Serio | ARCHITECTURE_RULES, UI_RULES, BR_COM_004_RULES |
| S5 UT code | Quyền chạy test project; dữ liệu test | — | CODING_RULES, QUALITY_RULES, QUALITY_RECORDS |
| S6 Evidence | 単体テスト実施_ルール; môi trường/DB/tool coverage; quyền chạy | — | QUALITY_RULES, QUALITY_RECORDS |
| S7 Acceptance | — | — | QUALITY_RULES, QUALITY_RECORDS |

Tài liệu đã đưa ở bước trước không cần đưa lại; agent đọc từ `runs/<ID>/inputs/` theo
source-manifest.

Rule tổng hợp là bản tra nhanh, ghi tên tài liệu/sheet/ô gốc. Khi cần xác nhận một ô, một
mâu thuẫn hoặc một phiên bản mới, agent **yêu cầu user đưa tài liệu gốc** rồi mới kết luận;
không mặc định bản tổng hợp mới hơn BD. Không copy tài liệu nguồn, credential hay settings
vào `.agents`.
