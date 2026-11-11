# Team

## Thông tin nhóm

- Tên nhóm: **DNH**
- Lớp: **L3B**
- Repo nhóm: `K5-L3B-DAY03-NhomDNH-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt:
  - URL: https://github.com/quocnghidev/K5-L3B-DAY03-NhomDNH-ResearchAgentToolEval
  - Nhánh nộp: `nearly-final` (merge vào `main` khi Đạt điền báo cáo cá nhân + push)
  - Commit chốt hiện tại: `30d3b00bd622c5177745e62e5ecc1d33f902db93`
- Chi tiết phân công theo timeline: xem [PHAN_CONG.md](PHAN_CONG.md)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Lã Quốc Nghị | 2A202603947 | quocnghidev@gmail.com | quocnghidev | Prompt & tối ưu eval (C1–C3) |
|   2 | Nguyễn Tiến Đạt | 2A202603922 | ntdkhongdeptrailam5924@gmail.com | duchosinh4to10 | Tool mới + unit test + khung UI (C4) |
|   3 | Lê Thanh Hà | 2A202603901 | haroman2808@gmail.com | thanhhale288 | Eval nhóm + live chat + báo cáo + hoàn thiện UI / chốt nộp (C5–C7, hỗ trợ C4) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

---

## Lã Quốc Nghị — 2A202603947

Báo cáo cá nhân: [report/team/2A202603947_LaQuocNghi.md](report/team/2A202603947_LaQuocNghi.md)

### Phần việc phụ trách

- Setup chung (`.env`, preflight, `pytest`)
- Baseline **v0** + phân loại lỗi FAIL (bảng B2)
- Sửa `artifacts/system_prompt.md` và `artifacts/tools.yaml`
- Chạy vòng tối ưu **v1 → v2 → v3**, ghi `artifacts/version_log.csv`
- Chốt merge mô tả tool mới của Đạt vào `tools.yaml`

### Đóng góp cụ thể

- Owner các file: `system_prompt.md`, `tools.yaml`, `version_log.csv`, run base v0–v3
- Khởi tạo `TEAM.md` + `PHAN_CONG.md`
- Tối ưu evidence-driven: v0 0.65 → v1 0.85 → v2 0.95 → v3 **1.0** (20/20, `provider_error_cases=0`)

### Bằng chứng

- `starter_v0/runs/v0_B_base_openrouter_20261110T181324961249.json`
- `starter_v0/runs/v1_B_base_openrouter_20261110T184102136031.json`
- `starter_v0/runs/v2_B_base_openrouter_20261110T185301286980.json`
- `starter_v0/runs/v3_B_base_openrouter_20261110T185429875666.json`
- `starter_v0/artifacts/version_log.csv`
- Bảng B1 / B2 trong `report/team/group_report.md`
- Commit kỹ thuật trên `main`

---

## Nguyễn Tiến Đạt — 2A202603922

Báo cáo cá nhân: [report/team/2A202603922_NguyenTienDat.md](report/team/2A202603922_NguyenTienDat.md)

### Phần việc phụ trách

- Thiết kế và viết **≥ 1 tool mới** (`tools/datetime_window/tool.py` + `TOOL.md`)
- Đăng ký tool trong `tools/__init__.py`
- Viết **≥ 3 unit test** trong `tests/test_tools_todo.py`
- Scaffold UI (Streamlit hoặc tương đương) + dependency trong `requirements.txt`
- Gửi Nghị mô tả tool (tên, params, khi nào dùng) để đưa vào prompt/`tools.yaml`

### Đóng góp cụ thể

- Owner các file: `tools/datetime_window/tool.py`, `tools/datetime_window/TOOL.md`, `tools/__init__.py`, `tests/test_tools_todo.py`
- Khung UI ban đầu để Hà hoàn thiện

### Bằng chứng

- Folder tool mới (`tools/datetime_window/`) + `TOOL.md`
- Output lệnh `pytest` (0 failed; ≥ 3 test tool mới không skip)
- Commit kỹ thuật trên nhánh `main` (Đạt tự ghi SHA khi push)

---

## Lê Thanh Hà — 2A202603901

Báo cáo cá nhân: [report/team/2A202603901_LeThanhHa.md](report/team/2A202603901_LeThanhHa.md)

### Phần việc phụ trách

- **C5 — Eval nhóm:** viết đúng 10 case `data/eval_group.json` (5 single + 5 multi; ≥ 1 route tool mới); chạy `--suite group`; lưu run hợp lệ và điền B3
- **C6 — UI & live chat:** UI Gemini-like cũ + live ≥ 3 kịch bản + transcript; Cloudflare Tunnel → URL A1
- **C7 — Báo cáo nhóm:** lắp/viết lại Phần A + B3/B4/B5a + mục 5–7 (giữ B1/B2 của Nghị); rà `SUBMISSION.md` / `RULES.md`
- **Hỗ trợ chốt C4 (để nộp):** đăng ký `datetime_window` vào registry/`tools.yaml`, unit test ≥ 3, xoá `dattask` hỏng, Việt hoá prompt/tools phục vụ group eval, siết expect multi-turn đến DeepSeek **1.0**

### Đóng góp cụ thể

- Viết `eval_group.json` G01–G10; siết expect/prompt sau fail DeepSeek 0.6 → **1.0**
- Run: `starter_v0/runs/v3_B_group_deepseek_20261111T012607013544.json` (`provider_error_cases=0`, 10/10)
- Đăng ký `datetime_window` (`tools/__init__.py` + `artifacts/tools.yaml`); mở rộng parse timeframe tiếng Việt; ≥ 3 test trong `tests/test_tools_todo.py`; xoá `tools/dattask/`
- Việt hoá `artifacts/system_prompt.md` + `artifacts/tools.yaml` cho routing group
- UI cũ (`starter_v0/ui/`) + `scripts/run_c6_live.py` + tunnel; live openrouter 3 kịch bản C6
- Báo cáo: A1/B4/B5a/mục 5–7 khớp evidence mới; cập nhật `TEAM.md` + `2A202603901_LeThanhHa.md`

### Bằng chứng

- `starter_v0/data/eval_group.json`
- `starter_v0/runs/v3_B_group_deepseek_20261111T012607013544.json` — group **1.0**
- `starter_v0/tools/datetime_window/` + đăng ký + unit test; pytest 0 failed
- Transcript C6: `v3_openrouter_ui_81a96500eb3d_…`, `…fc7e2e73cb96_…`, `…36347f0e1c8a_…`
- `report/team/group_report.md` — A1 URL: https://dnh-research-agent.onrender.com/
- `report/team/2A202603901_LeThanhHa.md`
