# Coverage <Function ID>

Inventory lấy từ code thực ở run trong test-report, không chỉ từ UT Design.
C1: tất cả nhánh hợp lệ được thực thi. C2: từng điều kiện Boolean đơn đánh giá thực tế T/F.
Không tính điều kiện bị short-circuit là đã đánh giá. Methods theo quality-plan.md.

## Branches

| Branch ID | Module ID | Location | Outcome | Case IDs | Evidence IDs | Exception ID |
|---|---|---|---|---|---|---|

## Conditions

| Condition ID | Module ID | Location | Expression | True cases | False cases | True evidence | False evidence | Exception ID |
|---|---|---|---|---|---|---|---|---|

Case IDs và Evidence IDs dùng danh sách dấu phẩy, ghép theo vị trí; mỗi evidence là
Evidence ID của case tương ứng trong Results. Không có thì ghi -. True/False evidence
phải chứng minh kết quả đánh giá điều kiện, không chỉ giá trị input. Exception ID dùng -
khi không loại trừ; chỉ loại trừ nguyên branch/condition có quyết định và chứng minh không khả thi.

## Modules

| Module ID | C1 raw | C1 excluded | C1 covered | C2 raw | C2 excluded | C2 covered | Evidence ID |
|---|---|---|---|---|---|---|---|

C1 raw = số branch; C2 raw = 2 × số điều kiện đơn. Covered là số kết quả thực thi
trong phạm vi hiệu lực. Báo riêng raw covered/raw total và covered/(raw-excluded),
không che tỷ lệ nguyên bản bằng tỷ lệ sau loại trừ. Script tính ngưỡng 100% từ counts.
Module không có branch/condition ghi count 0 và N/A trong diễn giải, vẫn có inventory evidence.

## Human verification

Reviewer đối chiếu inventory với toàn bộ scope code/tool và xác nhận evidence đúng run.
Script kiểm tra số liệu/liên kết, không tự chứng minh inventory đầy đủ hoặc assertion đúng.
Thiếu công cụ/evidence thì NOT VERIFIED, không ghi đạt.
