---
title: "Historic MITRE ATT&CK Footprint Data"
date: 2020-03-19
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/m8gpto/20200319_cool_query_friday_historic_mitre_attck/"
mitre: []
series: Cool Query Friday
---

# Historic MITRE ATT&CK Footprint Data

> Source: [https://www.reddit.com/r/crowdstrike/comments/m8gpto/20200319_cool_query_friday_historic_mitre_attck/](https://www.reddit.com/r/crowdstrike/comments/m8gpto/20200319_cool_query_friday_historic_mitre_attck/) — by Andrew-CS (CrowdStrike) — 2020-03-19

Welcome to our third installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/?f=flair_name%3A%22CQF%22). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
earliest=-365d ExternalApiType=Event_DetectionSummaryEvent 
| stats dc(AgentIdString) as uniqueEndpoints count(AgentIdString) as detectionCount by Tactic, Technique
| sort - detectionCount
```

## Query 2
```cql
earliest=-365d ExternalApiType=Event_DetectionSummaryEvent 
| stats dc(AgentIdString) as uniqueEndpoints count(AgentIdString) as detectionCount by Tactic, Technique
| eval detectsPerEndpoint=round(detectionCount/uniqueEndpoints,0)
| sort - detectionCount
```

## Query 3
```cql
earliest=-365d ExternalApiType=Event_DetectionSummaryEvent 
| timechart count(AgentIdString) as detectionCount by Tactic span=1month
| sort + _time
```

## Query 4
```cql
earliest=-7d@d ExternalApiType=Event_DetectionSummaryEvent 
| timechart count(AgentIdString) as detectionCount by Tactic span=1d
| sort + _time
```

## Query 5
```cql
earliest=-1month ExternalApiType=Event_DetectionSummaryEvent 
| timechart count(AgentIdString) as detectionCount by Tactic span=1w
| sort + _time
```

## Query 6
```cql
earliest=-1month ExternalApiType=Event_DetectionSummaryEvent MachineDomain="acme.co"
| timechart count(AgentIdString) as detectionCount by Tactic span=1w
| sort + _time
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
ExternalApiType=Event_DetectionSummaryEvent 
| rename AgentIdString AS aid | lookup local=true aid_master aid OUTPUT aip | iplocation aip | geostats latfield=lat longfield=lon count by Tactic
```
— [CS] Andrew-CS · comment score 3

### Q&A

**Q — [Community] MaxSecurity:** Do you know if Sub-Technique is plan to be add by Crowdstrike in the log ?

**A — [CS] Andrew-CS:** Yup! https://supportportal.crowdstrike.com/s/article/Tech-Alert-1st-Notice-MITRE-ATT-CK-Framework-Changes-in-31-Days
