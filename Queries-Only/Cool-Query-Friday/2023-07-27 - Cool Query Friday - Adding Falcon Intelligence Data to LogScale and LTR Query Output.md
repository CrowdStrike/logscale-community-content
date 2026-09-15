---
title: "Adding Falcon Intelligence Data to LogScale and LTR Query Output"
date: 2023-07-27
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/15b3nyu/20230727_cool_query_friday_adding_falcon/"
mitre: []
series: Cool Query Friday
---

# Adding Falcon Intelligence Data to LogScale and LTR Query Output

> Source: [https://www.reddit.com/r/crowdstrike/comments/15b3nyu/20230727_cool_query_friday_adding_falcon/](https://www.reddit.com/r/crowdstrike/comments/15b3nyu/20230727_cool_query_friday_adding_falcon/) — by Andrew-CS (CrowdStrike) — 2023-07-27

Welcome to our fifty-ninth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
| falconPID:=TargetProcessId | falconPID:=ContextProcessId
```

## Query 2
```cql
| falconPID:=concat([TargetProcessId,ContextProcessId])
```

## Query 3
```cql
| case { 
    #event_simpleName=ProcessRollup2| ImageFileName=/(\\Device\\HarddiskVolume\d+|\/)?(?<FilePath>(\\|\/).+(\\|\/))(?<FileName>.+)$/i | FileName:=lower("FileName");
    #event_simpleName=DnsRequest | ioc:lookup(field=[DomainName], type="domain");
    *;
    }
```

## Query 4
```cql
| selfJoinFilter(field=[aid, falconPID], where=[{#event_simpleName=ProcessRollup2 FileName=?FileName}, {#event_simpleName=DnsRequest ioc.detected=true}])
```

## Query 5
```cql
| groupBy([aid, falconPID], function=([count(#event_simpleName, distinct=true, as=eventCount), collect([ContextTimeStamp, DomainName, ioc[0].labels, UserSid, FileName, FilePath, CommandLine])]))
| eventCount>1
```

## Query 6
```cql
(#event_simpleName=ProcessRollup2 aid=?aid) OR (#event_simpleName=DnsRequest DomainName=?DomainName)
| falconPID:=TargetProcessId | falconPID:=ContextProcessId
| case {
    #event_simpleName=ProcessRollup2| ImageFileName=/(\\Device\\HarddiskVolume\d+|\/)?(?<FilePath>(\\|\/).+(\\|\/))(?<FileName>.+)$/i | FileName:=lower("FileName");
    #event_simpleName=DnsRequest | ioc:lookup(field=[DomainName], type="domain");
    *;
    }
| selfJoinFilter(field=[aid, falconPID], where=[{#event_simpleName=ProcessRollup2 FileName=?FileName}, {#event_simpleName=DnsRequest ioc.detected=true}])
| groupBy([aid, falconPID], function=([count(#event_simpleName, distinct=true, as=eventCount), collect([ContextTimeStamp, DomainName, ioc[0].labels, UserSid, FileName, FilePath, CommandLine])]))
| eventCount>1
```

## Query 7
```cql
| falcon_intel:=replace(field="ioc[0].labels", regex="\,", with="\n")
| falcon_intel:=replace(field="falcon_intel", regex="\/", with=": ")
```

## Query 8
```cql
| ContextTimeStamp:=ContextTimeStamp*1000 | ContextTimeStamp:=formatTime(format="%F %T.%L", field="ContextTimeStamp")
| Details:=format(format="\tTime:\t%s\nAgent ID:\t%s\nUser SID:\t%s\n\tFile:\t%s\n\tPath:\t%s\nCmd Line:\t%s\n\n", field=[ContextTimeStamp, aid, UserSid, FileName, FilePath, CommandLine])
```

## Query 9
```cql
// Un-comment one rootURL value
| rootURL := "https://falcon.crowdstrike.com/" /* US-1 */
//| rootURL := "https://falcon.us-2.crowdstrike.com/" /* US-2 */
//| rootURL := "https://falcon.laggar.gcw.crowdstrike.com/" /* Gov */
//| rootURL := "https://falcon.eu-1.crowdstrike.com/" /* EU */
| format("[Graph Explorer](%sgraphs/process-explorer/graph?id=pid:%s:%s)", field=["rootURL", "aid", "falconPID"], as="Graph Explorer")
```

## Query 10
```cql
| rename(field="Details", as="Execution Details")
| rename(field="DomainName", as="IOC")
| rename(field="falcon_intel", as="Falcon Intelligence")
| select([IOC, "Falcon Intelligence", "Execution Details", "Graph Explorer"])
```

## Query 11
```cql
(#event_simpleName=ProcessRollup2 aid=?aid) OR (#event_simpleName=DnsRequest DomainName=?DomainName)
| falconPID:=TargetProcessId | falconPID:=ContextProcessId
| case{ 
    #event_simpleName=ProcessRollup2| ImageFileName=/(\\Device\\HarddiskVolume\d+|\/)?(?<FilePath>(\\|\/).+(\\|\/))(?<FileName>.+)$/i | FileName:=lower("FileName");
    #event_simpleName=DnsRequest | ioc:lookup(field=[DomainName], type="domain");
    *;
    }
| selfJoinFilter(field=[aid, falconPID], where=[{#event_simpleName=ProcessRollup2 FileName=?FileName}, {#event_simpleName=DnsRequest ioc.detected=true}])
| groupBy([aid, falconPID], function=([count(#event_simpleName, distinct=true, as=eventCount), collect([ContextTimeStamp, DomainName, ioc[0].labels, UserSid, FileName, FilePath, CommandLine])]))
| eventCount>1
| falcon_intel:=replace(field="ioc[0].labels", regex="\,", with="\n")
| falcon_intel:=replace(field="falcon_intel", regex="\/", with=": ")
| ContextTimeStamp:=ContextTimeStamp*1000 | ContextTimeStamp:=formatTime(format="%F %T.%L", field="ContextTimeStamp")
| Details:=format(format="\tTime:\t%s\nAgent ID:\t%s\nUser SID:\t%s\n\tFile:\t%s\n\tPath:\t%s\nCmd Line:\t%s\n\n", field=[ContextTimeStamp, aid, UserSid, FileName, FilePath, CommandLine])
// Un-comment one rootURL value
| rootURL  := "https://falcon.crowdstrike.com/" /* US-1 */
//| rootURL  := "https://falcon.us-2.crowdstrike.com/" /* US-2 */
//| rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/" /* Gov */
//| rootURL  := "https://falcon.eu-1.crowdstrike.com/"  /* EU */
| format("[Graph Explorer](%sgraphs/process-explorer/graph?id=pid:%s:%s)", field=["rootURL", "aid", "falconPID"], as="Graph Explorer") 
| rename(field="Details", as="Execution Details")
| rename(field="DomainName", as="IOC")
| rename(field="falcon_intel", as="Falcon Intelligence")
| select([IOC, "Falcon Intelligence", "Execution Details", "Graph Explorer"])
```
