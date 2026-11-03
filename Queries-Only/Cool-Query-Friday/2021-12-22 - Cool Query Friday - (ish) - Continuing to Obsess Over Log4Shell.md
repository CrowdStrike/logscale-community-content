---
title: "(ish) - Continuing to Obsess Over Log4Shell"
date: 2021-12-22
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/rmgjli/20211222_cool_query_fridayish_continuing_to/"
mitre: []
series: Cool Query Friday
---

# (ish) - Continuing to Obsess Over Log4Shell

> Source: [https://www.reddit.com/r/crowdstrike/comments/rmgjli/20211222_cool_query_fridayish_continuing_to/](https://www.reddit.com/r/crowdstrike/comments/rmgjli/20211222_cool_query_fridayish_continuing_to/) — by Andrew-CS (CrowdStrike) — 2021-12-22

Welcome to our thirty-third installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
index=main sourcetype=ProcessRollup2* event_simpleName=ProcessRollup2
| search ComputerName IN (*), ParentBaseFileName IN (java, java.exe)
| stats dc(aid) as uniqueEndpoints, count(aid) as executionCount by event_platform, ParentBaseFileName, FileName
| sort +event_platform, -executionCount
```

## Query 2
```cql
[...]
| search event_platform IN (Mac), ComputerName IN (MD-*), ParentBaseFileName IN (java, java.exe)
[...]
```

## Query 3
```cql
index=main sourcetype=ProcessRollup2* event_simpleName=ProcessRollup2
| search event_platform IN (Mac), ComputerName IN (MD-*), ParentBaseFileName IN (java, java.exe)
| stats dc(aid) as uniqueEndpoints, count(aid) as executionCount by event_platform, ParentBaseFileName, FileName
| search NOT FileName IN (jspawnhelper, who, users)
| sort +event_platform, -executionCount
```

## Query 4
```cql
event_simpleName=CustomIOABasicProcessDetectionInfoEvent TemplateInstanceId_decimal=26 
|  stats dc(aid) as endpointCount count(aid) as alertCount by ParentImageFileName, ImageFileName, CommandLine
| sort - alertCount
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Q&A

**Q — [Community] jmcybersec:** The github log4j scanning script references a cast.exe file, but there is a 404 when i attempt to download and it doesn't show up anywhere on there? Any ideas what happened to this?

**A — [CS] Andrew-CS:** Hi there. If you download this file from Git and decompress it you'll get `cast.exe`: https://github.com/CrowdStrike/CAST/releases/download/v0.6.0/cast\_0.6.0\_Windows\_amd64.tar.gz
