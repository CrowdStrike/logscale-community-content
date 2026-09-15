---
title: "Windows T1087.001 - When You're Bored, Go Overboard"
date: 2023-04-07
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/12enf8y/20230407_cool_query_friday_windows_t1087001_when/"
mitre: [T1087, T1087.001]
series: Cool Query Friday
---

# Windows T1087.001 - When You're Bored, Go Overboard

> Source: [https://www.reddit.com/r/crowdstrike/comments/12enf8y/20230407_cool_query_friday_windows_t1087001_when/](https://www.reddit.com/r/crowdstrike/comments/12enf8y/20230407_cool_query_friday_windows_t1087001_when/) — by Andrew-CS (CrowdStrike) — 2023-04-07

Welcome to our fifty-sixth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
| CommandLine=/\s+(?<netCommand>(accounts|computer|config|continue|file|group|help|helpmsg|localgroup|name|pause|print|send|session|share|start|statistics|stop|time|use|user|view))\s+(?<netArguments>.+)/i
```

## Query 2
```cql
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\net1?\.exe/i
| CommandLine=/\s+(?<netCommand>(accounts|computer|config|continue|file|group|help|helpmsg|localgroup|name|pause|print|send|session|share|start|statistics|stop|time|use|user|view))\s+(?<netArguments>.+)/i
| select([netCommand, netArguments])
```

## Query 3
```cql
| regex("(?<netFlag>\/\w+)(\s+|\:|$)", field=netArguments, strict=false, repeat=true)
```

## Query 4
```cql
| CommandLine=/\s+(?<netCommand>(accounts|computer|config|continue|file|group|help|helpmsg|localgroup|name|pause|print|send|session|share|start|statistics|stop|time|use|user|view))\s+(?<netArguments>.+)/i
| regex("(?<netFlag>\/\w+)(\s+|\:|$)", field=netArguments, strict=false, repeat=true)
| default(value="none", field=[netFlag])
| select([netCommand, netFlag, netArguments])
```

## Query 5
```cql
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\(?<FileName>net1?\.exe)/i
| CommandLine=/\s+(?<netCommand>(accounts|computer|config|continue|file|group|help|helpmsg|localgroup|name|pause|print|send|session|share|start|statistics|stop|time|use|user|view))\s+(?<netArguments>.+)/i
| regex("(?<netFlag>\/\w+)(\s+|\:|$)", field=netArguments, strict=false, repeat=true)
| default(value="none", field=[netFlag])
| netCommand=?netCommand netFlag=?netFlag
| rootURL := "https://falcon.crowdstrike.com/"
| format("[Process Explorer](%sinvestigate/process-explorer/%s/%s)", field=["rootURL", "aid", "TargetProcessId"], as="Process Explorer")
| groupBy([ProcessStartTime, aid, FileName, netCommand, netArguments], function=collect([netFlag, "Process Explorer"]))
| select([ProcessStartTime, aid, FileName, netCommand, netFlag, netArguments, "Process Explorer"])
| ProcessStartTime := ProcessStartTime*1000 | formatTime(format="%F %T.%L", field="ProcessStartTime", as="ProcessStartTime")
```

## Query 6
```cql
| netCommand=?netCommand netFlag=?netFlag
```

## Query 7
```cql
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\net1?\.exe/i
| CommandLine=/\s+(?<netCommand>(accounts|computer|config|continue|file|group|help|helpmsg|localgroup|name|pause|print|send|session|share|start|statistics|stop|time|use|user|view))\s+(?<netArguments>.+)/i
| lower("netArguments") | lower("netCommand")
| regex("(?<netFlag>\/\w+)(\s+|\:|$)", field=netArguments, strict=false, repeat=true)
| lower("netFlag") 
| groupBy([netFlag])
```

## Query 8
```cql
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\(?<FileName>net1?\.exe)/i
| CommandLine=/\s+(?<netCommand>(accounts|computer|config|continue|file|group|help|helpmsg|localgroup|name|pause|print|send|session|share|start|statistics|stop|time|use|user|view))\s+(?<netArguments>.+)/i
| regex("(?<netFlag>\/\w+)(\s+|\:|$)", field=netArguments, strict=false, repeat=true)
| default(value="none", field=[netFlag])
| netCommand=?netCommand netFlag=?netFlag
| sankey(source="netCommand", target="netFlag", weight=count(aid))
```

## Query 9
```cql
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\(?<FileName>net1?\.exe)/i
| CommandLine=/\s+(?<netCommand>(accounts|computer|config|continue|file|group|help|helpmsg|localgroup|name|pause|print|send|session|share|start|statistics|stop|time|use|user|view))\s+(?<netArguments>.+)/i
| regex("(?<netFlag>\/\w+)(\s+|\:|$)", field=netArguments, strict=false, repeat=true)
| default(value="none", field=[netFlag])
| netCommand=?netCommand netFlag=?netFlag
| groupBy([netCommand])
```

## Query 10
```cql
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\(?<FileName>net1?\.exe)/i
| CommandLine=/\s+(?<netCommand>(accounts|computer|config|continue|file|group|help|helpmsg|localgroup|name|pause|print|send|session|share|start|statistics|stop|time|use|user|view))\s+(?<netArguments>.+)/i
| regex("(?<netFlag>\/\w+)(\s+|\:|$)", field=netArguments, strict=false, repeat=true)
| default(value="none", field=[netFlag])
| netCommand=?netCommand netFlag=?netFlag
| timeChart(netCommand, span=1d)
```
