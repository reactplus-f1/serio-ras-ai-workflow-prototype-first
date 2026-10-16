# Coding rules đã tổng hợp

Tổng hợp từ `【RAS】PG_ルール.xlsx` (sheet PGルール) và config thật của repo RAS
(`.editorconfig` của ras-system và ras-web, `eslint.config.js`, Prettier trong
`package.json`, `tsconfig.json`) tại thời điểm tổng hợp 10/2026. Khi làm PG, **xác nhận lại
trên repo user đưa**; nếu khác, ghi vị trí và áp dụng config của repo.

## Trạng thái nguồn

PGルール!D10,D13,D74:E77: UTF-8, CRLF, phân tích tĩnh không còn warning trước commit.
`【RAS】コーディング規約.xlsx` được tham chiếu tại C57:C58 nhưng chưa nhận được; khi cần,
yêu cầu user đưa. Không tuyên bố đã có toàn bộ coding convention của khách.

## Format theo phạm vi file

| Phạm vi | Quy tắc |
|---|---|
| Backend (ras-system) | UTF-8; CRLF; final newline; bỏ trailing whitespace; indent 4 |
| C# | Indent 4; brace xuống dòng; luôn dùng brace; System using trước và ngoài namespace |
| Project/JSON/YAML/XML, JS/TS/CSS/HTML trong backend | Indent 2 |
| .sh | LF |
| Markdown backend | Không trim trailing whitespace, không giới hạn line length |
| Frontend (ras-web) | UTF-8; indent 2; final newline; trim trailing whitespace; Markdown giữ trailing whitespace |
| TypeScript | Single quote; Prettier singleQuote=true, printWidth=100 |
| HTML | Prettier parser angular |

Frontend editorconfig không khai báo end_of_line; PG rule đặt CRLF làm baseline, ghi căn cứ
khi áp dụng. Không đổi hàng loạt format file cũ; không sửa config gốc để loại warning.

## C# naming và style

- Const, non-private static/readonly: PascalCase. Private field: _camelCase. Local/parameter:
  camelCase. Interface: I + PascalCase. Generic type parameter: T + PascalCase.
- Primitive dùng keyword; khai báo accessibility; `var` chỉ khi type apparent.
  File-scoped namespace là suggestion, không bắt refactor code cũ.
- Giữ severity thật của analyzer (IDE0005/0011/0049/0055/0065/0090/1006 warning; CS8618 silent
  cho migration). Silent không chứng minh nullable đúng; reviewer kiểm tra theo task.
- Comment/XML doc mô tả nghiệp vụ và quyết định cần hiểu khi review.

## Angular và TypeScript

- Component selector `app-…` kebab-case (element); directive selector `app…` camelCase
  (attribute). Giữ feature-based folders và shared components đã có.
- Type-like PascalCase; method/property/parameter camelCase; variable cho phép
  camelCase/UPPER_CASE.
- Ưu tiên `inject()`, signal input/output/model, readonly outputs. Lifecycle hook implements
  interface tương ứng.
- Template ưu tiên `[class]`/`[style]` binding; giữ accessibility rules.
- TypeScript strict, noImplicitReturns/noImplicitOverride/noFallthroughCasesInSwitch, strict
  templates. Không tắt strict để build đạt.
- ESLint của repo chọn config cụ thể; không giả định toàn bộ recommended rules đã bật.

`npm run lint` / `dotnet build` chỉ chạy khi được phép; báo warning/error của đúng commit.
PASS lint không chứng minh convention đầy đủ, nghiệp vụ hay coverage.
