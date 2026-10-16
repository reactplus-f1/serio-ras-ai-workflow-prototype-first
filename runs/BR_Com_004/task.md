# Task BR_Com_004

| Mục | Giá trị |
|---|---|
| Function ID | BR_Com_004 |
| Workflow step | Xem `python .agents/workflow/scripts/kit.py next`; không tự chuyển bước |
| Kit version | 0.3.0 |
| BD path | inputs/【RAS】(BR_Com_004)会議室タブレット登録_画面定義書.xlsx |
| Tài liệu liên quan | Xem pg-guide.md và source-manifest.md; user đưa theo bước (SOURCE_MAP) |
| Scope | Chức năng chính của BR_Com_004 会議室タブレット登録; BR_Com_003 会議室検索 và BR_Com_005 一括予約エラー表示 gọi dưới dạng mock |
| Ngoài scope | BR_Com_003 会議室検索 (child screen) và BR_Com_005 一括予約エラー表示: chỉ mock theo contract trong pg-guide §7; BR_Com_002 chỉ tham khảo; không làm tablet app WinUI / batch. Đã xác nhận G0 trong chat (2026-10-16) |
| Repository / build / test | `D:\Serio-AI\serio-ras` (reactplus-f1/serio-ras), branch `bd-to-pg` (xác nhận ở S2). Build: `dotnet build ras-system/src/Services/Ras/RasApi/RasApi.csproj`; `npx ng build --configuration development` (ras-web). Chạy local DB/BE/FE: `serio-ras/README.md` mục "Chạy môi trường local". UT project: ras-system/src/Services/Ras/RasApi.UnitTests (S6) |
| Dependency thật / mock | Thật: API_004/005/008, EF Core/PostgreSQL cho rooms_mst/tablets_mst/candidate_rooms_mst, auth/policy hiện có của repo (A-17). Mock: BR_Com_003, BR_Com_005. Đã xác nhận G0 trong chat (2026-10-16) |
| Quality target | C1 = 100%, C2 = 100% trong phạm vi hợp lệ được người review chốt; mọi case trong kế hoạch phải PASS |

## Người phụ trách

- User chốt nghiệp vụ: chưa ghi
- Dev chốt thiết kế: chưa ghi
- Reviewer UT/code: chưa ghi
- Người nghiệm thu: chưa ghi

## Ghi chú task

Hồ sơ task là Markdown theo config/workflow.json. Code và artifacts ở repo code / nơi user
chỉ định, liên kết qua manifest (đường dẫn). Điểm review G0–G6: user xác nhận trong chat; nguồn đã dùng ở
source-manifest.md; quality-plan.md (S4) ghi phạm vi kiểm thử. Agent không thao tác Git.
