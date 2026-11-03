---
title: "Hunting AI Tools, Models, Services, Agents, and SDKs with Falcon for IT"
date: 2026-04-24
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1suff2t/20260424_cool_query_friday_hunting_ai_tools/"
mitre: []
series: Cool Query Friday
---

# Hunting AI Tools, Models, Services, Agents, and SDKs with Falcon for IT

> Source: [https://www.reddit.com/r/crowdstrike/comments/1suff2t/20260424_cool_query_friday_hunting_ai_tools/](https://www.reddit.com/r/crowdstrike/comments/1suff2t/20260424_cool_query_friday_hunting_ai_tools/) — by Andrew-CS (CrowdStrike) — 2026-04-24

Welcome to our eighty-ninth installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

```cql
| groupBy([aid, _tools_f, _models_f, _mcp_f, _sdks_f, _agents_f, _total], function=[], limit=max)
| match(file="aid_master_main.csv", field=[aid], column=aid)
| formatTime(format="%F %T %Z", as="FirstSeen", field=FirstSeen)
| formatTime(format="%F %T %Z", as="LastSeen", field=LastSeen)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
| groupBy([aid, _tools_f, _models_f, _mcp_f, _sdks_f, _agents_f, _total], function=[], limit=max)
| match(file="aid_master_main.csv", field=[aid], column=aid)
| match(file="aid_master_details.csv", field=[aid], column=[aid], include=[SensorGroupingTags, FalconGroupingTags])
| formatTime(format="%F %T %Z", as="FirstSeen", field=FirstSeen)
| formatTime(format="%F %T %Z", as="LastSeen", field=LastSeen)
```
— [CS] Andrew-CS · comment score 1

### Operational caveats

> Hi there. I mean, Falcon for IT is executing the scripts using RTR... but if you initiate the scripts on your own the script output wouldn't be sent anywhere. A lot of the magic is the redirection of STDOUT back to Falcon and then putting it in a curated format. So... yes, could definitely be done... but would require a lot more elbow grease.
— [CS] Andrew-CS · score 1

### Q&A

**Q — [Community] OddFly6060:** | groupBy([aid, _tools_f, _models_f, _mcp_f, _sdks_f, _agents_f, _total], function=[], limit=max) | match(file="aid_master_main.csv", field=[aid], column=aid) | formatTime(format="%F %T %Z", as="FirstSeen", field=FirstSeen) | formatTime(format="%F %T %Z", as="LastSeen", field=LastSeen) How could I a …

**A — [CS] Andrew-CS:** Hi there. You would need just one more line... | groupBy([aid, _tools_f, _models_f, _mcp_f, _sdks_f, _agents_f, _total], function=[], limit=max) | match(file="aid_master_main.csv", field=[aid], column=aid) | match(file="aid_master_details.csv", field=[aid], column=[aid], include=[SensorGroupingTags, FalconGroupingTags]) | formatTime(format="%F %T %Z", as="FirstSeen", field=FirstSeen) | formatTime(format="%F %T %Z", as="LastSeen", field=LastSeen)

**Q — [Community] Gullible-PvM:** Is there a way to leverage these scripts through RTR/Fusion to do ad-hoc collections?

**A — [CS] Andrew-CS:** Hi there. I mean, Falcon for IT is executing the scripts using RTR... but if you initiate the scripts on your own the script output wouldn't be sent anywhere. A lot of the magic is the redirection of STDOUT back to Falcon and then putting it in a curated format. So... yes, could definitely be done... but would require a lot more elbow grease.
