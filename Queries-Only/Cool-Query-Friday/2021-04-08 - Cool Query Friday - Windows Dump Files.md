---
title: "Windows Dump Files"
date: 2021-04-08
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/mngo2l/20210408_cool_query_friday_windows_dump_files/"
mitre: []
series: Cool Query Friday
---

# Windows Dump Files

> Source: [https://www.reddit.com/r/crowdstrike/comments/mngo2l/20210408_cool_query_friday_windows_dump_files/](https://www.reddit.com/r/crowdstrike/comments/mngo2l/20210408_cool_query_friday_windows_dump_files/) — by Andrew-CS (CrowdStrike) — 2021-04-08

Welcome to our sixth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
event_platform=win (event_simpleName=ProcessRollup2 OR event_simpleName=SyntheticProcessRollup2) AND FileName=werfault.exe
| stats dc(aid) as endpointCount count(aid) as crashCount by ParentBaseFileName
| sort - crashCount
| rename ParentBaseFileName as crashingProgram
```

## Query 2
```cql
| sort + crashCount
```

## Query 3
```cql
event_platform=win (event_simpleName=ProcessRollup2 OR event_simpleName=SyntheticProcessRollup2) AND FileName=werfault.exe
| rare ParentBaseFileName limit=25
```

## Query 4
```cql
event_platform=win (event_simpleName=ProcessRollup2 OR event_simpleName=SyntheticProcessRollup2) AND FileName=werfault.exe
| common ParentBaseFileName limit=25
```

## Query 5
```cql
(event_simpleName=ProcessRollup2 OR event_simpleName=SyntheticProcessRollup2) AND FileName=WerFault.exe AND ParentBaseFileName=prunsrv-amd64.exe
| rename TargetProcessId_decimal AS ContextProcessId_decimal, FileName as crashProcessor, ParentBaseFileName as crashingProgram, RawProcessId_decimal as osPID
| join aid, ContextProcessId_decimal 
    [search event_simpleName=DmpFileWritten]
```

## Query 6
```cql
(event_simpleName=ProcessRollup2 OR event_simpleName=SyntheticProcessRollup2) AND FileName=WerFault.exe AND ParentBaseFileName=prunsrv-amd64.exe
| rename TargetProcessId_decimal AS ContextProcessId_decimal, FileName as crashProcessor, ParentBaseFileName as crashingProgram, RawProcessId_decimal as osPID
| join aid, ContextProcessId_decimal 
    [search event_simpleName=DmpFileWritten]
| table timestamp aid ComputerName UserName crashProcessor crashingProgram TargetFileName ContextProcessId_decimal, osPID
| sort + timestamp
| eval timestamp=timestamp/1000
| convert ctime(timestamp)
| rename ComputerName as endpointName, UserName as userName, TargetFileName as dmpFile, ContextTimeStamp_decimal, as crashTime, ContextProcessId_decimal as falconPID
```
