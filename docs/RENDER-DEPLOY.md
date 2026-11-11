# Deploy UI lên Render (không cần bật máy)

Link public chạy trên cloud; tắt laptop vẫn mở được.

## 1. Push code lên GitHub

Nhánh có `render.yaml` + `starter_v0/` (ví dụ `nearly-final` hoặc `main`).

## 2. Tạo service trên Render

1. Đăng ký / đăng nhập [https://dashboard.render.com](https://dashboard.render.com)
2. **New → Blueprint** → connect repo `K5-L3B-DAY03-NhomDNH-ResearchAgentToolEval`
3. Chọn nhánh vừa push → Apply `render.yaml`
4. Hoặc **New → Web Service** thủ công:
   - Root Directory: `starter_v0`
   - Build: `pip install -r requirements.txt`
   - Start: `bash scripts/start_ui_render.sh`
   - Health Check Path: `/api/health`

## 3. Điền Environment (Secrets)

Bắt buộc để chat chạy:

| Key | Ghi chú |
|---|---|
| `OPENROUTER_API_KEY` | Bắt buộc nếu `UI_PROVIDER=openrouter` |
| `TAVILY_API_KEY` | Tool `lookup` |
| `FIRECRAWL_API_KEY` | Tool `fetch` |
| `RAPIDAPI_KEY` | Tool `timeline` / `social_search` |

Tuỳ chọn: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.

**Không** upload file `.env`; dán từng key trên dashboard.

## 4. Lấy URL và ghi A1

Sau khi Deploy sống (Live):

`https://<tên-service>.onrender.com`

Dán vào mục **A1 — Link dùng thử** trong `report/team/group_report.md`.

Kiểm tra nhanh:

```bash
curl -sS https://<tên-service>.onrender.com/api/health
```

## 5. Lưu ý free tier

- Service **sleep** sau ~15 phút không traffic; lần mở sau cold start ~30–60s.
- Disk tạm: transcript trên server có thể mất khi redeploy.
- Evidence C6 trong repo (`transcripts/*.transcript.json`) vẫn dùng để chấm; Render chỉ để demo công khai.
