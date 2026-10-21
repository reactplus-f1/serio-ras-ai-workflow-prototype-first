# Source manifest BR_Com_004

Mọi nguồn thực sự dùng để đưa ra thiết kế (pg-guide.md), code PG (S2) và đối chiếu (S3).
Category: `CUSTOMER` = tài liệu gốc Serio (căn cứ expected); `INTERNAL` = rule nội bộ/workflow;
`SOURCE` = source/DB hiện có của repo (hiện trạng, không phải spec); `DERIVED` = tài liệu tổng
hợp/kết luận tự suy ra — không dùng thay spec gốc. Ngày Excel quy đổi từ serial trong 改訂履歴.

## Files

| ID | Path | Role | Category | Version | Used in |
|---|---|---|---|---|---|
| BD01 | inputs/【RAS】(BR_Com_004)会議室タブレット登録_画面定義書.xlsx | BD chính (画面定義書 BR_Com_004), toàn bộ sheet | CUSTOMER | Ver 1.01, 更新日 2026/07/31 (改訂履歴 C8) | S1, S2, S3 |
| LAY01 | inputs/layout/image3.png | Ảnh レイアウト (初期表示/会議室選択時), trích bằng `xlsx_media.py` từ BD01 → pg-guide 2a Layout spec | DERIVED | Từ BD01 Ver 1.01 (EMF → PNG ×2) | S1 (bổ sung 2026-10-20), S2, S3 |
| LAY02 | inputs/layout/image9.png | Icon 虫眼鏡 ((非表示)レイアウト部品 I11), trích bằng `xlsx_media.py` từ BD01 | DERIVED | Từ BD01 Ver 1.01 | S1 (bổ sung 2026-10-20), S2 |
| API01 | D:\Serio-AI\ras-docs\inputs\serio\【RAS】API一覧.xlsx | Endpoint, method, 利用可能ロール của API_004/005/008 (sheet API一覧 B5:K16) | CUSTOMER | Ver 1.02, 更新日 2026/07/30 (改訂履歴 C9); ras-docs commit c273973 | S2, S3 (S1 chỉ qua RULES01) |
| TBL01 | D:\Serio-AI\ras-docs\inputs\serio\【RAS】テーブル設計書.xlsx | Định nghĩa 会議室マスタ / タブレット管理マスタ / タブレット延長候補会議室マスタ | CUSTOMER | Ver 1.01, 更新日 2026/07/30 (改訂履歴 C8); ras-docs commit c273973 | S2, S3 (S1 chỉ qua RULES01) |
| CODE01 | inputs/【RAS】コーディング規約.xlsx | Coding convention Angular (F1–F9) và C# (B1–B9) | CUSTOMER | Ver 1.00, 更新日 2026/06/29 (表紙/改訂履歴) | S2, S3 |
| PGR01 | inputs/【RAS】PG_ルール.xlsx | PGルール (UTF-8, CRLF, DDL, static analysis), 開発手順書（API）/(Angular) (layer, Mapper, validation, vị trí FE) | CUSTOMER | Không ghi version trong file; bản nhận 2026-10-19 (SHA-256 18232FE761E7…) | S2, S3 |
| SRC01 | D:\Serio-AI\serio-ras | Source hiện có: kiến trúc, auth/policy, shared component, ApiService; nơi code PG | SOURCE | Phân tích S1 trên `main` 966def8; PG trên `bd-to-pg` 47cb3fe (+ README c94321d) và sửa API_008 policy chưa commit | S1, S2, S3 |
| SRC02 | D:\Serio-AI\serio-ras\ras-system\sql\ras_tables.sql | DDL hiện có của 3 bảng (đối chiếu với TBL01) | SOURCE | commit 0be714d | S1, S2 |
| RULES01 | ../../.agents/workflow/rules/BR_COM_004_RULES.md | Bản tra nhanh tổng hợp từ API一覧 / テーブル設計書 / BD003 / BD005 của kit cũ; dùng tạm ở S1 khi chưa có bản gốc (A-16) | DERIVED | Workflow repo commit 7697488 | S1 |
| RULES02 | ../../.agents/workflow/rules/ARCHITECTURE_RULES.md | Quy ước kiến trúc (layer, auth không bypass, citext) | INTERNAL | Workflow 0.3.0, commit 7697488 | S1, S2 |
| RULES03 | ../../.agents/workflow/rules/CODING_RULES.md | Tổng hợp CODE01/PGR01 + config repo (Rule ID trong code, convention check) | INTERNAL | Workflow 0.3.0, commit 7697488 | S2 |
| RULES04 | ../../.agents/workflow/rules/REPOSITORY_RULES.md | Cấu trúc repo serio-ras, lệnh build | INTERNAL | Workflow 0.3.0, commit 7697488 | S2 |
| RULES05 | ../../.agents/workflow/rules/UI_RULES.md | Quy ước màn Angular | INTERNAL | Workflow 0.3.0, commit 7697488 | S2 |
| DRV01 | dependency-analysis.md | Phân tích phụ thuộc BR_Com_003/005, contract mock D-01/D-02 (do user tạo); có trích digest BD003/BD005 của kit cũ (CTX, file gốc không còn) | DERIVED | 2026-10-16 | S1, S2 |

## Ghi chú căn cứ

- Expected nghiệp vụ chỉ lấy từ `CUSTOMER` (BD01, API01, TBL01; CODE01/PGR01 cho convention) hoặc giả định `A-xx` đã được duyệt.
  RULES01 và DRV01 là tài liệu tổng hợp: mọi kết luận lấy từ đó đã được đối chiếu lại với API01/TBL01
  ở S2–S3; phần nào chỉ có trong DRV01 (BD003/BD005) là giả định chờ QA.
- `dependency-analysis.md` §0 ghi API一覧 "v1.01"; bản thực tế đã dùng là Ver 1.02 (API01).
- Chưa dùng (chưa được cung cấp): BD gốc BR_Com_003/BR_Com_005, 画面共通仕様説明書, メッセージ一覧,
  単体テスト仕様書_ルール.
