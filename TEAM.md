# Team

## Thông tin nhóm

- Tên nhóm: **DNH**
- Lớp: **L3B**
- Repo nhóm: `K5-L3B-DAY03-NhomDNH-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt:
  - URL: https://github.com/quocnghidev/K5-L3B-DAY03-NhomDNH-ResearchAgentToolEval
  - Nhánh nộp: `nearly-final` (cần merge/push sang `main` nếu LMS yêu cầu `main`)
  - Commit chốt hiện tại: `8f1b96fcd67305a392e37c446e58f755935f7d4e`
- Chi tiết phân công kế hoạch + kết quả thực tế: xem [PHAN_CONG.md](PHAN_CONG.md)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò (kế hoạch → thực tế) |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Lã Quốc Nghị | 2A202603947 | quocnghidev@gmail.com | quocnghidev | Prompt & tối ưu eval (C1–C3) |
|   2 | Nguyễn Tiến Đạt | 2A202603922 | ntdkhongdeptrailam5924@gmail.com | duhocsinh4to10 | Tool mới (C4 khởi tạo); test/đăng ký/UI do Hà chốt sau |
|   3 | Lê Thanh Hà | 2A202603901 | haroman2808@gmail.com | thanhhale288 | Eval nhóm + live chat + báo cáo + UI (C5–C7); hỗ trợ chốt C4 |

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
- Phối hợp khai báo tool mới trong `tools.yaml` / prompt khi tool đã sẵn sàng

### Đóng góp cụ thể

- Owner các file: `system_prompt.md`, `tools.yaml` (vòng v0–v3), `version_log.csv`, run base v0–v3
- Khởi tạo `TEAM.md` + `PHAN_CONG.md`
- Tối ưu evidence-driven: v0 0.65 → v1 0.85 → v2 0.95 → v3 **1.0** (20/20, `provider_error_cases=0`)

### Bằng chứng

- `starter_v0/runs/v0_B_base_openrouter_20261110T181324961249.json`
- `starter_v0/runs/v1_B_base_openrouter_20261110T184102136031.json`
- `starter_v0/runs/v2_B_base_openrouter_20261110T185301286980.json`
- `starter_v0/runs/v3_B_base_openrouter_20261110T185429875666.json`
- `starter_v0/artifacts/version_log.csv`
- Bảng B1 / B2 trong `report/team/group_report.md`
- Commit kỹ thuật trên nhánh nhóm (`nearly-final` / lịch sử repo)

---

## Nguyễn Tiến Đạt — 2A202603922

Báo cáo cá nhân: [report/team/2A202603922_NguyenTienDat.md](report/team/2A202603922_NguyenTienDat.md)

### Phần việc phụ trách (kế hoạch ban đầu)

- Thiết kế và viết **≥ 1 tool mới**
- Đăng ký tool, viết ≥ 3 unit test, scaffold UI (theo `PHAN_CONG.md`)

### Đóng góp cụ thể (theo git — trung thực)

- Upload tool **`datetime_window`** (commit `c3c58af`): `tools/datetime_window/tool.py`, `TOOL.md`, `__init__.py` trong folder tool
- Bản đầu: parse timeframe **tiếng Anh**, trả `error` dict khi input xấu
- Có tạo thêm folder `dattask/` (sau đó nhóm xoá vì lệch contract)
- Cập nhật mô tả phần việc trong `TEAM.md` (commit `6b488f1`)
- **Không** hoàn thành một mình trên repo: đăng ký `tools/__init__.py` + `artifacts/tools.yaml`, unit test, Việt hoá parse, UI nộp bài — các phần này do **Hà** chốt sau

### Bằng chứng

- `starter_v0/tools/datetime_window/tool.py` + `TOOL.md` (code khởi tạo)
- Commit: `c3c58af` (`duhocsinh4to10`) — *Add files via upload*
- Báo cáo cá nhân: `report/team/2A202603922_NguyenTienDat.md`

---

## Lê Thanh Hà — 2A202603901

Báo cáo cá nhân: [report/team/2A202603901_LeThanhHa.md](report/team/2A202603901_LeThanhHa.md)

### Phần việc phụ trách

- **C5 — Eval nhóm:** viết đúng 10 case `data/eval_group.json` (5 single + 5 multi; ≥ 1 route tool mới); chạy `--suite group`; lưu run hợp lệ và điền B3
- **C6 — UI & live chat:** UI (`starter_v0/ui/`) + live ≥ 3 kịch bản + transcript; link dùng thử (tunnel / Render)
- **C7 — Báo cáo nhóm:** lắp/viết lại Phần A + B3/B4/B5a + mục 5–7 (giữ B1/B2 của Nghị)
- **Hỗ trợ chốt C4:** đăng ký `datetime_window`, unit test ≥ 3, xoá `dattask`, mở rộng parse tiếng Việt, siết group eval đến DeepSeek **1.0**

### Đóng góp cụ thể

- Viết `eval_group.json` G01–G10; siết expect/prompt sau fail DeepSeek 0.6 → **1.0**
- Run: `starter_v0/runs/v3_B_group_deepseek_20261111T012607013544.json` (`provider_error_cases=0`, 10/10)
- Đăng ký `datetime_window` (`tools/__init__.py` + `artifacts/tools.yaml`); mở rộng parse timeframe tiếng Việt; ≥ 3 test trong `tests/test_tools_todo.py`; xoá `tools/dattask/`
- Việt hoá / bổ sung rule routing group trong `artifacts/system_prompt.md` + `artifacts/tools.yaml`
- UI (`starter_v0/ui/`) + `scripts/run_c6_live.py` + tunnel/Render; live openrouter 3 kịch bản C6
- Báo cáo nhóm A1/B3/B4/B5a/mục 5–7 khớp evidence

### Bằng chứng

- `starter_v0/data/eval_group.json`
- `starter_v0/runs/v3_B_group_deepseek_20261111T012607013544.json` — group **1.0**
- `starter_v0/tools/datetime_window/` (sau khi đăng ký + VN) + unit test; pytest 0 failed
- Transcript C6: `v3_openrouter_ui_81a96500eb3d_…`, `…fc7e2e73cb96_…`, `…36347f0e1c8a_…`
- `report/team/group_report.md` — A1 / B3–B5a
- `report/team/2A202603901_LeThanhHa.md`
