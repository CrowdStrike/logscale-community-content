---
title: "Stats"
date: 2021-06-04
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/ns4k9q/20210604_cool_query_friday_stats/"
mitre: []
series: Cool Query Friday
---

# Stats

> Source: [https://www.reddit.com/r/crowdstrike/comments/ns4k9q/20210604_cool_query_friday_stats/](https://www.reddit.com/r/crowdstrike/comments/ns4k9q/20210604_cool_query_friday_stats/) — by Andrew-CS (CrowdStrike) — 2021-06-04

Welcome to our thirteenth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
[...]
| stats function(field) as outputName by field
```

## Query 2
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName=PowerShell.exe
| stats count(aid) as psExecutionCount by FileName
```

## Query 3
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName=PowerShell.exe
| stats count(aid) as psExecutionCount dc(aid) as uniqueSystemCount by FileName
```

## Query 4
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName=PowerShell.exe
| stats count(aid) as psExecutionCount dc(aid) as uniqueSystemCount earliest(ProcessStartTime_decimal) as earliestExecution latest(ProcessStartTime_decimal) as latestExecution by FileName
```

## Query 5
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName=PowerShell.exe
| stats count(aid) as psExecutionCount dc(aid) as uniqueSystemCount earliest(ProcessStartTime_decimal) as earliestExecution latest(ProcessStartTime_decimal) as latestExecution by FileName
| convert ctime(earliestExecution) ctime(latestExecution)
```

## Query 6
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName=PowerShell.exe
| stats count(aid) as psExecutionCount dc(aid) as uniqueSystemCount earliest(ProcessStartTime_decimal) as earliestExecution latest(ProcessStartTime_decimal) as latestExecution values(ComputerName) as endpointHostnames by FileName
| convert ctime(earliestExecution) ctime(latestExecution)
```

## Query 7
```cql
| stats sum(NumberField) as mySumOutput
```

## Query 8
```cql
| stats avg(NumberField) as myAvgOutput
```

## Query 9
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName=PowerShell.exe
| stats count(aid) as psExecutionCount dc(aid) as uniqueSystemCount earliest(ProcessStartTime_decimal) as earliestExecution latest(ProcessStartTime_decimal) as latestExecution values(ComputerName) as endpointHostnames by aid
| convert ctime(earliestExecution) ctime(latestExecution)
| sort - psExecutionCount
```

## Query 10
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName=PowerShell.exe
| stats count(aid) as psExecutionCount dc(aid) as uniqueSystemCount earliest(ProcessStartTime_decimal) as earliestExecution latest(ProcessStartTime_decimal) as latestExecution values(ComputerName) as endpointHostnames by SHA256HashData
| convert ctime(earliestExecution) ctime(latestExecution)
| sort - psExecutionCount
```

## Query 11
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName=PowerShell.exe
| stats count(aid) as psExecutionCount dc(aid) as uniqueSystemCount earliest(ProcessStartTime_decimal) as earliestExecution latest(ProcessStartTime_decimal) as latestExecution values(ComputerName) as endpointHostnames by ParentBaseFileName 
| convert ctime(earliestExecution) ctime(latestExecution)
| sort - psExecutionCount
```
