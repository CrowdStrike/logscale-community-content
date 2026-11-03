---
title: "(mini) - The Triumphant Return of aid_master as a File"
date: 2024-06-03
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1d76iro/20240603_cool_query_friday_mini_the_triumphant/"
mitre: []
series: Cool Query Friday
---

# (mini) - The Triumphant Return of aid_master as a File

> Source: [https://www.reddit.com/r/crowdstrike/comments/1d76iro/20240603_cool_query_friday_mini_the_triumphant/](https://www.reddit.com/r/crowdstrike/comments/1d76iro/20240603_cool_query_friday_mini_the_triumphant/) — by Andrew-CS (CrowdStrike) — 2024-06-03

Welcome to our seventy-fourth-and-a-half installment (there are no rules, here!) of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
| inputlookup aid_master
```

## Query 2
```cql
| readFile(aid_master_main.csv)
```

## Query 3
```cql
| readFile(aid_master_details.csv)
```

## Query 4
```cql
#event_simpleName=ProcessRollup2 event_platform=Win
| tail(10)
| match(file="aid_master_main.csv", field=aid, include=[AgentVersion, Version], ignoreCase=true, strict=false)
| table([aid, Computername, TargetProcessId, FileName, AgentVersion, Version])
```

## Query 5
```cql
| match(file="aid_master_main.csv", field=aid, include=[AgentVersion, Version], ignoreCase=true, strict=false)
```

## Query 6
```cql
#event_simpleName=ProcessRollup2 event_platform=Win
| tail(10)
| aid =~ match(file="aid_master_main.csv", column=aid, strict=false)
| table([aid, Computername, TargetProcessId, FileName, AgentVersion, Version])
```

## Query 7
```cql
| aid =~ match(file="aid_master_main.csv", column=aid, strict=false)
```

## Query 8
```cql
#event_simpleName=ProcessRollup2 event_platform=Win
| tail(10)
| aid =~ match(file="aid_master_main.csv", column=aid, strict=false)
| table([aid, Computername, TargetProcessId, FileName, AgentVersion, Version, MAC, ProductType])
```

## Query 9
```cql
| readFile("aid_master_main.csv")
| test(FirstSeen>(now()-604800000))
| FirstSeen:=formatTime(format="%F %F", field="FirstSeen")
```

## Query 10
```cql
#event_simpleName=UserLogon
| groupBy([aid, ComputerName], function=([selectFromMax(field="@timestamp", include=[UserName])]))
| match(file="aid_master_details.csv", field=aid, include=[SystemSerialNumber], ignoreCase=true, strict=false)
| rename(field="UserName", as="LastLoggedOnUser")
```

## Query 11
```cql
#event_simpleName=DnsRequest DomainName=/github.com$/i
| match(file="aid_master_main.csv", field=aid, include=[ProductType, Version], ignoreCase=true, strict=false)
| in(field="ProductType", values=[2,3])
| groupBy([aid, ComputerName, ContextBaseFileName], function=([collect([ProductType, Version, DomainName])]))
| $falcon/helper:enrich(field=ProductType)
```
