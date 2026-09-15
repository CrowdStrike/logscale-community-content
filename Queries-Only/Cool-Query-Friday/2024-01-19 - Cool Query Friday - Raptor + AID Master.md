---
title: "Raptor + AID Master"
date: 2024-01-19
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/19akavg/20240119_cool_query_friday_raptor_aid_master/"
mitre: []
series: Cool Query Friday
---

# Raptor + AID Master

> Source: [https://www.reddit.com/r/crowdstrike/comments/19akavg/20240119_cool_query_friday_raptor_aid_master/](https://www.reddit.com/r/crowdstrike/comments/19akavg/20240119_cool_query_friday_raptor_aid_master/) — by Andrew-CS (CrowdStrike) — 2024-01-19

Welcome to our seventy-second installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
| inputlookup aid_master
```

## Query 2
```cql
event_simpleName=ProcessRollup2
| head 5
| table aid, ComputerName, UserName, FileName
| lookup local=true aid_master aid OUTPUT Version
```

## Query 3
```cql
// Enter aid_master repository
#repo=sensor_metadata #data_source_name=aidmaster

// Fill blank FalconGroupingTags fields with a dash
| default(value="-", field=[FalconGroupingTags], replaceEmpty=true)

// For every aid, output the latest values for ComputerName, Version, AgentVersion, FalconGroupingTags
| groupBy([aid], function=([selectFromMax(field="@timestamp", include=[ComputerName, Version, AgentVersion, FalconGroupingTags])]))
```

## Query 4
```cql
// Enter aid_master repository for Windows systems
#repo=sensor_metadata #data_source_name=aidmaster event_platform=Win

// For every aid, output the latest values for event_platform, Version
| groupBy([aid], function=([selectFromMax(field="@timestamp", include=[Version])]))

// Aggregate for chart creation
| groupBy([Version])
```

## Query 5
```cql
#event_simpleName=ProcessRollup2 
| tail(5)
| table([aid, ComputerName, UserName, FileName])
| join(query={#repo=sensor_metadata #data_source_name=aidmaster | groupBy([aid], function=([selectFromMax(field="@timestamp", include=[Version])]))
}, field=[aid], include=[Version])
```

## Query 6
```cql
| join(query={#repo=sensor_metadata #data_source_name=aidmaster | groupBy([aid], function=([selectFromMax(field="@timestamp", include=[Version])]))
}, field=[aid], include=[Version])
```

## Query 7
```cql
#event_simpleName=ProcessRollup2
| tail(5)
| table([aid, ComputerName, UserName, FileName])
| join(query={#repo=sensor_metadata #data_source_name=aidmaster | groupBy([aid], function=([selectFromMax(field="@timestamp", include=[AgentVersion, Version, FirstSeen, Time])]))
}, field=[aid], include=[AgentVersion, Version, FirstSeen, Time])
| FirstSeen:=FirstSeen*1000 | FirstSeen:=formatTime(format="%F %T", field="FirstSeen")
| rename(field="Time", as="LastSeen")
```

## Query 8
```cql
| join(query={#repo=sensor_metadata #data_source_name=aidmaster | groupBy([aid], function=([selectFromMax(field="@timestamp", include=[AgentVersion, Version, FirstSeen, Time])]))
}, field=[aid], include=[AgentVersion, Version, FirstSeen, Time])
```

## Query 9
```cql
#repo=sensor_metadata #data_source_name=aidmaster event_platform=Win
| groupBy([aid], function=([selectFromMax(field="@timestamp", include=[AgentVersion, @timestamp])]))
| timeChart(AgentVersion, function=count(aid),span=1d, limit=10)
```

## Query 10
```cql
#repo=sensor_metadata #data_source_name=aidmaster event_platform=Lin
| groupBy([aid], function=([selectFromMax(field="@timestamp", include=[Version])]))
| groupBy([Version])
```

## Query 11
```cql
#repo=sensor_metadata #data_source_name=aidmaster FalconGroupingTags!=""
| groupBy([aid], function=([selectFromMax(field="@timestamp", include=[ComputerName]), collect([FalconGroupingTags], multival=false)]))
| sankey(source="ComputerName", target="FalconGroupingTags", weight=count(aid))
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
//| in(name, values=[NeighborListIP4V2, NeighborListIP4MacV1])
```
— [CS] Andrew-CS · comment score 1

```cql
| $falcon/investigate:not_managed()
```
— [CS] Andrew-CS · comment score 1

```cql
#repo=base_sensor #event_simpleName=ImageHash FileName=cellulardatacapabilityhandler.dll
| join(query={#repo=sensor_metadata #data_source_name=aidmaster 
| groupBy([aid], function=selectLast(AgentVersion), limit=max)} , field=[aid], include=[AgentVersion]) 
| table(fields=["aid","AgentVersion","FileName"])
```
— [CS] Andrew-CS · comment score 1

### Q&A

**Q — [Community] 65c0aedb:** How do you enrich events with `ComputerName` based on `aid` when you have more than 100000 hosts in `aid_master` ? Here my `groupBy` are yielding all sorts of warnings about chopped data, and a random number of `ComputerName` get outputted each time, usually 0 or 1. I sorted out my situation by pick …

**A — [CS] Andrew-CS:** You would want to override the default `groupBy` limit. #repo=base_sensor #event_simpleName=ImageHash FileName=cellulardatacapabilityhandler.dll | join(query={#repo=sensor_metadata #data_source_name=aidmaster | groupBy([aid], function=selectLast(AgentVersion), limit=max)} , field=[aid], include=[AgentVersion]) | table(fields=["aid","AgentVersion","FileName"])
