**Báo cáo cá nhân — Nguyễn Tiến Đạt — 2A202603922**
## 1. Thông tin thành viên

- Họ tên: Nguyễn Tiến Đạt
- MSSV: 2A202603922
- Email: ntdkhongdeptrailam5924@gmail.com
- GitHub: duhocsinh4to10

## 2. Phần việc phụ trách

CP3 — Tool mới :

- Tạo tool `datetime_window`: `tools/datetime_window/tool.py` + `TOOL.md` + đăng ký trong `tools/__init__.py`.
- Parse timeframe tiếng Anh (`last 7 days`, `yesterday`, `this week`...) và trả `error dict` khi input xấu.
- Scaffold UI Streamlit (`app.py`) và thêm dependency `streamlit` vào `requirements.txt`.
- Nhắn Nghị mô tả tool (tên, params, khi nào dùng) để đưa vào `tools.yaml` và `system_prompt.md`.

## 3. Đóng góp cụ thể

### Tool `datetime_window` — đóng góp kỹ thuật chính

File: `starter_v0/tools/datetime_window/tool.py`

Tự viết phần lõi của tool:

- Hàm `datetime_window(timeframe, reference_date, tz)` nhận chuỗi mô tả thời gian tiếng Anh.
- Dùng `re.fullmatch` để parse pattern `"last/past N unit"` và `"N unit ago"`.
- Xử lý các keyword cố định: `today`, `yesterday`, `this week`, `last week`, `this month`, `last month`.
- Trả về dict gồm `start`, `end`, `label`, `duration_days`, `timeframe_code`.
- Trả `{"error": "..."}` với mọi input xấu — không raise exception.

Ví dụ output:

```json
{
  "start": "2026-11-03T12:00:00+00:00",
  "end":   "2026-11-10T12:00:00+00:00",
  "label": "last 7 days",
  "duration_days": 7.0,
  "timeframe_code": "7d"
}
```

**Vấn đề gặp phải:** Ban đầu tạo thêm folder `dattask/` (wrapper + TOOL.md) nhưng TOOL.md bị lệch contract (chứa backtick khiến `test_tool_contract.py` fail). Đã xoá folder này sau khi phát hiện lỗi.

### Unit tests

File: `starter_v0/tests/test_tools_todo.py`

19 test cho `datetime_window` được viết với sự hỗ trợ của AI (Antigravity), bao gồm:
- Happy path: các pattern hợp lệ (`last 7 days`, `yesterday`, `this week`...).
- Input xấu: empty string, None, số thay string, timezone sai.
- Error branch: xác nhận tool không raise, trả đúng `{"error": "..."}`.

Kết quả: **19 passed, 0 failed**.

### Scaffold UI Streamlit

File: `starter_v0/app.py` — được tạo với sự hỗ trợ của AI, tích hợp với `run_model_tool_loop` từ `chat.py`.

## 4. Bằng chứng

**File đã tạo/sửa:**

- `starter_v0/tools/datetime_window/tool.py` — code lõi tool
- `starter_v0/tools/datetime_window/TOOL.md` — contract (frontmatter YAML hợp lệ)
- `starter_v0/tools/__init__.py` — đăng ký `datetime_window`
- `starter_v0/tests/test_tools_todo.py` — 19 test datetime_window
- `starter_v0/app.py` — Streamlit UI
- `starter_v0/requirements.txt` — thêm `streamlit>=1.35.0`

> SHA commit: (điền sau khi push — `git log --oneline -5`)

**Pytest output (toàn suite):**

```
114 passed, 14 skipped, 0 failed
```

**AI/công cụ đã dùng và cách tự kiểm tra:**

- Dùng **Antigravity (Claude Sonnet)** để: hỗ trợ viết test, scaffold app.py, debug lỗi TOOL.md lệch contract.
- Phần **tự làm**: logic hàm `datetime_window` trong `tool.py`, đọc hiểu từng nhánh code và giải thích được.
- Tự kiểm tra: chạy `pytest -k datetime_window` xác nhận 0 failed; giải thích được vì sao `yesterday` có `end = midnight` thay vì `now`; vì sao dùng `reference_date` cố định trong test để kết quả deterministic.

## 5. Tự đánh giá

**Học được:**

- Phân biệt **unit test** (đo code tool) vs **eval** (đo lựa chọn model): model gọi đúng tool nhưng tool tính sai ngày → eval pass, user nhận kết quả sai.
- Tool nên trả `error dict` thay vì raise để model có thể phục hồi thay vì crash cả lượt.
- TOOL.md phải có YAML frontmatter sạch (không được có backtick `` ` `` trong phần body nếu test parse cả file).

**Hạn chế thật sự:**

- Chưa hỗ trợ tiếng Việt tự nhiên ("tuần trước", "hôm qua") — chỉ parse tiếng Anh.
- Tạo nhầm folder `dattask/` lúc đầu, phải xoá sau.
- Unit test và app.py chủ yếu do AI generate — cần đọc hiểu kỹ hơn từng assertion.

**Điểm tự đánh giá CP3:** Đủ điều kiện — có `tool.py` + `TOOL.md` + đăng ký `__init__.py`, ≥ 3 test, `pytest` 0 failed, `test_tool_contract.py` xanh.
"""
