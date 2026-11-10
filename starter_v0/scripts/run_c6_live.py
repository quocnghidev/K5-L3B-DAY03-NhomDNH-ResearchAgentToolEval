#!/usr/bin/env python3
"""Chạy 3 kịch bản live C6 qua UI API; in đường dẫn transcript.

Yêu cầu UI đang chạy, ví dụ:
  python -m ui --provider openrouter --version v3 --host 127.0.0.1 --port 8792
  python scripts/run_c6_live.py --base http://127.0.0.1:8792
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
import urllib.error
import urllib.request
from typing import Any


SCENARIOS: list[dict[str, Any]] = [
    {
        "id": "research",
        "label": "Yêu cầu thường (research)",
        "turns": ["Tóm tắt tin AI hôm nay bằng tiếng Việt, ngắn gọn."],
        "expect_tools_any": {"lookup"},
    },
    {
        "id": "missing_info",
        "label": "Thiếu thông tin rồi bổ sung",
        "turns": [
            "Tóm tắt 5 tweet mới nhất giúp mình",
            "Handle là sama.",
        ],
        "expect_first_tool": "clarify",
        "expect_second_tool": "timeline",
    },
    {
        "id": "confirm_send",
        "label": "Yêu cầu gửi/đăng rồi xác nhận",
        "turns": [
            "Đăng lên Telegram nội dung: Bản tin AI tuần này.",
            "Có, xác nhận gửi.",
        ],
        "expect_first_tool": "clarify",
        "expect_second_tool": "send",
    },
]


def post(base: str, path: str, session_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    req = urllib.request.Request(
        f"{base.rstrip('/')}{path}",
        data=json.dumps({**payload, "session_id": session_id}).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Session-Id": session_id,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def tools_of(payload: dict[str, Any]) -> list[str]:
    return list(payload.get("tools") or [])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:8792")
    args = parser.parse_args()

    results: list[dict[str, Any]] = []
    for scenario in SCENARIOS:
        sid = uuid.uuid4().hex
        print(f"\n=== {scenario['id']}: {scenario['label']} ===")
        transcript = None
        turn_tools: list[list[str]] = []
        for text in scenario["turns"]:
            try:
                payload = post(args.base, "/api/chat", sid, {"text": text})
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                print(f"HTTP {exc.code}: {body}", file=sys.stderr)
                return 1
            except Exception as exc:
                print(f"FAIL: {exc}", file=sys.stderr)
                return 1
            used = tools_of(payload)
            turn_tools.append(used)
            transcript = payload.get("transcript")
            print(f"you> {text}")
            print(f"tools> {used or ['(none)']}")
            print(f"agent> {(payload.get('assistant_text') or '')[:240]}")
            print(f"status> {payload.get('status')} · {payload.get('summary')}")

        ok = True
        notes: list[str] = []
        if "expect_tools_any" in scenario:
            if not (set(turn_tools[0]) & set(scenario["expect_tools_any"])):
                ok = False
                notes.append(f"expected one of {sorted(scenario['expect_tools_any'])}, got {turn_tools[0]}")
        if scenario.get("expect_first_tool"):
            if scenario["expect_first_tool"] not in turn_tools[0]:
                ok = False
                notes.append(f"turn1 expected {scenario['expect_first_tool']}, got {turn_tools[0]}")
        if scenario.get("expect_second_tool") and len(turn_tools) > 1:
            if scenario["expect_second_tool"] not in turn_tools[1]:
                ok = False
                notes.append(f"turn2 expected {scenario['expect_second_tool']}, got {turn_tools[1]}")

        results.append(
            {
                "id": scenario["id"],
                "ok": ok,
                "notes": notes,
                "transcript": transcript,
                "turn_tools": turn_tools,
            }
        )
        print("CHECK>", "PASS" if ok else "FAIL", "; ".join(notes) or "ok")

    print("\n=== SUMMARY ===")
    all_ok = True
    for row in results:
        all_ok = all_ok and bool(row["ok"])
        print(f"{row['id']}: {'PASS' if row['ok'] else 'FAIL'} → {row['transcript']}")
        for note in row["notes"]:
            print(f"  - {note}")
    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
