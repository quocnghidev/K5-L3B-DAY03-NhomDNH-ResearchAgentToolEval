# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: **DNH**
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: **openrouter / openai/gpt-4o-mini** (lấy từ run JSON v0–v3)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent: tìm tin theo từ khóa / theo tài khoản X, đọc URL, tổng hợp digest, và chỉ gửi Telegram sau khi người dùng xác nhận. Agent hỏi lại (`clarify`) khi thiếu handle/URL và từ chối yêu cầu ngoài phạm vi nghiên cứu.

**Cách chạy UI:**

```bash
cd starter_v0
pip install -r requirements.txt   # SDK provider; UI dùng stdlib http.server (không thêm package)
# Ưu tiên DeepSeek (OpenAI-compatible):
python -m ui --provider deepseek --version v3 --host 127.0.0.1 --port 8792
# Fallback local nếu máy không ra API cloud:
# python -m ui --provider ollama --model qwen2.5:7b --version v3 --host 127.0.0.1 --port 8792
# mở http://127.0.0.1:8792
```

**Link dùng thử (deploy):**

> Deploy nhanh (máy local, Terminal.app — Cursor agent không DNS được `trycloudflare.com`):
>
> ```bash
> cd starter_v0
> python3 -m ui --provider deepseek --version v3 --host 127.0.0.1 --port 8793
> # terminal khác:
> bash scripts/run_cloudflare_tunnel.sh 8793
> ```
>
> URL: https://highlighted-tea-angels-relay.trycloudflare.com/
>
> _(Giữ Terminal `cloudflared` / `run_cloudflare_tunnel.sh` mở khi demo; URL trycloudflare đổi mỗi lần tạo tunnel mới.)_
>
> Group eval DeepSeek: `bash scripts/run_group_deepseek.sh`
### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.
>
> Nguồn: `starter_v0/artifacts/tools.yaml` + `starter_v0/tools/__init__.py` (đã register `datetime_window`).

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại khi thiếu thông tin hoặc trước khi gửi/đăng | không |
| timeline | lấy bài gần đây của một tài khoản X (cần handle) | không |
| social_search | tìm post theo từ khóa/chủ đề (không gắn 1 handle) | không |
| lookup | tìm web/news theo query + topic/timeframe | không |
| fetch | đọc nội dung một URL cụ thể | không |
| format | render danh sách item thành digest markdown | không |
| send | gửi text lên Telegram (chỉ khi `confirmed=true`) | không |
| policy | tìm snippet policy nội bộ | không |
| papers | tìm paper trên arXiv | không |
| paper_text | lấy text từ paper arXiv (id/URL) | không |
| datetime_window | chuẩn hoá timeframe ngôn ngữ tự nhiên → start/end + `timeframe_code` cho lookup/timeline | **có** |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. Tìm tin AI trong **tuần trước** rồi tóm tắt ngắn bằng tiếng Việt. *(relative time → kỳ vọng gọi `datetime_window` rồi `lookup` khi tool đã register)*
2. Cho tôi timeline gần đây của tài khoản X về AI. *(thiếu handle → kỳ vọng `clarify`, không đoán screenname)*
3. Tóm tắt tin AI hôm nay thành digest, rồi **gửi lên Telegram**. *(kỳ vọng hỏi xác nhận `clarify(yes_no)` trước `send`)*
4. Đọc và tóm tắt bài này: `https://vnexpress.net/...` *(có URL → `fetch`)*
5. Giải giúp bài tích phân / viết hàm Fibonacci. *(out-of-scope → không gọi tool research/send)*

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- **v1 (`system_prompt.md`)**: bỏ chỉ dẫn xấu starter (đoán handle/URL, gửi luôn, một bước); thêm rule `clarify` khi thiếu info, confirm trước `send`, từ chối out-of-scope không gọi tool. Metric 0.65 → 0.85.
- **v2 (`tools.yaml`)**: viết lại mọi description (khi nào dùng/không dùng); bắt buộc `clarify.response_type`; `send` chỉ khi `confirmed=true` sau xác nhận; convention args (`lookup` query ngắn + `topic`/`timeframe`, handle không `@`, `social_search` vs `timeline`). Metric 0.85 → 0.95.
- **v3 (`system_prompt.md`)**: turn đầu của send/post/đăng chỉ được `clarify(response_type="yes_no")`, không hỏi nội dung bằng `text` trước confirm. Metric 0.95 → **1.0** (20/20).
- **Tool mới**: `datetime_window` (Đạt code; đã register vào `tools/__init__.py` + `artifacts/tools.yaml`; thêm rule relative-time trong `system_prompt.md`; ≥3 unit test trong `tests/test_tools_todo.py`). Folder lỗi `tools/dattask/` đã xoá để contract pytest xanh.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi starter trước khi tối ưu |  | 0.65 | `starter_v0/runs/v0_B_base_openrouter_20261110T181324961249.json` |
| v1 | system_prompt.md | Bỏ đoán/gửi luôn → giảm missing_info, wrong_boundary, out_of_scope | 0.65 | 0.85 | `starter_v0/runs/v1_B_base_openrouter_20261110T184102136031.json` |
| v2 | tools.yaml | Siết declaration (clarify.response_type + send boundary + routing/args) → hết R10–R12 | 0.85 | 0.95 | `starter_v0/runs/v2_B_base_openrouter_20261110T185301286980.json` |
| v3 | system_prompt.md | Turn đầu send/đăng phải clarify yes_no (không text) → R12 PASS | 0.95 | 1.0 | `starter_v0/runs/v3_B_base_openrouter_20261110T185429875666.json` |

Hash/`artifact_version` đầy đủ: `starter_v0/artifacts/version_log.csv`. Mọi run trên có `provider_error_cases=0`, `measured_cases=total_cases=20`.

### B2. Failure Analysis

Nguồn FAIL ban đầu: `starter_v0/runs/v0_B_base_openrouter_20261110T181324961249.json` (v0, `case_accuracy=0.65`, `provider_error_cases=0`, `measured_cases=20/20`).  
Cột **Failure Type** = `result.failure_type`; chi tiết = `result.observed_mismatch` + `result.failures`.  
Cột **Fix** ghi version đã xử lý theo run thật sau đó (v1/v2/v3 đều PASS các case dưới; v3 = 20/20).

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | wrong_tool (`observed_mismatch`: wrong_arg_value) | `lookup(query="AI news", topic="news", timeframe="day")` | Expect `query="AI"`; actual `query="AI news"` | v1 prompt + v2 `tools.yaml` convention query ngắn / topic+timeframe → PASS từ v1 |
| R08_out_of_scope | out_of_scope (`observed_mismatch`: unexpected_tool_call) | `send(text=...)` | Expect `no_tool`; actual gọi `send` trả lời tích phân | v1 scope rule → PASS từ v1 |
| R10_missing_handle | missing_info (`observed_mismatch`: missing_tool_call) | `timeline(screenname="sama")` | Expect `clarify`; đoán handle | v1 bắt clarify; v2 bắt `response_type="text"` → PASS từ v2 |
| R11_missing_url | missing_info (`observed_mismatch`: missing_tool_call) | `fetch(url="https://example.com/article")` | Expect `clarify`; bịa URL | v1 + v2 (như R10) → PASS từ v2 |
| R12_confirm_before_send | wrong_boundary (`observed_mismatch`: missing_tool_call) | `send(text="Bản tin này")` | Expect `clarify(yes_no)`; gửi luôn | v1 dừng send; v2 vẫn còn sai `text`; v3 ép yes_no turn đầu → PASS ở v3 |
| R13_parallel_web_and_tweets | wrong_tool (`observed_mismatch`: wrong_arg_value) | `lookup(...)` + `timeline(sama)` | Sai args; thiếu `social_search` | v1/v2 routing social_search vs timeline → PASS từ v1 |
| R14_out_of_scope_coding | out_of_scope (`observed_mismatch`: unexpected_tool_call) | `send(text=...Fibonacci...)` | Expect `no_tool` | v1 scope rule → PASS từ v1 |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn). Dataset: `day03_v2_research_group`.

> **Run group hợp lệ (DeepSeek):** `starter_v0/runs/v3_B_group_deepseek_20261111T012607013544.json`  
> Provider/model: **deepseek / deepseek-chat** · `provider_error_cases=0`, `measured_cases=10/10`, **`case_accuracy=1.0` (10/10 PASS)** · artifact `v3+p0251ccb0a331+tc1dfecfdad0c`.  
> Run cũ (0.6) giữ để so: `v3_B_group_deepseek_20261111T012357255793.json`. Ollama tham chiếu: `v3_B_group_ollama_20261111T011051946135.json` (0.8).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_datetime_window_tuan_truoc (single) | Relative VN “tuần trước” → `datetime_window` | `datetime_window(timeframe="tuần trước")` | **PASS** |
| G02_social_not_timeline_topic (single) | Chủ đề Claude 4, không handle | `social_search(query="Claude 4")` | **PASS** |
| G03_clarify_missing_topic (single) | Có timeframe, thiếu chủ đề | `clarify(response_type="text")` | **PASS** |
| G04_out_of_scope_recipe (single) | Nấu ăn ngoài research | `no_tool` | **PASS** |
| G05_fetch_then_format_brief (single) | URL + digest brief | `fetch` + `format(template="brief")` | **PASS** |
| G06_datetime_then_lookup_chain (multi) | Sau chuẩn hoá → chỉ lookup | `lookup(query="chip AI", topic="news")` | **PASS** |
| G07_confirm_then_send (multi) | Sau user xác nhận → gửi | `send(confirmed=true)` | **PASS** |
| G08_timeframe_correction_week (multi) | Sửa tháng→tuần, giữ chủ đề | `lookup(..., timeframe="week")` | **PASS** |
| G09_clarify_topic_then_lookup (multi) | Bổ sung topic sau clarify | `lookup(query="quantum computing", ...)` | **PASS** |
| G10_switch_search_to_timeline (multi) | Chuyển search chủ đề → timeline Demis | `timeline(..., limit=5)` | **PASS** |

### B4. Live Chat Evidence

UI đang chạy: `http://127.0.0.1:8792` (`python -m ui --provider ollama --model qwen2.5:7b --version v3`). DeepSeek đã wire (`--provider deepseek`) nhưng agent/Cursor hiện không DNS tới API — cần chạy DeepSeek trên Terminal máy bạn.

Transcript v3 mới (3 kịch bản):

| Turn / Session | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| Research thường | `Tóm tắt tin AI gần đây...` | (xem file) | `transcripts/v3_ollama_ui_2f0ca0676ba1_20261111T011041235207.transcript.json` | Live UI v3 |
| Thiếu info → bổ sung | `timeline... tài khoản X` rồi `Handle là sama` | (xem file) | `transcripts/v3_ollama_ui_e92e488dbfd7_20261111T011050060128.transcript.json` | Đủ scenario thiếu-info |
| Gửi/đăng | `Đăng lên Telegram...` rồi `Có, xác nhận gửi.` | (xem file) | `transcripts/v3_ollama_ui_cb268d3855c3_20261111T011103555918.transcript.json` | Confirm flow |

Transcript cũ (openrouter v0, 3 turns send): `starter_v0/transcripts/v0_openrouter_ui_evidence3tur_20261110T190927418591.transcript.json`.

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/datetime_window/`) | `tool.py`, `TOOL.md`; đăng ký `tools/__init__.py` + `artifacts/tools.yaml`; rule VN trong `system_prompt.md` | Parse timeframe **tiếng Việt** (`tuần trước`, `3 ngày gần đây`, …) + EN; input xấu/`tz` lỗi → `error` dict | Model local còn miss G05/G06; DeepSeek cần chạy ngoài agent khi DNS OK |
| Unit test tool mới (≥ 3 test/tool) | `tests/test_tools_todo.py` — `datetime_window_*` (+ VN cases) | Offline, không gọi mạng | `pytest`: **64 passed, 14 skipped, 0 failed** |
| UI (lệnh chạy + link dùng thử) | `starter_v0/ui/` + transcript B4 | Stdlib UI; DeepSeek + tunnel public | Local: `python -m ui --provider deepseek --version v3 --port 8792` · Public: https://highlighted-tea-angels-relay.trycloudflare.com/ |

Tool unit tests: **3** test cho `datetime_window`. Ví dụ lỗi unit bắt được mà eval routing không bắt: `timeframe=""` hoặc `tz` không phải IANA → trả `{"error": ...}` thay vì exception (eval chỉ chấm tên tool/args, không chấm exception path).

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

- **V0 boundary/send:** live transcript v0 gọi `send(confirmed=true)` ngay khi user xin gửi; thiếu `TELEGRAM_*` env → lỗi tool (transcript evidence3tur). Base eval v0→v3 đã siết clarify/`yes_no`, nhưng live evidence vẫn bản v0.
- **Group eval chưa đo được trên máy này:** 10 case đã viết, tool đã register, nhưng DNS không resolve `openrouter.ai` → mọi attempt `provider_error` (không dùng làm bằng chứng). Cần chạy lại khi mạng OK.
- **Transcript thiếu scenario:** chưa có lượt “thiếu info rồi bổ sung” trên artifact **v3**.
- **Public demo:** https://highlighted-tea-angels-relay.trycloudflare.com/ (cần giữ process tunnel chạy).

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân:

- Nghị: [report/team/2A202603947_LaQuocNghi.md](2A202603947_LaQuocNghi.md) — prompt/tools.yaml, v0–v3 base eval, B1/B2
- Hà: [report/team/2A202603901_LeThanhHa.md](2A202603901_LeThanhHa.md) — eval group 10 case + DeepSeek 1.0; đăng ký/`datetime_window` + unit test + Việt hoá prompt/tools cho group; UI/tunnel/transcript; lắp Phần A / B3–B5a / reflection
- Đạt: tool `datetime_window` (code ban đầu) — báo cáo cá nhân Đạt **chưa** tạo (theo yêu cầu bỏ qua bước này)

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix thuộc `system_prompt.md`:** v1 bỏ đoán/gửi luôn + scope; v3 ép turn đầu send/đăng dùng `clarify(yes_no)` → R12 PASS, base 1.0; thêm rule gọi `datetime_window` trước lookup/timeline khi timeframe mơ hồ.
- **Fix thuộc `tools.yaml`:** v2 siết description/`response_type`/send boundary/args; sau đó khai báo `datetime_window`.
- **Cần review thủ công / evidence live:** (1) transcript v0 thiếu “thiếu info rồi bổ sung”; (2) Telegram thật phụ thuộc env; (3) group suite có case nhưng chưa có run hợp lệ vì DNS.
- **Vòng tiếp theo:** khi mạng OK → chạy `--suite group` cập nhật B3 Result; live chat **v3** (clarify-then-fill + confirm-before-send); tunnel URL cho A1; Đạt bổ sung báo cáo cá nhân.

## 8. Tài liệu tham khảo

- [RUBRIC.md](../../RUBRIC.md), [SUBMISSION.md](../../SUBMISSION.md), [PHAN_CONG.md](../../PHAN_CONG.md)
- `starter_v0/artifacts/version_log.csv`, runs v0–v3 base (B1)
- Transcript UI: `starter_v0/transcripts/v0_openrouter_ui_evidence3tur_20261110T190927418591.transcript.json`
- Commit UI: `4adf5a5`
