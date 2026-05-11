#!/usr/bin/env python3
"""
NG-SIEM QueryJob paginator (FalconPy) — retrieves all results from a
QueryJob using cursor-based pagination via the `around` parameter.

Uses the FalconPy NGSIEM service class with OAuth2 authentication.
The pagination mechanism is identical to direct LogScale QueryJobs:
  1. Create a QueryJob and poll until done
  2. Collect the initial 200-event buffer
  3. If hasMoreEvents="true", use cursor-based `around` pagination to
     walk backward through time and collect remaining events

Usage:
    export FALCON_CLIENT_ID="your-client-id"
    export FALCON_CLIENT_SECRET="your-client-secret"
    **OPTIONAL: export FALCON_BASE_URL="" # e.g. "https://api.us-2.crowdstrike.com" — leave empty for US-1
    python ngsiem_queryjob_paginator.py

Requirements:
    pip install crowdstrike-falconpy
"""

import json
import os
import sys
import time

from falconpy import NGSIEM

# ── Configuration ──────────────────────────────────────────────────────
REPO = "search-all"  # search-all | investigate_view | third-party | falcon_for_it_view | forensics_view
QUERY_STRING = "#event_simpleName=ProcessRollup2 | tail(500)"
START = "15m"
END = "now"
BASE_URL = os.environ.get("FALCON_BASE_URL", "")

PAGE_SIZE = 500
MAX_EVENTS = 0      # 0 = unlimited
OUTPUT_FILE = "ngsiem_queryjob_results.json"

# SSL: set to CA bundle path for corporate proxy, or False to skip verification
SSL_VERIFY = os.environ.get("CA_BUNDLE") or False
# ──────────────────────────────────────────────────────────────────────

CLIENT_ID = os.environ.get("FALCON_CLIENT_ID")
CLIENT_SECRET = os.environ.get("FALCON_CLIENT_SECRET")
if not CLIENT_ID or not CLIENT_SECRET:
    sys.exit("Error: set FALCON_CLIENT_ID and FALCON_CLIENT_SECRET environment variables")

ngsiem_kwargs = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "ssl_verify": SSL_VERIFY,
}
if BASE_URL:
    ngsiem_kwargs["base_url"] = BASE_URL

ngsiem = NGSIEM(**ngsiem_kwargs)


def start_search(around: dict | None = None) -> str:
    kwargs = {
        "repository": REPO,
        "query_string": QUERY_STRING,
        "start": START,
        "end": END,
        "is_live": False,
    }
    if around:
        kwargs["around"] = around

    resp = ngsiem.start_search(**kwargs)
    if resp["status_code"] != 200:
        sys.exit(f"Failed to start search: {resp}")
    return resp["resources"]["id"]


def poll_until_done(job_id: str) -> dict:
    while True:
        resp = ngsiem.get_search_status(repository=REPO, id=job_id)
        if resp["status_code"] == 404:
            return {"done": True, "events": [], "metaData": {}}
        if resp["status_code"] != 200:
            sys.exit(f"Poll failed ({resp['status_code']}): {resp}")

        resources = resp.get("resources") or resp.get("body", {})
        if resources.get("done", False):
            return resources

        wait_ms = resources.get("metaData", {}).get("pollAfter", 500)
        time.sleep(wait_ms / 1000.0)


def main():
    print(f"Query:  {QUERY_STRING}")
    print(f"Repo:   {REPO}")
    print(f"Range:  {START} → {END}")
    print()

    # Step 1: Initial query
    job_id = start_search()
    print(f"QueryJob created: {job_id}")

    data = poll_until_done(job_id)
    meta = data.get("metaData", {})
    has_more = meta.get("extraData", {}).get("hasMoreEvents", "false")
    processed = meta.get("processedEvents", "?")

    all_events: list[dict] = list(data.get("events", []))
    seen_ids: set[str] = {e.get("@id", "") for e in all_events}

    print(f"  Initial buffer: {len(all_events)} events  "
          f"(processedEvents={processed}  hasMoreEvents={has_more})")

    # Step 2: Cursor pagination using `around`
    # LogScale returns newest events first; the last event in the buffer is
    # the oldest. Anchor on it and request numberOfEventsBefore to walk
    # backward through time.
    page = 0
    while has_more == "true" and all_events:
        if MAX_EVENTS and len(all_events) >= MAX_EVENTS:
            all_events = all_events[:MAX_EVENTS]
            break

        oldest = all_events[-1]
        anchor_id = oldest.get("@id", "")
        anchor_ts = oldest.get("@timestamp")
        if not anchor_id or anchor_ts is None:
            break

        page += 1
        cursor_job_id = start_search(around={
            "eventId": anchor_id,
            "timestamp": int(anchor_ts),
            "numberOfEventsBefore": PAGE_SIZE,
            "numberOfEventsAfter": 0,
        })

        cursor_data = poll_until_done(cursor_job_id)
        events = cursor_data.get("events", [])
        new_events = [e for e in events if e.get("@id", "") not in seen_ids]

        if not new_events:
            break

        for e in new_events:
            seen_ids.add(e.get("@id", ""))
        all_events.extend(new_events)

        print(f"  page {page}: +{len(new_events)} events  (total: {len(all_events)})")
        time.sleep(0.5)

    if MAX_EVENTS and len(all_events) > MAX_EVENTS:
        all_events = all_events[:MAX_EVENTS]

    print(f"\nDone. {len(all_events)} total events.")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_events, f, indent=2)
    print(f"Results written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
