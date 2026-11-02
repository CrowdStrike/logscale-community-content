---
title: QueryJobs API Pagination
created: 2026-04-29
updated: 2026-05-11
tags: [logscale, ngsiem, api, python, pagination]
---

# QueryJobs API Pagination

## Overview

The LogScale/NG-SIEM QueryJobs API returns a **200-event result buffer** for filter (non-aggregate) queries. To retrieve all matching events, you must use **cursor-based pagination** via the `around` parameter.

Scripts: 
`queryjob_paginator.py` (direct LogScale) 
`ngsiem_queryjob_paginator.py` (FalconPy/NG-SIEM)

## Script Usage

### LogScale (direct API)

```bash
# One-time setup
cd _LogScale/script
python3 -m venv .venv
source .venv/bin/activate
pip install requests

# Environment variables (required)
export LOGSCALE_TOKEN="your-api-token"
export LOGSCALE_BASE_URL="https://your-logscale-instance.com/"
export LOGSCALE_REPO="your-repo-name"

# Run (wrap query in single quotes to preserve double quotes in CQL)
python queryjob_paginator.py -q '#event_simpleName=ProcessRollup2'

# With double quotes in the query
python queryjob_paginator.py -q '#event_simpleName=ProcessRollup2 | groupBy([aid], function=[count(as="Event Count")]) | sort("Event Count", limit=max)'

# Optional flags
python queryjob_paginator.py -q '...' -s 1h -e now -o results.json --max-events 5000 --page-size 200

# Help
python queryjob_paginator.py -h
```

**Parameters:**

| Flag | Description | Default |
|------|--------------|----------|
| `-q, --query` | CQL query string (required) | — |
| `-s, --start` | Start time | `15m` |
| `-e, --end` | End time | `now` |
| `-o, --output` | Output JSON file | `queryjob_results.json` |
| `--max-events` | Max events to retrieve | unlimited |
| `--page-size` | Events per cursor page | `200` |



### NG-SIEM (FalconPy)

```bash
# One-time setup (same venv)
pip install crowdstrike-falconpy

# Environment variables (required — or use -k/-s flags)
export FALCON_CLIENT_ID="your-client-id"
export FALCON_CLIENT_SECRET="your-client-secret"

# Optional environment variables
export FALCON_BASE_URL="https://api.us-2.crowdstrike.com"  # defaults to US-1
export FALCON_MEMBER_CID="child-cid"                       # for MSSP / flight control
export CA_BUNDLE="/path/to/ca-bundle.pem"                  # for corporate proxy

# Run
python ngsiem_queryjob_paginator.py -q '#event_simpleName=ProcessRollup2'

# With options
python ngsiem_queryjob_paginator.py -q '...' -r search-all --start 1h --end now
python ngsiem_queryjob_paginator.py -q '...' -b https://api.us-2.crowdstrike.com
python ngsiem_queryjob_paginator.py -q '...' -m CHILD_CID  # MSSP

# Help
python ngsiem_queryjob_paginator.py -h
```

**Parameters:**

| Flag | Env Var | Description | Default |
|------|---------|-------------|---------|
| `-k, --client-id` | `FALCON_CLIENT_ID` | OAuth2 client ID (required) | — |
| `-s, --client-secret` | `FALCON_CLIENT_SECRET` | OAuth2 client secret (required) | — |
| `-q, --query` | — | CQL query string (required) | — |
| `-r, --repo` | — | NG-SIEM repository | `search-all` |
| `--start` | — | Start time | `15m` |
| `--end` | — | End time | `now` |
| `-o, --output` | — | Output JSON file | `ngsiem_queryjob_results.json` |
| `--max-events` | — | Max events to retrieve | unlimited |
| `--page-size` | — | Events per cursor page | `200` |
| `-b, --base-url` | `FALCON_BASE_URL` | CrowdStrike API base URL | US-1 |
| `-m, --member-cid` | `FALCON_MEMBER_CID` | Child CID (MSSP / flight control) | — |

Required API scope: **NGSIEM: Read + Write**

## How QueryJobs Work

1. **Create** a QueryJob → returns a job ID
2. **Poll** (GET) → returns up to 200 events + metadata
3. **Check metadata** → `hasMoreEvents="true"` means more events exist beyond the buffer
4. **Paginate** using the `around` parameter to walk through remaining events

## Key Metadata Fields

| Field | Meaning |
|-------|---------|
| `metaData.resultBufferSize` | Events in the buffer (default 200 for filter queries) |
| `metaData.eventCount` | Number of events in current result set |
| `metaData.processedEvents` | Total matching events found by the query |
| `metaData.extraData.hasMoreEvents` | `"true"` (string!) if results exceed buffer |
| `metaData.isAggregate` | Aggregate queries return all results in one shot |
| `metaData.pollAfter` | Milliseconds to wait before next poll |

## Pagination Mechanisms

### 1. Offset/Limit (within the buffer only)

Query parameters on the GET poll request:
- `?paginationLimit=50&paginationOffset=0` — page within the 200-event buffer
- Only useful for paging within what's already buffered, **not** for getting more events

### 2. Cursor-Based (`around` parameter) — for results beyond the buffer

The `around` parameter creates a new QueryJob anchored on a specific event:

```json
{
  "queryString": "#event_simpleName=ProcessRollup2",
  "start": "15m",
  "end": "now",
  "around": {
    "eventId": "@id of anchor event",
    "timestamp": 1777469793821,
    "numberOfEventsBefore": 200,
    "numberOfEventsAfter": 0
  }
}
```

**Critical detail:** LogScale returns **newest events first**. The last event in the buffer is the **oldest**. To get more events, anchor on the oldest event and request `numberOfEventsBefore` (older events).

### 3. What Does NOT Work

- **Automatic cursor advancement** — the server does NOT track which segments you've consumed. Repeated polls return the same 200 events.
- **`dataspaces` endpoint** — legacy alias; use `/api/v1/repositories/` instead.
- **Offset/limit beyond the buffer** — `paginationOffset` only pages within `resultBufferSize`, not beyond it.

## Pagination Algorithm

```
1. Create QueryJob, poll until done=true
2. Collect initial 200 events
3. If hasMoreEvents="true":
   a. Take the LAST event (oldest, since results are newest-first)
   b. Create NEW QueryJob with `around`:
      - eventId = last event's @id
      - timestamp = last event's @timestamp
      - numberOfEventsBefore = 200
      - numberOfEventsAfter = 0
   c. Poll new job until done, collect events
   d. Deduplicate by @id (boundary event may repeat)
   e. Delete consumed QueryJob
   f. Repeat from (a) until no new events returned
```

## API Endpoints

### Direct LogScale
```
POST /api/v1/repositories/{repo}/queryjobs     — Create
GET  /api/v1/repositories/{repo}/queryjobs/{id} — Poll
DELETE /api/v1/repositories/{repo}/queryjobs/{id} — Cancel
```

### NG-SIEM (via CrowdStrike API gateway)
```
POST /humio/api/v1/repositories/{repo}/queryjobs     — Create
GET  /humio/api/v1/repositories/{repo}/queryjobs/{id} — Poll
DELETE /humio/api/v1/repositories/{repo}/queryjobs/{id} — Cancel
```

NG-SIEM repositories: `search-all`, `investigate_view`, `third-party`, `falcon_for_it_view`, `forensics_view`

## FalconPy Usage

```python
from falconpy import NGSIEM

with NGSIEM(client_id="...", client_secret="...") as ngsiem:
    if ngsiem.token_fail_reason:
        raise SystemExit(f"Auth failed: {ngsiem.token_fail_reason}")

    # Create
    resp = ngsiem.start_search(repository="search-all", query_string="...", start="1h", end="now")
    job_id = resp["resources"]["id"]

    # Poll (response is in resp["body"], not resp["resources"])
    resp = ngsiem.get_search_status(repository="search-all", id=job_id)
    data = resp.get("resources") or resp.get("body", {})
    events = data["events"]
    done = data["done"]

    # Cleanup
    ngsiem.stop_search(repository="search-all", id=job_id)
```

## Important Notes

- `hasMoreEvents` is a **string** (`"true"` / `"false"`), not a boolean
- `done=true` means the query finished, NOT that all results are delivered
- QueryJobs auto-delete after **90 seconds** of no polling
- Aggregate queries (`groupBy`, `count`, etc.) return all results in one response — no pagination needed
- Rate limit: 6000 concurrent query jobs per CID

## SSL / Corporate Proxy

For Zscaler environments, set `CA_BUNDLE` env var pointing to the CA certificate bundle. The FalconPy script reads this and passes it as `ssl_verify`. If unset, SSL verification is enabled by default.

## References

- [LogScale API — Query Jobs](https://library.humio.com/logscale-api/api-search-query.html)
- [LogScale API — Pagination](https://library.humio.com/logscale-api/api-search-pagination-api.html)
- [NG-SIEM Search APIs (CrowdStrike docs)](https://falcon.crowdstrike.com/documentation/page/bda96fc1)
