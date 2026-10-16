# Task <Function ID>

| Mục | Giá trị |
|---|---|
| Function ID | <Function ID> |
| Workflow step | Xem `python .agents/workflow/scripts/kit.py next`; không tự chuyển bước |
| Kit version | 0.3.0 |
| BD path | <đường dẫn BD.xlsx user đưa> |
| Tài liệu liên quan | Xem pg-guide.md và source-manifest.md; user đưa theo bước (SOURCE_MAP) |
| Scope | <phạm vi màn hình> |
| Ngoài scope | <phụ thuộc chỉ tham chiếu / mock> |
| Repository / build / test | <đường dẫn repo code, branch, lệnh build/test, tool/version do user đưa ở S2; chưa có ghi PENDING> |
| Dependency thật / mock | <phạm vi và giới hạn; chờ người chốt> |
| Quality target | C1 = 100%, C2 = 100% trong phạm vi hợp lệ được duyệt; case trong kế hoạch phải PASS |

## Người phụ trách

- User chốt nghiệp vụ:
- Dev chốt thiết kế:
- Reviewer UT/code:
- Người nghiệm thu:

## Ghi chú task

Hồ sơ task là Markdown theo config/workflow.json. Code và artifacts ở repo code / nơi user
chỉ định, liên kết qua manifest (đường dẫn). Điểm review G0–G5: user xác nhận trong chat; nguồn đã dùng ở
source-manifest.md; quality-plan.md (S3) ghi phạm vi kiểm thử. Agent không thao tác Git.
