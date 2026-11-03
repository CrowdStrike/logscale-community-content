---
title: "Coalesce"
date: 2021-09-24
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/puj8w6/20210924_cool_query_friday_coalesce/"
mitre: []
series: Cool Query Friday
---

# Coalesce

> Source: [https://www.reddit.com/r/crowdstrike/comments/puj8w6/20210924_cool_query_friday_coalesce/](https://www.reddit.com/r/crowdstrike/comments/puj8w6/20210924_cool_query_friday_coalesce/) — by Andrew-CS (CrowdStrike) — 2021-09-24

Welcome to our twenty-fourth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
aid=7ce9db2ac1da4e8fb116e494a8c77a2d 253714948641
| table ProcessStartTime_decimal, ContextTimeStamp_decimal, event_simpleName, FileName, CommandLine, DomainName, RespondingDnsServer
```

## Query 2
```cql
aid=7ce9db2ac1da4e8fb116e494a8c77a2d 253714948641
| eval falconPID=coalesce(TargetProcessId_decimal, ContextProcessId_decimal)
| eval details1=coalesce(FileName, DomainName, ExitCode_decimal)
| eval details2=coalesce(CommandLine, RespondingDnsServer)
```

## Query 3
```cql
aid=7ce9db2ac1da4e8fb116e494a8c77a2d 253714948641
| eval falconPID=coalesce(TargetProcessId_decimal, ContextProcessId_decimal)
| eval details1=coalesce(FileName, DomainName, ExitCode_decimal)
| eval details2=coalesce(CommandLine, RespondingDnsServer)
| table _time aid ComputerName falconPID event_simpleName details1 details2
| sort + _time
```

## Query 4
```cql
aid=7ce9db2ac1da4e8fb116e494a8c77a2d 253714948641
| eval falconPID=coalesce(TargetProcessId_decimal, ContextProcessId_decimal)
| eval details1=coalesce(FileName, DomainName, ExitCode_decimal)
| eval details2=coalesce(CommandLine, RespondingDnsServer)
| table _time aid ComputerName falconPID event_simpleName details1 details2
| sort + _time
| rename aid AS "Falcon AID", ComputerName AS "Endpoint", falconPID as "Falcon PID", event_simpleName AS "Falcon Event", details1 AS "Process Details 1", details2 AS "ProcessDetails 2"
```

## Query 5
```cql
aid=d61cc3e207fb4ef08e8b941d9b4feaa8 (TargetProcessId_decimal=1357691323426 OR ContextProcessId_decimal=1357691323426) AND (event_simpleName IN (ProcessRollup2, EndofProcess, DnsRequest, NetworkConnectIP4, *FileWritten, Asep*))
| eval Size_MB=round(Size_decimal/1024/1024,2)
| eval falconPID=coalesce(TargetProcessId_decimal, ContextProcessId_decimal)
| eval details1=coalesce(FileName, DomainName, ExitCode_decimal, RemoteIP, RegObjectName)
| eval details2=coalesce(CommandLine, RespondingDnsServer, Size_MB, RPort, RegValue, RegOperationType_decimal)
| eval details3=coalesce(Protocol_decimal, FilePath, RegStringValue)
| table _time aid ComputerName falconPID event_simpleName details1 details2 details3
| sort + _time
| rename aid AS "Falcon AID", ComputerName AS "Endpoint", falconPID as "Falcon PID", event_simpleName AS "Falcon Event", details1 AS "Process Details 1", details2 AS "Process Details 2", details3 AS "Process Details 3"
```
