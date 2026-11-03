---
title: "Mining EndOfProcess and Profiling Programs"
date: 2021-10-05
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/qna2ao/20211005_cool_query_friday_mining_endofprocess/"
mitre: []
series: Cool Query Friday
---

# Mining EndOfProcess and Profiling Programs

> Source: [https://www.reddit.com/r/crowdstrike/comments/qna2ao/20211005_cool_query_friday_mining_endofprocess/](https://www.reddit.com/r/crowdstrike/comments/qna2ao/20211005_cool_query_friday_mining_endofprocess/) — by Andrew-CS (CrowdStrike) — 2021-10-05

Welcome to our thirtieth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
index=main sourcetype=EndOfProcess* event_platform=win event_simpleName=EndOfProcess
| head 1
| fields *_decimal
```

## Query 2
```cql
[...]
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName
| eval FileName=lower(FileName)
```

## Query 3
```cql
[...]
| search FileName=powershell.exe
```

## Query 4
```cql
index=main sourcetype=EndOfProcess* event_platform=win event_simpleName=EndOfProcess ImageSubsystem_decimal=3
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName
| eval FileName=lower(FileName) 
| search FileName=powershell.exe
```

## Query 5
```cql
[...]
| fields cid, aid, TargetProcessId_decimal, SHA256HashData, FileName, ScreenshotsTakenCount_decimal, NewExecutableWrittenCount_decimal
```

## Query 6
```cql
[...]
| stats dc(aid) as endpointSampleSize, count(aid) as executionSampleSize, max(NewExecutableWrittenCount_decimal) as maxExeWritten, median(NewExecutableWrittenCount_decimal) as medianExeWritten, avg(NewExecutableWrittenCount_decimal) as avgExeWritten, stdev(NewExecutableWrittenCount_decimal) as stdevExeWritten, max(ScreenshotsTakenCount_decimal) as maxSST, median(ScreenshotsTakenCount_decimal) as medianSST, avg(ScreenshotsTakenCount_decimal) as avgSST, stdev(ScreenshotsTakenCount_decimal) as stdevSST by FileName
```

## Query 7
```cql
index=main sourcetype=EndOfProcess* event_platform=win event_simpleName=EndOfProcess ImageSubsystem_decimal=3
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName
| eval FileName=lower(FileName) 
| search FileName=powershell.exe
| fields cid, aid, TargetProcessId_decimal, SHA256HashData, FileName, ScreenshotsTakenCount_decimal, NewExecutableWrittenCount_decimal 
| search ScreenshotsTakenCount_decimal>0 OR NewExecutableWrittenCount_decimal>=2
```

## Query 8
```cql
[...]
| search ScreenshotsTakenCount_decimal>0 OR (NewExecutableWrittenCount_decimal>=2 AND NewExecutableWrittenCount_decimal!=27 AND NewExecutableWrittenCount_decimal!=28)
```

## Query 9
```cql
[...]
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName as cloudFileName
```

## Query 10
```cql
[...]
| eval cloudFileName=lower(cloudFileName) 
| search cloudFileName=powershell.exe
```

## Query 11
```cql
[...]
| search event_simpleName=ProcessRollup2 OR (event_simpleName=EndOfProcess AND ScreenshotsTakenCount_decimal>0 OR (NewExecutableWrittenCount_decimal>=2 AND NewExecutableWrittenCount_decimal!=27 AND NewExecutableWrittenCount_decimal!=28))
```

## Query 12
```cql
[...]
| stats dc(event_simpleName) as eventCount, earliest(ProcessStartTime_decimal) as procStartTime, values(ComputerName) as computerName, values(UserName) as userName, values(UserSid_readable) as userSid, values(FileName) as fileName, values(cloudFileName) as cloudFileName, values(CommandLine) as cmdLine, values(ScreenshotsTakenCount_decimal) as screenShotsTaken, values(NewExecutableWrittenCount_decimal) as ExesWritten by aid, TargetProcessId_decimal
| where eventCount>1
```

## Query 13
```cql
[...]
| table aid, computerName, userSid, userName, TargetProcessId_decimal, fileName, cloudFileName, ExesWritten, screenShotsTaken, cmdLine
| rename TargetProcessId_decimal as falconPID
```

## Query 14
```cql
(index=main sourcetype=EndOfProcess* event_platform=win event_simpleName=EndOfProcess ImageSubsystem_decimal=3) OR (index=main sourcetype=ProcessRollup2* event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3)
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName as cloudFileName
| eval cloudFileName=lower(cloudFileName) 
| search cloudFileName=powershell.exe
| search event_simpleName=ProcessRollup2 OR (event_simpleName=EndOfProcess AND ScreenshotsTakenCount_decimal>0 OR (NewExecutableWrittenCount_decimal>=2 AND NewExecutableWrittenCount_decimal!=27 AND NewExecutableWrittenCount_decimal!=28))
| stats dc(event_simpleName) as eventCount, earliest(ProcessStartTime_decimal) as procStartTime, values(ComputerName) as computerName, values(UserName) as userName, values(UserSid_readable) as userSid, values(FileName) as fileName, values(cloudFileName) as cloudFileName, values(CommandLine) as cmdLine, values(ScreenshotsTakenCount_decimal) as screenShotsTaken, values(NewExecutableWrittenCount_decimal) as ExesWritten by aid, TargetProcessId_decimal
| where eventCount>1
| table aid, computerName, userSid, userName, TargetProcessId_decimal, fileName, cloudFileName, ExesWritten, screenShotsTaken, cmdLine
| rename TargetProcessId_decimal as falconPID
```
