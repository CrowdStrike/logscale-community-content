---
title: "Falcon Fusion Friday"
date: 2021-08-20
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/p8d0rl/20210820_cool_query_friday_falcon_fusion_friday/"
mitre: []
series: Cool Query Friday
---

# Falcon Fusion Friday

> Source: [https://www.reddit.com/r/crowdstrike/comments/p8d0rl/20210820_cool_query_friday_falcon_fusion_friday/](https://www.reddit.com/r/crowdstrike/comments/p8d0rl/20210820_cool_query_friday_falcon_fusion_friday/) — by Andrew-CS (CrowdStrike) — 2021-08-20

Welcome to our twenty-second installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

```cql
earliest=-90d ExternalApiType=Event_DetectionSummaryEvent Tactic="Credential Access"
| rename AgentIdString as aid
| lookup local=true aid_master aid OUTPUT Version, ProductType
| where ProductType=1
| stats count(aid) as totalDetections dc(aid) as totalEndpoints values(Version) as osVersions by FileName
| sort - totalDetections
```
