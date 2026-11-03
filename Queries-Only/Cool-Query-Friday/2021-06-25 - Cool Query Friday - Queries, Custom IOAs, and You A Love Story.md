---
title: "Queries, Custom IOAs, and You: A Love Story"
date: 2021-06-25
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/o7nvts/20210625_cool_query_friday_queries_custom_ioas/"
mitre: []
series: Cool Query Friday
---

# Queries, Custom IOAs, and You: A Love Story

> Source: [https://www.reddit.com/r/crowdstrike/comments/o7nvts/20210625_cool_query_friday_queries_custom_ioas/](https://www.reddit.com/r/crowdstrike/comments/o7nvts/20210625_cool_query_friday_queries_custom_ioas/) — by Andrew-CS (CrowdStrike) — 2021-06-25

Welcome to our fifteenth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName=powershell.exe ProductType=3 
| stats  dc(aid) as endpointCount count(aid) as executionCount by ParentBaseFileName, FileName  
| sort  - executionCount
```

## Query 2
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName=powershell.exe ProductType=3 
| lookup aid_policy.csv aid OUTPUT groups
| eval groups=replace(groups, "'", "\"")
| spath input=groups output=group_id path={}
| mvexpand group_id
| lookup group_info.csv group_id OUTPUT name 
| stats  dc(aid) as endpointCount count(aid) as executionCount by ParentBaseFileName, FileName, name  
| sort  - executionCount
```

## Query 3
```cql
event_simpleName=CustomIOABasicProcessDetectionInfoEvent TemplateInstanceId_decimal=226 
|  stats dc(aid) as endpointCount count(aid) as alertCount by ParentImageFileName
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
event_platform=win event_simpleName=ProcessRollup2 FileName=powershell.exe ProductType=3
| lookup local=true aid_policy.csv aid OUTPUT groups
| eval groups=replace(groups, "'", "\"")
| spath input=groups output=group_id path={}
| mvexpand group_id
| lookup local=true group_info.csv group_id OUTPUT name
| stats dc(aid) as endpointCount count(aid) as executionCount by ParentBaseFileName, FileName, name
| sort - executionCount
```
— [CS] Andrew-CS · comment score 2
