---
title: "CLI Programs Running via Hidden Window"
date: 2021-07-16
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/olhnwf/20210716_cool_query_friday_cli_programs_running/"
mitre: []
series: Cool Query Friday
---

# CLI Programs Running via Hidden Window

> Source: [https://www.reddit.com/r/crowdstrike/comments/olhnwf/20210716_cool_query_friday_cli_programs_running/](https://www.reddit.com/r/crowdstrike/comments/olhnwf/20210716_cool_query_friday_cli_programs_running/) — by Andrew-CS (CrowdStrike) — 2021-07-16

Welcome to our seventeenth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
[...]
| rename FileName AS runningExe
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName FileDescription
| fillnull FileName, FileDescription value="N/A"
| eval cloudFileName=lower(FileName)
| eval FileName=lower(FileName)
```

## Query 2
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3 ShowWindowFlags_decimal=0
| rename FileName AS runningExe
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName FileDescription
| fillnull FileName, FileDescription value="N/A"
| eval runningExe=lower(runningExe)
| eval cloudFileName=lower(FileName)
| fields aid, ComputerName, runningExe cloudFileName, FileDescription
| rename FileDescription as cloudFileDescription
```

## Query 3
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3 ShowWindowFlags_decimal=0 UserSid_readable!=S-1-5-18
| rename FileName AS runningExe
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName FileDescription
| fillnull FileName, FileDescription value="N/A"
| eval runningExe=lower(runningExe)
| eval cloudFileName=lower(FileName)
| stats dc(aid) as systemCount count(aid) as runCount by runningExe, SHA256HashData, cloudFileName, FileDescription
| rename FileDescription as cloudFileDescription, SHA256HashData as sha256
| sort +systemCount, +runCount
```

## Query 4
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3 ShowWindowFlags_decimal=0 UserSid_readable!=S-1-5-18 FileName=powershell.exe
| rename FileName AS runningExe
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName FileDescription
| fillnull FileName, FileDescription value="N/A"
| eval runningExe=lower(runningExe)
| eval cloudFileName=lower(FileName)
| stats values(UserName) as userName dc(aid) as systemCount count(aid) as runCount by runningExe, CommandLine
| rename FileDescription as cloudFileDescription, SHA256HashData as sha256
| sort +systemCount, +runCount
```

## Query 5
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3 ShowWindowFlags_decimal=0 FileName=cmd.exe CommandLine="*powershell*"
| rename FileName AS runningExe
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName FileDescription
| fillnull FileName, FileDescription value="N/A"
| eval runningExe=lower(runningExe)
| eval cloudFileName=lower(FileName)
| stats values(UserName) as userName dc(aid) as systemCount count(aid) as runCount by runningExe, CommandLine
| rename FileDescription as cloudFileDescription, SHA256HashData as sha256
| sort +systemCount, +runCount
```
