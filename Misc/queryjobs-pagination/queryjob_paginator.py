#!/usr/bin/env python3
"""
LogScale QueryJob paginator — retrieves all results from a QueryJob using
cursor-based pagination via the `around` parameter.

The QueryJobs API returns a result buffer of 200 events (for filter queries).
To retrieve all matching events, this script:
  1. Creates a QueryJob and polls until done
  2. Collects the initial 200-event buffer
  3. If hasMoreEvents="true", uses the `around` parameter to create new
     QueryJobs anchored on the oldest event, walking backward through time
     until all events are collected

Setup (one-time):
    python3 -m venv .venv
    source .venv/bin/activate
    pip install requests

Activate venv (each session):
    source .venv/bin/activate

Environment variables:
    export LOGSCALE_TOKEN="your-api-token"              # Required
    export LOGSCALE_BASE_URL="https://your-instance/"   # Required
    export LOGSCALE_REPO="your-repo"                    # Required

Usage:
    python queryjob_paginator.py -q '#event_simpleName=ProcessRollup2'

    # Queries with double quotes — wrap in single quotes:
    python queryjob_paginator.py -q '#event_simpleName=ProcessRollup2 | groupBy([aid], function=[count(as="Event Count")])'

    # Optional flags:
    python queryjob_paginator.py -q '...' -s 1h -e now -o results.json --max-events 5000
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import requests

# ── Defaults ──────────────────────────────────────────────────────────
START = "15m"
END = "now"
PAGE_SIZE = 200
MAX_EVENTS = 0      # 0 = unlimited
OUTPUT_FILE = "queryjob_results.json"
# ──────────────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="LogScale QueryJob paginator with cursor-based pagination.",
        epilog="""Required environment variables:
  LOGSCALE_TOKEN      API token for authentication
  LOGSCALE_BASE_URL   LogScale instance URL (e.g. https://cloud.us-1.crowdstrike.com/)
  LOGSCALE_REPO       Repository name to query against""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-q", "--query",
        required=True,
        help="CQL query string. Wrap in single quotes to preserve double quotes: "
             "-q '#event_simpleName=ProcessRollup2 | groupBy([aid], function=[count(as=\"Event Count\")])'",
    )
    parser.add_argument("-s", "--start", default=START, help=f"Start time (default: {START})")
    parser.add_argument("-e", "--end", default=END, help=f"End time (default: {END})")
    parser.add_argument("-o", "--output", default=OUTPUT_FILE, help=f"Output file (default: {OUTPUT_FILE})")
    parser.add_argument("--max-events", type=int, default=MAX_EVENTS, help="Max events to retrieve (default: unlimited)")
    parser.add_argument("--page-size", type=int, default=PAGE_SIZE, help=f"Events per page (default: {PAGE_SIZE})")
    return parser.parse_args()


def create_queryjob(api_base: str, headers: dict, query_string: str,
                    start: str, end: str, around: dict | None = None) -> str:
    """Create a QueryJob and return its ID."""
    body = {
        "queryString": query_string,
        "start": start,
        "end": end,
        "isLive": False,
    }
    if around:
        body["around"] = around

    resp = requests.post(api_base, headers=headers, json=body)
    resp.raise_for_status()
    return resp.json()["id"]


def delete_queryjob(api_base: str, headers: dict, job_id: str) -> None:
    """Delete a QueryJob to free server resources."""
    requests.delete(f"{api_base}/{job_id}", headers=headers)


def poll_until_done(api_base: str, headers: dict, job_id: str) -> dict:
    """Poll a QueryJob until done and return the result payload."""
    poll_url = f"{api_base}/{job_id}"

    while True:
        resp = requests.get(poll_url, headers=headers)
        if resp.status_code == 404:
            return {"done": True, "events": [], "metaData": {}}
        resp.raise_for_status()
        data = resp.json()

        if data["done"]:
            return data

        wait_ms = data["metaData"].get("pollAfter", 500)
        time.sleep(wait_ms / 1000.0)


def main():
    args = parse_args()

    base_url = os.environ.get("LOGSCALE_BASE_URL", "")
    repo = os.environ.get("LOGSCALE_REPO", "")
    token = os.environ.get("LOGSCALE_TOKEN")
    missing = []
    if not token:
        missing.append("LOGSCALE_TOKEN")
    if not base_url:
        missing.append("LOGSCALE_BASE_URL")
    if not repo:
        missing.append("LOGSCALE_REPO")
    if missing:
        sys.exit(f"Error: set required environment variables: {', '.join(missing)}")

    api_base = f"{base_url.rstrip('/')}/api/v1/repositories/{repo}/queryjobs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    query_string = args.query
    start = args.start
    end = args.end
    output_file = args.output
    max_events = args.max_events
    page_size = args.page_size

    print(f"Query:  {query_string}")
    print(f"Repo:   {repo}")
    print(f"Range:  {start} → {end}")
    print()

    # Step 1: Initial query — get the first buffer of events
    job_id = create_queryjob(api_base, headers, query_string, start, end)
    print(f"QueryJob created: {job_id}")

    data = poll_until_done(api_base, headers, job_id)
    delete_queryjob(api_base, headers, job_id)

    meta = data.get("metaData", {})
    has_more = meta.get("extraData", {}).get("hasMoreEvents", "false")
    processed = meta.get("processedEvents", "?")

    all_events: list[dict] = list(data.get("events", []))
    seen_ids: set[str] = {e.get("@id", "") for e in all_events}

    print(f"  Initial buffer: {len(all_events)} events  "
          f"(processedEvents={processed}  hasMoreEvents={has_more})")

    # Step 2: Cursor pagination — walk backward through time using `around`
    # LogScale returns newest events first; the last event in the buffer is
    # the oldest. We anchor on it and request numberOfEventsBefore to get
    # progressively older events.
    page = 0
    while has_more == "true" and all_events:
        if max_events and len(all_events) >= max_events:
            all_events = all_events[:max_events]
            break

        oldest = all_events[-1]
        anchor_id = oldest.get("@id", "")
        anchor_ts = oldest.get("@timestamp")
        if not anchor_id or anchor_ts is None:
            break

        page += 1
        cursor_job_id = create_queryjob(api_base, headers, query_string, start, end, around={
            "eventId": anchor_id,
            "timestamp": int(anchor_ts),
            "numberOfEventsBefore": page_size,
            "numberOfEventsAfter": 0,
        })

        cursor_data = poll_until_done(api_base, headers, cursor_job_id)
        delete_queryjob(api_base, headers, cursor_job_id)

        events = cursor_data.get("events", [])
        new_events = [e for e in events if e.get("@id", "") not in seen_ids]

        if not new_events:
            break

        for e in new_events:
            seen_ids.add(e.get("@id", ""))
        all_events.extend(new_events)

        print(f"  page {page}: +{len(new_events)} events  (total: {len(all_events)})")
        time.sleep(0.5)

    if max_events and len(all_events) > max_events:
        all_events = all_events[:max_events]

    print(f"\nDone. {len(all_events)} total events.")

    with open(output_file, "w") as f:
        json.dump(all_events, f, indent=2)
    print(f"Results written to {output_file}")


if __name__ == "__main__":
    main()
