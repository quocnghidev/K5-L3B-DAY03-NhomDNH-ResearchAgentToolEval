# UI — cửa sổ chat DNH team

Transcript kiểu Gemini: bubble phải = bạn, chữ trái = DNH team agent.
Gọi cùng tool loop như `chat.py`, ghi transcript vào `transcripts/` **khi có tin nhắn đầu**.

Mỗi trình duyệt có `session_id` riêng (localStorage + header `X-Session-Id`).
Nút **Xóa cuộc trò chuyện** gọi `POST /api/reset`.

Server dùng **stdlib** (`http.server`) — không thêm package bắt buộc.

## Chạy (từ `starter_v0/`)

```bash
cd starter_v0
pip install -r requirements.txt
python3 -m ui --provider openrouter --model openai/gpt-4o-mini --version v3 --host 127.0.0.1 --port 8792
# → http://127.0.0.1:8792
```

Public:

```bash
bash scripts/run_cloudflare_tunnel.sh 8792
```

Live 3 kịch bản C6 (UI đang chạy):

```bash
python3 scripts/run_c6_live.py --base http://127.0.0.1:8792
```

## API

| | |
|--|--|
| `POST /api/chat` | header `X-Session-Id` + `{"text":"..."}` |
| `POST /api/reset` | xóa history + transcript mới |
| `POST /api/model` | chọn model (openrouter) theo session |
| `GET /api/health` | provider, model(s), version |
