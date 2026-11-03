---
title: "setTimeInterval()"
date: 2026-05-01
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1t0zcsz/20260501_cool_query_friday_settimeinterval/"
mitre: []
series: Cool Query Friday
---

# setTimeInterval()

> Source: [https://www.reddit.com/r/crowdstrike/comments/1t0zcsz/20260501_cool_query_friday_settimeinterval/](https://www.reddit.com/r/crowdstrike/comments/1t0zcsz/20260501_cool_query_friday_settimeinterval/) — by Andrew-CS (CrowdStrike) — 2026-05-01

Welcome to our ninetieth installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
setTimeInterval(start="7d")
| my-search-here
```

## Query 2
```cql
setTimeInterval(start="7d@d", end="1d@d", timezone="EST")
| my-search-here
```

## Query 3
```cql
setTimeInterval(start=1746054000000, end=1746780124517)
| my-search-here
```

## Query 4
```cql
setTimeInterval(start="1h")
| defineTable(
  start=24h,
  end=1h,
  query={event_platform=Win #event_simpleName=DnsRequest ContextBaseFileName="powershell.exe"},
  include=[DomainName, ContextBaseFileName],
  name="ps_dns")
| event_platform=Win #event_simpleName=DnsRequest ContextBaseFileName="powershell.exe"
| !match(table="ps_dns", field=DomainName, strict=true)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Q&A

**Q — [Community] dial647:** I have a question. I am trying to run a query for a 7 day period, and want the results when I have more than x number of events within a 10 mins time frame. Is it possible to achieve this using this statement?

**A — [CS] Andrew-CS:** Hi there. You’d want to use slidingTimeWindow(). We have a writeup on that [here](https://www.reddit.com/r/crowdstrike/s/KcZ1lzf6L4).
