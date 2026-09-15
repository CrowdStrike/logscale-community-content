---
title: "Scoping Discovery Via the net Command and Custom IOAs (T1087.001)"
date: 2021-08-06
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/oz7uvn/20210806_cool_query_friday_scoping_discovery_via/"
mitre: [T1087]
series: Cool Query Friday
---

# Scoping Discovery Via the net Command and Custom IOAs (T1087.001)

> Source: [https://www.reddit.com/r/crowdstrike/comments/oz7uvn/20210806_cool_query_friday_scoping_discovery_via/](https://www.reddit.com/r/crowdstrike/comments/oz7uvn/20210806_cool_query_friday_scoping_discovery_via/) — by Andrew-CS (CrowdStrike) — 2021-08-06

Welcome to our twentieth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
aid=7ce9db2ac1da4e8fb116e494a8c77a2d 65327048864
| eval endpointTime=mvappend(ContextTimeStamp_decimal, ProcessStartTime_decimal) 
| table endpointTime ComputerName UserName FileName CommandLine event_simpleName RawProcessId_decimal TargetProcessId_decimal ContextProcessId_decimal RpcClientProcessId_decimal
| sort + endpointTime
| convert ctime(endpointTime)
```

## Query 2
```cql
earliest=-7d event_platform=win event_simpleName=ProcessRollup2 (FileName=net.exe OR FileName=net1.exe)
| stats dc(aid) as uniqueEndpoints count(aid) as executionCount dc(CommandLine) as cmdLineVariations by FileName, ProductType
| sort + ProductType
```

## Query 3
```cql
earliest=-7d event_platform=win event_simpleName=ProcessRollup2 (FileName=net.exe OR FileName=net1.exe) CommandLine="* user *"
| stats values(CommandLine) as cmdLineVariations
```

## Query 4
```cql
earliest=-7d event_platform=win event_simpleName=ProcessRollup2 (FileName=net.exe OR FileName=net1.exe) CommandLine="* user *"
| search CommandLine="* /add*"
| stats values(CommandLine) as cmdLineVariations
```

## Query 5
```cql
earliest=-7d event_platform=win event_simpleName=ProcessRollup2 (FileName=net.exe OR FileName=net1.exe) CommandLine="* user *"
| search CommandLine="* /add*"
| stats dc(aid) as uniqueEndpoints count(aid) as executionCount values(CommandLine) as cmdLines by ProductType
```
