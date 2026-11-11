"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- datetime_window ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

datetime_window_tool = TOOL_FUNCTIONS["datetime_window"]


def test_datetime_window_happy_path_last_7_days() -> None:
    result = datetime_window_tool(
        timeframe="last 7 days",
        reference_date="2026-11-10T17:00:00",
        tz="UTC",
    )

    assert "error" not in result
    assert result["timeframe_code"] == "7d"
    assert result["label"] == "last 7 days"
    assert result["duration_days"] == 7.0
    assert result["start"] == "2026-11-03T17:00:00+00:00"
    assert result["end"] == "2026-11-10T17:00:00+00:00"


def test_datetime_window_vietnamese_tuan_truoc_and_relative_days() -> None:
    tuan = datetime_window_tool(
        timeframe="tuần trước",
        reference_date="2026-11-10T17:00:00",
        tz="UTC",
    )
    assert "error" not in tuan
    assert tuan["timeframe_code"] == "7d"
    assert tuan["label"] == "tuần trước"

    days = datetime_window_tool(
        timeframe="3 ngày gần đây",
        reference_date="2026-11-10T17:00:00",
        tz="UTC",
    )
    assert "error" not in days
    assert days["timeframe_code"] == "3d"
    assert days["label"] == "3 ngày gần đây"
    assert days["duration_days"] == 3.0


def test_datetime_window_bad_input_empty_timeframe() -> None:
    result = datetime_window_tool(timeframe="")

    assert isinstance(result, dict)
    assert "error" in result
    assert "start" not in result


def test_datetime_window_failure_returns_error_dict() -> None:
    bad_tz = datetime_window_tool(timeframe="last 7 days", tz="Not/A_Real_Zone")
    assert isinstance(bad_tz, dict)
    assert "error" in bad_tz
    assert "Timezone" in bad_tz["error"] or "timezone" in bad_tz["error"].lower()

    unparseable = datetime_window_tool(timeframe="sometime soon maybe")
    assert isinstance(unparseable, dict)
    assert "error" in unparseable
    assert "start" not in unparseable
