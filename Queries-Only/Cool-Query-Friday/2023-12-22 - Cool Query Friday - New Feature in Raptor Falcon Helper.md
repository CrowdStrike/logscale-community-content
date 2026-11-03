---
title: "New Feature in Raptor: Falcon Helper"
date: 2023-12-22
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/18off35/20231222_cool_query_friday_new_feature_in_raptor/"
mitre: []
series: Cool Query Friday
---

# New Feature in Raptor: Falcon Helper

> Source: [https://www.reddit.com/r/crowdstrike/comments/18off35/20231222_cool_query_friday_new_feature_in_raptor/](https://www.reddit.com/r/crowdstrike/comments/18off35/20231222_cool_query_friday_new_feature_in_raptor/) — by Andrew-CS (CrowdStrike) — 2023-12-22

Welcome to our seventy-first installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
#event_simpleName=UserLogon
| case {
        LogonType = "2"  | LogonType := "Interactive" ;
        LogonType = "3"  | LogonType := "Network" ;
        LogonType = "4"  | LogonType := "Batch" ;
        LogonType = "5"  | LogonType := "Service" ;
        LogonType = "6"  | LogonType := "Proxy" ;
        LogonType = "7"  | LogonType := "Unlock" ;
        LogonType = "8"  | LogonType := "Network Cleartext" ;
        LogonType = "9"  | LogonType := "New Credential" ;
        LogonType = "10" | LogonType := "Remote Interactive" ;
        LogonType = "11" | LogonType := "Cached Interactive" ;
        LogonType = "12" | LogonType := "Cached Remote Interactive" ;
        LogonType = "13" | LogonType := "Cached Unlock" ; 
        * }
| table([@timestamp, aid, ComputerName, UserName, LogonType])
```

## Query 2
```cql
#event_simpleName=UserLogon
| $falcon/helper:enrich(field=LogonType)
| table([@timestamp, aid, ComputerName, UserName, LogonType])
```

## Query 3
```cql
| $falcon/helper:enrich(field=FIELD)
```

## Query 4
```cql
#event_simpleName=ProcessRollup2 event_platform=Win
| select([@timestamp, aid, ComputerName, FileName, UserName, UserSid, TokenType, IntegrityLevel, ImageSubsystem])
```

## Query 5
```cql
#event_simpleName=ProcessRollup2 event_platform=Win
| select([@timestamp, aid, ComputerName, FileName, UserName, UserSid, TokenType, IntegrityLevel, ImageSubsystem])
| $falcon/helper:enrich(field=IntegrityLevel)
| $falcon/helper:enrich(field=TokenType)
| $falcon/helper:enrich(field=ImageSubsystem)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
#event_simpleName=UserLogon
| $falcon/helper:enrich(field=LogonType)
| table([@timestamp, aid, ComputerName, UserName, LogonType], limit=20000)
```
— [CS] Andrew-CS · comment score 2

```cql
| readFile("falcon/helper/mappings.csv")
| groupBy([Event])
```
— [CS] Andrew-CS · comment score 2

```cql
| _1 := ?field
| format("%s_%s", field=[_1, ?field], as=_3)
| match(field=_3, column=Key, include=[KeyValue], strict=false, file="mappings.csv")
| rename(KeyValue, as=?field)
| drop([_1, _2, _3, KeyValue])
```
— [CS] Andrew-CS · comment score 3

```cql
| $helper(field=LogonType)
```
— [CS] Andrew-CS · comment score 3

```cql
#event_simpleName=UserLogon LogonType=/^(2|10)$/
| tail(10)
| $helper(field=LogonType)
| $helper(field=UserIsAdmin)
| table([@timestamp, aid, ComputerName, UserName, UserIsAdmin, LogonType])
```
— [CS] Andrew-CS · comment score 3

```cql
| rootURL := "https://falcon.crowdstrike.com/"
| format("[Graph Explorer](%sgraphs/process-explorer/graph?id=pid:%s:%s)", field=["rootURL", "aid", "TargetProcessId"], as="Graph Explorer")
```
— [CS] Andrew-CS · comment score 2

```cql
#event_simpleName=ProcessRollup2 
| tail(10)
| rootURL := "https://falcon.crowdstrike.com/"
| format("[Graph Explorer](%sgraphs/process-explorer/graph?id=pid:%s:%s)", field=["rootURL",
"aid", "TargetProcessId"], as="Graph Explorer") 
| select([aid, ComputerName, FileName, "Graph Explorer"])
```
— [CS] Andrew-CS · comment score 2

```cql
#event_simpleName=ProcessRollup2 
| tail(10)
| select([aid, ComputerName, FileName])
| rootURL := "https://falcon.crowdstrike.com/"
| format("[Graph Explorer](%sgraphs/process-explorer/graph?id=pid:%s:%s)", field=["rootURL", "aid", "TargetProcessId"], as="Graph Explorer")
```
— [CS] Andrew-CS · comment score 2

```cql
#event_simpleName=DnsRequest 
| tail(10)
| rootURL := "https://falcon.crowdstrike.com/"
| format("[Graph Explorer](%sgraphs/process-explorer/graph?id=pid:%s:%s)", field=["rootURL", "aid", "ContextProcessId"], as="Graph Explorer") 
| select([aid, ComputerName, ContextBaseFileName, DomainName, "Graph Explorer"])
```
— [CS] Andrew-CS · comment score 2

```cql
| join({#data_source_name=cid_name | groupBy([cid], function=selectFromMax(field="@timestamp", include=[name]))}, field=cid, include=name, mode=left)
```
— [CS] Andrew-CS · comment score 2

```cql
#event_simpleName=ProcessRollup2
| tail(1)
| table([cid, aid, ComputerName, FileName, CommandLine])
| $getCID()
```
— [CS] Andrew-CS · comment score 2

```cql
#data_source_name=*
| groupBy(#data_source_name)
```
— [CS] Andrew-CS · comment score 1

### Q&A

**Q — [Community] vim_enthusiast:** If you ingest Falcon data to your own on-prem/cloud Splunk is it possible to install Falcon Helper somewhere?

**A — [CS] Andrew-CS:** Hi there. There is not. I don't know of a way to recreate this using SpQL based on how that query language works.

**Q — [Community] AlphaDomain:** Yup that worked and this is totally awesome and helpful. One more question as I am still a newbie, how would I throw in a limit=max. I am having trouble getting past the 200 elements by default limit when I remove the tail function.

**A — [CS] Andrew-CS:** | table([@timestamp, aid, ComputerName, UserName, UserIsAdmin, LogonType], limit=20000) That should do it!
