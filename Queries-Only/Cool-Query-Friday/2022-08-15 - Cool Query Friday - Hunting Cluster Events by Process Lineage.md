---
title: "Hunting Cluster Events by Process Lineage"
date: 2022-08-15
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/woz73a/20220815_cool_query_friday_hunting_cluster_events/"
mitre: []
series: Cool Query Friday
---

# Hunting Cluster Events by Process Lineage

> Source: [https://www.reddit.com/r/crowdstrike/comments/woz73a/20220815_cool_query_friday_hunting_cluster_events/](https://www.reddit.com/r/crowdstrike/comments/woz73a/20220815_cool_query_friday_hunting_cluster_events/) — by Andrew-CS (CrowdStrike) — 2022-08-15

Welcome to our forty-sixth installment of[ Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
[...]
| stats dc(FileName) as fnameCount, earliest(ProcessStartTime_decimal) as firstRun, latest(ProcessStartTime_decimal) as lastRun, values(FileName) as filesRun, values(CommandLine) as cmdsRun by cid, aid, ComputerName, ParentBaseFileName, ParentProcessId_decimal
```

## Query 2
```cql
[...]
| where fnameCount > 3
```

## Query 3
```cql
[...]
| where fnameCount>=9
```

## Query 4
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName IN (whoami.exe, arp.exe, cmd.exe, net.exe, net1.exe, ipconfig.exe, route.exe, netstat.exe, nslookup.exe)
| stats dc(FileName) as fnameCount, earliest(ProcessStartTime_decimal) as firstRun, latest(ProcessStartTime_decimal) as lastRun, values(FileName) as filesRun, values(CommandLine) as cmdsRun by cid, aid, ComputerName, ParentBaseFileName, ParentProcessId_decimal
| where fnameCount > 3
```

## Query 5
```cql
[...]
| eval timeDelta=lastRun-firstRun
| where timeDelta < 600
```

## Query 6
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName IN (whoami.exe, arp.exe, cmd.exe, net.exe, net1.exe, ipconfig.exe, route.exe, netstat.exe, nslookup.exe)
| stats dc(FileName) as fnameCount, earliest(ProcessStartTime_decimal) as firstRun, latest(ProcessStartTime_decimal) as lastRun, values(FileName) as filesRun, values(CommandLine) as cmdsRun by cid, aid, ComputerName, ParentBaseFileName, ParentProcessId_decimal
| where fnameCount > 3
| eval timeDelta=lastRun-firstRun
| where timeDelta < 600
```

## Query 7
```cql
[...]
| eval graphExplorer=case(ParentProcessId_decimal!="","https://falcon.crowdstrike.com/graphs/process-explorer/tree?id=pid:".aid.":".ParentProcessId_decimal)
| table cid, aid, ComputerName, ParentBaseFileName, filesRun, cmdsRun, timeDelta, graphExplorer
```

## Query 8
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName IN (whoami.exe, arp.exe, cmd.exe, net.exe, net1.exe, ipconfig.exe, route.exe, netstat.exe, nslookup.exe)
| stats dc(FileName) as fnameCount, earliest(ProcessStartTime_decimal) as firstRun, latest(ProcessStartTime_decimal) as lastRun, values(FileName) as filesRun, values(CommandLine) as cmdsRun by cid, aid, ComputerName, ParentBaseFileName, ParentProcessId_decimal
| where fnameCount > 3
| eval timeDelta=lastRun-firstRun
| where timeDelta < 600
| eval graphExplorer=case(ParentProcessId_decimal!="","https://falcon.crowdstrike.com/graphs/process-explorer/tree?id=pid:".aid.":".ParentProcessId_decimal)
| table cid, aid, ComputerName, ParentBaseFileName, filesRun, cmdsRun, timeDelta, graphExplorer
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Q&A

**Q — [Community] animatedgoblin:** During general alert reviews we noticed that the above query has a bit of a problem we _think_ we understand, but would like some clarity. Let's say for sake of example, we have fNameCount set to >3, and a time delta of 600. Now, let's say that we have a PowerShell process that is created at 12:00 a …

**A — [CS] Andrew-CS:** That does make sense and you are absolutely correct. The results will be affected by the `lastRun` time — which in your example puts `timeDelta` at 53 minutes. In the example article, we were working under the assumption that the tradecraft was programatic so we *should* be able to detect it with some time-boxing, however, if it where hands-on-keyboard and the timing were varied (because humans) we might want to make it time OR count. So something like "more than 5 of these things happen in my s …

**Q — [Community] animatedgoblin:** >more than 5 of these things happen in my search window That's super simple logic I hadn't considered! How would one implement that? Would it be something as simple as ``` | eval timeDelta=lastRun-firstRun | where (fnameCount > 3 AND timeDelta < 600) OR fnameCount > 5 ``` ?

**A — [CS] Andrew-CS:** Yup! Your idea to use `bucket` and then set your `span` to 10, 15, whatever minutes is also a good one as that will *chunck* up the rows in the given increments.
